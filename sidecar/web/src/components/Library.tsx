// The full skill library: the catalog, a skill's card, how skills work, adding one.
import {useEffect, useLayoutEffect, useRef, useState} from "react";
import {api, type Skill, type SkillReferences} from "../api";
import * as A from "../actions";
import {CATEGORIES, EXCLUSIVE, GROUPS, SKILL_MODES, group, originName, originOf, plural, sizeLabel} from "../lib/format";
import {pinned, set, skillOf, useApp, type Library as Lib, type State} from "../store";
import {Icon, Swatches} from "./bits";
import {Empty, Lbl} from "./Menus";
import {BackTop} from "./Settings";
import {shortcut} from "../lib/keyboard";
import {setSkillSources, skillCollection, toggleFavorite} from "../skillPrefs";
import {skillOrigins, sourceEnabled} from "../lib/skillSources";
import {SourceFilter} from "./SourceFilter";
import {ResourceFilter, ResourceTags} from "./ResourceFilter";
import {matchesResourceKind} from "../lib/designResources";
import {inMessage} from "../composer";

const scrolls: Record<string, number> = {};  // where each screen was scrolled to

export function Library() {
  const s = useApp(), lib = s.library!, body = useRef<HTMLDivElement>(null);
  const card = lib.screen === "card", k = card ? skillOf(lib.name!, s) : undefined;
  const key = lib.screen + (card ? lib.name : "");
  useLayoutEffect(() => {
    const el = body.current!;
    el.scrollTop = scrolls[key] || 0;
    return () => { scrolls[key] = el.scrollTop; };
  }, [key]);
  const title = card ? k?.title || lib.name! : lib.screen === "help" ? "Как устроены навыки" : lib.screen === "add" ? "Добавить навык" : "Навыки";
  const meta = card ? [group(k?.group)[0], k && originName(k), k?.category && CATEGORIES[k.category], k?.style].filter(Boolean).join(" · ") : `для всех файлов · ${(s.S.skills || []).length}`;
  const [content, footer] = lib.screen === "catalog" ? Catalog(s, lib) : card ? Card(s, lib, k) : lib.screen === "help" ? [<Help key="h" />, null] : [<Add key="a" />, null];
  return (
    <section className="skill-library page" id="skillLibrary" aria-label="Библиотека навыков">
      <BackTop id="libraryBack" title={title} sub={meta} onBack={A.libraryBack}>
        {lib.screen === "catalog" && <button className="btn" data-page="help" aria-label="Как устроены навыки" onClick={() => set({library: {...lib, screen: "help"}})}>?</button>}
      </BackTop>
      <div className="body" ref={body}>{content}</div>
      {footer && <footer className="pfoot">{footer}</footer>}
    </section>
  );
}

// Y: «Сам ⌄» opens a small menu of the three modes, with what each one means
function ModeSelect({k}: {k: Skill}) {
  const [open, setOpen] = useState(false), ref = useRef<HTMLSpanElement>(null);
  useEffect(() => {
    if (!open) return;
    const away = (e: MouseEvent) => { if (!ref.current?.contains(e.target as Node)) setOpen(false); };
    document.addEventListener("click", away);
    return () => document.removeEventListener("click", away);
  }, [open]);
  return (
    <span className="modewrap" ref={ref}>
      <button className={`modesel ${k.mode}`} data-mode={k.name} aria-label={`Режим ${k.title}`} aria-expanded={open} disabled={k.source === "pen.dev"}
        onClick={() => setOpen(!open)}>{SKILL_MODES[k.mode] || k.mode}<Icon n="chevron" /></button>
      {open && <div className="menu modemenu" onKeyDown={(e) => { if (e.key === "Escape") { e.stopPropagation(); setOpen(false); } }}>
        <div className="mhead"><b>{k.title}</b></div>
        {Object.keys(MODE_TEXT).map((m) => (
          <button key={m} className={`item two ${k.mode === m ? "on" : ""}`} data-set-mode={m} onClick={() => { setOpen(false); if (m !== k.mode) A.changeSkillMode(k.name, m); }}>
            <span className="grow">{MODE_TEXT[m][0]}<br /><small>{MODE_TEXT[m][1]}</small></span>{k.mode === m && <span className="check">✓</span>}</button>
        ))}
      </div>}
    </span>
  );
}

