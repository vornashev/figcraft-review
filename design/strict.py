#!/usr/bin/env python3
"""Adds the Strict screens F–P to the «Агент» page of design/review-ux.figcraft, right of «Strict · E».

Strict A–E (drawn by hand) cover the chat, the input and the remarks; these are the rest of the panel in the
same style, for approval: switching chats and remarks, the model menu, the + and @ menus, a finished turn,
settings, the image viewer, the skill library, a skill's card and the chat's skills. They are built from the
«Strict · Компоненты» section and bound to the Graphite mode of the Tokens collection. Reruns redraw only
these frames. Run with review-ux.figcraft as the current document.
"""

import lib  # noqa: E402
from lib import B, FC, run  # noqa: E402
from strict_icons import GLYPHS, ids, size_for  # noqa: E402

GRAPHITE = {
    "bg": "#17181B", "rail": "#121316", "card": "#1F2023", "line": "#27292E", "border": "#34373D",
    "text": "#E6E7EA", "text-dim": "#A6A9B0", "text-faint": "#878B94", "accent": "#8E95FF", "accent-hover": "#A5AAFF",
    "selected": "#2C2F4D", "nav-selected": "#25273D", "hover": "#232428", "surface": "#2A2C30", "highlight": "#1E2031",
    "highlight-border": "#4C51A6", "card-hover": "#242529", "card-active": "#24263A", "green": "#5FD38D", "red": "#FF6B7A",
    "yellow": "#F2C14E", "mauve": "#C29CFF", "orange": "#FF9F5A", "cyan": "#6CCFF6",
}
lib.VAR_FOR_HEX = {v: "color/" + k for k, v in GRAPHITE.items()}
lib.VAR_FOR_HEX["#121316"] = "color/inset"
lib.FONT = "Golos Text"
T = {k.replace("text-", ""): v for k, v in GRAPHITE.items()}
BG, CARD, LINE, BORDER, TEXT, DIM, FAINT = (T[k] for k in ("bg", "card", "line", "border", "text", "dim", "faint"))
SURFACE, HOVER, INSET, ACCENT = T["surface"], T["hover"], "#121316", T["accent"]
GREEN, RED, YELLOW, MAUVE, ORANGE = (T[k] for k in ("green", "red", "yellow", "mauve", "orange"))
SHADOW = [{"type": "dropShadow", "color": "#00000066", "offset": [0, 8], "radius": 24}]
MONO = "JetBrainsMono Nerd Font"
CLAUDE = ""
ICON_IDS = ids()

COMP = dict(top=47244641082, kbd=47244640914, button=47244640944, icon=47244640945, send=47244640946, tab=47244640970,
            chip=47244640971, option=47244641012, step=47244641013, change=47244641014, group=47244641078,
            skill=47244641079, remark=47244641080, message=47244641081, model=47244641091, input=47244641120)
SCREENS = ["F · Чаты и замечания", "G · Модель и доступ", "I · Меню +", "J · Меню @", "K · Итог хода",
           "L · Настройки", "M · Просмотр картинки", "N · Навыки", "O · Карточка навыка", "P · Навыки чата"]
X0, Y = 2760, 3880
SHOT = "dec0aa737746d0982058a564930dfafb792d241e671f00ad5b6d752c110a5eaf"


# ---- atoms ----

def text(b, parent, s, size=13, color=TEXT, bold=False, name=None, **kw):
    return b.text(parent, s, size, color, bold, name=name, **kw)


def code(b, parent, s, color=FAINT, name="Code"):
    r = b.node("text", parent, name, text=s, fontFamily=MONO, fontStyle="Regular", fontSize=11, fill=color)
    b.add("style.apply", {"ids": [r], "style": "Code"})
    return r


def glyph(b, parent, s, color=FAINT, size=14, name="Icon"):
    """An icon from «Strict · Иконки» for a Nerd Font glyph (strict_icons.py); other characters stay text, 14 wide."""
    if s in GLYPHS:
        n = size_for(name, size)
        r = b.inst(parent, ICON_IDS[GLYPHS[s]], name=name, width=n, height=n)
        if color != FAINT:
            b.ov(r, "Vector", fill=color)
        return r
    return b.node("text", parent, name, text=s, fontFamily=MONO, fontStyle="Regular", fontSize=size, fill=color,
                  width=14, textAlign="center", textAutoResize="height")


