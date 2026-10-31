#!/usr/bin/env python3
"""Adds the rest of the panel in the Strict style, a row below «Strict · Компоненты — дополнение».

Strict A–P are the canon; these are the states they leave out, drawn from the same components (the base set and
its «дополнение») and the UI review of the React build: a turn that broke or ran out of limit, pictures in a
message, a remark to check, notices, a chat's actions, clearing chats, the queue, a skill's mode, the library's
help and import, empty and error states. Reruns redraw only these frames. Run with review-ux.figcraft open.
"""
from strict import (ACCENT, BG, BORDER, CARD, CLAUDE, DIM, FAINT, GREEN, INSET, LINE, MAUVE, ORANGE, RED, SHADOW, SHOT,
                    SURFACE, TEXT, B, FC, back_top, body, button, card, code, composer, divider, glyph,
                    head, inst, item, kbd, keys, label, menu, run, spacer, text, top)

X0, Y = 0, 7560
HINT = "Задача. @слои. /навыки."
SCREENS = ["Q · Ход прервался", "R · Лимит подписки", "S · Картинки в сообщении", "T · Замечание на проверке",
           "U · Уведомления", "V · Действия с чатом", "W · Очистить чаты", "X · Очередь", "Y · Режим навыка",
           "Z · Как работают навыки", "AA · Добавить навык", "AB · Пустые и ошибки"]

# Variants of «Strict · Компоненты — дополнение», used as they are.
V = dict(toast_info=55834575116, toast_ok=55834575121, toast_danger=55834575126, banner_info=55834574989,
         banner_warn=55834574994, banner_danger=55834575003, chat=55834575045, chat_sel=55834575050,
         chat_run=55834575055, row=55834574922, row_check=55834574926, row_danger=55834574937, empty=55834575144,
         search=55834575073, file=55834575131, tile=55834575032, tile_up=55834575034, tile_fail=55834575037)


def screen(b, name, i, h=860):
    return b.col(None, "Strict · " + name, gap=0, w=400, h=h, fill=BG, cornerRadius=12, stroke=LINE, strokeWeight=1,
                 strokeAlign="inside", clip=True, x=X0 + i * 460, y=Y)


def v(b, parent, key, texts=None, **setp):
    """An instance of a «дополнение» variant; texts maps a child layer's name to its characters."""
    r = b.inst(parent, V[key], None, **setp)
    for child, s in (texts or {}).items():
        b.ov(r, child, characters=s)
    return r


def at(b, ref, x, y):
    b.set(ref, absolute=True, x=x, y=y)
    return ref


def user(b, parent, s):
    return inst(b, parent, "message", {"State": "Sent", "Text": s}, sizingH="fill")


def say(b, parent, s, color=TEXT):
    return text(b, parent, s, 13, color, name="Agent", sizingH="fill", textAutoResize="height")


def steps(b, parent, rows):
    f = b.col(parent, "Steps", gap=0, padding=[6, 4, 6, 4], fill=CARD, cornerRadius=10, sizingH="fill")
    for status, n, a, t in rows:
        inst(b, f, "step", {"Status": status, "Name": n, "Args": a, "Time": t}, sizingH="fill")
    return f


def changed(b, parent, count, rows, undone=False):
    """«Изменено на холсте»: the count on its own line under the title, so the buttons never squeeze it."""
    ch = b.col(parent, "Changed", gap=2, sizingH="fill")
    h = b.row(ch, "Header", gap=6, padding=[0, 0, 4, 0], sizingH="fill")
    text(b, h, "Изменено на холсте", 12, DIM, True)
    text(b, h, count, 12, FAINT, name="Count")
    spacer(b, h)
    if not undone:
        button(b, h, "Показать")
        button(b, h, "Отменить")
    for kind, n, d, k in rows:
        inst(b, ch, "change", {"Kind": kind, "Name": n, "Detail": d, "Id": k}, sizingH="fill")
    return ch


def stats(b, parent, s):
    return text(b, parent, s + "  ›", 12, FAINT, name="Stats")


# ---- screens ----

