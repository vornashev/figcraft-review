#!/usr/bin/env python3
"""Adds the variants screens VA–VE to the «Агент» page of design/review-ux.figcraft, a row under the source filters.

Variants the way pen.dev makes them good, run side by side: an orchestrator (an agent and model of its own) reads the
task, picks N different directions from the style library (every source: themes, design systems, later component
libraries) and lays out N frames; each lane — its own agent and model, its own guest in the file's live session, so
its own cursor and undo — draws one full variant in its frame; when all are done the orchestrator compares them.
Reruns redraw only these frames. Switches FigCraft to review-ux.figcraft for the run and back.
"""
from strict import (ACCENT, BG, BORDER, CARD, CLAUDE, DIM, FAINT, GREEN, INSET, LINE, MAUVE, ORANGE, SURFACE, TEXT,
                    B, FC, body, button, card, code, divider, glyph, inst, item, keys, label, menu, run, spacer,
                    text, top)

X0, Y = 0, 17400
SCREENS = ["VA · Варианты: дорожки", "VB · Стиль дорожки", "VC · Варианты в работе", "VD · Варианты готовы"]
CANVAS = "Strict · VE · На холсте"
NOTES = "Strict · Как работают варианты"
CODEX = "#5FD38D"
FILE = "person-site.figcraft"
TASK = "Новая главная портфолио: кейсы, обо мне, контакты"
LANES = [  # n, agent, model, style (origin · title), idea, swatches
    (1, "claude", "Opus 5.5", "Hallmark · Almanac", "Редакционный журнал", ["#F4EFE6", "#1E1B16", "#B4492F"]),
    (2, "codex", "GPT-6.1 Sol", "tweakcn · Graphite", "Тихий инструмент", ["#17181B", "#E6E7EA", "#8E95FF"]),
    (3, "claude", "Sonnet 5.5", "uipro · Swiss Grid", "Сетка и типографика", ["#FFFFFF", "#111111", "#E30613"]),
]


def screen(b, name, i, h=860):
    return b.col(None, "Strict · " + name, gap=0, w=400, h=h, fill=BG, cornerRadius=12, stroke=LINE, strokeWeight=1,
                 strokeAlign="inside", clip=True, x=X0 + i * 460, y=Y)


def mark(b, parent, agent, size=12):
    if agent == "claude":
        return glyph(b, parent, CLAUDE, ORANGE, size, name="Agent")
    return text(b, parent, "X", size, CODEX, True, name="Agent")


def swatches(b, parent, colors):
    s = b.row(parent, "Preview", gap=2)
    for k, c in enumerate(colors):
        b.rect(s, f"Swatch {k + 1}", 8, 8, c, cornerRadius=2, stroke=BORDER, strokeWeight=1)
    return s


def style_chip(b, parent, label_):
    return inst(b, parent, "chip", {"Kind": "Style", "Label": label_})


def count_pill(b, parent, n, open_=False):
    """×N next to the model: how many variants this message asks for; ×1 is the usual single answer."""
    r = b.row(parent, "Варианты", gap=4, h=26, sizingV="fixed", padding=[0, 8, 0, 8], cornerRadius=6,
              fill=SURFACE if open_ or n > 1 else "none", stroke=ACCENT if open_ else BORDER, strokeWeight=1)
    glyph(b, r, "\U000f0568", ACCENT if n > 1 else FAINT, 13, name="Icon")
    text(b, r, f"×{n}", 12, TEXT if n > 1 else DIM, n > 1, name="Count")
    return r


def composer_x(b, parent, hint, state="Empty", n=1, open_=False, model="Opus 5.5", mode="Только FigCraft"):
    c = b.col(parent, "Composer", gap=8, padding=[0, 12, 12, 12], sizingH="fill")
    inst(b, c, "input", {"State": state, "Text": hint}, sizingH="fill")
    r = b.row(c, "Model and variants", gap=6, sizingH="fill", crossAlign="center")
    inst(b, r, "model", {"Model": model, "Effort": "", "Mode": mode, "Show hint": False}, sizingH="fill")
    count_pill(b, r, n, open_)
    return c


