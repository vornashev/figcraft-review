"""python3 -m unittest sidecar/test_server.py — chats, prompts and turn bookkeeping without FigCraft or an agent."""
import atexit
import base64
import json
import os
import shutil
import sys
import tempfile
import time
import unittest
from unittest import mock

os.environ["XDG_STATE_HOME"] = tempfile.mkdtemp(prefix="figcraft-agent-test-")
atexit.register(shutil.rmtree, os.environ["XDG_STATE_HOME"], True)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import server  # noqa: E402
from server import App, new_steps, prompt_text, title_of  # noqa: E402


class Page(unittest.TestCase):
    def test_the_built_chat_or_how_to_build_it(self):
        with tempfile.TemporaryDirectory() as d:
            built = os.path.join(d, "index.html")
            self.assertEqual(server.page(built)[0], 503)
            self.assertIn(b"run build", server.page(built)[1])
            with open(built, "w") as f:
                f.write("<div id=root>")
            self.assertEqual(server.page(built), (200, b"<div id=root>"))
        self.assertTrue(server.PAGE.endswith(os.path.join("web", "dist", "index.html")))


class Prompt(unittest.TestCase):
    def test_segments(self):
        segs = [{"kind": "text", "text": "Сделай "}, {"kind": "layer", "id": 12, "label": "Title"},
                {"kind": "text", "text": " крупнее, как "}, {"kind": "image", "path": "/x.png", "label": "Картинка 1"},
                {"kind": "text", "text": " и по "}, {"kind": "remark", "num": 7, "label": "#7 Кнопка"}]
        self.assertEqual(prompt_text(segs), "Сделай «Title» (#12) крупнее, как [картинка 1] и по [замечание #7]")
        self.assertEqual(title_of(segs), "Сделай Title крупнее, как Картинка 1 и по #7 Кнопка")

    def test_files_of_any_type_and_size(self):
        self.assertEqual(prompt_text([{"kind": "text", "text": "Сверь с "}, {"kind": "file", "path": "/s/t.json", "label": "tokens.json"}]),
                         "Сверь с [файл tokens.json]")
        with tempfile.TemporaryDirectory() as d, mock.patch("server.IMAGES", d):
            big = b"x" * (9 << 20)  # over the old 8 MB cap
            up = App.upload(None, {"data": "data:application/zip;base64," + base64.b64encode(big).decode(), "name": "../log.zip"})
            self.assertEqual((os.path.dirname(up["path"]), up["path"].endswith("-log.zip"), up["size"]), (d, True, len(big)))

    def test_new_steps(self):
        self.assertEqual(new_steps(["b", "a"], ["d", "c", "b", "a"]), 2)
        self.assertEqual(new_steps(["b", "a"], ["b", "a"]), 0)
        self.assertEqual(new_steps([], ["x"]), 1)
        self.assertEqual(new_steps(["b", "a"], ["a"]), 0)  # undone below the old top: claim nothing
        same = ["Set properties"] * 3
        self.assertEqual(new_steps(same, ["Set properties"] * 5), 2)


class Marks(unittest.TestCase):
    def test_lines(self):
        text = "Поправил.\n✓ #3 Заголовок 28 px из стиля Heading\n? #4 — Какой отступ? | 16 | 24\nне #5 ✓\n✓#6: готово"
        self.assertEqual(server.marks(text), [(3, "done", "Заголовок 28 px из стиля Heading", []),
                                              (4, "ask", "Какой отступ?", ["16", "24"]), (6, "done", "готово", [])])

    def test_prompt(self):
        s = server.SYSTEM.format(name="x", path="/d/x.figcraft")
        self.assertIn("✓ #N", s)
        self.assertNotIn("doc.list", s)  # the agent's FigCraft holds only its file
        self.assertIn("Скиллы по дизайну", s)


class AgentEnv(unittest.TestCase):
    def test_each_login_gets_its_config_folder(self):
        from agents import ClaudeAccount
        os.environ["CLAUDE_CONFIG_DIR"] = "/x/.claude-second"
        try:
            self.assertNotIn("CLAUDE_CONFIG_DIR", server.agent_env(server.AGENTS["claude"]))
            self.assertEqual(server.agent_env(ClaudeAccount("c2", "/y"))["CLAUDE_CONFIG_DIR"], "/y")
        finally:
            del os.environ["CLAUDE_CONFIG_DIR"]

    def test_review_py_acts_on_the_chats_file_as_the_agent(self):
        env = server.agent_env(server.AGENTS["claude"], "/d/x.figcraft")
        self.assertEqual((env["FIGCRAFT_DOCUMENT"], env["FIGCRAFT_AGENT"]), ("/d/x.figcraft", server.AGENTS["claude"].name))
        self.assertNotIn("FIGCRAFT_DOCUMENT", server.agent_env(server.AGENTS["claude"]))


