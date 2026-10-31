#!/usr/bin/env python3
"""FigCraft Review as an app: one click starts FigCraft with its control port, imports the plugin, starts the chat's
server and opens the chat. An icon in the tray (the menu bar on macOS) keeps the quick actions and the updates.

    app.py            the app; a second start only opens the chat of the one running
    app.py --check    start the chat's server, check that it answers and stop it: the installers' smoke test
    app.py --quit     stop the running app and the chat's server (the uninstaller does)

The tray needs pystray and Pillow (the installers carry them); without them the app still starts everything once.
"""
import hashlib
import io
import json
import os
import socket
import subprocess
import sys
import threading
import time
import urllib.request
import webbrowser
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "agent"))
import desktop  # noqa: E402
import launch  # noqa: E402
import update  # noqa: E402
from control import Control  # noqa: E402

PORT = int(os.environ.get("FIGCRAFT_APP_PORT", "7981"))  # the running app listens here for a second start
CONTROL = int(os.environ.get("FIGCRAFT_PORT", "7979"))
REVIEW = os.path.join(HERE, "..", "agent", "review.py")
FIGCRAFT_RELEASES = "https://github.com/storytold/figcraft/releases/latest"
NAME = "FigCraft Review"


def manifest():
    """The plugin's manifest this copy carries: plugin/ in a release, the repository's own in a checkout."""
    for path in (os.path.join(update.ROOT, "plugin", "figcraft-plugin.json"), os.path.join(update.ROOT, "figcraft-plugin.json")):
        if os.path.isfile(path):
            return path
    return None


def hand_over(command="open"):
    """Ask a running app to do `command`; False when none runs."""
    try:
        with socket.create_connection(("127.0.0.1", PORT), timeout=2) as s:
            s.sendall(command.encode() + b"\n")
            return s.makefile().readline().strip() == "ok"
    except OSError:
        return False


def control_up():
    try:
        socket.create_connection(("127.0.0.1", CONTROL), timeout=1).close()
        return True
    except OSError:
        return False


def needs_plugin(plugins, mine):
    """Whether FigCraft's plugin list lacks this copy's plugin (its id at its version)."""
    have = next((p for p in plugins if p.get("id") == mine["id"]), None)
    return have is None or have.get("version") != mine["version"]


def cli_path(version):
    """Where the app keeps the macOS figcraft-cli matching FigCraft `version` (fc.py looks there)."""
    return os.path.join(desktop.state_dir(), "figcraft-cli", version, "figcraft-cli")


