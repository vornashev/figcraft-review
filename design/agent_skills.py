#!/usr/bin/env python3
"""Adds the skills screens L–P to the «Агент» page of design/review-ux.figcraft, as a row of their own under «Шаг 1».

How a chat picks design skills: «/» in the input, skills pinned to a chat, what the answer says it used, the library
(groups that new skills fall into) and one skill's card. Like agent_more.py it redraws only its own frames.
Run with review-ux.figcraft as the current document.
"""
from agent import *  # noqa: F403  (build.py's atoms, the panel's top bar, chips, marks, radio, group)
from agent_more import tabs

X0, Y = 0, 1830  # under «Шаг 1 · окно рядом»
SCREENS = ("L · Меню /", "M · Ответ со скиллами", "N · Скиллы чата", "O · Библиотека скиллов", "P · Карточка скилла")
XS = [X0 + i * 460 for i in range(len(SCREENS))]
NOTE_X, NOTE_W = X0 + len(SCREENS) * 460, 620

# Glyphs build.py doesn't have (Material Design Icons in the Nerd Font); "expanded" is the chevron, G["down"] a download.
SG = {k: chr(v) for k, v in dict(book=0xf0b64, palette=0xf03d8, phone=0xf011c, pin=0xf0403, shape=0xf0832,
                                  autofix=0xf0068, folder=0xf0256, cbOn=0xf0132, cbOff=0xf0131, chevron=0xf0140,
                                  chevronUp=0xf0143, lock=0xf033e, check=0xf05e0, puzzle=0xf0a66).items()}

# Groups come from the skill's SKILL.md (metadata.group); a skill without one lands in «Другие».
GROUPS = {
    "base": ("Основа", ACCENT, "book", "всегда в каждом ходе"),
    "style": ("Стиль", MAUVE, "palette", "один на чат"),
    "system": ("Дизайн-система", CYAN, "shape", "одна на чат"),
    "platform": ("Платформа", ORANGE, "phone", None),
    "quality": ("Качество", GREEN, "check", None),
    "task": ("Задачи", YELLOW, "autofix", None),
    "other": ("Другие", DIM, "puzzle", None),
}
GRAPHITE = ("#1C1D21", "#2A2B31", "#E4E6EE", "#8AA4FF")
PAPER = ("#F6F4EF", "#FFFFFF", "#1F2329", "#C2410C")
TOKYO = ("#1F2335", "#24283B", "#C0CAF5", "#7AA2F7")


def gicon(b, parent, group, size=14):
    _, color, icon, _ = GROUPS[group]
    return b.text(parent, SG[icon], size, color, name="Icon")


def skill_chip(b, parent, group, text, close=True, level=None):
    """A skill in the input or in an answer: its group's icon and colour; level says why it was used."""
    c = b.row(parent, text, gap=6, fill=SURFACE, cornerRadius=6, padding=[3, 8, 3, 6])
    gicon(b, c, group)
    b.text(c, text, 11, TEXT, name="Text")
    if level:
        b.text(c, level, 10, GREEN if level == "сам" else FAINT, name="Level")
    if close:
        b.text(c, G["close"], 14, FAINT, name="Remove")
    return c


def swatches(b, parent, colors, d=8):
    s = b.row(parent, "Preview", gap=2)
    for i, c in enumerate(colors):
        b.rect(s, f"Swatch {i + 1}", d, d, c, cornerRadius=2, stroke=LINE, strokeWeight=1)
    return s


def chevron(b, parent, up=False, color=FAINT):
    return b.text(parent, SG["chevronUp" if up else "chevron"], 14, color, name="Chevron")


def picker2(b, parent):
    p = b.row(parent, "Агент и модель", gap=6, cornerRadius=6, padding=[4, 8, 4, 6])
    mark(b, p, CLAUDE, "C", 16)
    b.text(p, "Claude Code", 11, DIM, name="Agent")
    b.text(p, "Opus 5.5", 11, TEXT, bold=True, name="Model")
    chevron(b, p)