class Comments(unittest.TestCase):
    """FigCraft's comment threads beside the remarks: who each waits for, and what the agent is told."""

    THREADS = [{"id": 1, "text": "@Claude кнопка мелкая", "author": "Тёма", "pageName": "Главная", "frameName": "Шапка",
                "mentions": [{"name": "Claude"}], "replies": []},
               {"id": 2, "text": "Заголовок жирнее", "author": "Тёма", "pageName": "Главная", "replies": [
                   {"author": "Тёма", "text": "@Codex глянь", "mentions": [{"name": "Codex"}]},
                   {"author": "Claude (agent)", "agent": True, "text": "Сделал Bold"}]}]

    def setUp(self):
        self.app = App()
        self.app.push = lambda e: None
        self.calls = []

        class Fc:
            def cmd(_, command, **params):
                self.calls.append((command, params))
                if command == "comment.list":
                    return {"comments": self.THREADS}
                if command == "comment.prompt":
                    return {"text": "# FigCraft feedback\n\nFix these comments… resolve…\n\n## Comment 1 — Page\n\n> @Claude кнопка мелкая\n"}
        self.fc = Fc()
        self.app.on_doc = lambda fn: fn(self.fc)

    def test_the_list_says_who_each_thread_waits_for(self):
        first, second = self.app.comment_list()
        self.assertEqual((first["answered"], first["last"], first["mentions"], first["frame"]), (False, None, ["Claude"], "Шапка"))
        self.assertEqual((second["answered"], second["last"], second["replies"]), (True, ["Claude (agent)", "Сделал Bold"], 2))
        self.assertEqual(second["mentions"], ["Codex"], "mentions in replies count too")
        self.assertEqual(self.calls[0], ("comment.list", {"filter": "open"}))

    def test_an_app_without_comments_gives_none(self):
        def broken(fn):
            raise RuntimeError("unknown command")
        self.app.on_doc = broken
        self.assertEqual(self.app.comment_list(), [])

    def test_the_agent_gets_the_threads_without_figcrafts_resolve_instructions(self):
        ctx, _ = self.app.context([{"kind": "comment", "id": 1}], lambda fn: fn(self.fc))
        self.assertIn("## Comment 1", ctx)
        self.assertNotIn("resolve", ctx)
        self.assertEqual(prompt_text([{"kind": "comment", "id": 1, "label": "x"}]), "[комментарий 1]")
        self.assertIn("comment.reply", server.SYSTEM.format(name="x", path="/x"))

    def test_open_remarks_bring_the_unanswered_threads(self):
        self.app.remark_context = lambda run, nums: "Открытых замечаний нет."
        ctx, _ = self.app.context([{"kind": "remarks"}], lambda fn: fn(self.fc))
        self.assertIn("Открытые комментарии FigCraft", ctx)
        self.assertEqual([p for c, p in self.calls if c == "comment.prompt"], [{"ids": [1], "filter": "all"}],
                         "thread 2 waits for the designer: the agent answered it")

    def test_the_designers_acts_go_through_the_control_channel(self):
        sent = []
        self.app.as_designer = lambda command, **params: sent.append((command, params))
        for act in ("go", "resolve"):
            self.app.comment_act({"id": 2, "action": act})
        self.app.comment_act({"id": 2, "action": "reply", "text": " ок "})
        self.assertEqual(sent, [("comment.open", {"id": 2}), ("comment.resolve", {"id": 2}), ("comment.reply", {"id": 2, "text": "ок"})])
        with self.assertRaises(ValueError):
            self.app.comment_act({"id": "2", "action": "go"})


class DesignMd(unittest.TestCase):
    def test_found_up_to_the_project_root_and_saved_from_an_answer(self):
        with tempfile.TemporaryDirectory() as d:
            os.makedirs(os.path.join(d, "repo", ".git"))
            os.makedirs(os.path.join(d, "repo", "design"))
            f = os.path.join(d, "repo", "design", "x.figcraft")
            self.assertEqual(server.design_md(f), (None, os.path.join(d, "repo", "DESIGN.md")))
            reply = {"parts": [{"kind": "text", "text": "Вот:\n```design-md\n# X — design context\nTODO: уточнить\n```\nГотово."}]}
            App.save_design_md({"file": f}, reply)
            self.assertEqual(reply["saved"], os.path.join(d, "repo", "DESIGN.md"))
            self.assertEqual(open(reply["saved"]).read(), "# X — design context\nTODO: уточнить\n")
            self.assertEqual(server.design_md(f)[0], reply["saved"])
            App.save_design_md({"file": f}, {"parts": [{"kind": "text", "text": "```design-md\n# v2\n```"}]})
            self.assertEqual(open(reply["saved"] + ".bak").read(), "# X — design context\nTODO: уточнить\n", "the old one is kept")
            nothing = {"parts": [{"kind": "text", "text": "без блока"}]}
            App.save_design_md({"file": f}, nothing)
            self.assertNotIn("saved", nothing)
            loose = os.path.join(d, "loose", "y.figcraft")
            os.makedirs(os.path.dirname(loose))
            self.assertEqual(server.design_md(loose)[1], os.path.join(d, "loose", "DESIGN.md"), "no project: next to the file")


class FakeGuest:
    """A guest whose FigCraft is a list of undo labels (newest first)."""

    def __init__(self, undo):
        self.undo, self.path = undo, "/tmp/a.figcraft"

    def run(self, fn):
        return fn(self)

    def doc(self, depth=0):
        return {"history": {"undo": list(self.undo)}}

    def cmd(self, command, **params):
        if command == "edit.undo":
            self.undo.pop(0)
        return {}