class App:
    def __init__(self):
        self.icon = None
        self.found = None  # the available update, as update.summary() gives it
        self.plugin_checked = False
        self.busy = threading.Lock()

    def say(self, title, body=""):
        desktop.notify_later(NAME, title, body)
        launch.log(f"{title} {body}".strip())

    # ---- what one click starts ----

    def start(self):
        self.ensure_figcraft()
        self.ensure_cli()
        state = launch.server_state()
        if state is not None:
            state = launch.restart_if_stale(state)
        if state is None:
            launch.start_server()
        launch.open_chat()

    def ensure_figcraft(self):
        """FigCraft with its control port, which the CLI and the chat attach to."""
        if control_up():
            return True
        app = desktop.figcraft_app()
        if not app:
            self.say("FigCraft не установлен", "Установите его: " + FIGCRAFT_RELEASES)
            return False
        if desktop.process_running("figcraft"):
            self.say("FigCraft запущен без канала управления", "Закройте FigCraft и нажмите «Запустить FigCraft» в меню FigCraft Review")
            return False
        desktop.detach(app[0] + ["--control", str(CONTROL)])
        for _ in range(60):
            if control_up():
                return True
            time.sleep(0.5)
        self.say("FigCraft не открыл канал управления", f"Порт {CONTROL} не отвечает")
        return False

    def ensure_cli(self):
        """macOS: FigCraft's CLI comes as its own download; fetch the one matching the installed app."""
        if not desktop.MAC or os.environ.get("FIGCRAFT_CLI"):
            return
        app = desktop.figcraft_app()
        version = app and app[1]
        if not version or os.path.isfile(cli_path(version)):
            return
        name = f"figcraft-cli-{version}-macos-universal.zip"
        base = f"https://github.com/storytold/figcraft/releases/download/v{version}/"
        try:
            sums = dict(reversed(line.split(None, 1)) for line in update._get(base + "SHA256SUMS.txt").decode().splitlines() if line.strip())
            expected = (sums.get(name) or sums.get("*" + name) or "").strip()
            self.say("Скачиваю figcraft-cli", f"FigCraft {version}, один раз")
            data = update._get(base + name, timeout=900)
            if hashlib.sha256(data).hexdigest() != expected:
                raise ValueError("контрольная сумма не совпала")
            target = cli_path(version)
            os.makedirs(os.path.dirname(target), exist_ok=True)
            with zipfile.ZipFile(io.BytesIO(data)) as z:
                member = next(n for n in z.namelist() if n.endswith("/figcraft-cli"))
                with z.open(member) as src, open(target + ".part", "wb") as out:
                    out.write(src.read())
            os.chmod(target + ".part", 0o755)
            os.replace(target + ".part", target)
        except (OSError, ValueError, StopIteration, zipfile.BadZipFile) as e:
            self.say("figcraft-cli не скачан", str(e)[:200])

    def ensure_plugin(self):
        """Import this copy's plugin when FigCraft lacks it or has another version: the same id replaces the old."""
        path = manifest()
        if not path:
            return
        ctl = Control(CONTROL, timeout=20)
        try:
            with open(path, encoding="utf-8") as f:
                mine = json.load(f)
            plugins = (ctl.call("plugin.list") or {}).get("plugins") or []
            if needs_plugin(plugins, mine):
                ctl.call("plugin.import", path=path)
                fresh = not any(p.get("id") == mine["id"] for p in plugins)
                self.say(f"Плагин {'установлен' if fresh else 'обновлён'}: {mine['version']}", "Plugins ▸ Review в FigCraft")
        except (OSError, RuntimeError, ValueError) as e:
            launch.log(f"plugin import: {e}")
        finally:
            ctl.close()

    # ---- the tray's actions ----

    def review(self, *args):
        """Run review.py like a hotkey would: it notifies about what it did."""
        subprocess.Popen([sys.executable, REVIEW, *args], stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                         stderr=subprocess.DEVNULL, **desktop.NO_WINDOW)

    def check_update(self, force=False):
        found = update.summary(update.check(force))
        if found and found != self.found:
            self.say(f"Доступна версия {found['version']}", "Обновить — в меню FigCraft Review" if found["auto"] else found["url"])
        elif force and not found:
            self.say("Обновлений нет", f"Версия {update.current()}")
        self.found = found
        if self.icon:
            self.icon.update_menu()

    def install_update(self):
        """Download, check and install the update; the installer starts the app again."""
        found = update.check()
        if not found:
            return self.say("Обновлений нет", f"Версия {update.current()}")
        if not update.summary(found)["auto"]:
            return webbrowser.open(found["url"])
        if (launch.server_state() or {}).get("running"):
            return self.say("Обновление подождёт", "Агент ещё работает: обновите, когда он закончит")
        if not self.busy.acquire(blocking=False):
            return
        try:
            self.say(f"Скачиваю {found['version']}")
            installer = update.download(found)
            pids = [os.getpid()]
            server = launch.server_pid()
            if server:
                pids.append(server)
            update.apply(installer, pids)
        except (OSError, ValueError) as e:
            self.busy.release()
            return self.say("Обновление не установлено", str(e)[:200])
        self.quit()

    def quit(self):
        launch.stop_server()
        if self.icon:
            self.icon.stop()
        os._exit(0)

    # ---- the loop ----

    def listen(self, server):
        """A second start (or the chat's «Обновить») asks this app to act."""
        while True:
            conn, _ = server.accept()
            with conn:
                command = conn.makefile().readline().strip()
                if command == "open":
                    threading.Thread(target=self.start, daemon=True).start()
                    conn.sendall(b"ok\n")
                elif command == "quit":
                    conn.sendall(b"ok\n")
                    self.quit()
                elif command == "update":  # it quits this app: answer first, tell how it went in notifications
                    conn.sendall(b"ok\n")
                    threading.Thread(target=self.install_update, daemon=True).start()
                else:
                    conn.sendall(b"?\n")

    def watch(self):
        """FigCraft coming and going (the plugin is checked each time it comes up) and the daily update check."""
        last = 0
        while True:
            up = control_up()
            if up and not self.plugin_checked:
                self.ensure_plugin()
            self.plugin_checked = up
            if self.icon:
                self.icon.title = NAME if up else f"{NAME} · FigCraft не подключён"
            if time.time() - last > 3600:
                last = time.time()
                self.check_update()
            time.sleep(5)

    def menu(self, pystray):
        item, sep = pystray.MenuItem, pystray.Menu.SEPARATOR
        later = lambda f: lambda: threading.Thread(target=f, daemon=True).start()  # noqa: E731
        return pystray.Menu(
            item("Открыть чат", later(self.start), default=True),
            item("Скопировать замечания", later(lambda: self.review("--copy"))),
            item("Добавить замечание", later(lambda: self.review("annotate"))),
            sep,
            item("Запустить FigCraft", later(self.ensure_figcraft), visible=lambda _: not control_up()),
            item(lambda _: f"Обновить до {self.found['version']}" if self.found else "Проверить обновления",
                 later(lambda: self.install_update() if self.found else self.check_update(force=True))),
            item("Папка логов", lambda: desktop.open_path(desktop.state_dir())),
            sep,
            item("Выход", self.quit))

    def run(self, server):
        threading.Thread(target=self.listen, args=(server,), daemon=True).start()
        threading.Thread(target=self.start, daemon=True).start()
        try:
            import pystray
            from PIL import Image
        except ImportError:  # no tray: the app answers second starts until it's closed
            launch.log("no pystray: the app runs without a tray icon")
            self.watch()
            return
        image = Image.open(os.path.join(HERE, "icon.png"))
        self.icon = pystray.Icon("figcraft-review", image, NAME, self.menu(pystray))

        def setup(icon):
            icon.visible = True
            if desktop.MAC:  # a menu-bar app: no Dock icon for the Python inside the bundle
                try:
                    from AppKit import NSApplication
                    NSApplication.sharedApplication().setActivationPolicy_(1)
                except ImportError:
                    pass
            threading.Thread(target=self.watch, daemon=True).start()
        self.icon.run(setup)  # on macOS the tray must own the main thread


def check():
    """The installers' smoke test: the tray's modules load and the chat's server answers."""
    import pystray  # noqa: F401
    from PIL import Image  # noqa: F401
    launch.start_server()
    try:
        for _ in range(120):  # a first start compiles every module
            if launch.server_state() is not None:
                break
            time.sleep(0.5)
        with urllib.request.urlopen(f"http://127.0.0.1:{launch.PORT}/", timeout=10) as r:
            if b"<html" not in r.read():
                raise SystemExit("the chat page isn't served")
        print("ok", update.current())
    finally:
        launch.stop_server()


def main(args):
    if "--check" in args:
        return check()
    if "--quit" in args:
        if not hand_over("quit"):
            launch.stop_server()
        return
    if hand_over("open"):
        return
    server = socket.socket()
    try:
        server.bind(("127.0.0.1", PORT))
    except OSError:  # another start won the race
        hand_over("open")
        return
    server.listen()
    App().run(server)


if __name__ == "__main__":
    main(sys.argv[1:])
