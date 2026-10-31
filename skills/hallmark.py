#!/usr/bin/env python3
"""Hallmark (github.com/nutlope/hallmark, MIT) as the chat's skills: its 50 themes become «style» skills, the rest
stays one manual skill, skills/skills/hallmark, whose SKILL.md is ours (adapted to FigCraft) and is left alone here.

    skills/hallmark.py <hallmark checkout> [--ref <commit>]

A theme's OKLCH colours are written as hex (FigCraft takes #RRGGBB[AA]), its genre file goes in with it, and the
HTML font links are dropped. Run it again to take a newer Hallmark: the generated folders are replaced.
"""
import argparse
import json
import math
import os
import re
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "skills")
REPO = "https://github.com/nutlope/hallmark"

GENRE = {"editorial": "редакционный", "modern-minimal": "минимализм", "atmospheric": "атмосферный", "playful": "игривый"}
PAPER = {"light": "светлый", "mid": "средний тон", "dark": "тёмный"}
POSTURE = {"restrained": "сдержанный акцент", "committed": "уверенный акцент", "full-palette": "полная палитра",
           "drenched": "залит цветом"}

ADAPT = """\
# {name} — a Hallmark style

The designer chose this style for the chat. A style is a material: paper, ink, faces, rules, radius, depth, controls
and voice. It is never a layout. It was written for web pages in CSS; in FigCraft:

- **Tokens become the file's variables.** Look at the file's variables first (`variable.export`). With no colour
  collection for this style, make one named «{name}»: the `--color-*` tokens as colour variables without the prefix
  (`paper`, `ink`, `accent`…), radii as numbers; bind fills, strokes and radii to them (`variable.bind`), never paste
  hex. A file that already has its own colour system keeps it: restyle it onto this one only when asked.
- **Faces.** Check each family with `text.fonts {{family}}`. A missing one: say so in one line and take the nearest
  installed face of the same class ({display_class}); never swap silently. Make text styles for display, body, labels
  and code from the Type section.
- **CSS in FigCraft terms.** box-shadow → drop or inner shadow effects; border → an inside stroke; border-radius →
  cornerRadius; `corner-shape: bevel` has no equivalent, use the fallback radius; gradients → gradient fills;
  `var()` and `color-mix()` → the nearest token. Hover, pressed, focus, disabled are component variants, not
  transitions. Motion does not apply to a static mockup.
- **App screens** (most work here): the style lends its palette, faces, radius and surfaces, never its layout,
  navigation or ornament. The accent marks the primary action, the selection and state, nothing else; a second
  neutral carries sidebars, toolbars and panels; controls are 32 to 40 px; the type scale steps by 1.125 to 1.2 and
  no display face sits on labels, buttons or data. Range, textures, generated fields and photographs are for pages.
- **Colours below are hex,** converted from the theme's OKLCH (an alpha is the last two digits).
"""


def oklch_hex(L, C, H, alpha=None):
    a, b = C * math.cos(math.radians(H)), C * math.sin(math.radians(H))
    l_ = (L + 0.3963377774 * a + 0.2158037573 * b) ** 3
    m_ = (L - 0.1055613458 * a - 0.0638541728 * b) ** 3
    s_ = (L - 0.0894841775 * a - 1.2914855480 * b) ** 3
    rgb = (4.0767416621 * l_ - 3.3077115913 * m_ + 0.2309699292 * s_,
           -1.2684380046 * l_ + 2.6097574011 * m_ - 0.3413193965 * s_,
           -0.0041960863 * l_ - 0.7034186147 * m_ + 1.7076147010 * s_)
    out = "#"
    for x in rgb:
        x = 12.92 * x if x <= 0.0031308 else 1.055 * max(x, 0) ** (1 / 2.4) - 0.055
        out += f"{round(min(max(x, 0), 1) * 255):02X}"
    if alpha is not None and alpha < 1:
        out += f"{round(alpha * 255):02X}"
    return out


OKLCH = re.compile(r"oklch\(\s*([\d.]+)(%?)\s+([\d.]+)\s+([\d.]+)(?:deg)?\s*(?:/\s*([\d.]+)(%?))?\s*\)")


def hexed(text):
    def one(m):
        L = float(m[1]) / (100 if m[2] else 1)
        alpha = None if m[5] is None else float(m[5]) / (100 if m[6] else 1)
        return oklch_hex(L, float(m[3]), float(m[4]), alpha)
    return OKLCH.sub(one, text)


def header(text):
    """A theme file's header block (flat `key: value` lines) and what follows it."""
    _, head, body = text.split("---", 2)
    fields = {}
    for line in head.strip().splitlines():
        k, _, v = line.partition(":")
        fields[k.strip()] = v.strip()
    return fields, body.lstrip("\n")


def token(body, name):
    m = re.search(rf"--color-{name}:\s*(#[0-9A-F]{{6}})\b", body)
    return m[1] if m else None


def style_skill(theme, genres):
    with open(theme, encoding="utf-8") as f:
        h, body = header(f.read())
    body = hexed(body)
    body = re.sub(r"\A# .*\n+", "", body)  # our title replaces the theme's
    body = re.sub(r"```html\n.*?```\n*", "", body, flags=re.S)  # font <link>s for a web page
    body = body.replace("\n## ", "\n### ").replace("\n# ", "\n## ")
    display_class, _, face = h["display"].partition(" ")
    colors = [c for c in (token(body, n) for n in ("paper", "paper-2", "ink", "accent", "accent-2")) if c]
    summary = ", ".join(x for x in (GENRE.get(h["genre"]), PAPER.get(h["paper"].split()[0]),
                                    POSTURE.get(h["posture"])) if x)
    description = f"{h['name']}: {h['material']}. Fits: {h['keywords']}"
    genre = genres.get(h["genre"], "").replace("# Genre:", "## Genre:", 1)
    genre = re.sub(r"\n+Stamp: .*$", "\n", genre.strip()) + "\n"
    front = "\n".join([
        "---",
        f"name: hallmark-{h['slug']}",
        "description: " + json.dumps(description, ensure_ascii=False),
        "metadata:",
        "  group: style",
        "  origin: hallmark",
        "  category: themes",
        f"  style: {h['genre']}",
        "  mode: manual",
        f"  title: {h['name']}",
        f"  summary: {summary}",
        f"  preview: \"{' '.join(colors[:5])} · {face}\"",
        "---", ""])
    text = front + ADAPT.format(name=h["name"], display_class=display_class) + "\n" + genre + "\n## The theme\n\n" + body
    return h, text.rstrip() + "\n"


