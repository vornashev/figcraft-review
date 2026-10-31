#!/usr/bin/env python3
"""Import pinned TypeUI, tweakcn and UI UX Pro Max collections into FigCraft.

python skills/design_collections.py --cache /tmp/figcraft-design-import --fetch
node skills/render_collection_previews.mjs /tmp/figcraft-design-import/render-manifest.json

Source revisions are pinned in collections.lock.json. Downloads are cached, original specifications and
licenses are preserved, and downloaded JavaScript is parsed as data rather than executed.
"""
import argparse
import concurrent.futures
import csv
import hashlib
import html
import json
import re
import subprocess
import time
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCES = json.loads((HERE / "collections.lock.json").read_text())
LABELS = {"typeui": "TypeUI", "tweakcn": "tweakcn", "uipro": "UI UX Pro Max"}


def download(url):
    for attempt in range(3):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "FigCraft-collections-import"})
            with urllib.request.urlopen(req, timeout=45) as response:
                return response.read()
        except OSError:
            if attempt == 2:
                raise
            time.sleep(attempt + 1)


def fetch_sources(cache):
    jobs = []
    for name, source in SOURCES.items():
        folder = cache / name
        folder.mkdir(parents=True, exist_ok=True)
        if (folder / "source.json").exists() and json.loads((folder / "source.json").read_text()) != source:
            raise ValueError(f"Cache revision mismatch: {name}; use a new cache directory")
        tree = json.loads(download(f"https://api.github.com/repos/{source['repo']}/git/trees/{source['sha']}?recursive=1"))
        if tree.get("truncated"):
            raise ValueError("Incomplete source tree")
        for item in tree["tree"]:
            path = item["path"]
            take = item["type"] == "blob" and (path == "LICENSE"
                or name == "typeui" and (re.fullmatch(r"skills/[a-z0-9-]+/(SKILL|DESIGN)\.md", path)
                    or path == "skills/index.json" or re.fullmatch(r"registry-examples/[a-z0-9-]+-marketing\.png", path))
                or name == "tweakcn" and path == "utils/theme-presets.ts"
                or name == "uipro" and path == "src/ui-ux-pro-max/data/styles.csv")
            if take:
                jobs.append((folder, source, path))
        (folder / "source.json").write_text(json.dumps(source))

    def fetch(job):
        folder, source, path = job
        target = folder / path
        if not target.exists():
            data = download(f"https://raw.githubusercontent.com/{source['repo']}/{source['sha']}/{path}")
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
        list(pool.map(fetch, jobs))


def text(value):
    # Keep frontmatter one line; the original specifications retain the exact source wording.
    return " ".join(str(value).split()).replace('"', "’")


def header(name, title, origin, summary, description, colors=(), font="", style=""):
    if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or len(name) > 64:
        raise ValueError(f"Invalid skill name: {name}")
    metadata = {"group": "style", "origin": origin, "category": "themes", "mode": "manual",
                "title": title, "summary": summary, "style": style}
    if colors or font:
        metadata["preview"] = " ".join(colors[:5]) + (" · " + font if font else "")
    return "---\nname: " + name + "\ndescription: " + json.dumps(text(description), ensure_ascii=False) + "\nmetadata:\n" + "\n".join(
        f"  {key}: {json.dumps(text(value), ensure_ascii=False)}" for key, value in metadata.items() if value) + "\n---\n\n"


