#!/usr/bin/env python3
"""Draws the agent panel concept on the «Агент» page of design/review-ux.figcraft.

Same builder and atoms as build.py; run with review-ux.figcraft as the current document.
"""
import os
import sys

from build import *  # noqa: F403  (lib's tokens and helpers, plus pin/key/button/toast/caption_at)

PANEL_W, PANEL_H = 400, 860
CLAUDE, CODEX, PI = "#D97757", "#10A37F", MAUVE  # brand-ish marks on the canvas only
LETTER = {"Claude Code": "C", "Codex": "X", "pi": "π", "Cursor": "▲"}


def panel(b, name, x, y):
    return b.col(None, name, gap=0, w=PANEL_W, h=PANEL_H, fill=BG, cornerRadius=12, stroke=BORDER, strokeWeight=1,
                 strokeAlign="inside", clip=True, effects=SHADOW, x=x, y=y)


def topbar(b, p, title="Новый чат", open_=False):
    t = b.row(p, "Top bar", gap=8, sizingH="fill", padding=[10, 10, 10, 12])
    s = b.row(t, "Чаты файла", gap=8, sizingH="fill", fill=SURFACE if open_ else CARD, cornerRadius=8, padding=[7, 10, 7, 10],
              stroke=ACCENT if open_ else LINE, strokeWeight=1)
    b.text(s, G["file"], 14, FAINT, name="Icon")
    col = b.col(s, "Titles", gap=1, sizingH="fill")
    b.text(col, title, 12, TEXT, bold=True, name="Chat")
    b.text(col, "design.figcraft", 10, FAINT, name="File")
    b.text(s, G["up" if open_ else "down"], 14, FAINT, name="Chevron")
    button(b, t, "Новый", "add", "line")
    icon_button(b, t, "settings", "Настройки")
    b.rect(p, "Divider", PANEL_W, 1, LINE)


def chip(b, parent, icon, text, color=DIM, live=False, close=True):
    c = b.row(parent, text, gap=6, fill="none" if live else SURFACE, cornerRadius=6, padding=[3, 8, 3, 6],
              **({"stroke": ACCENT, "strokeWeight": 1, "dashes": [3, 3]} if live else {}))
    b.text(c, G[icon], 14, ACCENT if live else color, name="Icon")
    b.text(c, text, 11, ACCENT if live else TEXT, name="Text")
    if live:
        b.text(c, G["add"], 14, ACCENT, name="Add")
    elif close:
        b.text(c, G["close"], 14, FAINT, name="Remove")
    return c


def mark(b, parent, color, letter, d=18):
    m = b.frame(parent, "Mark", "horizontal", w=d, h=d, fill=color, cornerRadius=5, mainAlign="center", crossAlign="center")
    b.text(m, letter, 10, BG, bold=True, name="Letter")
    return m


def picker(b, parent, agent="Claude Code", model="Opus 5.5", color=CLAUDE, open_=False):
    p = b.row(parent, "Агент и модель", gap=6, cornerRadius=6, padding=[4, 8, 4, 6], fill=SURFACE if open_ else "none")
    mark(b, p, color, LETTER[agent], 16)
    b.text(p, agent, 11, DIM, name="Agent")
    b.text(p, model, 11, TEXT, bold=True, name="Model")
    b.text(p, G["down"], 14, FAINT, name="Chevron")


