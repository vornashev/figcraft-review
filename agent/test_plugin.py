"""python3 -m unittest agent/test_plugin.py — the built plugin in a headless FigCraft.

Needs FIGCRAFT_TEST_FILE (a .figcraft to copy) and the module built:
cargo build --release --target wasm32-unknown-unknown
"""
import os
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import review  # noqa: E402
from fc import FC  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WASM = os.path.join(ROOT, "target/wasm32-unknown-unknown/release/figcraft_review.wasm")


@unittest.skipUnless(os.environ.get("FIGCRAFT_TEST_FILE") and os.path.exists(WASM), "set FIGCRAFT_TEST_FILE and build the plugin")
class Plugin(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        path = os.path.join(self.dir, "copy.figcraft")
        shutil.copy(os.environ["FIGCRAFT_TEST_FILE"], path)
        self.fc = FC(file=path)
        self.fc.cmd("plugin.import", path=ROOT)

    def tearDown(self):
        self.fc.p.kill()
        self.fc.p.wait()
        shutil.rmtree(self.dir)

    def run_command(self, _id, **params):
        return self.fc.tool("run_command", {"command": _id, "params": params})

    def event(self, control, value=None):
        """Use a panel control; the panel's controls afterwards, by name (notes as note<i>)."""
        self.run_command("plugin.event", id=review.PLUGIN, control=control, **({} if value is None else {"value": value}))
        ui = self.run_command("plugin.ui", id=review.PLUGIN)
        out = {c.get("name") or f"note{i}": c for i, c in enumerate(ui["controls"])}
        out["values"] = ui.get("values") or {}
        return out

    def notes(self):
        """num → (text, status, replies)."""
        out = {}
        for a in self.fc.cmd("annotation.list", page="all")["annotations"]:
            n = review.parse(a["label"])
            out[n["num"]] = (n["text"], (a.get("category") or {}).get("name"), n["replies"])
        return out

    def labels(self, ui):
        return [c["label"] for k, c in ui.items() if k.startswith("note")]

    def test_panel(self):
        tops = self.fc.tops()
        a, b = tops[0]["id"], tops[1]["id"]
        self.fc.cmd("annotation.add", id=a, label="Нативная")
        self.fc.cmd("select.set", ids=[b])
        r = self.run_command("plugin.run", id=review.PLUGIN, command="panel")
        self.assertEqual([c.get("name") for c in r["panel"]["controls"] if c.get("name")], ["text", "add", "selection", "items"])
        self.assertEqual(self.notes()[1][:2], ("Нативная", "Открыто"), "the panel numbers a native annotation")
        self.assertIn(f"«{tops[1]['name']}»", r["panel"]["controls"][0]["label"])

        self.fc.cmd("select.set", ids=[a])  # another layer: typing names it anew, the text stays
        ui = self.event("text", "Отступ слева больше")
        self.assertIn(f"«{tops[0]['name']}»", self.labels(ui)[0])
        self.assertIn("уже #1", self.labels(ui)[0])
        self.fc.cmd("select.set", ids=[b])
        ui = self.event("selection")
        self.assertIn(f"«{tops[1]['name']}»", self.labels(ui)[0])
        ui = self.event("add")
        self.assertEqual(self.notes()[2], ("Отступ слева больше", "Открыто", []))
        self.assertEqual(ui["values"].get("text"), "", "the field is cleared for the next remark")
        self.assertTrue(any("Добавлено #2" in t for t in self.labels(ui)))
        self.assertEqual(ui["add"]["label"], "Добавить #3")
        self.assertTrue(ui["values"]["items"].startswith("○ #2 · "), "the new remark is picked")

        ui = self.event("items", next(o for o in ui["items"]["options"] if "#1" in o))
        self.assertEqual(self.fc.doc(0)["selection"], [a], "a pick goes to the layer")
        ui = self.event("done")
        self.assertEqual(self.notes()[1][1], "Готово")
        self.assertIn("reopen", ui, "a done remark offers to reopen it")
        self.assertTrue(ui["items"]["options"][-1].startswith("✓ #1"), "done ones go last")
        self.event("reopen")
        self.assertEqual(self.notes()[1][1], "Открыто")
        self.event("items", next(o for o in ui["items"]["options"] if "#2" in o))
        self.event("remove")
        self.assertNotIn(2, self.notes())

    def test_widget_and_agent(self):
        tops = self.fc.tops()
        a, b = tops[0]["id"], tops[1]["id"]
        self.fc.cmd("annotation.add", id=a, label="#1 · Первое")
        self.fc.cmd("annotation.add", id=b, label="#2 · Второе")
        w = self.run_command("widget.insert", plugin=review.PLUGIN, x=0, y=-3000)
        self.assertEqual(sorted(t for t in w["targets"] if t.startswith("t.")), sorted([f"t.{a}.0", f"t.{b}.0"]))
        r = self.run_command("widget.click", id=w["id"], target=f"t.{b}.0")
        self.assertEqual(self.notes()[2][1], "Готово")
        self.assertEqual([t for t in r["targets"] if t.startswith("t.")], [f"t.{a}.0"], "done ones are hidden")
        r = self.run_command("widget.click", id=w["id"], target="done")
        self.assertTrue(r["state"]["showDone"])
        self.assertEqual(len([t for t in r["targets"] if t.startswith("t.")]), 2)
        self.run_command("widget.click", id=w["id"], target=f"o.{a}.{self.fc.doc(0)['currentPage']}")
        self.assertEqual(self.fc.doc(0)["selection"], [a])

        review.FC = lambda: self.fc  # the agent's side: a question, then the widget follows
        review.main(["ask", "1", "Насколько?"])
        self.assertEqual(self.notes()[1][1], "Вопрос")
        self.assertEqual(self.run_command("widget.list")["widgets"][0]["plugin"], review.PLUGIN)
        if os.environ.get("SHOT"):
            self.fc.shot(w["id"], os.environ["SHOT"], 700)

if __name__ == "__main__":
    unittest.main()
