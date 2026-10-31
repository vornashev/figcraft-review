#!/usr/bin/env python3
"""Import OpenDesign's public prompt + reference bundles as FigCraft skills.

    python3 skills/opendesign.py [--index saved-catalog.html] [--cache DIR] [--out DIR]

They go to your own skills (~/.config/figcraft-agent/skills): OpenDesign's prompts and images aren't licensed for
redistribution, so the repository carries only this importer. The cache (~/.cache/figcraft-agent/opendesign by
default) makes retries resumable. Generated skills include the unmodified upstream prompt and image,
a short FigCraft adapter, provenance, and the library's references.json. No downloaded code is run.
`--adapter` rewrites only the adapter (SKILL.md) of skills already in --out, without downloading.
"""
import argparse
import concurrent.futures
import hashlib
import io
import json
import re
import time
import urllib.request
import zipfile
from datetime import date
from html.parser import HTMLParser
from pathlib import Path, PurePosixPath

SITE = "https://open-design.ai"
CATEGORIES = {"websites": "Сайты", "apps": "Приложения", "dashboards": "Дашборды", "slides": "Презентации", "graphics": "Графика"}


class Catalog(HTMLParser):
    def __init__(self):
        super().__init__()
        self.entries, self.current, self.raw, self.paragraph = [], None, False, False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "article" and "data-prompt-card" in attrs:
            self.current = {k[5:]: v for k, v in attrs.items() if k.startswith("data-")}
            self.current.update(prompt="", summary="")
        if self.current is not None:
            if tag == "textarea" and "data-card-raw" in attrs:
                self.raw = True
            if tag == "p" and not self.raw:
                self.paragraph = True

    def handle_data(self, text):
        if self.current is not None:
            if self.raw:
                self.current["prompt"] += text
            elif self.paragraph:
                self.current["summary"] += text

    def handle_endtag(self, tag):
        if tag == "textarea":
            self.raw = False
        if tag == "p":
            self.paragraph = False
        if tag == "article" and self.current is not None:
            self.entries.append(self.current)
            self.current = None


def parse_catalog(text):
    parser = Catalog()
    parser.feed(text)
    entries = parser.entries
    if not entries or len({e["slug"] for e in entries}) != len(entries):
        raise ValueError("Empty catalog or duplicate prompt slugs")
    for e in entries:
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", e["slug"]) or len("opendesign-" + e["slug"]) > 64:
            raise ValueError(f"Invalid skill name: {e['slug']}")
        if e["category"] not in CATEGORIES or not e["prompt"].strip() or not e["summary"].strip():
            raise ValueError(f"Incomplete prompt: {e['slug']}")
    return entries


def download(url):
    for attempt in range(3):
        try:
            request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(request, timeout=30) as response:
                return response.read()
        except OSError:
            if attempt == 2:
                raise
            time.sleep(attempt + 1)


def unpack(data):
    """Validate the whole archive before writing anything outside the download cache."""
    with zipfile.ZipFile(io.BytesIO(data)) as archive:
        files = {}
        entries = archive.infolist()
        if len(entries) > 100 or sum(e.file_size for e in entries) > 32 * 1024 * 1024:
            raise ValueError("Oversized OpenDesign bundle")
        for entry in entries:
            path = PurePosixPath(entry.filename)
            if path.is_absolute() or ".." in path.parts or "\\" in entry.filename or (entry.external_attr >> 16) & 0o170000 == 0o120000:
                raise ValueError("Unsafe path in OpenDesign bundle")
            if not entry.is_dir():
                if entry.filename in files:
                    raise ValueError("Duplicate file in OpenDesign bundle")
                files[entry.filename] = archive.read(entry)
    if not all(name in files for name in ("prompt.txt", "reference.webp")):
        raise ValueError("Bundle lacks prompt.txt or reference.webp")
    image = files["reference.webp"]
    if image[:4] != b"RIFF" or image[8:12] != b"WEBP":
        raise ValueError("Reference is not a WebP image")
    if not files["prompt.txt"].decode("utf-8").strip():
        raise ValueError("Empty prompt")
    return files


def adapter(slug, title):
    """The SKILL.md body: the task as a checklist; how much of the picture to take is the chat's reference mode."""
    return f"""# {title} — OpenDesign

Use this task reference when its content and workflow fit the user's brief. It is a checklist, not a template.

- Read [the original task brief](references/prompt.md) for its required content, structure, states and acceptance checks.
- The user's existing layout and the document's design system come first: when asked to redraw a frame, keep its content and structure and use this task to check what is missing. Its fallback design direction ("If no system is supplied…") applies only when the document has no visual style of its own and no style skill is chosen.
- [The visual reference](assets/reference.webp) is an AI-generated concept with fictional sample content. Use it as the chat's reference mode says, checklist by default:
  - checklist: don't open the image; skip the brief's sections on the reference image, its visual direction and the visual comparison.
  - inspiration: take its hierarchy, rhythm and density, not its palette, fonts or decorative motifs. Before designing, say in one line what you take and what you leave; afterwards compare a screenshot of your frame with it and rework if the palette and layout match.
  - replica: reconstruct its composition and visual direction; compare the frame at matching proportions and state material departures or unavailable assets.
- The target in this workspace is the user's FigCraft document. Translate the brief into editable text, shapes, auto-layout and components. Map visual values to the document's variables and text styles; reuse its components where they fit.
- The original brief describes web/app implementation. In FigCraft, represent the relevant screens, states and transitions in the design. Implement runtime behavior or change project code only when the user requests that output and the current access mode permits it.
- Replace bracketed project, audience, content and brand inputs with the supplied brief. Ask only for missing inputs that materially affect this task. Preserve the scope the user chose rather than adding every example feature.
- Never place the reference image as the finished interface.

Source: {SITE}/prompts/{slug}/
"""


