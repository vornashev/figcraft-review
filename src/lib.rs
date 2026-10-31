//! Review: numbered remarks on layers kept as FigCraft annotations.
//!
//! The "Remark…" panel adds a remark to the selected layers and lists the document's remarks (a
//! pick goes to the layer; done, reopen, remove). The widget lists them on the canvas: a click on
//! a badge ticks a remark off, on a row goes to its layer, ↻ redraws it (agent/review.py clicks it).

pub mod review;

use figcraft_plugin_sdk::{
    Event, Input, Result, Value, Widget, call, entry, json, notify, render_widget, selection, show_ui,
};
use review::{Note, Remark, STATUSES, Target};

/// Status categories, made when the document lacks them.
fn ensure_statuses() -> Result<()> {
    let have = call("annotation.categories", &json!({}))?;
    let names: Vec<&str> =
        have["categories"].as_array().into_iter().flatten().filter_map(|c| c["name"].as_str()).collect();
    for (_, name, color) in STATUSES {
        if !names.contains(&name) {
            call("annotation.addCategory", &json!({"name": name, "color": color}))?;
        }
    }
    Ok(())
}

/// Every remark on every page, numbered (annotations made by hand get the next numbers).
fn load() -> Result<Vec<Remark>> {
    ensure_statuses()?;
    let mut rs = Vec::new();
    for page in call("page.list", &json!({}))?.as_array().into_iter().flatten() {
        let (Some(id), name) = (page["id"].as_u64(), page["name"].as_str().unwrap_or_default()) else { continue };
        if page["divider"].as_bool() == Some(true) {
            continue;
        }
        for a in call("annotation.list", &json!({"page": id}))?["annotations"].as_array().into_iter().flatten() {
            let (Some(layer), Some(index)) = (a["id"].as_u64(), a["index"].as_u64()) else { continue };
            rs.push(Remark {
                page: id,
                page_name: name.into(),
                layer,
                index,
                name: a["name"].as_str().unwrap_or_default().into(),
                note: review::parse(a["label"].as_str().unwrap_or_default()),
                status: review::status_by_name(a["category"]["name"].as_str()),
            });
        }
    }
    for i in review::normalize(&mut rs) {
        save(&rs[i])?;
    }
    Ok(rs)
}

fn save(r: &Remark) -> Result<Value> {
    call(
        "annotation.edit",
        &json!({"id": r.layer, "index": r.index, "category": review::status_name(r.status.unwrap_or("open")),
                                     "label": review::build(&r.note)}),
    )
}

fn go_to(r: &Remark) -> Result<()> {
    call("page.select", &json!({"id": r.page}))?;
    call("select.set", &json!({"ids": [r.layer]}))?;
    call("view.zoomSelection", &json!({}))?;
    Ok(())
}

/// The open document's name (the widget's title).
fn doc_name() -> String {
    let docs = call("doc.list", &json!({})).unwrap_or(Value::Null);
    let list = docs["documents"].as_array().or(docs.as_array()).cloned().unwrap_or_default();
    list.iter()
        .find(|d| d["current"].as_bool() == Some(true) || d["active"].as_bool() == Some(true))
        .and_then(|d| d["name"].as_str().map(str::to_string))
        .unwrap_or_else(|| "Ревью".into())
}

// ---- widget ----

fn on_widget(w: Widget) -> Result<Value> {
    let mut show_done = w.state["showDone"].as_bool().unwrap_or(false);
    let mut rs = load()?;
    match w.target.as_deref().and_then(review::target) {
        Some(Target::ShowDone) => show_done = !show_done,
        Some(Target::Toggle { layer, index }) => {
            if let Some(r) = rs.iter_mut().find(|r| r.layer == layer && r.index == index) {
                r.status = Some(review::toggled(r.status));
                save(r)?;
            }
        }
        Some(Target::Open { layer, page }) => {
            if let Some(r) = rs.iter().find(|r| r.layer == layer && r.page == page) {
                go_to(r)?;
            }
        }
        Some(Target::Refresh) | None => {}
    }
    render_widget(&json!({"state": {"showDone": show_done}, "root": review::view(&rs, show_done, &doc_name())}))?;
    Ok(json!({"summary": review::summary(&rs)}))
}

// ---- panel ----

/// The selected layers as the panel names them, and the remarks already on them.
fn selected_note(rs: &[Remark]) -> String {
    let ids = selection();
    let Some(first) = ids.first() else { return "Выделите слой на холсте".into() };
    let n = call("node.get", &json!({"id": first})).unwrap_or(Value::Null);
    let more = if ids.len() > 1 { format!(" и ещё {}", ids.len() - 1) } else { String::new() };
    let on: Vec<String> =
        rs.iter().filter(|r| ids.contains(&r.layer)).map(|r| format!("#{}", r.note.num.unwrap_or(0))).collect();
    let on = if on.is_empty() { String::new() } else { format!(" · уже {}", on.join(", ")) };
    review::short(
        &format!(
            "Слой: «{}» {}{more}{on}",
            n["name"].as_str().unwrap_or("?"),
            n["type"].as_str().unwrap_or("").to_lowercase()
        ),
        990,
    )
}

