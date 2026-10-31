#!/usr/bin/env python3
"""Adds the screens VF–VI under the variants row of the «Агент» page of design/review-ux.figcraft: what comes after
the lanes.

A lane is kept: «Доработать» continues its own session in its frame, «Повторить» runs a failed one again (another
model if asked). «Беру этот» keeps one frame, removes the others with their «V k ·» tokens and makes the winner's
tokens the file's — one undo step. Then the winning lane carries its style to the other screens, or a new lane
mixes parts of several. ×N gains the axis (стиль · структура · адаптив), presets, a time limit per lane and «от
рамки»: lanes redo a selected frame instead of drawing in empty ones. Reruns redraw only these frames.
"""
from strict import (ACCENT, BG, CARD, DIM, FAINT, INSET, LINE, MAUVE, SURFACE, TEXT, B, FC, body,
                    button, card, code, divider, glyph, inst, keys, label, menu, run, spacer, text, top)
from variants import (FILE, LANES, agent_select, composer_x, lane_card, mark, segmented, style_chip, style_select)

X0, Y = 0, 18500
SCREENS = ["VF · Доработать вариант", "VG · Беру этот", "VH · Варианты: настройки", "VI · Перенести и смешать"]
NOTES = "Strict · После вариантов"
RED = "#FF6B7A"


def screen(b, name, i, h=860):
    return b.col(None, "Strict · " + name, gap=0, w=400, h=h, fill=BG, cornerRadius=12, stroke=LINE, strokeWeight=1,
                 strokeAlign="inside", clip=True, x=X0 + i * 460, y=Y)


def done_card(b, parent, n, took):
    """A lane done: its time, Показать / Отменить, and under them what to do with the variant itself."""
    _, agent, model, style, idea, _ = LANES[n - 1]
    c = lane_card(b, parent, n, agent, model, style, idea, "done", took=took)
    a = b.row(c, "Next", gap=6, sizingH="fill", crossAlign="center")
    button(b, a, "Доработать")
    button(b, a, "Беру этот")
    return c


def seg(b, parent, name, values, on, w=None):
    s = b.row(parent, name, gap=2, padding=2, fill=INSET, cornerRadius=6, stroke=LINE, strokeWeight=1)
    for v in values:
        c = b.row(s, v, gap=0, w=w or 52, h=24, sizingH="fixed", sizingV="fixed", mainAlign="center",
                  crossAlign="center", cornerRadius=4, fill=SURFACE if v == on else "none")
        text(b, c, v, 12, TEXT if v == on else DIM, v == on)
    return s


def target_bar(b, parent, n):
    """Above the input: the next message goes to lane n, its agent and its frame, not to the orchestrator."""
    _, agent, model, _, idea, _ = LANES[n - 1]
    r = b.row(parent, "Target", gap=6, h=28, sizingV="fixed", padding=[0, 8, 0, 8], cornerRadius=6, fill=SURFACE,
              stroke=ACCENT, strokeWeight=1, sizingH="fill", crossAlign="center")
    glyph(b, r, "\U000f0568", ACCENT, 13, name="Icon")
    text(b, r, f"В вариант {n} · {idea}", 12, TEXT, True, name="Lane", sizingH="fill", textAutoResize="truncate")
    mark(b, r, agent)
    text(b, r, model, 11, DIM, name="Model")
    text(b, r, "×", 13, FAINT, name="Close")
    return r


def run_bar(b, parent, cost, took, picked=None):
    """Under the lanes: the run's total — time, what it cost where the CLI says so — and what to do with it."""
    r = b.col(parent, "Запуск", gap=8, padding=[10, 12, 10, 12], fill=CARD, cornerRadius=8, stroke=LINE, strokeWeight=1,
              sizingH="fill")
    h = b.row(r, "Total", gap=6, sizingH="fill", crossAlign="center")
    glyph(b, h, "\U000f0568", ACCENT, 13, name="Icon")
    text(b, h, f"Варианты ×3 · {took}", 12, TEXT, True, name="Run")
    spacer(b, h)
    text(b, h, cost, 12, DIM, name="Cost")
    if picked:
        text(b, r, picked, 12, DIM, name="Picked", sizingH="fill", textAutoResize="height")
    return r


# ---- screens ----

