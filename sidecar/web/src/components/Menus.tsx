// The menus (Strict D, F, G, I, J, P): one at a time, over the input (or under the title for the chats).
import {useLayoutEffect, useRef, useState} from "react";
import * as A from "../actions";
import * as ed from "../composer";
import {EXCLUSIVE, REMARKS, ago, group, modelDescription, originName, originOf, short} from "../lib/format";
import {agentOf, autoOn, modelName, pinned, set, skillOf, useApp, type State} from "../store";
import type {Axis} from "../api";
import {Icon, Mark, Swatches} from "./bits";
import {isIcon} from "../lib/icons";
import {shortcut} from "../lib/keyboard";
import {toggleFavorite} from "../skillPrefs";
import {SourceFilter} from "./SourceFilter";
import {ResourceFilter, ResourceTags} from "./ResourceFilter";
import {sourceEnabled} from "../lib/skillSources";

export function Menus() {
  const s = useApp();
  if (!s.menu || s.settingsOpen || s.library) return null;
  if (s.menu === "chats") return <Menu kind="chats" anchor="chatsBtn" below><ChatsMenu s={s} /></Menu>;
  if (s.menu === "plus") return <Menu kind="plus" anchor="box"><PlusMenu s={s} /></Menu>;
  if (s.menu === "models") return <ModelPicker s={s} />;
  if (s.menu === "pinned") return <Menu kind="pinned" anchor="box"><PinnedMenu s={s} /></Menu>;
  if (s.menu === "slash" && s.slash) return <Menu kind="slash" anchor="box"><SlashMenu s={s} /></Menu>;
  if (s.menu === "mention" && s.mention) return <Menu kind="mention" anchor="box"><MentionMenu s={s} /></Menu>;
  if (s.menu === "variants") return <Menu kind="variants" anchor="box" className="variants-menu"><VariantsMenu s={s} /></Menu>;
  return null;
}

function Menu({kind, anchor, below, className = "", children}: {kind: string; anchor: string; below?: boolean; className?: string; children: React.ReactNode}) {
  const ref = useRef<HTMLDivElement>(null);
  useLayoutEffect(() => {  // follows its anchor: the input grows under it
    const r = document.getElementById(anchor)?.getBoundingClientRect(), m = ref.current!;
    if (!r) return;
    if (below) m.style.top = r.bottom + 6 + "px"; else m.style.bottom = innerHeight - r.top + 6 + "px";
  });
  return <div ref={ref} className={`menu ${className}`} data-kind={kind} role={kind === "models" ? "dialog" : undefined} aria-label={kind === "models" ? "Модель и агент" : undefined} style={{left: 8, right: 8}} onClick={(e) => e.stopPropagation()}>{children}</div>;
}

// a group's label: «Чаты файла 3», «Доступ для всех чатов»
export const Lbl = ({children, note, right, g}: {children: React.ReactNode; note?: string; right?: React.ReactNode; g?: string}) => (
  <div className={`lbl${g ? " g-" + g : ""}`}>{g && <i className="gdot" />}<span>{children}</span>{note && <span className="note">{note}</span>}{right != null && <span className="right">{right}</span>}</div>
);
export const Keys = ({pairs, children}: {pairs: [string, string][]; children?: React.ReactNode}) => (
  <div className="keys">{pairs.map(([k, v]) => [<kbd key={k}>{k}</kbd>, <span key={k + v}>{v}</span>])}{children}</div>
);
const Divider = () => <div className="divider" />;
export const Toggle = ({on}: {on: boolean}) => <span className={`toggle ${on ? "on" : ""}`} />;

