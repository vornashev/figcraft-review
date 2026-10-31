#!/usr/bin/env python3
"""Draws the review UX concept into the open FigCraft document (design/review-ux.figcraft).

Uses the builder in lib.py (vendored from omarchy-mihomo): Tokyo Night tokens, text styles, one batch.
Run with review-ux.figcraft as the current document; it adds a fresh copy of every frame.
"""

from lib import *  # noqa: E402,F403

CAP, DESK, SECTION = CANVAS["caption"], CANVAS["desktop"], CANVAS["section"]
ACCENT_HOVER, HIGHLIGHT = TOKENS["accent-hover"], TOKENS["highlight"]
SHADOW = [{"type": "dropShadow", "color": "#00000066", "offset": [0, 12], "radius": 32}]
STATUS = {"open": RED, "question": YELLOW, "review": CYAN, "accepted": GREEN}
CARD_W = 380
DOC = "Tabka — Newtab & Popup"


# ---- atoms ----

def pin(b, parent, n, color=RED, d=22, **kw):
    p = b.frame(parent, f"Pin #{n}", "horizontal", w=d, h=d, fill=color, cornerRadius=d // 2, mainAlign="center",
                crossAlign="center", **kw)
    b.text(p, str(n), 11 if d >= 22 else 10, BG, bold=True, name="Number")
    return p


def key(b, parent, s, color=FAINT, line=BORDER):
    k = b.row(parent, "Key", gap=0, padding=[1, 5, 1, 5], cornerRadius=4, stroke=line, strokeWeight=1)
    b.text(k, s, 10, color)
    return k


def button(b, parent, label=None, icon=None, kind="soft", keys=None, wide=False, color=None, name=None):
    fill = {"primary": ACCENT, "soft": SURFACE, "ghost": "none", "line": "none", "good": GREEN + "2E"}[kind]
    fg = {"primary": BG, "good": GREEN}.get(kind, color or TEXT)
    extra = {"stroke": BORDER, "strokeWeight": 1} if kind == "line" else {}
    if wide:
        extra["sizingH"] = "fill"
    r = b.row(parent, name or label or "Icon button", gap=6, fill=fill, cornerRadius=6,
              padding=[6, 10, 6, 10] if label else 5, **extra)
    if icon:
        b.text(r, G[icon], 14, fg, name="Icon")
    if label:
        b.text(r, label, 12, fg, bold=kind in ("primary", "good"), name="Label")
    if keys:
        if wide:
            spacer(b, r)
        key(b, r, keys, BG if kind == "primary" else FAINT, BG if kind == "primary" else BORDER)
    return r


def toast(b, parent, icon, text, action=None, color=GREEN, **kw):
    t = b.row(parent, "Toast", gap=10, fill=RAIL, cornerRadius=8, padding=[10, 14, 10, 14], stroke=BORDER, strokeWeight=1,
              effects=SHADOW, **kw)
    b.text(t, G[icon], 14, color, name="Icon")
    b.text(t, text, 12, TEXT, name="Text")
    if action:
        b.text(t, action, 12, ACCENT, bold=True, name="Action")
    return t


def caption_at(b, x, y, title, note, w=1180):
    b.text(None, title, 22, CAP, bold=True, name="Сценарий", x=x, y=y)
    b.text(None, note, 13, DIM, name="Пояснение", w=w, x=x, y=y + 36, textAutoResize="height")


# ---- the review card (the widget on the canvas) ----

def card(b, name, x, y):
    return b.col(None, name, gap=0, w=CARD_W, fill=BG, cornerRadius=12, stroke=BORDER, strokeWeight=1, strokeAlign="inside",
                 clip=True, effects=SHADOW, x=x, y=y)


def card_head(b, c, summary):
    h = b.row(c, "Header", gap=8, sizingH="fill", padding=[12, 12, 10, 14])
    t = b.col(h, "Titles", gap=2, sizingH="fill")
    b.text(t, "Ревью", 13, TEXT, bold=True, name="Title")
    b.text(t, f"{DOC} · {summary}", 11, FAINT, name="Summary")
    button(b, h, icon="refresh", kind="ghost", color=FAINT, name="Refresh")