def refine(b, i):
    """VF: a lane done is kept — «Доработать» sends the next message into it; a failed one runs again."""
    s = screen(b, SCREENS[0], i)
    top(b, s, "Новая главная портфолио", FILE)
    m = body(b, s, gap=12)
    done_card(b, m, 1, "4 мин 10 с")
    c = lane_card(b, m, 2, "codex", "GPT-6.1 Sol", LANES[1][3], LANES[1][4], "error")
    text(b, c, "Codex: лимит запросов исчерпан", 12, RED, name="Error", sizingH="fill", textAutoResize="height")
    a = b.row(c, "Retry", gap=6, sizingH="fill", crossAlign="center")
    text(b, a, "Ещё раз", 12, FAINT, name="Label")
    agent_select(b, a, "claude", "Sonnet 5.5")
    spacer(b, a)
    button(b, a, "Повторить", "Primary")
    done_card(b, m, 3, "3 мин 05 с")
    c = b.col(s, "Composer", gap=8, padding=[0, 12, 12, 12], sizingH="fill")
    target_bar(b, c, 1)
    inst(b, c, "input", {"State": "Filled", "Text": "Шапку плотнее, кейсы крупнее, без серого"}, sizingH="fill")
    r = b.row(c, "Model and variants", gap=6, sizingH="fill", crossAlign="center")
    inst(b, r, "model", {"Model": "Opus 5.5", "Effort": "", "Mode": "Только FigCraft", "Show hint": False},
         sizingH="fill")
    return s


def pick(b, i):
    """VG: after the comparison — the run's cost and time; «Беру 1» keeps one frame and its tokens, one undo."""
    s = screen(b, SCREENS[1], i)
    top(b, s, "Новая главная портфолио", FILE)
    m = body(b, s, gap=12)
    c = b.col(m, "Сравнение", gap=6, sizingH="fill")
    h = b.row(c, "Who", gap=6, crossAlign="center")
    mark(b, h, "claude")
    text(b, h, "Оркестратор · сравнение", 12, DIM, True)
    text(b, c, "Беру 1: у портфолио главное — кейсы, журнал даёт им голос. Из 2 стоит взять таблицу кейсов.",
         13, TEXT, name="Pick", sizingH="fill", textAutoResize="height")
    r = run_bar(b, m, "$1.84 · Codex без цены", "11 мин")
    a = b.row(r, "Actions", gap=6, sizingH="fill", crossAlign="center")
    button(b, a, "Беру 1", "Primary")
    button(b, a, "Смешать…")
    spacer(b, a)
    button(b, a, "Сравнить снова")
    divider(b, m)
    r = run_bar(b, m, "$1.84", "11 мин", "Взят вариант 1 «Журнал». Убраны рамки 2–3 и их коллекции «V2 ·», «V3 ·»; "
                                       "«V1 · Журнал» стала «Журнал», стили «V1/…» — без префикса.")
    a = b.row(r, "Actions", gap=6, sizingH="fill", crossAlign="center")
    button(b, a, "Перенести на экраны", "Primary")
    button(b, a, "Адаптив")
    spacer(b, a)
    button(b, a, "Отменить")
    composer_x(b, s, "Уточнить. @слои. /навыки.", n=1)
    return s