def inst(b, parent, comp, props=None, **setp):
    return b.inst(parent, COMP[comp], props, **setp)


def kbd(b, parent, key):
    return inst(b, parent, "kbd", {"Key": key})


def button(b, parent, label, variant="Ghost", **setp):
    return inst(b, parent, "button", {"Variant": variant, "Label": label}, **setp)


def spacer(b, parent):
    return b.frame(parent, "Spacer", "horizontal", h=1, sizingH="fill")


def divider(b, parent, inset=0):
    if not inset:
        return b.rect(parent, "Divider", 10, 1, LINE, sizingH="fill")
    w = b.frame(parent, "Divider", "horizontal", padding=[4, inset, 4, inset], sizingH="fill")
    b.rect(w, "Line", 10, 1, LINE, sizingH="fill")
    return w


def screen(b, name, i):
    return b.col(None, "Strict · " + name, gap=0, w=400, h=860, fill=BG, cornerRadius=12, stroke=LINE, strokeWeight=1,
                 strokeAlign="inside", clip=True, x=X0 + i * 460, y=Y)


def top(b, parent, title, file=None, action=None, new=True):
    props = {"Title": title, "Show file": file is not None, "Show new": new, "Show action": action is not None}
    if file is not None:
        props["File"] = file
    r = inst(b, parent, "top", props, sizingH="fill")
    if action:
        b.ovp(r, "Action", {"Label": action})
    return r


def back_top(b, parent, title, sub, trail=None):
    """A page's own top bar: back, title and what it applies to."""
    r = b.row(parent, "Top bar", gap=8, h=48, padding=[0, 12, 0, 8], sizingH="fill", sizingV="fixed")
    inst(b, r, "icon", {"Icon": "\U000f004d"})
    text(b, r, title, 13, TEXT, True, name="Title")
    text(b, r, sub, 12, FAINT, name="File", sizingH="fill")
    if trail:
        trail(r)
    b.rect(parent, "Divider", 10, 1, LINE, sizingH="fill")
    return r


def body(b, parent, gap=16, padding=(12, 16, 16, 16), main="min"):
    return b.col(parent, "Body", gap=gap, padding=list(padding), sizingH="fill", sizingV="fill", mainAlign=main)


def composer(b, parent, hint="Задача. @слои. /скиллы.", state="Empty", model_hint=None):
    c = b.col(parent, "Composer", gap=8, padding=[0, 12, 12, 12], sizingH="fill")
    inst(b, c, "input", {"State": state, "Text": hint}, sizingH="fill")
    props = {"Model": "Sonnet 5.5", "Effort": "", "Mode": "Только FigCraft", "Show hint": model_hint is not None}
    if model_hint:
        props["Hint"] = model_hint
    inst(b, c, "model", props, sizingH="fill")
    return c


def menu(b, parent, name, x=8, y=None, bottom=None, w=382):
    """A popup over the panel: card, border, shadow; positioned absolutely in its screen."""
    m = b.col(parent, name, gap=0, w=w, fill=CARD, stroke=BORDER, strokeWeight=1, strokeAlign="inside", cornerRadius=12,
              padding=4, effects=SHADOW, sizingH="fixed")
    b.set(m, absolute=True, x=x, y=y if y is not None else 0)
    return m


def head(b, parent, title, trail=None, trail_color=FAINT):
    h = b.row(parent, "Header", gap=8, padding=[8, 8, 8, 8], sizingH="fill")
    text(b, h, title, 12, DIM, True, name="Title", sizingH="fill")
    if trail:
        text(b, h, trail, 12, trail_color, name="Trail")
    return h


def label(b, parent, title, note=None, right=None, dot=None):
    g = b.row(parent, "Group · " + title, gap=6, padding=[8, 8, 4, 8], sizingH="fill")
    if dot:
        b.rect(g, "Dot", 8, 8, dot, cornerRadius=2)
    text(b, g, title, 11, FAINT, True, name="Label")
    if note:
        text(b, g, note, 11, FAINT, name="Note")
    if right:
        spacer(b, g)
        text(b, g, right, 11, FAINT, name="Right")
    return g


