"""Coding agents behind the chat: find their CLI, list models, start one turn and read its events.

Every agent turns its own JSON lines into the same events:
  {"kind": "session", "id"}                         the agent's session, to resume the chat later
  {"kind": "delta", "text"}                         the answer as it is typed
  {"kind": "text", "text"}                          a finished piece of the answer (replaces the deltas)
  {"kind": "step", "id", "label", "status", "mut", "ids", "images"?}   a tool call: "run", then "ok" or "error";
                                                    mut: it changes the design, ids: layers it names,
                                                    images: pictures it returned ({"type", "data"} in base64)
  {"kind": "usage", "input"?, "output"?, "cacheRead"?, "cacheWrite"?, "turns"?, "context"?, "window"?}
                                                    tokens: the chat adds up the counts; context (what the last
                                                    request held) and window (its limit) are the latest
  {"kind": "done", "error"?, "cost"?, "denied"?}    the turn is over; denied: tools it wasn't allowed
"""
import json
import os
import re
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "agent"))
import skills  # noqa: E402
from desktop import NO_WINDOW  # noqa: E402

MODES = ("figcraft", "terminal")  # only FigCraft (+ reading files) | the agent's own settings, as in a terminal

# FigCraft tools and commands that only read; everything else of FigCraft's counts as a change.
READ_TOOLS = {"inspect_document", "get_node", "screenshot", "list_commands", "inspect_ui", "export", "open_file",
              "save_file", "select", "pointer", "key"}
READ_COMMANDS = ("list", "get", "inspect", "help", "view.", "select.", "ui.", "page.list", "page.select", "doc.list",
                 "version.list", "annotation.list", "annotation.categories", "comment.list", "style.list",
                 "variable.list", "component.list", "plugin.ui", "widget.list", "selection.colors", "file.save")


def short(s, n=70):
    s = " ".join(str(s or "").split())
    return s if len(s) <= n else s[: n - 1] + "…"


def unwrap(name, args):
    """(tool, args) with pi's MCP proxy (`mcp {tool, args}`) and the server prefixes taken off."""
    args = args if isinstance(args, dict) else {}
    if name in ("mcp", "mcp__figcraft") and args.get("tool"):
        name, args = str(args["tool"]), args.get("args") if isinstance(args.get("args"), dict) else {}
    return str(name).removeprefix("mcp__figcraft__").removeprefix("figcraft_").removeprefix("figcraft."), args


def figcraft_tool(raw):
    return str(raw).startswith(("mcp__figcraft", "figcraft")) or raw == "mcp"


def tool_label(name, args):
    """A tool call as a step line: «batch · Review UX», «Bash · ls design», «Read · lib.py»."""
    name, args = unwrap(name, args)
    for key in ("label", "command", "description", "filter", "file_path", "path", "pattern", "query", "id"):
        v = args.get(key)
        if v not in (None, "", []):
            if key in ("file_path", "path"):
                v = os.path.basename(str(v))
            if name in ("run_command", "Bash", "bash", "shell") and key == "command":
                v = str(v).removeprefix("/usr/bin/bash -lc ").strip("'\"")
            return f"{name} · {short(v, 60)}"
    return name


def changes_design(raw, args):
    """Whether a FigCraft tool call edits the document."""
    if not figcraft_tool(raw):
        return False
    name, args = unwrap(raw, args)
    if name == "run_command":
        return not str(args.get("command", "")).startswith(READ_COMMANDS)
    if name == "batch":
        return any(not str(c.get("command", "")).startswith(READ_COMMANDS)
                   for c in args.get("commands") or [] if isinstance(c, dict))
    if "." in name:  # pi calls commands as tools of their own
        return not name.startswith(READ_COMMANDS)
    return name not in READ_TOOLS