class Turn(unittest.TestCase):
    def setUp(self):
        self.app = App()
        self.app.push = lambda e: None
        self.chat = {"id": "c1", "file": "/tmp/a.figcraft", "fileName": "a", "title": "t", "messages": [], "session": None}
        self.reply = {"role": "assistant", "parts": [], "running": True}
        self.chat["messages"].append(self.reply)

    def feed(self, *events):
        return [self.app.apply(self.chat, self.reply, e) for e in events]

    def test_a_skill_the_agent_opens_itself(self):
        self.app.took_skill = lambda chat, reply, name: reply.setdefault("skills", []).append({"name": name, "level": "auto"})
        self.feed({"kind": "step", "id": "r", "label": "Read · SKILL.md", "status": "run", "skill": "better-ui"})
        self.assertEqual(self.reply["skills"], [{"name": "better-ui", "level": "auto"}])

    def test_streaming_then_final_text(self):
        self.feed({"kind": "session", "id": "s1"}, {"kind": "delta", "text": "Смот"}, {"kind": "delta", "text": "рю"})
        self.assertEqual(self.reply["parts"], [{"kind": "text", "text": "Смотрю", "streaming": True}])
        self.feed({"kind": "text", "text": "Смотрю."},
                  {"kind": "step", "id": "t", "label": "set_properties", "status": "run", "mut": True, "ids": [3]},
                  {"kind": "step", "id": "t", "status": "ok", "ids": [4]}, {"kind": "delta", "text": "Го"})
        p = self.reply["parts"]
        self.assertEqual(p[0], {"kind": "text", "text": "Смотрю.", "streaming": False})
        self.assertEqual((p[1]["status"], p[1]["ids"]), ("ok", [3, 4]))
        self.assertEqual(p[2]["text"], "Го")
        self.assertEqual(self.chat["session"], "s1")

    def test_a_screenshot_is_kept_for_the_chat(self):
        self.feed({"kind": "step", "id": "s", "label": "screenshot", "status": "run"},
                  {"kind": "step", "id": "s", "status": "ok", "images": [{"type": "image/png", "data": "iVBORw0KGgo="}]})
        shots = self.reply["parts"][0]["shots"]
        self.assertEqual(len(shots), 1)
        self.assertTrue(shots[0].startswith(server.SHOTS) and shots[0].endswith(".png"))
        with open(shots[0], "rb") as f:
            self.assertEqual(f.read(), b"\x89PNG\r\n\x1a\n")

    def test_old_screenshots_go(self):
        self.app.settings["shotDays"] = 7
        old, new = self.app.keep_images([{"type": "image/png", "data": "iVBORw0KGgo="}] * 2)
        os.utime(old, (time.time() - 8 * 86400,) * 2)
        info = self.app.agent_shots()
        self.assertEqual(self.app.agent_shots(7, remove=True)["count"], info["count"] - 1)
        self.assertFalse(os.path.exists(old))
        self.assertTrue(os.path.exists(new))
        self.assertEqual(self.app.agent_shots(remove=True)["count"], 0)
        self.assertFalse(os.path.exists(new))

    def test_catalog_values(self):
        names = {"VariableID:2": "color/bg"}
        self.assertEqual(server.value_of({"type": "color", "value": {"r": 1, "g": 0, "b": 0.5, "a": 1}}, names), "#FF0080")
        self.assertEqual(server.value_of({"type": "color", "value": {"r": 0, "g": 0, "b": 0, "a": 0.5}}, names), "#00000080")
        self.assertEqual(server.value_of({"type": "alias", "value": "VariableID:2"}, names), "→ color/bg")
        self.assertEqual(server.value_of({"type": "float", "value": 16.0}, names), "16")
        self.assertEqual(server.value_of({"type": "string", "value": "Inter"}, names), "«Inter»")
        # colours calculated from others (FigCraft 0.13)
        self.assertEqual(server.value_of({"type": "colorAlpha", "value": {"variable": "VariableID:2", "opacity": 0.4}}, names),
                         "= color/bg × 40%")
        self.assertEqual(server.value_of({"type": "colorMix", "value": {"from": {"variable": "VariableID:2"}, "t": 0.30000001,
                                                                        "to": {"literal": {"r": 1, "g": 0, "b": 0, "a": 1}}}}, names),
                         "= mix(color/bg, #FF0000, 0.3)")
        self.assertEqual(server.type_of({"font_family": "Inter", "font_style": "SemiBold", "font_size": 80.0,
                                         "line_height": {"unit": "percent", "value": 104.0},
                                         "letter_spacing": {"unit": "percent", "value": -3.0}}), "Inter SemiBold 80/104% -3%")
        self.assertEqual(server.type_of({"font_family": "Inter", "font_style": "Regular", "font_size": 13.0,
                                         "line_height": {"unit": "auto"}, "letter_spacing": {"unit": "percent", "value": 0.0}}),
                         "Inter Regular 13/auto")

    def test_a_resumed_sessions_turn_costs_what_it_adds(self):
        # Claude reports the whole session's cost; a new session (another agent) starts from zero
        self.feed({"kind": "session", "id": "s1"}, {"kind": "done", "cost": 11.18})
        self.assertEqual(self.reply["cost"], 11.18)
        self.feed({"kind": "done", "cost": 12.04})
        self.assertAlmostEqual(self.reply["cost"], 0.86)
        self.feed({"kind": "session", "id": "s2"}, {"kind": "done", "cost": 0.5})
        self.assertEqual(self.reply["cost"], 0.5)

    def test_usage_adds_up(self):
        self.feed({"kind": "usage", "input": 10, "output": 5, "cacheRead": 90, "turns": 1, "context": 100},
                  {"kind": "usage", "input": 2, "output": 7, "cacheRead": 100, "turns": 1, "context": 109, "window": 200000})
        self.assertEqual(self.reply["usage"], {"input": 12, "output": 12, "cacheRead": 190, "cacheWrite": 0, "turns": 2,
                                               "context": 109, "window": 200000})

    def test_steps_time_themselves(self):
        with mock.patch("server.time.time", side_effect=[100.0, 100.4]):
            self.feed({"kind": "step", "id": "s", "label": "component.create · Button", "status": "run"},
                      {"kind": "step", "id": "s", "status": "ok"})
        self.assertEqual((self.reply["parts"][0]["t0"], self.reply["parts"][0]["took"]), (100.0, 0.4))

    def test_reads_collect_no_ids(self):
        self.feed({"kind": "step", "id": "r", "label": "get_node", "status": "run", "mut": False, "ids": []},
                  {"kind": "step", "id": "r", "status": "ok", "ids": [9, 10]})
        self.assertEqual(self.reply["parts"][0]["ids"], [])

    def test_done_and_finish(self):
        err = self.feed({"kind": "done", "cost": 0.02, "denied": [{"tool": "Bash", "label": "Bash · ls"}]})[0]
        self.assertIsNone(err)
        self.assertEqual(self.reply["denied"][0]["tool"], "Bash")
        self.feed({"kind": "step", "id": "s", "label": "x", "status": "run", "mut": True, "ids": [5]})
        self.app.procs["c1"] = (None, self.chat["file"], 0)
        self.app.chats["c1"] = self.chat
        self.app.finish(self.chat, self.reply, None, ["old"], FakeGuest(["mine 2", "mine 1", "old"]), server.time.time())
        self.assertFalse(self.reply["running"])
        self.assertEqual(self.reply["parts"][0]["status"], "stopped")
        self.assertEqual(self.reply["changes"], {"steps": 2, "top": ["mine 2", "mine 1"], "ids": [5], "layers": []})
        self.assertNotIn("c1", self.app.procs)
        saved = server.load(server.chat_file(self.chat["file"]), {})
        self.assertIn("c1", saved["chats"])

    def test_undo_only_on_top(self):
        self.reply["changes"] = {"steps": 1, "top": ["agent"], "ids": [5]}
        self.reply["running"] = False
        self.app.chats["c1"] = self.chat
        with self.assertRaises(ValueError):  # no guest: its history is gone
            self.app.undo_changes({"chat": "c1", "index": 0})
        g = FakeGuest(["later", "agent"])
        self.app.guests.known = lambda path, slot=0: g
        with self.assertRaises(ValueError):
            self.app.undo_changes({"chat": "c1", "index": 0})
        g.undo = ["agent", "older"]
        self.app.procs["c2"] = (None, self.chat["file"], 0)
        with self.assertRaises(ValueError):  # an agent is working in the file
            self.app.undo_changes({"chat": "c1", "index": 0})
        del self.app.procs["c2"]
        self.app.undo_changes({"chat": "c1", "index": 0})
        self.assertEqual(g.undo, ["older"])
        self.assertTrue(self.reply["changes"]["undone"])

    def test_one_turn_per_file(self):
        self.app.doc = {"path": self.chat["file"], "name": "a"}
        self.app.chats["c1"] = self.chat
        self.app.procs["c1"] = (None, self.chat["file"], 0)
        before = set(self.app.chats)
        with self.assertRaises(ValueError) as e:
            self.app.send({"segments": [{"kind": "text", "text": "ещё"}]})
        self.assertIn("уже работает агент", str(e.exception))
        self.assertEqual(set(self.app.chats), before)  # no empty chat left behind


