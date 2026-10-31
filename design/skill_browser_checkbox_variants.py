#!/usr/bin/env python3
"""Two checkbox variants of B, including explicit 400px preview states. Additive canvas work only."""
import json
from pathlib import Path
from skill_browser_variants import Tokens, SKILLS, image, screen
from strict import FC, BG, CARD, BORDER, TEXT, DIM, FAINT, ACCENT, HOVER, SURFACE, button as base_button, divider, inst, kbd, run, spacer, text

NAME = "Strict · Навыки — выбор и предпросмотр B1–B2"
SELECTED = {0, 2}


def button(b, parent, label, variant="Ghost", **props):
    props.setdefault("height", 28)
    props.setdefault("sizingV", "fixed")
    return base_button(b, parent, label, variant, **props)


def top(b, parent, detail=False):
    row = b.row(parent, "Шапка", gap=8, h=48, padding=[0, 12, 0, 12], sizingH="fill")
    if detail:
        button(b, row, "‹ К навыкам")
        text(b, row, "Предпросмотр", 13, TEXT, True, sizingH="fill", textAutoResize="height")
    else:
        text(b, row, "Навыки к сообщению", 13, TEXT, True)
        spacer(b, row)
    text(b, row, "2 выбрано", 12, ACCENT)
    if not detail:
        button(b, row, "Закрыть")


def filters(b, parent, narrow=False):
    col = b.col(parent, "Поиск и фильтры", gap=8, padding=[0, 12, 12, 12], sizingH="fill")
    search = b.row(col, "Поиск", gap=8, padding=[8, 10, 8, 10], fill=SURFACE, cornerRadius=6, sizingH="fill")
    text(b, search, "Найти навык…", 12, FAINT)
    row = b.row(col, "Фильтры", gap=4, sizingH="fill", wrap=True)
    values = [("Все", "291"), ("Недавние", "6"), ("Избранное", "3"), ("Сайты", "67"), ("Приложения", "71")]
    for label, count in values:
        inst(b, row, "tab", {"Label": label, "Count": count, "State": "Selected" if label == "Сайты" else "Default"})


def checkbox_row(b, parent, index, active=False):
    """Use the file's Checkbox Skill row; selection is separate from the preview highlight."""
    name = SKILLS[index][0]
    r = inst(b, parent, "skill", {"Control": "Checkbox", "Checked": "On" if index in SELECTED else "Off", "State": "Default",
        "Name": name, "Description": "", "Hint": ""}, sizingH="fill", height=30)
    b.ov(r, "Description", visible=False)
    b.ov(r, "Hint", visible=False)
    b.ov(r, "Name", sizingH="fill", textAutoResize="height")
    return r


def footer(b, parent, narrow=False):
    divider(b, parent)
    chosen = b.col(parent, "Выбранные навыки", gap=4, padding=[10, 12, 6, 12], sizingH="fill")
    text(b, chosen, "Выбраны: Creative Studio Portfolio · Annual Report Microsite", 11, DIM, sizingH="fill", textAutoResize="height")
    row = b.row(parent, "Действия", gap=8, h=46, padding=[0, 12, 0, 12], sizingH="fill")
    kbd(b, row, "Space"); text(b, row, "выбрать", 11, FAINT)
    if not narrow:
        kbd(b, row, "↑↓"); text(b, row, "предпросмотр", 11, FAINT)
    spacer(b, row)
    button(b, row, "Добавить 2 навыка", "Primary")


def preview(b, parent, width, narrow=False, checked=False):
    text(b, parent, SKILLS[0][0], 18, TEXT, True, sizingH="fill", textAutoResize="height")
    text(b, parent, "OpenDesign · Сайты · Editorial", 11, DIM)
    image(b, parent, SKILLS[0][1], width, round(width * 2 / 3))
    text(b, parent, "Портфолио студии: три проекта, выразительная типографика, изображения и подписи в единой иерархии.", 13, DIM, sizingH="fill", textAutoResize="height")
    if checked:
        checkbox_row(b, parent, 0)
        text(b, parent, "Выбран для сообщения", 11, ACCENT)
    row = b.row(parent, "Референс и избранное", gap=4, sizingH="fill")
    button(b, row, "Увеличить")
    button(b, row, "В избранное")
    text(b, parent, "Просмотр не меняет выбранные навыки", 11, FAINT, sizingH="fill", textAutoResize="height")