def handoff(b, c, n, pressed=False, note="Открытые замечания с путями слоёв и инструкцией"):
    w = b.col(c, "Handoff", gap=6, sizingH="fill", padding=[0, 12, 12, 12])
    r = b.row(w, "Отдать агенту", gap=8, sizingH="fill", fill=ACCENT_HOVER if pressed else ACCENT, cornerRadius=8,
              padding=[10, 12, 10, 12], **({"stroke": TEXT, "strokeWeight": 2} if pressed else {}))
    b.text(r, G["copy"], 14, BG, name="Icon")
    b.text(r, f"Отдать агенту · {n}" if n else "Нечего отдавать", 13, BG, bold=True, name="Label")
    spacer(b, r)
    key(b, r, "SUPER+ALT+A", BG, BG)
    b.text(w, note, 10, FAINT, w="fill", name="Note")


def section(b, c, title, n, color, collapsed=False):
    b.rect(c, "Divider", CARD_W, 1, LINE)
    s = b.row(c, title, gap=8, sizingH="fill", padding=[10, 14, 6, 14])
    b.ellipse(s, "Dot", 8, color)
    b.text(s, title, 11, DIM, bold=True, name="Title")
    b.text(s, str(n), 11, FAINT, name="Count")
    spacer(b, s)
    b.text(s, G["collapsed" if collapsed else "expanded"], 14, FAINT, name="Chevron")


def remark_head(b, parent, n, color, text, layer, tag=None, tag_color=None):
    top = b.row(parent, "Top", gap=10, sizingH="fill", crossAlign="min")
    pin(b, top, n, color, 20)
    body = b.col(top, "Body", gap=2, sizingH="fill")
    b.text(body, text, 12, TEXT, w="fill", name="Text")
    b.text(body, layer, 10, FAINT, w="fill", name="Layer")
    if tag:
        b.text(top, tag, 10, tag_color, bold=True, name="Tag")
    return top


def row_open(b, c, n, text, layer, hover=False, new=False):
    r = b.col(c, f"#{n}", gap=6, sizingH="fill", padding=[8, 14, 8, 14], fill=HOVER if hover else HIGHLIGHT if new else "none")
    top = remark_head(b, r, n, RED, text, layer, "только что" if new else None, ACCENT)
    if hover:
        acts = b.row(top, "Actions", gap=2)
        button(b, acts, icon="arrow", kind="ghost", color=DIM, name="К слою")
        button(b, acts, icon="edit", kind="ghost", color=DIM, name="Изменить")
        button(b, acts, icon="remove", kind="ghost", color=DIM, name="Удалить")
    return r


def agent_says(b, parent, who, text, color):
    wrap = b.row(parent, "Agent", gap=0, sizingH="fill", crossAlign="min")
    b.frame(wrap, "Indent", None, w=30, h=1)
    a = b.col(wrap, "Reply", gap=4, sizingH="fill")
    b.text(a, who, 10, color, bold=True, name="Who")
    b.text(a, text, 12, DIM, w="fill", name="Says")
    return a


def row_question(b, c, n, text, layer, question, options):
    r = b.col(c, f"#{n}", gap=8, sizingH="fill", padding=[10, 14, 12, 14], fill=HIGHLIGHT)
    remark_head(b, r, n, YELLOW, text, layer, "вопрос", YELLOW)
    a = agent_says(b, r, "Claude спрашивает", question, YELLOW)
    for i, o in enumerate(options, 1):
        opt = b.row(a, f"Вариант {i}", gap=8, sizingH="fill", fill=SURFACE, cornerRadius=6, padding=[7, 10, 7, 8])
        key(b, opt, str(i))
        b.text(b.col(opt, "Text", sizingH="fill"), o, 12, TEXT, w="fill", name="Label")
    own = b.row(a, "Свой ответ", gap=8, sizingH="fill", cornerRadius=6, padding=[7, 10, 7, 10], stroke=BORDER, strokeWeight=1)
    b.text(own, "или ответь словами…", 12, FAINT, name="Placeholder")
    return r


def thumb(b, parent, label, after):
    t = b.col(parent, label, gap=4, sizingH="fill")
    f = b.frame(t, "Preview", None, w=150, h=64, fill=SECTION, cornerRadius=6, clip=True, sizingH="fill",
                stroke=CYAN if after else LINE, strokeWeight=1)
    b.rect(f, "Sidebar", 40, 64, CARD)
    if after:
        for i in range(4):
            b.rect(f, "Tile", 7, 7, RED if i == 0 else SURFACE, x=4 + i * 9, y=5, cornerRadius=2)
    b.rect(f, "Name", 24, 5, SURFACE, x=5, y=18 if after else 6, cornerRadius=2)
    for i in range(3):
        b.rect(f, "Page", 28, 4, SURFACE, x=5, y=(30 if after else 18) + i * 9, cornerRadius=2)
    b.text(t, label, 10, CYAN if after else FAINT, name="Label")