function ChatsMenu({s}: {s: State}) {  // F: the file's remarks and chats; a chat's actions behind ⋯ (V)
  const busy = new Set(s.S.running.map((r) => r.chat)), here = (id: string) => s.view === "chat" && s.chat?.id === id;
  const chats = s.S.chats.filter((c) => !s.gone.includes(c.id)), open = s.R.list.filter((r) => r.status === "open").length;
  const [more, setMore] = useState<string | null>(null), [renaming, setRenaming] = useState<string | null>(null);
  return <>
    <button className={`item two ${s.view === "remarks" ? "on" : ""}`} data-remarks onClick={A.showRemarks}>
      <span className="lead"><i className={`sqm${open ? "" : " off"}`} /></span><span className="grow">Замечания<br /><small>{open || s.R.list.length ? A.remarksCount() : "нет открытых"}</small></span><span className="lead">›</span>
    </button>
    <Divider />
    {chats.length ? <>
      <Lbl right={chats.length}>Чаты файла</Lbl>
      {chats.map((c) => [
        <div key={c.id} className={`item two ${here(c.id) ? "on" : ""}${more === c.id ? " hold" : ""}`} data-id={c.id} onClick={() => renaming !== c.id && A.openChat(c.id)}>
          <span className="lead"><Mark id={c.agent} /></span>
          {renaming === c.id
            ? <input className="grow rename" data-rename defaultValue={c.title} autoFocus onClick={(e) => e.stopPropagation()} onFocus={(e) => e.currentTarget.select()}
                onKeyDown={(e) => {
                  e.stopPropagation();
                  if (e.key === "Enter") { setRenaming(null); A.renameChat(c.id, e.currentTarget.value); }
                  if (e.key === "Escape") setRenaming(null);
                }} onBlur={() => setRenaming(null)} />
            : <span className="grow">{c.title}<br /><small>{busy.has(c.id) ? "работает · " : ""}{ago(c.updated)}{c.model ? " · " + modelName(agentOf(c.agent, s), c.model) : ""}</small></span>}
          {busy.has(c.id) ? <span className="spin" /> : here(c.id) ? <span className="check">✓</span> : null}
          <button className="ic more" data-more-chat={c.id} title="Действия с чатом" aria-label="Действия с чатом"
            onClick={(e) => { e.stopPropagation(); setMore(more === c.id ? null : c.id); }}>⋯</button>
        </div>,
        more === c.id && (  // under its row, inside the list: a popup would be cut by the list's scroll
            <div key={c.id + "-acts"} className="rowmenu" onClick={(e) => e.stopPropagation()}>
              <button className="item" data-chat-act="rename" onClick={() => { setMore(null); setRenaming(c.id); }}><span className="t">Переименовать</span></button>
              <button className="item" data-chat-act="copy" onClick={() => { setMore(null); A.copyChat(c.id); }}><span className="t">Копировать как Markdown</span></button>
              <Divider />
              <button className="item danger" data-del={c.id} onClick={() => { setMore(null); A.deleteChat(c.id); }}><span className="t">Удалить чат</span></button>
            </div>
        ),
      ])}
      <Keys pairs={[["↑↓", "выбрать"], ["↵", "открыть"]]}><button className="btn primary" data-new onClick={A.newChat}>+ Новый чат</button></Keys>
    </> : (
      <Empty title="Чатов пока нет" hint="Опишите задачу в поле ниже — чат появится здесь.">
        <button className="btn" data-new onClick={A.newChat}>+ Новый чат</button>
      </Empty>
    )}
  </>;
}

// AB: nothing to show, said once and the same everywhere
export const Empty = ({title, hint, children}: {title: string; hint?: string; children?: React.ReactNode}) => (
  <div className="empty-state"><i /><b>{title}</b>{hint && <span>{hint}</span>}{children}</div>
);

// a row of a menu: lead glyph, title, a faint description, something on the right
function Item({a, lead, title, desc, trail, on, onClick, k}: {a?: string; lead?: React.ReactNode; title: React.ReactNode; desc?: React.ReactNode;
  trail?: React.ReactNode; on?: boolean; onClick: () => void; k?: number}) {
  return (
    <button className={`item ${on ? "on" : ""}`} data-a={a} data-k={k} onMouseDown={(e) => k != null && e.preventDefault()} onClick={onClick}>
      {lead != null && (typeof lead === "string" ? <span className="ic">{isIcon(lead) ? <Icon n={lead} /> : lead}</span> : lead)}
      <span className="t">{title}</span><span className="desc">{desc}</span>{trail}
    </button>
  );
}

function PlusMenu({s}: {s: State}) {  // I: what can go into the message
  const sel = s.S.selection.filter((n) => !n.more), open = s.R.list.filter((r) => r.status === "open").length;
  const pins = pinned(s).map(ed.skillName);
  const run = (a: string) => () => {
    A.closeMenu();
    if (a === "sel") ed.insertSelection();
    else if (a === "rem") { if (!ed.segments().some((x) => x.kind === "remarks")) ed.insertChips([REMARKS]); }
    else if (a === "library") A.openLibrary();
    else if (a === "skill") setTimeout(ed.openSlashInText);
    else if (a === "pins") setTimeout(() => A.openMenu("pinned"));
    else if (a === "at") A.insertMention();
    else if (a === "pic") A.pickFiles();
    else if (a === "vars" || a === "design") A.insertTask(a);
  };
  return <>
    <Lbl>Вставить</Lbl>
    <Item a="sel" lead="#" title="Выделенные слои" desc={sel.length ? short(sel.map((n) => n.name).join(", "), 40) : "ничего не выделено"} trail={<kbd>Tab</kbd>} onClick={run("sel")} />
    <Item a="rem" lead="alert" title="Открытые замечания" desc={`${open} открыто`} onClick={run("rem")} />
    <Item a="at" lead="@" title="Слой или замечание" desc="по имени" trail={<kbd>@</kbd>} onClick={run("at")} />
    <Item a="pic" lead="attach" title="Файлы и картинки" desc="или вставьте, перетащите" onClick={run("pic")} />
    <Divider />
    <Lbl>Навыки</Lbl>
    <Item a="skill" lead="book" title="Навык к сообщению" trail={<kbd>/</kbd>} onClick={run("skill")} />
    <Item a="pins" lead="pin" title="Навыки чата" desc={pins.length ? pins.join(" · ") : "ничего не закреплено"} onClick={run("pins")} />
    <Item a="library" lead="puzzle" title="Все навыки" desc="библиотека и режимы" trail={<span className="ic">›</span>} onClick={run("library")} />
    <Divider />
    <Lbl>Задачи</Lbl>
    <Item a="vars" lead="branch" title="Варианты" desc="2–3 направления, сценарии те же" onClick={run("vars")} />
    <Item a="design" lead="doc" title={s.S.designMd?.exists ? "Обновить DESIGN.md" : "Составить DESIGN.md"} desc="о продукте для агента" onClick={run("design")} />
    <Divider />
    <Item a="shots" lead="image" title="PNG слоёв из чипов" desc="к каждому сообщению" trail={<Toggle on={!!s.S.settings.shots} />}
      onClick={() => A.saveSettings({shots: !s.S.settings.shots})} />
  </>;
}