def pinned_row(b, parent, names, open_=False):
    """The chat's pinned skills, above the input: stay for every message of this chat; a click opens N."""
    r = b.row(parent, "Скиллы чата", gap=6, sizingH="fill", cornerRadius=6, padding=[4, 6, 4, 6],
              fill=SURFACE if open_ else "none")
    b.text(r, SG["pin"], 14, MAUVE, name="Icon")
    b.text(r, "Скиллы чата", 11, FAINT, name="Label")
    b.text(r, " · ".join(names), 11, TEXT, name="Names")
    spacer(b, r)
    chevron(b, r, up=open_)
    return r


def composer2(b, p, chips=(), skills=(), pinned=(), typed=None, placeholder="Опиши, что поменять в макете…",
              pinned_open=False, focus=False):
    w = b.col(p, "Composer", gap=6, sizingH="fill", padding=[0, 10, 10, 10])
    if pinned:
        pinned_row(b, w, pinned, pinned_open)
    c = b.col(w, "Box", gap=8, sizingH="fill", fill=CARD, cornerRadius=12, padding=10,
              stroke=ACCENT if focus else BORDER, strokeWeight=1)
    if chips or skills:
        r = b.row(c, "Context", gap=6, sizingH="fill", wrap=True)
        for icon, text in chips:
            chip(b, r, icon, text)
        for group, text in skills:
            skill_chip(b, r, group, text)
    b.text(c, typed or placeholder, 13, TEXT if typed else FAINT, w="fill", name="Input")
    bar = b.row(c, "Bar", gap=6, sizingH="fill")
    button(b, bar, icon="add", kind="ghost", color=DIM, name="Attach")
    spacer(b, bar)
    picker2(b, bar)
    send = b.frame(bar, "Send", "horizontal", w=28, h=28, fill=ACCENT if typed else SURFACE, cornerRadius=14,
                   mainAlign="center", crossAlign="center")
    b.text(send, G["up"], 14, BG if typed else FAINT, name="Icon")
    b.text(w, "Enter — отправить · @ — слой или замечание · / — скилл", 10, FAINT, name="Hint")


def popover(b, p, name):
    m = b.col(p, name, gap=2, sizingH="fill", padding=[0, 10, 6, 10])
    return b.col(m, "Box", gap=2, sizingH="fill", fill=CARD, cornerRadius=10, padding=8, stroke=BORDER, strokeWeight=1,
                 effects=SHADOW)


def group_head(b, parent, group, note=None, pad=(8, 6, 4, 6)):
    title, _, _, rule = GROUPS[group]
    h = b.row(parent, title, gap=6, sizingH="fill", padding=list(pad))
    gicon(b, h, group)
    b.text(h, title.upper(), 10, FAINT, bold=True, name="Group", letterSpacing=1)
    if note or rule:
        b.text(h, "· " + (note or rule), 10, FAINT, name="Rule")
    return h


def check(b, parent, on, radio_=False):
    if radio_:
        f = b.frame(parent, "Radio", "horizontal", w=14, h=14, cornerRadius=7, stroke=ACCENT if on else BORDER,
                    strokeWeight=1.5, mainAlign="center", crossAlign="center")
        if on:
            b.ellipse(f, "Dot", 6, ACCENT)
        return f
    return b.text(parent, SG["cbOn" if on else "cbOff"], 14, ACCENT if on else FAINT, name="Checkbox")


def menu_item(b, parent, name, note, on=False, radio_=False, active=False, preview=None, source=None):
    r = b.row(parent, name, gap=8, sizingH="fill", cornerRadius=6, padding=[6, 8, 6, 8], fill=SEL if active else "none")
    check(b, r, on, radio_)
    b.text(r, name, 12, TEXT, name="Name")
    b.text(r, note, 10, FAINT, name="Note")
    spacer(b, r)
    if source:
        b.text(r, source, 10, CYAN, name="Source")
    if preview:
        swatches(b, r, preview)
    return r