def composer(b, p, chips=(), live=None, placeholder="Опиши, что поменять в макете…", typed=None, busy=False, open_=False):
    w = b.col(p, "Composer", gap=6, sizingH="fill", padding=[0, 10, 10, 10])
    c = b.col(w, "Box", gap=8, sizingH="fill", fill=CARD, cornerRadius=12, padding=10, stroke=ACCENT if typed else BORDER,
              strokeWeight=1)
    if chips or live:
        r = b.row(c, "Context", gap=6, sizingH="fill")
        for icon, text in chips:
            chip(b, r, icon, text)
        if live:
            chip(b, r, "seen", live, live=True)
    b.text(c, typed or placeholder, 13, TEXT if typed else FAINT, w="fill", name="Input")
    bar = b.row(c, "Bar", gap=6, sizingH="fill")
    button(b, bar, icon="add", kind="ghost", color=DIM, name="Attach")
    spacer(b, bar)
    picker(b, bar, open_=open_)
    send = b.frame(bar, "Send", "horizontal", w=28, h=28, fill=RED if busy else ACCENT if typed else SURFACE, cornerRadius=14,
                   mainAlign="center", crossAlign="center")
    b.text(send, G["close" if busy else "up"], 14, BG if busy or typed else FAINT, name="Icon")
    hint = "Esc — остановить" if busy else "Enter — отправить · @ — слой или замечание"
    b.text(w, hint, 10, FAINT, name="Hint")


def scene_empty(b, x, y):
    p = panel(b, "A · Пустой чат", x, y)
    topbar(b, p)
    body = b.col(p, "Body", gap=14, sizingH="fill", sizingV="fill", padding=[24, 16, 16, 16], mainAlign="max")
    b.text(body, "Что поправить в макете?", 18, TEXT, bold=True, name="Title")
    b.text(body, "Агент видит этот файл, выделение и замечания. Ответы и правки остаются в чате этого файла.",
           12, DIM, w="fill", name="Lead")
    for icon, s in (("problems", "Разбери открытые замечания · 3"), ("edit", "Собери экран по выделенному фрейму"),
                    ("sets", "Проверь цвета и тексты по токенам"), ("terminal", "Опиши компонент для кода")):
        r = b.row(body, s, gap=10, sizingH="fill", fill=CARD, cornerRadius=8, padding=[9, 12, 9, 12], stroke=LINE, strokeWeight=1)
        b.text(r, G[icon], 14, ACCENT, name="Icon")
        b.text(r, s, 12, TEXT, name="Text")
    ctx = b.col(body, "Контекст файла", gap=8, sizingH="fill", paddingTop=8)
    b.text(ctx, "КОНТЕКСТ ФАЙЛА", 10, FAINT, bold=True, name="Title", letterSpacing=1)
    r = b.row(ctx, "Chips", gap=6)
    chip(b, r, "file", "DESIGN.md", close=False)
    chip(b, r, "problems", "3 замечания", RED, close=False)
    chip(b, r, "sets", "Tokens · 28", close=False)
    composer(b, p, live="«WorkspaceHeader» frame")


def step(b, parent, icon, text, color=GREEN, faint=False):
    r = b.row(parent, text, gap=8, sizingH="fill")
    b.text(r, G[icon], 14, color, name="Icon")
    b.text(r, text, 11, FAINT if faint else DIM, name="Text")