def item(b, parent, title, desc=None, lead=None, lead_color=FAINT, trail=None, state=None, wrap=False, two=False):
    """A row of a menu or list: lead glyph, title and description, something on the right."""
    fill = {"selected": SURFACE, "hover": HOVER}.get(state, "none")
    r = b.row(parent, title, gap=8, padding=[7 if two else 6, 8, 7 if two else 6, 8], cornerRadius=6, fill=fill,
              sizingH="fill", crossAlign="center")
    if lead is not None:
        if isinstance(lead, str):
            glyph(b, r, lead, lead_color, 13 if len(lead) == 1 and ord(lead) < 0x2000 else 14, name="Lead")
        else:
            lead(r)
    if two:
        t = b.col(r, "Text", gap=2, sizingH="fill")
        text(b, t, title, 13, TEXT, name="Title", sizingH="fill", textAutoResize="truncate" if not wrap else "height")
        if desc:
            text(b, t, desc, 12, FAINT, name="Description", sizingH="fill",
                 textAutoResize="truncate" if not wrap else "height")
    else:
        text(b, r, title, 13, TEXT, name="Title")
        if desc:
            text(b, r, desc, 12, FAINT, name="Description", sizingH="fill", textAutoResize="truncate")
        else:
            spacer(b, r)
    if trail:
        trail(r)
    return r


def toggle(b, parent, on=True):
    t = b.frame(parent, "Toggle", None, 28, 16, fill=TEXT if on else SURFACE, cornerRadius=8)
    b.ellipse(t, "Knob", 12, BG if on else FAINT, x=14 if on else 2, y=2)
    return t


def card(b, parent, name, padding=4, gap=0):
    return b.col(parent, name, gap=gap, padding=padding, fill=CARD, stroke=LINE, strokeWeight=1, strokeAlign="inside",
                 cornerRadius=10, sizingH="fill")


def keys(b, parent, pairs, right=None):
    f = b.row(parent, "Footer", gap=6, padding=[8, 6, 4, 8], sizingH="fill")
    for k, v in pairs:
        kbd(b, f, k)
        text(b, f, v, 11, FAINT, name=v)
    if right:
        spacer(b, f)
        right(f)
    return f


def dim_chat(b, parent):
    """The conversation behind a popup."""
    m = body(b, parent)
    inst(b, m, "message", {"State": "Sent", "Text": "Кнопки на B и H разные по радиусу и цвету. Приведи к токенам и сделай одним компонентом"},
         sizingH="fill")
    text(b, m, "›  2 вызова · 1 сообщение", 12, FAINT)
    text(b, m, "Нашёл 7 кнопок: три радиуса (6, 8, 12) и две заливки. Собираю компонент Button на токенах и заменяю им старые кнопки.",
         13, TEXT, name="Agent", sizingH="fill", textAutoResize="height")
    return m


# ---- screens ----

def chats(b, i):
    """F: the title opens the file's chats and its remarks; a waiting count sits next to the file name."""
    s = screen(b, "F · Чаты и замечания", i)
    top(b, s, "Привести кнопки к токенам", "review-ux.figcraft")
    dim_chat(b, s)
    composer(b, s)
    m = menu(b, s, "Chats menu", y=54)
    item(b, m, "Замечания", "2 открыто · 1 ждёт ответа", lead=lambda r: b.rect(r, "Dot", 8, 8, MAUVE, cornerRadius=2),
         trail=lambda r: text(b, r, "›", 13, FAINT, name="Chevron"), two=True)
    divider(b, m, 4)
    label(b, m, "Чаты файла", right="3")
    item(b, m, "Привести кнопки к токенам и собрать компонент", "сейчас · Sonnet 5.5", CLAUDE, ORANGE,
         trail=lambda r: text(b, r, "✓", 12, TEXT, True, name="Check"), state="selected", two=True)
    item(b, m, "Стиль чата как у Orca", "работает · 2 мин · Opus 5.5", CLAUDE, ORANGE,
         trail=lambda r: b.ellipse(r, "Running", 10, "none", stroke=ACCENT, strokeWeight=1.5), two=True)
    item(b, m, "Пустые состояния списка", "вчера · GPT-5.5", "X", GREEN,
         trail=lambda r: button(b, r, "Удалить"), state="hover", two=True)
    keys(b, m, [("↑↓", "выбрать"), ("↵", "открыть")], right=lambda f: button(b, f, "+ Новый чат", "Primary"))
    return s


