#!/usr/bin/env python3
"""Three editable skill-preview proposals beside the Strict screens; never redraw existing screens."""
import json
from pathlib import Path
from strict import (B, FC, BG, CARD, BORDER, TEXT, DIM, FAINT, ACCENT, SURFACE, HOVER,
                    button, divider, inst, kbd, run, spacer, text)

NAME = "Strict · Навыки — крупный просмотр"
ROOT = Path(__file__).resolve().parent.parent
SKILLS = [
    ("Creative Studio Portfolio", "creative-studio-portfolio", "Портфолио студии · Editorial"),
    ("Architecture Project Index", "architecture-project-index", "Проекты архитектурного бюро · Editorial"),
    ("Annual Report Microsite", "annual-report-site", "Годовой отчёт · Minimal"),
    ("Accessibility Statement Page", "accessibility-statement-page", "Доступность продукта · Bold"),
]


class Tokens(B):
    def node(self, type, parent=None, name=None, *args, **props):
        ref = super().node(type, parent, name, *args, **props)
        for field, prefix in (("gap", "space/"), ("cornerRadius", "radius/")):
            n = props.get(field)
            if n in ({2, 4, 6, 8, 10, 12, 16, 20} if field == "gap" else {4, 6, 8, 10, 12}):
                self.add("variable.bind", {"ids": [ref], "field": field, "variable": prefix + str(n)})
        return ref


def image(b, parent, slug, w, h):
    r = b.rect(parent, "Референс · " + slug, w, h, CARD, cornerRadius=6)
    b.add("image.place", {"path": str(ROOT / "skills/skills" / ("opendesign-" + slug) / "assets/reference.webp"), "target": r, "mode": "fit"})
    return r


def tabs(b, parent, values, active):
    row = b.row(parent, "Фильтры", gap=4, sizingH="fill")
    for value in values:
        inst(b, row, "tab", {"Label": value, "Count": {"Все": "291", "Недавние": "6", "Избранное": "3", "Сайты": "67", "Приложения": "71"}.get(value, ""), "State": "Selected" if value == active else "Default"})
    return row


def header(b, parent, mode, compact=False):
    row = b.row(parent, "Шапка навыков", gap=8, h=48, padding=[0, 16, 0, 16], sizingH="fill")
    text(b, row, "Предпросмотр" if compact else "Навыки к сообщению", 13, TEXT, True)
    spacer(b, row)
    if not compact:
        text(b, row, "1 выбрано", 12, ACCENT)
    button(b, row, mode, "Ghost")
    button(b, row, "Закрыть", "Ghost")
    return row


def filters(b, parent):
    r = b.col(parent, "Поиск и фильтры", gap=8, padding=[0, 16, 12, 16], sizingH="fill")
    search = b.row(r, "Поиск", gap=8, padding=[8, 12, 8, 12], fill=SURFACE, cornerRadius=6, sizingH="fill")
    text(b, search, "Найти навык…", 12, FAINT)
    tabs(b, r, ["Все", "Недавние", "Избранное", "Сайты", "Приложения"], "Сайты")
    return r


def footer(b, parent, primary="Добавить 1 навык"):
    divider(b, parent)
    row = b.row(parent, "Действия", gap=8, h=48, padding=[0, 16, 0, 16], sizingH="fill")
    kbd(b, row, "Tab"); text(b, row, "тип", 11, FAINT)
    kbd(b, row, "↑↓"); text(b, row, "навык", 11, FAINT)
    spacer(b, row)
    button(b, row, primary, "Primary")


def screen(b, parent, name, w=840, h=820):
    return b.col(parent, name, gap=0, w=w, h=h, fill=BG, cornerRadius=12, stroke=BORDER, strokeWeight=1, clip=True)