def broke(b, i):
    """Q: the turn broke on a step: what was done stays, the card says why and continues from that step."""
    s = screen(b, SCREENS[0], i)
    top(b, s, "Кнопка «Войти» с состояниями", "review-ux.figcraft")
    m = body(b, s, gap=14)
    user(b, m, "Сделай «Войти» компонентом с состояниями: обычная, наведение, нажатие, загрузка, недоступна")
    text(b, m, "›  6 из 9 шагов · 1 сообщение", 12, FAINT)
    steps(b, m, [("Done", "component.create", "Button/Войти", "0.6s"), ("Done", "variable.bind", "Hover · accent-hover", "0.3s"),
                 ("Done", "node.set", "Pressed · scale 0.96", "0.2s"), ("Done", "variable.bind", "Disabled · text-faint", "0.3s"),
                 ("Error", "node.set", "Loading", "30s")])
    changed(b, m, "4 варианта", [("Added", "Button/Войти", "компонент", "#5120"), ("Added", "Hover", "вариант", "#5124"),
                                 ("Added", "Pressed", "вариант", "#5127")])
    v(b, m, "banner_danger", {"Title": "Ход прервался на шаге 6 из 9",
                              "Text": "FigCraft не ответил за 30 с — похоже, в нём открыт диалог. Закройте его и продолжите: агент начнёт с «Загрузки» и не повторит сделанное.",
                              "Label": "Продолжить с шага 6", "Button · ghost": "Лог"}, sizingH="fill")
    stats(b, m, "Работал 48 с · $0.06")
    composer(b, s, "Уточнить. @слои. /навыки.")
    return s


def limit(b, i):
    """R: the subscription ran out mid-turn: another agent takes the chat over from the same step."""
    s = screen(b, SCREENS[1], i)
    top(b, s, "Кнопка «Войти» с состояниями", "review-ux.figcraft")
    m = body(b, s, gap=14)
    user(b, m, "Сделай «Войти» компонентом с состояниями: обычная, наведение, нажатие, загрузка, недоступна")
    text(b, m, "›  6 из 9 шагов · 1 сообщение", 12, FAINT)
    say(b, m, "Собрал Button/Войти и четыре варианта из пяти. На «Загрузке» закончился лимит.")
    changed(b, m, "4 варианта", [("Added", "Button/Войти", "компонент", "#5120"), ("Added", "Hover", "вариант", "#5124"),
                                 ("Added", "Pressed", "вариант", "#5127")])
    v(b, m, "banner_warn", {"Title": "Лимит Claude Pro до 18:40",
                            "Text": "Сделано 5 из 9 шагов. Codex получит этот чат и начнёт с варианта «Загрузка».",
                            "Label": "Продолжить в Codex", "Button · ghost": "Другая модель…"}, sizingH="fill")
    stats(b, m, "Работал 1 мин 4 с · $0.09")
    composer(b, s, "Уточнить. @слои. /навыки.")
    return s


def pictures(b, i):
    """S: pictures in a sent message: numbered, so the text and the agent can say «картинка 2»."""
    s = screen(b, SCREENS[2], i)
    top(b, s, "Шапка как на референсе", "review-ux.figcraft")
    m = body(b, s, gap=14)
    u = b.col(m, "User message", gap=6, sizingH="fill", crossAlign="max")
    th = b.row(u, "Thumbs", gap=6)
    for k in range(3):
        t = b.frame(th, f"Picture {k + 1}", None, 64, 64, fill=INSET, cornerRadius=8, stroke=BORDER, strokeWeight=1,
                    strokeAlign="inside", clip=True)
        b.set(t, fills=[{"type": "image", "image": SHOT, "scaleMode": "fill"}])
        n = b.row(t, "Number", gap=0, w=16, h=16, fill=BG, cornerRadius=4, mainAlign="center", sizingH="fixed", sizingV="fixed")
        at(b, n, 4, 44)
        text(b, n, str(k + 1), 10, TEXT, True)
    user(b, u, "Шапка как на картинке 1, список чатов — как на 2. Отступы поля — как на 3")
    text(b, m, "›  7 вызовов · 1 сообщение", 12, FAINT)
    say(b, m, "Шапка как на картинке 1: название чата слева, «Новый» и настройки справа. Список чатов — строками, как на 2. Поле ввода: паддинг 12, радиус 12, как на 3.")
    changed(b, m, "6 слоёв", [("Changed", "Top bar", "A · Пустой чат · раскладка", "#3001"),
                              ("Changed", "Chats menu", "F · Чаты · строки", "#3163"),
                              ("Changed", "Composer", "B · Разговор · паддинг 12", "#3055")])
    stats(b, m, "Работал 52 с · $0.07")
    c = b.col(s, "Composer", gap=8, padding=[0, 12, 12, 12], sizingH="fill")
    hint = b.row(c, "Hint", gap=6, padding=[0, 6, 0, 6], sizingH="fill")
    text(b, hint, "Клик по картинке — просмотр", 11, FAINT, sizingH="fill")
    kbd(b, hint, "⌘V")
    text(b, hint, "вставить картинку", 11, FAINT)
    inst(b, c, "input", {"State": "Empty", "Text": "Уточнить. @слои. /навыки."}, sizingH="fill")
    inst(b, c, "model", {"Model": "Sonnet 5.5", "Effort": "", "Mode": "Только FigCraft", "Show hint": False}, sizingH="fill")
    return s


