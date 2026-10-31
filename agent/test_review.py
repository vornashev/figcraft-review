"""python3 -m unittest agent/test_review.py — labels, and the whole loop on a copy of a .figcraft file.

The loop runs only with FIGCRAFT_TEST_FILE set (a design to copy); FigCraft opens it headless.
"""
import contextlib
import io
import os
import shutil
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import review  # noqa: E402
from fc import FC  # noqa: E402


class Labels(unittest.TestCase):
    def test_round_trip(self):
        n = {"num": 7, "text": "Кнопка налезает", "replies": [("Claude", "увеличил padding"), ("Я", "ок")]}
        label = review.build(n)
        self.assertEqual(label, "#7 · Кнопка налезает\n↳ Claude: увеличил padding\n↳ Я: ок")
        self.assertEqual(review.parse(label), n)

    def test_native_and_odd_labels(self):
        p = review.parse
        self.assertEqual((p("Сделать крупнее")["num"], p("Сделать крупнее")["text"]), (None, "Сделать крупнее"))
        self.assertEqual(p(None)["text"], "")
        self.assertEqual(p("#3 · две\nстроки")["text"], "две\nстроки")
        self.assertEqual(p("#3 · a\n↳ Claude: x\ny")["replies"], [("Claude", "x\ny")])
        self.assertEqual(p("↳ not a reply: first line")["text"], "↳ not a reply: first line")

    def test_question_options(self):
        self.assertEqual(review.question("Как? · варианты: 1) Вид · ⋯; 2) Только «+»"), ("Как?", ["Вид · ⋯", "Только «+»"]))
        self.assertEqual(review.question("Просто вопрос"), ("Просто вопрос", []))

    def test_plural(self):
        self.assertEqual([review.plural(n, review.REMARKS) for n in (1, 3, 5, 11, 21, 22)],
                         ["1 замечание", "3 замечания", "5 замечаний", "11 замечаний", "21 замечание", "22 замечания"])


@unittest.skipUnless(os.environ.get("FIGCRAFT_TEST_FILE"), "set FIGCRAFT_TEST_FILE to a .figcraft file")
class Loop(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp()
        path = os.path.join(self.dir, "copy.figcraft")
        shutil.copy(os.environ["FIGCRAFT_TEST_FILE"], path)
        self.fc = FC(file=path)
        review.FC = lambda: self.fc  # one headless session for every call
        review.SHOTS = os.path.join(self.dir, "shots")

    def tearDown(self):
        self.fc.p.kill()
        self.fc.p.wait()
        shutil.rmtree(self.dir)

    def run_cli(self, *args):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            review.main(list(args))
        return out.getvalue()

    def test_add_export_done(self):
        tops = [t for t in self.fc.tops() if t.get("childCount")]  # a frame with layers inside, whatever comes first
        frame = tops[0]["id"]
        inner = (self.fc.node(frame, 1).get("children") or [{"id": frame}])[0]["id"]
        self.fc.cmd("annotation.add", id=frame, label="Нативная, без номера")  # made in Dev Mode by hand
        self.fc.cmd("annotation.add", id=inner, label="#5 · Срочно")
        self.assertIn("#7 on", self.run_cli("add", str(inner), "Текст", "налезает"))
        md = self.run_cli()
        self.assertTrue(md.startswith(f"# FigCraft — {self.fc.doc(1)['name']} · 3 замечания\n"), md[:80])
        self.assertIn("\n---\n## 5. Срочно\n- **Слой:** `", md)
        self.assertIn(f"» · #{inner}\n- **Путь:** {tops[0]['name']} › ", md)
        self.assertLess(md.index("## 5. Срочно"), md.index("## 6. Нативная, без номера"))
        self.assertIn("- **Размер:** ", md)
        self.assertNotIn("**Скриншот:**", md, "no shots unless asked")
        shot = self.run_cli("show", "7", "--shots").split("**Скриншот:** ")[1].split(" ")[0]
        self.assertTrue(os.path.getsize(shot) > 0, shot)
        self.assertIn("## 5.", self.run_cli("next"))
        self.assertIn("#7 → Проверь", self.run_cli("done", "7", "увеличил", "отступ"))
        self.assertIn("#6 → Вопрос", self.run_cli("ask", "6", "насколько?", "--option", "на 8", "--option", "на 16"))
        self.assertIn("- **Ответ (Claude):** насколько? · варианты: 1) на 8; 2) на 16", self.run_cli("show", "6"))
        md = self.run_cli()
        self.assertIn("· 1 замечание", md)
        self.assertIn("Ещё 2 замечания ждут дизайнера", md)
        self.assertNotIn("## 6.", md)
        self.assertNotIn("## 7.", md)
        self.assertIn("## 7. Текст налезает (проверь)", self.run_cli("--all"))
        cats = {c["name"]: c["count"] for c in self.fc.cmd("annotation.categories")["categories"]}
        self.assertEqual((cats["Проверь"], cats["Вопрос"], cats["Открыто"]), (1, 1, 1))
        self.assertIn("#7 → Готово", self.run_cli("accept", "7"))
        listed = self.run_cli("list")
        self.assertIn("#5 [Открыто] Срочно", listed)
        self.assertIn("(1 ответ.)", listed)

if __name__ == "__main__":
    unittest.main()