def write_bundle(out, name, title, origin, summary, description, originals, source_paths, images, links, colors=(), font="", style="", note=""):
    folder = out / name
    (folder / "references").mkdir(parents=True, exist_ok=True)
    (folder / "assets").mkdir(exist_ok=True)
    for rel, data in originals.items():
        dest = folder / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(data if isinstance(data, bytes) else data.encode())
    reads = "\n".join(f"- [{Path(path).name}]({path})" for path in originals if path.startswith("references/") and not path.endswith(".html"))
    body = f"""# {title} — {LABELS[origin]}

Apply this visual direction when the user chooses it or the brief explicitly asks for this style.

Read the relevant local specification before designing:
{reads}

Inspect the images listed in [references.json](references.json). {note}

For FigCraft, translate colors, typography, spacing, radii and effects into editable layers, file variables,
text styles and component variants. Check installed fonts and state substitutions. Reuse the document's existing
system where it fits; change an established brand or layout only within the user's request. CSS examples describe
visual intent; do not require a web framework to draw the design. Keep supplied content and workflows. A sample
preview is a reference, not a finished screen to flatten into the canvas. If multiple styles are selected, use the
user's stated relationship between them (alternatives, comparison, or combination) rather than dropping one.
Source workflows for authoring guideline documents apply when that is the requested deliverable; otherwise use
their visual foundations to complete the user's design task. Locally rendered specimens use available system
fonts as fallbacks; the source specification remains authoritative for the intended font families.
"""
    (folder / "SKILL.md").write_text(header(name, title, origin, summary, description, colors, font, style) + body)
    (folder / "references.json").write_text(json.dumps({"images": images, "links": links}, ensure_ascii=False, indent=2) + "\n")
    source = SOURCES[origin]
    attribution = f"# {title}\n\nCollection: {LABELS[origin]}\nRepository: https://github.com/{source['repo']}\nRevision: {source['sha']}\n\n"
    attribution += "\n".join(f"- https://github.com/{source['repo']}/blob/{source['sha']}/{path}" for path in source_paths)
    attribution += "\n\nChanges: original data/specifications retained; FigCraft adapter and metadata added. " + note + "\n"
    attribution += "\nOriginal files (SHA-256):\n" + "\n".join(f"- {path}: {hashlib.sha256(data if isinstance(data, bytes) else data.encode()).hexdigest()}" for path, data in originals.items()) + "\n"
    (folder / "ATTRIBUTION.md").write_text(attribution)
    return folder


def import_typeui(cache, out):
    root = cache / "typeui"
    index = json.loads((root / "skills/index.json").read_text())
    rendered = []
    for slug, entry in sorted(index.items()):
        skill = root / entry["skillPath"]
        design = root / entry["designPath"]
        source = skill.read_text()
        desc = re.search(r"^description:\s*(.+)$", source, re.M)
        desc = desc[1].strip('"') if desc else f"{entry['name']} design system."
        colors = list(dict.fromkeys(re.findall(r"#[0-9A-Fa-f]{6}\b", source)))
        roles = dict(re.findall(r"\b([a-z]+)=(#[0-9A-Fa-f]{6})\b", source))
        if all(key in roles for key in ("surface", "text", "primary")):
            colors = [roles["surface"], roles["surface"], roles["text"], roles["primary"], roles.get("secondary", roles["primary"])]
        face = re.search(r"Fonts: primary=([^,|\n]+)", source)
        preview = root / "registry-examples" / (slug + "-marketing.png")
        if not preview.is_file():
            raise ValueError(f"Missing TypeUI reference: {slug}")
        paths = [entry["skillPath"], entry["designPath"], f"registry-examples/{preview.name}"]
        folder = write_bundle(out, "typeui-" + slug, entry["name"], "typeui", desc, desc,
            {"references/upstream-SKILL.md": skill.read_bytes(), "references/DESIGN.md": design.read_bytes(), "LICENSE": (root / "LICENSE").read_bytes()}, paths,
            [{"file": "assets/preview.webp", "label": "Оригинальное превью TypeUI"}],
            [{"label": "Пример TypeUI", "url": f"https://typeui.sh/design-skills/{slug}"},
             {"label": "Исходник", "url": f"https://github.com/{SOURCES['typeui']['repo']}/tree/{SOURCES['typeui']['sha']}/skills/{slug}"}],
            colors, face[1].strip() if face else "", slug, "The preview is an upstream TypeUI example, compressed to WebP.")
        subprocess.run(["magick", str(preview), "-resize", "1400x1400>", "-quality", "88", str(folder / "assets/preview.webp")], check=True)
        rendered.append(folder)
    return rendered


def safe_css(value):
    value = str(value).strip()
    if re.search(r"[{}<>;]|url\s*\(|expression\s*\(", value, re.I):
        raise ValueError(f"Unexpected CSS value: {value}")
    return value