def review(b, i):
    """T: a remark the agent fixed waits for the designer: what changed, accept or send back; the way back to the chat."""
    s = screen(b, SCREENS[3], i)
    back_top(b, s, "Замечания", "review-ux.figcraft", trail=lambda r: button(b, r, "Исправить все", "Primary"))
    t = b.row(s, "Tabs", gap=4, padding=[8, 12, 8, 12], sizingH="fill")
    for k, (n, c) in enumerate([("Все", "5"), ("Открыто", "2"), ("Вопросы", "1"), ("Проверь", "2")]):
        inst(b, t, "tab", {"State": "Selected" if k == 3 else "Default", "Label": n, "Count": c})
    b.rect(s, "Divider", 10, 1, LINE, sizingH="fill")
    m = b.col(s, "List", gap=2, padding=[4, 8, 8, 8], sizingH="fill", sizingV="fill")
    inst(b, m, "group", {"Tone": "Review", "Label": "Проверь", "Count": "2"}, sizingH="fill")
    c = b.col(m, "#11 · selected", gap=10, padding=10, fill=CARD, cornerRadius=10, sizingH="fill")
    h = b.row(c, "Head", gap=10, sizingH="fill", crossAlign="min")
    glyph(b, h, "✓", GREEN, 13, name="Status")
    tx = b.col(h, "Text", gap=3, sizingH="fill")
    text(b, tx, "Строки агентов одной высоты", 13, TEXT, name="Title", sizingH="fill", textAutoResize="height")
    text(b, tx, "C · Выбор агента / Agents", 12, FAINT, name="Meta")
    text(b, h, "#11", 11, FAINT, name="Id")
    a = b.col(c, "Agent", gap=4, padding=[8, 10, 8, 10], fill=INSET, cornerRadius=6, sizingH="fill")
    text(b, a, "Агент: паддинг 8, высота 36 у четырёх строк", 12, DIM, sizingH="fill", textAutoResize="height")
    code(b, a, "padding   6 → 8      height   32 → 36", DIM)
    r = b.row(c, "Actions", gap=6, sizingH="fill")
    button(b, r, "Показать")
    spacer(b, r)
    button(b, r, "Вернуть…")
    button(b, r, "Принять  A", "Primary")
    inst(b, m, "remark", {"Status": "Review", "Id": "#9", "Title": "Подписи у иконок в шапке", "Meta": "A · Пустой чат / Top bar"},
         sizingH="fill")
    d = b.row(m, "Closed", gap=8, padding=[12, 8, 6, 8], sizingH="fill")
    text(b, d, "›", 12, FAINT)
    text(b, d, "Закрыто", 11, FAINT, True)
    text(b, d, "3", 11, FAINT)
    spacer(b, d)
    text(b, d, "в каждой вкладке", 11, FAINT)
    b.rect(s, "Divider", 10, 1, LINE, sizingH="fill")
    keys(b, s, [("↑↓", "выбрать"), ("A", "принять"), ("R", "вернуть"), ("Esc", "к чату")])
    return s


