// The conversation: the start card of an empty chat, the designer's messages and the agent's answers.
import {Fragment, useEffect, useLayoutEffect, useRef, useState} from "react";
import {api, type Message, type Seg, type Step} from "../api";
import {aimAt, continueTurn, copyMessage, freshChat, mixDraft, openMenu, openViewer, runAct, showRemarks, startChoices, startPicked, toast, unqueue} from "../actions";
import {editor} from "../composer";
import {clock, duration, groupSteps, layerType, md, plural, short, splitAnswer, tokens, type Block} from "../lib/format";
import {agentOf, get, modelName, set, useApp, type State} from "../store";
import {Chip, FileTile, Icon, Mark, Md, Picture} from "./bits";

export function Messages() {
  const s = useApp(), main = useRef<HTMLElement>(null), atBottom = useRef(true);
  const chat = s.chat;
  useLayoutEffect(() => { if (atBottom.current && main.current) main.current.scrollTop = main.current.scrollHeight; });
  const onScroll = () => { const m = main.current!; atBottom.current = m.scrollHeight - m.scrollTop - m.clientHeight < 40; };
  if (!chat?.messages?.length) return <main id="main"><Start s={s} /></main>;
  const last = chat.messages.length - 1, ends: Record<string, number> = {}, current = new Map<string, number>();
  chat.messages.forEach((m, i) => {
    const r = runOf(m);
    if (r) ends[r] = i;  // the run's bar goes under whatever of it came last
    if (m.lane && (!m.lane.kind || m.lane.kind === "more" || m.lane.kind === "retry")) current.set(`${m.lane.run}:${m.lane.n}`, i);
  });
  const row = (m: Message, i: number) => m.role === "user"
    ? (m.toLane && m.auto ? <div className="automsg">Оркестратор → вариант {m.toLane.n} «{m.toLane.title}»: {short(m.text || "", 120)}</div>
      : m.auto ? <div className="automsg">Чат попросил оркестратора сравнить варианты</div> : <UserMessage msg={m} />)
    : m.lane ? <LaneCard msg={m} index={i} s={s} current={current.get(`${m.lane.run}:${m.lane.n}`) === i} />
    : <Answer msg={m} index={i} isLast={i === last} s={s} />;
  return (
    <main id="main" ref={main} onScroll={onScroll}>
      {chat.messages.map((m, i) => <Fragment key={i}>{row(m, i)}{runOf(m) && ends[runOf(m)!] === i && <RunBar run={runOf(m)!} s={s} />}</Fragment>)}
      {(s.queued[chat.id] || []).map((segs, k) => <UserMessage key={"q" + k} msg={{role: "user", segments: segs}} queue={k} />)}
    </main>
  );
}

function Start({s}: {s: State}) {
  return (
    <div className="empty">
      <div className="intro"><h1>Что поправить в макете?</h1><p>Агент видит файл, выделение и замечания. Правки появляются на холсте сразу.</p></div>
      {!s.start.off && (
        <div className="start" id="start">
          <div className="shead"><span>С чего начать</span><span>Esc</span></div>
          {startChoices(s).map((c, k) => (
            <button key={k} className={`choice ${k === s.start.pick ? "on" : ""}`} data-start={k} onClick={() => { set({start: {...s.start, pick: k}}); startPicked(k); }}>
              <span>{k + 1}</span><span><b>{c.title}</b><small>{c.desc}</small></span>
            </button>
          ))}
          <button className="other" id="startOther" onClick={() => { set({start: {...s.start, off: true}}); editor().focus(); }}>Что-то другое…</button>
          <div className="sfoot"><kbd>1–3</kbd><span className="caption">выбрать</span><button className="btn primary" id="startGo" onClick={() => startPicked()}>Начать ↵</button></div>
        </div>
      )}
    </div>
  );
}