def toggle(b, parent, on):
    t = b.frame(parent, "Toggle", "horizontal", w=28, h=16, cornerRadius=8, fill=ACCENT if on else SURFACE,
                padding=[2, 2, 2, 2], mainAlign="max" if on else "min", crossAlign="center")
    b.ellipse(t, "Knob", 12, BG if on else FAINT)
    return t


def mode_pill(b, parent, mode):
    color = {"Всегда": ACCENT, "Сам": GREEN, "Вручную": DIM}[mode]
    m = b.row(parent, "Режим", gap=2, cornerRadius=6, padding=[3, 6, 3, 8], stroke=LINE, strokeWeight=1)
    b.text(m, mode, 11, color, name="Mode")
    chevron(b, m)
    return m


def back_bar(b, p, title, note):
    t = b.row(p, "Top bar", gap=10, sizingH="fill", padding=[10, 10, 10, 10])
    icon_button(b, t, "back", "Назад")
    col = b.col(t, "Titles", gap=1, sizingH="fill")
    b.text(col, title, 13, TEXT, bold=True, name="Title")
    b.text(col, note, 10, FAINT, name="Note")
    b.rect(p, "Divider", PANEL_W, 1, LINE)
    return t


# ---- screens ----

def scene_slash(b, x, y):
    """«/» in the input: skills by group, several at once; chips appear as they are ticked."""
    p = panel(b, SCREENS[0], x, y)
    topbar(b, p, "Экран входа")
    tabs(b, p, "Чат", badge=0)
    spacer(b, p)
    box = popover(b, p, "Меню /")
    h = b.row(box, "Head", gap=6, sizingH="fill", padding=[2, 6, 4, 6])
    b.text(h, "/ — СКИЛЛЫ К СООБЩЕНИЮ", 10, FAINT, bold=True, name="Title", letterSpacing=1)
    spacer(b, h)
    b.text(h, "3 выбрано", 10, ACCENT, name="Count")
    group_head(b, box, "style")
    menu_item(b, box, "Graphite", "тихий инструмент", on=True, radio_=True, preview=GRAPHITE)
    menu_item(b, box, "Paper", "светлый, как документ", radio_=True, preview=PAPER)
    group_head(b, box, "system")
    menu_item(b, box, "Tokyo Night", "токены этого проекта", radio_=True, source="проект", preview=TOKYO)
    menu_item(b, box, "Material 3", "компоненты и токены M3", radio_=True)
    group_head(b, box, "platform")
    menu_item(b, box, "Android", "360 dp, жесты, панели", on=True, active=True)
    menu_item(b, box, "iOS", "390 pt, HIG, safe area")
    group_head(b, box, "quality", note="агент берёт сам, если подходит")
    menu_item(b, box, "better-typography", "шкала, пары, переносы", on=True)
    menu_item(b, box, "better-layout", "группы, выравнивание")
    more = b.row(box, "Ещё", gap=6, sizingH="fill", padding=[4, 8, 4, 30])
    b.text(more, "ещё 6 · better-colors, better-writing, Варианты…", 10, FAINT, name="Text")
    b.rect(box, "Divider", PANEL_W - 38, 1, LINE)
    foot = b.row(box, "Keys", gap=6, sizingH="fill", padding=[6, 6, 2, 6], wrap=True)
    for k, s in (("Space", "отметить"), ("Tab", "закрепить в чате"), ("Enter", "готово")):
        key(b, foot, k)
        b.text(foot, s, 10, FAINT, name="Hint")
    composer2(b, p, skills=(("style", "Graphite"), ("platform", "Android"), ("quality", "better-typography")),
              typed="Собери экран входа: почта, пароль, вход через Google /", focus=True)