def scene_chat(b, x, y):
    p = panel(b, "B · Разговор", x, y)
    topbar(b, p, "Шапка: компоновка действий")
    body = b.col(p, "Messages", gap=14, sizingH="fill", sizingV="fill", padding=[16, 14, 16, 14])
    me = b.col(body, "Вы", gap=8, sizingH="fill", fill=CARD, cornerRadius=10, padding=12)
    r = b.row(me, "Context", gap=6)
    chip(b, r, "path", "◇ Header › Actions · 151×32", close=False)
    chip(b, r, "problems", "#3", RED, close=False)
    b.text(me, "Собери действия справа: вид, ⋯ и «+ Коллекция» с подписью. Как в карточках, без своих цветов.",
           12, TEXT, w="fill", name="Text")
    ag = b.col(body, "Агент", gap=10, sizingH="fill")
    who = b.row(ag, "Who", gap=8)
    mark(b, who, CLAUDE, "C")
    b.text(who, "Claude Code · Opus 5.5", 11, DIM, bold=True, name="Name")
    steps = b.col(ag, "Шаги", gap=6, sizingH="fill", fill=SECTION, cornerRadius=8, padding=10)
    step(b, steps, "check", "Прочитал «Header» и компоненты Button, Seg")
    step(b, steps, "check", "Собрал Actions: Seg · IconButton · Button/Primary")
    step(b, steps, "check", "Привязал цвета к Tokens, текст — к Body/Bold")
    step(b, steps, "refresh", "Делаю скриншот для проверки…", ACCENT, faint=True)
    b.text(ag, "Справа теперь три элемента: переключатель вида сегментом, ⋯ и основная кнопка «+ Коллекция». "
               "Отступы 8, как в соседних карточках.", 12, TEXT, w="fill", name="Text")
    res = b.row(ag, "Итог", gap=8, sizingH="fill", fill=HIGHLIGHT, cornerRadius=8, padding=[8, 10, 8, 10], stroke=LINE,
                strokeWeight=1)
    b.text(res, G["edit"], 14, CYAN, name="Icon")
    b.text(res, "Изменено 6 слоёв", 12, TEXT, bold=True, name="Text")
    spacer(b, res)
    b.text(res, "Показать", 12, ACCENT, bold=True, name="Show")
    b.text(res, "Отменить", 12, DIM, name="Undo")
    composer(b, p, live="«Sidebar» frame", busy=True, placeholder="Можно дописать, пока агент работает…")


def scene_picker(b, x, y):
    p = panel(b, "C · Выбор агента", x, y)
    topbar(b, p, "Шапка: компоновка действий")
    spacer(b, p)
    menu = b.col(p, "Меню агентов", gap=2, sizingH="fill", padding=[0, 10, 6, 10])
    box = b.col(menu, "Box", gap=2, sizingH="fill", fill=CARD, cornerRadius=10, padding=8, stroke=BORDER, strokeWeight=1,
                effects=SHADOW)
    s = b.row(box, "Search", gap=8, sizingH="fill", fill=BG, cornerRadius=6, padding=[6, 8, 6, 8])
    b.text(s, G["search"], 14, FAINT, name="Icon")
    b.text(s, "Найти модель…", 12, FAINT, name="Placeholder")
    for agent, color, status, models, picked in (
            ("Claude Code", CLAUDE, "подписка", ["Fable 5.1", "Opus 5.5", "Sonnet 5.5", "Haiku 5.5"], "Opus 5.5"),
            ("Codex", CODEX, "подписка", ["GPT-6.1 Sol", "GPT-6 Astra", "GPT-6 Luna"], None),
            ("pi", PI, "свои провайдеры", ["DeepSeek V4 Pro", "Qwen 3.8 Max"], None)):
        h = b.row(box, agent, gap=8, sizingH="fill", padding=[8, 6, 4, 6])
        mark(b, h, color, LETTER[agent], 16)
        b.text(h, agent.upper(), 10, FAINT, bold=True, name="Agent", letterSpacing=1)
        spacer(b, h)
        b.ellipse(h, "Dot", 6, GREEN)
        b.text(h, status, 10, FAINT, name="Status")
        for m in models:
            r = b.row(box, m, gap=8, sizingH="fill", cornerRadius=6, padding=[6, 8, 6, 30], fill=SEL if m == picked else "none")
            b.text(r, m, 12, TEXT, name="Model")
            spacer(b, r)
            if m == picked:
                b.text(r, G["check"], 14, ACCENT, name="Check")
    b.rect(box, "Divider", PANEL_W - 36, 1, LINE)
    f = b.row(box, "Подключить", gap=8, sizingH="fill", padding=[6, 8, 4, 8])
    b.text(f, G["settings"], 14, DIM, name="Icon")
    b.text(f, "Агенты и доступ…", 12, DIM, name="Text")
    composer(b, p, typed="Собери действия справа…", open_=True)