def specimen(title, origin, tokens, mode="light", extra=None):
    """An explicit token specimen, not a claimed upstream screenshot or a layout prescription."""
    t = {"background": "#f5f5f5", "foreground": "#1d1d1d", "card": "#ffffff", "card-foreground": "#1d1d1d",
         "muted": "#f0f0f0", "muted-foreground": "#666666", "primary": "#333333", "primary-foreground": "#ffffff",
         "secondary": "#eeeeee", "secondary-foreground": "#222222", "accent": "#dddddd", "border": "#dddddd",
         "radius": "8px", "font-sans": "Arial, sans-serif", **tokens}
    variables = ";".join(f"--{k}:{safe_css(v)}" for k, v in t.items())
    custom = ";".join(f"{k}:{safe_css(v)}" for k, v in (extra or {}).items())
    shadows = all(k in t for k in ("shadow-offset-x", "shadow-offset-y", "shadow-blur", "shadow-spread", "shadow-color"))
    if shadows:
        shadow_color = f"color-mix(in srgb, {t['shadow-color']} {float(t.get('shadow-opacity', '.1')) * 100}%, transparent)"
        custom += ";box-shadow:" + " ".join(t[k] for k in ("shadow-offset-x", "shadow-offset-y", "shadow-blur", "shadow-spread")) + " " + shadow_color
    swatches = "".join(f'<i style="background:var(--{c})"></i>' for c in ("primary", "secondary", "accent", "foreground", "muted"))
    return f"""<!doctype html><html><meta charset="utf-8"><style>
*{{box-sizing:border-box}}body{{margin:0;{variables};background:var(--background);color:var(--foreground);font:16px var(--font-sans)}}
main{{width:1080px;height:720px;padding:38px 44px}}header{{display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid var(--border);padding-bottom:18px;font-size:13px}}
.mark{{font-size:20px;font-weight:700}}.caption{{color:var(--muted-foreground);font-size:12px;letter-spacing:.06em;text-transform:uppercase}}
h1{{font-size:42px;line-height:1.15;margin:30px 0 8px;letter-spacing:-.035em}}p{{color:var(--muted-foreground);line-height:1.5;margin:0 0 20px}}
.layout{{display:grid;grid-template-columns:1.4fr 1fr;gap:24px}}.card{{background:var(--card);color:var(--card-foreground);border:1px solid var(--border);border-radius:var(--radius);padding:24px;{custom}}}
h2{{font-size:20px;margin:0 0 20px}}.metric{{font-size:46px;line-height:1.2;font-weight:650;letter-spacing:-.04em;margin:8px 0}}.bar{{display:flex;height:105px;align-items:end;gap:12px;margin:22px 0 18px}}
.bar i{{flex:1;background:var(--primary);border-radius:var(--radius) var(--radius) 0 0}}.bar i:nth-child(3n){{background:var(--accent)}}
.line{{border-top:1px solid var(--border);padding:12px 0;display:flex;justify-content:space-between;align-items:center;font-size:14px}}.pill{{background:var(--secondary);color:var(--secondary-foreground);padding:5px 9px;border-radius:var(--radius);font-size:12px}}
button,input{{font:inherit;border-radius:var(--radius);padding:12px 16px;width:100%;margin:8px 0;border:1px solid var(--border)}}button{{background:var(--primary);color:var(--primary-foreground);border:0;font-weight:600}}
input{{background:var(--background);color:var(--foreground)}}label{{font-size:13px}}.swatches{{display:flex;gap:8px;margin:20px 0}}.swatches i{{height:34px;flex:1;border:1px solid var(--border);border-radius:var(--radius)}}
footer{{margin-top:22px;display:flex;justify-content:space-between;color:var(--muted-foreground);font-size:11px}}
</style><main><header><span class="mark">{html.escape(title)}</span><span>{LABELS[origin]} / {html.escape(mode.title())}</span></header>
<h1>A clear view of your work.</h1><p>Typography, surfaces, controls and color — in one visual direction.</p>
<div class="layout"><section class="card"><span class="caption">Workspace overview</span><div class="metric">24,860</div><div class="bar">{''.join(f'<i style="height:{v}%"></i>' for v in (30,48,41,66,58,78,68,95,84))}</div>
<div class="line"><span>Design review</span><span class="pill">In progress</span></div><div class="line"><span>Component library</span><span>12 updates</span></div><div class="line"><span>Release checklist</span><span>8 / 10</span></div></section>
<section class="card"><h2>Start something good.</h2><p>A focused space for the next idea.</p><label>Project name<input value="Northstar workspace" readonly></label><label>Team<input value="Design & product" readonly></label><button>Create workspace</button><div class="swatches">{swatches}</div><span class="caption">Palette · type · radius · depth</span></section></div>
<footer><span>FigCraft specimen · rendered from source specifications</span><span>Illustrative content · not an upstream screenshot</span></footer></main></html>"""


