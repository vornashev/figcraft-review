"""Design skills: where they come from, their group and mode, and what one turn of a chat gets of them.

A skill is a folder with SKILL.md. Its frontmatter may say how the chat shows and uses it:

    metadata:
      group: style      # base · style · system · platform · quality · task (anything else: other)
      mode: manual      # always · auto (the agent picks it by its description) · manual (only when chosen)
      title: Graphite
      summary: тихий инструмент
      preview: "#1C1D21 #2A2B31 #E4E6EE #8AA4FF · Inter"

The chat uses skills on three levels — always (mode), pinned to the chat, attached to one message — and lists the
«auto» ones for the agent to open itself. Chosen skills go into the prompt as their SKILL.md, once per agent session.

A task skill with a reference image (OpenDesign's) is used as the chat's reference mode says: a checklist of content
and structure (the default), an inspiration for hierarchy and rhythm, or a replica of the picture.
"""
import json
import os
import re
import shutil
import time
from urllib.parse import urlencode, urlsplit

HERE = os.path.dirname(os.path.abspath(__file__))
GROUPS = ("base", "style", "system", "library", "platform", "quality", "task", "other")
EXCLUSIVE = {"system"}  # design systems are exclusive; themes can be combined
MODES = ("always", "auto", "manual")
LEVELS = ("always", "chat", "message", "auto")
MAX_BODY = 20000
REFERENCES = ("checklist", "inspire", "replicate")
SOURCES = ("Порядок источников, когда они расходятся: макет и дизайн-система файла (если просят переделать макет — его "
           "контент и структура главные), затем задача дизайнера, стиль-скиллы и только потом задачные скиллы.")
REFERENCE = {
    "checklist": "Задачные скиллы с референсом ({names}) — чек-лист, а не образец: бери из них состав контента, порядок "
                 "блоков и проверки приёмки. Картинку-референс не открывай; в их references/prompt.md пропусти разделы о "
                 "референсе, визуальном направлении и сравнении с картинкой. Вид — из макета, дизайн-системы файла и "
                 "стиль-скиллов.",
    "inspire": "Задачные скиллы с референсом ({names}) — вдохновение: посмотри картинку-референс и возьми иерархию, ритм "
               "и плотность, но не палитру, шрифты и декоративные мотивы — их бери из файла и стиль-скиллов. До работы "
               "одной строкой назови, что берёшь и что нет. В конце сравни скриншот своей рамки с референсом: если "
               "совпадают палитра и раскладка, переделай.",
    "replicate": "Задачные скиллы с референсом ({names}) — реплика: воспроизведи композицию и визуальное направление "
                 "картинки-референса по их инструкциям; контент и бренд — дизайнера.",
}


def personal_dir():
    return os.path.expanduser("~/.config/figcraft-agent/skills")


def sources(file=None):
    """(id, folder) by priority: a skill of the same name in an earlier one wins."""
    out = []
    root = project_root(file) if file else None
    if root:
        out.append(("project", os.path.join(root, ".figcraft", "skills")))
    out += [("mine", personal_dir()),
            ("builtin", os.path.normpath(os.path.join(HERE, "..", "skills", "skills"))),
            ("pen.dev", os.path.expanduser("~/.pencil/skills"))]
    return out


def project_root(file):
    """The folder with .git above a design file, or None."""
    d = os.path.dirname(os.path.abspath(file))
    home = os.path.expanduser("~")
    while True:
        if os.path.exists(os.path.join(d, ".git")):
            return d
        up = os.path.dirname(d)
        if up == d or d == home:
            return None
        d = up


def _scalar(v):
    v = v.strip()
    if v[:1] in "\"'" and v[-1:] == v[:1] and len(v) > 1:
        return v[1:-1]
    return re.sub(r"\s+#.*$", "", v)


def frontmatter(text):
    """(fields, body) of a SKILL.md: top-level scalars, folded or literal blocks, and one level of nested maps."""
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end < 0:
        return {}, text
    head, rest = text[3:end], text[end + 4:]  # rest: what follows the closing ---, on its line and after
    body = rest.split("\n", 1)[1] if "\n" in rest else ""
    out, lines, i = {}, head.splitlines(), 0
    while i < len(lines):
        line = lines[i]
        i += 1
        if not line.strip() or line.lstrip().startswith("#") or line[:1] in " \t" or ":" not in line:
            continue
        key, _, val = line.partition(":")
        val = val.strip()
        if val and val not in (">", ">-", "|", "|-"):
            out[key.strip()] = _scalar(val)
            continue
        block = []
        while i < len(lines) and (not lines[i].strip() or lines[i][:1] in " \t"):
            block.append(lines[i])
            i += 1
        rows = [b.strip() for b in block if b.strip() and not b.strip().startswith("#")]
        if not val and rows and all(re.match(r"^[\w.-]+\s*:", r) for r in rows):
            out[key.strip()] = {k.strip(): _scalar(v) for k, _, v in (r.partition(":") for r in rows)}
        else:
            out[key.strip()] = ("\n" if val.startswith("|") else " ").join(rows)
    return out, body.lstrip("\n")