def row_review(b, c, n, text, layer, summary):
    r = b.col(c, f"#{n}", gap=8, sizingH="fill", padding=[10, 14, 12, 14], fill=HIGHLIGHT)
    remark_head(b, r, n, CYAN, text, layer, "проверь", CYAN)
    a = agent_says(b, r, "Claude сделал", summary, CYAN)
    th = b.row(a, "Было / стало", gap=8, sizingH="fill")
    thumb(b, th, "было", False)
    thumb(b, th, "стало", True)
    acts = b.row(a, "Actions", gap=6, sizingH="fill")
    button(b, acts, "Принять", "check", "good", keys="Enter")
    button(b, acts, "Вернуть", "undo", "line")
    spacer(b, acts)
    button(b, acts, icon="arrow", kind="ghost", color=DIM, name="К слою")
    return r


# ---- the FigCraft canvas with a mock screen ----

SX, SY = 40, 56  # the mock screen inside the canvas frame
TITLE = (146, 13)


def canvas(b, name, x, y):
    f = b.frame(None, name, None, w=760, h=500, fill=RAIL, cornerRadius=12, clip=True, x=x, y=y, stroke=BORDER,
                strokeWeight=1, strokeAlign="inside")
    b.text(f, "Главная · новый стиль", 11, FAINT, name="Frame name", x=SX, y=SY - 20)
    s = b.frame(f, "Макет", None, w=600, h=400, x=SX, y=SY, fill=SECTION)
    b.rect(s, "Sidebar", 130, 400, CARD)
    b.rect(s, "Workspaces", 98, 16, SURFACE, x=16, y=16, cornerRadius=4)
    for i in range(7):
        b.rect(s, "Page", 70 + (i * 13) % 30, 8, SURFACE, x=16, y=52 + i * 24, cornerRadius=3)
    b.text(s, "Главная", 14, TEXT, bold=True, name="Title", x=TITLE[0], y=TITLE[1])
    for i in range(3):
        b.rect(s, "Action", 22, 22, SURFACE, x=514 + i * 28, y=11, cornerRadius=5)
    for i in range(2):
        for j in range(3):
            cell = b.frame(s, "Card", None, w=134, h=84, x=146 + j * 146, y=60 + i * 96, fill=CARD, cornerRadius=6, clip=True)
            b.rect(cell, "Thumb", 134, 50, SURFACE)
            b.rect(cell, "Line", 80, 6, SURFACE, x=10, y=64, cornerRadius=3)
    return f


def selection_box(b, f, x, y, w, h, size):
    b.rect(f, "Selection", w, h, "none", x=x, y=y, stroke=ACCENT, strokeWeight=1.5)
    for hx, hy in ((x, y), (x + w, y), (x, y + h), (x + w, y + h)):
        b.rect(f, "Handle", 6, 6, TEXT, x=hx - 3, y=hy - 3, stroke=ACCENT, strokeWeight=1)
    s = b.row(f, "Size", gap=0, fill=ACCENT, cornerRadius=3, padding=[1, 5, 1, 5], x=x + w / 2 - 26, y=y + h + 6)
    b.text(s, size, 10, BG, name="Size")


PINS = {1: (16, 16), 2: (16, 124), 3: (514, 11), 4: TITLE}  # layer corners in the mock


def pins(b, f, colors):
    for n, color in colors.items():
        px, py = PINS[n]
        pin(b, f, n, color, x=SX + px - 11, y=SY + py - 11)


# ---- scenes ----