def agent_select(b, parent, agent, model, name="Агент и модель"):
    r = b.row(parent, name, gap=6, h=28, sizingV="fixed", padding=[0, 8, 0, 8], cornerRadius=6, fill=INSET,
              stroke=LINE, strokeWeight=1)
    mark(b, r, agent)
    text(b, r, model, 12, TEXT, name="Model")
    glyph(b, r, "\U000f0140", FAINT, 12, name="Chevron")
    return r


def style_select(b, parent, style=None, colors=None):
    r = b.row(parent, "Стиль", gap=6, h=28, sizingV="fixed", padding=[0, 8, 0, 8], cornerRadius=6, sizingH="fill",
              fill=INSET, stroke=LINE, strokeWeight=1)
    glyph(b, r, "\U000f03d8", MAUVE if style else FAINT, 13, name="Icon")
    text(b, r, style or "Авто", 12, TEXT if style else DIM, name="Style", sizingH="fill", textAutoResize="truncate")
    if colors:
        swatches(b, r, colors)
    glyph(b, r, "\U000f0140", FAINT, 12, name="Chevron")
    return r


def segmented(b, parent, values, on):
    s = b.row(parent, "Количество", gap=2, padding=2, fill=INSET, cornerRadius=6, stroke=LINE, strokeWeight=1)
    for v in values:
        c = b.row(s, str(v), gap=0, w=34, h=24, sizingH="fixed", sizingV="fixed", mainAlign="center",
                  crossAlign="center", cornerRadius=4, fill=SURFACE if v == on else "none")
        text(b, c, f"×{v}", 12, TEXT if v == on else DIM, v == on)
    return s


def lane_card(b, parent, n, agent, model, style, idea, state, steps=None, took=None, undone=False):
    """One lane in the chat: who draws it, its direction, how far it got, and its own Показать / Отменить."""
    c = card(b, parent, f"Дорожка {n}", padding=[10, 12, 10, 12], gap=8)
    h = b.row(c, "Header", gap=8, sizingH="fill", crossAlign="center")
    text(b, h, str(n), 12, FAINT, True, name="Number")
    mark(b, h, agent)
    text(b, h, idea, 13, TEXT, True, name="Idea", sizingH="fill", textAutoResize="truncate")
    if state == "run":
        text(b, h, took or "", 12, FAINT, name="Time")
        b.ellipse(h, "Running", 8, ACCENT)
    elif state == "done":
        text(b, h, "✓", 12, GREEN, True, name="Status")
    elif state == "error":
        text(b, h, "×", 12, "#FF6B7A", True, name="Status")
    m = b.row(c, "Meta", gap=6, sizingH="fill", crossAlign="center")
    text(b, m, model, 12, DIM, name="Model")
    text(b, m, "·", 12, FAINT)
    style_chip(b, m, style)
    if steps:
        inst(b, c, "step", {"Status": "Running" if state == "run" else "Done", "Name": steps[0], "Args": steps[1],
                            "Time": steps[2]}, sizingH="fill")
    if state == "done":
        a = b.row(c, "Actions", gap=6, sizingH="fill", crossAlign="center")
        text(b, a, "Отменено" if undone else (took or ""), 12, FAINT, name="Summary")
        spacer(b, a)
        if not undone:
            button(b, a, "Показать")
            button(b, a, "Отменить")
    return c


def plan_block(b, parent):
    """The orchestrator's short plan: the anchor screen, its size and the N directions it chose."""
    p = b.col(parent, "План оркестратора", gap=8, sizingH="fill")
    h = b.row(p, "Who", gap=6, crossAlign="center")
    mark(b, h, "claude")
    text(b, h, "Оркестратор · Opus 5.5", 12, DIM, True)
    text(b, p, "Опорный экран — главная, 1440 × 1024. Три разных направления: журнал с крупной антиквой, "
               "тихий инструмент с плотной сеткой кейсов, швейцарская сетка. Рамки 1–3 справа от «01 Главная».",
         13, TEXT, name="Plan", sizingH="fill", textAutoResize="height")
    return p


# ---- screens ----