def copy_references(src, dest, slug, ref):
    """Bundle the site's desktop/phone screenshots; a skill-only checkout has the theme JPG instead."""
    repo = os.path.abspath(os.path.join(src, "..", ".."))
    images, sources = [], []
    for kind, file, label in (("desk", "preview.webp", "Десктоп"), ("phone", "mobile.webp", "Телефон")):
        path = f"site/assets/{kind}/{slug}.webp"
        local = os.path.join(repo, path)
        if os.path.isfile(local):
            shutil.copy(local, os.path.join(dest, file))
            images.append({"file": file, "label": label})
            sources.append(f"{REPO}/blob/{ref}/{path}")
    if not images:
        path = os.path.join(src, "references", "themes", slug + ".jpg")
        if os.path.isfile(path):
            shutil.copy(path, os.path.join(dest, "preview.jpg"))
            images.append({"file": "preview.jpg", "label": "Десктоп"})
            sources.append(f"{REPO}/blob/{ref}/skills/hallmark/references/themes/{slug}.jpg")
    refs = {"images": images, "links": [
        {"label": "Открыть пример", "url": f"https://www.usehallmark.com/themes/{slug}/"},
        {"label": "Исходник темы", "url": f"{REPO}/blob/{ref}/skills/hallmark/references/themes/{slug}.md"}]}
    with open(os.path.join(dest, "references.json"), "w", encoding="utf-8") as f:
        json.dump(refs, f, ensure_ascii=False, indent=2)
        f.write("\n")
    return sources


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("hallmark", help="a Hallmark checkout (or its skills/hallmark folder)")
    ap.add_argument("--ref", default="main", help="the commit it is, for ATTRIBUTION.md")
    a = ap.parse_args()
    src = a.hallmark if os.path.isfile(os.path.join(a.hallmark, "SKILL.md")) else os.path.join(a.hallmark, "skills", "hallmark")
    refs = os.path.join(src, "references")
    genres = {}
    for g in os.listdir(os.path.join(refs, "genres")):
        with open(os.path.join(refs, "genres", g), encoding="utf-8") as f:
            genres[g[:-3]] = f.read()

    for d in os.listdir(OUT):
        if d.startswith("hallmark-"):
            shutil.rmtree(os.path.join(OUT, d))
    themes = []
    for t in sorted(os.listdir(os.path.join(refs, "themes"))):
        if not t.endswith(".md") or t == "README.md":
            continue
        h, text = style_skill(os.path.join(refs, "themes", t), genres)
        d = os.path.join(OUT, f"hallmark-{h['slug']}")
        os.makedirs(d)
        with open(os.path.join(d, "SKILL.md"), "w", encoding="utf-8") as f:
            f.write(text)
        images = copy_references(src, d, h["slug"], a.ref)
        with open(os.path.join(d, "ATTRIBUTION.md"), "w", encoding="utf-8") as f:
            f.write(f"# hallmark-{h['slug']}\n\n- Source: {REPO}/blob/{a.ref}/skills/hallmark/references/themes/{t}\n"
                    "- Changes: OKLCH as hex, the genre file added, notes for FigCraft on top\n"
                    + "".join(f"- Preview: {url}\n" for url in images) +
                    "- License: MIT, see ../hallmark/LICENSE\n")
        themes.append(h)

    # the rest of Hallmark: its references without the themes, which live in the style skills now
    dst = os.path.join(OUT, "hallmark")
    os.makedirs(dst, exist_ok=True)
    shutil.rmtree(os.path.join(dst, "references"), ignore_errors=True)
    shutil.copytree(refs, os.path.join(dst, "references"), ignore=lambda d, names: names if os.path.basename(d) == "themes" else [])
    os.rmdir(os.path.join(dst, "references", "themes"))
    shutil.copy(os.path.join(src, "LICENSE"), dst)
    rows = [f"| {h['name']} | `../hallmark-{h['slug']}/SKILL.md` | {h['genre']} | {h['paper'].split()[0]} | "
            f"{h['display'].partition(' ')[2]} | {h['keywords']} |" for h in themes]
    with open(os.path.join(dst, "references", "themes.md"), "w", encoding="utf-8") as f:
        f.write("# Themes\n\nEach is a style skill next to this one; read only the one you pick.\n\n"
                "| Theme | File | Genre | Paper | Display | Fits |\n| --- | --- | --- | --- | --- | --- |\n"
                + "\n".join(rows) + "\n")
    with open(os.path.join(dst, "ATTRIBUTION.md"), "w", encoding="utf-8") as f:
        f.write(f"# hallmark\n\n- Source: {REPO}/tree/{a.ref}/skills/hallmark\n"
                "- Changes: SKILL.md rewritten for FigCraft; scripts left out; themes and their preview pictures moved to the "
                "hallmark-* style skills (skills/hallmark.py)\n- License: see LICENSE\n")
    print(f"{len(themes)} styles, hallmark references in {dst}")


if __name__ == "__main__":
    main()
