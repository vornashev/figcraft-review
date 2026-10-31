#!/usr/bin/env python3
"""Header variants for the Strict panel, on a board below Strict Q–AB.

The canon «Top bar» puts the chat's title, the file, «+ Новый ⌘N» and the gear in one row: busy, and nothing says
the title opens the chats. Each column is one answer, drawn in four states: an ordinary chat, a long title while the
agent works and a question waits, the remarks, and the chats open. Reruns redraw only the board.
"""
from strict import (BG, BORDER, CLAUDE, DIM, FAINT, HOVER, LINE, MAUVE, ORANGE, SURFACE, TEXT, B, FC,
                    divider, glyph, keys, label, menu, run, spacer, text)
from strict_more import v

NAME = "Strict · Шапка — варианты"
X, Y = 0, 8520
PLUS, GEAR, DOWN, LIST, BACK = "\U000f0415", "", "\U000f0140", "\U000f0279", "\U000f004d"
UNFOLD = "\U000f054f"
LONG = "Привести кнопки к токенам и собрать компонент"


def icon(b, parent, g, color=FAINT, fill="none", name="Icon"):
    r = b.row(parent, name, gap=0, w=28, h=28, fill=fill, cornerRadius=6, mainAlign="center", sizingH="fixed", sizingV="fixed")
    glyph(b, r, g, color, 14)
    return r


def bar(b, parent, h=48, padding=(0, 8, 0, 12)):
    r = b.row(parent, "Top bar", gap=4, h=h, padding=list(padding), sizingH="fill", sizingV="fixed")
    return r


def title(b, parent, s, size=13, fill=False, name="Title"):
    return b.text(parent, s, size, TEXT, True, name=name, **({"sizingH": "fill", "textAutoResize": "truncate"} if fill else {}))


def wait(b, parent, n):
    """A question waits: a mauve count, the same in every variant."""
    w = b.row(parent, "Waiting", gap=4, padding=[1, 6, 1, 5], fill="#C29CFF26", cornerRadius=8)
    b.ellipse(w, "Dot", 6, MAUVE)
    text(b, w, str(n), 11, MAUVE, True)
    return w


def running(b, parent):
    return b.ellipse(parent, "Running", 8, "none", stroke="#8E95FF", strokeWeight=1.5)


def chats_menu(b, panel, x=8, y=44, w=382, remarks=True, file_head=False):
    m = menu(b, panel, "Chats menu", x=x, y=y, w=w)
    if file_head:
        h = b.row(m, "File", gap=6, padding=[6, 8, 4, 8], sizingH="fill")
        text(b, h, "review-ux.figcraft", 11, FAINT, True)
        spacer(b, h)
        text(b, h, "3 чата", 11, FAINT)
    if remarks:
        r = b.row(m, "Замечания", gap=8, padding=[7, 8, 7, 8], cornerRadius=6, sizingH="fill")
        b.rect(r, "Dot", 8, 8, MAUVE, cornerRadius=2)
        t = b.col(r, "Text", gap=2, sizingH="fill")
        text(b, t, "Замечания", 13, TEXT)
        text(b, t, "2 открыто · 1 ждёт ответа", 12, FAINT)
        text(b, r, "›", 13, FAINT)
        divider(b, m, 4)
        label(b, m, "Чаты файла", right="3")
    v(b, m, "chat_sel", {"Title": "Привести кнопки к токенам", "Meta": "сейчас · Sonnet 5.5"}, sizingH="fill")
    v(b, m, "chat_run", {"Title": "Стиль чата как у Orca", "Meta": "работает · 2 мин · Opus 5.5"}, sizingH="fill")
    v(b, m, "chat", {"Title": "Пустые состояния списка", "Meta": "вчера · GPT-5.5"}, sizingH="fill")
    keys(b, m, [("↑↓", "выбрать"), ("↵", "открыть")])
    return m


# Each variant: fn(b, panel, state) draws the header of one state into its panel; state is
# "chat", "long", "remarks" or "open" (then it also draws the menu).

def chevron(b, p, st):
    """V1: the title is a button with ⌄; «Новый» and settings are bare icons; the file moves into the menu."""
    r = bar(b, p)
    sel = b.row(r, "Chat select", gap=6, padding=[4, 8, 4, 8], cornerRadius=6, fill=HOVER if st == "open" else "none",
                sizingH="fill" if st == "long" else "hug")
    if st == "long":
        running(b, sel)
    title(b, sel, {"chat": "Привести кнопки к токенам", "long": LONG, "remarks": "Замечания", "open": "Привести кнопки к токенам"}[st],
          fill=st == "long")
    glyph(b, sel, DOWN, FAINT, 14, name="Chevron")
    if st == "long":
        wait(b, r, 1)
    else:
        spacer(b, r)
    if st != "remarks":
        icon(b, r, PLUS)
    icon(b, r, GEAR)
    if st == "open":
        chats_menu(b, p, file_head=True)