class CanvasGuest(FakeGuest):
    """A guest with top-level frames, whose batch makes new ones (or copies, renamed by the node.set after them),
    and the file's collections and styles."""

    def __init__(self):
        super().__init__([])
        self.frames, self.next = [{"id": 5, "name": "01 Главная", "x": 0, "y": 100, "width": 1440, "height": 900}], 10
        self.collections, self.styles, self.steps = [], [], []

    def tops(self):
        return self.frames

    def node(self, id, depth=1):
        f = next((f for f in self.frames if f.get("id") == id), None)
        if f is None:
            raise RuntimeError(f"no such layer {id}")
        return f

    def cmd(self, command, **params):
        if command == "variable.list":
            return {"collections": self.collections, "variables": []}
        if command == "style.list":
            return self.styles
        return super().cmd(command, **params)

    def batch(self, steps, label="Batch"):
        self.label, out = label, []
        self.steps.append(steps)
        self.undo.insert(0, label)
        for st in steps:
            c, prm = st["command"], st["params"]
            self.next += 1
            if c == "node.create":
                self.frames.append({**prm, "id": self.next})
                out.append({"id": self.next})
            elif c == "edit.duplicate":
                src = self.node(prm["ids"][0])
                self.frames.append({**src, "id": self.next, "x": src["x"] + prm["dx"], "y": src["y"] + prm["dy"],
                                    "copy": src["id"]})
                out.append({"ids": [self.next]})
            elif c == "node.set" and "ids" not in prm:  # the selection: the copy just made
                self.frames[-1].update(prm)
                out.append({"ok": True})
            else:
                out.append({"ok": True})
        return out


STYLE = {"name": "almanac", "title": "Almanac", "group": "style", "mode": "manual", "source": "builtin", "summary": "журнал",
         "description": "", "dir": "/nonexistent", "path": "/nonexistent/SKILL.md", "origin": "hallmark"}
STYLES = [STYLE, {**STYLE, "name": "graphite", "title": "Graphite", "origin": "tweakcn"},
          {**STYLE, "name": "swiss", "title": "Swiss", "origin": "uipro"},
          {**STYLE, "name": "dusk", "title": "Dusk"}, {**STYLE, "name": "bloom", "title": "Bloom"}]


