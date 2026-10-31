"""python3 -m unittest sidecar/test_agents.py — the agents' JSON lines as chat events (samples from real runs)."""
import http.server
import json
import os
import subprocess
import sys
import tempfile
import threading
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "agent"))
from agents import AGENTS, changes_design, claude_accounts, layer_ids, tool_label  # noqa: E402
import bridge  # noqa: E402


class Parse(unittest.TestCase):
    def test_claude(self):
        p = AGENTS["claude"].parse
        self.assertEqual(p({"type": "system", "subtype": "init", "session_id": "s1"}), [{"kind": "session", "id": "s1"}])
        out = p({"type": "assistant", "message": {"content": [
            {"type": "text", "text": "Смотрю"},
            {"type": "tool_use", "id": "t1", "name": "mcp__figcraft__batch", "input": {"label": "Review UX", "commands": []}}]}})
        self.assertEqual(out, [{"kind": "text", "text": "Смотрю"},
                               {"kind": "step", "id": "t1", "label": "batch · Review UX", "status": "run", "mut": False, "ids": []}])
        self.assertEqual(p({"type": "user", "message": {"content": [{"type": "tool_result", "tool_use_id": "t1", "is_error": True}]}}),
                         [{"kind": "step", "id": "t1", "status": "error", "ids": []}])
        res = p({"type": "user", "message": {"content": [{"type": "tool_result", "tool_use_id": "t2",
                                                           "content": [{"type": "text", "text": '{"created": [{"id": 41}]}'}]}]}})
        self.assertEqual(res[0]["ids"], [41])
        shot = p({"type": "user", "message": {"content": [{"type": "tool_result", "tool_use_id": "t3", "content": [
            {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": "iVBO"}}]}]}})
        self.assertEqual(shot[0]["images"], [{"type": "image/png", "data": "iVBO"}])
        pi = AGENTS["pi"].parse({"type": "tool_execution_end", "toolCallId": "t4", "result": {"content": [
            {"type": "image", "data": "R0lG", "mimeType": "image/gif"}]}})
        self.assertEqual(pi[0]["images"], [{"type": "image/gif", "data": "R0lG"}])
        delta = {"type": "stream_event", "event": {"type": "content_block_delta", "delta": {"type": "text_delta", "text": "См"}}}
        self.assertEqual(p(delta), [{"kind": "delta", "text": "См"}])
        self.assertEqual(p({"type": "user", "message": {"content": "plain"}}), [])
        done = p({"type": "result", "session_id": "s1", "total_cost_usd": 0.01, "is_error": True, "result": "limit"})
        self.assertEqual(done[-1], {"kind": "done", "cost": 0.01, "error": "limit"})
        denied = p({"type": "result", "permission_denials": [{"tool_name": "Bash", "tool_input": {"command": "ls"}}]})
        self.assertEqual(denied[-1]["denied"], [{"tool": "Bash", "label": "Bash · ls"}])
        usage = p({"type": "result", "num_turns": 2, "modelUsage": {"m": {"contextWindow": 1000000}}, "usage": {
            "input_tokens": 3, "output_tokens": 50, "cache_read_input_tokens": 900, "cache_creation_input_tokens": 400,
            "iterations": [{"input_tokens": 1, "cache_creation_input_tokens": 300},
                           {"input_tokens": 2, "cache_read_input_tokens": 900, "cache_creation_input_tokens": 100}]}})[1]
        self.assertEqual(usage, {"kind": "usage", "input": 3, "output": 50, "cacheRead": 900, "cacheWrite": 400,
                                 "turns": 2, "context": 1002, "window": 1000000})

    def test_codex(self):
        p = AGENTS["codex"].parse
        self.assertEqual(p({"type": "thread.started", "thread_id": "x"}), [{"kind": "session", "id": "x"}])
        cmd = {"id": "i1", "type": "command_execution", "command": "/usr/bin/bash -lc 'echo hi'", "exit_code": None}
        self.assertEqual(p({"type": "item.started", "item": cmd})[0]["label"], "shell · echo hi")
        self.assertEqual(p({"type": "item.completed", "item": cmd | {"exit_code": 1}})[0]["status"], "error")
        self.assertEqual(p({"type": "item.completed", "item": {"type": "agent_message", "text": "готово"}}),
                         [{"kind": "text", "text": "готово"}])
        self.assertEqual(p({"type": "item.completed", "item": {"type": "reasoning", "text": "…"}}), [])
        self.assertEqual(p({"type": "turn.failed", "error": {"message": "нет доступа"}}), [{"kind": "done", "error": "нет доступа"}])
        self.assertEqual(p({"type": "turn.completed", "usage": {"input_tokens": 1000, "cached_input_tokens": 800, "output_tokens": 30}}),
                         [{"kind": "usage", "input": 200, "output": 30, "cacheRead": 800, "cacheWrite": 0}, {"kind": "done"}])

    def test_pi(self):
        p = AGENTS["pi"].parse
        self.assertEqual(p({"type": "session", "id": "p1"}), [{"kind": "session", "id": "p1"}])
        start = p({"type": "tool_execution_start", "toolCallId": "c1", "toolName": "mcp",
                   "args": {"tool": "figcraft_inspect_document", "server": "figcraft", "args": {}}})
        self.assertEqual(start, [{"kind": "step", "id": "c1", "label": "inspect_document", "status": "run", "mut": False, "ids": []}])
        self.assertEqual(p({"type": "message_end", "message": {"role": "assistant", "content": [
            {"type": "toolCall", "name": "bash"}, {"type": "text", "text": "ок"}]}}), [{"kind": "text", "text": "ок"}])
        self.assertEqual(p({"type": "message_end", "message": {"role": "user", "content": [{"type": "text", "text": "q"}]}}), [])
        self.assertEqual(p({"type": "message_end", "message": {"role": "assistant", "content": [], "usage": {
            "input": 10, "output": 5, "cacheRead": 90, "cacheWrite": 0, "cost": {"total": 0.1}}}}),
            [{"kind": "usage", "input": 10, "output": 5, "cacheRead": 90, "cacheWrite": 0, "turns": 1, "context": 100}])
        self.assertEqual(p({"type": "agent_end"}), [{"kind": "done"}])

    def test_changes(self):
        self.assertFalse(changes_design("mcp__figcraft__get_node", {"id": 3}))
        self.assertFalse(changes_design("Read", {"file_path": "x"}))
        self.assertTrue(changes_design("mcp__figcraft__set_properties", {"ids": [3]}))
        self.assertFalse(changes_design("mcp__figcraft__run_command", {"command": "variable.list"}))
        self.assertTrue(changes_design("mcp__figcraft__batch", {"commands": [{"command": "page.list"}, {"command": "node.reparent"}]}))
        self.assertTrue(changes_design("mcp", {"tool": "figcraft_create_node", "args": {}}))
        self.assertEqual(layer_ids({"ids": [1, 2], "x": {"parent": 7, "id": True}, "s": '[{"id": 9}]'}), {1, 2, 7, 9})
        step = AGENTS["claude"].parse({"type": "assistant", "message": {"content": [
            {"type": "tool_use", "id": "t", "name": "mcp__figcraft__set_properties", "input": {"ids": [5], "props": {}}}]}})
        self.assertEqual((step[0]["mut"], step[0]["ids"]), (True, [5]))

    def test_labels_and_commands(self):
        self.assertEqual(tool_label("Read", {"file_path": "/a/b/lib.py"}), "Read · lib.py")
        self.assertEqual(tool_label("mcp__figcraft__screenshot", {}), "screenshot")
        self.assertEqual(AGENTS["codex"].title("gpt-6.1-sol"), "GPT-6.1 Sol")
        c = AGENTS["claude"].command("claude-opus-5-5", "s1", "/tmp/m.json", "sys", "figcraft")
        self.assertEqual(c[c.index("--resume") + 1], "s1")
        self.assertIn("mcp__figcraft", c)
        self.assertIn("--include-partial-messages", c)
        self.assertEqual(c[c.index("--permission-mode") + 1], "default")
        self.assertEqual(c[c.index("--tools") + 1:c.index("--allowedTools")], ["Bash", "Edit", "Glob", "Grep", "Read", "Write"])
        self.assertIn("--disable-slash-commands", c)
        c = AGENTS["claude"].command("m", None, "/tmp/m.json", "sys", "figcraft", allow=["Bash", "WebFetch(domain:a.b)"])
        self.assertIn("Bash", c[c.index("--allowedTools") + 1:])
        self.assertIn("WebFetch", c[c.index("--tools") + 1:c.index("--allowedTools")], "a granted tool has to exist too")
        t = AGENTS["claude"].command("m", None, "/tmp/m.json", "sys", "terminal")
        self.assertFalse({"--allowedTools", "--tools", "--disable-slash-commands"} & set(t))
        with tempfile.TemporaryDirectory() as d:
            mcp = os.path.join(d, "m.json")
            with open(mcp, "w", encoding="utf-8") as f:
                json.dump({"mcpServers": {"figcraft": {"command": "/usr/bin/python3", "args": ["bridge.py", "--doc", "k"]}}}, f)
            x = AGENTS["codex"].command("gpt-6-luna", "t1", mcp, "sys", "figcraft")
            y = AGENTS["codex"].command("gpt-6-luna", None, mcp, "sys", "figcraft", images=["/tmp/a.png"])
        self.assertIn('mcp_servers.figcraft.args=["bridge.py", "--doc", "k"]', x)
        self.assertEqual(x[1:4], ["exec", "resume", "t1"])
        self.assertNotIn("-s", x, "`codex exec resume` has no -s")
        self.assertIn('sandbox_mode="read-only"', x)
        self.assertIn('mcp_servers.figcraft.default_tools_approval_mode="approve"', x,
                      "approval_policy never refuses the tools that write unless they are approved up front")
        self.assertEqual(x[-1], "-")
        self.assertEqual(y[y.index("-i") + 1], "/tmp/a.png")

    def test_skills_reach_every_agent_the_same_way(self):
        for a in ("claude", "pi"):
            c = AGENTS[a].command("m", None, "/tmp/m.json", "sys", "figcraft")
            self.assertFalse({"--plugin-dir", "--skill"} & set(c), "skills come in the prompt, not as flags")
        step = AGENTS["claude"].parse({"type": "assistant", "message": {"content": [
            {"type": "tool_use", "id": "r", "name": "Read", "input": {"file_path": "/x/skills/better-ui/SKILL.md"}}]}})[0]
        self.assertEqual(step["skill"], "better-ui")
        step = AGENTS["codex"].parse({"type": "item.started", "item": {"id": "c", "type": "command_execution",
                                                                     "command": "cat /s/better-layout/SKILL.md"}})[0]
        self.assertEqual(step["skill"], "better-layout")
        self.assertNotIn("skill", AGENTS["claude"].parse({"type": "assistant", "message": {"content": [
            {"type": "tool_use", "id": "r", "name": "Read", "input": {"file_path": "/x/README.md"}}]}})[0])

    def test_claude_accounts(self):
        with tempfile.TemporaryDirectory() as home:
            for d, f in ((".claude-second", ".credentials.json"), (".claude-work", ".claude.json"), (".claude-empty", None)):
                os.makedirs(os.path.join(home, d))
                if f:
                    open(os.path.join(home, d, f), "w", encoding="utf-8").close()
            rc = os.path.join(home, ".bashrc")
            with open(rc, "w", encoding="utf-8") as f:
                f.write("alias ll='ls -l'\nalias claude-2='CLAUDE_CONFIG_DIR=\"$HOME/.claude-second\" claude'\n"
                        "alias claude='claude --verbose'\n")
            accs = {a.id: a for a in claude_accounts([rc], home)}
            self.assertEqual(list(accs), ["claude:claude-2", "claude:claude-work"], "the alias names its folder; others by name")
            a = accs["claude:claude-2"]
            self.assertEqual((a.name, a.env(), a.account()), ("Claude Code · claude-2",
                             {"CLAUDE_CONFIG_DIR": os.path.join(home, ".claude-second")}, os.path.join(home, ".claude-second")))
            self.assertEqual(a.command("m", None, "/tmp/m.json", "sys", "figcraft")[1:3], ["-p", "--output-format"])
        self.assertEqual(AGENTS["claude"].env(), {"CLAUDE_CONFIG_DIR": None}, "the default login even under claude-2")


class Bridge(unittest.TestCase):
    def test_answers_on_one_line(self):
        tree = {"id": 7, "x": 2.0, "w": 2.5, "styles": {"fill": None, "text": "S:1"}, "fills": [], "children": [],
                "layout": {"mode": "horizontal", "gridRows": 2, "crossGap": 4.0}}
        out = {"result": {"content": [{"type": "text", "text": json.dumps(tree, indent=2)}, {"type": "image", "data": "x"}]}}
        bridge.compact({"method": "tools/call", "params": {"name": "get_node"}}, out)
        self.assertEqual(out["result"]["content"][0]["text"],
                         '{"id":7,"x":2,"w":2.5,"styles":{"text":"S:1"},"layout":{"mode":"horizontal","crossGap":4}}')
        self.assertEqual(layer_ids(out["result"]["content"][0]["text"]), {7})
        out = {"result": {"content": [{"type": "text", "text": json.dumps({"a": None, "b": [1]}, indent=2)}]}}
        bridge.compact({"method": "tools/call", "params": {"name": "run_command"}}, out)
        self.assertEqual(out["result"]["content"][0]["text"], '{"a":null,"b":[1]}', "only layer trees are pruned")
        text = {"result": {"content": [{"type": "text", "text": "3 commands (id — label"}]}}
        self.assertEqual(bridge.compact({"method": "tools/call", "params": {"name": "list_commands"}}, text), text)

    def test_list_commands_keeps_parameters_for_the_commands_it_names(self):
        listed = ("3 commands (id — label [menu] (shortcut) params; * = undoable):\n"
                  "node.create* — Create layer {type, path? (vector: SVG path data), props?}\n"
                  "file.exportSvg — Export selection as SVG [File] {ids?, path?}\n"
                  "vector.create* — Vector {path (SVG path data)}")
        out = {"result": {"content": [{"type": "text", "text": listed}]}}
        bridge.compact({"method": "tools/call", "params": {"name": "list_commands", "arguments": {"filter": "svg"}}}, out)
        lines = out["result"]["content"][0]["text"].splitlines()
        self.assertEqual(lines[1:4], ["node.create* — Create layer", "file.exportSvg — Export selection as SVG [File] {ids?, path?}",
                                      "vector.create* — Vector"], "svg only in their parameters: id and label")
        self.assertIn("filter = id", lines[-1])
        out = {"result": {"content": [{"type": "text", "text": listed}]}}
        bridge.compact({"method": "tools/call", "params": {"name": "list_commands", "arguments": {"filter": "node.create"}}}, out)
        self.assertIn("node.create* — Create layer {type,", out["result"]["content"][0]["text"])


    def test_build_is_one_batch(self):
        tree = {"name": "Card", "layout": "vertical", "fill": "$color/bg", "children": [
            {"type": "text", "text": "Hi", "textStyle": "Body", "fills": "$color/text"},
            {"component": "Site/Header", "properties": {"Title": "A"}, "width": 300}]}
        steps, made = bridge.expand({"tree": tree, "parent": 9}, lambda: {"Site/Header": 77})
        self.assertEqual([s["command"] for s in steps], ["node.create", "variable.bind", "node.create", "style.apply",
                                                         "variable.bind", "instance.create", "node.set", "instance.setProperties"])
        self.assertEqual(steps[0]["params"], {"type": "frame", "name": "Card", "parent": 9, "select": False,
                                              "props": {"layout": "vertical", "sizingH": "hug", "sizingV": "hug"}})
        row = bridge.expand({"tree": {"layout": "horizontal", "width": 200}})[0][0]["params"]["props"]
        self.assertEqual(row, {"layout": "horizontal", "fill": "none", "sizingV": "hug"}, "see-through, hugs what isn't sized")
        self.assertEqual(steps[1]["params"], {"ids": [{"$step": 0}], "field": "fill", "variable": "color/bg"})
        self.assertEqual(steps[2]["params"]["parent"], {"$step": 0})
        self.assertEqual(steps[4]["params"]["field"], "fill", "fills binds the first fill")
        self.assertEqual(steps[5]["params"], {"component": 77, "parent": {"$step": 0}})
        self.assertEqual(steps[6]["params"], {"ids": [{"$step": 5}], "width": 300})
        self.assertEqual(made, [(0, "Card"), (2, "Hi"), (5, "frame")])
        sent = []

        def send(msg):
            sent.append(msg)
            return {"result": {"content": [{"type": "text", "text": json.dumps([{"id": 10 + i} for i in range(len(steps))])}]}}
        out = bridge.build({"id": 1, "method": "tools/call", "params": {"name": "build", "arguments": {"tree": tree}}}, send)
        self.assertEqual(sent[-1]["params"]["name"], "batch")
        self.assertEqual(json.loads(out["result"]["content"][0]["text"])[0], {"id": 10, "name": "Card"})
        self.assertEqual(layer_ids(out["result"]["content"][0]["text"]), {10, 12, 15}, "«Показать» finds the layers it made")
        self.assertTrue(bridge.build({"id": 2, "params": {"arguments": {"tree": [3]}}}, send)["result"]["isError"])


    def test_bridge_adds_styles_everywhere_and_variants_outside_lanes(self):
        names = lambda slot: [t["name"] for t in bridge.tools_for(slot)]  # noqa: E731
        self.assertEqual(names("0"), ["build", "styles", "variants", "lane"])
        self.assertEqual(names("2"), ["build", "styles"], "a lane can't start variants of its own")

    def test_tools_with_non_ascii_descriptions_survive_a_windows_code_page(self):
        """The agent reads the bridge's stdout as UTF-8: a code page (cp1252 on Windows) used to crash it on tools/list."""
        class Server(http.server.BaseHTTPRequestHandler):
            def do_POST(self):
                msg = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
                tool = {"name": "run_command", "description": "Команда → слой", "inputSchema": {"type": "object"}}
                body = json.dumps({"jsonrpc": "2.0", "id": msg["id"], "result": {"tools": [tool]}}).encode()
                self.send_response(200)
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, *args):
                pass
        server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Server)
        threading.Thread(target=server.serve_forever, daemon=True).start()
        self.addCleanup(server.shutdown)
        from desktop import windowless_python  # pythonw on Windows: its pipes must work too
        out = subprocess.run([windowless_python(), bridge.__file__, "--doc", "k", "--port", str(server.server_port), "--token", "t"],
                             input='{"jsonrpc":"2.0","id":1,"method":"tools/list"}\n'.encode(), capture_output=True, timeout=30,
                             env={**os.environ, "PYTHONIOENCODING": "cp1252", "PYTHONUTF8": "0"})
        self.assertEqual(out.returncode, 0, out.stderr.decode("utf-8", "replace"))
        tools = json.loads(out.stdout.decode("utf-8"))["result"]["tools"]
        self.assertEqual(tools[0]["description"], "Команда → слой")
        self.assertIn("build", [t["name"] for t in tools])


if __name__ == "__main__":
    unittest.main()