def icon_button(b, parent, icon, name, color=DIM):
    f = b.frame(parent, name, "horizontal", w=40, h=40, cornerRadius=8, stroke=BORDER, strokeWeight=1, mainAlign="center",
                crossAlign="center")
    b.text(f, G[icon], 14, color, name="Icon")
    return f


def radio(b, parent, title, note, on):
    r = b.row(parent, title, gap=10, sizingH="fill", cornerRadius=8, padding=[9, 12, 9, 12], crossAlign="min",
              stroke=ACCENT if on else LINE, strokeWeight=1, fill=HIGHLIGHT if on else "none")
    dot = b.frame(r, "Radio", "horizontal", w=16, h=16, cornerRadius=8, stroke=ACCENT if on else BORDER, strokeWeight=1.5,
                  mainAlign="center", crossAlign="center")
    if on:
        b.ellipse(dot, "Dot", 8, ACCENT)
    col = b.col(r, "Text", gap=2, sizingH="fill")
    b.text(col, title, 12, TEXT, bold=True, name="Title")
    b.text(col, note, 11, FAINT, w="fill", name="Note")


def group(b, parent, title):
    g = b.col(parent, title, gap=8, sizingH="fill")
    b.text(g, title.upper(), 10, FAINT, bold=True, name="Title", letterSpacing=1)
    return g


def scene_settings(b, x, y):
    """A screen of its own: the chat and the input give way to it, ← goes back."""
    p = panel(b, "D · Настройки", x, y)
    t = b.row(p, "Top bar", gap=10, sizingH="fill", padding=[10, 10, 10, 10])
    icon_button(b, t, "back", "Назад")
    col = b.col(t, "Titles", gap=1, sizingH="fill")
    b.text(col, "Настройки", 13, TEXT, bold=True, name="Title")
    b.text(col, "для всех файлов", 10, FAINT, name="Note")
    b.rect(p, "Divider", PANEL_W, 1, LINE)
    body = b.col(p, "Body", gap=22, sizingH="fill", padding=[16, 14, 16, 14])
    g = group(b, body, "Агенты")
    lst = b.col(g, "List", gap=0, sizingH="fill", fill=CARD, cornerRadius=10, stroke=LINE, strokeWeight=1, clip=True)
    for i, (agent, color, ver, path, models, ok) in enumerate((
            ("Claude Code", CLAUDE, "2.1.311", "~/.local/share/mise/…/claude", "4 модели", True),
            ("Codex", CODEX, "0.164.0", "~/.local/share/mise/…/codex", "8 моделей", True),
            ("pi", PI, "1.4.0", "~/.local/share/mise/…/pi", "406 моделей", True),
            ("Cursor", SURFACE, "", "не найден в PATH", "", False))):
        if i:
            b.rect(lst, "Divider", PANEL_W - 30, 1, LINE)
        r = b.row(lst, agent, gap=10, sizingH="fill", padding=[10, 12, 10, 12])
        mark(b, r, color, LETTER[agent], 28)
        info = b.col(r, "Info", gap=2, sizingH="fill")
        nm = b.row(info, "Name", gap=6)
        b.text(nm, agent, 12, TEXT if ok else DIM, bold=True, name="Name")
        if ver:
            b.text(nm, ver, 10, FAINT, name="Version")
        b.text(info, path, 10, FAINT, name="Path")
        if ok:
            b.text(r, models, 10, DIM, name="Models")
        else:
            button(b, r, "Как установить", kind="line")
    g = group(b, body, "Доступ агента")
    radio(b, g, "Только FigCraft", "Меняет макет и читает файлы проекта. Команды и правки файлов — нет.", True)
    radio(b, g, "Как в терминале", "Разрешения из настроек самого агента. Нужно для скриптов проекта.", False)
    g = group(b, body, "Чаты")
    r = b.row(g, "Storage", gap=10, sizingH="fill", fill=CARD, cornerRadius=10, padding=[10, 12, 10, 12], stroke=LINE,
              strokeWeight=1)
    col = b.col(r, "Text", gap=2, sizingH="fill")
    b.text(col, "У этого файла 3 чата", 12, TEXT, name="Count")
    b.text(col, "~/.local/state/figcraft-agent", 10, FAINT, name="Path")
    button(b, r, "Очистить", kind="line", color=RED)
    spacer(b, p)
    f = b.col(p, "Footer", sizingH="fill", padding=[0, 14, 14, 14])
    b.text(f, "Агенты работают через свои CLI и ваши подписки — ключи не нужны.", 10, FAINT, name="Footnote", w="fill")


