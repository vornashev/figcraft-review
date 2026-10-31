"""desktop.py picks the right tool per platform: the calls are mocked, so every branch runs on any OS."""
import base64
import os
import subprocess
import sys
import unittest
from unittest import mock

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import desktop  # noqa: E402


def done(out="", code=0):
    return subprocess.CompletedProcess([], code, out, "")


class Desktop(unittest.TestCase):
    def on(self, system, tools=(), env=None):
        """Pretend to be on system ('mac', 'windows' or 'linux') with these tools on PATH."""
        for p in (mock.patch.object(desktop, "MAC", system == "mac"), mock.patch.object(desktop, "WINDOWS", system == "windows"),
                  mock.patch.object(desktop.shutil, "which", lambda t: t in tools and "/usr/bin/" + t),
                  mock.patch.dict(os.environ, env or {}, clear=False)):
            p.start()
            self.addCleanup(p.stop)
        run = mock.patch.object(desktop.subprocess, "run", return_value=done("Кнопка мелкая\n")).start()
        self.addCleanup(mock.patch.stopall)
        return run

    def test_copy_per_platform(self):
        for system, tools, env, cmd in [("mac", (), {}, "pbcopy"), ("windows", (), {}, "powershell"),
                                        ("linux", ("wl-copy", "xclip"), {"WAYLAND_DISPLAY": "wayland-1"}, "wl-copy"),
                                        ("linux", ("xclip",), {"WAYLAND_DISPLAY": ""}, "xclip")]:
            with self.subTest(system=system, cmd=cmd):
                run = self.on(system, tools, env)
                self.assertTrue(desktop.copy("# FigCraft — 2 замечания"))
                self.assertEqual(run.call_args.args[0][0], cmd)
                sent = run.call_args.kwargs["input"]
                if system == "windows":  # base64, past PowerShell's code page
                    sent = base64.b64decode(sent).decode("utf-8")
                self.assertEqual(sent, "# FigCraft — 2 замечания")
                mock.patch.stopall()

    def test_copy_without_a_tool(self):
        run = self.on("linux", (), {"WAYLAND_DISPLAY": ""})
        self.assertFalse(desktop.copy("x"))
        run.assert_not_called()

    def test_prompt(self):
        for system, tools, cmd in [("mac", (), "osascript"), ("windows", (), "powershell"), ("linux", ("zenity",), "zenity"),
                                   ("linux", ("kdialog",), "kdialog")]:
            with self.subTest(cmd=cmd):
                run = self.on(system, tools)
                if system == "windows":
                    run.return_value = done(base64.b64encode("Кнопка мелкая".encode()).decode() + "\r\n")
                self.assertEqual(desktop.prompt("Замечание #3", "К «Title»"), "Кнопка мелкая")
                self.assertEqual(run.call_args.args[0][0], cmd)
                mock.patch.stopall()

    def test_prompt_cancelled_or_missing(self):
        run = self.on("linux", ("zenity",))
        run.return_value = done("", 1)
        self.assertIsNone(desktop.prompt("t", "x"))
        mock.patch.stopall()
        self.on("linux", ())
        self.assertIsNone(desktop.prompt("t", "x"))

    def test_quoting(self):
        self.assertEqual(desktop._quote('say "hi" \\ bye'), '"say \\"hi\\" \\\\ bye"')
        self.assertEqual(desktop._ps("it's"), "'it''s'")

    def test_terminate_marks_the_process(self):
        p = mock.Mock(pid=42)
        run = self.on("windows")
        desktop.terminate(p)
        self.assertTrue(p.stopped)
        self.assertEqual(run.call_args.args[0], ["taskkill", "/T", "/F", "/PID", "42"])
        mock.patch.stopall()
        self.on("linux")
        desktop.terminate(p)
        p.terminate.assert_called_once()


if __name__ == "__main__":
    unittest.main()