def scene_answer(b, x, y):
    """The answer says which skills it used and why: always, the chat's, this message's, taken by itself."""
    p = panel(b, SCREENS[1], x, y)
    topbar(b, p, "Экран входа")
    tabs(b, p, "Чат", badge=0)
    body = b.col(p, "Messages", gap=14, sizingH="fill", sizingV="fill", padding=[16, 14, 16, 14])
    me = b.col(body, "Вы", gap=8, sizingH="fill", fill=CARD, cornerRadius=10, padding=12)
    r = b.row(me, "Context", gap=6)
    skill_chip(b, r, "quality", "better-typography", close=False)
    b.text(me, "Собери экран входа: почта, пароль, вход через Google", 12, TEXT, w="fill", name="Text")
    ag = b.col(body, "Агент", gap=10, sizingH="fill")
    who = b.row(ag, "Who", gap=8)
    mark(b, who, CLAUDE, "C")
    b.text(who, "Claude · Opus 5.5 · $0.11", 11, DIM, bold=True, name="Name")
    used = b.col(ag, "Скиллы", gap=8, sizingH="fill", fill=SECTION, cornerRadius=8, padding=[8, 10, 10, 10])
    h = b.row(used, "Head", gap=6, sizingH="fill")
    b.text(h, SG["book"], 14, MAUVE, name="Icon")
    b.text(h, "Скиллы · 5", 11, DIM, name="Summary")
    b.text(h, "4 выбраны, 1 сам", 11, FAINT, name="Note")
    spacer(b, h)
    chevron(b, h, up=True)
    cs = b.row(used, "Chips", gap=6, sizingH="fill", wrap=True)
    for group, name, level in (("base", "figcraft-design", "всегда"), ("style", "Graphite", "чат"),
                               ("platform", "Android", "чат"), ("quality", "better-typography", "сообщение"),
                               ("quality", "better-accessibility", "сам")):
        skill_chip(b, cs, group, name, close=False, level=level)
    steps = b.row(ag, "Шаги", gap=6, sizingH="fill", fill=SECTION, cornerRadius=8, padding=[8, 10, 8, 10])
    b.text(steps, "9 шагов · 9 ok", 11, FAINT, name="Summary")
    b.text(ag, "Собрал «Вход» 360 × 800: заголовок, почта, пароль с показом, «Войти» и «Через Google» ниже, "
               "ссылка «Забыли пароль?». Рядом состояния: ошибка пароля и загрузка.", 12, TEXT, w="fill", name="Text")
    b.text(ag, "Проверка: цели 48 dp, контраст текста 7.2:1, поля подписаны, ошибка не только цветом.",
           11, DIM, w="fill", name="Check line")
    bar = b.row(ag, "Изменено", gap=6, sizingH="fill", fill=SECTION, cornerRadius=8, padding=[4, 4, 4, 10])
    b.text(bar, G["edit"], 14, GREEN, name="Icon")
    b.text(bar, "Изменено: 3 фрейма", 11, DIM, name="Text")
    spacer(b, bar)
    for a in ("Показать", "Отменить"):
        button(b, bar, a, kind="ghost", color=DIM)
    composer2(b, p, pinned=("Graphite", "Android"))