def layer_ids(obj, out=None, depth=0):
    """Layer ids named in a tool's arguments or result (keys id, ids, parent; JSON inside strings too)."""
    out = set() if out is None else out
    if depth > 12 or len(out) > 200:
        return out
    if isinstance(obj, str) and obj[:1] in "{[":
        try:
            return layer_ids(json.loads(obj), out, depth + 1)
        except ValueError:
            return out
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in ("id", "parent") and isinstance(v, int) and not isinstance(v, bool):
                out.add(v)
            elif k == "ids" and isinstance(v, list):
                out.update(i for i in v if isinstance(i, int) and not isinstance(i, bool))
            else:
                layer_ids(v, out, depth + 1)
    elif isinstance(obj, list):
        for v in obj:
            layer_ids(v, out, depth + 1)
    return out


def result_images(obj, out=None, depth=0):
    """Pictures in a tool's result, as {"type", "data"}: MCP's {type: image, data, mimeType} and Claude's
    {type: image, source: {media_type, data}}."""
    out = [] if out is None else out
    if depth > 6 or len(out) >= 8:
        return out
    if isinstance(obj, dict):
        src = obj.get("source") if isinstance(obj.get("source"), dict) else obj
        if obj.get("type") == "image" and isinstance(src.get("data"), str):
            out.append({"type": src.get("media_type") or src.get("mimeType") or "image/png", "data": src["data"]})
        else:
            for v in obj.values():
                result_images(v, out, depth + 1)
    elif isinstance(obj, list):
        for v in obj:
            result_images(v, out, depth + 1)
    return out


def step_end(id_, error, result):
    step = {"kind": "step", "id": id_, "status": "error" if error else "ok", "ids": sorted(layer_ids(result))}
    images = result_images(result)
    if images:
        step["images"] = images
    return step


def step_start(id_, raw, args):
    mut = changes_design(raw, args)
    step = {"kind": "step", "id": id_, "label": tool_label(raw, args), "status": "run", "mut": mut,
            "ids": sorted(layer_ids(unwrap(raw, args)[1])) if mut else []}
    skill = skills.named(raw, args)
    if skill:
        step["skill"] = skill  # it opens a design skill: the answer names it as taken by the agent itself
    return step


def claude_usage(e):
    """A Claude result's tokens: the turn's totals, the context of its last request, the model's window."""
    u = e.get("usage") or {}
    last = (u.get("iterations") or [u])[-1]
    out = {"kind": "usage", "input": u.get("input_tokens", 0), "output": u.get("output_tokens", 0),
           "cacheRead": u.get("cache_read_input_tokens", 0), "cacheWrite": u.get("cache_creation_input_tokens", 0),
           "turns": e.get("num_turns") or len(u.get("iterations") or []),
           "context": sum(last.get(k, 0) for k in ("input_tokens", "cache_read_input_tokens", "cache_creation_input_tokens"))}
    windows = [m.get("contextWindow") for m in (e.get("modelUsage") or {}).values() if m.get("contextWindow")]
    if windows:
        out["window"] = max(windows)
    return out


class Agent:
    id = name = binary = ""

    def path(self):
        return shutil.which(self.binary)

    def env(self):
        """Variables this agent's process gets on top of the server's (None: remove it)."""
        return {}

    def version(self):
        try:
            out = subprocess.run([self.path(), "--version"], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=10, **NO_WINDOW).stdout
            return out.strip().splitlines()[0] if out.strip() else ""
        except (OSError, subprocess.SubprocessError, TypeError):
            return ""

    def info(self):
        p = self.path()
        return {"id": self.id, "name": self.name, "path": p, "ok": bool(p), "version": self.version() if p else "",
                "models": self.models() if p else [], "allows": self.allows(), "account": self.account()}

    def account(self):
        """The account's config folder, for an agent that is a second login of another."""
        return None

    def models(self):
        return []

    def allows(self):
        """Whether a chat can grant this agent the tools it was refused."""
        return False

    def stdin(self):
        """Whether the prompt goes to stdin (else it is the last argument)."""
        return True

    def system_in_prompt(self):
        """Whether the system text goes at the top of the first prompt (no flag for it)."""
        return False