function UserMessage({msg, queue}: {msg: Message; queue?: number}) {
  const segs: Seg[] = msg.segments || [{kind: "text", text: msg.text}];
  const pics = segs.filter((x) => x.kind === "image" && x.path), files = segs.filter((x) => x.kind === "file");
  const body = segs.filter((x) => x.kind !== "image" && x.kind !== "file");
  return (
    <div className={`umsg${queue != null ? " queued" : ""}`}>
      {pics.length > 0 && <div className="thumbs">{pics.map((p, i) => <Picture key={i} s={p} i={i} onOpen={() => openViewer(pics, i)} />)}</div>}
      {(body.length > 0 || files.length > 0) && (
        <div className="me">{files.map((f, i) => <FileTile key={i} s={f} />)}{body.map((x, i) => x.kind === "text" ? x.text : <Chip key={i} c={x} />)}</div>
      )}
      {(msg.times || 0) > 1 && <span className="caption times-note">×{msg.times} варианта · оркестратор и дорожки</span>}
      {msg.toLane && <span className="caption times-note to-lane"><Icon n="branch" />в вариант {msg.toLane.n} · {msg.toLane.title}</span>}
      {queue == null && <button className="copy" title="Скопировать сообщение: вставится с чипами" onClick={() => copyMessage(segs)}><Icon n="copy" />Копировать</button>}
      {queue != null && <span className="caption">в очереди · после этого ответа <button data-unqueue={queue} onClick={() => unqueue(queue)}>убрать</button></span>}
    </div>
  );
}

const STATUS: Record<string, string> = {ok: "✓", error: "×", run: "", stopped: "–"};
function StepRow({s}: {s: Step}) {
  const [, tick] = useState(0);
  useEffect(() => { if (s.status !== "run" || !s.t0) return; const t = setInterval(() => tick((n) => n + 1), 1000); return () => clearInterval(t); }, [s.status, s.t0]);
  const [name, ...rest] = String(s.label).split(" · ");
  const time = s.status === "run" ? (s.t0 ? clock(Math.max(0, Date.now() / 1000 - s.t0)) : "") : s.took != null ? `${s.took}s` : "";
  return <div className={`step ${s.status}`}><i>{STATUS[s.status] ?? ""}</i><span className="name">{name}</span><code>{rest.join(" · ")}</code><span className="time">{time}</span></div>;
}
const Blocks = ({list}: {list: Block[]}) => <>{list.map((p, k) => p.kind === "steps"
  ? <div className="steps" key={k}>{p.list.map((st, j) => <StepRow key={j} s={st} />)}</div>
  : <Md key={k} className={`text${p.streaming ? " streaming" : ""}`} html={md(p.text)} />)}</>;

async function answerAct(act: "show" | "undo" | "allow", index: number, tools?: string[]) {
  const chat = get().chat;
  if (!chat) return;
  try {
    if (act === "show") await api("/api/show", {chat: chat.id, index});
    else if (act === "undo") { await api("/api/undo", {chat: chat.id, index}); toast("Правки агента отменены"); }
    else set({chat: await api("/api/allow", {chat: chat.id, tools})});
  } catch (err) { toast((err as Error).message); }
}

