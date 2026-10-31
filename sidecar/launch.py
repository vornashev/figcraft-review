#!/usr/bin/env python3
"""Opens the FigCraft Agent chat beside FigCraft; starts its server when it isn't running.

    launch.py [--server]     --server: only make sure the server runs

The chat page is rebuilt from web/src when a source is newer than the build (and npm is there). A server older than
its code is restarted unless an agent is at work in it. The chat opens as a Chromium-family app window (Chromium,
Chrome, Edge, Brave), else in the default browser; on Hyprland it goes to FigCraft's workspace, since FigCraft 0.11
answers only while its window is visible.
"""
import glob
import json
import os
import shutil
import signal
import subprocess
import sys
import time
import urllib.request
import webbrowser
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "agent"))
import desktop  # noqa: E402

WEB = os.path.join(HERE, "web")
PORT = int(os.environ.get("FIGCRAFT_AGENT_PORT", "7980"))
HOST = "figcraft-agent.localhost"  # Chromium resolves *.localhost itself; the window is named after the host
CLASS = f"chrome-{HOST}__-Default"  # Chromium names --app windows after the host; --class is ignored on Wayland
MAC, WINDOWS = desktop.MAC, desktop.WINDOWS


STATE = desktop.state_dir()
os.makedirs(STATE, exist_ok=True)
LOG = os.path.join(STATE, "server.log")
PIDFILE = os.path.join(STATE, "server.pid")


def log(line):
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now():%F %T} figcraft-agent: {line}\n")


def newest(*roots, pattern="*"):
    """The latest mtime of the files under roots matching pattern, 0 when none."""
    times = [os.path.getmtime(f) for r in roots for f in glob.glob(os.path.join(r, "**", pattern), recursive=True)
             if os.path.isfile(f)]
    return max(times, default=0)


def build_page():
    page = os.path.join(WEB, "dist", "index.html")
    built = os.path.getmtime(page) if os.path.exists(page) else 0
    files = [os.path.join(WEB, f) for f in ("index.html", "package.json")]
    sources = max([newest(os.path.join(WEB, "src"))] + [os.path.getmtime(f) for f in files if os.path.exists(f)])
    if built and built >= sources:
        return
    npm = shutil.which("npm")
    if not npm:
        if not built:
            print("figcraft-agent: the chat page isn't built and npm isn't installed", file=sys.stderr)
        return
    with open(LOG, "a", encoding="utf-8") as out:
        if not os.path.isdir(os.path.join(WEB, "node_modules")):
            subprocess.run([npm, "--prefix", WEB, "ci"], stdout=out, stderr=out)
        if subprocess.run([npm, "--prefix", WEB, "run", "build"], stdout=out, stderr=out).returncode:
            print(f"figcraft-agent: the chat page didn't build, see {LOG}", file=sys.stderr)


def server_state():
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{PORT}/api/state", timeout=2) as r:
            return json.load(r)
    except (OSError, ValueError):
        return None


def kill(pid):
    if WINDOWS:
        subprocess.run(["taskkill", "/T", "/F", "/PID", str(pid)], capture_output=True)
    else:
        try:
            os.kill(pid, signal.SIGTERM)
        except OSError:
            pass


def alive(pid):
    if WINDOWS:
        out = subprocess.run(["tasklist", "/FI", f"PID eq {pid}", "/NH"], capture_output=True, text=True, encoding="utf-8", errors="replace").stdout
        return str(pid) in out
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def restart_if_stale(state):
    """Stop a server this launcher started whose code changed since; not while an agent is at work in it."""
    try:
        with open(PIDFILE, encoding="utf-8") as f:
            pid, started = int(f.read()), os.path.getmtime(PIDFILE)
    except (OSError, ValueError):
        return state
    code = max(os.path.getmtime(f) for d in (HERE, os.path.join(HERE, "..", "agent"))
               for f in glob.glob(os.path.join(d, "*.py")) if not os.path.basename(f).startswith("test_"))
    if code <= started or not alive(pid):
        return state
    if state.get("running"):
        print("figcraft-agent: the server's code changed, but an agent is working: it restarts next time", file=sys.stderr)
        return state
    kill(pid)
    for _ in range(30):
        if not alive(pid):
            break
        time.sleep(0.1)
    log("restarted the server, its code changed")
    return None


def start_server():
    flags = {"creationflags": subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP} if WINDOWS \
        else {"start_new_session": True}
    with open(LOG, "a", encoding="utf-8") as out:
        p = subprocess.Popen([sys.executable, os.path.join(HERE, "server.py"), "--port", str(PORT)],
                             stdin=subprocess.DEVNULL, stdout=out, stderr=out, **flags)
    with open(PIDFILE, "w", encoding="utf-8") as f:
        f.write(str(p.pid))
    for _ in range(50):
        if server_state() is not None:
            return
        time.sleep(0.1)


def browser():
    """A Chromium-family browser that can open an --app window, or None."""
    names = ["chromium", "chromium-browser", "google-chrome", "google-chrome-stable", "brave-browser", "microsoft-edge"]
    found = [shutil.which(n) for n in names]
    if MAC:
        found += [f"/Applications/{app}.app/Contents/MacOS/{app}" for app in
                  ("Google Chrome", "Chromium", "Brave Browser", "Microsoft Edge")]
    if WINDOWS:
        roots = [os.environ.get(v, "") for v in ("ProgramFiles", "ProgramFiles(x86)", "LOCALAPPDATA")]
        found += [os.path.join(r, *rel) for r in roots for rel in
                  (("Google", "Chrome", "Application", "chrome.exe"), ("Microsoft", "Edge", "Application", "msedge.exe"),
                   ("BraveSoftware", "Brave-Browser", "Application", "brave.exe"))]
    return next((b for b in found if b and os.path.isfile(b)), None)


def detach(cmd):
    flags = {"creationflags": subprocess.DETACHED_PROCESS} if WINDOWS else {"start_new_session": True}
    subprocess.Popen(cmd, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, **flags)


def hypr_window(cls, field):
    """A field of the first Hyprland window of a class ("workspace.name"), or None."""
    out = subprocess.run(["hyprctl", "clients", "-j"], capture_output=True, text=True, encoding="utf-8").stdout
    for c in json.loads(out or "[]"):
        if c.get("class") == cls:
            for key in field.split("."):
                c = c.get(key) if isinstance(c, dict) else None
            return c
    return None


def open_chat():
    exe = browser()
    if not exe:
        webbrowser.open(f"http://127.0.0.1:{PORT}/")
        return
    app = [exe, f"--app=http://{HOST}:{PORT}/"]
    if not shutil.which("hyprctl"):
        detach(app)
        return
    win = hypr_window(CLASS, "address")
    if not win:
        detach(app)
        for _ in range(80):
            win = hypr_window(CLASS, "address")
            if win:
                break
            time.sleep(0.1)
        else:
            return
    subprocess.run(["hyprctl", "dispatch", f'hl.dsp.focus({{ window = "address:{win}" }})'], capture_output=True)
    ws = hypr_window("ai.storyteller.figcraft", "workspace.name")
    if ws and hypr_window(CLASS, "workspace.name") != ws:
        subprocess.run(["hyprctl", "dispatch", f'hl.dsp.window.move({{ workspace = "name:{ws}" }})'], capture_output=True)


def main(args):
    build_page()
    state = server_state()
    if state is not None:
        state = restart_if_stale(state)
    if state is None:
        start_server()
    if "--server" not in args:
        open_chat()


if __name__ == "__main__":
    main(sys.argv[1:])