const ACCESS: [string, string, string][] = [["figcraft", "Только FigCraft", "макет и файлы проекта"], ["terminal", "Как в терминале", "права из настроек агента"]];
export const AccessRadios = ({mode}: {mode: string}) => <>{ACCESS.map(([k, n, d]) => (
  <button key={k} className={`rradio ${mode === k ? "on" : ""}`} role="radio" aria-checked={mode === k} data-m={k} onClick={() => A.saveSettings({mode: k})}>
    <span className="r" /><span>{n}</span><span className="desc">{d}</span></button>
))}</>;

function ModelPicker({s}: {s: State}) {  // G: agents, their models and the agent's access
  const agents = s.S.agents.filter((a) => a.ok);
  const [active, setActive] = useState(() => agents.find((a) => a.id === s.S.settings.agent)?.id || agents[0]?.id);
  const [q, setQ] = useState("");
  const list = useRef<HTMLDivElement>(null), tabs = useRef<HTMLDivElement>(null);
  const a = agents.find((x) => x.id === active), query = q.trim().toLowerCase();
  const models = (a?.models || []).filter((x) => !query || `${x.name} ${x.id} ${modelDescription(x)}`.toLowerCase().includes(query));
  const choose = (id: string) => {
    A.chooseModel(active!, id);
    A.closeMenu();
    document.getElementById("pickerBtn")?.focus();
  };
  const onKeyDown = (e: React.KeyboardEvent) => {
    if (e.nativeEvent.isComposing || e.ctrlKey || e.altKey || e.metaKey) return;
    if (e.key === "Escape") { e.preventDefault(); e.stopPropagation(); A.closeMenu(); document.getElementById("pickerBtn")?.focus(); return; }
    const rows = [...list.current!.querySelectorAll<HTMLElement>("[data-model]")], at = rows.indexOf(document.activeElement as HTMLElement);
    if (e.key === "Tab" && agents.length > 1 && ((e.target as HTMLElement).tagName === "INPUT" || at >= 0 || tabs.current?.contains(e.target as Node))) {
      e.preventDefault();
      const next = (agents.findIndex((a) => a.id === active) + (e.shiftKey ? -1 : 1) + agents.length) % agents.length;
      setActive(agents[next].id); setQ("");
      tabs.current?.querySelectorAll<HTMLButtonElement>("button")[next]?.focus();
      return;
    }
    if (e.key === "ArrowDown" || e.key === "ArrowUp") {
      if (!rows.length) return;
      e.preventDefault();
      const back = e.key === "ArrowUp";
      rows[at < 0 ? (back ? rows.length - 1 : 0) : (at + (back ? -1 : 1) + rows.length) % rows.length]?.focus();
    }
    else if (e.key === "Enter" && ((e.target as HTMLElement).tagName === "INPUT" || at >= 0)) { e.preventDefault(); (at >= 0 ? rows[at] : rows[0])?.click(); }
  };
  return (
    <Menu kind="models" anchor="pickerBtn" className="model-picker">
      <div onKeyDown={onKeyDown} style={{display: "contents"}}>
        <div className="search"><Icon n="search" /><input id="q" aria-label="Найти модель" placeholder="Найти модель…" value={q} autoFocus onInput={(e) => setQ(e.currentTarget.value)} /></div>
        <div className="tabs" ref={tabs} role="tablist" aria-label="Агенты" style={{padding: "8px 4px 4px"}}>
          {agents.map((x) => <button key={x.id} className="tab" role="tab" aria-selected={x.id === active} data-agent={x.id} onClick={() => setActive(x.id)}>{x.name}<small>{x.models.length}</small></button>)}
        </div>
        <Lbl right={a ? "доступен" : undefined}>Модели</Lbl>
        <div className="model-list" role="tabpanel" aria-label="Модели" ref={list}>
          {models.length ? models.map((x) => {
            const selected = s.S.settings.agent === active && s.S.settings.model === x.id;
            return <button key={x.id} className={`item ${selected ? "on" : ""}`} data-model={x.id} aria-pressed={selected} onClick={() => choose(x.id)}>
              <span className="t">{x.name}</span><small className="desc">{modelDescription(x)}</small>{selected && <span className="check">✓</span>}</button>;
          }) : <div className="item"><small>{a ? "Модели не найдены" : "Нет доступных агентов"}</small></div>}
        </div>
        <Divider />
        <Lbl note="для всех чатов">Доступ</Lbl>
        <AccessRadios mode={s.S.settings.mode} />
        <Keys pairs={[["Tab", "агент"], ["↑↓", "модель"], ["Enter", "готово"]]}>
          <button className="btn" id="toSettings" title="Агенты, доступ, навыки и чаты файла" onClick={() => set({menu: null, settingsOpen: true})}><Icon n="gear" />Настройки<kbd>{shortcut(",")}</kbd></button></Keys>
      </div>
    </Menu>
  );
}