class Variants(unittest.TestCase):
    def setUp(self):
        self.app = App()
        self.app.push = lambda e: None
        self.app.save = lambda path: None
        self.app.skill_catalog = lambda file=None: STYLES
        self.app.agent_list = lambda: [{"id": "codex", "models": [{"id": "gpt-6.1-sol"}]}]
        self.app.lane_turn = lambda chat, reply, segs=None: self.lanes.append(reply)
        self.lanes, self.guest = [], CanvasGuest()
        self.app.guests.get = lambda path, slot=0, name="": self.guest
        self.reply = {"role": "assistant", "agent": "claude", "model": "claude-opus-5-5", "parts": [], "running": True}
        self.chat = {"id": "c1", "file": "/tmp/a.figcraft", "fileName": "a", "title": "t", "skills": [], "session": "s",
                     "messages": [{"role": "user", "text": "главная", "segments": [{"kind": "text", "text": "главная"}]},
                                  self.reply]}
        self.app.chats["c1"] = self.chat
        self.app.procs["c1"] = (None, self.chat["file"], 0)
        self.app.settings["variants"] = server.variant_settings(
            {"count": 3, "lanes": [{"agent": "codex", "model": "", "style": "graphite"}, {"agent": "nope"}]})

    def call(self, name, args, turn="c1", slot="0"):
        q = {"doc": [server.key_of(self.chat["file"])], "slot": [slot], "turn": [turn]}
        return self.app.mcp(q, {"jsonrpc": "2.0", "id": 7, "method": "tools/call", "params": {"name": name, "arguments": args}})

    def start(self, n=3, **more):
        return self.call("variants", {"frame": {"width": 1440, "height": 1024}, "directions": [
            {"title": t, "idea": "i", "style": st} for t, st in
            zip(("Журнал", "Инструмент", "Сетка"), ("graphite", "almanac", "swiss"))][:n], **more})

    def finish_all(self):
        for k in [k for k in self.app.procs]:
            self.app.procs.pop(k)
        for m in self.chat["messages"]:
            m["running"] = False

    def test_frames_lanes_and_who_draws_each(self):
        out = self.start()
        self.assertEqual(out["id"], 7)
        self.assertNotIn("isError", out["result"])
        made = self.guest.frames[1:]
        self.assertEqual([(f["name"], f["x"], f["y"]) for f in made],
                         [("1. Журнал", 1840, 100), ("2. Инструмент", 3480, 100), ("3. Сетка", 5120, 100)],
                         "a row right of the page's content, one undo step")
        self.assertEqual(self.guest.label, "Варианты ×3: рамки")
        lanes = [m for m in self.chat["messages"] if m.get("lane")]
        self.assertEqual(lanes, self.lanes)
        self.assertEqual([(m["agent"], m["model"], m["lane"]["style"], m["lane"]["frame"]) for m in lanes],
                         [("codex", "gpt-6.1-sol", "graphite", 11), ("claude", "claude-opus-5-5", "almanac", 12),
                          ("claude", "claude-opus-5-5", "swiss", 13)],
                         "the designer's lane and style win; an unknown agent falls back to the orchestrator")
        self.assertEqual(self.reply["variants"]["frames"], [11, 12, 13])
        self.assertEqual(sorted(k for k in self.app.procs if ":" in k), ["c1:1", "c1:2", "c1:3"])
        self.assertIn({"chat": "c1", "file": "/tmp/a.figcraft", "lane": 2}, self.app.running())
        again = self.start()
        self.assertTrue(again["result"]["isError"], "one run per turn")

    def test_bad_calls_say_why(self):
        bad = self.call("variants", {"frame": {"width": 1440, "height": 900},
                                     "directions": [{"title": "A", "style": "zzz"}, {"title": "B", "style": "zzz"}]})
        self.assertIn("нет стиля «zzz»", bad["result"]["content"][0]["text"])
        lane = self.call("variants", {"frame": {"width": 1, "height": 1}, "directions": [{"title": "A"}]}, turn="c1:2")
        self.assertIn("не у дорожки", lane["result"]["content"][0]["text"])
        self.assertEqual(self.guest.frames[1:], [])

    def test_the_orchestrator_compares_once_all_are_done(self):
        self.start()
        asked = []
        self.app.start_turn = lambda chat, agent, model, segs, variants=1, auto=False, extra=None: asked.append(
            (agent.id, model, auto, segs, extra))
        run = self.reply["variants"]["run"]
        for k in ("c1:1", "c1:2", "c1"):
            self.app.procs.pop(k)
            self.app.compare_when_done(run)
        self.assertEqual(asked, [], "lane 3 still works")
        self.app.procs.pop("c1:3")
        self.app.compare_when_done(run)
        self.app.compare_when_done(run)
        self.assertEqual(len(asked), 1)
        self.assertEqual(asked[0][:3], ("claude", "claude-opus-5-5", True))
        self.assertIn("1. Журнал (#11, Codex)", asked[0][3][0]["text"])
        self.assertEqual(asked[0][4], {"compare": run})
        self.app.procs["c1"] = (None, self.chat["file"], 0)
        with self.assertRaises(ValueError):  # the designer's «Сравнить снова» waits for the file
            self.app.compare_again({"chat": "c1", "run": run})
        self.app.procs.pop("c1")
        self.app.compare_again({"chat": "c1", "run": run})
        self.assertEqual(len(asked), 2)

    def test_a_stopped_run_is_not_compared(self):
        self.start()
        asked = []
        self.app.start_turn = lambda *a, **k: asked.append(a)
        self.app.stop("c1")
        for k in [k for k in self.app.procs]:
            self.app.procs.pop(k)
        self.app.compare_when_done(self.reply["variants"]["run"])
        self.assertEqual(asked, [])

    def test_a_lane_undoes_in_its_own_history(self):
        self.start()
        lane = next(m for m in self.chat["messages"] if (m.get("lane") or {}).get("n") == 2)
        lane.update(running=False, changes={"steps": 1, "top": ["Build"], "ids": [12]})
        mine, other = FakeGuest(["Build"]), FakeGuest(["Build"])
        self.app.guests.known = lambda path, slot=0: {2: mine, 1: other}.get(slot)
        with self.assertRaises(ValueError):  # lane 2 still runs in that slot
            self.app.undo_changes({"chat": "c1", "index": self.chat["messages"].index(lane)})
        self.app.procs.pop("c1:2")
        self.app.undo_changes({"chat": "c1", "index": self.chat["messages"].index(lane)})
        self.assertEqual((mine.undo, other.undo), ([], ["Build"]), "lanes 1 and 3 keep working, their steps stay")

    def test_styles_tool(self):
        listed = self.call("styles", {"query": "журнал"})["result"]["content"][0]["text"]
        self.assertIn("- almanac — Almanac · стиль · hallmark · журнал", listed)
        self.assertTrue(self.call("styles", {"name": "zzz"})["result"]["isError"])

    def test_orchestrator_prompt_names_the_lanes_and_pinned_styles(self):
        text = self.app.orchestrate_text(self.chat, 3, server.AGENTS["claude"], "claude-opus-5-5")
        self.assertIn("Варианты ×3", text)
        self.assertIn("1 — Codex · gpt-6.1-sol, 2 — Claude Code · claude-opus-5-5", text)
        self.assertIn("1 — Graphite (graphite)", text)

    def test_settings_are_cleaned(self):
        v = server.variant_settings({"count": 99, "orchestrator": {"agent": "claude", "model": "m"},
                                     "lanes": [{"agent": "codex", "model": "x", "style": "s"}, "junk"] * 5})
        self.assertEqual((v["count"], v["orchestrator"], len(v["lanes"])), (6, {"agent": "claude", "model": "m"}, 6))
        self.assertEqual(v["lanes"][:2], [{"agent": "codex", "model": "x", "style": "s"}, None])
        self.assertEqual((v["axis"], v["limit"]), ("style", 0))
        v = server.variant_settings({"axis": "adaptive", "limit": "20", "presets": [
            {"name": "  Claude +  Codex ", "count": 2, "lanes": [{"agent": "codex"}], "limit": 5}, {"name": ""}, "x"]})
        self.assertEqual((v["axis"], v["limit"]), ("adaptive", 20))
        self.assertEqual(v["presets"], [{"name": "Claude + Codex", "count": 2, "orchestrator": None,
                                         "lanes": [{"agent": "codex", "model": ""}], "axis": "style"}])

    def test_directions_must_differ(self):
        same = self.call("variants", {"frame": {"width": 900, "height": 900}, "directions": [
            {"title": "A", "style": "graphite"}, {"title": "B", "style": "dusk"}, {"title": "C", "style": "dusk"}]})
        self.assertIn("стили повторяются", same["result"]["content"][0]["text"])
        one = self.call("variants", {"frame": {"width": 900, "height": 900}, "directions": [
            {"title": "A"}, {"title": "B", "style": "dusk"}, {"title": "C", "style": "bloom"}, {"title": "D", "style": "almanac"}]})
        self.assertIn("из одного источника (hallmark)", one["result"]["content"][0]["text"])
        twice = self.call("variants", {"frame": {"width": 900, "height": 900}, "directions": [{"title": "A"}, {"title": "a"}]})
        self.assertIn("названия направлений повторяются", twice["result"]["content"][0]["text"])
        ok = self.call("variants", {"axis": "structure", "frame": {"width": 900, "height": 900}, "directions": [
            {"title": "A"}, {"title": "B", "style": "dusk"}, {"title": "C", "style": "dusk"}]})
        self.assertNotIn("isError", ok["result"], "one style for all is the point of «structure»")
        self.assertEqual([m["lane"]["axis"] for m in self.lanes], ["structure"] * 3)

    def test_variants_of_a_frame_are_its_copies(self):
        bad = self.call("variants", {"base": "99", "directions": [{"title": "A"}]})
        self.assertIn("не рамка верхнего уровня", bad["result"]["content"][0]["text"])
        out = self.call("variants", {"base": "5", "axis": "adaptive", "directions": [
            {"title": "Телефон", "frame": {"width": 390, "height": 844}}, {"title": "Десктоп"}]})
        self.assertNotIn("isError", out["result"])
        made = self.guest.frames[1:]
        self.assertEqual([(f["name"], f["copy"], f["x"], f["width"], f["height"]) for f in made],
                         [("1. Телефон", 5, 1840, 390, 844), ("2. Десктоп", 5, 2430, 1440, 900)],
                         "copies of #5 in a row, each its direction's size, the base's by default")
        self.assertEqual(len(self.guest.steps), 1, "one undo step")
        self.assertEqual(self.lanes[0]["lane"]["base"], "5")

    def test_lane_numbers_go_on_across_runs(self):
        self.start(2)
        self.finish_all()
        self.reply2 = {"role": "assistant", "agent": "claude", "model": "m", "parts": [], "running": True}
        self.chat["messages"] += [{"role": "user", "text": "смешай"}, self.reply2]
        self.app.procs["c1"] = (None, self.chat["file"], 0)
        self.call("variants", {"frame": {"width": 900, "height": 900}, "directions": [{"title": "Микс 1+2"}]})
        self.assertEqual(self.lanes[-1]["lane"]["n"], 3, "«V3 ·» can't clash with the first run's «V1 ·»")
        self.assertEqual(self.guest.frames[-1]["name"], "3. Микс 1+2")

    def test_a_lane_goes_on(self):
        self.start()
        run = self.reply["variants"]["run"]
        with self.assertRaises(ValueError):
            self.app.lane_act({"chat": "c1", "n": 2, "text": "плотнее"})  # still drawing
        self.finish_all()
        first = self.lanes[1]
        first["lane"]["session"] = "sess-2"
        self.app.procs["c9"] = (None, self.chat["file"], 0)
        with self.assertRaises(ValueError):  # another chat's turn in the file
            self.app.lane_act({"chat": "c1", "n": 2, "text": "плотнее"})
        del self.app.procs["c9"]
        self.app.procs["c1"] = (None, self.chat["file"], 0)  # the orchestrator's own turn is fine
        self.app.lane_act({"chat": "c1", "n": 2, "segments": [{"kind": "text", "text": "плотнее"}]})
        user, more = self.chat["messages"][-2:]
        self.assertEqual(user["toLane"], {"run": run, "n": 2, "title": "Инструмент"})
        self.assertEqual((more["agent"], more["lane"]["kind"], more["lane"]["resume"], more["lane"]["note"],
                          more["lane"]["frame"]), ("claude", "more", "sess-2", "плотнее", 12))
        self.assertIn("c1:2", self.app.procs)
        self.assertEqual(self.app.lanes_of(self.chat, run)[2], more, "the latest attempt stands for the lane")

    def test_a_failed_lane_runs_again_by_another_agent(self):
        self.start()
        self.finish_all()
        old = self.lanes[0]
        old.update(error="лимит", lane={**old["lane"], "session": "x"})
        self.app.lane_act({"chat": "c1", "n": 1, "kind": "retry", "agent": "claude", "model": "claude-sonnet-5-5"})
        new = self.chat["messages"][-1]
        self.assertTrue(old["retried"])
        self.assertEqual((new["agent"], new["model"], new["lane"]["kind"], new["lane"]["resume"]),
                         ("claude", "claude-sonnet-5-5", "retry", None))
        self.assertFalse(any(m.get("toLane") for m in self.chat["messages"]), "no message from the designer: just again")

    def test_the_orchestrator_sends_work_into_a_lane(self):
        self.start()
        self.finish_all()
        self.app.procs["c1"] = (None, self.chat["file"], 0)
        out = self.call("lane", {"n": 3, "brief": "кейсы крупнее"})
        self.assertNotIn("isError", out["result"])
        user = self.chat["messages"][-2]
        self.assertEqual((user["auto"], user["toLane"]["n"], user["text"]), (True, 3, "кейсы крупнее"))
        self.assertTrue(self.call("lane", {"n": 3, "brief": "x"}, turn="c1:3", slot="3")["result"]["isError"])

    def test_pick_keeps_one_variant_and_its_tokens(self):
        self.start()
        self.finish_all()
        run = self.reply["variants"]["run"]
        self.guest.collections = [{"id": "C1", "name": "V1 · Журнал"}, {"id": "C2", "name": "V2 · Инструмент"},
                                  {"id": "C0", "name": "Tokens"}]
        self.guest.styles = [{"id": "S1", "name": "V1/Body"}, {"id": "S2", "name": "V2/Body"}, {"id": "S3", "name": "V3/H1"}]
        self.app.guests.known = lambda path, slot=0: self.guest
        self.app.pick_variant({"chat": "c1", "run": run, "n": 1})
        steps = [(s["command"], s["params"]) for s in self.guest.steps[-1]]
        self.assertEqual(steps, [
            ("edit.delete", {"ids": [12, 13]}), ("variable.deleteCollection", {"collection": "C2"}),
            ("style.delete", {"style": "S2"}), ("style.delete", {"style": "S3"}),
            ("variable.renameCollection", {"collection": "C1", "name": "Журнал"}),
            ("style.move", {"styles": ["S1"], "folder": ""}), ("node.set", {"ids": [11], "name": "Журнал"})])
        picked = self.reply["variants"]["picked"]
        self.assertEqual((picked["n"], picked["collection"], picked["frames"], picked["top"]),
                         (1, "Журнал", [12, 13], ["Варианты: беру 1"]))
        with self.assertRaises(ValueError):
            self.app.pick_variant({"chat": "c1", "run": run, "n": 2})
        self.app.pick_variant({"chat": "c1", "run": run, "undo": True})
        self.assertTrue(picked["undone"])
        self.assertNotIn("Варианты: беру 1", self.guest.undo)
        self.app.lane_act({"chat": "c1", "run": run, "n": 1, "kind": "spread"})
        self.assertEqual(self.chat["messages"][-1]["lane"]["kind"], "spread")

    def test_what_a_lane_is_told(self):
        self.start()
        self.finish_all()
        ran = []
        app = self.app
        app.execute = lambda chat, reply, agent, model, prompt, images, guest, started, marks, tid, slot, session: \
            ran.append((prompt, tid, slot, session))
        app.catalog = lambda run: "КАТАЛОГ"
        del app.lane_turn  # the real one
        app.lane_turn(self.chat, self.lanes[1])
        prompt, tid, slot, session = ran[-1]
        self.assertEqual((tid, slot, session), ("c1:2", 2, None))
        for part in ("КАТАЛОГ", "Ты дорожка 2", "рамки #12 «2. Инструмент»\n(1440×1024)", "коллекции «V2 · Инструмент»",
                     "Стиль: Almanac", "Задача дизайнера:\nглавная"):
            self.assertIn(part, prompt)
        self.lanes[1]["lane"]["session"] = "s2"
        app.lane_act({"chat": "c1", "n": 2, "text": "плотнее"})
        import time as t
        for _ in range(50):
            if len(ran) > 1:
                break
            t.sleep(0.01)
        prompt, tid, slot, session = ran[-1]
        self.assertEqual(session, "s2", "its own session goes on")
        self.assertTrue(prompt.startswith("Дизайнер о твоём варианте 2 «Инструмент» (рамка #12): плотнее"), prompt)

    def test_orchestrator_prompt_follows_the_axis_and_the_frame_pointed_at(self):
        self.app.settings["variants"]["axis"] = "structure"
        text = self.app.orchestrate_text(self.chat, 2, server.AGENTS["claude"], "m", [{"kind": "layer", "id": "5", "label": "01"}])
        self.assertIn("разных структур в одной системе", text)
        self.assertIn("axis «structure», base «5»", text)


