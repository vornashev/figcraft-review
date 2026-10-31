#!/usr/bin/env python3
"""Add four editable source-filter proposals to the Agent page; leave the app code unchanged."""
import json
from pathlib import Path
from skill_browser_variants import Tokens, screen
from strict import (FC, BG, CARD, BORDER, TEXT, DIM, FAINT, ACCENT, SURFACE,
                    ICON_IDS, button as base_button, divider, inst, kbd, run, spacer, text)

NAME = "Strict · Источники — компактные варианты A–D"
ROOT = Path(__file__).resolve().parent.parent
ORIGINS = [("OpenDesign", 230), ("Hallmark", 51), ("TypeUI", 67), ("tweakcn", 42),
           ("UI UX Pro Max", 79), ("Встроенные", 7), ("pen.dev", 3)]
ON = {"Hallmark", "TypeUI"}
NAMES = {"A": "Кнопка со списком", "B": "Два чипса + ещё", "C": "Иконка со счётчиком", "D": "Чипсы в одну строку"}


def button(b, parent, label, **props):
    return base_button(b, parent, label, "Ghost", height=28, sizingV="fixed", **props)


def pill(b, parent, label, count=None, chevron=False, active=True, icon=False):
    r = b.row(parent, label, gap=6, h=28, sizingV="fixed", padding=[0, 8, 0, 8],
              fill=SURFACE if active else "none", stroke=ACCENT if active else BORDER, strokeWeight=1, cornerRadius=6)
    if icon:
        b.inst(r, ICON_IDS["puzzle"], width=14, height=14)
    text(b, r, label, 12, TEXT if active else DIM)
    if count is not None:
        text(b, r, str(count), 11, ACCENT if active else FAINT)
    if chevron:
        b.inst(r, ICON_IDS["chevron"], width=12, height=12)
    return r


def view_switch(b, parent, small=False):
    row = b.row(parent, "Режимы отображения", gap=2, h=28, padding=2, fill=BG, cornerRadius=6, stroke=BORDER, strokeWeight=1)
    for label in ("Список", "Сетка", "Просмотр"):
        c = b.row(row, label, gap=0, padding=[3, 6, 3, 6], fill=SURFACE if label == "Просмотр" else "none", cornerRadius=4)
        text(b, c, label, 10 if small else 11, TEXT if label == "Просмотр" else DIM, label == "Просмотр")


def source_control(b, parent, variant, narrow=False, state="partial", scrolled=False):
    if variant == "A":
        return pill(b, parent, "Источники", "Все 7" if state == "all" else "0/7" if state == "none" else "2/7", True, state != "all", True)
    if variant == "B":
        r = b.row(parent, "Выбранные источники", gap=6)
        if state == "all":
            pill(b, r, "Все источники", 7, True, False)
        elif state == "none":
            pill(b, r, "Источники", "0/7", True)
        else:
            pill(b, r, "Hallmark ×"); pill(b, r, "TypeUI ×"); pill(b, r, "+5", chevron=True, active=False)
        return r
    if variant == "C":
        r = b.row(parent, "Источники · кнопка и счётчик", gap=4, h=28, padding=[0, 7, 0, 7], fill=SURFACE,
                  stroke=ACCENT if state != "all" else BORDER, strokeWeight=1, cornerRadius=6)
        b.inst(r, ICON_IDS["puzzle"], width=16, height=16)
        text(b, r, "7" if state == "all" else "0" if state == "none" else "2", 11, ACCENT)
        return r
    outer = b.row(parent, "Источники · одна строка без переноса", gap=6, sizingH="fill", h=28)
    clip = b.row(outer, "Горизонтальная прокрутка", gap=0, h=28, sizingH="fill", clip=True)
    track = b.row(clip, "Лента чипсов", gap=6, h=28)
    items = ORIGINS[3:] if scrolled else [("Все", 479)] + ORIGINS
    for label, _ in items:
        pill(b, track, ("✓ " if label in ON else "") + label, active=label in ON)
    button(b, outer, "‹" if scrolled else "›")
    return outer


def header(b, parent, variant, narrow=False, scrolled=False):
    top = b.row(parent, "Шапка", gap=8, h=44, padding=[0, 12, 0, 12], sizingH="fill")
    text(b, top, "Навыки к сообщению", 12, TEXT, True)
    spacer(b, top)
    if not narrow:
        if variant in ("A", "C"):
            source_control(b, top, variant)
        view_switch(b, top)
    if narrow:
        controls = b.row(parent, "Управление на узкой панели", gap=8, padding=[0, 12, 8, 12], sizingH="fill")
        if variant in ("A", "C"):
            source_control(b, controls, variant, True)
        spacer(b, controls); view_switch(b, controls, True)
    tabs = b.row(parent, "Типы навыков", gap=4, padding=[0, 8, 8, 8], sizingH="fill", wrap=True)
    for label, count in [("Все", "118"), ("Недавние", "0"), ("Избранное", "0"), ("Темы", "117"), ("Общие", "1")]:
        inst(b, tabs, "tab", {"Label": label, "Count": count, "State": "Selected" if label == "Все" else "Default"})
    if variant in ("B", "D"):
        r = b.row(parent, "Компактный фильтр источников", gap=8, padding=[0, 12, 8, 12], sizingH="fill")
        if not narrow:
            text(b, r, "Источники", 11, FAINT)
        source_control(b, r, variant, narrow, scrolled=scrolled)