def settings_link(b, parent):
    """Settings live at the foot of the model menu, not in the header: agents, access and skills are what it sets."""
    r = b.row(parent, "Settings", gap=6, padding=[2, 6, 2, 6], cornerRadius=6)
    g = glyph(b, r, "\uf013", FAINT, 12)
    b.set(g, textAutoResize="height", width=10.5, textAlign="left")
    text(b, r, "Настройки", 12, DIM, name="Label")
    kbd(b, r, "⌘,")
    return r


def models(b, i):
    """G: the model row opens agents, their models and the agent's access."""
    s = screen(b, "G · Модель и доступ", i)
    top(b, s, "Новый чат", "review-ux.figcraft")
    body(b, s)
    composer(b, s)
    m = menu(b, s, "Model menu", y=356)
    f = b.row(m, "Search", gap=8, padding=[7, 10, 7, 10], fill=INSET, cornerRadius=6, sizingH="fill")
    glyph(b, f, "\U000f0349", FAINT, 13)
    text(b, f, "Найти модель…", 13, FAINT, name="Placeholder")
    tabs = b.row(m, "Agents", gap=4, padding=[8, 4, 4, 4], sizingH="fill")
    for k, (n, c) in enumerate([("Claude Code", "4"), ("Codex", "3"), ("pi", "12")]):
        inst(b, tabs, "tab", {"State": "Selected" if k == 0 else "Default", "Label": n, "Count": c})
    label(b, m, "Модели", right="доступен")
    for n, d, on in [("Fable 5.1", "Самая сильная, отвечает дольше", False), ("Opus 5.5", "Для экранов и дизайн-системы", False),
                     ("Sonnet 5.5", "Быстрее, для правок по замечаниям", True), ("Haiku 5.5", "Тексты и мелкие правки", False)]:
        item(b, m, n, d, trail=(lambda r: text(b, r, "✓", 12, TEXT, True, name="Check")) if on else None,
             state="selected" if on else None)
    divider(b, m, 4)
    label(b, m, "Доступ", "для всех чатов")
    for n, d, on in [("Только FigCraft", "макет и файлы проекта", True), ("Как в терминале", "права из настроек агента", False)]:
        inst(b, m, "skill", {"Control": "Radio", "Checked": "On" if on else "Off", "State": "Default", "Name": n,
                             "Description": d}, sizingH="fill")
    keys(b, m, [("↑↓", "выбрать"), ("↵", "готово")], right=lambda f: settings_link(b, f))
    return s


def plus(b, i):
    """I: + next to the model: what can go into the message."""
    s = screen(b, "I · Меню +", i)
    top(b, s, "Новый чат", "review-ux.figcraft")
    body(b, s)
    composer(b, s)
    m = menu(b, s, "Plus menu", y=232)
    label(b, m, "Вставить")
    item(b, m, "Выделенные слои", "Composer, Send", "#", trail=lambda r: kbd(b, r, "Tab"), state="selected")
    item(b, m, "Открытые замечания", "2 открыто", "\U000f0026")
    item(b, m, "Слой или замечание", "по имени", "@", trail=lambda r: kbd(b, r, "@"))
    item(b, m, "Файлы и картинки", "или вставьте, перетащите", "\U000f0224")
    divider(b, m, 4)
    label(b, m, "Навыки")
    item(b, m, "Навык к сообщению", None, "\U000f0b64", trail=lambda r: kbd(b, r, "/"))
    item(b, m, "Навыки чата", "figcraft-design · Almanac", "\U000f0403")
    item(b, m, "Все навыки", "библиотека и режимы", "\U000f0a66", trail=lambda r: text(b, r, "›", 13, FAINT))
    divider(b, m, 4)
    label(b, m, "Задачи")
    item(b, m, "Варианты", "2–3 направления, сценарии те же", "\U000f0568")
    item(b, m, "Составить DESIGN.md", "о продукте для агента", "\U000f0219")
    divider(b, m, 4)
    item(b, m, "PNG слоёв из чипов", "к каждому сообщению", "\U000f02e9", trail=lambda r: toggle(b, r, True))
    return s


