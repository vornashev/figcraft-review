//! The review without FigCraft: labels, statuses and the widget's layers. Matches agent/review.py.
//!
//! A label is `#N · text` (text may run over several lines), then `↳ Author: reply` lines. The
//! status is the annotation's category.

use figcraft_plugin_sdk::{Value, json};

/// (key, category name, colour).
pub const STATUSES: [(&str, &str, &str); 5] = [
    ("open", "Открыто", "#F7768E"),
    ("question", "Вопрос", "#E0AF68"),
    ("done", "Готово", "#9ECE6A"),
    ("rejected", "Отклонено", "#737AA2"),
    ("review", "Проверь", "#7DCFFF"),
];

/// Rows the widget draws at most (each is up to 6 layers of the 256 a widget may have).
pub const MAX_ROWS: usize = 30;

#[derive(Clone, Debug, Default, PartialEq)]
pub struct Note {
    pub num: Option<u64>,
    pub text: String,
    pub replies: Vec<(String, String)>,
}

/// One remark: an annotation and where it is.
#[derive(Clone, Debug, Default, PartialEq)]
pub struct Remark {
    pub page: u64,
    pub page_name: String,
    pub layer: u64,
    pub index: u64,
    pub name: String,
    pub note: Note,
    /// A key of [`STATUSES`]; None when the annotation has no status category yet.
    pub status: Option<&'static str>,
}

fn reply(line: &str) -> Option<(String, String)> {
    let rest = line.strip_prefix('↳')?.trim_start();
    let (author, text) = rest.split_once(':')?;
    let n = author.chars().count();
    (1..=40).contains(&n).then(|| (author.trim().to_string(), text.trim().to_string()))
}

pub fn parse(label: &str) -> Note {
    let mut note = Note::default();
    let mut body: Vec<&str> = Vec::new();
    for line in label.split('\n') {
        if let Some(r) = reply(line).filter(|_| !body.is_empty() || !note.replies.is_empty()) {
            note.replies.push(r);
        } else if let Some(last) = note.replies.last_mut() {
            last.1.push('\n');
            last.1.push_str(line);
        } else {
            body.push(line);
        }
    }
    let text = body.join("\n").trim().to_string();
    let head = text.strip_prefix('#').and_then(|rest| {
        let digits: String = rest.chars().take_while(char::is_ascii_digit).collect();
        let tail = rest[digits.len()..].trim_start().strip_prefix('·')?;
        Some((digits.parse::<u64>().ok()?, tail.trim().to_string()))
    });
    match head {
        Some((num, t)) => {
            note.num = Some(num);
            note.text = t;
        }
        None => note.text = text,
    }
    note
}

pub fn build(n: &Note) -> String {
    let mut s = format!("#{} · {}", n.num.unwrap_or(0), n.text);
    for (a, r) in &n.replies {
        s.push_str(&format!("\n↳ {a}: {r}"));
    }
    s
}

pub fn status_by_name(category: Option<&str>) -> Option<&'static str> {
    STATUSES.iter().find(|(_, name, _)| Some(*name) == category).map(|(key, _, _)| *key)
}

pub fn status_name(key: &str) -> &'static str {
    STATUSES.iter().find(|(k, _, _)| *k == key).map_or(STATUSES[0].1, |(_, name, _)| name)
}

pub fn status_color(key: &str) -> &'static str {
    STATUSES.iter().find(|(k, _, _)| *k == key).map_or(STATUSES[0].2, |(_, _, c)| c)
}

pub fn closed(status: Option<&str>) -> bool {
    matches!(status, Some("done" | "rejected"))
}

pub fn glyph(status: Option<&str>) -> &'static str {
    match status {
        Some("done") => "✓",
        Some("question") => "?",
        Some("rejected") => "–",
        Some("review") => "◎",
        _ => "○",
    }
}

pub fn next_number(rs: &[Remark]) -> u64 {
    rs.iter().filter_map(|r| r.note.num).max().unwrap_or(0) + 1
}