def setup(b, i):
    """VA: ×N opens the lanes: how many, who orchestrates, and each lane's agent, model and style."""
    s = screen(b, SCREENS[0], i)
    top(b, s, "Новый чат", FILE)
    body(b, s)
    composer_x(b, s, TASK, "Filled", n=3, open_=True)
    m = menu(b, s, "Variants menu", y=392)
    h = b.row(m, "Header", gap=8, padding=[8, 8, 6, 8], sizingH="fill", crossAlign="center")
    text(b, h, "Варианты", 12, DIM, True, name="Title")
    spacer(b, h)
    segmented(b, h, [1, 2, 3, 4, 6], 3)
    label(b, m, "Оркестратор", "план и сравнение")
    o = b.row(m, "Оркестратор", gap=8, padding=[4, 8, 6, 8], sizingH="fill", crossAlign="center")
    agent_select(b, o, "claude", "Opus 5.5")
    text(b, o, "выбирает направления, не рисует", 11, FAINT, name="Note", sizingH="fill", textAutoResize="truncate")
    divider(b, m, 4)
    label(b, m, "Дорожки", "каждая — свой агент, курсор и отмена")
    for n, agent, model, style, _, colors in LANES:
        r = b.row(m, f"Дорожка {n}", gap=8, padding=[4, 8, 4, 8], sizingH="fill", crossAlign="center")
        text(b, r, str(n), 12, FAINT, True, name="Number", w=10)
        agent_select(b, r, agent, model)
        style_select(b, r, style if n == 1 else None, colors if n == 1 else None)
    keys(b, m, [("1–6", "сколько"), ("↵", "готово")],
         right=lambda f: text(b, f, "Для новых чатов файла", 11, ACCENT, name="Defaults"))
    return s


def style_pick(b, i):
    """VB: a lane's style from the whole library — themes of every source, design systems — or Авто."""
    s = screen(b, SCREENS[1], i)
    top(b, s, "Новый чат", FILE)
    body(b, s)
    composer_x(b, s, TASK, "Filled", n=3, open_=True)
    m = menu(b, s, "Lane style", y=300)
    f = b.row(m, "Search", gap=8, padding=[7, 10, 7, 10], fill=INSET, cornerRadius=6, sizingH="fill")
    glyph(b, f, "\U000f0349", FAINT, 13)
    text(b, f, "Стиль дорожки 1…", 13, FAINT, name="Placeholder")
    item(b, m, "Авто", "оркестратор выберет разные", "\U000f0068", ACCENT,
         trail=lambda r: text(b, r, "✓", 12, TEXT, True, name="Check"), state="selected", two=True)
    label(b, m, "Дизайн-системы", "компоненты и токены", dot="#6CCFF6")
    item(b, m, "Tokyo Night", "токены этого проекта · проект", "\U000f0832", "#6CCFF6", two=True)
    label(b, m, "Стили", "238 · Hallmark, tweakcn, uipro, typeui", dot=MAUVE)
    for title, origin, colors, hover in [("Almanac", "Hallmark · журнал, антиква", ["#F4EFE6", "#1E1B16", "#B4492F"], True),
                                         ("Graphite", "tweakcn · тихий инструмент", ["#17181B", "#E6E7EA", "#8E95FF"], False),
                                         ("Swiss Grid", "uipro · сетка и гротеск", ["#FFFFFF", "#111111", "#E30613"], False),
                                         ("Brutal", "Hallmark · жёсткие рамки", ["#FFFDF5", "#000000", "#FF4D00"], False)]:
        item(b, m, title, origin, "\U000f03d8", MAUVE, trail=lambda r, c=colors: swatches(b, r, c),
             state="hover" if hover else None, two=True)
    keys(b, m, [("↑↓", "выбрать"), ("↵", "закрепить за дорожкой"), ("Esc", "назад")])
    return s


def running(b, i):
    """VC: the run in the chat: the orchestrator's plan, then the lanes working side by side."""
    s = screen(b, SCREENS[2], i)
    top(b, s, "Новая главная портфолио", FILE)
    m = body(b, s, gap=12)
    inst(b, m, "message", {"State": "Sent", "Text": TASK + " · ×3"}, sizingH="fill")
    plan_block(b, m)
    for (n, agent, model, style, idea, _), (st, took) in zip(LANES, [(("build", "Hero · журнальная обложка", "4.1s"), "2:14"),
                                                              (("build", "Кейсы · таблица", "2.7s"), "1:58"),
                                                              (("screenshot", "3. Swiss Grid", "0.9s"), "2:31")]):
        lane_card(b, m, n, agent, model, style, idea, "run", st, took)
    w = b.row(s, "Working", gap=8, padding=[0, 16, 8, 16], sizingH="fill", crossAlign="center")
    b.ellipse(w, "Spin", 8, ACCENT)
    text(b, w, "Работают 3 дорожки · 2:31", 12, DIM, name="Status", sizingH="fill")
    button(b, w, "Остановить все")
    composer_x(b, s, "Уточнить. @слои. /навыки.", "Running", n=3)
    return s


