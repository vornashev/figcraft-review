#!/usr/bin/env python3
"""Packs the release assets into dist/.

    scripts/package.py plugin                 figcraft-review-plugin-vX.Y.Z.zip: the manifest and the .wasm
    scripts/package.py linux|macos|windows    figcraft-review-vX.Y.Z-<os>.tar.gz (.zip for windows): the CLI, the chat,
                                              the skills, the plugin and an install script
    scripts/package.py windows-app            FigCraftReview-Setup-vX.Y.Z.exe: the app with its own Python (Inno Setup 6)
    scripts/package.py macos-app              FigCraftReview-vX.Y.Z-macos-<arch>.dmg: FigCraft Review.app, for this Mac's arch

Needs the built plugin (cargo build --release --target wasm32-unknown-unknown) and chat page (sidecar/web/dist).
The app installers are built on their own OS: they run the bundled Python to install the tray's wheels.
"""
import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
import tarfile
import urllib.request
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
WASM = ROOT / "target/wasm32-unknown-unknown/release/figcraft_review.wasm"
PAGE = ROOT / "sidecar/web/dist/index.html"
SKIP = shutil.ignore_patterns("__pycache__", "*.pyc", "test_*", ".DS_Store")
PACKAGING = ROOT / "packaging"
CACHE = DIST / "cache"


def version():
    return json.loads((ROOT / "figcraft-plugin.json").read_text(encoding="utf-8"))["version"]


def need(*paths):
    missing = [str(p.relative_to(ROOT)) for p in paths if not p.exists()]
    if missing:
        sys.exit("build first, missing: " + ", ".join(missing))