def notices(b, i):
    """U: what stays (banner under the bar) and what passes (toasts at the top, never over the input)."""
    s = screen(b, SCREENS[4], i)
    top(b, s, "Привести кнопки к токенам", "review-ux.figcraft")
    bw = b.col(s, "Banner", gap=0, padding=[8, 12, 0, 12], sizingH="fill")
    v(b, bw, "banner_info", {"Title": "Агенты работают ещё в 2 файлах",
                             "Text": "Откройте файл в FigCraft, чтобы увидеть чат. Когда закончат — придёт уведомление."}, sizingH="fill")
    m = body(b, s)
    user(b, m, "Кнопки на B и H разные по радиусу и цвету. Приведи к токенам и сделай одним компонентом")
    text(b, m, "›  2 вызова · 1 сообщение", 12, FAINT)
    say(b, m, "Нашёл 7 кнопок: три радиуса (6, 8, 12) и две заливки. Собираю компонент Button на токенах.")
    tw = b.col(s, "Toasts", gap=6, w=376, padding=[0, 0, 8, 0], fill=BG, sizingH="fixed")
    at(b, tw, 12, 124)
    for key, tx in [("toast_ok", {"Text": "tabka-ui: готово · 4 шага", "Action": "Открыть файл"}),
                    ("toast_info", {"Text": "Чат «Пустые состояния» удалён", "Action": "Вернуть"}),
                    ("toast_danger", {"Text": "screen-12.png не загрузился", "Action": "Повторить"})]:
        v(b, tw, key, tx, sizingH="fill", stroke=BORDER, strokeWeight=1, strokeAlign="inside", effects=SHADOW)
    composer(b, s, HINT)
    return s


def chat_actions(b, i):
    """V: a chat's actions sit behind ⋯, so a click near the row never deletes; deleting is undone from a toast."""
    s = screen(b, SCREENS[5], i)
    top(b, s, "Привести кнопки к токенам", "review-ux.figcraft")
    body(b, s)
    composer(b, s, HINT)
    m = menu(b, s, "Chats menu", y=54)
    item(b, m, "Замечания", "2 открыто · 1 ждёт ответа", lead=lambda r: b.rect(r, "Dot", 8, 8, MAUVE, cornerRadius=2),
         trail=lambda r: text(b, r, "›", 13, FAINT, name="Chevron"), two=True)
    divider(b, m, 4)
    label(b, m, "Чаты файла", right="3")
    v(b, m, "chat_sel", {"Title": "Привести кнопки к токенам", "Meta": "сейчас · Sonnet 5.5"}, sizingH="fill")
    v(b, m, "chat_run", {"Title": "Стиль чата как у Orca", "Meta": "работает · 2 мин · Opus 5.5"}, sizingH="fill")
    v(b, m, "chat", {"Title": "Пустые состояния списка", "Meta": "вчера · GPT-5.5"}, sizingH="fill")
    keys(b, m, [("↑↓", "выбрать"), ("↵", "открыть")], right=lambda f: button(b, f, "+ Новый чат", "Primary"))
    p = menu(b, s, "Chat actions", x=196, y=242, w=196)
    v(b, p, "row", {"Label": "Переименовать", "Meta": "F2"}, sizingH="fill")
    v(b, p, "row", {"Label": "Копировать как Markdown", "Meta": ""}, sizingH="fill")
    divider(b, p, 4)
    v(b, p, "row_danger", {"Label": "Удалить чат", "Meta": "⌫"}, sizingH="fill")
    return s


def clear(b, i):
    """W: «Очистить» asks in its own row, with the count, instead of a system dialog."""
    s = screen(b, SCREENS[6], i)
    back_top(b, s, "Настройки", "для всех файлов")
    m = body(b, s, gap=8, padding=(8, 12, 16, 12))
    label(b, m, "Агенты")
    c = card(b, m, "Agents")
    for mark, color, n, d, trail in [(CLAUDE, ORANGE, "Claude Code", "2.1.12 · ~/.claude", "4 модели"),
                                     ("X", GREEN, "Codex", "0.44.0 · ~/.local/bin/codex", "3 модели")]:
        item(b, c, n, d, mark, color, trail=lambda r, t=trail: text(b, r, t, 12, FAINT, name="Count"), two=True)
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
    c = b.col(m, "Chats · confirm", gap=10, padding=[10, 12, 10, 12], fill=CARD, stroke=RED, strokeWeight=1,
              strokeAlign="inside", cornerRadius=10, sizingH="fill")
    text(b, c, "Удалить 3 чата файла review-ux.figcraft?", 13, TEXT, name="Question")
    text(b, c, "Вместе с историей сообщений. Правки на холсте останутся.", 12, FAINT, sizingH="fill", textAutoResize="height")
    a = b.row(c, "Actions", gap=6, sizingH="fill")
    spacer(b, a)
    button(b, a, "Отмена")
    r = b.row(a, "Delete", gap=0, padding=[4, 10, 4, 10], fill=RED, cornerRadius=6)
    text(b, r, "Удалить 3 чата", 12, BG, True)
    text(b, m, "Агенты работают через свои CLI и ваши подписки — ключи не нужны. Чат продолжает сессию агента.",
         11, FAINT, name="Foot", sizingH="fill", textAutoResize="height")
    return s