def import_tweakcn(cache, out):
    root = cache / "tweakcn"
    presets = json.loads(subprocess.check_output(["node", str(HERE / "read_theme_presets.mjs"), str(root / "utils/theme-presets.ts")]))
    jobs, folders = [], []
    for slug, preset in presets.items():
        title = preset["label"]
        light = preset["styles"]["light"]
        font = light.get("font-sans", "sans-serif").split(",")[0].strip('"')
        summary = f"Светлая и тёмная тема · {font} · радиус {light.get('radius', 'по умолчанию')}"
        colors = [light[k] for k in ("background", "card", "foreground", "primary", "accent") if re.fullmatch(r"#[\da-fA-F]{6}", light.get(k, ""))]
        tokens = json.dumps(preset, ensure_ascii=False, indent=2) + "\n"
        css = "\n\n".join((":root" if mode == "light" else ".dark") + " {\n" + "\n".join(f"  --{k}: {v};" for k, v in values.items()) + "\n}" for mode, values in preset["styles"].items())
        folder = write_bundle(out, "tweakcn-" + slug, title, "tweakcn", summary, f"{title}: tweakcn theme with light and dark semantic color tokens, typography, radii and shadows.",
            {"references/tokens.json": tokens, "references/theme.css": css, "LICENSE": (root / "LICENSE").read_bytes()}, ["utils/theme-presets.ts"],
            [{"file": f"assets/{mode}.webp", "label": f"{'Светлый' if mode == 'light' else 'Тёмный'} образец по токенам"} for mode in ("light", "dark")],
            [{"label": "Редактор tweakcn", "url": "https://tweakcn.com"}, {"label": "Исходные пресеты", "url": f"https://github.com/{SOURCES['tweakcn']['repo']}/blob/{SOURCES['tweakcn']['sha']}/utils/theme-presets.ts"}],
            colors, font, "theme", "Previews are locally rendered token specimens; layouts and sample text are illustrative. Dark mode inherits unspecified foundation tokens from light mode, as in the source theme.")
        for mode in ("light", "dark"):
            values = {**light, **preset["styles"][mode]}
            page = folder / f"assets/{mode}.html"
            page.write_text(specimen(title, "tweakcn", values, mode))
            jobs.append({"html": str(page.resolve()), "image": str(page.with_suffix(".webp").resolve())})
        folders.append(folder)
    return folders, jobs


def css_declarations(source):
    # A comma can separate declarations, font families, shadows, or function arguments.
    # Split at the next property name, preserving rgba(), gradients and font stacks intact.
    matches = list(re.finditer(r"(?<![\w-])([\w-]+)\s*:\s*", source))
    out = {}
    for i, match in enumerate(matches):
        value = source[match.end():matches[i + 1].start() if i + 1 < len(matches) else len(source)].strip(" ,;")
        if value.count("(") == value.count(")"):
            out[match[1]] = value
    return out


