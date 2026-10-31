"""Each file an agent works in gets its own headless FigCraft, a guest in the app's live session of that file.

The app hosts the file (`collab.host`, this machine only); the guest joins it and runs the agent's MCP requests,
so its edits show in the app at once while agents in other files work too, whatever tab or workspace is in
front. The guest's undo history holds only the agent's steps.
"""
import json
import os
import subprocess
import sys
import threading
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "agent"))
from fc import FC, _cli  # noqa: E402


def host_link(fc, path):
    """The link of the app's own live session of file `path`; hosts it (opening the file) when there's none.
    Hosting acts on the active document, so the app switches to the file for a moment and back."""
    docs = fc.docs()
    back = next((i for i, d in enumerate(docs) if d.get("active")), None)
    idx = next((i for i, d in enumerate(docs) if d.get("path") == path), None)
    moved = idx is None
    if moved:
        idx = fc.cmd("file.open", path=path)["index"]  # opens it as the active tab
    mine = next((s for s in fc.cmd("collab.peers").get("sessions") or [] if s.get("document") == idx), None)
    if mine and mine.get("role") == "host" and mine.get("status") == "live" and mine.get("link"):
        link = mine["link"]
    elif mine and mine.get("status") in ("live", "connecting"):
        raise ValueError("файл уже в другой live-сессии: агенту нужна своя, локальная")
    else:
        moved = moved or idx != back
        fc.cmd("doc.switch", index=idx)
        link = fc.cmd("collab.host", bind="local")["link"]
    if moved and back is not None:
        fc.cmd("doc.switch", index=back)
    return link


class Guest(FC):
    """A headless FigCraft in the live session of one file; FC's helpers act on that file."""

    def __init__(self, path, link, name="Агент"):
        self.path, self.link, self.name = path, link, name
        self.lock = threading.Lock()
        self.used = time.time()
        self.p = subprocess.Popen(_cli() + ["mcp"], stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                  stderr=subprocess.DEVNULL, text=True, encoding="utf-8", bufsize=1)
        self.n = 0
        self.document = None
        # the name the agent's comments are signed with ("<name> (agent)"), as its cursor is named
        self.init = self.rpc("initialize", {"protocolVersion": "2025-06-18", "capabilities": {},
                                            "clientInfo": {"name": name, "version": "1"}})
        self._send({"jsonrpc": "2.0", "method": "notifications/initialized"})
        try:
            self.cmd("pref.userName", name=name)  # what the designer sees on the agent's cursor
        except RuntimeError:
            pass
        self.cmd("collab.join", link=link)
        for _ in range(80):
            peers = self.cmd("collab.peers")
            if peers.get("status") == "live":
                return
            if peers.get("status") == "failed":
                break
            time.sleep(0.25)
        self.close()
        raise RuntimeError(f"не подключился к файлу: {peers.get('reason') or peers.get('status')}")

    def live(self):
        if self.p.poll() is not None:
            return False
        try:
            with self.lock:
                return self.cmd("collab.peers").get("status") == "live"
        except (RuntimeError, OSError, ValueError):
            return False

    def run(self, fn):
        with self.lock:
            self.used = time.time()
            return fn(self)

    def forward(self, msg):
        """An agent's JSON-RPC request, answered by this FigCraft under the request's own id."""
        with self.lock:
            self.used = time.time()
            self.n += 1
            self._send({"jsonrpc": "2.0", "id": self.n, "method": msg.get("method"), "params": msg.get("params") or {}})
            while True:
                line = self.p.stdout.readline()
                if not line:
                    raise RuntimeError("FigCraft агента закрылся")
                try:
                    out = json.loads(line)
                except ValueError:
                    continue
                if out.get("id") == self.n:
                    out["id"] = msg.get("id")
                    return out

    def close(self):
        try:
            self.p.terminate()
            self.p.wait(5)
        except (OSError, subprocess.TimeoutExpired):
            self.p.kill()


class Guests:
    """The guests by file and slot; a new one when the session is gone (the tab was closed, the server restarted).
    Slot 0 is the chat's agent; variants' lanes get slots 1…N: each its own peer in the file's live session, so
    its own cursor and an undo history of its own steps only."""

    IDLE = 20 * 60

    def __init__(self, app_call):
        self.app_call = app_call  # runs fn(fc) on the attached app
        self.by_path = {}  # (path, slot) → Guest
        self.lock = threading.Lock()

    def get(self, path, slot=0, name=None):
        """The guest of (path, slot); `name` (who acts: the agent's name) gives a new one when the old one is
        someone else, since a connection keeps the name it began with. None takes whoever is there."""
        with self.lock:
            g = self.by_path.get((path, slot))
            if g and g.live() and name in (None, g.name):
                return g
            if g:
                g.close()
            g = Guest(path, self.app_call(lambda fc: host_link(fc, path)), name or "Агент")
            self.by_path[(path, slot)] = g
            return g

    def known(self, path, slot=0):
        g = self.by_path.get((path, slot))
        return g if g and g.p.poll() is None else None

    def reap(self, busy):
        """Close guests idle for IDLE seconds that no running turn uses; `busy` holds (path, slot)."""
        with self.lock:
            for key, g in list(self.by_path.items()):
                if key not in busy and time.time() - g.used > self.IDLE:
                    g.close()
                    del self.by_path[key]