function PinnedMenu({s}: {s: State}) {  // P: the chat's skills: always on, pinned, may the agent pick more
  const always = (s.S.skills || []).filter((k) => k.mode === "always");
  const pins = pinned(s).map((n) => skillOf(n, s) || {name: n, title: n, group: "other", summary: "нет такого навыка", mode: "", source: ""});
  const defaults = s.S.skillDefaults || [];
  const same = defaults.length === pins.length && pins.every((k) => defaults.includes(k.name));
  const unpin = (n: string) => A.setPinned(pinned().filter((x) => x !== n)).catch((err) => A.toast(err.message));
  const row = (k: typeof pins[number], lock?: boolean) => (
    <div className={`item g-${k.group}`} key={k.name}><i className="gdot" />
      <span className="t">{k.title}</span><span className="desc">{lock ? k.summary : group(k.group)[0].toLowerCase()}</span><Swatches s={k} />
      {lock ? <span className="ic" title="Режим «всегда»"><Icon n="lock" /></span>
        : <button className="ic" data-unpin={k.name} title="Убрать из чата" onClick={() => unpin(k.name)}>×</button>}
    </div>
  );
  return <>
    <div className="mhead"><b>Навыки этого чата</b><span>идут с каждым сообщением</span></div>
    {always.length > 0 && <><Lbl>Всегда</Lbl>{always.map((k) => row(k, true))}</>}
    <Lbl right={pins.length}>Закреплены</Lbl>{pins.map((k) => row(k))}
    <Item a="add" lead="+" title="Добавить навык" onClick={A.openPinSkills} />
    <Divider />
    <button className="item two" data-a="auto" onClick={A.toggleAuto}>
      <span className="grow" style={{whiteSpace: "normal"}}><span className="t">Агент может взять ещё</span><br /><small>навыки с режимом «Сам» — по описанию</small></span><Toggle on={autoOn(s)} />
    </button>
    <Divider />
    <div className="row" style={{padding: "6px 4px 4px"}}>
      <button className="btn" data-a="library" onClick={A.openLibrary}>Все навыки ›</button><span className="grow" />
      <button className="btn" data-a="defaults" disabled={same} onClick={A.saveDefaults}>{same ? <><Icon n="check" /> Так начинаются новые чаты файла</> : "Для новых чатов файла"}</button>
    </div>
  </>;
}