def scene_pinned(b, x, y):
    """The chat's skills: what is always on, what this chat pinned, whether the agent may pick more itself."""
    p = panel(b, SCREENS[2], x, y)
    topbar(b, p, "Экран входа")
    tabs(b, p, "Чат", badge=0)
    spacer(b, p)
    box = popover(b, p, "Скиллы чата")
    h = b.row(box, "Head", gap=6, sizingH="fill", padding=[2, 6, 2, 6])
    b.text(h, "СКИЛЛЫ ЭТОГО ЧАТА", 10, FAINT, bold=True, name="Title", letterSpacing=1)
    lead = b.row(box, "Lead", gap=0, sizingH="fill", padding=[0, 6, 0, 6])
    b.text(lead, "Идут с каждым сообщением, пока не уберёшь", 11, FAINT, w="fill", name="Text")
    sec = b.row(box, "Всегда", gap=8, sizingH="fill", padding=[10, 6, 4, 6])
    b.text(sec, "ВСЕГДА", 10, FAINT, bold=True, name="Title", letterSpacing=1)
    r = b.row(box, "figcraft-design", gap=8, sizingH="fill", padding=[6, 8, 6, 8])
    gicon(b, r, "base")
    b.text(r, "figcraft-design", 12, TEXT, name="Name")
    b.text(r, "продуктовый UI", 10, FAINT, name="Note")
    spacer(b, r)
    b.text(r, SG["lock"], 14, FAINT, name="Lock")
    sec = b.row(box, "Закреплены", gap=8, sizingH="fill", padding=[10, 6, 4, 6])
    b.text(sec, "ЗАКРЕПЛЕНЫ В ЧАТЕ · 2", 10, FAINT, bold=True, name="Title", letterSpacing=1)
    for group, name, note, prev in (("style", "Graphite", "стиль", GRAPHITE), ("platform", "Android", "платформа", None)):
        r = b.row(box, name, gap=8, sizingH="fill", cornerRadius=6, padding=[6, 8, 6, 8], fill=HOVER if prev else "none")
        gicon(b, r, group)
        b.text(r, name, 12, TEXT, name="Name")
        b.text(r, note, 10, FAINT, name="Note")
        spacer(b, r)
        if prev:
            swatches(b, r, prev)
        b.text(r, G["close"], 14, FAINT if not prev else DIM, name="Remove")
    add = b.row(box, "Добавить", gap=8, sizingH="fill", padding=[6, 8, 6, 8])
    b.text(add, G["add"], 14, ACCENT, name="Icon")
    b.text(add, "Добавить скилл", 12, ACCENT, name="Label")
    spacer(b, add)
    key(b, add, "/")
    b.rect(box, "Divider", PANEL_W - 38, 1, LINE)
    auto = b.row(box, "Сам", gap=10, sizingH="fill", padding=[8, 8, 6, 8], crossAlign="min")
    col = b.col(auto, "Text", gap=2, sizingH="fill")
    b.text(col, "Агент может взять ещё", 12, TEXT, name="Title")
    b.text(col, "Скиллы с режимом «Сам» — по описанию, когда подходят к задаче. В ответе видно какие.",
           11, FAINT, w="fill", name="Note")
    toggle(b, auto, True)
    b.rect(box, "Divider", PANEL_W - 38, 1, LINE)
    foot = b.row(box, "Footer", gap=6, sizingH="fill", padding=[6, 4, 2, 4])
    button(b, foot, "Для новых чатов файла", kind="line")
    spacer(b, foot)
    button(b, foot, "Все скиллы", icon="arrow", kind="ghost", color=DIM)
    composer2(b, p, pinned=("Graphite", "Android"), pinned_open=True)


def lib_row(b, parent, group, name, note, mode, source=None, preview=None, first=False):
    if not first:
        b.rect(parent, "Divider", PANEL_W - 30, 1, LINE)
    r = b.row(parent, name, gap=10, sizingH="fill", padding=[8, 12, 8, 12])
    gicon(b, r, group)
    info = b.col(r, "Info", gap=2, sizingH="fill")
    nm = b.row(info, "Name", gap=6)
    b.text(nm, name, 12, TEXT, bold=True, name="Name")
    if preview:
        swatches(b, nm, preview)
    meta = b.row(info, "Meta", gap=6)
    b.text(meta, note, 10, FAINT, name="Note")
    if source:
        b.text(meta, "· " + source, 10, CYAN if source == "проект" else FAINT, name="Source")
    mode_pill(b, r, mode)


def lib_group(b, body, group, rows, note=None):
    g = b.col(body, GROUPS[group][0], gap=6, sizingH="fill")
    group_head(b, g, group, note=note, pad=(0, 2, 0, 2))
    lst = b.col(g, "List", gap=0, sizingH="fill", fill=CARD, cornerRadius=10, stroke=LINE, strokeWeight=1, clip=True)
    for i, row in enumerate(rows):
        lib_row(b, lst, group, *row, first=i == 0)
    return lst