def scene_sessions(b, x, y):
    p = panel(b, "E · Чаты файла", x, y)
    topbar(b, p, "Шапка: компоновка действий", open_=True)
    m = b.col(p, "Меню чатов", gap=2, sizingH="fill", padding=[0, 10, 0, 10])
    box = b.col(m, "Box", gap=2, sizingH="fill", fill=CARD, cornerRadius=10, padding=8, stroke=BORDER, strokeWeight=1,
                effects=SHADOW)
    for file, chats in (("design.figcraft · этот файл", [("Шапка: компоновка действий", "Claude · сейчас", True),
                                                         ("Компактное окно — отступы", "Codex · 2 ч", False),
                                                         ("Токены Tokyo Night", "Claude · вчера", False)]),
                        ("tabka-ui.figcraft", [("Полоска пространств", "Claude · вчера", False)])):
        b.text(box, file.upper(), 10, FAINT, bold=True, name="File", letterSpacing=1)
        for title, meta, cur in chats:
            r = b.row(box, title, gap=8, sizingH="fill", cornerRadius=6, padding=[7, 8, 7, 8], fill=SEL if cur else "none")
            col = b.col(r, "Text", gap=1, sizingH="fill")
            b.text(col, title, 12, TEXT, name="Title")
            b.text(col, meta, 10, FAINT, name="Meta")
    spacer(b, p)
    composer(b, p)


def scene_layout(b, x, y):
    """Step 1 (a window beside FigCraft) and step 2 (the panel inside it), as two desktops."""
    for i, (title, inside) in enumerate((("Шаг 1 · окно рядом (сайдкар)", False), ("Шаг 2 · панель внутри FigCraft (патч)", True))):
        dx = x + i * 720
        b.text(None, title, 14, CAP, bold=True, name="Подпись", x=dx, y=y)
        d = b.frame(None, title, None, w=680, h=380, fill=DESK, cornerRadius=10, clip=True, x=dx, y=y + 30)
        fw = 680 - 24 if inside else 440
        f = b.frame(d, "FigCraft", None, w=fw, h=356, x=12, y=12, fill=SECTION, cornerRadius=8, stroke=BORDER, strokeWeight=1)
        b.rect(f, "Toolbar", fw, 28, CARD)
        b.text(f, "FigCraft — design.figcraft", 10, FAINT, name="Title", x=12, y=8)
        left = 150 if inside else 0
        if inside:
            pnl = b.frame(f, "Agent panel", None, w=140, h=328, x=0, y=28, fill=BG, stroke=ACCENT, strokeWeight=1.5)
            b.rect(pnl, "Chat", 116, 40, CARD, x=12, y=14, cornerRadius=4)
            b.rect(pnl, "Chat", 90, 28, CARD, x=12, y=62, cornerRadius=4)
            b.rect(pnl, "Composer", 116, 40, CARD, x=12, y=276, cornerRadius=6, stroke=BORDER, strokeWeight=1)
        b.rect(f, "Layers", 90, 328, CARD, x=left, y=28)
        b.rect(f, "Canvas frame", 180 if inside else 160, 200, SURFACE, x=left + 130, y=80, cornerRadius=4)
        pin(b, f, 1, RED, x=left + 122, y=72)
        b.rect(f, "Inspector", 110, 328, CARD, x=fw - 110, y=28)
        if not inside:
            s = b.frame(d, "Сайдкар", None, w=208, h=356, x=460, y=12, fill=BG, cornerRadius=8, stroke=ACCENT, strokeWeight=1.5)
            b.text(s, "FigCraft Agent", 10, DIM, name="Title", x=12, y=10)
            b.rect(s, "Chat", 184, 60, CARD, x=12, y=36, cornerRadius=4)
            b.rect(s, "Chat", 140, 40, CARD, x=12, y=104, cornerRadius=4)
            b.rect(s, "Composer", 184, 52, CARD, x=12, y=292, cornerRadius=6, stroke=BORDER, strokeWeight=1)
        note = ("Отдельное окно в тайлинге Hyprland. Работает с любым FigCraft; выделение — опросом по MCP, номера — аннотации."
                if not inside else "Тот же движок агента, но панель слева в FigCraft: события выделения и метки на холсте.")
        b.text(None, note, 12, DIM, name="Пояснение", w=680, x=dx, y=y + 420, textAutoResize="height")