function SlashMenu({s}: {s: State}) {  // D
  const slash = s.slash!, it = slash.items, msg = slash.mode === "message";
  const sources = slash.sources === undefined ? s.slashSources : slash.sources, origins = ed.slashOrigins();
  const categories = ed.slashCategories(sources), category = slash.category || "all";
  const grid = s.slashView === "grid", preview = s.slashView === "preview";
  const picked = new Set(msg ? ed.inMessage() : pinned(s)), pins = new Set(pinned(s));
  const cur = Math.min(slash.i, Math.max(it.length - 1, 0));
  const active = it[cur];
  const ref = useRef<HTMLDivElement>(null), inspector = useRef<HTMLElement>(null);
  useLayoutEffect(() => { ref.current?.querySelector(".item.on")?.scrollIntoView({block: "nearest"}); }, [cur, category, sources, slash.q, s.slashView]);
  useLayoutEffect(() => { if (inspector.current) inspector.current.scrollTop = 0; }, [active?.name]);
  const pick = (k: number) => { set({slash: {...slash, i: k}}); msg ? ed.toggleSlash() : A.pinSlash(); };
  const showMore = (g: string) => { const open = new Set([...slash.open, g]); set({slash: {...slash, open, items: ed.slashItems(slash.q, open, category, sources)}}); };
  const sourceHint = sources === null ? "" : sources.length ? `Источники: ${origins.filter((o) => sources.includes(o.id)).map((o) => o.label).join(", ")}. ` : "Включите хотя бы один источник. ";
  const backToSkills = () => msg ? ed.focusEditor() : document.getElementById("sq")?.focus();
  const out: React.ReactNode[] = [];
  let g: string | null = null;
  const more = (gr: string | null) => gr && it.more?.[gr]
    ? <button key={"m" + gr} className="item more" data-more={gr} onMouseDown={(e) => e.preventDefault()} onClick={() => showMore(gr)}>Ещё {it.more[gr]}<span className="note">прокрутите или нажмите ↓</span></button> : null;
  it.forEach((k, i) => {
    if (k.group !== g) {
      if (g !== null) out.push(more(g), <div key={"s" + k.group + i} className="sep" />);
      g = k.group;
      const gr = group(k.group);
      out.push(<div key={"h" + k.group + i} className={`head g-${k.group}`}>{gr[0]}{gr[2] && k.group !== "base" && <span className="note">{gr[2]}</span>}</div>);
    }
    const on = picked.has(k.name), radio = EXCLUSIVE.has(k.group), now = i === cur;
    out.push(
      <div className="slash-entry" key={k.name}>
        {preview && <button className={`slash-check ${on ? "picked" : ""}`} aria-label={`${on ? "Убрать" : "Выбрать"}: ${k.title}`} aria-pressed={on} onMouseDown={(e) => e.preventDefault()} onClick={() => pick(i)}><span className={`ctl ${radio ? "round" : "check"}`} /></button>}
        <button className={`item slash-choice ${on ? "picked" : ""} ${now ? "on" : ""}`} data-k={i} title={[k.title, originName(k), k.description || k.summary].join(" · ")} aria-pressed={preview ? undefined : on} aria-current={preview && now ? "true" : undefined} onMouseDown={(e) => e.preventDefault()} onClick={() => preview ? set({slash: {...slash, i}}) : pick(i)}>
        {!preview && <span className={`ctl ${radio ? "round" : "check"}`} />}
        {k.thumbnail && <span className="slash-preview"><img className="slash-thumb" src={k.thumbnail} alt="" loading="lazy" /></span>}
        <span className="slash-copy"><span data-skill-title>{k.title}</span><small>{k.summary}</small>
          <span className="slash-meta">{k.origin || k.source !== "builtin" ? <span className="src">{originName(k)}</span> : null}<Swatches s={k} /></span>
          <ResourceTags skill={k} />
        </span>
        {msg && pins.has(k.name) && <span className="pin" title="Закреплён в чате"><Icon n="pin" /></span>}
      </button>{!preview && <button className={`favorite-btn${s.skillPrefs.favorites.includes(k.name) ? " selected" : ""}`} data-favorite={k.name} aria-label={`${s.skillPrefs.favorites.includes(k.name) ? "Убрать из избранного" : "В избранное"}: ${k.title}`}
        aria-pressed={s.skillPrefs.favorites.includes(k.name)} title={s.skillPrefs.favorites.includes(k.name) ? "Убрать из избранного" : "В избранное"} onMouseDown={(e) => e.preventDefault()} onClick={() => toggleFavorite(k.name)}>
        <Icon n={s.skillPrefs.favorites.includes(k.name) ? "starred" : "star"} /></button>}</div>);
  });
  out.push(more(g));
  return <>
    <div className="slash-header">
      <div className="title"><span className="grow">{msg ? "Навыки к сообщению" : "Закрепить в чате"}</span>{picked.size > 0 && <span>{picked.size} выбрано</span>}
        <div className="slash-tools"><SourceFilter options={origins} value={sources} scope="slash" onChange={ed.filterSlashSources} back={backToSkills} />
        <div className="slash-display" role="group" aria-label="Вид навыков">{(["list", "grid", "preview"] as const).map((view) => <button key={view} data-skill-view={view} aria-pressed={s.slashView === view}
          onMouseDown={(e) => e.preventDefault()} onClick={() => ed.setSlashView(view)}>{view === "list" ? "Список" : view === "grid" ? "Сетка" : "Просмотр"}</button>)}</div>
        </div>
      </div>
      <div className="slash-filters">
        <div className="tabs slash-collections" role="group" aria-label="Подборка навыков">{categories.filter((c) => ["all", "recent", "favorites"].includes(c.id)).map((c) => <button key={c.id} className="tab" data-slash-category={c.id}
          aria-pressed={category === c.id} tabIndex={-1} onMouseDown={(e) => e.preventDefault()} onClick={() => ed.filterSlash(c.id)}>{c.label}<small>{c.count}</small></button>)}</div>
        <div className="tabs slash-types" role="group" aria-label="Тип навыка">{categories.filter((c) => !["all", "recent", "favorites"].includes(c.id)).map((c) => <button key={c.id} className="tab" data-slash-category={c.id}
          aria-pressed={category === c.id} tabIndex={-1} onMouseDown={(e) => e.preventDefault()} onClick={() => ed.filterSlash(c.id)}>{c.label}<small>{c.count}</small></button>)}</div>
        {category === "design-systems" && <ResourceFilter composer skills={(s.S.skills || []).filter((k) => k.mode !== "always" && sourceEnabled(sources, originOf(k)))} value={slash.resourceKind} onChange={ed.filterSlashResourceKind} />}
      </div>
      {!msg && <div style={{padding: "0 4px 4px"}}><input id="sq" placeholder="Найти навык…" autoFocus value={slash.q}
        onChange={(e) => set({slash: {...slash, q: e.target.value, i: 0, items: ed.slashItems(e.target.value, slash.open, category, sources)}})}
        onKeyDown={(e) => A.slashKeys(e)} /></div>}
    </div>
    <div className={`slash-body${preview ? " with-preview" : ""}`}>
    <div className={`slash-list${grid ? " skill-grid" : ""}`} ref={ref} aria-label="Навыки выбранного типа" onWheel={(e) => { if (e.deltaY > 0) ed.expandSlash(); }} onScroll={(e) => { if (e.currentTarget.scrollTop > 0) ed.expandSlash(); }}>
      {out}
      {!it.length && <Empty title={sources?.length === 0 ? "Источники выключены" : category === "favorites" && !slash.q ? "В избранном пока пусто" : category === "recent" && !slash.q ? "Недавних навыков пока нет" : "Ничего не нашлось"} hint={sourceHint + (slash.q ? `Нет навыка «${slash.q}»${category !== "all" ? ` в разделе «${categories.find((c) => c.id === category)?.label}»` : ""}. Измените запрос, тип или источник.` : category === "favorites" ? "Нажмите звёздочку рядом с нужным навыком." : category === "recent" ? "Здесь появятся выбранные и закреплённые навыки." : "Выберите другой тип, источник или откройте библиотеку.")}>
        {category !== "all" && <button className="btn line" data-reset-slash onMouseDown={(e) => e.preventDefault()} onClick={() => ed.filterSlash("all")}>Все типы</button>}
        {sources !== null && <button className="btn line" data-reset-origin onMouseDown={(e) => e.preventDefault()} onClick={() => ed.filterSlashSources(null)}>Все источники</button>}
      </Empty>}
    </div>
    {preview && active && <aside className={`slash-inspector${active.thumbnail ? "" : " text-only"}`} ref={inspector} aria-label="Предпросмотр навыка" data-preview-skill={active.name}>
      {active.thumbnail && <div className="inspector-media"><img key={active.name} src={active.thumbnail} alt={`Превью ${active.title}`} /></div>}
      <div className="inspector-copy"><strong>{active.title}</strong><div className="slash-meta"><span className="src">{originName(active)}</span><Swatches s={active} /></div>
        <ResourceTags skill={active} /><p>{active.description || active.summary}</p></div>
      <div className="inspector-actions"><button className={`btn inspector-select ${picked.has(active.name) ? "picked" : ""}`} data-preview-select aria-pressed={picked.has(active.name)} onMouseDown={(e) => e.preventDefault()} onClick={() => pick(cur)}>
        <span className={`ctl ${EXCLUSIVE.has(active.group) ? "round" : "check"}`} />{picked.has(active.name) ? msg ? "Добавлен к сообщению" : "Закреплён в чате" : msg ? "Добавить к сообщению" : "Закрепить в чате"}</button>
        <button className={`favorite-btn${s.skillPrefs.favorites.includes(active.name) ? " selected" : ""}`} data-favorite={active.name} aria-label={s.skillPrefs.favorites.includes(active.name) ? "Убрать из избранного" : "В избранное"} title={s.skillPrefs.favorites.includes(active.name) ? "Убрать из избранного" : "В избранное"} aria-pressed={s.skillPrefs.favorites.includes(active.name)} onMouseDown={(e) => e.preventDefault()} onClick={() => toggleFavorite(active.name)}><Icon n={s.skillPrefs.favorites.includes(active.name) ? "starred" : "star"} /></button>
      </div>
    </aside>}
    </div>
    <div className="slash-footer">
      <div className="keys"><kbd>Tab</kbd>тип<kbd>Alt+←/→</kbd>источник<kbd>{grid ? "←↑↓→" : "↑↓"}</kbd>навык{msg && <><kbd>Space</kbd>отметить</>}<kbd>Enter</kbd>{msg ? "готово" : "закрепить"}</div>
      <div className="slash-actions">
        {msg && <button className="btn" data-pin-current disabled={!it.length} onMouseDown={(e) => e.preventDefault()} onClick={A.pinSlash}>
          <Icon n="pin" />{it[cur] && pins.has(it[cur].name) ? "Открепить" : "Закрепить в чате"}<kbd>{shortcut("Enter")}</kbd></button>}
        <button className="btn" data-library onClick={A.openLibrary}>Все навыки ›</button>
      </div>
    </div>
  </>;
}