def gallery(b, parent):
    s = screen(b, parent, "A · Крупные карточки")
    header(b, s, "Карточки  /  Список")
    filters(b, s)
    body = b.col(s, "Карточки навыков", gap=12, padding=[4, 16, 16, 16], sizingH="fill", sizingV="fill")
    for offset in (0, 2):
        row = b.row(body, "Ряд карточек", gap=12, sizingH="fill", crossAlign="min")
        for i in range(offset, offset + 2):
            name, slug, meta = SKILLS[i]
            c = b.col(row, name, gap=8, padding=12, fill=CARD, cornerRadius=10, stroke=ACCENT if i == 0 else BORDER, strokeWeight=1, sizingH="fill")
            image(b, c, slug, 374, 218)
            r = b.row(c, "Название", gap=6, sizingH="fill")
            text(b, r, name, 13, TEXT, True, sizingH="fill", textAutoResize="height")
            text(b, r, "Выбран" if i == 0 else "☆", 11, ACCENT if i == 0 else FAINT)
            text(b, c, "OpenDesign · " + meta, 11, DIM, sizingH="fill", textAutoResize="height")
    footer(b, s)
    return s


def detail(b, parent, narrow=False):
    s = screen(b, parent, "B · Список и предпросмотр" if not narrow else "B · Узкая панель", w=400 if narrow else 840)
    header(b, s, "Предпросмотр" if not narrow else "Назад к списку", compact=narrow)
    if not narrow:
        filters(b, s)
    body = b.row(s, "Список и крупный референс", gap=0, sizingH="fill", sizingV="fill", crossAlign="min")
    if not narrow:
        left = b.col(body, "Навыки", gap=4, w=286, padding=[4, 8, 12, 8], sizingV="fill")
        for i, (name, slug, meta) in enumerate(SKILLS):
            r = b.col(left, name, gap=6, padding=10, fill=HOVER if i == 0 else "none", cornerRadius=6, sizingH="fill")
            text(b, r, name, 13, TEXT, i == 0, sizingH="fill", textAutoResize="height")
            text(b, r, "OpenDesign · " + meta, 11, FAINT, sizingH="fill", textAutoResize="height")
        text(b, left, "Все 67 навыков доступны при прокрутке", 11, DIM, sizingH="fill", textAutoResize="height")
    right = b.col(body, "Предпросмотр выбранного навыка", gap=12, padding=16, fill=CARD, sizingH="fill", sizingV="fill")
    text(b, right, SKILLS[0][0], 18, TEXT, True, sizingH="fill", textAutoResize="height")
    text(b, right, "OpenDesign · Сайты · Editorial", 11, DIM)
    image(b, right, SKILLS[0][1], 368 if narrow else 522, 246 if narrow else 300)
    text(b, right, "Три проекта, выразительная типографика и асимметричная сетка. Названия, роль студии и ссылки остаются рядом с изображениями.", 13, DIM, sizingH="fill", textAutoResize="height")
    row = b.row(right, "Вторичные действия", gap=6, sizingH="fill")
    button(b, row, "Открыть референс", "Ghost")
    button(b, row, "В избранное", "Ghost")
    text(b, right, "↑↓ — следующий навык; предпросмотр меняется сразу", 11, FAINT, sizingH="fill", textAutoResize="height")
    footer(b, s, "Использовать навык")
    return s


def focus(b, parent):
    s = screen(b, parent, "C · Референс во весь просмотр")
    header(b, s, "Референс  /  По размеру")
    r = b.row(s, "Текущий навык", gap=12, padding=[0, 20, 12, 20], sizingH="fill")
    text(b, r, "‹", 18, DIM, True)
    text(b, r, SKILLS[0][0], 18, TEXT, True, sizingH="fill")
    text(b, r, "1 / 67", 12, DIM)
    text(b, r, "›", 18, DIM, True)
    body = b.col(s, "Крупный референс", gap=16, padding=20, sizingH="fill", sizingV="fill")
    image(b, body, SKILLS[0][1], 800, 526)
    text(b, body, "OpenDesign · Сайты · Editorial", 12, DIM)
    row = b.row(body, "Масштаб", gap=8, sizingH="fill")
    button(b, row, "−", "Ghost"); text(b, row, "100%", 12, DIM); button(b, row, "+", "Ghost")
    button(b, row, "Вписать", "Ghost"); spacer(b, row); button(b, row, "В избранное", "Ghost")
    text(b, body, "← → — листать навыки · Esc — вернуться в список", 11, FAINT)
    footer(b, s, "Использовать навык")
    return s


