#!/usr/bin/env python3
"""Where settings go once the gear leaves the header: a board below «Strict · Шапка — варианты».

Settings hold the agents, their access, the skills and the file's chats. Each column moves the way in next to one of
those: the chats menu under the title, the model menu, or the model row itself. Reruns redraw only the board.
"""
from strict import (BG, DIM, FAINT, LINE, MAUVE, TEXT, B, FC, body, composer, dim_chat, divider, glyph, inst, item,
                    kbd, keys, label, menu, run, text, top)
from strict_more import v

NAME = "Strict · Настройки — куда"
X, Y = 0, 9820
GEAR = ""


def screen(b, parent, name):
    return b.col(parent, name, gap=0, w=400, h=860, fill=BG, cornerRadius=12, stroke=LINE, strokeWeight=1,
                 strokeAlign="inside", clip=True, sizingH="fixed", sizingV="fixed")


def settings_row(b, m, desc):
    return item(b, m, "Настройки", desc, GEAR, FAINT, trail=lambda r: kbd(b, r, "⌘,"))


def in_chats(b, s):
    """1: the title's menu is the panel's own menu: remarks, chats, and settings at the bottom."""
    top(b, s, "Привести кнопки к токенам", "review-ux.figcraft")
    dim_chat(b, s)
    composer(b, s, "Задача. @слои. /навыки.")
    m = menu(b, s, "Chats menu", y=54)
    item(b, m, "Замечания", "2 открыто · 1 ждёт ответа", lead=lambda r: b.rect(r, "Dot", 8, 8, MAUVE, cornerRadius=2),
         trail=lambda r: text(b, r, "›", 13, FAINT, name="Chevron"), two=True)
    divider(b, m, 4)
    label(b, m, "Чаты файла", right="3")
    v(b, m, "chat_sel", {"Title": "Привести кнопки к токенам", "Meta": "сейчас · Sonnet 5.5"}, sizingH="fill")
    v(b, m, "chat_run", {"Title": "Стиль чата как у Orca", "Meta": "работает · 2 мин · Opus 5.5"}, sizingH="fill")
    v(b, m, "chat", {"Title": "Пустые состояния списка", "Meta": "вчера · GPT-5.5"}, sizingH="fill")
    divider(b, m, 4)
    settings_row(b, m, "агенты, доступ, навыки")
    keys(b, m, [("↑↓", "выбрать"), ("↵", "открыть")])


def in_model(b, s):
    """2: settings are about agents, access and skills — the model menu already shows two of them."""
    top(b, s, "Новый чат", "review-ux.figcraft")
    body(b, s)
    composer(b, s, "Задача. @слои. /навыки.")
    m = menu(b, s, "Model menu", y=372)
    v(b, m, "search", {"Placeholder": "Найти модель…", "Count": ""}, sizingH="fill")
    tabs = b.row(m, "Agents", gap=4, padding=[8, 4, 4, 4], sizingH="fill")
    for k, (n, c) in enumerate([("Claude Code", "4"), ("Codex", "3"), ("pi", "12")]):
        inst(b, tabs, "tab", {"State": "Selected" if k == 0 else "Default", "Label": n, "Count": c})
    label(b, m, "Модели")
    for n, d, on in [("Opus 5.5", "Для экранов и дизайн-системы", False), ("Sonnet 5.5", "Быстрее, для правок по замечаниям", True),
                     ("Haiku 5.5", "Тексты и мелкие правки", False)]:
        item(b, m, n, d, trail=(lambda r: text(b, r, "✓", 12, TEXT, True, name="Check")) if on else None,
             state="selected" if on else None)
    divider(b, m, 4)
    label(b, m, "Доступ", "для всех чатов")
    for n, d, on in [("Только FigCraft", "макет и файлы проекта", True), ("Как в терминале", "права из настроек агента", False)]:
        inst(b, m, "skill", {"Control": "Radio", "Checked": "On" if on else "Off", "State": "Default", "Name": n,
                             "Description": d}, sizingH="fill")
    divider(b, m, 4)
    settings_row(b, m, "агенты, навыки, чаты файла")


def in_row(b, s):
    """3: a quiet gear at the end of the model row, beside the agent it configures."""
    top(b, s, "Привести кнопки к токенам", "review-ux.figcraft")
    dim_chat(b, s)
    c = b.col(s, "Composer", gap=8, padding=[0, 12, 12, 12], sizingH="fill")
    inst(b, c, "input", {"State": "Empty", "Text": "Уточнить. @слои. /навыки."}, sizingH="fill")
    r = b.row(c, "Bottom", gap=4, sizingH="fill")
    inst(b, r, "model", {"Model": "Sonnet 5.5", "Effort": "", "Mode": "Только FigCraft", "Show hint": False}, sizingH="fill")
    g = b.row(r, "Settings", gap=0, w=24, h=24, cornerRadius=6, mainAlign="center", sizingH="fixed", sizingV="fixed")
    glyph(b, g, GEAR, FAINT, 13)


OPTIONS = [
    ("1 · В меню заголовка", "Заголовок открывает всё о панели: замечания, чаты, внизу — настройки. Один вход, "
                             "но настройки для всех файлов оказываются в меню этого файла.", in_chats),
    ("2 · В меню модели", "Настройки — это агенты, доступ и навыки; меню модели уже показывает модели и доступ. "
                          "Последняя строка ведёт дальше. Логично, но нужно знать, что модель — вход.", in_model),
    ("3 · В строке модели", "Тихая шестерёнка в конце нижней строки, рядом с моделью и режимом. Видна всегда, "
                            "но шапка чище только потому, что шум переехал вниз.", in_row),
]


def main():
    fc = FC()
    old = [t["id"] for t in fc.tops() if t["name"] == NAME]
    if old:
        fc.cmd("edit.delete", ids=old)
    b = B()
    board = b.col(None, NAME, gap=24, padding=40, fill="#16161E", cornerRadius=4, x=X, y=Y)
    text(b, board, "Настройки — куда, если не в шапку", 22, "#E6E9F5", True)
    text(b, board, "В шапке остаются выбор чата и «+». Настройки нужны редко: агенты, доступ, навыки, чаты файла. "
                   "Во всех вариантах работает ⌘,.", 11, FAINT, w=1300, textAutoResize="height")
    cols = b.row(board, "Options", gap=60, crossAlign="min")
    for name, note, fn in OPTIONS:
        c = b.col(cols, name, gap=10, w=400, sizingH="fixed")
        text(b, c, name, 13, "#E6E9F5", True)
        text(b, c, note, 11, DIM, sizingH="fill", textAutoResize="height")
        fn(b, screen(b, c, name))
    res = run(fc, b, NAME)
    fc.cmd("variable.setMode", ids=[res[board["$step"]]["id"]], collection="Tokens", mode="Graphite")
    print(res[board["$step"]]["id"])
    fc.tool("save_file", {})


if __name__ == "__main__":
    main()