def scene_library(b, x, y):
    """Settings › Скиллы: every skill by group, how each one is used, where they come from."""
    p = panel(b, SCREENS[3], x, y)
    back_bar(b, p, "Скиллы", "для всех файлов · 16")
    body = b.col(p, "Body", gap=14, sizingH="fill", sizingV="fill", padding=[12, 14, 12, 14])
    s = b.row(body, "Search", gap=8, sizingH="fill", fill=CARD, cornerRadius=8, padding=[7, 10, 7, 10], stroke=LINE,
              strokeWeight=1)
    b.text(s, G["search"], 14, FAINT, name="Icon")
    b.text(s, "Найти скилл…", 12, FAINT, name="Placeholder")
    f = b.row(body, "Группы", gap=6, sizingH="fill", wrap=True)
    for label, n, on in (("Все", 16, True), ("Стиль", 2, False), ("Дизайн-система", 2, False), ("Платформа", 2, False),
                         ("Качество", 7, False), ("Задачи", 2, False)):
        c = b.row(f, label, gap=4, cornerRadius=6, padding=[3, 8, 3, 8], fill=SEL if on else "none",
                  stroke=ACCENT if on else LINE, strokeWeight=1)
        b.text(c, label, 11, TEXT if on else DIM, name="Label")
        b.text(c, str(n), 10, FAINT, name="Count")
    lib_group(b, body, "base", [("figcraft-design", "продуктовый UI, самопроверка", "Всегда", "встроенный")])
    lib_group(b, body, "style", [("Graphite", "тихий инструмент", "Вручную", "встроенный", GRAPHITE),
                                 ("Paper", "светлый, как документ", "Вручную", "встроенный", PAPER)])
    lib_group(b, body, "system", [("Tokyo Night", "токены и компоненты", "Вручную", "проект", TOKYO),
                                  ("Material 3", "компоненты и токены M3", "Вручную", "мой")])
    lib_group(b, body, "platform", [("Android", "360 dp, жесты, панели", "Сам", "мой"),
                                    ("iOS", "390 pt, HIG, safe area", "Сам", "мой")])
    q = b.row(body, "Качество", gap=6, sizingH="fill", fill=CARD, cornerRadius=10, stroke=LINE, strokeWeight=1,
              padding=[9, 12, 9, 12])
    gicon(b, q, "quality")
    b.text(q, "КАЧЕСТВО · 7", 10, FAINT, bold=True, name="Group", letterSpacing=1)
    b.text(q, "better-* · все «Сам»", 10, FAINT, name="Note")
    spacer(b, q)
    chevron(b, q)
    spacer(b, body)
    foot = b.col(p, "Footer", gap=8, sizingH="fill", padding=[10, 14, 14, 14])
    b.rect(foot, "Divider", PANEL_W - 28, 1, LINE)
    r = b.row(foot, "Источники", gap=8, sizingH="fill")
    b.text(r, SG["folder"], 14, FAINT, name="Icon")
    b.text(r, "встроенные · мои · проект · pen.dev", 11, DIM, name="Sources")
    spacer(b, r)
    button(b, r, "Добавить", icon="add", kind="line")


