"""FigCraft's control channel (`figcraft --control 7979`), spoken directly: JSON lines over the loopback.

The MCP backend (agent/fc.py) covers the document and acts as an agent; this covers what is the designer's own
(comments signed with their name) and the app's event log (`events.poll`). One connection per caller, since a
reply comes back on the connection that asked, and a poll holds its connection until it answers.
"""
import json
import socket
import threading


class Control:
    def __init__(self, port=7979, timeout=70):
        self.port, self.timeout = port, timeout
        self.sock, self.file, self.n = None, None, 0
        self.lock = threading.Lock()

    def _connect(self):
        self.sock = socket.create_connection(("127.0.0.1", self.port), timeout=self.timeout)
        self.file = self.sock.makefile("rwb")

    def close(self):
        if self.sock:
            try:
                self.sock.close()
            except OSError:
                pass
        self.sock = self.file = None

    def call(self, method, **params):
        """The method's result; RuntimeError with the app's message when it fails, OSError when the app is gone."""
        with self.lock:
            for attempt in (0, 1):  # the app drops idle connections after 60 s: reconnect once
                try:
                    if self.sock is None:
                        self._connect()
                    self.n += 1
                    self.file.write(json.dumps({"id": self.n, "method": method, "params": params}, ensure_ascii=False).encode() + b"\n")
                    self.file.flush()
                    line = self.file.readline()
                    if not line:
                        raise ConnectionResetError("FigCraft closed the control connection")
                    break
                except OSError:
                    self.close()
                    if attempt:
                        raise
            out = json.loads(line)
        if not out.get("ok"):
            raise RuntimeError(out.get("error") or "control request failed")
        return out.get("result")