class Claude(Agent):
    id, name, binary = "claude", "Claude Code", "claude"
    MODELS = [("claude-fable-5-1", "Fable 5.1"), ("claude-opus-5-5", "Opus 5.5"), ("claude-sonnet-5-5", "Sonnet 5.5"),
              ("claude-haiku-5-5", "Haiku 5.5")]

    def models(self):
        return [{"id": i, "name": n} for i, n in self.MODELS]

    def allows(self):
        return True

    def env(self):
        return {"CLAUDE_CONFIG_DIR": None}  # the default login, even when the server was started from another one

    def command(self, model, session, mcp_file, system, mode, allow=(), images=()):
        cmd = [self.path(), "-p", "--output-format", "stream-json", "--verbose", "--include-partial-messages",
               "--model", model, "--mcp-config", mcp_file, "--strict-mcp-config", "--append-system-prompt", system]
        tools = (["mcp__figcraft", "Read", "Glob", "Grep"] if mode == "figcraft" else []) + list(allow)
        if mode == "figcraft":  # ask-mode in -p denies whatever isn't allowed, and says so in the result
            # only the tools it may use or be granted (Bash, Edit, Write: refused, they offer «Разрешить») are defined,
            # no Agent, ScheduleWakeup… nor ToolSearch, so figcraft's aren't deferred, and no listing of the login's
            # own skills: ~6k tokens less on every request
            builtin = {"Bash", "Edit", "Write"} | {t.split("(")[0] for t in tools if not t.startswith("mcp__")}
            cmd += ["--permission-mode", "default", "--disable-slash-commands", "--tools", *sorted(builtin)]
        if tools:
            cmd += ["--allowedTools", *tools]
        if session:
            cmd += ["--resume", session]
        return cmd

    def parse(self, e):
        t = e.get("type")
        if t == "system" and e.get("subtype") == "init":
            return [{"kind": "session", "id": e.get("session_id")}]
        if t == "stream_event":
            ev = e.get("event") or {}
            d = ev.get("delta") or {}
            if ev.get("type") == "content_block_delta" and d.get("type") == "text_delta" and d.get("text"):
                return [{"kind": "delta", "text": d["text"]}]
            return []
        if t == "assistant":
            out = []
            for c in (e.get("message") or {}).get("content") or []:
                if c.get("type") == "text" and c.get("text", "").strip():
                    out.append({"kind": "text", "text": c["text"]})
                elif c.get("type") == "tool_use":
                    out.append(step_start(c.get("id"), c.get("name"), c.get("input")))
            return out
        if t == "user":
            content = (e.get("message") or {}).get("content")
            if not isinstance(content, list):
                return []
            return [step_end(c.get("tool_use_id"), c.get("is_error"), c.get("content"))
                    for c in content if isinstance(c, dict) and c.get("type") == "tool_result"]
        if t == "result":
            done = {"kind": "done", "cost": e.get("total_cost_usd")}
            if e.get("is_error"):
                done["error"] = short(e.get("result") or e.get("subtype") or "ошибка", 300)
            denied = [{"tool": d.get("tool_name"), "label": tool_label(d.get("tool_name"), d.get("tool_input"))}
                      for d in e.get("permission_denials") or [] if isinstance(d, dict) and d.get("tool_name")]
            if denied:
                done["denied"] = denied
            return [{"kind": "session", "id": e.get("session_id")}, claude_usage(e), done]
        return []