def setup(b, i):
    """VH: ×N's menu, full: the axis, presets, a time limit per lane and «от рамки» when a frame is selected."""
    s = screen(b, SCREENS[2], i)
    top(b, s, "Новый чат", FILE)
    body(b, s)
    composer_x(b, s, "Варианты этой главной", "Filled", n=3, open_=True)
    m = menu(b, s, "Variants menu", y=210)
    h = b.row(m, "Header", gap=8, padding=[8, 8, 6, 8], sizingH="fill", crossAlign="center")
    text(b, h, "Варианты", 12, DIM, True, name="Title")
    spacer(b, h)
    segmented(b, h, [1, 2, 3, 4, 6], 3)
    p = b.row(m, "Presets", gap=6, padding=[2, 8, 6, 8], sizingH="fill", crossAlign="center")
    for name, on in (("Claude + Codex", True), ("Все Opus", False)):
        inst(b, p, "chip", {"Kind": "Style", "Label": name}, opacity=1 if on else 0.6)
    spacer(b, p)
    text(b, p, "+ Сохранить", 11, ACCENT, name="Save")
    label(b, m, "Чем отличаются")
    ax = b.row(m, "Axis row", gap=0, padding=[0, 8, 0, 8], sizingH="fill")
    seg(b, ax, "Axis", ["Стиль", "Структура", "Адаптив"], "Стиль", w=114)
    t = b.row(m, "From frame", gap=8, padding=[8, 8, 4, 8], sizingH="fill", crossAlign="center")
    glyph(b, t, "\U000f0568", MAUVE, 13, name="Icon")
    text(b, t, "От рамки «01 Главная»: копии, а не пустые рамки", 12, TEXT, name="Base", sizingH="fill",
         textAutoResize="truncate")
    divider(b, m, 4)
    label(b, m, "Оркестратор")
    o = b.row(m, "Оркестратор", gap=8, padding=[4, 8, 6, 8], sizingH="fill", crossAlign="center")
    agent_select(b, o, "claude", "Opus 5.5")
    label(b, m, "Дорожки")
    for n, agent, model, style, _, colors in LANES:
        r = b.row(m, f"Дорожка {n}", gap=8, padding=[4, 8, 4, 8], sizingH="fill", crossAlign="center")
        text(b, r, str(n), 12, FAINT, True, name="Number", w=10)
        agent_select(b, r, agent, model)
        style_select(b, r, None)
    lim = b.row(m, "Limit", gap=8, padding=[6, 8, 4, 8], sizingH="fill", crossAlign="center")
    text(b, lim, "Не дольше", 12, DIM, name="Label", sizingH="fill")
    seg(b, lim, "Limit", ["∞", "10 мин", "20 мин"], "20 мин")
    keys(b, m, [("1–6", "сколько"), ("↵", "готово")])
    return s


def spread(b, i):
    """VI: the winner carries its style to the other screens in its own session; a mix is a new lane of its own."""
    s = screen(b, SCREENS[3], i)
    top(b, s, "Новая главная портфолио", FILE)
    m = body(b, s, gap=12)
    inst(b, m, "message", {"State": "Sent", "Text": "Смешай: шапка и кейсы из 1, таблица кейсов из 2"}, sizingH="fill")
    p = b.col(m, "Mix plan", gap=6, sizingH="fill")
    h = b.row(p, "Who", gap=6, crossAlign="center")
    mark(b, h, "claude")
    text(b, h, "Оркестратор · Opus 5.5", 12, DIM, True)
    r = b.row(p, "Runline", gap=6, crossAlign="center")
    glyph(b, r, "\U000f0568", ACCENT, 13, name="Icon")
    text(b, r, "Варианты ×1: рамка «4. Микс 1+2»", 12, DIM, name="Run")
    c = lane_card(b, m, 4, "claude", "Opus 5.5", "Hallmark · Almanac", "Микс: журнал + таблица кейсов", "run",
                  ("build", "Кейсы · таблица из #2", "3.2s"), "1:12")
    divider(b, m)
    c = card(b, m, "Перенос", padding=[10, 12, 10, 12], gap=8)
    h = b.row(c, "Header", gap=8, sizingH="fill", crossAlign="center")
    text(b, h, "1", 12, FAINT, True, name="Number")
    mark(b, h, "claude")
    text(b, h, "Перенести на экраны · Журнал", 13, TEXT, True, name="Idea", sizingH="fill", textAutoResize="truncate")
    b.ellipse(h, "Running", 8, ACCENT)
    mm = b.row(c, "Meta", gap=6, sizingH="fill", crossAlign="center")
    text(b, mm, "Opus 5.5 · своя сессия", 12, DIM, name="Model")
    style_chip(b, mm, "Hallmark · Almanac")
    inst(b, c, "step", {"Status": "Running", "Name": "build", "Args": "02 Кейс · по токенам «Журнал»", "Time": "5.0s"},
         sizingH="fill")
    w = b.row(s, "Working", gap=8, padding=[0, 16, 8, 16], sizingH="fill", crossAlign="center")
    b.ellipse(w, "Spin", 8, ACCENT)
    text(b, w, "Работают 2 дорожки · 1:12", 12, DIM, name="Status", sizingH="fill")
    button(b, w, "Остановить все")
    composer_x(b, s, "Уточнить. @слои. /навыки.", "Running", n=1)
    return s