def queue(b, i):
    """X: while the agent works, ↵ and the round button queue the message; stopping is its own control."""
    s = screen(b, SCREENS[7], i)
    top(b, s, "Привести кнопки к токенам", "review-ux.figcraft")
    m = body(b, s)
    user(b, m, "Кнопки на B и H разные по радиусу и цвету. Приведи к токенам и сделай одним компонентом")
    text(b, m, "›  2 вызова · 1 сообщение", 12, FAINT)
    say(b, m, "Нашёл 7 кнопок: три радиуса (6, 8, 12) и две заливки. Собираю компонент Button на токенах.")
    steps(b, m, [("Done", "component.create", "Button", "0.4s"), ("Done", "variable.bind", "fill, cornerRadius · 4", "0.3s"),
                 ("Running", "instance.create", "3 из 7", "0:06")])
    inst(b, m, "message", {"State": "Queued", "Text": "и на экране C тоже", "Note": "в очереди · после этого ответа · убрать"},
         sizingH="fill")
    c = b.col(s, "Composer", gap=8, padding=[0, 12, 12, 12], sizingH="fill")
    run_ = b.row(c, "Running", gap=8, padding=[0, 6, 0, 6], sizingH="fill")
    b.ellipse(run_, "Spinner", 10, "none", stroke=ACCENT, strokeWeight=1.5)
    text(b, run_, "Работает · 0:42", 11, DIM, name="Status", sizingH="fill")
    st = b.row(run_, "Stop", gap=6, padding=[2, 8, 2, 6], fill=SURFACE, cornerRadius=6)
    b.rect(st, "Square", 8, 8, TEXT, cornerRadius=1)
    text(b, st, "Остановить", 11, TEXT)
    kbd(b, st, "Esc Esc")
    inst(b, c, "input", {"State": "Filled", "Text": "и кнопку «Отмена» тоже", "Hint": "↵ в очередь"}, sizingH="fill")
    inst(b, c, "model", {"Model": "Sonnet 5.5", "Effort": "", "Mode": "Только FigCraft", "Show hint": False}, sizingH="fill")
    return s


MODES = {"auto": ("Сам", GREEN), "manual": ("Вручную", DIM), "always": ("Всегда", TEXT)}