class Codex(Agent):
    id, name, binary = "codex", "Codex", "codex"
    CACHE = os.path.expanduser("~/.codex/models_cache.json")

    def models(self):
        try:
            d = json.load(open(self.CACHE, encoding="utf-8"))
            ms = d.get("models", d) if isinstance(d, dict) else d
            ids = [m.get("slug") or m.get("id") for m in ms if isinstance(m, dict)]
        except (OSError, ValueError):
            ids = []
        ids = [i for i in ids if i and "review" not in i and "reserve" not in i] or ["gpt-6.1-sol"]
        return [{"id": i, "name": self.title(i)} for i in ids]

    @staticmethod
    def title(slug):
        """gpt-6.1-sol → GPT-6.1 Sol."""
        p = slug.split("-")
        return f"GPT-{p[1]} " + " ".join(w.title() for w in p[2:]) if p[0] == "gpt" and len(p) > 1 else slug

    def system_in_prompt(self):
        return True

    def command(self, model, session, mcp_file, system, mode, allow=(), images=()):
        with open(mcp_file, encoding="utf-8") as f:  # Codex takes MCP servers as config overrides, not a file
            srv = json.load(f)["mcpServers"]["figcraft"]
        conf = ["-c", f"mcp_servers.figcraft.command={json.dumps(srv['command'])}",
                "-c", f"mcp_servers.figcraft.args={json.dumps(srv['args'])}",
                # with approval_policy never, a tool Codex would ask about (any that writes) is refused instead
                "-c", 'mcp_servers.figcraft.default_tools_approval_mode="approve"',
                "-c", 'approval_policy="never"',
                # a config override, not -s: `exec resume` has no -s
                "-c", f'sandbox_mode="{"read-only" if mode == "figcraft" else "workspace-write"}"']
        head = [self.path(), "exec"] + (["resume", session] if session else [])
        pics = [x for p in images for x in ("-i", p)]
        return head + ["--json", "--skip-git-repo-check", "-m", model] + conf + pics + ["-"]

    def parse(self, e):
        t = e.get("type")
        if t == "thread.started":
            return [{"kind": "session", "id": e.get("thread_id")}]
        if t in ("item.started", "item.completed"):
            it = e.get("item") or {}
            kind = it.get("type")
            if kind == "agent_message":
                return [{"kind": "text", "text": it.get("text", "")}] if t == "item.completed" and it.get("text") else []
            if kind in ("reasoning", None):
                return []
            if kind == "mcp_tool_call":
                raw, args = "mcp__figcraft__" + str(it.get("tool")), it.get("arguments")
            elif kind == "command_execution":
                raw, args = "shell", {"command": it.get("command")}
            elif kind == "file_change":
                raw, args = "файлы", {"description": ", ".join(os.path.basename(c.get("path", "")) for c in it.get("changes") or [])}
            elif kind == "web_search":
                raw, args = "поиск", {"query": it.get("query")}
            else:
                raw, args = kind, {}
            step = step_start(it.get("id"), raw, args)
            if t == "item.started":
                return [step]
            bad = it.get("status") == "failed" or (it.get("exit_code") not in (None, 0)) or it.get("error")
            step["status"] = "error" if bad else "ok"
            if step["mut"]:
                step["ids"] = sorted(set(step["ids"]) | layer_ids(it.get("result")))
            images = result_images(it.get("result"))
            if images:
                step["images"] = images
            return [step]
        if t == "turn.completed":
            u = e.get("usage") or {}  # its input counts the cached part too
            cached = u.get("cached_input_tokens", 0)
            return [{"kind": "usage", "input": u.get("input_tokens", 0) - cached, "output": u.get("output_tokens", 0),
                     "cacheRead": cached, "cacheWrite": u.get("cache_write_input_tokens", 0)}, {"kind": "done"}]
        if t in ("turn.failed", "error"):
            err = e.get("error") or e.get("message") or "ошибка"
            return [{"kind": "done", "error": short(err.get("message") if isinstance(err, dict) else err, 300)}]
        return []