def header(b):
    b.text(None, "FigCraft Review", 40, CAP, bold=True, name="Заголовок", x=0, y=0)
    b.text(None, "Замечания к макету как разговор с агентом. Три нажатия на цикл: отметить, отдать, решить. "
                 "Всё, что ждёт тебя, — наверху; агент отвечает вариантами, и ты выбираешь кликом, а не пишешь.",
           15, DIM, name="Принцип", w=1180, x=0, y=60, textAutoResize="height")
    flow = b.row(None, "Цикл", gap=14, x=0, y=140)
    steps = [("Отметить", "Выделил слой, нажал N, написал, Enter. Пин с номером — сразу на слое.", "SUPER+ALT+N", RED),
             ("Отдать агенту", "Одна кнопка: открытые замечания с путями слоёв уходят в буфер.", "SUPER+ALT+A", ACCENT),
             ("Агент правит", "Сам отмечает: «сделал — проверь» или «вопрос» с вариантами.", "review.py done / ask", MAUVE),
             ("Решить", "Принять, вернуть или выбрать вариант — прямо в карточке или у пина.", "клик · 1 / 2", GREEN)]
    for i, (title, text, k, color) in enumerate(steps, 1):
        if i > 1:
            b.text(flow, "→", 22, FAINT, name="Arrow")
        s = b.col(flow, f"{i} · {title}", gap=8, w=262, fill=CARD, cornerRadius=10, padding=14, stroke=LINE, strokeWeight=1)
        t = b.row(s, "Title", gap=8)
        pin(b, t, i, color)
        b.text(t, title, 13, TEXT, bold=True, name="Title")
        b.text(s, text, 12, DIM, w="fill", name="Text")
        key(b, s, k)
    legend = b.row(None, "Статусы", gap=28, x=0, y=330)
    for color, name, note in ((RED, "Открыто", "у агента"), (YELLOW, "Вопрос", "ждёт твоего ответа"),
                              (CYAN, "Проверь", "агент сделал"), (GREEN, "Принято", "закрыто тобой")):
        it = b.row(legend, name, gap=8)
        pin(b, it, "N", color, 20)
        b.text(it, name, 12, TEXT, bold=True, name="Name")
        b.text(it, note, 12, FAINT, name="Note")


def scene_annotate(b, y):
    caption_at(b, 0, y, "1 · Отметить", "Выделяешь слой и жмёшь N: ввод открывается рядом со слоем, в нём уже имя слоя. "
               "Enter — пин с номером встаёт на слой, карточка ревью тут же показывает новое замечание. "
               "Ни типов, ни приоритетов: номер, текст, слой.")
    f = canvas(b, "1a · Ввод у слоя", 0, y + 100)
    pins(b, f, {1: RED, 2: RED, 3: RED})
    tx, ty = SX + TITLE[0] - 4, SY + TITLE[1] - 4
    selection_box(b, f, tx, ty, 72, 26, "64 × 18")
    pin(b, f, 4, RED, x=tx - 11, y=ty - 11, opacity=0.6)
    comp = b.col(f, "Ввод замечания", gap=10, w=330, fill=CARD, cornerRadius=10, padding=12, stroke=BORDER, strokeWeight=1,
                 effects=SHADOW, x=tx, y=ty + 54)
    top = b.row(comp, "Layer", gap=8, sizingH="fill")
    pin(b, top, 4, RED, 20)
    b.text(top, "TEXT «Title» · Header", 11, DIM, name="Layer")
    field = b.col(comp, "Field", gap=0, sizingH="fill", fill=BG, cornerRadius=6, padding=[8, 10, 8, 10], stroke=ACCENT,
                  strokeWeight=1)
    b.text(field, "Заголовок крупнее, как у «Дизайн» в карточках|", 13, TEXT, w="fill", name="Typed")
    hints = b.row(comp, "Hints", gap=10)
    for k, t in (("Enter", "добавить"), ("Shift+Enter", "ещё слой"), ("Esc", "отмена")):
        h = b.row(hints, t, gap=4)
        key(b, h, k)
        b.text(h, t, 10, FAINT, name="Hint")

    c = card(b, "1b · Карточка после Enter", 820, y + 100)
    card_head(b, c, "4 открыто")
    handoff(b, c, 4)
    section(b, c, "У агента", 4, RED)
    row_open(b, c, 4, "Заголовок крупнее, как у «Дизайн» в карточках", "Главная · новый стиль › Header › Title", new=True)
    row_open(b, c, 1, "Сейчас там другой вид", "Sidebar › WorkspaceHeader", hover=True)
    row_open(b, c, 2, "Встроить полоску пространств в дизайн проекта", "app-header › .workspace-strip")
    row_open(b, c, 3, "Подумать о компоновке", "app-header › .header-actions")
    toast(b, None, "check", "Добавлено #4", "Отменить", x=820, y=y + 560)