def read_skill(folder, source):
    try:
        with open(os.path.join(folder, "SKILL.md"), encoding="utf-8") as f:
            fields, _ = frontmatter(f.read(16000))
    except OSError:
        return None
    meta = fields.get("metadata") if isinstance(fields.get("metadata"), dict) else {}
    name = str(fields.get("name") or os.path.basename(folder))
    group = meta.get("group") if meta.get("group") in GROUPS else "other"
    # without a mode of its own: the agent may pick it, as Claude Code does — unless it is someone else's (pen.dev)
    mode = meta.get("mode") if meta.get("mode") in MODES else "manual" if source == "pen.dev" else "auto"
    desc = " ".join(str(fields.get("description") or "").split())
    out = {"name": name, "title": meta.get("title") or name, "summary": meta.get("summary") or desc[:90],
           "description": desc[:400], "group": group, "mode": mode, "source": source,
           "dir": folder, "path": os.path.join(folder, "SKILL.md")}
    for key in ("origin", "category", "style", "resource_kind", "formats", "resource_source", "access"):
        if isinstance(meta.get(key), str) and meta[key].strip():
            out[key] = meta[key].strip()[:100]
    if meta.get("preview"):
        colors = re.findall(r"#[0-9A-Fa-f]{6}\b", meta["preview"])
        font = meta["preview"].split("·", 1)[1].strip() if "·" in meta["preview"] else ""
        out["preview"] = {"colors": colors[:6], "font": font}
    images = references(out)["images"]
    if images:
        out["thumbnail"] = images[0]["url"]
    return out


_cache = {}


def catalog(file=None, ttl=3.0):
    """Every skill for a design file, by group then title; a new folder shows up within `ttl` seconds."""
    key = project_root(file) if file else None
    hit = _cache.get(key)
    if hit and time.time() - hit[0] < ttl:
        return hit[1]
    seen = {}
    for source, root in sources(file):
        if not os.path.isdir(root):
            continue
        for d in sorted(os.listdir(root)):
            folder = os.path.join(root, d)
            if os.path.isfile(os.path.join(folder, "SKILL.md")):
                s = read_skill(folder, source)
                if s and s["name"] not in seen:
                    seen[s["name"]] = s
    out = sorted(seen.values(), key=lambda s: (GROUPS.index(s["group"]), s["title"].lower()))
    _cache[key] = (time.time(), out)
    return out


def body(skill):
    try:
        with open(skill["path"], encoding="utf-8") as f:
            return frontmatter(f.read())[1][:MAX_BODY].strip()
    except OSError:
        return ""


def pick(cat, pinned=(), message=()):
    """[(skill, level)] a turn uses: the «always» ones, the chat's, this message's. A later level wins in a name
    and, for design systems, in the group. Styles from the chat and message are combined."""
    by = {s["name"]: s for s in cat}
    out = []
    for level, names in (("always", [s["name"] for s in cat if s["mode"] == "always"]), ("chat", pinned), ("message", message)):
        for n in names:
            s = by.get(n)
            if not s:
                continue
            out = [(p, lv) for p, lv in out if p["name"] != n and not (s["group"] in EXCLUSIVE and p["group"] == s["group"])]
            out.append((s, level))
    return out


def used(skill, level):
    return {"name": skill["name"], "title": skill["title"], "group": skill["group"], "level": level}


def referenced(skill):
    """A task skill that comes with a reference image: what the reference mode is about."""
    return skill["group"] == "task" and bool(references(skill)["images"])