def mode(b, i):
    """Y: a skill's mode is a small menu in the panel's style, with what each mode means."""
    s = screen(b, SCREENS[8], i)
    back_top(b, s, "Навыки", "для всех файлов · 58", trail=lambda r: button(b, r, "?"))
    m = body(b, s, gap=6, padding=(12, 12, 12, 12))
    v(b, m, "search", {"Placeholder": "Найти навык…", "Count": "58"}, sizingH="fill")
    tabs = b.row(m, "Groups", gap=4, padding=[4, 0, 4, 0], sizingH="fill", wrap=True)
    for k, (n, c) in enumerate([("Все", "58"), ("Основа", "1"), ("Стиль", "50"), ("Качество", "6"), ("Задачи", "2")]):
        inst(b, tabs, "tab", {"State": "Selected" if k == 0 else "Default", "Label": n, "Count": c})
    for g, color, note, rows in [
        ("Основа", ACCENT, "всегда в каждом ходе", [("figcraft-design", "работа с FigCraft, токены, проверка", "always")]),
        ("Стиль", MAUVE, "один на чат", [("Almanac", "редакционный, сдержанный акцент", "manual"),
                                         ("Arcade", "игривый, тёмный, полная палитра", "manual")]),
        ("Качество", GREEN, None, [("better-accessibility", "фокус, клавиатура, контраст", "auto"),
                                   ("better-layout", "группы, выравнивание, адаптив", "auto")])]:
        label(b, m, g, note, dot=color)
        c = card(b, m, g)
        for n, d, md in rows:
            t, tc = MODES[md]
            item(b, c, n, d, trail=lambda r, t=t, tc=tc: text(b, r, t + "  ⌄", 12, tc, name="Mode"),
                 state="hover" if n == "better-accessibility" else None)
    f = b.row(s, "Footer", gap=8, padding=[10, 16, 12, 16], sizingH="fill")
    spacer(b, f)
    button(b, f, "+ Добавить навык")
    p = menu(b, s, "Mode menu", x=176, y=412, w=212)
    head(b, p, "better-accessibility")
    for n, d, on in [("Сам", "агент берёт по описанию", True), ("Вручную", "через / или закрепить", False),
                     ("Всегда", "с каждым сообщением", False)]:
        item(b, p, n, d, trail=(lambda r: text(b, r, "✓", 12, TEXT, True, name="Check")) if on else None,
             state="selected" if on else None, two=True)
    return s


def help_(b, i):
    """Z: the library's «?»: modes, groups, sources and the SKILL.md header, in the panel's own type."""
    s = screen(b, SCREENS[9], i)
    back_top(b, s, "Как работают навыки", "библиотека")
    m = body(b, s, gap=14, padding=(14, 16, 16, 16))
    for t, p in [("Четыре режима", "Всегда — с каждым сообщением. В чате — закреплён над полем. В сообщении — чип через / на один ход, Tab закрепляет в чате. Сам — агент берёт по описанию."),
                 ("Группы", "Основа, Стиль, Дизайн-система, Платформа, Качество, Задачи, Другие. Стиль и дизайн-система — по одному на чат: второй заменяет первый."),
                 ("Источники", "Проект — .figcraft/skills, мои — ~/.config/figcraft-agent/skills, встроенные, pen.dev (только чтение). При одинаковом имени побеждает первый.")]:
        sec = b.col(m, t, gap=4, sizingH="fill")
        text(b, sec, t, 12, TEXT, True)
        text(b, sec, p, 12, DIM, sizingH="fill", textAutoResize="height")
    sec = b.col(m, "SKILL.md", gap=6, sizingH="fill")
    text(b, sec, "Новый навык — папка с SKILL.md", 12, TEXT, True)
    cb = b.col(sec, "Code", gap=2, padding=[10, 12, 10, 12], fill=INSET, cornerRadius=6, sizingH="fill")
    for ln in ["---", "name: style-graphite", "description: Тихий рабочий инструмент", "metadata:", "  group: style",
               "  title: Graphite", "  summary: Серые поверхности, один акцент", "  mode: manual", "---"]:
        code(b, cb, ln, DIM)
    text(b, sec, "Без metadata навык попадёт в «Другие» с режимом «Сам». Новые папки появляются без перезапуска.", 11, FAINT,
         sizingH="fill", textAutoResize="height")
    f = b.row(s, "Footer", gap=8, padding=[10, 16, 12, 16], sizingH="fill")
    spacer(b, f)
    button(b, f, "+ Добавить навык")
    return s


def add(b, i):
    """AA: import a skill folder: one field, its error in place, and the manual way."""
    s = screen(b, SCREENS[10], i)
    back_top(b, s, "Добавить навык", "в мои навыки")
    m = body(b, s, gap=12, padding=(14, 16, 16, 16))
    text(b, m, "Папка со SKILL.md на этом компьютере. Её скопируют в мои навыки; папки с тем же именем останутся.", 12, DIM,
         sizingH="fill", textAutoResize="height")
    f = b.col(m, "Field", gap=6, sizingH="fill")
    text(b, f, "Путь к папке", 11, FAINT, True)
    inp = b.row(f, "Input", gap=8, padding=[8, 10, 8, 10], fill=INSET, stroke=RED, strokeWeight=1, strokeAlign="inside",
                cornerRadius=6, sizingH="fill")
    code(b, inp, "~/Projects/my-skill", TEXT)
    spacer(b, inp)
    glyph(b, inp, "\U000f024b", FAINT, 13, name="Browse")
    text(b, f, "В папке нет SKILL.md", 11, RED, name="Error")
    r = b.row(m, "Actions", gap=6, sizingH="fill")
    spacer(b, r)
    button(b, r, "Отмена")
    button(b, r, "Добавить", "Primary")
    divider(b, m)
    sec = b.col(m, "Manual", gap=4, sizingH="fill")
    text(b, sec, "Или положите папку сами", 12, TEXT, True)
    text(b, sec, "В ~/.config/figcraft-agent/skills или в .figcraft/skills проекта — навык появится в библиотеке сразу.", 12,
         DIM, sizingH="fill", textAutoResize="height")
    return s