def scene_card(b, x, y):
    """One skill: what it looks like (for a style), how it is used, what is inside, which agents load it."""
    p = panel(b, SCREENS[4], x, y)
    back_bar(b, p, "Graphite", "Стиль · встроенный · skills/style-graphite")
    body = b.col(p, "Body", gap=18, sizingH="fill", sizingV="fill", padding=[14, 14, 14, 14])
    pv = b.col(body, "Превью", gap=10, sizingH="fill", fill=GRAPHITE[0], cornerRadius=10, padding=14,
               stroke=LINE, strokeWeight=1)
    top = b.row(pv, "Образец", gap=10, sizingH="fill")
    b.text(top, "Aa", 22, GRAPHITE[2], bold=True, name="Type")
    col = b.col(top, "Шрифт", gap=1, sizingH="fill")
    b.text(col, "Inter · 13 / 20", 11, GRAPHITE[2], name="Font")
    b.text(col, "радиус 6 · плотно · без теней", 10, "#8B8F9C", name="Rules")
    btn_ = b.row(top, "Кнопка", gap=0, fill=GRAPHITE[3], cornerRadius=6, padding=[6, 12, 6, 12])
    b.text(btn_, "Войти", 12, GRAPHITE[0], bold=True, name="Label")
    sw = b.row(pv, "Цвета", gap=6, sizingH="fill")
    for c, role in zip(GRAPHITE, ("фон", "поверхность", "текст", "акцент")):
        cc = b.col(sw, role, gap=4, sizingH="fill")
        b.rect(cc, "Swatch", 10, 24, c, cornerRadius=4, sizingH="fill", stroke="#3A3C44", strokeWeight=1)
        b.text(cc, role, 10, "#8B8F9C", name="Role")
    b.text(body, "Тихий рабочий инструмент: серые поверхности, один холодный акцент только на главном действии, "
                 "плотные списки. Для редакторов и панелей, которые открыты весь день.", 12, DIM, w="fill", name="About")
    g = group(b, body, "Как применять")
    radio(b, g, "Только вручную", "Через / или закрепить в чате. Стиль — один на чат: выбор заменит текущий.", True)
    radio(b, g, "Агент берёт сам", "Когда задача подходит под описание скилла.", False)
    g = group(b, body, "Внутри · 4 файла · 14 КБ")
    lst = b.col(g, "Files", gap=4, sizingH="fill")
    for f, size in (("SKILL.md", "3 КБ"), ("tokens.md", "2 КБ"), ("components.md", "6 КБ"), ("examples/ · 2 картинки", "3 КБ")):
        r = b.row(lst, f, gap=8, sizingH="fill")
        b.text(r, G["file"], 14, FAINT, name="Icon")
        b.text(r, f, 11, DIM, name="Name")
        spacer(b, r)
        b.text(r, size, 10, FAINT, name="Size")
    g = group(b, body, "Агенты")
    lst = b.col(g, "Agents", gap=6, sizingH="fill")
    for agent, color, how in (("Claude Code", CLAUDE, "загружает сам"), ("pi", PI, "загружает сам"),
                              ("Codex", CODEX, "читает файлы по списку")):
        r = b.row(lst, agent, gap=8, sizingH="fill")
        mark(b, r, color, LETTER[agent], 16)
        b.text(r, agent, 11, TEXT, name="Agent")
        spacer(b, r)
        b.text(r, how, 10, FAINT, name="How")
    foot = b.row(p, "Footer", gap=8, sizingH="fill", padding=[10, 14, 14, 14])
    button(b, foot, "Закрепить в этом чате", icon=None, kind="primary", wide=True)
    button(b, foot, "Папка", kind="line")