function Catalog(s: State, lib: Lib): [React.ReactNode, React.ReactNode] {  // N: search, groups, every skill with its mode
  const cat = s.S.skills || [], filtered = A.librarySkills(s);
  const sources = lib.sources ?? null;
  const sourceSkills = cat.filter((k) => sourceEnabled(sources, originOf(k)));
  const categories = [...new Set(sourceSkills.map((k) => k.category).filter((c): c is string => !!c))];
  const collectionSkills = skillCollection(sourceSkills, lib.collection);
  const countSkills = collectionSkills.filter((k) => (!lib.category || lib.category === "all" || k.category === lib.category) && matchesResourceKind(k, lib.category, lib.resourceKind));
  const filters = [["all", ["Все"]] as [string, string[]], ...Object.entries(GROUPS)].filter(([g]) => g === "all" || countSkills.some((k) => k.group === g));
  return [<>
    <div className="search"><Icon n="search" />
      <input id="skillSearch" placeholder="Найти навык…" aria-label="Найти навык" autoFocus defaultValue={lib.q} onInput={(e) => set({library: {...lib, q: e.currentTarget.value}})} /></div>
    <div className="tabs">{[["all", "Все навыки"], ["recent", "Недавние"], ["favorites", "Избранное"]].map(([id, name]) => <button key={id} className="tab" data-skill-collection={id} aria-pressed={(lib.collection || "all") === id}
      onClick={() => set({library: {...lib, collection: id}})}>{name}<small>{skillCollection(cat, id).length}</small></button>)}</div>
    <div className="library-filters">
      <SourceFilter options={skillOrigins(cat)} value={sources} scope="library" onChange={(value) => {
        setSkillSources(value); set({library: {...lib, sources: value, category: "all", resourceKind: "all", group: "all"}});
      }} />
      {categories.length > 0 && <label>Тип<select aria-label="Тип дизайна" id="skillCategory" value={lib.category || "all"}
        onChange={(e) => set({library: {...lib, category: e.currentTarget.value, resourceKind: "all", group: "all"}})}>
        <option value="all">Все типы · {sourceSkills.length}</option>
        {categories.map((c) => <option key={c} value={c}>{CATEGORIES[c] || c} · {sourceSkills.filter((k) => k.category === c).length}</option>)}
      </select></label>}
    </div>
    {lib.category === "design-systems" && <ResourceFilter skills={collectionSkills} value={lib.resourceKind} onChange={(resourceKind) => set({library: {...lib, resourceKind, group: "all"}})} />}
    <div className="tabs" style={{padding: "4px 0"}}>{filters.map(([g, gr]) => (
      <button key={g} data-group={g} className="tab" aria-pressed={lib.group === g} onClick={() => set({library: {...lib, group: g}})}>
        {gr[0]}<small>{g === "all" ? countSkills.length : countSkills.filter((k) => k.group === g).length}</small></button>
    ))}</div>
    {(lib.collection === "recent" ? [["recent", ["Недавно использованные"]] as [string, string[]]] : Object.entries(GROUPS)).map(([g, gr]) => {
      const list = g === "recent" ? filtered : filtered.filter((k) => k.group === g);
      return list.length ? <div key={g} style={{display: "contents"}}>
        <Lbl g={g === "recent" ? undefined : g} note={gr[2]}>{gr[0]}</Lbl>
        <div className="card">{list.map((k) => (
          <div className="crow skill-entry" key={k.name}>
            <button data-skill={k.name} title={k.title} onClick={() => A.openSkill(k.name)}>
              {k.thumbnail && <img className="skill-thumb" src={k.thumbnail} alt="" width="64" height="44" loading="lazy" />}
              <span className="skill-copy"><span className="skill-heading"><span className="t">{k.title}</span>
                <span className={`origin-tag ${originOf(k)}`}>{originName(k)}</span><Swatches s={k} /></span>
                <span className="desc">{[CATEGORIES[k.category || ""], k.style, k.summary].filter(Boolean).join(" · ")}</span><ResourceTags skill={k} /></span>
            </button>
            <button className={`favorite-btn${s.skillPrefs.favorites.includes(k.name) ? " selected" : ""}`} data-favorite={k.name} aria-pressed={s.skillPrefs.favorites.includes(k.name)} aria-label={`Избранное: ${k.title}`} title="Избранное" onClick={() => toggleFavorite(k.name)}><Icon n={s.skillPrefs.favorites.includes(k.name) ? "starred" : "star"} /></button>
            <ModeSelect k={k} />
          </div>
        ))}</div>
      </div> : null;
    })}
    {!filtered.length && <Empty title={!lib.q && lib.collection === "favorites" ? "В избранном пока пусто" : !lib.q && lib.collection === "recent" ? "Недавних навыков пока нет" : cat.length ? "Ничего не нашлось" : "Навыков пока нет"}
      hint={lib.collection === "favorites" ? "Добавьте нужные навыки звёздочкой в общем списке." : lib.collection === "recent" ? "Здесь появятся выбранные и закреплённые навыки." : cat.length ? "Попробуйте другое слово или измените фильтры." : "Добавьте навык в библиотеку."}>
      <button className="btn" onClick={() => { setSkillSources(null); set({library: {...lib, collection: "all", q: "", group: "all", sources: null, category: "all", resourceKind: "all"}}); }}>Все навыки</button></Empty>}
  </>, <>
    <span className="grow" />
    <button className="btn" data-page="add" onClick={() => set({library: {...lib, screen: "add"}})}>+ Добавить навык</button>
  </>];
}