function MentionMenu({s}: {s: State}) {  // J: the page's remarks and layers
  const m = s.mention!;
  const indexed = m.items.map((x, k) => [x, k] as const);
  const row = ([x, k]: typeof indexed[number]) => (
    <Item key={k} k={k} on={k === m.i} title={x.c.label} desc={x.desc}
      lead={x.c.kind === "remark" ? <span className={`ring ${x.status || ""}`} /> : <span className={`ic${x.mauve ? " mauve" : ""}`}>{x.c.icon}</span>}
      trail={k === m.i ? <kbd>↵</kbd> : undefined} onClick={() => ed.chooseMention(k)} />
  );
  const remarks = indexed.filter(([x]) => x.c.kind === "remark"), layers = indexed.filter(([x]) => x.c.kind !== "remark");
  return <>
    <div className="mhead"><b>{m.q ? `@${m.q}` : "Слои страницы и замечания"}</b>{m.items.length > 0 && <span>{m.items.length} найдено</span>}</div>
    {remarks.length > 0 && <><Lbl>Замечания</Lbl>{remarks.map(row)}</>}
    {layers.length > 0 && <><Lbl>Слои страницы</Lbl>{layers.map(row)}</>}
    {!m.items.length && (m.indexing ? <div className="item"><small>Собираю слои страницы…</small></div>
      : <Empty title="Ничего не нашлось" hint="Попробуйте другое слово: имя слоя или текст замечания." />)}
    <Keys pairs={[["↑↓", "выбрать"], ["↵", "вставить"], ["Esc", "закрыть"]]} />
  </>;
}