function Answer({msg, index, isLast, s}: {msg: Message; index: number; isLast: boolean; s: State}) {
  const {head, tail, calls, says} = splitAnswer(msg.parts || [], msg.running);
  const foldKey = `${s.chat?.id}:${index}`, ch = msg.changes;
  const tools = [...new Set((msg.denied || []).map((d) => d.tool))];
  const rows = (ch?.layers || []);
  const more = ch ? ch.ids.length - rows.length : 0;
  return (
    <div className="agent" data-i={index}>
      {!!msg.skills?.length && (
        <div className="skills">Навыки{msg.skills.map((k) => (
          <span key={k.name} className={`chip skill g-${k.group}`} title={k.name}><i className="sq" /><span>{k.title}</span>{k.level === "auto" && <span className="lv auto">сам</span>}</span>
        ))}</div>
      )}
      {head.length > 0 && (
        <details className="fold" open={s.foldOpen.has(foldKey)} onToggle={(e) => {
          const open = (e.target as HTMLDetailsElement).open, f = new Set(get().foldOpen);
          if (open === f.has(foldKey)) return;
          open ? f.add(foldKey) : f.delete(foldKey); set({foldOpen: f});
        }}>
          <summary>{[calls && plural(calls, ["вызов", "вызова", "вызовов"]), says && plural(says, ["сообщение", "сообщения", "сообщений"])].filter(Boolean).join(" · ")}</summary>
          <Blocks list={groupSteps(head)} />
        </details>
      )}
      <Blocks list={groupSteps(tail)} />
      {msg.running && !msg.parts?.length && <div className="typing">Думает…</div>}
      {msg.variants && <div className="changes runline"><Icon n="branch" /><span className="grow">Варианты ×{msg.variants.count}: рамки {msg.variants.frames.map((f) => `#${f}`).join(", ")}, дорожки ниже</span></div>}
      {ch && !msg.running && (
        <div className="changed">
          <div className="chead">
            <b>Изменено на холсте</b>
            <small title={ch.ids.length ? plural(ch.ids.length, ["слой", "слоя", "слоёв"]) : undefined}>{plural(ch.steps, ["шаг", "шага", "шагов"])}</small>
            {ch.undone ? <small style={{flex: "none"}}>Отменено</small> : <>
              {ch.ids.length > 0 && <button className="btn" data-act="show" onClick={() => answerAct("show", index)}>Показать</button>}
              <button className="btn" data-act="undo" title={`edit.undo × ${ch.steps}, если поверх ничего не правили`} onClick={() => answerAct("undo", index)}>Отменить</button>
            </>}
          </div>
          {rows.map((l) => l.removed
            ? <div className="change removed" key={l.id}><i>−</i><span className="name">удалён</span><small /><code>#{l.id}</code></div>
            : <div className="change" key={l.id}><i>~</i><span className="name">{l.name}</span><small>{[l.top, layerType(l.type)].filter(Boolean).join(" · ")}</small><code>#{l.id}</code></div>)}
          {more > 0 && rows.length > 0 && <div className="change"><i>…</i><small>и ещё {plural(more, ["слой", "слоя", "слоёв"])}</small></div>}
        </div>
      )}
      {msg.error && <Broken msg={msg} isLast={isLast} s={s} />}
      {msg.saved && <div className="changes"><i>✓</i><span className="grow">Сохранил {msg.saved.split("/").slice(-2).join("/")}</span></div>}
      {!!msg.marked?.length && (
        <div className="changes"><i>✓</i><span className="grow">{msg.marked.map((m) => `#${m.num} → ${m.status === "review" ? "Проверь" : "Вопрос"}`).join(", ")}</span>
          <button className="btn" data-act="remarks" onClick={showRemarks}>Замечания ›</button></div>
      )}
      {!!msg.denied?.length && isLast && !msg.running && (
        <div className="deny"><b>Не хватило доступа</b>{msg.denied.map((d, k) => <code key={k}>{d.label}</code>)}
          <div className="row"><span className="caption">только в этом чате</span>
            <button className="btn primary" data-act="allow" title={tools.join(", ")} onClick={() => answerAct("allow", index, tools)}>Разрешить и продолжить</button></div>
        </div>
      )}
      {!msg.running && (msg.usage || msg.took || msg.cost) ? <Stats msg={msg} open={s.statsOpen} /> : null}
      {isLast && !msg.running && (msg.usage?.context || 0) >= BIG_CONTEXT && (
        <div className="deny bigctx"><b>Контекст {tokens(msg.usage!.context!)}</b>
          <span>Каждый запрос агента перечитывает его целиком — так быстро уходят лимиты. Дальше дешевле в новом чате.</span>
          <div className="row"><span className="caption">черновик возьмёт итог этого ответа</span>
            <button className="btn primary" data-act="fresh" onClick={() => freshChat(msg)}>Новый чат с итогом</button></div>
        </div>
      )}
    </div>
  );
}

const runOf = (m: Message) => m.lane?.run || m.compare || m.variants?.run || m.toLane?.run;
const KIND: Record<string, string> = {more: "Доработка", spread: "Перенос на экраны", adapt: "Адаптив"};

// VC, VD, VF: one variant, drawn by its own agent in its own frame: the direction, how far it got, its own Показать /
// Отменить; once done — «Доработать» (the next message goes into it) and «Беру этот», or, broken, «Повторить» by any
// agent. «Подробнее» opens the whole answer, as any other.
function LaneCard({msg, index, s, current}: {msg: Message; index: number; s: State; current: boolean}) {
  const l = msg.lane!, ch = msg.changes, a = agentOf(msg.agent, s);
  const [open, setOpen] = useState(false);
  const [again, setAgain] = useState(`${msg.agent}/${msg.model || ""}`);
  const steps = (msg.parts || []).filter((p): p is Step => p.kind === "step"), now = steps[steps.length - 1];
  const stopped = !msg.running && !msg.error && steps.some((p) => p.status === "stopped");
  const state = msg.running ? "run" : msg.error ? "error" : stopped ? "stopped" : "done";
  const head = s.chat?.messages.find((m) => m.variants?.run === l.run), picked = head?.variants?.picked;
  const taken = !!picked && !picked.undone;
  const retry = () => { const [agent, ...model] = again.split("/"); runAct("/api/lane", {run: l.run, n: l.n, kind: "retry", agent, model: model.join("/")}); };
  return (
    <div className={`lane ${state}${msg.retried ? " retried" : ""}${taken && current && picked!.n === l.n ? " picked" : ""}`} data-lane={l.n} data-i={index}>
      <div className="lhead"><b className="num">{l.n}</b><Mark id={msg.agent} />
        <span className="idea" title={l.note || l.idea}>{l.kind && KIND[l.kind] ? `${KIND[l.kind]} · ${l.title}` : l.title}</span>
        {state === "run" ? <><small>{plural(steps.length, ["шаг", "шага", "шагов"])}</small><i className="live" /></>
          : <span className={state === "done" ? "ok" : "bad"}>{state === "done" ? "✓" : state === "stopped" ? "–" : "×"}</span>}</div>
      <div className="lmeta"><span>{modelName(a, msg.model) || a?.name}</span>
        {l.styleTitle && <span className="chip skill g-style"><i className="sq" /><span>{l.styleTitle}</span></span>}
        <code>#{l.frame}</code>{msg.retried && <small>попытка, запущена снова</small>}</div>
      {state === "run" && now && <StepRow s={now} />}
      {msg.error && <div className="error">{short(msg.error, 160)}</div>}
      {!msg.running && (
        <div className="lfoot">
          <small>{ch?.undone ? "Отменено" : ch ? plural(ch.steps, ["шаг", "шага", "шагов"]) + (msg.took ? ` · ${duration(msg.took)}` : "") : "без правок"}</small>
          <span className="grow" />
          <button className="btn" data-act="details" aria-expanded={open} onClick={() => setOpen(!open)}>{open ? "Свернуть" : "Подробнее"}</button>
          {ch && !ch.undone && <>
            {ch.ids.length > 0 && <button className="btn" data-act="show" onClick={() => answerAct("show", index)}>Показать</button>}
            <button className="btn" data-act="undo" onClick={() => answerAct("undo", index)}>Отменить</button>
          </>}
        </div>
      )}
      {!msg.running && current && state === "done" && !msg.retried && (
        <div className="lnext">
          <button className="btn" data-lane-act="more" title="Следующее сообщение — в эту дорожку: её агент, сессия и рамка"
            onClick={() => aimAt({run: l.run, n: l.n, title: l.title, agent: msg.agent, model: msg.model})}>Доработать</button>
          {!taken && <button className="btn" data-lane-act="pick" title="Остальные рамки запуска и их токены — убрать, этот — оставить. Одним шагом отмены"
            onClick={() => runAct("/api/pick", {run: l.run, n: l.n}, `Взят вариант ${l.n}`)}>Беру этот</button>}
        </div>
      )}
      {!msg.running && current && state !== "done" && !msg.retried && (
        <div className="lnext">
          <small>Ещё раз</small>
          <select className="vsel" aria-label="Агент и модель повтора" value={again} onChange={(e) => setAgain(e.currentTarget.value)}>
            {s.S.agents.filter((x) => x.ok).map((x) => <optgroup key={x.id} label={x.name}>
              {x.models.map((m) => <option key={m.id} value={`${x.id}/${m.id}`}>{m.name}</option>)}</optgroup>)}
          </select>
          <span className="grow" />
          <button className="btn primary" data-lane-act="retry" onClick={retry}>Повторить</button>
        </div>
      )}
      {open && <Answer msg={{...msg, changes: undefined, error: undefined}} index={index} isLast={false} s={s} />}
    </div>
  );
}

// VG: under a run — its time and cost (where the CLI reports one), then what to do with it: mix, compare again; once
// one is taken, carry it on to the other screens or to other widths, or put everything back.
function RunBar({run, s}: {run: string; s: State}) {
  const ms = s.chat!.messages, head = ms.find((m) => m.variants?.run === run);
  if (!head) return null;
  const v = head.variants!, all = ms.filter((m) => m.role === "assistant" && (m === head || m.lane?.run === run || m.compare === run));
  const working = all.filter((m) => m.running).length;
  const cost = all.reduce((sum, m) => sum + (m.cost || 0), 0);
  const free = [...new Set(all.filter((m) => !m.running && m.cost == null).map((m) => agentOf(m.agent, s)?.name || m.agent))];
  const took = v.started && v.ended ? Math.round(v.ended - v.started) : 0;  // wall time, in whole minutes once long
  const lanes = new Map<number, {n: number; title: string}>();
  ms.forEach((m) => { if (m.lane?.run === run && !m.lane.kind) lanes.set(m.lane.n, {n: m.lane.n, title: m.lane.title}); });
  const p = v.picked && !v.picked.undone ? v.picked : null;
  const removed = p ? [p.frames.length && plural(p.frames.length, ["рамка", "рамки", "рамок"]),
    p.collections && plural(p.collections, ["коллекция", "коллекции", "коллекций"]), p.styles && plural(p.styles, ["стиль", "стиля", "стилей"])].filter(Boolean) : [];
  const gone = p ? [removed.length && `убрано: ${removed.join(", ")}`, p.collection && `«${p.collection}» теперь коллекция файла`].filter(Boolean).join("; ") : "";
  return (
    <div className="runbar" data-run={run}>
      <div className="rhead"><Icon n="branch" /><b>Варианты ×{v.count}{took ? ` · ${took >= 60 ? `${Math.round(took / 60)} мин` : `${took} с`}` : ""}</b><span className="grow" />
        <small>{working ? `работают ${working}` : [cost ? `$${cost.toFixed(2)}` : "", free.length ? `${free.join(", ")} без цены` : ""].filter(Boolean).join(" · ")}</small></div>
      {p && <p className="caption">Взят вариант {p.n} «{p.title}»{gone ? `: ${gone}` : ""}.</p>}
      {v.picked?.undone && <p className="caption">Выбор отменён: рамки и токены вернулись.</p>}
      {!working && <div className="row">
        {p ? <>
          <button className="btn primary" data-run-act="spread" title="Победитель в своей сессии переоформит остальные экраны"
            onClick={() => runAct("/api/lane", {run, n: p.n, kind: "spread"})}>Перенести на экраны</button>
          <button className="btn" data-run-act="adapt" onClick={() => runAct("/api/lane", {run, n: p.n, kind: "adapt"})}>Адаптив</button>
          <span className="grow" />
          <button className="btn" data-run-act="unpick" title="edit.undo выбора, если поверх ничего не правили"
            onClick={() => runAct("/api/pick", {run, undo: true}, "Выбор отменён")}>Отменить</button>
        </> : <>
          {lanes.size > 1 && <button className="btn" data-run-act="mix" title="Оркестратор соберёт новый вариант из частей этих"
            onClick={() => mixDraft([...lanes.values()])}>Смешать…</button>}
          <span className="grow" />
          <button className="btn" data-run-act="compare" onClick={() => runAct("/api/compare", {run})}>Сравнить снова</button>
        </>}
      </div>}
    </div>
  );
}

// Q, R: the turn broke or the subscription ran out: what is kept, and the way on
// not a bare "usage": a CLI's argument error prints "Usage: …"
const LIMIT = /usage.?limit|rate.?limit|limit (?:reached|exceeded)|hit your limit|quota|лимит|исчерпан/i;
function Broken({msg, isLast, s}: {msg: Message; isLast: boolean; s: State}) {
  const steps = (msg.parts || []).filter((p) => p.kind === "step"), done = steps.filter((p) => p.status === "ok").length;
  const limit = LIMIT.test(msg.error || ""), who = agentOf(msg.agent, s)?.name || "агента";
  const title = limit ? `Закончился лимит ${who}` : steps.length ? `Ход прервался на шаге ${done + 1}` : "Ход прервался";
  const kept = done ? `Сделано шагов: ${done}, они на холсте. ` : "";
  return (
    <div className={`banner ${limit ? "warn" : "danger"} notice`}><i /><div>
      <b>{title}</b><span>{kept}{msg.error}</span>
      {isLast && !msg.running && <div className="row">
        {limit && <button className="btn" data-act="model" onClick={(e) => { e.stopPropagation(); openMenu("models"); }}>Другая модель…</button>}
        <button className="btn primary" data-act="continue" onClick={continueTurn}>{done ? `Продолжить с шага ${done + 1}` : "Продолжить"}</button>
      </div>}
    </div></div>
  );
}

const BIG_CONTEXT = 200_000;  // tokens: past this a chat's every request costs more than a fresh chat's whole turn

// What the turn took, folded under one line; open or closed, every answer follows the last choice.
function Stats({msg, open}: {msg: Message; open: boolean}) {
  const u = msg.usage || {};
  // everything the model read: the CLIs count the cached part apart, so their bare "input" is only the new tail
  const input = (u.input || 0) + (u.cacheRead || 0) + (u.cacheWrite || 0);
  const rows = ([
    ["Стоимость", msg.cost ? `$${msg.cost.toFixed(2)}` : null],
    ["Входящие токены", input],
    ["Исходящие токены", u.output],
    ["Чтение кэша", u.cacheRead],
    ["Запись в кэш", u.cacheWrite],
    ["Контекст", u.context ? `${tokens(u.context)}${u.window ? ` из ${tokens(u.window)}` : ""}` : null],
    ["Запросов к модели", u.turns ? String(u.turns) : null],
    ["Подготовка", msg.phases?.prep != null ? `${msg.phases.prep} с` : null],
    ["До первого ответа", msg.phases?.first != null ? `${msg.phases.first} с` : null],
  ] as [string, string | number | null | undefined][]).filter(([, v]) => v != null && v !== 0);
  const head = [msg.took ? `Работал ${duration(msg.took)}` : "Готово", msg.cost ? `$${msg.cost.toFixed(2)}` : ""].filter(Boolean).join(" · ");
  return (
    <details className="stats" open={open} onToggle={(e) => {
      const now = (e.target as HTMLDetailsElement).open;
      if (now === get().statsOpen) return;
      set({statsOpen: now});
      try { localStorage.setItem("statsOpen", now ? "1" : "0"); } catch { /* no storage */ }
    }}>
      <summary>{head}</summary>
      {rows.length > 0 && <dl>{rows.map(([k, v]) => [<dt key={k + "t"}>{k}</dt>, <dd key={k + "d"}>{typeof v === "number" ? tokens(v) : v}</dd>])}</dl>}
    </details>
  );
}