def reference(b, parent, width, height):
    r = b.rect(parent, "Оригинальное превью TypeUI · Editorial", width, height, CARD, cornerRadius=6)
    b.add("image.place", {"path": str(ROOT / "skills/skills/typeui-editorial/assets/preview.webp"), "target": r, "mode": "fit"})


def skill_row(b, parent, name, source, active=False):
    row = b.col(parent, name, gap=3, padding=8, fill=SURFACE if active else "none", cornerRadius=6, sizingH="fill")
    instance = inst(b, row, "skill", {"Control": "Checkbox", "Checked": "On" if active else "Off", "State": "Default",
                                      "Name": name, "Description": "", "Hint": ""}, sizingH="fill", height=26)
    b.ov(instance, "Description", visible=False); b.ov(instance, "Hint", visible=False)
    b.ov(instance, "Name", sizingH="fill", textAutoResize="height")
    text(b, row, source, 11, FAINT)


def content(b, parent, narrow=False):
    if narrow:
        area = b.col(parent, "Контент на узкой панели", gap=10, padding=[4, 12, 12, 12], sizingH="fill", sizingV="fill")
        reference(b, area, 374, 210)
        text(b, area, "Editorial", 18, TEXT, True)
        text(b, area, "TypeUI · редакционная типографика и сетка", 11, DIM, sizingH="fill", textAutoResize="height")
        divider(b, area)
        for label, source in [("Editorial", "TypeUI"), ("Editorial", "Hallmark"), ("Enterprise", "TypeUI")]:
            skill_row(b, area, label, source, source == "TypeUI" and label == "Editorial")
        return
    body = b.row(parent, "Список и крупное превью", gap=0, sizingH="fill", sizingV="fill", crossAlign="min")
    left = b.col(body, "Навыки", gap=4, w=260, padding=[4, 8, 8, 8], sizingV="fill")
    for name, source in [("Editorial", "TypeUI"), ("Editorial", "Hallmark"), ("Enterprise", "TypeUI"), ("Expressive", "TypeUI")]:
        skill_row(b, left, name, source, name == "Editorial" and source == "TypeUI")
    right = b.col(body, "Крупный просмотр", gap=8, padding=12, fill=CARD, sizingH="fill", sizingV="fill")
    reference(b, right, 554, 252)
    text(b, right, "Editorial", 18, TEXT, True)
    text(b, right, "TypeUI · журнальная сетка, антиква, спокойная иерархия", 12, DIM, sizingH="fill", textAutoResize="height")


def footer(b, parent):
    divider(b, parent)
    row = b.row(parent, "Клавиатура и действия", gap=6, h=40, padding=[0, 12, 0, 12], sizingH="fill")
    kbd(b, row, "↑↓"); text(b, row, "навык", 11, FAINT)
    kbd(b, row, "Space"); text(b, row, "выбрать", 11, FAINT)
    spacer(b, row); button(b, row, "Все навыки ›")


def popup(b, screen_ref, variant):
    # On a 400px panel, anchor the popup to its compact control. It overlays content, not layout.
    x, y = (12, 80) if variant == "A" else (12, 140) if variant == "B" else (60, 80)
    p = b.col(screen_ref, "Источники · раскрытый список", gap=0, w=328, padding=4, fill=CARD,
              stroke=BORDER, strokeWeight=1, cornerRadius=8,
              effects=[{"type": "dropShadow", "color": "#00000066", "offset": [0, 8], "radius": 20}])
    b.set(p, absolute=True, x=x, y=y)
    top = b.row(p, "Заголовок списка", gap=8, padding=8, sizingH="fill")
    text(b, top, "Источники", 13, TEXT, True); spacer(b, top); text(b, top, "2 из 7", 11, ACCENT)
    for name, count in ORIGINS:
        r = inst(b, p, "skill", {"Control": "Checkbox", "Checked": "On" if name in ON else "Off", "State": "Default",
                                  "Name": name, "Description": "", "Hint": str(count)}, sizingH="fill", height=30)
        b.ov(r, "Description", visible=False)
        b.ov(r, "Hint", visible=True)
        b.ov(r, "Name", sizingH="fill", textAutoResize="height")
    divider(b, p)
    actions = b.row(p, "Все / ни одного", gap=8, padding=4, sizingH="fill")
    button(b, actions, "Все"); button(b, actions, "Ни одного"); spacer(b, actions); button(b, actions, "Готово")
    text(b, p, "Изменения сохраняются сразу", 11, FAINT, sizingH="fill", textAutoResize="height")