def finished(b, i):
    """VD: lanes done, each with its own Показать / Отменить; the orchestrator compares and picks one."""
    s = screen(b, SCREENS[3], i)
    top(b, s, "Новая главная портфолио", FILE)
    m = body(b, s, gap=12)
    for n, agent, model, style, idea, _ in LANES:
        lane_card(b, m, n, agent, model, style, idea, "done", took={1: "4 мин 10 с", 2: "3 мин 42 с", 3: ""}[n],
                  undone=n == 3)
    c = b.col(m, "Сравнение", gap=8, sizingH="fill")
    h = b.row(c, "Who", gap=6, crossAlign="center")
    mark(b, h, "claude")
    text(b, h, "Оркестратор · сравнение", 12, DIM, True)
    t = b.col(c, "Table", gap=0, fill=CARD, cornerRadius=8, stroke=LINE, strokeWeight=1, sizingH="fill")
    for k, (a, bb, cc) in enumerate([("", "Сильная сторона", "Компромисс"),
                                    ("1 Журнал", "характер, кейсы читаются", "длинная страница"),
                                    ("2 Инструмент", "плотно, быстро найти", "холодно для портфолио")]):
        r = b.row(t, f"Row {k}", gap=8, padding=[6, 10, 6, 10], sizingH="fill")
        for v, wdt in ((a, 84), (bb, 120), (cc, 120)):
            text(b, r, v, 11, FAINT if k == 0 else TEXT, k == 0, w=wdt, textAutoResize="height")
        if k < 2:
            b.rect(t, "Line", 10, 1, LINE, sizingH="fill")
    text(b, c, "Беру 1: у портфолио главное — кейсы, журнал даёт им голос. Из 2 стоит взять таблицу кейсов.",
         13, TEXT, name="Pick", sizingH="fill", textAutoResize="height")
    composer_x(b, s, "Уточнить. @слои. /навыки.", n=1)
    return s


def canvas(b):
    """VE: what the designer sees in FigCraft: three frames in a row and a named cursor in each."""
    w = b.col(None, CANVAS, gap=16, w=1360, h=740, fill="#1E1E1E", cornerRadius=12, padding=24, stroke=LINE,
              strokeWeight=1, strokeAlign="inside", clip=True, x=X0 + 4 * 460, y=Y)
    text(b, w, "FigCraft · person-site · справа от «01 Главная»", 12, FAINT, name="Where")
    r = b.row(w, "Frames", gap=40, sizingH="fill")
    for n, agent, model, style, idea, colors in LANES:
        col = b.col(r, f"{n}. {idea}", gap=8)
        text(b, col, f"{n}. {idea}", 12, DIM, name="Frame name")
        f = b.col(col, "Frame", gap=14, w=400, h=600, sizingH="fixed", sizingV="fixed", fill=colors[0], padding=28,
                  stroke=BORDER, strokeWeight=1)
        b.rect(f, "Nav", 344, 10, colors[1], cornerRadius=2, opacity=0.25)
        b.rect(f, "Headline", 300 if n != 2 else 220, 40, colors[1], cornerRadius=2)
        b.rect(f, "Headline 2", 220 if n != 2 else 160, 40, colors[1], cornerRadius=2, opacity=0.85)
        b.rect(f, "Accent", 90, 24, colors[2], cornerRadius=4 if n != 3 else 0)
        g = b.row(f, "Cases", gap=10)
        for k in range(3 if n != 1 else 2):
            b.rect(g, f"Case {k + 1}", 100 if n != 1 else 160, 120, colors[1], cornerRadius=4 if n == 2 else 0,
                   opacity=0.12)
        cur = b.row(col, "Cursor", gap=4, crossAlign="center")
        glyph(b, cur, "\U000f0415", ORANGE if agent == "claude" else CODEX, 12, name="Pointer")
        tag = b.row(cur, "Name", gap=0, padding=[2, 6, 2, 6], cornerRadius=4, fill=ORANGE if agent == "claude" else CODEX)
        text(b, tag, f"Вариант {n} · {'Claude' if agent == 'claude' else 'Codex'}", 11, BG, True)
    return w


