#!/usr/bin/env python3
"""Adds screens H–K to the «Агент» page of design/review-ux.figcraft, right of what is there.

Unlike agent.py it redraws only its own frames (and their captions), so screens drawn by hand or by an agent
in the chat stay. Run with review-ux.figcraft as the current document.
"""
from agent import *  # noqa: F403  (build.py's atoms, the panel's top bar, chips and composer)
from build import row_open, row_question, row_review  # noqa: E402

X0, Y = 3680, 180  # right of G · Просмотр картинки
SCREENS = ("H · Замечания", "I · Меню @", "J · Итог ответа", "K · Несколько файлов")
XS = [X0 + i * 460 for i in range(len(SCREENS))]


def tabs(b, p, active, badge=2):
    t = b.row(p, "Tabs", gap=2, sizingH="fill", padding=[0, 10, 0, 10])
    for name, icon in (("Чат", "logs"), ("Замечания", "problems")):
        on = name == active
        tab = b.col(t, name, gap=0)
        r = b.row(tab, "Label", gap=6, padding=[8, 10, 7, 10])
        b.text(r, G[icon], 14, TEXT if on else FAINT, name="Icon")
        b.text(r, name, 12, TEXT if on else FAINT, name="Text")
        if name == "Замечания" and badge:
            bd = b.row(r, "Badge", gap=0, fill=CYAN, cornerRadius=8, padding=[0, 6, 0, 6])
            b.text(bd, str(badge), 10, BG, bold=True, name="Count")
        b.rect(tab, "Underline", 1, 2, ACCENT if on else "none", sizingH="fill")
    b.rect(p, "Divider", PANEL_W, 1, LINE)


def section(b, parent, title, action=None):
    g = b.col(parent, title, gap=8, sizingH="fill")
    h = b.row(g, "Head", gap=8, sizingH="fill", sizingV="hug")
    b.text(h, title.upper(), 10, FAINT, bold=True, name="Title", letterSpacing=1)
    if action:
        spacer(b, h)
        button(b, h, action, "sparkles", "primary")
    return g


def scene_remarks(b, x, y):
    p = panel(b, SCREENS[0], x, y)
    topbar(b, p, "Шапка: компоновка действий")
    tabs(b, p, "Замечания")
    body = b.col(p, "Body", gap=16, sizingH="fill", sizingV="fill", padding=[14, 14, 14, 14])
    add = b.row(body, "Новое замечание", gap=8, sizingH="fill", fill=CARD, cornerRadius=8, padding=[8, 10, 8, 10],
                stroke=BORDER, strokeWeight=1)
    b.text(add, "Замечание к «Actions» — Enter", 12, FAINT, name="Placeholder")
    g = section(b, body, "Ждут тебя · 2")
    card = b.col(g, "Cards", gap=8, sizingH="fill")
    q = b.col(card, "Вопрос", gap=0, sizingH="fill", cornerRadius=10, stroke=ACCENT, strokeWeight=1, clip=True)
    row_question(b, q, 3, "Иконка щита мельче остальных", "Shield · Настройки", "Какой кегль?", ["16, как у пунктов", "18"])
    rv = b.col(card, "Проверка", gap=0, sizingH="fill", cornerRadius=10, stroke=LINE, strokeWeight=1, clip=True)
    row_review(b, rv, 4, "Заголовок крупнее", "Title · Обзор", "22 → 28, стиль Heading")
    g = section(b, body, "У агента · 1", "Отдать агенту · 1")
    lst = b.col(g, "List", gap=0, sizingH="fill", fill=CARD, cornerRadius=10, clip=True)
    row_open(b, lst, 5, "Кнопка налезает на край", "◇ Button · Footer")
    acc = b.row(body, "Принято", gap=6, sizingH="fill")
    b.text(acc, "ПРИНЯТО · 3", 10, FAINT, bold=True, name="Title", letterSpacing=1)
    b.text(acc, G["down"], 14, FAINT, name="Chevron")