def mention(b, i):
    """J: @ in the text: the page's remarks and layers, inserted as chips."""
    s = screen(b, "J · Меню @", i)
    top(b, s, "Новый чат", "review-ux.figcraft")
    body(b, s)
    c = b.col(s, "Composer", gap=8, padding=[0, 12, 12, 12], sizingH="fill")
    inst(b, c, "input", {"State": "Filled", "Text": "Убери тень у @comp"}, sizingH="fill")
    inst(b, c, "model", {"Model": "Sonnet 5.5", "Effort": "", "Mode": "Только FigCraft", "Show hint": False}, sizingH="fill")
    m = menu(b, s, "Mention menu", y=420)
    head(b, m, "@comp", "4 найдено")
    label(b, m, "Замечания")
    item(b, m, "#12 Убрать тень у панели ввода", "Composer", lambda r: b.ellipse(r, "Status", 12, "none", stroke=ORANGE,
                                                                                    strokeWeight=1.5))
    label(b, m, "Слои страницы")
    item(b, m, "Composer", "frame · 374×88", "#", trail=lambda r: kbd(b, r, "↵"), state="selected")
    item(b, m, "Composer field", "component · 374×105", "❖", MAUVE)
    item(b, m, "Composer", "instance · B · Разговор", "◇", MAUVE)
    keys(b, m, [("↑↓", "выбрать"), ("↵", "вставить"), ("Esc", "закрыть")])
    return s


def turn(b, i):
    """K: a finished turn: what changed, remarks it marked, access it lacked, what it took."""
    s = screen(b, "K · Итог хода", i)
    top(b, s, "Привести кнопки к токенам и собрать компонент", "review-ux.figcraft")
    m = body(b, s)
    inst(b, m, "message", {"State": "Sent", "Text": "Собери кнопки в компонент и проверь сборку"}, sizingH="fill")
    text(b, m, "›  9 вызовов · 2 сообщения", 12, FAINT)
    text(b, m, "Собрал Button на токенах и заменил им 7 кнопок. Сборку проверить не смог — нужен Bash.", 13, TEXT,
         name="Agent", sizingH="fill", textAutoResize="height")
    ch = b.col(m, "Changed", gap=2, sizingH="fill")
    h = b.row(ch, "Header", gap=6, padding=[0, 0, 4, 0], sizingH="fill")
    text(b, h, "Изменено на холсте", 12, DIM, True)
    text(b, h, "9 шагов", 12, FAINT, name="Count")
    spacer(b, h)
    button(b, h, "Показать")
    button(b, h, "Отменить")
    for kind, n, d, k in [("Added", "Button", "компонент", "#4710"), ("Changed", "Отправить", "B · Разговор · радиус 6", "#3055"),
                          ("Changed", "Принять", "H · Замечания · заливка", "#4331")]:
        inst(b, ch, "change", {"Kind": kind, "Name": n, "Detail": d, "Id": k}, sizingH="fill")
    mk = b.row(m, "Marked", gap=8, sizingH="fill")
    text(b, mk, "✓", 12, GREEN, True, name="Status")
    text(b, mk, "#12 → Проверь", 12, TEXT, name="Remarks")
    spacer(b, mk)
    button(b, mk, "Замечания ›")
    d = card(b, m, "Denied", padding=[10, 12, 10, 12], gap=8)
    text(b, d, "Не хватило доступа", 12, YELLOW, True)
    code(b, d, "Bash · npm run build", DIM)
    a = b.row(d, "Actions", gap=6, sizingH="fill")
    text(b, a, "только в этом чате", 11, FAINT, name="Scope")
    spacer(b, a)
    button(b, a, "Разрешить и продолжить ↵", "Primary")
    st = b.col(m, "Stats", gap=6, sizingH="fill")
    text(b, st, "Работал 1 мин 12 с · $0.18  ⌄", 12, FAINT, name="Summary")
    g = b.col(st, "Numbers", gap=3, padding=[8, 10, 8, 10], fill=INSET, cornerRadius=6, sizingH="fill")
    for k, v in [("Входящие токены", "182.4k"), ("Исходящие токены", "6.1k"), ("Чтение кэша", "1.2M"),
                 ("Контекст", "64.0k из 200.0k"), ("До первого ответа", "3 с")]:
        r = b.row(g, k, gap=8, sizingH="fill")
        text(b, r, k, 11, FAINT)
        spacer(b, r)
        code(b, r, v, DIM)
    e = b.row(m, "Error", gap=8, sizingH="fill")
    text(b, e, "Ход прервался: агент закрылся с кодом 1", 12, RED, name="Error", sizingH="fill", textAutoResize="height")
    composer(b, s, "Уточнить. @слои. /скиллы.")
    return s