/// Numbers and statuses for annotations made without them (by hand in Dev Mode), sorted by number:
/// the indexes of the remarks to save.
pub fn normalize(rs: &mut Vec<Remark>) -> Vec<usize> {
    let mut next = next_number(rs);
    let mut marked: Vec<(Remark, bool)> = rs
        .drain(..)
        .map(|mut r| {
            let changed = r.note.num.is_none() || r.status.is_none();
            if r.note.num.is_none() {
                r.note.num = Some(next);
                next += 1;
            }
            r.status = r.status.or(Some("open"));
            (r, changed)
        })
        .collect();
    marked.sort_by_key(|(r, _)| r.note.num);
    let mut out = Vec::new();
    for (i, (r, changed)) in marked.into_iter().enumerate() {
        if changed {
            out.push(i);
        }
        rs.push(r);
    }
    out
}

/// A click on a badge: open ⇄ done (a question or a refusal also becomes done).
pub fn toggled(status: Option<&str>) -> &'static str {
    if status == Some("done") { "open" } else { "done" }
}

/// `3 замечания · 1 готово`.
pub fn summary(rs: &[Remark]) -> String {
    let n = rs.len();
    if n == 0 {
        return "Замечаний нет".into();
    }
    let word = match (n % 10, n % 100) {
        (_, 11..=14) => "замечаний",
        (1, _) => "замечание",
        (2..=4, _) => "замечания",
        _ => "замечаний",
    };
    let mut s = format!("{n} {word}");
    let done = rs.iter().filter(|r| closed(r.status)).count();
    if done > 0 {
        s.push_str(&format!(" · {done} готово"));
    }
    let asked = rs.iter().filter(|r| r.status == Some("question")).count();
    if asked > 0 {
        s.push_str(&format!(" · {asked} с вопросом"));
    }
    let review = rs.iter().filter(|r| r.status == Some("review")).count();
    if review > 0 {
        s.push_str(&format!(" · {review} проверить"));
    }
    s
}

/// A reply as shown: `ask --option`'s «вопрос · варианты: 1) A; 2) B» becomes «вопрос — A / B».
pub fn reply_text(t: &str) -> String {
    match t.split_once(" · варианты: ") {
        Some((q, opts)) => {
            let opts: Vec<&str> = opts.split("; ").map(|o| o.split_once(") ").map_or(o, |(_, x)| x)).collect();
            format!("{q} — {}", opts.join(" / "))
        }
        None => t.to_string(),
    }
}

pub fn short(s: &str, n: usize) -> String {
    let one = s.replace('\n', " ");
    if one.chars().count() <= n {
        one
    } else {
        format!("{}…", one.chars().take(n.saturating_sub(1)).collect::<String>())
    }
}

/// Open ones first, then closed, each by number.
pub fn ordered(rs: &[Remark]) -> Vec<&Remark> {
    let mut v: Vec<&Remark> = rs.iter().collect();
    v.sort_by_key(|r| (closed(r.status), r.note.num));
    v
}

/// A list option: `○ #3 · Header — text`.
pub fn option(r: &Remark) -> String {
    format!("{} #{} · {} — {}", glyph(r.status), r.note.num.unwrap_or(0), short(&r.name, 24), short(&r.note.text, 60))
}

/// The number an option or any `#N` text names.
pub fn number_in(s: &str) -> Option<u64> {
    let rest = &s[s.find('#')? + 1..];
    let digits: String = rest.chars().take_while(char::is_ascii_digit).collect();
    digits.parse().ok()
}

/// What a click target names.
#[derive(Debug, PartialEq)]
pub enum Target {
    Refresh,
    ShowDone,
    Toggle { layer: u64, index: u64 },
    Open { layer: u64, page: u64 },
}

pub fn target(t: &str) -> Option<Target> {
    let mut parts = t.split('.');
    let head = parts.next()?;
    match head {
        "refresh" => Some(Target::Refresh),
        "done" => Some(Target::ShowDone),
        "t" | "o" => {
            let a = parts.next()?.parse::<u64>().ok()?;
            let b = parts.next()?.parse::<u64>().ok()?;
            Some(if head == "t" { Target::Toggle { layer: a, index: b } } else { Target::Open { layer: a, page: b } })
        }
        _ => None,
    }
}

// The widget's colours (Tokyo Night, like the panels around it).
const BG: &str = "#1A1B26";
const ROW: &str = "#24283B";
const LINE: &str = "#3B4261";
const TEXT: &str = "#C0CAF5";
const DIM: &str = "#A9B1D6";
const FAINT: &str = "#737AA2";
const ON_BADGE: &str = "#1A1B26";