function Preview({k}: {k: Skill}) {
  const colors = (k.preview?.colors || []).filter((c) => /^#[0-9a-f]{6}$/i.test(c));
  if (!colors.length) return null;
  const [bg, , ink = "#EDE7DC", accent = ink] = colors;
  return (
    <div className="skill-preview" style={{background: bg, color: ink}}>
      <div className="sample"><b>Aa</b><span>{k.preview!.font || "Палитра стиля"}</span><em style={{background: accent, color: bg}}>Войти</em></div>
      <div className="skill-palette">{colors.map((c, i) => <div key={i} title={["фон", "поверхность", "текст", "акцент"][i] || c}><i style={{background: c}} /></div>)}</div>
    </div>
  );
}

function References({title, refs}: {title: string; refs: SkillReferences}) {
  const [index, setIndex] = useState(0), [failed, setFailed] = useState(false);
  const image = refs.images[index];
  const open = () => set({gallery: {pics: refs.images.map((i) => ({kind: "image", path: i.url, label: `${title} · ${i.label}`})), index}});
  return <section className="skill-references" aria-label="Референсы навыка">
    {refs.images.length > 0 && <>
      <div className="reference-head"><span className="caption grow">Пример оформления</span>
        <div className="tabs" aria-label="Вид превью">{refs.images.map((i, n) => <button key={i.file} className="tab" aria-pressed={index === n} data-preview={n}
          onClick={() => { setIndex(n); setFailed(false); }}>{i.label}</button>)}</div>
      </div>
      {image && (failed ? <div className="reference-error"><span>Не удалось загрузить превью</span><button className="btn line" onClick={() => setFailed(false)}>Повторить</button></div>
        : <button className="reference-shot" data-reference-image aria-label={`Увеличить ${title} · ${image.label}`} onClick={open}>
          <img key={image.url} src={image.url} alt={`${title} — ${image.label}`} onError={() => setFailed(true)} />
          <span className="enlarge">Увеличить ↗</span>
        </button>)}
    </>}
    {refs.links.length > 0 && <div className="reference-links">{refs.links.map((l) => <a key={l.url} className="btn line" href={l.url} target="_blank" rel="noopener noreferrer">{l.label} ↗</a>)}</div>}
  </section>;
}

const MODE_TEXT: Record<string, [string, string]> = {manual: ["Вручную", "через / или закрепить в чате"], auto: ["Сам", "агент берёт по описанию"],
  always: ["Всегда", "с каждым сообщением"]};
function Card(s: State, lib: Lib, k?: Skill): [React.ReactNode, React.ReactNode] {  // O: its look, what it does, how it applies, its files
  if (!k) return [<p key="none">Навык больше не доступен в этом файле.</p>, null];
  const d = lib.detail, ro = k.source === "pen.dev";
  return [<>
    <ResourceTags skill={k} />
    {d?.references && (d.references.images.length > 0 || d.references.links.length > 0) && <References key={k.name} title={k.title} refs={d.references} />}
    <Preview k={k} />
    <p className="desc-text">{k.description || k.summary}</p>
    <Lbl>Как применять</Lbl>
    <div className="card">
      {Object.keys(MODE_TEXT).map((m) => (
        <button key={m} className={`rradio ${k.mode === m ? "on" : ""}`} role="radio" aria-checked={k.mode === m} data-card-mode={m} disabled={ro} onClick={() => A.changeSkillMode(k.name, m)}>
          <span className="r" /><span>{MODE_TEXT[m][0]}</span><span className="desc">{MODE_TEXT[m][1]}{m === "manual" && EXCLUSIVE.has(k.group) ? " · один в группе" : ""}</span></button>
      ))}
    </div>
    {ro && <small>Источник pen.dev — только чтение</small>}
    {lib.error ? <><p className="error">{lib.error}</p><button className="btn line" data-retry onClick={() => A.openSkill(k.name)}>Повторить загрузку</button></>
      : !d ? <p role="status">Загрузка файлов навыка…</p>
      : <>
        <Lbl note={`${plural(d.files.length, ["файл", "файла", "файлов"])}${d.truncated ? "+" : ""} · ${sizeLabel(d.files.reduce((n, f) => n + f.size, 0))}`}>Внутри</Lbl>
        <div className="card files">{d.files.map((f) => <div className="f skill-file" key={f.name}><code>{f.name}</code><span>{sizeLabel(f.size)}</span></div>)}</div>
        <details><summary className="caption">Инструкция SKILL.md</summary><pre>{d.body}</pre></details>
        <small title={d.dir}>{d.dir}</small>
      </>}
  </>, <>
    <div className="skill-apply">
      <button className="btn primary" data-add-message disabled={k.mode === "always" || inMessage().includes(k.name)} onClick={() => A.addSkillToMessage(k)}>
        {inMessage().includes(k.name) ? "Уже в сообщении" : "В сообщение"}</button>
      <button className="btn" data-pin disabled={k.mode === "always"} onClick={() => A.togglePin(k).catch((err) => A.toast(err.message))}>
        {k.mode === "always" ? "Включён всегда" : pinned(s).includes(k.name) ? "Убрать из чата" : "Закрепить в чате"}</button>
    </div>
    <button className={`btn${s.skillPrefs.favorites.includes(k.name) ? " favorite-active" : ""}`} data-favorite={k.name} aria-pressed={s.skillPrefs.favorites.includes(k.name)} onClick={() => toggleFavorite(k.name)}><Icon n={s.skillPrefs.favorites.includes(k.name) ? "starred" : "star"} />Избранное</button>
    <span className="grow" />
    <button className="btn" data-folder onClick={() => api("/api/skill-folder", {name: k.name}).catch((err) => A.toast(err.message))}>Папка</button>
  </>];
}

// Z: how skills work, in the panel's words
const Help = () => <>
  <section><h2>Четыре уровня</h2><p>Всегда — с каждым сообщением. В чате — закреплён над полем ввода. В сообщении — чип через / на один ход; {shortcut("Enter")} в меню закрепляет его в чате, Tab переключает типы навыков. Сам — агент берёт навык по описанию, если в чате это разрешено. Ответ называет навыки, которые взял.</p></section>
  <section><h2>Группы</h2><p>Основа, Стиль, Дизайн-система, Библиотека компонентов, Платформа, Качество, Задачи и Другие. Дизайн-система — одна на чат: вторая заменяет первую. Стили и библиотеки компонентов можно сочетать. Дизайн-система в сообщении заменяет закреплённую на один ход.</p></section>
  <section><h2>Дизайн-системы</h2><p>Скиллы с локальными токенами, правилами компонентов и превью. «В сообщение» добавляет скилл на один ход, «Закрепить в чате» — для следующих сообщений. Агент читает инструкцию и локальные спецификации, создаёт переменные, стили и редактируемые компоненты выбранной системы. Внутри типа доступны фильтры: дизайн-системы, UI-киты, компоненты и блоки.</p></section>
  <section><h2>Источники</h2><p>В каталоге можно выбрать OpenDesign, Hallmark или другие источники, затем тип дизайна. Поиск и фильтры сохраняются при переходе между карточками. Миниатюра открывает карточку с полным референсом.</p><p>Проект — .figcraft/skills, мои — ~/.config/figcraft-agent/skills, встроенные, pen.dev (только чтение). При одинаковом имени побеждает первый.</p></section>
  <section><h2>Агентам</h2><p>Текст SKILL.md агент получает один раз на сессию, потом напоминание. Для режима «Сам» — описания и пути к файлам.</p></section>
  <section><h2>Новый навык — папка с SKILL.md</h2>
  <pre>{"---\nname: style-graphite\ndescription: Тихий рабочий инструмент\nmetadata:\n  group: style\n  title: Graphite\n  summary: Серые поверхности, один акцент\n  preview: \"#1C1D21 #2A2B31 #E4E6EE #8AA4FF · Inter\"\n  mode: manual\n---"}</pre>
  <p className="caption">Без metadata навык попадёт в «Другие» с режимом «Сам». Новые папки появляются без перезапуска.</p></section>
</>;

// AA: one field, its error under it, and the way without the form
function Add() {
  const [error, setError] = useState(""), [busy, setBusy] = useState(false);
  return <>
    <p>Папка со SKILL.md на этом компьютере. Её скопируют в мои навыки; папки с тем же именем останутся.</p>
    <form id="skillImport" onSubmit={async (e) => {
      e.preventDefault(); setBusy(true); setError("");
      try { await A.importSkill((e.currentTarget.elements.namedItem("folder") as HTMLInputElement).value); } catch (err) { setError((err as Error).message); setBusy(false); }
    }}>
      <label htmlFor="skillFolder">Путь к папке</label>
      <input id="skillFolder" className={error ? "bad" : ""} placeholder="~/Projects/my-skill" name="folder" required onInput={() => error && setError("")} />
      <p className="error" id="importError" role="alert">{error}</p>
      <div className="row"><span className="grow" /><button type="button" className="btn" onClick={A.libraryBack}>Отмена</button>
        <button className="btn primary" disabled={busy}>Добавить</button></div>
    </form>
    <section><h2>Или положите папку сами</h2><p>В ~/.config/figcraft-agent/skills или в .figcraft/skills проекта — навык появится в библиотеке сразу.</p></section>
  </>;
}
