"""The few desktop calls the CLI and the chat make, on Linux, macOS and Windows.

Each one is best effort: a missing tool (no notification daemon, no zenity) is skipped, not an error.
"""
import base64
import os
import shutil
import subprocess
import sys
import tempfile
import threading

MAC, WINDOWS = sys.platform == "darwin", sys.platform == "win32"


def _run(cmd, **kw):
    try:
        return subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", **kw)
    except OSError:
        return None


def _quote(s):
    """An AppleScript string literal."""
    return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'


def _ps(s):
    """A PowerShell single-quoted string literal."""
    return "'" + s.replace("'", "''") + "'"


def runtime_dir():
    """Where scratch files (screenshots for the agent) go."""
    return os.environ.get("XDG_RUNTIME_DIR") or tempfile.gettempdir()


def state_dir(app="figcraft-agent"):
    """Where an app keeps chats and logs: $XDG_STATE_HOME (Linux), ~/Library/Application Support, %LOCALAPPDATA%."""
    if WINDOWS:
        base = os.environ.get("LOCALAPPDATA") or os.path.expanduser("~")
    elif MAC:
        base = os.path.expanduser("~/Library/Application Support")
    else:
        base = os.environ.get("XDG_STATE_HOME") or os.path.expanduser("~/.local/state")
    return os.path.join(base, app)


def _b64(text):
    return base64.b64encode(text.encode("utf-8")).decode()


def copy(text):
    """Put text on the clipboard; False when no clipboard tool was found."""
    if MAC:
        cmd = ["pbcopy"]
    elif WINDOWS:  # the text goes as base64: pipes to PowerShell use the console's code page, not UTF-8
        cmd = ["powershell", "-NoProfile", "-Command",
               "Set-Clipboard ([Text.Encoding]::UTF8.GetString([Convert]::FromBase64String([Console]::In.ReadToEnd())))"]
        text = _b64(text)
    elif os.environ.get("WAYLAND_DISPLAY") and shutil.which("wl-copy"):
        cmd = ["wl-copy"]
    elif shutil.which("xclip"):
        cmd = ["xclip", "-selection", "clipboard"]
    elif shutil.which("xsel"):
        cmd = ["xsel", "--clipboard", "--input"]
    else:
        return False
    done = _run(cmd, input=text)
    return bool(done) and done.returncode == 0


def notify(app, title, body=""):
    if MAC:
        _run(["osascript", "-e", f"display notification {_quote(body)} with title {_quote(title)} subtitle {_quote(app)}"])
    elif WINDOWS:  # a balloon tip: the one toast PowerShell can show without extra modules
        _run(["powershell", "-NoProfile", "-Command",
              "Add-Type -AssemblyName System.Windows.Forms; $n = New-Object System.Windows.Forms.NotifyIcon; "
              "$n.Icon = [System.Drawing.SystemIcons]::Information; $n.Visible = $true; "
              f"$n.ShowBalloonTip(3000, {_ps(title)}, {_ps(body or app)}, 'None'); Start-Sleep 3; $n.Dispose()"])
    elif shutil.which("notify-send"):
        _run(["notify-send", "-a", app, "-t", "3000", title, body])


def notify_later(app, title, body=""):
    """notify() without waiting for it (the chat's server calls it from a request)."""
    threading.Thread(target=notify, args=(app, title, body), daemon=True).start()


def prompt(title, text):
    """Ask for one line of text in a dialog; None when cancelled or no dialog tool was found."""
    if MAC:
        done = _run(["osascript", "-e", f"text returned of (display dialog {_quote(text)} default answer \"\" "
                                        f"with title {_quote(title)})"])
    elif WINDOWS:
        done = _run(["powershell", "-NoProfile", "-Command", "Add-Type -AssemblyName Microsoft.VisualBasic; "
                     f"$r = [Microsoft.VisualBasic.Interaction]::InputBox({_ps(text)}, {_ps(title)}); "
                     "[Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($r))"])
        if done and not done.returncode:
            done.stdout = base64.b64decode(done.stdout.strip()).decode("utf-8")
    elif shutil.which("zenity"):
        done = _run(["zenity", "--entry", "--title", title, "--text", text, "--width", "480"])
    elif shutil.which("kdialog"):
        done = _run(["kdialog", "--title", title, "--inputbox", text])
    else:
        return None
    if not done or done.returncode:
        return None
    return done.stdout.strip() or None


def open_path(path):
    """Show a folder or file in the system's file manager or default app."""
    if WINDOWS:
        os.startfile(path)
        return
    try:
        subprocess.Popen(["open" if MAC else "xdg-open", path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except OSError:
        pass


def terminate(p):
    """Stop a child process. On Windows the whole tree: agent CLIs from npm run behind a .cmd shim."""
    p.stopped = True
    if WINDOWS:
        _run(["taskkill", "/T", "/F", "/PID", str(p.pid)])
    else:
        p.terminate()