def compact_item(b, parent, index, opened=False, inline=False):
    card = b.col(parent, SKILLS[index][0], gap=4, padding=8, fill=HOVER if opened else "none", cornerRadius=6, sizingH="fill")
    checkbox_row(b, card, index, opened)
    text(b, card, "OpenDesign · " + SKILLS[index][2], 11, DIM, sizingH="fill", textAutoResize="height")
    if opened:
        row = b.row(card, "Открытый предпросмотр", gap=6, sizingH="fill")
        text(b, row, "Предпросмотр" if inline else "Открыт справа", 11, ACCENT)
        if inline:
            spacer(b, row)
            button(b, row, "Свернуть")
    if opened and inline:
        image(b, card, SKILLS[index][1], 358, 238)
        row = b.row(card, "Действия референса", gap=4, sizingH="fill")
        button(b, row, "Увеличить")
        button(b, row, "В избранное")
    return card


def rich_item(b, parent, index, active=False, narrow=False):
    card = b.col(parent, SKILLS[index][0], gap=6, padding=8, fill=CARD, cornerRadius=8, stroke=ACCENT if active else BORDER, strokeWeight=1, sizingH="fill")
    checkbox_row(b, card, index)
    row = b.row(card, "Изображение и описание", gap=10, sizingH="fill", crossAlign="min")
    image(b, row, SKILLS[index][1], 96 if narrow else 88, 64 if narrow else 59)
    info = b.col(row, "Сведения", gap=4, sizingH="fill")
    text(b, info, "OpenDesign · " + SKILLS[index][2], 11, DIM, sizingH="fill", textAutoResize="height")
    button(b, info, "Смотреть →")
    return card


def wide(b, parent, variant):
    s = screen(b, parent, "B1 · Чекбоксы и постоянное превью" if variant == 1 else "B2 · Карточки с выбором и просмотром", h=860)
    top(b, s); filters(b, s)
    body = b.row(s, "Список и предпросмотр", gap=0, sizingH="fill", sizingV="fill", crossAlign="min")
    left_width = 286 if variant == 1 else 332
    left = b.col(body, "Список навыков", gap=6, padding=[8, 8, 12, 8], w=left_width, sizingV="fill")
    for i in range(4):
        if variant == 1:
            compact_item(b, left, i, i == 0)
        else:
            rich_item(b, left, i, i == 0)
    text(b, left, "4 из 67 · остальные при прокрутке", 11, FAINT, sizingH="fill", textAutoResize="height")
    right = b.col(body, "Крупный предпросмотр", gap=12, padding=16, fill=CARD, sizingH="fill", sizingV="fill")
    preview(b, right, 520 if variant == 1 else 474)
    footer(b, s)
    return s


def narrow_inline(b, parent):
    s = screen(b, parent, "B1 · 400 px · превью под строкой", w=400, h=900)
    top(b, s); filters(b, s, True)
    body = b.col(s, "Единый список с раскрытым превью", gap=6, padding=[4, 12, 12, 12], sizingH="fill", sizingV="fill")
    for i in range(4):
        compact_item(b, body, i, opened=i == 0, inline=i == 0)
    footer(b, s, True)
    return s


def narrow_cards(b, parent):
    s = screen(b, parent, "B2 · 400 px · список перед просмотром", w=400, h=900)
    top(b, s); filters(b, s, True)
    body = b.col(s, "Навыки с миниатюрами", gap=8, padding=[4, 12, 12, 12], sizingH="fill", sizingV="fill")
    for i in range(4):
        rich_item(b, body, i, active=i == 0, narrow=True)
    text(b, body, "«Смотреть» открывает референс. Чекбокс выбирает навык.", 11, FAINT, sizingH="fill", textAutoResize="height")
    footer(b, s, True)
    return s