def notes(b, x, y):
    """How it works, for the reader of the canvas: levels, groups, sources, what new skills declare."""
    n = b.col(None, "Как устроены скиллы", gap=18, w=NOTE_W, fill=SECTION, cornerRadius=12, padding=24, x=x, y=y)
    b.text(n, "Как устроены скиллы", 18, CAP, bold=True, name="Title")
    for title, text in (
            ("Четыре уровня", "Всегда — база (figcraft-design), включается в библиотеке. В чате — закреплены, видны "
                              "строкой над полем и идут с каждым сообщением. В сообщении — «/» ставит чип на один ход, "
                              "Tab в меню закрепляет в чате. Сам — агент берёт скилл с режимом «Сам» по описанию; "
                              "в ответе строка «Скиллы» говорит, что и почему было использовано."),
            ("Группы", "Основа, Стиль, Дизайн-система, Платформа, Качество, Задачи, Другие. Стиль и дизайн-система — "
                       "по одному в чате: второй заменяет первый (в меню это радио, а не галочка). Если выбраны оба, "
                       "компоненты и токены берутся из дизайн-системы, стиль задаёт остальное."),
            ("Новые скиллы", "Скилл — папка с SKILL.md. Группу, превью и режим по умолчанию он объявляет сам в "
                             "metadata; без них попадает в «Другие» и всё равно работает. Папку подхватывают без "
                             "перезапуска — ни меню, ни библиотеку править не нужно."),
            ("Источники", "встроенные — figcraft-review/skills · мои — ~/.config/figcraft-agent/skills · "
                          "проект — <проект>/.figcraft/skills, едут с репозиторием · pen.dev — ~/.pencil/skills, "
                          "только чтение. Одинаковое имя: проект > мои > встроенные."),
            ("Агентам", "Выбранные вручную сервер называет в ходе: «Используй скиллы: …» с путями. Claude и pi "
                        "загружают их сами, Codex читает файлы по списку.")):
        s = b.col(n, title, gap=6, sizingH="fill")
        b.text(s, title.upper(), 10, FAINT, bold=True, name="Head", letterSpacing=1)
        b.text(s, text, 12, DIM, w="fill", name="Text")
    code = b.col(n, "SKILL.md", gap=0, sizingH="fill", fill=RAIL, cornerRadius=8, padding=[12, 14, 12, 14],
                 stroke=LINE, strokeWeight=1)
    b.text(code, "---\nname: style-graphite\ndescription: Тихий рабочий инструмент: серые поверхности,\n"
                 "  один холодный акцент, плотные списки…\nmetadata:\n  group: style          # base · style · system ·\n"
                 "                         # platform · quality · task\n  title: Graphite\n"
                 "  preview: \"#1C1D21 #2A2B31 #E4E6EE #8AA4FF · Inter\"\n  mode: manual           # always · auto · manual\n---",
           11, TEXT, w="fill", name="Frontmatter")
    b.text(n, "Пример — style-graphite и Paper, Material 3, Android, iOS — будущие скиллы. Сейчас есть "
              "figcraft-design и семь better-*.", 11, FAINT, w="fill", name="Note")


def main():
    fc = FC()
    active = next(d for d in fc.cmd("doc.list") if d["active"])
    assert (active.get("path") or "").endswith("review-ux.figcraft"), f"open review-ux.figcraft first, not {active['name']}"
    page = next(p for p in fc.cmd("page.list") if p["name"] == "Агент")
    fc.cmd("page.select", id=page["id"])
    mine = [t["id"] for t in fc.tops() if t.get("name") in SCREENS + ("Как устроены скиллы",)
            or (t.get("name") in ("Подпись", "Сценарий", "Пояснение") and t.get("y", 0) >= Y - 160)]
    if mine:
        fc.cmd("edit.delete", ids=mine)
    b = B()
    caption_at(b, X0, Y - 150, "Скиллы в чате",
               "Как выбрать скиллы дизайна и применить в чате — один или несколько, на одно сообщение или на весь чат, "
               "и куда встанут новые: стили, дизайн-системы, платформы.", w=2200)
    for x, title, fn in zip(XS, ("L · / — скиллы к сообщению, несколько сразу", "M · Ответ говорит, какие скиллы взял",
                                 "N · Скиллы чата: всегда, закреплены, сам", "O · Библиотека: группы и режимы",
                                 "P · Карточка скилла стиля"),
                            (scene_slash, scene_answer, scene_pinned, scene_library, scene_card)):
        b.text(None, title, 14, CAP, bold=True, name="Подпись", x=x, y=Y - 30)
        fn(b, x, Y)
    notes(b, NOTE_X, Y)
    run(fc, b, "Agent panel: skills screens L–P")


if __name__ == "__main__":
    main()