def notes(b):
    n = b.col(None, NOTES, gap=16, w=620, fill=CARD, cornerRadius=12, padding=24, stroke=LINE, strokeWeight=1,
              strokeAlign="inside", x=X0 + 4 * 460 + 1400, y=Y)
    text(b, n, "Как работают варианты", 18, TEXT, True, name="Title")
    for title, s in (
            ("Когда", "×N в строке модели — на одно сообщение. Без него агент делает один вариант в одном хорошем "
                      "стиле, а на «дай несколько вариантов» сам запускает варианты с дорожками из этого меню."),
            ("Оркестратор", "Свой агент и модель. Решает опорный экран и размер, ищет в библиотеке стилей N разных "
                            "направлений (разные источники и структура, не перекраска), ставит N рамок в ряд и "
                            "раздаёт задания. Сам не рисует; когда дорожки закончат — сравнивает и советует."),
            ("Дорожки", "Каждая — отдельный CLI (Claude, Codex, pi) со своей моделью и своим участником в live-сессии "
                        "файла: свой курсор «Вариант k · агент», своя история — отмена одной не трогает другие. "
                        "Рисует только в своей рамке, токены кладёт в свою коллекцию «V k · стиль»."),
            ("Библиотека стилей", "Всё, что объявлено как style или system в SKILL.md, из любого источника: темы "
                                  "Hallmark, tweakcn, uipro, typeui, дизайн-системы проекта, позже — библиотеки "
                                  "компонентов. Новые появляются сами. Стиль, закреплённый за дорожкой, сильнее "
                                  "выбора оркестратора.")):
        sct = b.col(n, title, gap=6, sizingH="fill")
        text(b, sct, title.upper(), 10, FAINT, True, name="Head", letterSpacing=1)
        text(b, sct, s, 12, DIM, name="Text", sizingH="fill", textAutoResize="height")
    code(b, n, "variants({frame: {width, height}, directions: [{title, idea, style?, brief}]})", DIM)
    return n


BUILD = [setup, style_pick, running, finished]


def main():
    fc = FC()
    docs = fc.cmd("doc.list")
    back = next((i for i, d in enumerate(docs) if d.get("active")), None)
    idx = next(i for i, d in enumerate(docs) if (d.get("path") or "").endswith("design/review-ux.figcraft"))
    fc.cmd("doc.switch", index=idx)
    try:
        page = next(p for p in fc.cmd("page.list") if p["name"] == "Агент")
        fc.cmd("page.select", id=page["id"])
        names = {"Strict · " + n for n in SCREENS} | {CANVAS, NOTES}
        old = [t["id"] for t in fc.tops() if t.get("name") in names
               or (t.get("name") in ("Подпись", "Сценарий") and Y - 200 <= t.get("y", 0) < Y)]
        if old:
            fc.cmd("edit.delete", ids=old)
        b = B()
        text(b, None, "Варианты: оркестратор и параллельные дорожки", 18, TEXT, True, name="Сценарий", x=X0, y=Y - 110)
        text(b, None, "Как в pen.dev: на каждый вариант — свой ход, своя идея и свой стиль из библиотеки; здесь "
                      "дорожки идут параллельно, каждая своим агентом и моделью.", 13, DIM, name="Подпись",
             x=X0, y=Y - 80, w=1600, textAutoResize="height")
        frames = [fn(b, i) for i, fn in enumerate(BUILD)] + [canvas(b), notes(b)]
        for i, title in enumerate(SCREENS):
            text(b, None, title, 14, TEXT, True, name="Подпись", x=X0 + i * 460, y=Y - 30)
        res = run(fc, b, "Variants screens VA–VE")
        ids = [res[f["$step"]]["id"] for f in frames]
        fc.cmd("variable.setMode", ids=ids, collection="Tokens", mode="Graphite")
        print(ids)
    finally:
        if back is not None and back != idx:
            fc.cmd("doc.switch", index=back)


if __name__ == "__main__":
    main()