def main():
    fc = FC()
    active = next(d for d in fc.cmd("doc.list") if d["active"])
    assert (active.get("path") or "").endswith("review-ux.figcraft"), f"open review-ux.figcraft first, not {active['name']}"
    pages = fc.cmd("page.list")
    if pages[0]["name"] != "Ревью":
        fc.cmd("page.rename", id=pages[0]["id"], name="Ревью")
    page = next((p for p in pages if p["name"] == "Агент"), None)
    if page is None:
        fc.cmd("page.add", name="Агент")
        page = next(p for p in fc.cmd("page.list") if p["name"] == "Агент")
    fc.cmd("page.select", id=page["id"])
    b = B()
    b.text(None, "FigCraft Agent", 40, CAP, bold=True, name="Заголовок", x=0, y=0)
    b.text(None, "Чат с агентом у каждого файла, как в pen.dev: Claude Code, Codex или pi через их CLI и ваши подписки. "
                 "Агент видит выделение и замечания, правит макет через MCP и показывает, что изменил.",
           15, DIM, name="Принцип", w=1400, x=0, y=60, textAutoResize="height")
    for i, (fn, title) in enumerate(((scene_empty, "A · Пустой чат: подсказки и контекст файла"),
                                     (scene_chat, "B · Разговор: чипы слоёв, шаги, итог правки"),
                                     (scene_picker, "C · Агент и модель"))):
        b.text(None, title, 14, CAP, bold=True, name="Подпись", x=i * 460, y=150)
        fn(b, i * 460, 180)
    for i, (fn, title) in enumerate(((scene_sessions, "E · Чаты файла"), (scene_settings, "D · Настройки — отдельный экран"))):
        b.text(None, title, 14, CAP, bold=True, name="Подпись", x=1380 + i * 460, y=150)
        fn(b, 1380 + i * 460, 180)
    scene_layout(b, 0, 1120)
    # The page is redrawn whole; screens drawn beside these (F, G by hand, H–K by agent_more.py) would be lost.
    own = {c["params"].get("name") for c in b.cmds if c["command"] == "node.create" and "parent" not in c["params"]}
    tops = fc.tops()
    foreign = sorted({t.get("name") for t in tops} - own)
    if foreign and "--force" not in sys.argv:
        raise SystemExit("the «Агент» page has screens this script doesn't draw, it would delete them: "
                         + ", ".join(foreign) + ". Redraw single screens instead (see agent_more.py) or pass --force.")
    if tops:
        fc.cmd("edit.delete", ids=[t["id"] for t in tops])
    run(fc, b, "Agent panel concept")
    fc.cmd("file.save", path=os.path.join(os.path.dirname(os.path.abspath(__file__)), "review-ux.figcraft"))


if __name__ == "__main__":
    main()
