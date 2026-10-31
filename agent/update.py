"""Updates from GitHub Releases: a newer version, this OS's installer for it, checked against the release's SHA256SUMS.

Only the installed app (the Windows setup, the macOS .app: our own Python beside the code) updates itself; a source
checkout or a terminal bundle is told where the release is.
"""
import hashlib
import json
import os
import platform
import re
import sys
import tempfile
import time
import urllib.request

import desktop

REPO = "vornashev/figcraft-review"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # the app: agent/, sidecar/, skills/, plugin/
RUNTIME = os.path.join(os.path.dirname(ROOT), "python")  # the installed app's own Python, beside ROOT
CACHE = os.path.join(desktop.state_dir(), "update.json")
DAY = 24 * 3600
SEMVER = re.compile(r"^v?(\d+)\.(\d+)\.(\d+)(?:-([0-9A-Za-z.]+))?$")


def current():
    """This copy's version, from the plugin's manifest."""
    for path in (os.path.join(ROOT, "plugin", "figcraft-plugin.json"), os.path.join(ROOT, "figcraft-plugin.json")):
        try:
            with open(path, encoding="utf-8") as f:
                return json.load(f)["version"]
        except (OSError, ValueError, KeyError):
            continue
    return "0.0.0"


def key(version):
    """A sort key: SemVer order, a prerelease below its release (0.5.0-rc.2 < 0.5.0-rc.10 < 0.5.0); None if not SemVer."""
    m = SEMVER.match(version or "")
    if not m:
        return None
    pre = m[4]
    tail = (1,) if pre is None else (0, *((0, int(p), "") if p.isdigit() else (1, 0, p) for p in pre.split(".")))
    return (int(m[1]), int(m[2]), int(m[3]), tail)


def installed():
    """Whether this is the installed app, which can replace itself."""
    return os.path.realpath(sys.executable).startswith(os.path.realpath(RUNTIME) + os.sep)


def asset_name(version):
    """This OS's installer in a release, or None (Linux: the tar.gz is installed by hand)."""
    if desktop.WINDOWS:
        return f"FigCraftReview-Setup-v{version}.exe"
    if desktop.MAC:
        return f"FigCraftReview-v{version}-macos-{'arm64' if platform.machine() == 'arm64' else 'x64'}.dmg"
    return None


def newest(releases, have):
    """The newest release above `have`, as {version, url, notes, assets}; prereleases only while `have` is one."""
    mine, best = key(have), None
    for r in releases:
        k = key(r.get("tag_name"))
        if r.get("draft") or k is None or k <= mine or (r.get("prerelease") and "-" not in have):
            continue
        if best is None or k > best[0]:
            best = (k, r)
    if not best:
        return None
    r = best[1]
    return {"version": r["tag_name"].lstrip("v"), "url": r.get("html_url"), "notes": (r.get("body") or "")[:2000],
            "assets": {a["name"]: a["browser_download_url"] for a in r.get("assets", [])}}


def _get(url, timeout=30):
    req = urllib.request.Request(url, headers={"User-Agent": "figcraft-review", "Accept": "application/vnd.github+json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read()


def check(force=False):
    """The available update or None; asks GitHub at most once a day unless forced. Network errors give None."""
    try:
        with open(CACHE, encoding="utf-8") as f:
            cached = json.load(f)
    except (OSError, ValueError):
        cached = {}
    have = current()
    if not force and cached.get("have") == have and time.time() - cached.get("at", 0) < DAY:
        return cached.get("update")
    try:
        found = newest(json.loads(_get(f"https://api.github.com/repos/{REPO}/releases?per_page=30")), have)
    except (OSError, ValueError):
        return cached.get("update") if cached.get("have") == have else None
    os.makedirs(os.path.dirname(CACHE), exist_ok=True)
    with open(CACHE, "w", encoding="utf-8") as f:
        json.dump({"at": time.time(), "have": have, "update": found}, f)
    return found


def summary(found):
    """What the chat and the tray show: {version, url, auto} (auto: one click installs it)."""
    if not found:
        return None
    return {"version": found["version"], "url": found["url"], "auto": installed() and asset_name(found["version"]) in found["assets"]}


def download(found, into=None):
    """This OS's installer from the release, checked against its SHA256SUMS; the file's path. ValueError if it can't."""
    name = asset_name(found["version"])
    if not name or name not in found["assets"] or "SHA256SUMS" not in found["assets"]:
        raise ValueError("в релизе нет установщика для этой системы")
    sums = dict(reversed(line.split(None, 1)) for line in _get(found["assets"]["SHA256SUMS"]).decode().splitlines() if line.strip())
    expected = sums.get(name) or sums.get("*" + name)
    if not expected:
        raise ValueError(f"{name} нет в SHA256SUMS")
    data = _get(found["assets"][name], timeout=600)
    if hashlib.sha256(data).hexdigest() != expected.strip():
        raise ValueError(f"контрольная сумма {name} не совпала")
    path = os.path.join(into or tempfile.mkdtemp(prefix="figcraft-review-update-"), name)
    with open(path, "wb") as f:
        f.write(data)
    return path


MAC_SWAP = r"""dmg="$1"; bundle="$2"; shift 2
for pid in "$@"; do while kill -0 "$pid" 2>/dev/null; do sleep 0.3; done; done
mnt=$(mktemp -d) && hdiutil attach -nobrowse -readonly -mountpoint "$mnt" "$dmg" >/dev/null || exit 1
new=$(ls -d "$mnt"/*.app | head -n 1)
rm -rf "$bundle.new" && ditto "$new" "$bundle.new" && rm -rf "$bundle.old" && mv "$bundle" "$bundle.old" \
  && mv "$bundle.new" "$bundle" && rm -rf "$bundle.old"
hdiutil detach "$mnt" >/dev/null
rm -f "$dmg"
open "$bundle"
"""


def apply(installer, pids):
    """Install once `pids` (this app and its server) have exited, then start the app again."""
    pids = [str(p) for p in pids]
    if desktop.WINDOWS:  # Inno Setup: /SILENT shows only its progress
        wait = "; ".join(f"Wait-Process -Id {p} -ErrorAction SilentlyContinue" for p in pids)
        app = os.path.join(ROOT, "sidecar", "app.py")
        desktop.detach(["powershell", "-NoProfile", "-WindowStyle", "Hidden", "-Command",
                        f"{wait}; Start-Process -Wait -FilePath {desktop._ps(installer)} -ArgumentList '/SILENT','/SUPPRESSMSGBOXES','/NORESTART'; "
                        f"Start-Process -FilePath {desktop._ps(desktop.windowless_python())} -ArgumentList {desktop._ps(chr(34) + app + chr(34))}"])
    elif desktop.MAC:
        bundle = os.path.dirname(os.path.dirname(os.path.dirname(ROOT)))  # X.app/Contents/Resources/app
        desktop.detach(["/bin/sh", "-c", MAC_SWAP, "update", installer, bundle, *pids])
    else:
        raise ValueError("на Linux обновление ставится вручную")