def settings(b, i):
    """L: settings for every file: agents, their access, skills, the file's chats."""
    s = screen(b, "L · Настройки", i)
    back_top(b, s, "Настройки", "для всех файлов")
    m = body(b, s, gap=8, padding=(8, 12, 16, 12))
    label(b, m, "Агенты")
    c = card(b, m, "Agents")
    for mark, color, n, d, trail in [(CLAUDE, ORANGE, "Claude Code", "2.1.12 · ~/.claude", "4 модели"),
                                     (CLAUDE, ORANGE, "Claude Code · work", "аккаунт ~/.claude-work", "4 модели"),
                                     ("X", GREEN, "Codex", "0.44.0 · ~/.local/bin/codex", "3 модели"),
                                     ("π", MAUVE, "pi", "1.4.0 · ~/.local/bin/pi", "12 моделей")]:
        item(b, c, n, d, mark, color, trail=lambda r, t=trail: text(b, r, t, 12, FAINT, name="Count"), two=True)
    item(b, c, "Cursor", "не найден в PATH", "?", FAINT, trail=lambda r: button(b, r, "Как установить"), two=True)
    label(b, m, "Доступ агента")
    c = card(b, m, "Access")
    for n, d, on in [("Только FigCraft", "макет и файлы проекта", True), ("Как в терминале", "права из настроек агента", False)]:
        inst(b, c, "skill", {"Control": "Radio", "Checked": "On" if on else "Off", "State": "Default", "Name": n,
                             "Description": d}, sizingH="fill")
    label(b, m, "Навыки")
    c = card(b, m, "Skills")
    item(b, c, "Все навыки", "библиотека · 58 · группы и режимы", "\U000f0a66",
         trail=lambda r: text(b, r, "›", 13, FAINT), two=True)
    label(b, m, "Чаты")
    c = card(b, m, "Chats")
    item(b, c, "У этого файла 3 чата", "~/.local/state/figcraft-agent", None,
         trail=lambda r: button(b, r, "Очистить"), two=True)
    text(b, m, "Агенты работают через свои CLI и ваши подписки — ключи не нужны. Чат продолжает сессию агента.",
         11, FAINT, name="Foot", sizingH="fill", textAutoResize="height")
    return s


def viewer(b, i):
    """M: a picture from the input or a message, full panel."""
    s = screen(b, "M · Просмотр картинки", i)
    h = b.row(s, "Top bar", gap=8, h=48, padding=[0, 12, 0, 16], sizingH="fill", sizingV="fixed")
    text(b, h, "Картинка 2", 13, TEXT, True, name="Title")
    text(b, h, "1440×900 · 2 из 3", 12, FAINT, name="Meta", sizingH="fill")
    inst(b, h, "icon", {"Icon": "\U000f01da"})
    inst(b, h, "icon", {"Icon": "\U000f0156"})
    st = b.row(s, "Stage", gap=8, padding=[8, 12, 8, 12], sizingH="fill", sizingV="fill")
    for side in ("‹", "›"):
        if side == "›":
            img = b.frame(st, "Picture", None, 10, 220, fill=INSET, cornerRadius=8, sizingH="fill", sizingV="fill")
            b.set(img, fills=[{"type": "image", "image": SHOT, "scaleMode": "fit"}])
        nav = b.row(st, "Prev" if side == "‹" else "Next", gap=0, w=28, h=28, fill=SURFACE, cornerRadius=14,
                    mainAlign="center", sizingH="fixed", sizingV="fixed")
        text(b, nav, side, 13, DIM, True)
    bar = b.row(s, "Tools", gap=0, sizingH="fill", mainAlign="center")
    tools = b.row(bar, "Zoom", gap=4, padding=[3, 4, 3, 4], fill=SURFACE, cornerRadius=8)
    for t in ("−", "64%", "+", "Вписать"):
        p = b.row(tools, t, gap=0, padding=[2, 8, 2, 8], cornerRadius=6)
        text(b, p, t, 12, DIM if t != "64%" else TEXT)
    strip = b.row(s, "Strip", gap=8, padding=[12, 0, 8, 0], sizingH="fill", mainAlign="center")
    for k in range(3):
        t = b.frame(strip, f"Thumb {k + 1}", None, 48, 48, fill=INSET, cornerRadius=6, stroke=TEXT if k == 1 else BORDER,
                    strokeWeight=2 if k == 1 else 1, strokeAlign="inside", clip=True)
        b.set(t, fills=[{"type": "image", "image": SHOT, "scaleMode": "fill"}])
    k = keys(b, s, [("Esc", "закрыть"), ("← →", "листать"), ("колесо", "масштаб")])
    b.set(k, padding=[4, 16, 16, 16], mainAlign="center")
    return s