fn chip(target: &str, label: &str, on: bool) -> Value {
    json!({"type": "frame", "name": label, "target": target, "layout": "horizontal", "padding": 6, "radius": 6,
           "fill": if on { "#2E3A5C" } else { ROW }, "stroke": LINE,
           "children": [{"type": "text", "text": label, "size": 11, "color": if on { TEXT } else { DIM }}]})
}

fn row(r: &Remark, pages: bool) -> Value {
    let status = r.status.unwrap_or("open");
    let done = closed(Some(status));
    let badge = json!({"type": "frame", "name": "Badge", "target": format!("t.{}.{}", r.layer, r.index), "layout": "horizontal",
                       "justify": "center", "align": "center", "width": 22, "height": 22, "radius": 11, "fill": status_color(status),
                       "children": [{"type": "text", "text": if done { glyph(Some(status)).to_string() } else { r.note.num.unwrap_or(0).to_string() },
                                     "size": 10, "bold": true, "color": ON_BADGE}]});
    let place = if pages { format!("{} · {}", r.name, r.page_name) } else { r.name.clone() };
    let mut texts = vec![
        json!({"type": "text", "name": "Layer", "text": short(&place, 56), "size": 10, "color": FAINT, "width": 368}),
        json!({"type": "text", "name": "Text", "text": short(&r.note.text, 200), "size": 12, "color": if done { FAINT } else { TEXT }, "width": 368}),
    ];
    if let Some((a, t)) = r.note.replies.last() {
        texts.push(json!({"type": "text", "name": "Reply", "text": short(&format!("↳ {a}: {}", reply_text(t)), 160), "size": 10,
                          "color": if status == "question" { STATUSES[1].2 } else { DIM }, "width": 368}));
    }
    json!({"type": "frame", "name": format!("#{}", r.note.num.unwrap_or(0)), "target": format!("o.{}.{}", r.layer, r.page),
           "layout": "horizontal", "gap": 10, "align": "min", "padding": 10, "radius": 8, "fill": ROW,
           "children": [badge, {"type": "frame", "name": "Texts", "layout": "vertical", "gap": 3, "children": texts}]})
}