def two_lines(b, p, st, chev="after"):
    """V2: the file is a quiet first line; the chat is the second, with ⌄, and takes the full width.

    chev: where the ⌄ goes: "after" the title, "small" after it and lighter, "unfold" (⇕) beside both lines,
    "edge" at the right end of the select, so the whole width reads as one control."""
    r = bar(b, p, 52, (0, 8, 0, 8))
    hover = st in ("open", "hover")
    sel = b.row(r, "Chat select", gap=8, padding=[4, 8, 4, 8], cornerRadius=6, fill=HOVER if hover else "none",
                sizingH="fill" if chev == "edge" or st == "long" else "hug")
    wide = "fill" if chev == "edge" or st == "long" else "hug"
    lines = b.col(sel, "Lines", gap=1, sizingH=wide)
    f = b.row(lines, "File", gap=6, sizingH=wide)
    text(b, f, "review-ux.figcraft", 11, FAINT)
    if st == "long":
        text(b, f, "· работает 0:42", 11, FAINT)
    t = b.row(lines, "Chat", gap=4 if chev == "small" else 6, sizingH=wide)
    title(b, t, {"chat": "Привести кнопки к токенам", "long": LONG, "remarks": "Замечания · 3 открыто",
                 "open": "Привести кнопки к токенам", "hover": "Привести кнопки к токенам"}[st], fill=st == "long")
    if chev in ("after", "small"):
        glyph(b, t, DOWN, FAINT if chev == "after" else "#5C6069", 14 if chev == "after" else 12, name="Chevron")
    if st == "long":
        wait(b, t, 1)
    if chev == "unfold":
        glyph(b, sel, UNFOLD, DIM if hover else FAINT, 14, name="Chevron")
    if chev == "edge":
        glyph(b, sel, DOWN, DIM if hover else FAINT, 14, name="Chevron")
    if chev in ("after", "small", "unfold") and st != "long":
        spacer(b, r)
    if st != "remarks":
        icon(b, r, PLUS)
    icon(b, r, GEAR)
    if st == "open":
        chats_menu(b, p, y=50)


def list_button(b, p, st):
    """V3: a list button on the left says «chats» by itself and carries the waiting count; the title is just a title."""
    r = bar(b, p, padding=(0, 8, 0, 8))
    lb = b.row(r, "Chats", gap=4, h=28, padding=[0, 6, 0, 6], cornerRadius=6, fill=SURFACE if st == "open" else "none",
               sizingV="fixed")
    glyph(b, lb, LIST, DIM, 15)
    if st == "long":
        b.ellipse(lb, "Badge", 7, MAUVE)
    b.rect(r, "Rule", 1, 16, LINE)
    if st == "long":
        running(b, r)
    title(b, r, {"chat": "Привести кнопки к токенам", "long": LONG, "remarks": "Замечания", "open": "Привести кнопки к токенам"}[st],
          fill=True)
    if st != "remarks":
        icon(b, r, PLUS)
    icon(b, r, GEAR)
    if st == "open":
        chats_menu(b, p, file_head=True)


def split(b, p, st):
    """V4: chats and remarks are two controls: the chat select, and a remarks button with its count."""
    r = bar(b, p, padding=(0, 8, 0, 8))
    if st == "remarks":
        icon(b, r, BACK)
        title(b, r, "Замечания", fill=True)
    else:
        sel = b.row(r, "Chat select", gap=6, padding=[4, 8, 4, 8], cornerRadius=6, fill=HOVER if st == "open" else "none",
                    sizingH="fill")
        if st == "long":
            running(b, sel)
        title(b, sel, LONG if st == "long" else "Привести кнопки к токенам", fill=True)
        glyph(b, sel, DOWN, FAINT, 14, name="Chevron")
    rb = b.row(r, "Remarks", gap=5, h=28, padding=[0, 8, 0, 7], cornerRadius=6, fill=SURFACE if st == "remarks" else "none",
               sizingV="fixed")
    b.ellipse(rb, "Ring", 10, "none", stroke=MAUVE, strokeWeight=1.5)
    text(b, rb, "2", 12, MAUVE if st == "long" else DIM, True)
    if st != "remarks":
        icon(b, r, PLUS)
    icon(b, r, GEAR)
    if st == "open":
        chats_menu(b, p, remarks=False, file_head=True)


def field(b, p, st):
    """V5: the chat select looks like a select: a bordered field with the agent, «+» joined to it."""
    r = bar(b, p, padding=(0, 8, 0, 8))
    if st == "remarks":
        icon(b, r, BACK)
        title(b, r, "Замечания", fill=True)
        icon(b, r, GEAR)
        return
    g = b.row(r, "Select", gap=0, h=32, stroke=BORDER if st != "open" else "#4C51A6", strokeWeight=1, strokeAlign="inside",
              cornerRadius=8, sizingH="fill", sizingV="fixed", clip=True)
    sel = b.row(g, "Chat", gap=8, padding=[0, 8, 0, 10], h=32, sizingH="fill", sizingV="fixed",
                fill="#1E2031" if st == "open" else "none")
    if st == "long":
        running(b, sel)
    else:
        glyph(b, sel, CLAUDE, ORANGE, 12, name="Agent")
    title(b, sel, LONG if st == "long" else "Привести кнопки к токенам", fill=True)
    if st == "long":
        wait(b, sel, 1)
    glyph(b, sel, DOWN, FAINT, 14, name="Chevron")
    b.rect(g, "Rule", 1, 32, BORDER)
    nb = b.row(g, "New", gap=0, w=32, h=32, mainAlign="center", sizingH="fixed", sizingV="fixed")
    glyph(b, nb, PLUS, DIM, 14)
    icon(b, r, GEAR)
    if st == "open":
        chats_menu(b, p, y=44, file_head=True)