def ink_on(color):
    rgb = [int(color[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    linear = [v / 12.92 if v <= .04045 else ((v + .055) / 1.055) ** 2.4 for v in rgb]
    luminance = sum(v * weight for v, weight in zip(linear, (.2126, .7152, .0722)))
    return "#111111" if luminance > .18 else "#ffffff"


def style_tokens(row):
    colors = list(dict.fromkeys(re.findall(r"#[\da-fA-F]{6}\b", row["Primary Colors"] + ", " + row["Secondary Colors"])))
    dark = row["Preferred Mode"] == "dark" or row["Light Mode ✓"] == "unsupported"
    bg, fg = ("#141414", "#f5f5f5") if dark else ("#fafafa", "#1d1d1d")
    accent = next((c for c in colors if c.lower() not in ("#000000", "#ffffff", "#808080")), fg)
    props = {}
    allowed = {"font-family", "font-weight", "border-radius", "box-shadow", "border", "text-shadow", "letter-spacing", "backdrop-filter", "background", "background-color"}
    for key, value in css_declarations(row["CSS/Technical Keywords"]).items():
        if key in allowed and not re.search(r"[{}<>;]|url\s*\(", value, re.I):
            props[key] = value.strip()
    # Spec values can be ranges or descriptions, not CSS; only use concrete radius values in the specimen.
    radius = props.pop("border-radius", "8px")
    radius = re.sub(r"^(\d+)-(?:\d+)(px|rem|em|%)$", r"\1\2", radius)
    if not re.fullmatch(r"\d+(?:\.\d+)?(?:px|rem|em|%)", radius):
        radius = "8px"
    tokens = {"background": bg, "foreground": fg, "card": "#202020" if dark else "#ffffff", "card-foreground": fg,
            "muted": "#292929" if dark else "#eeeeee", "muted-foreground": "#bbbbbb" if dark else "#666666",
            "border": "#444444" if dark else "#dddddd", "primary": accent, "primary-foreground": ink_on(accent),
            "secondary": colors[1] if len(colors) > 1 else bg, "accent": colors[2] if len(colors) > 2 else accent,
            "radius": radius}
    if "glass" in row["Style ID"] and len(colors) > 1:
        tokens.update(background=f"linear-gradient(135deg, {colors[0]}66, {colors[1]}66)", card="rgb(255 255 255 / .35)")
    if row["Style ID"].startswith("neumorphism"):
        tokens.update(background=colors[-1], card=colors[-1])
    return tokens, props, colors


def import_uipro(cache, out):
    root = cache / "uipro"
    source_path = "src/ui-ux-pro-max/data/styles.csv"
    rows = list(csv.DictReader((root / source_path).open()))
    jobs, folders = [], []
    for row in rows:
        if row["Status"] not in ("active", "supplemental"):
            continue
        slug, title = row["Style ID"], row["Style Category"]
        summary = row["Keywords"] + (" · дополнительный стиль" if row["Status"] == "supplemental" else "")
        spec = "# " + title + "\n\n" + "\n\n".join(f"## {k}\n\n{v}" for k, v in row.items() if v)
        tokens, props, colors = style_tokens(row)
        preview_colors = [tokens[key] if re.fullmatch(r"#[\da-fA-F]{6}", tokens[key]) else "#fafafa"
                          for key in ("background", "card", "foreground", "primary", "secondary")]
        folder = write_bundle(out, "uipro-" + slug, title, "uipro", summary, f"{title}: {row['Keywords']}. Fits: {row['Best For']}. {row['Aliases']}",
            {"references/style.json": json.dumps(row, ensure_ascii=False, indent=2) + "\n", "references/style.md": spec + "\n", "LICENSE": (root / "LICENSE").read_bytes()}, [source_path],
            [{"file": "assets/preview.webp", "label": "Образец по спецификации стиля"}],
            [{"label": "Каталог UI UX Pro Max", "url": "https://www.uupm.cc/"}, {"label": "Исходная спецификация", "url": f"https://github.com/{SOURCES['uipro']['repo']}/blob/{SOURCES['uipro']['sha']}/{source_path}"}],
            preview_colors, props.get("font-family", ""), row["Type"], "The preview is a locally rendered, illustrative specimen of the style's colors and concrete CSS properties, not an upstream screenshot. Consult the full specification for materials, composition, motion and platform requirements; sample values fill gaps where the source is qualitative.")
        page = folder / "assets/preview.html"
        page.write_text(specimen(title, "uipro", tokens, row["Preferred Mode"], props))
        jobs.append({"html": str(page.resolve()), "image": str(page.with_suffix(".webp").resolve())})
        folders.append(folder)
    return folders, jobs


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache", type=Path, required=True)
    parser.add_argument("--out", type=Path, default=HERE / "skills")
    parser.add_argument("--fetch", action="store_true")
    args = parser.parse_args()
    if args.fetch:
        fetch_sources(args.cache)
    for name, source in SOURCES.items():
        if json.loads((args.cache / name / "source.json").read_text()) != source:
            raise ValueError(f"Cache revision mismatch: {name}")
    typeui = import_typeui(args.cache, args.out)
    tweakcn, tweak_jobs = import_tweakcn(args.cache, args.out)
    uipro, uipro_jobs = import_uipro(args.cache, args.out)
    jobs = tweak_jobs + uipro_jobs
    manifest = {"sources": SOURCES, "counts": {"typeui": len(typeui), "tweakcn": len(tweakcn), "uipro": len(uipro)}, "previews": jobs}
    # A local rendering queue contains absolute paths and stays in the import cache.
    (args.cache / "render-manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(manifest["counts"]) + f"; {len(jobs)} previews to render")


if __name__ == "__main__":
    main()