def prompt(cat, picked, sent, auto=True, reference="checklist"):
    """The skills' part of a turn's prompt. `sent` ({names, index, reference}, kept per agent session) is updated: a
    skill whose text this session already has is only named, and the list of «auto» ones is repeated only when it
    changed. Task skills with a reference image get the order of sources and the reference mode with every turn
    that uses them, and once per change when the agent may only open them itself."""
    reference = reference if reference in REFERENCES else "checklist"
    parts = []
    new = [s for s, _ in picked if s["name"] not in sent["names"]]
    old = [s for s, _ in picked if s["name"] in sent["names"]]
    if new:
        parts.append("Скиллы к этому ходу — следуй им. Файлы, на которые они ссылаются, лежат рядом с SKILL.md:")
        for s in new:
            parts.append(f"<skill name=\"{s['name']}\" path=\"{s['path']}\">\n{body(s)}\n</skill>")
        sent["names"] = sent["names"] + [s["name"] for s in new]
    if old:
        parts.append("Продолжай следовать скиллам: " + ", ".join(s["title"] for s in old) + ".")
    have = {s["name"] for s, _ in picked} | set(sent["names"])  # chosen now, or their text is in the session already
    rest = [s for s in cat if s["mode"] == "auto" and s["name"] not in have] if auto else []
    index = auto_index(rest)
    if index and index != sent.get("index"):
        parts.append("Ещё скиллы: если задача о теме одного из них, открой его SKILL.md и следуй ему.\n" + index)
    sent["index"] = index
    tasks = [s["name"] for s, _ in picked if referenced(s)]
    if not tasks and any(referenced(s) for s in rest) and sent.get("reference") != reference:
        tasks = ["из списка"]
    if tasks:
        parts.append(SOURCES + " " + REFERENCE[reference].format(names=", ".join(tasks)))
        sent["reference"] = reference
    return "\n\n".join(parts)


def auto_index(rest):
    """The skills an agent may open itself, short: it goes into every request of the session, so each folder's path
    is given once, and a collection (OpenDesign's 230 task bundles…) is its names only: they say what they are."""
    out, folders = [], {}
    for s in rest:
        folders.setdefault(os.path.dirname(os.path.dirname(s["path"])), []).append(s)
    for folder, items in folders.items():
        out.append(f"{folder}/<имя>/SKILL.md:")
        out += [f"- {s['name']} — {s['summary']}" for s in items if not s.get("origin")]
        kits = {}
        for s in items:
            if s.get("origin"):
                kits.setdefault(s["origin"], []).append(s["name"])
        out += [f"- {origin}: {', '.join(names)}" for origin, names in kits.items()]
    return "\n".join(out)


SKILL_FILE = re.compile(r"([A-Za-z0-9._-]+)/SKILL\.md")


def named(raw, args):
    """The skill a tool call opens: Claude's Skill tool, or reading some …/<name>/SKILL.md (Read, cat, pi's read)."""
    if raw == "Skill" and isinstance(args, dict) and args.get("skill"):
        return str(args["skill"]).split(":")[-1]
    m = SKILL_FILE.search(str(args))
    return m.group(1) if m else None


STYLE_GROUPS = ("system", "library", "style")  # what `styles` offers: design systems, component libraries, styles


def styles_index(cat, query="", group=None, limit=40):
    """The style library as the agent's `styles` tool lists it: design systems and styles of every source, those
    with all words of `query` in their name, summary, description, origin or category. ([shown], total)."""
    words = str(query or "").lower().split()
    found = []
    for s in cat:
        if s["group"] not in STYLE_GROUPS or (group and s["group"] != group):
            continue
        hay = " ".join(str(s.get(k) or "") for k in ("name", "title", "summary", "description", "origin", "category", "style"))
        if all(w in hay.lower() for w in words):
            found.append(s)
    found.sort(key=lambda s: STYLE_GROUPS.index(s["group"]))
    return found[:limit], len(found)


def style_line(s):
    """One entry of the list: name — title · group · origin · platform · summary · colours · font."""
    p = s.get("preview") or {}
    kind = {"system": "дизайн-система", "library": "библиотека компонентов"}.get(s["group"], "стиль")
    bits = [s["title"], kind, s.get("origin") or s["source"],
            s.get("style"), s["summary"], " ".join(p.get("colors") or []), p.get("font")]
    return f"- {s['name']} — " + " · ".join(str(b) for b in bits if b)


def style_text(s):
    """A style in full for the agent that picked it: its SKILL.md and where its files and references are."""
    refs = references(s)
    images = ", ".join(os.path.join(s["dir"], i["file"]) for i in refs["images"][:6])
    return (f"<skill name=\"{s['name']}\" path=\"{s['path']}\">\n{body(s)}\n</skill>"
            + (f"\nКартинки-референсы: {images}" if images else ""))