def scene_mention(b, x, y):
    p = panel(b, SCREENS[1], x, y)
    topbar(b, p, "Шапка: компоновка действий")
    tabs(b, p, "Чат")
    spacer(b, p)
    menu = b.col(p, "Меню @", gap=2, sizingH="fill", padding=[0, 10, 6, 10])
    box = b.col(menu, "Box", gap=2, sizingH="fill", fill=CARD, cornerRadius=10, padding=8, stroke=BORDER, strokeWeight=1,
                effects=SHADOW)
    b.text(box, "@BU — СЛОИ СТРАНИЦЫ И ЗАМЕЧАНИЯ", 10, FAINT, bold=True, name="Head", letterSpacing=1)
    for icon, color, text, where, on in (("problems", YELLOW, "#7 Кнопка налезает на край", "замечание", True),
                                          ("seen", DIM, "Button", "Окно › Footer", False),
                                          ("seen", DIM, "Button label", "Footer › Button", False),
                                          ("seen", DIM, "Buttons", "Обзор › Header", False)):
        r = b.row(box, text, gap=8, sizingH="fill", cornerRadius=6, padding=[6, 8, 6, 8], fill=SEL if on else "none")
        b.text(r, G[icon], 14, color, name="Icon")
        b.text(r, text, 12, TEXT, name="Name")
        b.text(r, where, 10, FAINT, name="Where")
    foot = b.row(box, "Keys", gap=6, padding=[6, 8, 2, 8])
    for k, s in (("↑↓", "выбор"), ("Enter", "вставить"), ("Esc", "закрыть")):
        key(b, foot, k)
        b.text(foot, s, 10, FAINT, name="Hint")
    composer(b, p, typed="Поправь отступ у @Bu")


def scene_result(b, x, y):
    p = panel(b, SCREENS[2], x, y)
    topbar(b, p, "Замечания: шапка")
    tabs(b, p, "Чат", badge=1)
    body = b.col(p, "Messages", gap=14, sizingH="fill", sizingV="fill", padding=[16, 14, 16, 14])
    me = b.col(body, "Вы", gap=8, sizingH="fill", fill=CARD, cornerRadius=10, padding=12)
    r = b.row(me, "Context", gap=6)
    chip(b, r, "problems", "Замечания", RED, close=False)
    b.text(me, "Поправь макет по открытым замечаниям", 12, TEXT, w="fill", name="Text")
    ag = b.col(body, "Агент", gap=10, sizingH="fill")
    who = b.row(ag, "Who", gap=8)
    mark(b, who, CLAUDE, "C")
    b.text(who, "Claude · Opus 5.5 · $0.04", 11, DIM, bold=True, name="Name")
    steps = b.row(ag, "Шаги", gap=6, sizingH="fill", fill=SECTION, cornerRadius=8, padding=[8, 10, 8, 10])
    b.text(steps, "5 шагов · 5 ok", 11, FAINT, name="Summary")
    b.text(ag, "Заголовок теперь стиля Heading, отступ кнопки 16 из Tokens.", 12, TEXT, w="fill", name="Text")
    b.text(ag, "✓ #4 Заголовок 28, стиль Heading", 12, DIM, w="fill", name="Mark line")
    for icon, color, text, acts in (("edit", GREEN, "Изменено: 3 шага · 2 слоя", ("Показать", "Отменить")),
                                    ("problems", CYAN, "Отметил: #4 → Проверь", ("Замечания",))):
        bar = b.row(ag, text, gap=6, sizingH="fill", fill=SECTION, cornerRadius=8, padding=[4, 4, 4, 10])
        b.text(bar, G[icon], 14, color, name="Icon")
        b.text(bar, text, 11, DIM, name="Text")
        spacer(b, bar)
        for a in acts:
            button(b, bar, a, kind="ghost", color=DIM)
    deny = b.col(ag, "Нет доступа", gap=8, sizingH="fill", fill=YELLOW + "14", cornerRadius=8, padding=[8, 10, 10, 10],
                 stroke=YELLOW + "55", strokeWeight=1)
    t = b.row(deny, "Text", gap=6, sizingH="fill")
    b.text(t, "Агенту не хватило доступа:", 12, YELLOW, bold=True, name="Lead")
    b.text(t, "Bash · npm run tokens", 11, TEXT, name="Tool")
    button(b, deny, "Разрешить Bash в этом чате и продолжить", kind="primary")
    composer(b, p)