def plugin(into):
    """The manifest beside the module, its `main` pointing there."""
    into.mkdir(parents=True)
    manifest = json.loads((ROOT / "figcraft-plugin.json").read_text(encoding="utf-8"))
    manifest["main"] = WASM.name
    (into / "figcraft-plugin.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    shutil.copy2(WASM, into / WASM.name)


def bundle(system, into):
    into.mkdir(parents=True)
    shutil.copytree(ROOT / "agent", into / "agent", ignore=SKIP)
    sidecar = into / "sidecar"
    sidecar.mkdir()
    for f in (ROOT / "sidecar").iterdir():
        if f.suffix == ".py" and not f.name.startswith("test_") or f.name in ("figcraft-agent", "figcraft-agent.cmd", "README.md", "icon.png"):
            shutil.copy2(f, sidecar / f.name)
    (sidecar / "web/dist").mkdir(parents=True)
    shutil.copy2(PAGE, sidecar / "web/dist/index.html")
    shutil.copytree(ROOT / "skills", into / "skills", ignore=SKIP)
    plugin(into / "plugin")
    shutil.copytree(ROOT / "docs", into / "docs")
    for f in ("README.md", "LICENSE", "THIRD_PARTY.md", "CHANGELOG.md", "AGENTS.md"):
        shutil.copy2(ROOT / f, into / f)
    install = "install.ps1" if system == "windows" else "install.sh"
    shutil.copy2(ROOT / "packaging" / install, into / install)


def sha256(path):
    with open(path, "rb") as f:
        return hashlib.file_digest(f, "sha256").hexdigest()


def runtime(build, into):
    """The pinned Python (packaging/runtime.json) unpacked as into/python, with the tray app's wheels; its interpreter."""
    pinned = json.loads((PACKAGING / "runtime.json").read_text(encoding="utf-8"))
    spec = pinned["builds"][build]
    archive = CACHE / spec["file"]
    if not archive.exists() or sha256(archive) != spec["sha256"]:
        CACHE.mkdir(parents=True, exist_ok=True)
        urllib.request.urlretrieve(pinned["base"] + spec["file"].replace("+", "%2B"), archive)
        if sha256(archive) != spec["sha256"]:
            sys.exit(f"{spec['file']}: the checksum doesn't match packaging/runtime.json")
    with tarfile.open(archive) as t:
        t.extractall(into, filter="data")
    python = into / "python" / ("python.exe" if build.startswith("windows") else "bin/python3")
    run = lambda *a: subprocess.run([str(python), *a], check=True)  # noqa: E731
    if subprocess.run([str(python), "-m", "pip", "--version"], capture_output=True).returncode:
        run("-m", "ensurepip")
    run("-m", "pip", "install", "-q", "--no-cache-dir", "--only-binary", ":all:", "--no-warn-script-location",
        "--disable-pip-version-check", "-r", str(PACKAGING / "requirements-app.txt"))
    return python


def windows_app(v):
    """The runtime, the app and command shims staged, then compiled by Inno Setup into the setup .exe."""
    stage = DIST / "stage" / "FigCraftReview"
    runtime("windows-x64", stage)
    bundle("windows", stage / "app")
    (stage / "app" / "install.ps1").unlink()
    (stage / "bin").mkdir()
    (stage / "bin" / "figcraft-review.cmd").write_text(
        '@"%~dp0..\\python\\python.exe" "%~dp0..\\app\\agent\\review.py" %*\r\n', encoding="utf-8", newline="")
    (stage / "bin" / "figcraft-agent.cmd").write_text(
        '@start "" "%~dp0..\\python\\pythonw.exe" "%~dp0..\\app\\sidecar\\app.py"\r\n', encoding="utf-8", newline="")
    iscc = shutil.which("iscc") or r"C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
    subprocess.run([iscc, "/Q", f"/DVersion={v}", f"/DSource={stage}", f"/DOutput={DIST}",
                    str(PACKAGING / "windows" / "figcraft-review.iss")], check=True)
    return DIST / f"FigCraftReview-Setup-v{v}.exe"


def macos_app(v):
    """FigCraft Review.app (ad-hoc signed) in a .dmg with an Applications link, for this Mac's architecture."""
    arch = "arm64" if platform.machine() == "arm64" else "x64"
    stage = DIST / "stage"
    app = stage / "dmg" / "FigCraft Review.app"
    resources = app / "Contents" / "Resources"
    python = runtime(f"macos-{arch}", resources)
    bundle("macos", resources / "app")
    (resources / "app" / "install.sh").unlink()
    (app / "Contents" / "MacOS").mkdir(parents=True)
    exe = app / "Contents" / "MacOS" / "FigCraft Review"
    shutil.copy2(PACKAGING / "macos" / "launcher.sh", exe)
    exe.chmod(0o755)
    plist = (PACKAGING / "macos" / "Info.plist").read_text(encoding="utf-8").replace("@VERSION@", v.split("-")[0])
    (app / "Contents" / "Info.plist").write_text(plist, encoding="utf-8")
    iconset = stage / "icon.iconset"
    iconset.mkdir()
    for size in (16, 32, 128, 256, 512):
        for scale in (1, 2):
            name = f"icon_{size}x{size}{'@2x' if scale == 2 else ''}.png"
            subprocess.run(["sips", "-z", str(size * scale), str(size * scale), str(PACKAGING / "icon.png"),
                            "--out", str(iconset / name)], check=True, capture_output=True)
    subprocess.run(["iconutil", "-c", "icns", "-o", str(resources / "icon.icns"), str(iconset)], check=True)
    # bytecode now, so the signed bundle isn't written to when it runs
    subprocess.run([str(python), "-m", "compileall", "-q", str(resources / "app"), str(resources / "python" / "lib")])
    subprocess.run(["codesign", "--force", "--deep", "--sign", "-", str(app)], check=True)
    (stage / "dmg" / "Applications").symlink_to("/Applications")
    out = DIST / f"FigCraftReview-v{v}-macos-{arch}.dmg"
    out.unlink(missing_ok=True)
    subprocess.run(["hdiutil", "create", "-volname", "FigCraft Review", "-srcfolder", str(stage / "dmg"),
                    "-format", "UDZO", "-ov", str(out)], check=True)
    return out


def tar(src, out):
    def mode(info):  # scripts stay executable whatever the checkout did to their bits
        name = info.name.rsplit("/", 1)[-1]
        if info.isfile() and (name in ("install.sh", "figcraft-agent") or name.endswith(".py")):
            info.mode = 0o755
        return info
    with tarfile.open(out, "w:gz") as t:
        t.add(src, src.name, filter=mode)


def zip_(src, out):
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(src.rglob("*")):
            z.write(f, f.relative_to(src.parent))


def main(what):
    v = version()
    stage = DIST / "stage"
    shutil.rmtree(stage, ignore_errors=True)
    if what == "plugin":
        need(WASM)
        plugin(stage / "figcraft-review-plugin")
        out = DIST / f"figcraft-review-plugin-v{v}.zip"
        zip_(stage / "figcraft-review-plugin", out)
    elif what in ("linux", "macos", "windows"):
        need(WASM, PAGE)
        bundle(what, stage / "figcraft-review")
        out = DIST / (f"figcraft-review-v{v}-{what}." + ("zip" if what == "windows" else "tar.gz"))
        (zip_ if what == "windows" else tar)(stage / "figcraft-review", out)
    elif what in ("windows-app", "macos-app"):
        need(WASM, PAGE)
        out = (windows_app if what == "windows-app" else macos_app)(v)
    else:
        sys.exit(__doc__)
    shutil.rmtree(stage)
    print(out.relative_to(ROOT))


if __name__ == "__main__":
    os.chdir(ROOT)
    main(sys.argv[1] if len(sys.argv) > 1 else "")
