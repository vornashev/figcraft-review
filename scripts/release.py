#!/usr/bin/env python3
"""Cuts a release: one version everywhere, a dated CHANGELOG section, tests, a commit and a tag. It doesn't push.

    scripts/release.py X.Y.Z            release (X.Y.Z-rc.N: a prerelease, the CHANGELOG stays in Unreleased)
    scripts/release.py --check X.Y.Z    exit 1 unless every version is X.Y.Z and the CHANGELOG has its section
    scripts/release.py --notes X.Y.Z    print that CHANGELOG section (Unreleased for a prerelease)
"""
import json
import os
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPO = "https://github.com/vornashev/figcraft-review"
SEMVER = re.compile(r"^\d+\.\d+\.\d+(-[0-9A-Za-z.]+)?$")
JSON_FILES = ["figcraft-plugin.json", "sidecar/web/package.json", "skills/.claude-plugin/plugin.json"]


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


def write(path, text):
    (ROOT / path).write_text(text, encoding="utf-8")


def versions():
    """Each versioned file → its version."""
    out = {f: json.loads(read(f))["version"] for f in JSON_FILES}
    out["Cargo.toml"] = re.search(r'^version = "(.+?)"', read("Cargo.toml"), re.M).group(1)
    lock = json.loads(read("sidecar/web/package-lock.json"))
    out["sidecar/web/package-lock.json"] = lock["version"]
    out["Cargo.lock"] = re.search(r'name = "figcraft-review"\nversion = "(.+?)"', read("Cargo.lock")).group(1)
    return out


def bump(v):
    for f in JSON_FILES:  # only the top-level "version", so the files keep their layout
        write(f, re.sub(r'^(  "version": )"[^"]*"', rf'\g<1>"{v}"', read(f), count=1, flags=re.M))
    write("Cargo.toml", re.sub(r'^version = ".+?"', f'version = "{v}"', read("Cargo.toml"), count=1, flags=re.M))
    write("Cargo.lock", re.sub(r'(name = "figcraft-review"\nversion = )".+?"', rf'\g<1>"{v}"', read("Cargo.lock")))
    lock = read("sidecar/web/package-lock.json")
    lock = re.sub(r'^(  "version": )"[^"]*"', rf'\g<1>"{v}"', lock, count=1, flags=re.M)
    lock = re.sub(r'(  "packages": \{\n    "": \{\n      "name": "[^"]*",\n      "version": )"[^"]*"', rf'\g<1>"{v}"', lock)
    write("sidecar/web/package-lock.json", lock)


def section(changelog, title):
    """The body of `## [title]`, or None."""
    m = re.search(rf"^## \[{re.escape(title)}\][^\n]*\n(.*?)(?=^## \[|^\[[^\]]+\]: |\Z)", changelog, re.M | re.S)
    return m.group(1).strip() if m else None


def date_changelog(v):
    """Unreleased becomes `## [v] - today` under a fresh Unreleased; the compare links follow."""
    text = read("CHANGELOG.md")
    if not section(text, "Unreleased"):
        sys.exit("CHANGELOG.md: nothing under ## [Unreleased]")
    text = text.replace("## [Unreleased]\n", f"## [Unreleased]\n\n## [{v}] - {date.today():%Y-%m-%d}\n", 1)
    previous = re.findall(r"^## \[(\d[^\]]*)\]", text, re.M)[1:2]
    text = re.sub(r"^\[Unreleased\]: .*$", f"[Unreleased]: {REPO}/compare/v{v}...HEAD", text, flags=re.M)
    link = f"{REPO}/compare/v{previous[0]}...v{v}" if previous else f"{REPO}/releases/tag/v{v}"
    text = re.sub(r"^(\[Unreleased\]: .*)$", rf"\1\n[{v}]: {link}", text, count=1, flags=re.M)
    write("CHANGELOG.md", text)


def run(*cmd, env=None):
    print("$", " ".join(cmd), flush=True)
    if subprocess.run(cmd, cwd=ROOT, env={**os.environ, **(env or {})}).returncode:
        sys.exit(f"failed: {' '.join(cmd)}")


def check(v):
    wrong = {f: have for f, have in versions().items() if have != v}
    if wrong:
        sys.exit("versions differ from " + v + ": " + ", ".join(f"{f} {have}" for f, have in wrong.items()))
    if "-" not in v and section(read("CHANGELOG.md"), v) is None:
        sys.exit(f"CHANGELOG.md has no ## [{v}] section")


def release(v):
    git = lambda *a: subprocess.run(["git", *a], cwd=ROOT, capture_output=True, text=True, encoding="utf-8").stdout.strip()  # noqa: E731
    if git("status", "--porcelain"):
        sys.exit("the working tree isn't clean")
    if git("branch", "--show-current") != "main":
        sys.exit("release from main")
    if git("tag", "-l", f"v{v}"):
        sys.exit(f"v{v} exists")
    bump(v)
    if "-" not in v:
        date_changelog(v)
    check(v)
    run("cargo", "test", "-q")
    run(sys.executable, "-m", "unittest", "discover", "-s", "agent", "-p", "test_*.py")
    run(sys.executable, "-m", "unittest", "discover", "-s", "sidecar", "-p", "test_*.py")
    run("npm", "--prefix", "sidecar/web", "test")
    if os.environ.get("FIGCRAFT_TEST_FILE"):
        run(sys.executable, "-m", "unittest", "agent/test_review.py", "agent/test_plugin.py")
    else:
        print("FIGCRAFT_TEST_FILE isn't set: the tests with FigCraft didn't run", file=sys.stderr)
    run("git", "add", "-A")
    run("git", "commit", "-q", "-m", f"Release v{v}")
    run("git", "tag", "-a", f"v{v}", "-m", f"FigCraft Review {v}")
    print(f"\nTagged v{v}. Check it, then: git push origin main v{v}")


def main(args):
    if len(args) == 2 and args[0] in ("--check", "--notes") and SEMVER.match(args[1]):
        if args[0] == "--check":
            check(args[1])
            print(f"{args[1]}: versions and CHANGELOG agree")
        else:
            text = read("CHANGELOG.md")
            print(section(text, args[1]) or section(text, "Unreleased") or "")
    elif len(args) == 1 and SEMVER.match(args[0]):
        release(args[0])
    else:
        sys.exit(__doc__)


if __name__ == "__main__":
    main(sys.argv[1:])