def narrow_focus(b, parent):
    s = screen(b, parent, "B2 · 400 px · экран предпросмотра", w=400, h=900)
    top(b, s, True)
    body = b.col(s, "Полноразмерный предпросмотр в панели", gap=12, padding=[12, 16, 16, 16], sizingH="fill", sizingV="fill")
    preview(b, body, 366, True, True)
    nav = b.row(body, "Соседние навыки", gap=8, sizingH="fill")
    button(b, nav, "‹ Предыдущий"); spacer(b, nav); button(b, nav, "Следующий ›")
    text(b, body, "Назад вернёт фильтры, позицию списка и оба выбранных навыка.", 11, FAINT, sizingH="fill", textAutoResize="height")
    footer(b, s, True)
    return s


def main():
    fc = FC()
    try:
        if any(n["name"] == NAME for n in fc.tops()):
            raise SystemExit("Board exists: edit its frames rather than duplicate")
        b = Tokens()
        root = b.col(None, NAME, gap=20, padding=20, w=1740, fill=BG, x=0, y=13200)
        text(b, root, "Выбор нескольких навыков и место для превью", 22, TEXT, True)
        text(b, root, "Чекбоксы отмечают Creative Studio Portfolio и Annual Report Microsite. Фокус и просмотр не меняют этот выбор.", 13, DIM)
        columns = b.row(root, "Две версии B", gap=20, sizingH="fill", crossAlign="min")
        frames = []
        for variant in (1, 2):
            col = b.col(columns, f"Вариант B{variant}", gap=12, w=840)
            text(b, col, "B1 · Компактный список + постоянное превью" if variant == 1 else "B2 · Миниатюры + отдельное действие просмотра", 18, TEXT, True)
            text(b, col, "Строка показывает референс справа; в 400 px он раскрывается прямо под строкой." if variant == 1 else "Крупнее миниатюры и явное «Смотреть»; в 400 px открывается отдельный экран.", 12, DIM, sizingH="fill", textAutoResize="height")
            frames.append(wide(b, col, variant))
            text(b, col, "Узкая панель · референс внутри списка" if variant == 1 else "Узкая панель · от списка к референсу и обратно", 18, TEXT, True)
            row = b.row(col, "Узкие состояния", gap=20, sizingH="fill", crossAlign="min")
            if variant == 1:
                frames.append(narrow_inline(b, row))
                note = b.col(row, "Поведение B1", gap=12, w=400, padding=16, fill=CARD, cornerRadius=10)
                text(b, note, "Что происходит в 400 px", 18, TEXT, True, sizingH="fill", textAutoResize="height")
                for line in ["Чекбокс только меняет выбор.", "Нажатие на название раскрывает референс под строкой.", "Одновременно раскрыт один референс.", "Кнопка «Свернуть» освобождает место списку.", "Нижняя панель всегда показывает два выбранных навыка."]:
                    text(b, note, line, 13, DIM, sizingH="fill", textAutoResize="height")
            else:
                frames.append(narrow_cards(b, row)); frames.append(narrow_focus(b, row))
        notes = b.col(root, "Общие состояния", gap=8, padding=16, fill=CARD, cornerRadius=10, sizingH="fill")
        text(b, notes, "Состояния и клавиатура", 18, TEXT, True)
        text(b, notes, "Space — выбрать навык · ↑↓ — сменить референс · Enter — добавить выбранные · Esc — свернуть превью / вернуться к списку", 13, DIM)
        text(b, notes, "Загрузка — плейсхолдер в той же области. Ошибка — «Не удалось загрузить превью» и «Повторить». Выбор не сбрасывается. При нуле выбранных кнопка добавления неактивна.", 13, DIM, sizingH="fill", textAutoResize="height")
        result = run(fc, b, "Навыки · B1–B2 с чекбоксами")
        root_id = result[root["$step"]]["id"]
        ids = [result[r["$step"]]["id"] for r in frames]
        fc.cmd("variable.setMode", ids=[root_id], collection="Tokens", mode="Graphite")
        fc.tool("save_file", {})
        for i, ident in enumerate(ids, 1):
            fc.shot(ident, f"/tmp/figcraft-checkbox-variant-{i}.png", max_size=1000)
        fc.cmd("view.set", zoom=0.65, cx=870, cy=13800)
        out = {"board": root_id, "frames": ids}
        Path('/tmp/figcraft-checkbox-variant-ids.json').write_text(json.dumps(out))
        print(json.dumps(out))
    finally:
        fc.p.terminate()


if __name__ == "__main__":
    main()