VARIANTS = [
    ("V1 · Шеврон", "Название чата — кнопка с ⌄, «Новый» и настройки — иконки без подписей. Файл уходит в шапку меню. "
                    "Меньше всего шума; выбор чата узнаётся по ⌄.", chevron),
    ("V2 · Две строки", "Тихая первая строка — файл и статус, вторая — чат с ⌄ во всю ширину. Название не обрезается "
                        "из-за файла, но шапка выше на 4 px.", two_lines),
    ("V3 · Кнопка чатов", "Список чатов — отдельная иконка слева, на ней точка, когда агент ждёт ответа. "
                          "Название только читается. Привычно по мессенджерам, но иконку надо узнать.", list_button),
    ("V4 · Чат и замечания отдельно", "Селектор чата с ⌄ и кнопка замечаний со счётчиком. Меню чатов — только чаты, "
                                      "замечания в один клик; из замечаний — стрелка назад.", split),
    ("V5 · Поле-селектор", "Чат — поле с рамкой, как обычный select, «+» приклеен к нему. Самая очевидная механика, "
                           "но больше рамок в панели, где их и так мало.", field),
]
STATES = [("chat", "Обычный чат", 48), ("long", "Длинное название · агент работает · 1 ждёт ответа", 48),
          ("remarks", "Замечания", 48), ("open", "Открыт выбор чата", 340)]


def main():
    fc = FC()
    old = [t["id"] for t in fc.tops() if t["name"] == NAME]
    if old:
        fc.cmd("edit.delete", ids=old)
    b = B()
    board = b.col(None, NAME, gap=24, padding=40, fill="#16161E", cornerRadius=4, x=X, y=Y)
    text(b, board, "Шапка — варианты", 22, "#E6E9F5", True)
    text(b, board, "Сейчас в одной строке название, файл, «+ Новый ⌘N» и настройки: шумно, и не видно, что название "
                   "открывает чаты. Каждый вариант — в четырёх состояниях.", 11, FAINT, w=1200, textAutoResize="height")
    cols = b.row(board, "Variants", gap=60, crossAlign="min")
    for name, note, fn in VARIANTS:
        c = b.col(cols, name, gap=10, w=400, sizingH="fixed")
        text(b, c, name, 13, "#E6E9F5", True)
        text(b, c, note, 11, DIM, sizingH="fill", textAutoResize="height")
        for st, cap, h in STATES:
            text(b, c, cap, 11, FAINT)
            p = b.col(c, st, gap=0, w=400, h=h if st == "open" else None, fill=BG, cornerRadius=12, stroke=LINE,
                      strokeWeight=1, strokeAlign="inside", clip=True, sizingH="fixed")
            fn(b, p, st)
    text(b, board, "V2 · где шеврон", 13, "#E6E9F5", True)
    cols = b.row(board, "Chevron", gap=60, crossAlign="min")
    for chev, name, note in [
            ("after", "1 · Сразу за названием", "Как сейчас: ⌄ гуляет вместе с длиной названия и спорит с плашкой «ждёт»."),
            ("small", "2 · За названием, тише", "Тот же порядок, ⌄ меньше и бледнее: меньше шума, но и заметность ниже."),
            ("unfold", "3 · ⇕ рядом с обеими строками", "Значок выбора из списка по центру блока: относится и к файлу, и к чату."),
            ("edge", "4 · На краю, как у select", "Вся ширина — один контрол, ⌄ всегда на одном месте перед «+»; длинное название обрезается перед ним.")]:
        c = b.col(cols, name, gap=10, w=400, sizingH="fixed")
        text(b, c, name, 13, "#E6E9F5", True)
        text(b, c, note, 11, DIM, sizingH="fill", textAutoResize="height")
        for st, cap in [("chat", "Обычный чат"), ("hover", "Наведение"), ("long", "Длинное название · 1 ждёт ответа")]:
            text(b, c, cap, 11, FAINT)
            p = b.col(c, st, gap=0, w=400, fill=BG, cornerRadius=12, stroke=LINE, strokeWeight=1, strokeAlign="inside",
                      clip=True, sizingH="fixed")
            two_lines(b, p, st, chev)
    res = run(fc, b, NAME)
    fc.cmd("variable.setMode", ids=[res[board["$step"]]["id"]], collection="Tokens", mode="Graphite")
    print(res[board["$step"]]["id"])
    fc.tool("save_file", {})


if __name__ == "__main__":
    main()