class Pi(Agent):
    id, name, binary = "pi", "pi", "pi"

    def models(self):
        try:
            out = subprocess.run([self.path(), "--list-models"], capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=20, **NO_WINDOW).stdout
        except (OSError, subprocess.SubprocessError):
            return []
        rows = [line.split() for line in out.splitlines()[1:] if line.strip()]
        return [{"id": f"{r[0]}/{r[1]}", "name": f"{r[1]} · {r[0]}"} for r in rows if len(r) >= 2]

    def stdin(self):
        return False

    def command(self, model, session, mcp_file, system, mode, allow=(), images=()):
        cmd = [self.path(), "-p", "--mode", "json", "--model", model, "--mcp-config", mcp_file, "--append-system-prompt", system]
        if mode == "figcraft":
            cmd += ["--tools", "read,grep,find,ls,mcp,mcp__figcraft"]  # pi reaches MCP servers through «mcp»
        if session:
            cmd += ["--session", session]
        return cmd

    def parse(self, e):
        t = e.get("type")
        if t == "session":
            return [{"kind": "session", "id": e.get("id")}]
        if t == "message_update":
            a = e.get("assistantMessageEvent") or {}
            return [{"kind": "delta", "text": a["delta"]}] if a.get("type") == "text_delta" and a.get("delta") else []
        if t == "message_end" and (e.get("message") or {}).get("role") == "assistant":
            u = e["message"].get("usage") or {}
            got = {k: u.get(k, 0) for k in ("input", "output", "cacheRead", "cacheWrite")}
            return [{"kind": "text", "text": c["text"]} for c in e["message"].get("content") or []
                    if isinstance(c, dict) and c.get("type") == "text" and c.get("text", "").strip()] + (
                [{"kind": "usage", **got, "turns": 1, "context": got["input"] + got["cacheRead"] + got["cacheWrite"]}] if u else [])
        if t == "tool_execution_start":
            return [step_start(e.get("toolCallId"), e.get("toolName"), e.get("args"))]
        if t == "tool_execution_end":
            return [step_end(e.get("toolCallId"), e.get("isError"), (e.get("result") or {}).get("content"))]
        if t == "agent_end":
            return [{"kind": "done"}]
        if t == "error":
            return [{"kind": "done", "error": short(e.get("message") or e.get("error"), 300)}]
        return []


class ClaudeAccount(Claude):
    """Another Claude Code login: the same CLI with its own CLAUDE_CONFIG_DIR (`alias claude-2='CLAUDE_CONFIG_DIR=… claude'`)."""

    def __init__(self, alias, folder):
        self.id, self.name, self.folder = f"claude:{alias}", f"Claude Code · {alias}", folder

    def env(self):
        return {"CLAUDE_CONFIG_DIR": self.folder}

    def account(self):
        return self.folder


RC_FILES = ("~/.bashrc", "~/.bash_aliases", "~/.zshrc", "~/.profile", "~/.config/fish/config.fish")
ALIAS = re.compile(r"""^\s*alias\s+([\w.-]+)\s*=?\s*(['"])\s*(?:env\s+)?CLAUDE_CONFIG_DIR=(["']?)(\S+?)\3\s+claude\b[^'"]*\2""", re.M)


def claude_accounts(rc_files=RC_FILES, home=None):
    """Claude Code logins besides ~/.claude: the shell aliases that set CLAUDE_CONFIG_DIR, then the ~/.claude-*
    folders with a login that no alias names (named after the folder)."""
    home = home or os.path.expanduser("~")
    found = {}
    for rc in rc_files:
        try:
            with open(home + rc[1:] if rc.startswith("~") else rc, encoding="utf-8", errors="replace") as f:
                text = f.read()
        except OSError:
            continue
        for m in ALIAS.finditer(text):
            d = m.group(4).replace("${HOME}", home).replace("$HOME", home)
            d = os.path.normpath(home + d[1:] if d.startswith("~") else d)
            if m.group(1) != "claude" and d != os.path.join(home, ".claude") and d not in found.values():
                found[m.group(1)] = d
    for name in sorted(os.listdir(home)) if os.path.isdir(home) else []:
        d = os.path.join(home, name)
        if (name.startswith(".claude-") and d not in found.values() and os.path.isdir(d)
                and any(os.path.isfile(os.path.join(d, f)) for f in (".credentials.json", ".claude.json"))):
            found.setdefault(name[1:], d)
    return [ClaudeAccount(a, d) for a, d in found.items()]


AGENTS = {a.id: a for a in (Claude(), *claude_accounts(), Codex(), Pi())}
