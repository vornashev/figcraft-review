#!/usr/bin/env python3
"""Packs the release assets into dist/.

    scripts/package.py plugin                 figcraft-review-plugin-vX.Y.Z.zip: the manifest and the .wasm
    scripts/package.py linux|macos|windows    figcraft-review-vX.Y.Z-<os>.tar.gz (.zip for windows): the CLI, the chat,
                                              the skills, the plugin and an install script

Needs the built plugin (cargo build --release --target wasm32-unknown-unknown) and chat page (sidecar/web/dist).
"""
import json
import os
import shutil
import sys
import tarfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
WASM = ROOT / "target/wasm32-unknown-unknown/release/figcraft_review.wasm"
PAGE = ROOT / "sidecar/web/dist/index.html"
SKIP = shutil.ignore_patterns("__pycache__", "*.pyc", "test_*", ".DS_Store")


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
        if f.suffix == ".py" and not f.name.startswith("test_") or f.name in ("figcraft-agent", "figcraft-agent.cmd", "README.md"):
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
    else:
        sys.exit(__doc__)
    shutil.rmtree(stage)
    print(out.relative_to(ROOT))


if __name__ == "__main__":
    os.chdir(ROOT)
    main(sys.argv[1] if len(sys.argv) > 1 else "")