def panel(b, parent, variant, narrow=False, opened=False):
    name = f"{variant} · " + ("400 px · выбор источников" if opened else "400 px · закрыто" if narrow else "840 px · компактный фильтр")
    s = screen(b, parent, name, w=400 if narrow else 840, h=660 if narrow else 520)
    header(b, s, variant, narrow, scrolled=opened and variant == "D")
    content(b, s, narrow); footer(b, s)
    if opened and variant != "D":
        popup(b, s, variant)
    return s


def main():
    fc = FC()
    try:
        doc = fc.doc(0)
        if Path(doc.get("path", "")).resolve() != ROOT / "design/review-ux.figcraft":
            raise SystemExit("Open FigCraft Review — UX before building these variants")
        if any(n["name"] == NAME for n in fc.tops()):
            raise SystemExit("Board already exists; inspect and edit it rather than duplicate")
        b = Tokens()
        board = b.col(None, NAME, gap=20, padding=20, w=3460, fill=BG, x=0, y=15520)
        text(b, board, "Компактные источники · четыре варианта", 22, TEXT, True)
        text(b, board, "Одинаковые данные: Hallmark + TypeUI · 2 из 7 источников · 118 навыков. Сравниваем закрытое состояние, выбор и панель 400 px.", 13, DIM)
        row = b.row(board, "Четыре подхода", gap=20, sizingH="fill", crossAlign="min")
        captions = {
            "A": ("Рекомендую: фильтр рядом с режимом, без отдельной строки. Названия источников — в списке с чекбоксами.", "Самый понятный баланс: одна кнопка, явный счётчик, полный выбор по нажатию."),
            "B": ("Показываем только два включённых источника. Остальные пять — в «+5». Чипс можно выключить через ×.", "Имена остаются на виду. При большом выборе шапка всё равно занимает только одну строку."),
            "C": ("Иконка плагина и число включённых источников. По наведению: «Источники: Hallmark, TypeUI».", "Минимум места. Но назначение менее заметно: нужен хороший ховер и состояние активного фильтра."),
            "D": ("Сохраняем прямые переключатели: убираем счётчики, запрещаем перенос, узкий ряд можно прокрутить.", "Не нужно открывать список. Занимает 28 px по высоте; часть источников скрыта на узкой панели."),
        }
        frames = []
        for variant in "ABCD":
            col = b.col(row, f"{variant} · {NAMES[variant]}", gap=12, w=840)
            text(b, col, f"{variant} · {NAMES[variant]}" + (" — рекомендую" if variant == "A" else ""), 18, TEXT, True)
            text(b, col, captions[variant][0], 12, DIM, sizingH="fill", textAutoResize="height")
            frames.append(panel(b, col, variant))
            text(b, col, "Узкая панель · закрыто / " + ("прокручено" if variant == "D" else "открыт выбор"), 13, TEXT, True)
            states = b.row(col, "Два состояния в 400 px", gap=20, crossAlign="min", sizingH="fill")
            frames.append(panel(b, states, variant, True)); frames.append(panel(b, states, variant, True, True))
            note = b.col(col, "Комментарий к варианту", gap=6, padding=12, fill=CARD, cornerRadius=8, sizingH="fill")
            text(b, note, captions[variant][1], 13, DIM, sizingH="fill", textAutoResize="height")
            text(b, note, "Выбор сохраняется · можно включить несколько или выключить все · Esc закрывает выбор", 11, FAINT, sizingH="fill", textAutoResize="height")
        state_row = b.row(board, "Компактный индикатор · состояния A", gap=12, padding=12, fill=CARD, cornerRadius=8, sizingH="fill")
        text(b, state_row, "A · Все / часть / ни одного", 13, TEXT, True)
        for state in ("all", "partial", "none"):
            source_control(b, state_row, "A", state=state)
        text(b, state_row, "При нуле источников — пустое состояние и «Включить все». Без сброса выбранных навыков.", 12, DIM)
        result = run(fc, b, "Навыки · компактные источники A–D")
        board_id = result[board["$step"]]["id"]
        ids = [result[frame["$step"]]["id"] for frame in frames]
        fc.cmd("variable.setMode", ids=[board_id], collection="Tokens", mode="Graphite")
        fc.tool("save_file", {})
        for index, ident in enumerate(ids):
            fc.shot(ident, f"/tmp/figcraft-source-option-{index + 1}.png", max_size=1000)
        fc.shot(board_id, "/tmp/figcraft-source-options-board.png", max_size=2600)
        fc.cmd("view.set", zoom=0.34, cx=1730, cy=16250)
        output = {"board": board_id, "frames": ids}
        Path('/tmp/figcraft-source-option-ids.json').write_text(json.dumps(output))
        print(json.dumps(output))
    finally:
        fc.p.terminate()


if __name__ == "__main__":
    main()