MODES = {"auto": ("Сам", GREEN), "manual": ("Вручную", DIM), "always": ("Всегда", TEXT)}


def library(b, i):
    """N: every skill by group, its mode in the library, a search and the group filter."""
    s = screen(b, "N · Навыки", i)
    back_top(b, s, "Навыки", "для всех файлов · 58", trail=lambda r: button(b, r, "?"))
    m = body(b, s, gap=6, padding=(12, 12, 12, 12))
    f = b.row(m, "Search", gap=8, padding=[7, 10, 7, 10], fill=INSET, cornerRadius=6, sizingH="fill")
    glyph(b, f, "\U000f0349", FAINT, 13)
    text(b, f, "Найти навык…", 13, FAINT, name="Placeholder")
    tabs = b.row(m, "Groups", gap=4, padding=[4, 0, 4, 0], sizingH="fill", wrap=True)
    for k, (n, c) in enumerate([("Все", "58"), ("Основа", "1"), ("Стиль", "50"), ("Качество", "6"), ("Задачи", "2")]):
        inst(b, tabs, "tab", {"State": "Selected" if k == 0 else "Default", "Label": n, "Count": c})
    for g, color, note, rows in [
        ("Основа", ACCENT, "всегда в каждом ходе", [("figcraft-design", "работа с FigCraft, токены, проверка", "always")]),
        ("Стиль", MAUVE, "один на чат", [("Almanac", "редакционный, сдержанный акцент", "manual"),
                                         ("Arcade", "игривый, тёмный, полная палитра", "manual")]),
        ("Качество", GREEN, None, [("better-accessibility", "фокус, клавиатура, контраст", "auto"),
                                   ("better-layout", "группы, выравнивание, адаптив", "auto")]),
        ("Задачи", YELLOW, None, [("better-interface", "ревью экрана по всем better-*", "manual")])]:
        label(b, m, g, note, dot=color)
        c = card(b, m, g)
        for n, d, mode in rows:
            t, tc = MODES[mode]
            item(b, c, n, d, trail=lambda r, t=t, tc=tc: text(b, r, t + " ⌄", 12, tc, name="Mode"))
    f = b.row(s, "Footer", gap=8, padding=[10, 16, 12, 16], sizingH="fill")
    text(b, f, "встроенные · мои · проект · pen.dev", 11, FAINT, sizingH="fill")
    button(b, f, "+ Добавить")
    return s


def skill_card(b, i):
    """O: one skill: its look, what it does, how it applies, its files, pin it to the chat."""
    s = screen(b, "O · Карточка навыка", i)
    back_top(b, s, "Almanac", "Стиль · встроенный")
    m = body(b, s, gap=12, padding=(12, 16, 12, 16))
    p = b.col(m, "Preview", gap=10, padding=14, fill="#F4EFE6", cornerRadius=10, sizingH="fill")
    r = b.row(p, "Sample", gap=10, sizingH="fill")
    b.node("text", r, "Aa", text="Aa", fontFamily="Inter", fontStyle="Bold", fontSize=22, fill="#1F1D1A")
    b.node("text", r, "Font", text="Source Serif · 15/24", fontFamily="Inter", fontStyle="Regular", fontSize=11,
           fill="#4F4B44", sizingH="fill")
    btn = b.row(r, "Button", gap=0, padding=[6, 12, 6, 12], fill="#B4532A", cornerRadius=6)
    b.node("text", btn, "Войти", text="Войти", fontFamily="Inter", fontStyle="Bold", fontSize=12, fill="#F4EFE6")
    sw = b.row(p, "Palette", gap=6, sizingH="fill")
    for c in ("#F4EFE6", "#E6DED0", "#1F1D1A", "#B4532A"):
        b.node("rectangle", sw, c, 10, 24, fill=c, cornerRadius=4, stroke="#00000022", strokeWeight=1, sizingH="fill")
    text(b, m, "Редакционный стиль: тёплая бумага, сериф в заголовках, один сдержанный акцент. Для текстовых экранов и документации.",
         13, DIM, name="Description", sizingH="fill", textAutoResize="height")
    label(b, m, "Как применять")
    c = card(b, m, "Modes")
    for n, d, on in [("Вручную", "через / или закрепить в чате", True), ("Сам", "агент берёт по описанию", False),
                     ("Всегда", "с каждым сообщением", False)]:
        inst(b, c, "skill", {"Control": "Radio", "Checked": "On" if on else "Off", "State": "Default", "Name": n,
                             "Description": d}, sizingH="fill")
    label(b, m, "Внутри", "4 файла · 12 КБ")
    c = card(b, m, "Files", padding=[6, 10, 6, 10], gap=4)
    for n, sz in [("SKILL.md", "3 КБ"), ("tokens.md", "4 КБ"), ("components.md", "4 КБ"), ("examples/", "1 картинка")]:
        r = b.row(c, n, gap=8, sizingH="fill")
        code(b, r, n, DIM)
        spacer(b, r)
        text(b, r, sz, 11, FAINT)
    f = b.row(s, "Footer", gap=8, padding=[10, 16, 12, 16], sizingH="fill")
    button(b, f, "Закрепить в этом чате", "Primary")
    spacer(b, f)
    button(b, f, "Папка")
    return s


