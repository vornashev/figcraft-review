"""python3 -m unittest sidecar/test_app.py — the tray app's decisions, without FigCraft, a tray or the network."""
import os
import socket
import sys
import threading
import unittest
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import app  # noqa: E402


class Plugin(unittest.TestCase):
    def test_import_only_when_missing_or_another_version(self):
        mine = {"id": "vornashev.figcraft-review", "version": "1.0.0"}
        self.assertTrue(app.needs_plugin([], mine))
        self.assertTrue(app.needs_plugin([{"id": mine["id"], "version": "0.9.0"}], mine))
        self.assertFalse(app.needs_plugin([{"id": "other", "version": "0.1"}, {"id": mine["id"], "version": "1.0.0"}], mine))

    def test_the_bundled_manifest_is_imported_into_figcraft(self):
        calls = []

        class Control:
            def __init__(self, *a, **kw):
                pass

            def call(self, method, **params):
                calls.append((method, params))
                return {"plugins": [{"id": "vornashev.figcraft-review", "version": "0.0.1"}]} if method == "plugin.list" else {}

            def close(self):
                pass
        a = app.App()
        with mock.patch.object(app, "Control", Control), mock.patch.object(a, "say") as say:
            a.ensure_plugin()
        self.assertEqual([m for m, _ in calls], ["plugin.list", "plugin.import"])
        self.assertEqual(calls[1][1]["path"], app.manifest())
        self.assertIn("обновлён", say.call_args[0][0])


class Start(unittest.TestCase):
    def test_a_second_start_hands_over_to_the_running_app(self):
        server = socket.socket()
        server.bind(("127.0.0.1", 0))
        server.listen()
        a = app.App()
        opened = threading.Event()
        a.start = opened.set
        threading.Thread(target=a.listen, args=(server,), daemon=True).start()
        with mock.patch.object(app, "PORT", server.getsockname()[1]):
            self.assertTrue(app.hand_over("open"))
        self.assertTrue(opened.wait(5))
        server.close()
        with mock.patch.object(app, "PORT", 1):
            self.assertFalse(app.hand_over("open"), "nothing listens: start the app")

    def test_figcraft_missing_or_running_without_its_port_is_said_not_started(self):
        a = app.App()
        with mock.patch.object(app, "control_up", return_value=False), mock.patch.object(a, "say") as say, \
                mock.patch.object(app.desktop, "detach") as detach:
            with mock.patch.object(app.desktop, "figcraft_app", return_value=None):
                self.assertFalse(a.ensure_figcraft())
            self.assertIn("не установлен", say.call_args[0][0])
            with mock.patch.object(app.desktop, "figcraft_app", return_value=(["figcraft"], None)), \
                    mock.patch.object(app.desktop, "process_running", return_value=True):
                self.assertFalse(a.ensure_figcraft())
            self.assertIn("без канала управления", say.call_args[0][0])
            detach.assert_not_called()


if __name__ == "__main__":
    unittest.main()