// VA, VB, VH: ×N — how many variants the next message asks for, presets, what the lanes differ in, who orchestrates,
// each lane's agent, model and style, how long a lane may take. Kept for every chat; a lane left unset draws with the
// orchestrator's agent and model. A frame chip in the message: the lanes redo copies of it.
const TIMES = [1, 2, 3, 4, 6];
const AXES: [Axis, string][] = [["style", "Стиль"], ["structure", "Структура"], ["adaptive", "Адаптив"]];
const LIMITS: [number, string][] = [[0, "∞"], [10, "10 мин"], [20, "20 мин"]];
function VariantsMenu({s}: {s: State}) {
  const [pick, setPick] = useState<{who: number; kind: "model" | "style"} | null>(null);  // who: -1 the orchestrator
  const v = s.S.settings.variants || {}, n = s.times;
  const orch = v.orchestrator || {agent: s.S.settings.agent || "claude", model: s.S.settings.model || ""};
  const lane = (i: number) => v.lanes?.[i] || {agent: orch.agent, model: orch.model};
  const frames = ed.segments().filter((x) => x.kind === "layer"), base = frames.length === 1 ? frames[0] : null;
  if (pick) return <VariantPick s={s} pick={pick} lane={pick.who < 0 ? orch : lane(pick.who)} back={() => setPick(null)} />;
  const who = (l: {agent: string; model: string}, i: number) => (
    <button className="vsel" data-vmodel={i} title="Агент и модель" onClick={() => setPick({who: i, kind: "model"})}>
      <Mark id={l.agent} /><span>{modelName(agentOf(l.agent, s), l.model) || "модель агента"}</span><Icon n="chevron" /></button>
  );
  return <div onKeyDown={(e) => { const k = Number(e.key); if (TIMES.includes(k) && (e.target as HTMLElement).tagName !== "INPUT") set({times: k}); }}
    style={{display: "contents"}}>
    <div className="mhead"><b>Варианты</b>
      <span className="seg" role="radiogroup" aria-label="Сколько вариантов">{TIMES.map((k) => (
        <button key={k} role="radio" aria-checked={k === n} className={k === n ? "on" : ""} data-times={k} onClick={() => set({times: k})}>×{k}</button>))}</span>
    </div>
    {!!v.presets?.length || n > 1 ? <div className="presets">{(v.presets || []).map((p) => (
      <span key={p.name} className="chip preset"><button data-preset={p.name} title={`×${p.count}`} onClick={() => A.applyPreset(p.name)}>{p.name}</button>
        <button className="x" aria-label={`Удалить пресет ${p.name}`} onClick={() => A.dropPreset(p.name)}>×</button></span>))}
      <span className="grow" />{n > 1 && <button className="link" data-preset-save onClick={() => A.savePreset()}>+ Сохранить</button>}</div> : null}
    {n === 1 ? <p className="vnote">×1 — обычный ответ. С ×2 и больше оркестратор подберёт разные направления, а дорожки нарисуют их параллельно — каждая своим агентом, курсором и отменой.</p> : <>
      <Lbl>Чем отличаются</Lbl>
      <div className="vrow"><span className="seg wide" role="radiogroup" aria-label="Чем отличаются варианты">{AXES.map(([k, label]) => (
        <button key={k} role="radio" aria-checked={(v.axis || "style") === k} className={(v.axis || "style") === k ? "on" : ""} data-axis={k}
          onClick={() => A.saveVariants({axis: k})}>{label}</button>))}</span></div>
      {base && <div className="vrow base"><Icon n="branch" /><small>От рамки «{base.label}»: копии, а не пустые рамки</small></div>}
      <Divider />
      <Lbl note="план и сравнение">Оркестратор</Lbl>
      <div className="vrow">{who(orch, -1)}<small>выбирает направления, не рисует</small></div>
      <Divider />
      <Lbl note="каждая — свой агент, курсор и отмена">Дорожки</Lbl>
      {Array.from({length: n}, (_, i) => {
        const l = lane(i), st = l.style ? skillOf(l.style, s) : undefined;
        return <div className="vrow" key={i} data-lane={i + 1}><b className="num">{i + 1}</b>{who(l, i)}
          <button className="vsel style" data-vstyle={i} title="Стиль дорожки" onClick={() => setPick({who: i, kind: "style"})}>
            <Icon n="palette" /><span className={st ? "" : "auto"}>{st ? st.title : "Авто"}</span>{st && <Swatches s={st} />}<Icon n="chevron" /></button>
        </div>;
      })}
      <div className="vrow limit"><small className="grow">Не дольше</small><span className="seg" role="radiogroup" aria-label="Время на дорожку">{LIMITS.map(([k, label]) => (
        <button key={k} role="radio" aria-checked={(v.limit || 0) === k} className={(v.limit || 0) === k ? "on" : ""} data-limit={k}
          onClick={() => A.saveVariants({limit: k})}>{label}</button>))}</span></div>
    </>}
    <Keys pairs={[["1–6", "сколько"], ["Esc", "готово"]]} />
  </div>;
}

