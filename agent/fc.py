"""Minimal MCP client for FigCraft.

Attaches to the running app (`figcraft --control PORT`) through `figcraft-cli mcp --attach`, or,
with FIGCRAFT_FILE (or `file=`), opens that file in a headless session (tests; nothing is saved).
"""
import base64
import glob
import json
import os
import shutil
import subprocess
import sys
import time

import desktop
from desktop import NO_WINDOW


def _cli():
    if os.environ.get("FIGCRAFT_CLI"):
        return [os.environ["FIGCRAFT_CLI"]]
    if shutil.which("figcraft-cli"):
        return ["figcraft-cli"]
    images = sorted(glob.glob(os.path.expanduser("~/Applications/figcraft-*.AppImage")))
    if images:
        return [images[-1], "cli"]
    # The MSI and the portable zip put figcraft-cli.exe beside figcraft.exe; on macOS it comes as its own zip.
    for exe in [os.path.join(os.environ.get(v, ""), "ArtCraft", "FigCraft", "figcraft-cli.exe")
                for v in ("ProgramW6432", "ProgramFiles", "ProgramFiles(x86)")] + [os.path.expanduser("~/bin/figcraft-cli")]:
        if os.path.isfile(exe):
            return [exe]
    # macOS: the FigCraft Review app downloads the CLI matching the installed FigCraft (sidecar/app.py)
    fetched = glob.glob(os.path.join(desktop.state_dir(), "figcraft-cli", "*", "figcraft-cli"))
    if fetched:
        return [max(fetched, key=os.path.getmtime)]
    if shutil.which("figcraft"):
        return ["figcraft", "cli"]
    raise SystemExit("figcraft-cli not found: set FIGCRAFT_CLI")


# The tools that take `document` (FigCraft 0.13): the call acts on that open file, the tab in front stays.
DOC_TOOLS = {"run_command", "batch", "create_node", "set_properties", "inspect_document", "get_node", "select", "export",
             "screenshot", "save_file", "undo", "redo"}


class FC:
    """`name` is who FigCraft says acts (comments are signed "<name> (agent)"); FIGCRAFT_AGENT overrides it.
    `document` (an open file's id or path; FIGCRAFT_DOCUMENT) pins every call to that file, whatever tab is in front."""

    def __init__(self, port=None, file=None, name="figcraft-review", document=None):
        file = file or os.environ.get("FIGCRAFT_FILE")
        port = str(port or os.environ.get("FIGCRAFT_PORT", "7979"))
        self.p = subprocess.Popen(_cli() + (["mcp"] if file else ["mcp", "--attach", port]), stdin=subprocess.PIPE,
                                  stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, text=True, encoding="utf-8", bufsize=1,
                                  **NO_WINDOW)
        self.n = 0
        self.document = None if file else document or os.environ.get("FIGCRAFT_DOCUMENT") or None
        self.rpc("initialize", {"protocolVersion": "2025-06-18", "capabilities": {},
                                "clientInfo": {"name": os.environ.get("FIGCRAFT_AGENT") or name, "version": "1"}})
        self._send({"jsonrpc": "2.0", "method": "notifications/initialized"})
        if file:
            self.tool("open_file", {"path": os.path.abspath(file)})

    def _send(self, msg):
        self.p.stdin.write(json.dumps(msg) + "\n")
        self.p.stdin.flush()

    def rpc(self, method, params):
        self.n += 1
        self._send({"jsonrpc": "2.0", "id": self.n, "method": method, "params": params})
        while True:
            line = self.p.stdout.readline()
            if not line:
                raise RuntimeError("figcraft-cli closed the connection (is the app running with --control?)")
            m = json.loads(line)
            if m.get("id") == self.n:
                if "error" in m:
                    raise RuntimeError(m["error"])
                return m["result"]

    def call(self, name, args, retries=12):
        """Raw tools/call result; retries while the app window is hidden."""
        if self.document is not None and name in DOC_TOOLS and "document" not in args:
            args = {**args, "document": self.document}
        r = self.rpc("tools/call", {"name": name, "arguments": args})
        if r.get("isError"):
            txt = "".join(c.get("text", "") for c in r.get("content", []) if c.get("type") == "text")
            # The app answers only while its window is on screen (another workspace pauses it). A request it never
            # started "was not applied" and is safe to send again; one it is "still running" will take effect, so
            # sending it again would apply it twice.
            if ("waiting for the UI" in txt or "it was not applied" in txt) and retries:
                if retries == 12:
                    print("FigCraft window is hidden; waiting for it…", file=sys.stderr)
                time.sleep(5)
                return self.call(name, args, retries - 1)
            raise RuntimeError(txt[:2000])
        return r

    def tool(self, name, args, retries=12):
        r = self.call(name, args, retries)
        txt = "".join(c.get("text", "") for c in r.get("content", []) if c.get("type") == "text")
        try:
            return json.loads(txt)
        except ValueError:
            return txt

    def shot(self, id, path, max_size=1000, scale=None):
        """Save a PNG of one layer to `path` (look at it with Read only when needed)."""
        r = self.call("screenshot", {"ids": [id], "maxSize": max_size} | ({"scale": scale} if scale else {}))
        img = next(c for c in r["content"] if c.get("type") == "image")
        with open(path, "wb") as f:
            f.write(base64.b64decode(img["data"]))
        return path

    def cmd(self, command, **params):
        return self.tool("run_command", {"command": command, "params": params})

    def batch(self, commands, label="Batch"):
        return self.tool("batch", {"commands": commands, "label": label})

    def node(self, id, depth=1, fields=None):
        """One layer to `depth`; `fields` keeps only those properties (ids and children always come)."""
        return self.tool("get_node", {"id": id, "depth": depth} | ({"fields": fields} if fields is not None else {}))

    def docs(self):
        """The open files as doc.list gives them, each with its `path`: an agent's doc.list names no paths
        (FigCraft 0.13), so each file's path comes from inspecting it in place."""
        out = self.cmd("doc.list")
        for d in out:
            if "path" not in d:
                d["path"] = self.tool("inspect_document", {"depth": 0, "document": d["id"]}).get("path")
        return out

    def doc(self, depth=0):
        return self.tool("inspect_document", {"depth": depth})

    def tops(self, doc=None, page=None):
        """Top-level layers of page `page` (default: the current one)."""
        doc = doc or self.doc(1)
        page = page or doc.get("currentPage", doc["pages"][0]["id"])
        listed = next((p for p in doc["pages"] if p["id"] == page), {})
        if "children" in listed:
            return listed["children"]
        return self.node(page, 1).get("children") or []