def details(skill):
    """Inspect the catalog entry's own folder without following linked subdirectories."""
    files = []
    for root, dirs, names in os.walk(skill["dir"], followlinks=False):
        dirs[:] = sorted(d for d in dirs if not d.startswith(".") and not os.path.islink(os.path.join(root, d)))
        for name in sorted(names):
            path = os.path.join(root, name)
            if os.path.islink(path) or not os.path.isfile(path):
                continue
            files.append({"name": os.path.relpath(path, skill["dir"]), "size": os.path.getsize(path)})
            if len(files) >= 500:
                return {**skill, "body": body(skill), "files": files, "truncated": True, "references": references(skill)}
    return {**skill, "body": body(skill), "files": files, "truncated": False, "references": references(skill)}


IMAGE_TYPES = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp", ".gif": "image/gif"}


def image_path(skill, file):
    """Only raster images inside this skill's own folder, including through symlinks."""
    folder = os.path.realpath(skill["dir"])
    path = os.path.realpath(os.path.join(folder, file))
    if not path.startswith(folder + os.sep) or os.path.splitext(path)[1].lower() not in IMAGE_TYPES or not os.path.isfile(path):
        raise ValueError("Картинка навыка не найдена")
    return path


def references(skill):
    """Optional references.json: local preview images and links to the examples they show."""
    try:
        with open(os.path.join(skill["dir"], "references.json"), encoding="utf-8") as f:
            data = json.loads(f.read(65536))
    except (OSError, ValueError):
        return {"images": [], "links": []}
    if not isinstance(data, dict):
        return {"images": [], "links": []}
    images, links = [], []
    for entry in (data["images"][:16] if isinstance(data.get("images"), list) else []):
        if not isinstance(entry, dict) or not isinstance(entry.get("file"), str):
            continue
        try:
            image_path(skill, entry["file"])
        except (ValueError, OSError):
            continue
        images.append({"file": entry["file"], "label": str(entry.get("label") or "Превью")[:120],
                       "url": "/api/skill-image?" + urlencode({"name": skill["name"], "file": entry["file"]})})
    for entry in (data["links"][:20] if isinstance(data.get("links"), list) else []):
        if not isinstance(entry, dict) or not isinstance(entry.get("url"), str):
            continue
        try:
            u = urlsplit(entry["url"])
            if u.scheme not in ("http", "https") or not u.netloc:
                continue
        except ValueError:
            continue
        links.append({"url": entry["url"], "label": str(entry.get("label") or u.netloc)[:120]})
    return {"images": images, "links": links}


def reference_image(skill, file):
    if file not in {i["file"] for i in references(skill)["images"]}:
        raise ValueError("Картинка навыка не найдена")
    path = image_path(skill, file)
    with open(path, "rb") as f:
        return f.read(), IMAGE_TYPES[os.path.splitext(path)[1].lower()]


def import_folder(folder):
    """Copy a user-selected skill into the personal source; never replace an existing folder."""
    folder = os.path.realpath(os.path.expanduser(folder))
    skill = read_skill(folder, "mine")
    if not skill:
        raise ValueError("В папке не найден SKILL.md")
    name = os.path.basename(folder)
    if name.startswith(".") or not re.fullmatch(r"[\w.-]+", name):
        raise ValueError("Название папки должно состоять из букв, цифр, точек и дефисов")
    total, count = 0, 0
    for root, dirs, files in os.walk(folder, followlinks=False):
        for f in dirs + files:
            if os.path.islink(os.path.join(root, f)):
                raise ValueError("Для добавления выберите папку без символических ссылок")
        for f in files:
            total += os.path.getsize(os.path.join(root, f))
            count += 1
        if total > 32 * 1024 * 1024 or count > 1000:
            raise ValueError("Скилл больше 32 МБ или содержит больше 1000 файлов")
    target = personal_dir()
    os.makedirs(target, exist_ok=True)
    dest = os.path.join(target, name)
    if os.path.exists(dest):
        raise ValueError("Скилл с такой папкой уже есть в моих скиллах")
    if os.path.commonpath([folder, dest]) == folder:
        raise ValueError("Папка назначения находится внутри выбранного скилла")
    os.mkdir(dest)  # exclusive: a concurrent import cannot replace an existing skill
    try:
        shutil.copytree(folder, dest, dirs_exist_ok=True)
    except OSError:
        shutil.rmtree(dest, ignore_errors=True)
        raise
    _cache.clear()
    return read_skill(dest, "mine")