def empty(b, i):
    """AB: what the panel says when there is nothing to show or FigCraft is out of reach."""
    s = b.col(None, "Strict · " + SCREENS[11], gap=18, padding=[16, 12, 16, 12], w=400, fill=BG, cornerRadius=12,
              stroke=LINE, strokeWeight=1, strokeAlign="inside", x=X0 + i * 460, y=Y)
    text(b, s, "Пустые состояния и ошибки", 13, TEXT)

    def part(name, caption):
        p = b.col(s, name, gap=6, sizingH="fill")
        text(b, p, caption, 11, FAINT)
        return p

    p = part("1 · Нет чатов", "Меню чатов у нового файла — без «Чаты файла 0»")
    mm = b.col(p, "Chats menu", gap=0, padding=4, fill=CARD, stroke=BORDER, strokeWeight=1, strokeAlign="inside",
               cornerRadius=12, sizingH="fill")
    item(b, mm, "Замечания", "нет открытых", lead=lambda r: b.rect(r, "Dot", 8, 8, FAINT, cornerRadius=2),
         trail=lambda r: text(b, r, "›", 13, FAINT, name="Chevron"), two=True)
    divider(b, mm, 4)
    v(b, mm, "empty", {"Title": "Чатов пока нет", "Hint": "Опишите задачу в поле ниже — чат появится здесь.",
                           "Label": "+ Новый чат"}, sizingH="fill")
    p = part("2 · Поиск без результатов", "@, / и библиотека — одинаково")
    v(b, p, "search", {"Placeholder": "kanban", "Count": "0"}, sizingH="fill")
    v(b, p, "empty", {"Title": "Ничего не нашлось", "Hint": "Попробуйте другое слово или добавьте навык из папки.",
                      "Label": "Добавить навык"}, sizingH="fill")
    p = part("3 · FigCraft не отвечает", "Над чатом, пока окно не ответит; агенты ждут")
    v(b, p, "banner_danger", {"Title": "FigCraft не отвечает",
                              "Text": "Окно свёрнуто, на другом рабочем столе или запущено без --control 7979.",
                              "Label": "Проверить снова", "Button · ghost": "Как запустить"}, sizingH="fill")
    p = part("4 · Файл не сохранён", "Чаты привязаны к файлу на диске")
    v(b, p, "banner_warn", {"Title": "Сохраните файл",
                            "Text": "Чаты хранятся рядом с файлом — у несохранённого их негде держать.",
                            "Label": "Сохранить  ⌘S", "Button · ghost": ""}, sizingH="fill")
    p = part("5 · Агент не найден", "В меню модели вместо списка моделей")
    c = card(b, p, "Agent missing")
    item(b, c, "Codex", "не найден в PATH", "X", FAINT, trail=lambda r: button(b, r, "Как установить"), two=True)
    return s


BUILD = [broke, limit, pictures, review, notices, chat_actions, clear, queue, mode, help_, add, empty]


def main():
    fc = FC()
    old = [t["id"] for t in fc.tops() if t["name"].removeprefix("Strict · ") in SCREENS]
    if old:
        fc.cmd("edit.delete", ids=old)
    b = B()
    frames = [fn(b, i) for i, fn in enumerate(BUILD)]
    res = run(fc, b, "Strict Q–AB")
    ids = [res[f["$step"]]["id"] for f in frames]
    fc.cmd("variable.setMode", ids=ids, collection="Tokens", mode="Graphite")
    print(ids)


if __name__ == "__main__":
    main()