function VariantPick({s, pick, lane, back}: {s: State; pick: {who: number; kind: "model" | "style"}; lane: {agent: string; model: string; style?: string}; back: () => void}) {
  const [q, setQ] = useState("");
  const words = q.toLowerCase().split(/\s+/).filter(Boolean);
  const hit = (...xs: (string | undefined)[]) => words.every((w) => xs.join(" ").toLowerCase().includes(w));
  const done = (p: Promise<unknown>) => { p.then(back); };
  const title = pick.who < 0 ? "Оркестратор" : `Дорожка ${pick.who + 1}`;
  if (pick.kind === "model") {
    const choose = (agent: string, model: string) => done(pick.who < 0 ? A.saveVariants({orchestrator: {agent, model}})
      : A.setLane(pick.who, {agent, model, ...(lane.style ? {style: lane.style} : {})}));
    return <>
      <div className="search"><Icon n="search" /><input aria-label="Найти модель" placeholder={`${title}: агент и модель…`} value={q} autoFocus onInput={(e) => setQ(e.currentTarget.value)} /></div>
      <div className="vlist">{s.S.agents.filter((a) => a.ok).map((a) => {
        const models = a.models.filter((m) => hit(a.name, m.name, m.id));
        return models.length ? <div key={a.id}><Lbl>{a.name}</Lbl>{models.map((m) => {
          const on = lane.agent === a.id && lane.model === m.id;
          return <button key={m.id} className={`item ${on ? "on" : ""}`} data-pick-model={`${a.id}/${m.id}`} onClick={() => choose(a.id, m.id)}>
            <Mark id={a.id} /><span className="t">{m.name}</span><small className="desc">{modelDescription(m)}</small>{on && <span className="check">✓</span>}</button>;
        })}</div> : null;
      })}</div>
      <Keys pairs={[["Esc", "закрыть"]]}><button className="btn" onClick={back}>← Назад</button></Keys>
    </>;
  }
  const choose = (style?: string) => done(A.setLane(pick.who, {agent: lane.agent, model: lane.model, ...(style ? {style} : {})}));
  const all = (s.S.skills || []).filter((k) => ["system", "library", "style"].includes(k.group) && hit(k.title, k.name, k.summary, originName(k)));
  const row = (k: typeof all[number]) => (
    <button key={k.name} className={`item two ${lane.style === k.name ? "on" : ""}`} data-pick-style={k.name} onClick={() => choose(k.name)}>
      <span className="grow"><span className="t">{k.title}</span><small className="desc">{[originName(k), k.summary].filter(Boolean).join(" · ")}</small></span>
      <Swatches s={k} />{lane.style === k.name && <span className="check">✓</span>}</button>
  );
  const systems = all.filter((k) => k.group === "system"), libs = all.filter((k) => k.group === "library"), styles = all.filter((k) => k.group === "style");
  return <>
    <div className="search"><Icon n="search" /><input aria-label="Найти стиль" placeholder={`Стиль: ${title.toLowerCase()}…`} value={q} autoFocus onInput={(e) => setQ(e.currentTarget.value)} /></div>
    <div className="vlist">
      {!words.length && <button className={`item two ${lane.style ? "" : "on"}`} data-pick-style="" onClick={() => choose()}>
        <span className="grow"><span className="t">Авто</span><small className="desc">оркестратор выберет разные</small></span>{!lane.style && <span className="check">✓</span>}</button>}
      {systems.length > 0 && <><Lbl g="system" note="компоненты и токены">Дизайн-системы</Lbl>{systems.slice(0, 40).map(row)}</>}
      {libs.length > 0 && <><Lbl g="library" note="экран из готовых компонентов">Библиотеки компонентов</Lbl>{libs.slice(0, 40).map(row)}</>}
      {styles.length > 0 && <><Lbl g="style" right={styles.length}>Стили</Lbl>{styles.slice(0, 60).map(row)}</>}
      {!all.length && <div className="item"><small>Ничего не нашлось</small></div>}
    </div>
    <Keys pairs={[["Esc", "закрыть"]]}><button className="btn" onClick={back}>← Назад</button></Keys>
  </>;
}