def scene_files(b, x, y):
    p = panel(b, SCREENS[3], x, y)
    topbar(b, p, "Шапка: компоновка действий", open_=True)
    m = b.col(p, "Меню чатов", gap=2, sizingH="fill", padding=[0, 10, 0, 10])
    box = b.col(m, "Box", gap=2, sizingH="fill", fill=CARD, cornerRadius=10, padding=8, stroke=BORDER, strokeWeight=1,
                effects=SHADOW)
    b.text(box, "DESIGN.FIGCRAFT · ЭТОТ ФАЙЛ", 10, FAINT, bold=True, name="File", letterSpacing=1)
    for title, meta, run_ in (("Шапка: компоновка действий", "Claude · работает", True), ("Токены Tokyo Night", "Claude · вчера", False)):
        r = b.row(box, title, gap=8, sizingH="fill", cornerRadius=6, padding=[7, 8, 7, 8], fill=SEL if run_ else "none")
        col = b.col(r, "Text", gap=1, sizingH="fill")
        b.text(col, title, 12, TEXT, name="Title")
        b.text(col, meta, 10, ACCENT if run_ else FAINT, name="Meta")
        if run_:
            b.text(r, G["refresh"], 14, ACCENT, name="Running")
    spacer(b, p)
    info = b.row(p, "Другие файлы", gap=8, sizingH="fill", padding=[0, 10, 8, 10])
    ban = b.row(info, "Banner", gap=8, sizingH="fill", fill=ACCENT + "1A", cornerRadius=8, padding=[8, 10, 8, 10])
    b.text(ban, G["sparkles"], 14, ACCENT, name="Icon")
    b.text(ban, "Агенты работают ещё в 2 файлах. Когда закончат, придёт уведомление.", 11, ACCENT, w="fill", name="Text")
    note = b.row(p, "Уведомление", gap=0, sizingH="fill", padding=[0, 10, 8, 10])
    toast(b, note, "check", "tabka-ui: готово · 4 шага правок", color=GREEN, sizingH="fill")
    composer(b, p, typed="Сделай ещё вариант с иконками")


def main():
    fc = FC()
    active = next(d for d in fc.cmd("doc.list") if d["active"])
    assert (active.get("path") or "").endswith("review-ux.figcraft"), f"open review-ux.figcraft first, not {active['name']}"
    page = next(p for p in fc.cmd("page.list") if p["name"] == "Агент")
    fc.cmd("page.select", id=page["id"])
    mine = [t["id"] for t in fc.tops() if t.get("name") in SCREENS or t.get("name") == "test-undo"
            or (t.get("name") == "Подпись" and round(t.get("x", 0)) in XS)]
    if mine:
        fc.cmd("edit.delete", ids=mine)
    b = B()
    for x, title, fn in zip(XS, ("H · Замечания: ждут тебя, у агента, принято", "I · @: слои страницы и замечания",
                                 "J · Итог ответа: правки, отметки, доступ", "K · Несколько файлов сразу"),
                            (scene_remarks, scene_mention, scene_result, scene_files)):
        b.text(None, title, 14, CAP, bold=True, name="Подпись", x=x, y=Y - 30)
        fn(b, x, Y)
    run(fc, b, "Agent panel: screens H–K")


if __name__ == "__main__":
    main()