def main():
    fc = FC()
    try:
        existing = next((n for n in fc.tops() if n["name"] == NAME), None)
        if existing:
            raise SystemExit(f"Board already exists: {existing['id']}; edit it rather than duplicate")
        b = Tokens()
        board = b.col(None, NAME, gap=20, padding=20, w=2600, fill=BG, x=0, y=11100)
        text(b, board, "Как рассматривать навыки крупнее", 22, TEXT, True)
        text(b, board, "Один и тот же навык и референс. A — сравнить несколько; B — быстро выбирать с крупным просмотром; C — рассмотреть детали.", 13, DIM)
        row = b.row(board, "Три режима увеличенного просмотра", gap=20, crossAlign="min", sizingH="fill")
        refs = []
        builders = [(gallery, "A · Крупные карточки", "Лучше для сравнения внешнего вида. Меньше навыков видно одновременно."),
                    (detail, "B · Список + предпросмотр — рекомендую", "Стрелки листают навыки, справа сразу виден референс. Для ширины от 760 px."),
                    (focus, "C · Фокус на референсе", "Максимум места для деталей; весь список временно скрыт.")]
        for fn, title, caption in builders:
            col = b.col(row, title, gap=10, w=840)
            text(b, col, title, 18, TEXT, True)
            text(b, col, caption, 12, DIM, sizingH="fill", textAutoResize="height")
            refs.append(fn(b, col))
        lower = b.row(board, "Узкая панель и состояния", gap=20, crossAlign="min", sizingH="fill")
        narrow = b.col(lower, "B · На узкой панели", gap=10, w=400)
        text(b, narrow, "B · Узкая панель 400 px", 18, TEXT, True)
        text(b, narrow, "Предпросмотр открывается вместо списка; Назад возвращает позицию и фильтры.", 12, DIM, sizingH="fill", textAutoResize="height")
        refs.append(detail(b, narrow, True))
        states = b.col(lower, "Состояния предпросмотра", gap=16, w=840, padding=20, fill=CARD, cornerRadius=10)
        text(b, states, "Общее поведение для всех вариантов", 18, TEXT, True)
        for title, caption in [("Загрузка", "Скелетон на месте референса. Название навыка и кнопка Назад доступны сразу."),
                               ("Превью не загрузилось", "Понятное сообщение и Повторить; выбор навыка остаётся доступным."),
                               ("Нет референса", "Палитра и описание. Не показываем выдуманное изображение."),
                               ("Избранное пока пусто", "Нажмите звёздочку рядом с нужным навыком; кнопка Все навыки возвращает каталог."),
                               ("Недавние", "Последние выбранные и закреплённые навыки, сначала недавно использованные."),
                               ("Длинное название", "Перенос в крупном просмотре. В строке — сокращение и полное имя при наведении.")]:
            text(b, states, title, 13, TEXT, True)
            text(b, states, caption, 13, DIM, sizingH="fill", textAutoResize="height")
        result = run(fc, b, "Навыки · варианты крупного просмотра")
        board_id = result[board["$step"]]["id"]
        ids = [result[r["$step"]]["id"] for r in refs]
        fc.cmd("variable.setMode", ids=[board_id], collection="Tokens", mode="Graphite")
        fc.tool("save_file", {})
        for i, node_id in enumerate(ids):
            fc.shot(node_id, f"/tmp/figcraft-skill-preview-{i + 1}.png", max_size=1000)
        fc.cmd("view.set", zoom=0.8, cx=1320, cy=11650)
        Path('/tmp/figcraft-skill-preview-ids.json').write_text(json.dumps({"board": board_id, "frames": ids}))
        print(json.dumps({"board": board_id, "frames": ids}))
    finally:
        fc.p.terminate()


if __name__ == "__main__":
    main()