/// The widget: the document's remarks, open ones first (closed ones only with `show_done`).
pub fn view(rs: &[Remark], show_done: bool, title: &str) -> Value {
    let pages = rs.iter().map(|r| r.page).collect::<std::collections::BTreeSet<_>>().len() > 1;
    let shown: Vec<&Remark> = ordered(rs).into_iter().filter(|r| show_done || !closed(r.status)).collect();
    let done = rs.iter().filter(|r| closed(r.status)).count();
    let mut children = vec![
        json!({"type": "frame", "name": "Header", "layout": "horizontal", "gap": 8, "align": "center", "children": [
            {"type": "frame", "name": "Heading", "layout": "vertical", "gap": 2, "width": 260, "align": "min", "children": [
                {"type": "text", "name": "Title", "text": short(title, 32), "size": 13, "bold": true, "color": TEXT},
                {"type": "text", "name": "Summary", "text": summary(rs), "size": 11, "color": FAINT},
            ]},
            chip("done", &if show_done { "Скрыть готовые".to_string() } else { format!("Готовые {done}") }, show_done),
            chip("refresh", "↻", false),
        ]}),
    ];
    children.extend(shown.iter().take(MAX_ROWS).map(|r| row(r, pages)));
    if shown.len() > MAX_ROWS {
        children.push(
            json!({"type": "text", "text": format!("и ещё {}", shown.len() - MAX_ROWS), "size": 10, "color": FAINT}),
        );
    }
    if shown.is_empty() {
        let empty = if rs.is_empty() {
            "Выделите слой и нажмите SUPER+ALT+N или откройте «Замечание…»"
        } else {
            "Все замечания закрыты"
        };
        children
            .push(json!({"type": "text", "name": "Empty", "text": empty, "size": 12, "color": FAINT, "width": 408}));
    }
    children.push(
        json!({"type": "text", "name": "Hint", "text": "SUPER+ALT+A — скопировать для агента · клик по номеру — готово",
                         "size": 10, "color": FAINT, "width": 408}),
    );
    json!({"type": "frame", "name": "Review", "layout": "vertical", "gap": 8, "padding": 14, "radius": 12, "width": 436, "align": "min",
           "fill": BG, "stroke": LINE, "children": children})
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn replies_with_options() {
        assert_eq!(reply_text("Какой размер? · варианты: 1) 16; 2) 18"), "Какой размер? — 16 / 18");
        assert_eq!(reply_text("увеличил до 16"), "увеличил до 16");
    }

    fn r(num: Option<u64>, status: Option<&'static str>) -> Remark {
        Remark {
            layer: 5,
            index: 0,
            page: 1,
            name: "Header".into(),
            note: Note { num, text: "x".into(), ..Note::default() },
            status,
            ..Remark::default()
        }
    }

    #[test]
    fn labels_round_trip_like_review_py() {
        let n = Note {
            num: Some(7),
            text: "Кнопка налезает".into(),
            replies: vec![("Claude".into(), "увеличил padding".into()), ("Я".into(), "ок".into())],
        };
        let label = build(&n);
        assert_eq!(label, "#7 · Кнопка налезает\n↳ Claude: увеличил padding\n↳ Я: ок");
        assert_eq!(parse(&label), n);
        assert_eq!(parse("Сделать крупнее"), Note { text: "Сделать крупнее".into(), ..Note::default() });
        assert_eq!(parse("#3 · две\nстроки").text, "две\nстроки");
        assert_eq!(parse("#3 · a\n↳ Claude: x\ny").replies, vec![("Claude".to_string(), "x\ny".to_string())]);
        assert_eq!(parse("↳ not a reply: first").text, "↳ not a reply: first");
        assert_eq!(parse("#12x · no").num, None);
    }

    #[test]
    fn numbers_statuses_and_targets() {
        let mut rs = vec![r(Some(4), Some("done")), r(None, None), r(Some(2), None)];
        assert_eq!(normalize(&mut rs), vec![0, 2], "the new number and the missing status are saved, #4 isn't");
        assert_eq!(
            rs.iter().map(|r| (r.note.num, r.status)).collect::<Vec<_>>(),
            vec![(Some(2), Some("open")), (Some(4), Some("done")), (Some(5), Some("open"))]
        );
        assert_eq!(summary(&rs), "3 замечания · 1 готово");
        assert_eq!((summary(&rs[..1]), summary(&[])), ("1 замечание".to_string(), "Замечаний нет".to_string()));
        assert_eq!(
            ordered(&rs).iter().map(|r| r.note.num).collect::<Vec<_>>(),
            vec![Some(2), Some(5), Some(4)],
            "open first"
        );
        assert_eq!((toggled(Some("done")), toggled(Some("open")), toggled(Some("question"))), ("open", "done", "done"));
        assert_eq!(option(&rs[0]), "○ #2 · Header — x");
        assert_eq!(number_in("✓ #12 · x"), Some(12));
        assert_eq!(target("t.42.1"), Some(Target::Toggle { layer: 42, index: 1 }));
        assert_eq!(target("o.42.7"), Some(Target::Open { layer: 42, page: 7 }));
        assert_eq!(
            (target("refresh"), target("done"), target("t.x"), target("zzz")),
            (Some(Target::Refresh), Some(Target::ShowDone), None, None)
        );
    }

    #[test]
    fn widget_hides_done_and_caps_rows() {
        let rows = |v: &Value| {
            v["children"]
                .as_array()
                .map_or(0, |c| c.iter().filter(|c| c["target"].as_str().is_some_and(|t| t.starts_with("o."))).count())
        };
        let rs = vec![r(Some(1), Some("open")), r(Some(2), Some("done"))];
        assert_eq!((rows(&view(&rs, false, "design")), rows(&view(&rs, true, "design"))), (1, 2));
        let many: Vec<Remark> = (1..=40).map(|n| r(Some(n), Some("open"))).collect();
        assert_eq!(rows(&view(&many, false, "design")), MAX_ROWS);
        assert_eq!(row(&rs[1], false)["children"][0]["children"][0]["text"], "✓");
        assert_eq!(row(&rs[0], false)["children"][0]["children"][0]["text"], "1");
        assert_eq!(
            row(&Remark { page_name: "Б".into(), ..rs[0].clone() }, true)["children"][1]["children"][0]["text"],
            "Header · Б"
        );
    }
}