def notes(b):
    n = b.col(None, NOTES, gap=16, w=620, fill=CARD, cornerRadius=12, padding=24, stroke=LINE, strokeWeight=1,
              strokeAlign="inside", x=X0 + 4 * 460, y=Y)
    text(b, n, "После вариантов", 18, TEXT, True, name="Title")
    for title, s in (
            ("Доработать", "Следующее сообщение идёт в дорожку: тот же агент, его сессия, его рамка и курсор. "
                           "Оркестратор сам направит туда «доработай второй» (инструмент lane)."),
            ("Повторить", "Упавшая или остановленная дорожка — ещё раз, можно другим агентом и моделью. Пока она "
                          "работает, сравнение ждёт; «Сравнить снова» — когда угодно."),
            ("Беру этот", "Одним шагом отмены: остальные рамки запуска удалены с их коллекциями «V k ·» и стилями "
                          "«V k/»; коллекция победителя теряет префикс и становится коллекцией файла."),
            ("Перенести и смешать", "Победитель в своей сессии переоформляет остальные экраны файла (или адаптив). "
                                    "Смешать — новая дорожка в новой рамке: бриф называет, что взять из каких рамок."),
            ("Оси и пресеты", "Стиль — разные стили из библиотеки, без повторов; структура — одна система, разные "
                              "раскладки; адаптив — один стиль, своя ширина у каждой рамки. Пресет — набор дорожек."),
            ("Деньги и время", "Цена — сумма по оркестратору и дорожкам, где CLI её сообщает (Codex — нет). Лимит "
                               "— время на дорожку: по нему её останавливают; деньгами ограничить нельзя, цена "
                               "приходит в конце."),
            ("Библиотеки компонентов", "group: library в SKILL.md — набор готовых компонентов. styles показывает их "
                                       "рядом с системами; дорожка с библиотекой собирает экран из её компонентов.")):
        sct = b.col(n, title, gap=6, sizingH="fill")
        text(b, sct, title.upper(), 10, FAINT, True, name="Head", letterSpacing=1)
        text(b, sct, s, 12, DIM, name="Text", sizingH="fill", textAutoResize="height")
    code(b, n, "variants({axis, base?, frame, directions: [{title, idea, style?, frame?, brief}]}) · lane({n, brief})",
         DIM)
    return n


BUILD = [refine, pick, setup, spread]


def main():
    fc = FC()
    docs = fc.cmd("doc.list")
    back = next((i for i, d in enumerate(docs) if d.get("active")), None)
    idx = next(i for i, d in enumerate(docs) if (d.get("path") or "").endswith("design/review-ux.figcraft"))
    fc.cmd("doc.switch", index=idx)
    try:
        page = next(p for p in fc.cmd("page.list") if p["name"] == "Агент")
        fc.cmd("page.select", id=page["id"])
        names = {"Strict · " + n for n in SCREENS} | {NOTES}
        old = [t["id"] for t in fc.tops() if t.get("name") in names
               or (t.get("name") in ("Подпись", "Сценарий") and Y - 200 <= t.get("y", 0) < Y)]
        if old:
            fc.cmd("edit.delete", ids=old)
        b = B()
        text(b, None, "После вариантов: доработать, взять, перенести", 18, TEXT, True, name="Сценарий", x=X0, y=Y - 110)
        text(b, None, "Запуск — не демо: дорожку можно продолжить или повторить, победителя взять с его токенами, "
                      "стиль перенести на остальные экраны или смешать варианты.", 13, DIM, name="Подпись",
             x=X0, y=Y - 80, w=1600, textAutoResize="height")
        frames = [fn(b, i) for i, fn in enumerate(BUILD)] + [notes(b)]
        for i, title in enumerate(SCREENS):
            text(b, None, title, 14, TEXT, True, name="Подпись", x=X0 + i * 460, y=Y - 30)
        res = run(fc, b, "Variants screens VF–VI")
        ids = [res[f["$step"]]["id"] for f in frames]
        fc.cmd("variable.setMode", ids=ids, collection="Tokens", mode="Graphite")
        print(ids)
    finally:
        if back is not None and back != idx:
            fc.cmd("doc.switch", index=back)


if __name__ == "__main__":
    main()