def rewrite_adapters(output):
    """Re-render SKILL.md of every imported skill in place; the frontmatter and the other files stay."""
    count = 0
    for path in sorted(output.glob("opendesign-*/SKILL.md")):
        text = path.read_text(encoding="utf-8")
        end = text.index("\n---\n", 3) + 5
        title = re.search(r'^  title: (.+)$', text[:end], re.M).group(1)
        path.write_text(text[:end] + adapter(path.parent.name[len("opendesign-"):], json.loads(title)), encoding="utf-8")
        count += 1
    return count


def write_skill(entry, data, output):
    files = unpack(data)
    slug, title = entry["slug"], entry["name"]
    folder = output / ("opendesign-" + slug)
    (folder / "assets").mkdir(parents=True, exist_ok=True)
    (folder / "references").mkdir(exist_ok=True)
    # The original prompt stays intact, outside the small entrypoint loaded into every turn.
    (folder / "references/prompt.md").write_bytes(files.pop("prompt.txt"))
    (folder / "assets/reference.webp").write_bytes(files.pop("reference.webp"))
    if "README.txt" in files:
        (folder / "references/source-bundle.txt").write_bytes(files.pop("README.txt"))
    for name, content in files.items():
        path = folder / "assets/upstream" / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
    desc = f"{title}: {entry['summary']} OpenDesign {entry['category']} reference in the {entry['style']} direction."
    header = "\n".join(["---", f"name: opendesign-{slug}", "description: " + json.dumps(desc, ensure_ascii=False),
        "metadata:", "  group: task", "  origin: opendesign", f"  category: {entry['category']}",
        "  style: " + json.dumps(entry["style"]), "  title: " + json.dumps(title),
        "  summary: " + json.dumps(entry["summary"], ensure_ascii=False), "---", ""])
    (folder / "SKILL.md").write_text(header + adapter(slug, title), encoding="utf-8")
    refs = {"images": [{"file": "assets/reference.webp", "label": "Референс"}], "links": [
        {"label": "Промпт OpenDesign", "url": f"{SITE}/prompts/{slug}/"},
        {"label": "Оригинальный набор", "url": f"{SITE}/prompts/{slug}/reference.zip"}]}
    (folder / "references.json").write_text(json.dumps(refs, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    attribution = f"""# {title}

- Collection: OpenDesign; original prompt and reference image supplied by OpenDesign.
- Source: {SITE}/prompts/{slug}/
- Download: {SITE}/prompts/{slug}/reference.zip
- Retrieved: {date.today().isoformat()}
- Archive SHA-256: {hashlib.sha256(data).hexdigest()}
- Changes: original prompt and image preserved; FigCraft adapter and library metadata added.
- The source reference is an AI-generated concept with fictional sample content.
- Source terms: {SITE}/terms/ . This adaptation does not relicense the original content.
"""
    (folder / "ATTRIBUTION.md").write_text(attribution, encoding="utf-8")
    return folder


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--index", type=Path, help="saved HTML of the All Prompts catalog")
    parser.add_argument("--out", type=Path, default=Path("~/.config/figcraft-agent/skills").expanduser())
    parser.add_argument("--cache", type=Path, default=Path("~/.cache/figcraft-agent/opendesign").expanduser(),
                        help="download archive folder, reused on retry")
    parser.add_argument("--adapter", action="store_true", help="only rewrite SKILL.md of the skills already in --out")
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()
    if args.adapter:
        return print(f"{rewrite_adapters(args.out)} adapters rewritten")
    html = args.index.read_text() if args.index else download(SITE + "/prompts/?type=all").decode()
    entries = parse_catalog(html)
    args.cache.mkdir(parents=True, exist_ok=True)
    def import_one(entry):
        cached = args.cache / (entry["slug"] + ".zip")
        data = cached.read_bytes() if cached.exists() else download(f"{SITE}/prompts/{entry['slug']}/reference.zip")
        unpack(data)
        cached.write_bytes(data)
        return write_skill(entry, data, args.out)
    with concurrent.futures.ThreadPoolExecutor(max_workers=max(1, min(8, args.workers))) as pool:
        for n, folder in enumerate(pool.map(import_one, entries), 1):
            if n % 25 == 0 or n == len(entries):
                print(f"{n}/{len(entries)} · {folder.name}", flush=True)


if __name__ == "__main__":
    main()