def scene_handoff(b, y):
    caption_at(b, 0, y, "2 · Отдать агенту", "Одна большая кнопка — главное действие карточки. В буфер уходит "
               "Markdown: инструкция, затем по замечанию — текст, слой, путь, компонент. Вставляешь агенту, ничего не дописывая.")
    c = card(b, "2a · Кнопка нажата", 0, y + 100)
    card_head(b, c, "4 открыто")
    handoff(b, c, 4, pressed=True, note="Скопировано — вставь агенту (Claude Code, Cursor…)")
    section(b, c, "У агента", 4, RED)
    for n, t, l in ((1, "Сейчас там другой вид", "Sidebar › WorkspaceHeader"),
                    (2, "Встроить полоску пространств в дизайн проекта", "app-header › .workspace-strip"),
                    (3, "Подумать о компоновке", "app-header › .header-actions"),
                    (4, "Заголовок крупнее, как у «Дизайн» в карточках", "Header › Title")):
        row_open(b, c, n, t, l)
    toast(b, None, "copy", "Скопировано 4 замечания — вставь агенту", color=ACCENT, x=440, y=y + 100)
    md = b.col(None, "2b · Что получит агент", gap=10, w=560, fill=SECTION, cornerRadius=10, padding=16, stroke=LINE,
               strokeWeight=1, x=440, y=y + 170)
    b.text(md, "ЧТО ПОЛУЧИТ АГЕНТ", 11, FAINT, bold=True, name="Title", letterSpacing=1)
    b.text(md, "# FigCraft — " + DOC + " · 4 замечания\n"
               "Поправь макет по замечаниям; значения — из дизайн-системы файла.\n"
               "Сделал — review.py done N \"…\"; вопрос — review.py ask N \"…\" --option …\n"
               "---\n"
               "## 4. Заголовок крупнее, как у «Дизайн» в карточках\n"
               "- Слой: `TEXT` «Title» · #23790\n"
               "- Путь: Главная · новый стиль › Header › Title\n"
               "- Текст: \"Главная\"\n"
               "## 1. Сейчас там другой вид\n"
               "…", 11, DIM, w="fill", name="Markdown", lineHeight=18)


def scene_decide(b, y):
    caption_at(b, 0, y, "3 · Решить", "Агент закончил — карточка сама собирает наверх то, что ждёт тебя. "
               "Вопрос приходит с вариантами: клик по варианту и есть ответ. Сделанное — с «было / стало» и двумя "
               "кнопками. Те же решения доступны у пина на холсте.")
    c = card(b, "3a · Ждут тебя", 0, y + 100)
    card_head(b, c, "2 ждут тебя")
    section(b, c, "Ждут тебя", 2, YELLOW)
    row_question(b, c, 3, "Подумать о компоновке", "app-header › .header-actions",
                 "Как собрать действия справа в шапке?",
                 ["Вид · ⋯ · «+ Коллекция» с подписью", "Только «+ Коллекция», вид — в меню ⋯"])
    row_review(b, c, 1, "Сейчас там другой вид", "Sidebar › WorkspaceHeader",
               "Добавил полоску пространств над шапкой, стрелку заменил на шестерёнку — как в приложении.")
    section(b, c, "У агента", 1, RED)
    row_open(b, c, 4, "Заголовок крупнее, как у «Дизайн» в карточках", "Header › Title")
    section(b, c, "Принято", 1, GREEN, collapsed=True)

    f = canvas(b, "3b · Решение у пина", 440, y + 100)
    pins(b, f, {1: CYAN, 2: GREEN, 3: YELLOW, 4: RED})
    px, py = SX + PINS[3][0], SY + PINS[3][1]
    pop = b.col(f, "Поповер у пина", gap=8, w=300, fill=CARD, cornerRadius=10, padding=12, stroke=BORDER, strokeWeight=1,
                effects=SHADOW, x=px - 300 + 22, y=py + 18)
    top = b.row(pop, "Top", gap=8, sizingH="fill")
    pin(b, top, 3, YELLOW, 20)
    b.text(top, "Claude спрашивает", 11, YELLOW, bold=True, name="Who")
    b.text(pop, "Как собрать действия справа в шапке?", 12, TEXT, w="fill", name="Question")
    for i, o in enumerate(["Вид · ⋯ · «+ Коллекция»", "Вид — в меню ⋯"], 1):
        opt = b.row(pop, f"Вариант {i}", gap=8, sizingH="fill", fill=SURFACE, cornerRadius=6, padding=[6, 10, 6, 8])
        key(b, opt, str(i))
        b.text(opt, o, 12, TEXT, name="Label")
    tip = b.row(f, "Подсказка у пина #1", gap=8, fill=CARD, cornerRadius=8, padding=[6, 10, 6, 8], stroke=BORDER,
                strokeWeight=1, x=SX + PINS[1][0] + 18, y=SY + PINS[1][1] + 22)
    b.text(tip, G["check"], 14, CYAN, name="Icon")
    b.text(tip, "Сделано — Enter принять", 11, DIM, name="Text")