class SkillLibrary(unittest.TestCase):
    def setUp(self):
        from unittest.mock import patch
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = self.tmp.name
        self.folder = os.path.join(self.root, "graphite")
        os.makedirs(self.folder)
        with open(os.path.join(self.folder, "SKILL.md"), "w") as f:
            f.write("---\nname: graphite\nmetadata:\n  group: style\n  mode: manual\n---\n\nGraphite body")
        with open(os.path.join(self.folder, "tokens.md"), "w") as f:
            f.write("Tokens")
        self.skill = server.skills.read_skill(self.folder, "builtin")
        self.cat = patch.object(server.skills, "catalog", return_value=[self.skill])
        self.cat.start()
        self.addCleanup(self.cat.stop)
        settings = patch.object(server, "SETTINGS", os.path.join(self.root, "settings.json"))
        settings.start()
        self.addCleanup(settings.stop)
        self.app = App()
        self.app.state = lambda: {}

    def test_the_chats_reference_mode_reaches_the_prompt(self):
        self.skill.update(group="task", mode="always")
        from unittest.mock import patch
        refs = patch.object(server.skills, "references", return_value={"images": [{"file": "ref.png"}], "links": []})
        refs.start()
        self.addCleanup(refs.stop)
        chat = {"id": "c1", "file": "/x.figcraft", "skills": [], "messages": []}
        self.app.chats["c1"] = chat
        self.app.save = lambda file: None
        self.app.push_chat = lambda chat: None
        self.assertIn("— чек-лист", self.app.skills_part(chat, {}, server.AGENTS["claude"], []), "checklist by default")
        self.app.set_skills({"chat": "c1", "reference": "inspire"})
        self.app.set_skills({"chat": "c1", "reference": "bad"})
        self.assertEqual(chat["reference"], "inspire", "an unknown mode is ignored")
        self.assertIn("— вдохновение", self.app.skills_part(chat, {}, server.AGENTS["claude"], []))

    def test_details_and_modes_change_the_actual_prompt_and_survive_restart(self):
        details = server.skills.details(self.app.find_skill("graphite"))
        self.assertEqual([f["name"] for f in details["files"]], ["SKILL.md", "tokens.md"])
        self.assertEqual(details["body"], "Graphite body")
        for mode, expected in [("always", ["always"]), ("manual", []), ("auto", [])]:
            self.app.set_skill_mode({"name": "graphite", "mode": mode})
            self.assertEqual(App().skill_list()[0]["mode"], mode)
            chat, reply = {"file": "/x.figcraft"}, {}
            prompt = self.app.skills_part(chat, reply, server.AGENTS["claude"], [])
            self.assertEqual([s["level"] for s in reply["skills"]], expected)
            self.assertEqual("Graphite body" in prompt, mode == "always")
            self.assertEqual("- graphite" in prompt, mode == "auto")
        self.assertEqual(self.skill["mode"], "manual", "catalog metadata stays unchanged")
        with self.assertRaises(ValueError):
            self.app.set_skill_mode({"name": "graphite", "mode": "bad"})
        with self.assertRaises(ValueError):
            self.app.find_skill("../../elsewhere")
        self.skill["source"] = "pen.dev"
        with self.assertRaises(ValueError):
            self.app.set_skill_mode({"name": "graphite", "mode": "auto"})

    def test_import_preserves_files_rejects_duplicates_and_links(self):
        from unittest.mock import patch
        home = os.path.join(self.root, "home")
        with patch.object(server.skills, "personal_dir", return_value=home):
            imported = server.skills.import_folder(self.folder)
            self.assertEqual(imported["source"], "mine")
            self.assertTrue(os.path.isfile(os.path.join(imported["dir"], "tokens.md")))
            with self.assertRaises(ValueError):
                server.skills.import_folder(self.folder)
            with open(os.path.join(imported["dir"], "tokens.md")) as f:
                self.assertEqual(f.read(), "Tokens")
            os.symlink("tokens.md", os.path.join(self.folder, "link"))
            with self.assertRaises(ValueError):
                server.skills.import_folder(self.folder)

    def test_references_serve_only_listed_images_inside_the_skill(self):
        image = os.path.join(self.folder, "preview.webp")
        with open(image, "wb") as f:
            f.write(b"webp preview")
        outside = os.path.join(self.root, "outside.png")
        with open(outside, "wb") as f:
            f.write(b"private")
        os.symlink(outside, os.path.join(self.folder, "linked.png"))
        manifest = {"images": [{"file": "preview.webp", "label": "Десктоп"}, {"file": "../outside.png"},
                                {"file": "linked.png"}, {"file": "SKILL.md"}, {"file": "missing.png"}],
                    "links": [{"label": "Пример", "url": "https://example.org/theme/"},
                              {"url": "javascript:alert(1)"}, {"url": "file:///etc/passwd"}]}
        with open(os.path.join(self.folder, "references.json"), "w") as f:
            json.dump(manifest, f)
        refs = server.skills.details(self.skill)["references"]
        self.assertEqual([i["file"] for i in refs["images"]], ["preview.webp"])
        self.assertEqual(refs["images"][0]["url"], "/api/skill-image?name=graphite&file=preview.webp")
        self.assertEqual(refs["links"], [{"label": "Пример", "url": "https://example.org/theme/"}])
        self.assertEqual(server.skills.reference_image(self.skill, "preview.webp"), (b"webp preview", "image/webp"))
        for file in ("../outside.png", "linked.png", "SKILL.md", "tokens.md"):
            with self.assertRaises(ValueError):
                server.skills.reference_image(self.skill, file)

    def test_references_are_optional_and_malformed_manifests_are_ignored(self):
        self.assertEqual(server.skills.references(self.skill), {"images": [], "links": []})
        for content in ("{bad json", "[]", '{"images": 3, "links": "wrong"}'):
            with open(os.path.join(self.folder, "references.json"), "w") as f:
                f.write(content)
            self.assertEqual(server.skills.references(self.skill), {"images": [], "links": []})

    def test_collection_metadata_is_independent_of_the_installation_source(self):
        with open(os.path.join(self.folder, "SKILL.md"), "w") as f:
            f.write("---\nname: graphite\nmetadata:\n  group: task\n  origin: opendesign\n  category: apps\n  style: Soft\n---\nTask body")
        with open(os.path.join(self.folder, "reference.webp"), "wb") as f:
            f.write(b"image")
        with open(os.path.join(self.folder, "references.json"), "w") as f:
            json.dump({"images": [{"file": "reference.webp"}]}, f)
        skill = server.skills.read_skill(self.folder, "builtin")
        self.assertEqual((skill["origin"], skill["category"], skill["source"], skill["style"]), ("opendesign", "apps", "builtin", "Soft"))
        self.assertIn("skill-image?name=graphite", skill["thumbnail"])
        with mock.patch.object(server.skills, "catalog", return_value=[skill]):
            entry = self.app.skill_list()[0]
        self.assertEqual((entry["origin"], entry["category"], entry["thumbnail"]), ("opendesign", "apps", skill["thumbnail"]))
        self.assertNotIn("dir", entry)

    def test_design_resource_metadata_reaches_the_catalog_and_card(self):
        meta = {"category": "design-systems", "resource_kind": "components", "formats": "figma code",
                "resource_source": "mixed", "access": "mixed"}
        with open(os.path.join(self.folder, "SKILL.md"), "w") as f:
            f.write("---\nname: graphite\nmetadata:\n  group: library\n"
                    + "".join(f"  {k}: {v}\n" for k, v in meta.items()) + "---\nComponent guidance")
        skill = server.skills.read_skill(self.folder, "builtin")
        with mock.patch.object(server.skills, "catalog", return_value=[skill]):
            entry = self.app.skill_list()[0]
        detail = server.skills.details(skill)
        for key, value in meta.items():
            self.assertEqual(entry[key], value)
            self.assertEqual(detail[key], value)
        self.assertEqual(entry["group"], "library")
        self.assertNotIn("dir", entry)


class Storage(unittest.TestCase):
    def test_migrate_and_cap(self):
        old = {f"c{i}": {"id": f"c{i}", "file": f"/f{i % 2}.figcraft", "messages": [{"role": "user", "text": str(k)} for k in range(400)]}
               for i in range(3)}
        server.store(server.OLD_CHATS, old)
        app = App()
        self.assertEqual(set(app.chats), {"c0", "c1", "c2"})
        self.assertFalse(os.path.exists(server.OLD_CHATS))
        app.save("/f0.figcraft")
        saved = server.load(server.chat_file("/f0.figcraft"), {})["chats"]
        self.assertEqual(set(saved), {"c0", "c2"})
        self.assertEqual(len(saved["c0"]["messages"]), server.KEEP_MESSAGES)
        self.assertEqual(set(App().chats), {"c0", "c1", "c2"})


if __name__ == "__main__":
    unittest.main()