def pinned(b, i):
    """P: «Закреплено в чате» over the input opens the chat's skills."""
    s = screen(b, "P · Навыки чата", i)
    top(b, s, "Стиль чата как у Orca", "review-ux.figcraft")
    body(b, s)
    c = b.col(s, "Composer", gap=8, padding=[0, 12, 12, 12], sizingH="fill")
    pr = b.row(c, "Pinned", gap=6, padding=[0, 6, 0, 6], sizingH="fill")
    text(b, pr, "Закреплено в чате", 11, FAINT)
    text(b, pr, "Almanac · better-layout", 11, DIM, sizingH="fill")
    text(b, pr, "⌃", 11, FAINT)
    inst(b, c, "input", {"State": "Empty", "Text": "Задача. @слои. /скиллы."}, sizingH="fill")
    inst(b, c, "model", {"Model": "Sonnet 5.5", "Effort": "", "Mode": "Только FigCraft", "Show hint": False}, sizingH="fill")
    m = menu(b, s, "Pinned menu", y=402)
    head(b, m, "Навыки этого чата", "идут с каждым сообщением")
    label(b, m, "Всегда")
    item(b, m, "figcraft-design", "работа с FigCraft", lambda r: b.rect(r, "Mark", 7, 7, ACCENT, cornerRadius=2),
         trail=lambda r: glyph(b, r, "\U000f033e", FAINT, 13, name="Lock"))
    label(b, m, "Закреплены", right="2")
    item(b, m, "Almanac", "стиль", lambda r: b.rect(r, "Mark", 7, 7, MAUVE, cornerRadius=2),
         trail=lambda r: text(b, r, "×", 13, FAINT, name="Remove"))
    item(b, m, "better-layout", "качество", lambda r: b.rect(r, "Mark", 7, 7, GREEN, cornerRadius=2),
         trail=lambda r: text(b, r, "×", 13, FAINT, name="Remove"), state="hover")
    item(b, m, "Добавить навык", None, "+", DIM)
    divider(b, m, 4)
    item(b, m, "Агент может взять ещё", "навыки с режимом «Сам» — по описанию", None,
         trail=lambda r: toggle(b, r, True), two=True)
    divider(b, m, 4)
    f = b.row(m, "Footer", gap=6, padding=[6, 4, 4, 4], sizingH="fill")
    button(b, f, "Все навыки ›")
    spacer(b, f)
    button(b, f, "Для новых чатов файла")
    return s


BUILD = [chats, models, plus, mention, turn, settings, viewer, library, skill_card, pinned]


def main():
    fc = FC()
    tops = fc.tops()
    old = [t["id"] for t in tops if t["name"].removeprefix("Strict · ") in SCREENS]
    if old:
        fc.cmd("edit.delete", ids=old)
    b = B()
    frames = [fn(b, i) for i, fn in enumerate(BUILD)]
    res = run(fc, b, "Strict F–P")
    ids = [res[f["$step"]]["id"] for f in frames]
    fc.cmd("variable.setMode", ids=ids, collection="Tokens", mode="Graphite")
    print(ids)


if __name__ == "__main__":
    main()