def scene_done(b, y):
    caption_at(b, 0, y, "4 · Всё закрыто", "Когда всё принято, карточка говорит об этом одной строкой и предлагает "
               "следующий шаг. Принятые свёрнуты, их можно раскрыть.", w=380)
    c = card(b, "4 · Пусто", 0, y + 120)
    card_head(b, c, "всё принято")
    e = b.col(c, "Empty", gap=10, sizingH="fill", padding=[24, 20, 24, 20], crossAlign="center")
    b.text(e, G["statusCheck"], 22, GREEN, name="Icon")
    b.text(e, "Все 4 замечания приняты", 13, TEXT, bold=True, name="Title")
    b.text(e, "Выдели слой и нажми SUPER+ALT+N, чтобы начать новый круг", 12, FAINT, name="Hint", w=300, textAlign="center",
           textAutoResize="height")
    section(b, c, "Принято", 4, GREEN, collapsed=True)


def feasibility(b, x, y):
    b.text(None, "Что из этого есть в FigCraft 0.11", 22, CAP, bold=True, name="Сценарий", x=x, y=y)
    t = b.col(None, "Реализуемость (plugin API 3)", gap=0, w=760, fill=CARD, cornerRadius=10, stroke=LINE, strokeWeight=1,
              clip=True, x=x, y=y + 50)
    rows = [("Карточка с разделами и решениями", "можно", GREEN, "Виджет рисует что угодно из frame/text/rect, клики — target."),
            ("Варианты ответа, «Принять / Вернуть»", "можно", GREEN, "Клик в виджете → annotation.edit. Агент шлёт варианты: ask N \"…\" --option A --option B."),
            ("Статус «Проверь»", "можно", GREEN, "Ещё одна категория: done агента → «Проверь», «Принять» → «Принято»."),
            ("Было / стало", "обход", YELLOW, "Виджет показывает image: review.py кладёт PNG до и после правки в состояние виджета."),
            ("Пины с номерами на слоях", "обход", YELLOW, "Плагин не рисует поверх холста: номера видны в Dev Mode, или слои-метки в скрытой группе «Ревью»."),
            ("Ввод у слоя по N", "обход", YELLOW, "Своих хоткеев у плагина нет: SUPER+ALT+N открывает окно ввода с именем слоя."),
            ("Кнопка «Отдать агенту» копирует", "нельзя", RED, "Буфера у плагина нет: копирует SUPER+ALT+A, кнопка в карточке — подсказка."),
            ("Клавиши 1 / 2 / Enter для решений", "нельзя", RED, "Только клики по виджету; клавиши — в будущем API или через хоткеи review.py.")]
    for i, (what, verdict, color, how) in enumerate(rows):
        r = b.row(t, what, gap=16, sizingH="fill", padding=[10, 16, 10, 16], crossAlign="min", fill=HOVER if i % 2 else "none")
        b.text(r, what, 12, TEXT, bold=True, name="What", w=230, textAutoResize="height")
        v = b.row(r, "Verdict", gap=6, w=70)
        b.ellipse(v, "Dot", 8, color)
        b.text(v, verdict, 12, color, name="Verdict")
        b.text(r, how, 12, DIM, w="fill", name="How")


def main():
    fc = FC()
    b = B()
    header(b)
    scene_annotate(b, 460)
    scene_handoff(b, 1220)
    scene_decide(b, 1880)
    scene_done(b, 2840)
    feasibility(b, 440, 2840)
    run(fc, b, "Review UX concept")


if __name__ == "__main__":
    main()