fn panel(rs: &[Remark], picked: Option<u64>, clear: bool, message: Option<String>) -> Result<Value> {
    let mut text = json!({"type": "text", "name": "text", "label": "Замечание"});
    if clear {
        text["value"] = json!("");
    }
    let mut c = vec![
        json!({"type": "note", "label": selected_note(rs)}),
        text,
        json!({"type": "button", "name": "add", "label": format!("Добавить #{}", review::next_number(rs))}),
        json!({"type": "button", "name": "selection", "label": "↻"}),
        json!({"type": "note", "label": message.map_or_else(|| review::summary(rs), |m| format!("{m} · {}", review::summary(rs)))}),
    ];
    let current = picked.and_then(|n| rs.iter().find(|r| r.note.num == Some(n)));
    if !rs.is_empty() {
        let options: Vec<String> = review::ordered(rs).into_iter().take(60).map(review::option).collect();
        let mut list = json!({"type": "list", "name": "items", "label": "Замечания", "options": options});
        if let Some(r) = current {
            list["value"] = json!(review::option(r));
        }
        c.push(list);
    }
    if let Some(r) = current {
        if let Some((a, t)) = r.note.replies.last() {
            c.push(json!({"type": "note", "label": review::short(&format!("↳ {a}: {}", review::reply_text(t)), 990)}));
        }
        c.push(if review::closed(r.status) {
            json!({"type": "button", "name": "reopen", "label": "Вернуть в работу"})
        } else {
            json!({"type": "button", "name": "done", "label": "Готово"})
        });
        c.push(json!({"type": "button", "name": "remove", "label": "Удалить"}));
    }
    c.push(json!({"type": "note", "label": "SUPER+ALT+A — скопировать все открытые для агента"}));
    show_ui(&json!({"title": "Замечание", "controls": c}))?;
    Ok(Value::Null)
}

fn on_event(e: Event) -> Result<Value> {
    let mut rs = load()?;
    let picked = e.values["items"].as_str().and_then(review::number_in);
    let at = |rs: &[Remark], n: Option<u64>| rs.iter().position(|r| n.is_some() && r.note.num == n);
    match e.control.as_str() {
        "add" => {
            let ids = selection();
            if ids.is_empty() {
                notify("Сначала выделите слой");
                return panel(&rs, picked, false, None);
            }
            let text = e.values["text"].as_str().unwrap_or_default().trim();
            if text.is_empty() {
                notify("Напишите замечание");
                return panel(&rs, picked, false, None);
            }
            let first = review::next_number(&rs);
            for (i, id) in ids.iter().enumerate() {
                let note = Note { num: Some(first + i as u64), text: text.into(), replies: vec![] };
                call(
                    "annotation.add",
                    &json!({"id": id, "label": review::build(&note), "category": review::status_name("open")}),
                )?;
            }
            let last = first + ids.len() as u64 - 1;
            let msg = if last == first {
                format!("Добавлено #{first}")
            } else {
                format!("Добавлено #{first}–#{last}")
            };
            panel(&load()?, Some(last), true, Some(msg))
        }
        "items" => {
            let n = e.value.as_str().and_then(review::number_in);
            if let Some(i) = at(&rs, n) {
                go_to(&rs[i])?;
            }
            panel(&rs, n, false, None)
        }
        "done" | "reopen" => {
            let mut msg = None;
            if let Some(i) = at(&rs, picked) {
                let r = &mut rs[i];
                r.status = Some(if e.control == "done" { "done" } else { "open" });
                save(r)?;
                msg = Some(format!(
                    "#{} {}",
                    r.note.num.unwrap_or(0),
                    if e.control == "done" { "готово" } else { "снова в работе" }
                ));
            }
            panel(&rs, picked, false, msg)
        }
        "remove" => {
            let mut msg = None;
            if let Some(i) = at(&rs, picked) {
                let r = rs.remove(i);
                call("annotation.remove", &json!({"id": r.layer, "index": r.index}))?;
                msg = Some(format!("#{} удалено", r.note.num.unwrap_or(0)));
                rs = load()?;
            }
            panel(&rs, None, false, msg)
        }
        // Typing in the field, ↻ and anything else: redraw, which also names the selection anew.
        _ => panel(&rs, picked, false, None),
    }
}

fn run(input: Input) -> Result<Value> {
    if let Some(w) = input.widget {
        return on_widget(w);
    }
    if let Some(e) = input.event {
        return on_event(e);
    }
    panel(&load()?, None, false, None)
}

entry!(run);
