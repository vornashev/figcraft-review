// Remarks: filters, groups by what they wait for, the selected one opened.
import {useState} from "react";
import type {Comment, Remark} from "../api";
import {act, actComment, askRemark, fixComment, fixRemark, remarkOrder} from "../actions";
import {short} from "../lib/format";
import {set, useApp, type State} from "../store";

export function RemarkTabs() {
  const s = useApp();
  if (!s.S.doc.name) return <div className="rtabs" id="rtabs" />;
  const {by} = remarkOrder(s);
  const n = (st: string) => by([st]).length;
  const tabs: [string, string, number][] = [["all", "Все", n("open") + n("question") + n("review")], ["open", "Открыто", n("open")],
    ["question", "Вопросы", n("question")], ["review", "Проверь", n("review")]];
  return (
    <div className="rtabs" id="rtabs">
      {tabs.map(([k, l, c]) => <button key={k} className={`rtab ${s.R.filter === k ? "on" : ""}`} data-filter={k} onClick={() => set({R: {...s.R, filter: k, active: 0}})}>{l}<span>{c}</span></button>)}
    </div>
  );
}

export function Remarks() {
  const s = useApp();
  if (!s.S.doc.name) return <div className="remarks" id="remarks"><div className="rempty">FigCraft не открыт</div></div>;
  const {groups, order, closed} = remarkOrder(s);
  const comments = s.R.filter === "all" ? [...s.R.comments].sort((a, b) => Number(b.answered) - Number(a.answered)) : [];
  const active = order[Math.min(s.R.active, Math.max(order.length - 1, 0))];
  const sel = s.S.selection.filter((n) => !n.more);
  const pick = (r: Remark) => {
    const i = order.indexOf(r);
    if (i >= 0 && i !== s.R.active) set({R: {...s.R, active: i}});
    act(r.num, "go");
  };
  return (
    <div className="remarks" id="remarks">
      {s.R.error && <div className="error" style={{padding: 8}}>{s.R.error}</div>}
      {sel.length > 0 && <div className="addbox"><Field id="newRemark" placeholder={`Замечание к «${short(sel[0].name, 24)}»${sel.length > 1 ? ` +${sel.length - 1}` : ""} — Enter`} onEnter={(t) => act(0, "add", t)} /></div>}
      {groups.map(([k, l, list]) => [
        <div key={"g" + k} className={`rgroup ${k}`}><span>{l}</span><span>{list.length}</span></div>,
        ...list.map((r) => r === active || r.status === "question" ? <Card key={r.num} r={r} s={s} onPick={() => pick(r)} /> : <Row key={r.num} r={r} onPick={() => pick(r)} />),
      ])}
      {comments.length > 0 && [
        <div key="gc" className="rgroup comments"><span>Комментарии FigCraft</span><span>{comments.length}</span></div>,
        ...comments.map((c) => <CommentCard key={"c" + c.id} c={c} />),
      ]}
      {!order.length && !comments.length && <div className="rempty">{s.R.list.length ? "Здесь пусто" : "Замечаний нет. Выдели слой в FigCraft, чтобы добавить замечание"}</div>}
      {closed.length > 0 && (
        <details className="rclosed" id="closed" open={!!s.R.showClosed} onToggle={(e) => { const open = (e.target as HTMLDetailsElement).open; if (open !== !!s.R.showClosed) set({R: {...s.R, showClosed: open}}); }}>
          <summary className="rgroup closed"><span>Закрыто</span><span>{closed.length}</span></summary>
          {closed.map((r) => <Row key={r.num} r={r} onPick={() => act(r.num, "go")} />)}
        </details>
      )}
    </div>
  );
}

const meta = (r: Remark) => [r.page, r.name].filter(Boolean).join(" / ");
const said = (r: Remark) => r.replies.length ? r.replies[r.replies.length - 1] : null;

const Row = ({r, extra, onPick}: {r: Remark; extra?: string; onPick: () => void}) => (
  <button className="rrow" data-n={r.num} data-pick title={r.text} onClick={onPick}>
    <span className={`st ${r.status}`} /><span className="rtext"><span>{r.text}</span><small>{extra || meta(r)}</small></span><span className="rid">#{r.num}</span>
  </button>
);

// a text field that sends on Enter and forgets on Esc; it keeps what is typed while the list refreshes
function Field({onEnter, onEscape, ...props}: {onEnter: (t: string) => void; onEscape?: () => void} & React.InputHTMLAttributes<HTMLInputElement>) {
  const [v, setV] = useState("");
  return <input {...props} value={v} onChange={(e) => setV(e.target.value)} onKeyDown={(e) => {
    if (e.key === "Escape") { setV(""); e.currentTarget.blur(); onEscape?.(); e.stopPropagation(); }
    if (e.key !== "Enter" || !v.trim()) return;
    e.stopPropagation();  // or the page's Enter would act on the card once the field is blurred
    const t = v.trim(); setV(""); e.currentTarget.blur(); onEnter(t);
  }} />;
}

// A FigCraft comment thread: the agent fixes it and replies in the thread; the designer resolves it or answers.
function CommentCard({c}: {c: Comment}) {
  const [replying, setReplying] = useState(false);
  const where = [c.author, [c.page, c.frame].filter(Boolean).join(" / "), c.replies ? `${c.replies} отв.` : ""].filter(Boolean).join(" · ");
  return (
    <div className="rcard comment" data-comment={c.id}>
      <button className="rrow" data-pick title={c.text} onClick={() => actComment(c.id, "go")}>
        <span className={`st ${c.answered ? "review" : "open"}`} />
        <span className="rtext"><span>{c.text}</span><small>{where}</small></span>
        {c.mentions.length > 0 && <span className="rid">@{c.mentions.join(" @")}</span>}
      </button>
      {c.last && <div className="says">{c.last[0]}: {c.last[1]}</div>}
      {replying && <Field data-reply="" placeholder="Ответ в треде — Enter" autoFocus onEscape={() => setReplying(false)}
        onEnter={(t) => { setReplying(false); actComment(c.id, "reply", t); }} />}
      <div className="ractions">
        <button className="btn" data-go onClick={() => actComment(c.id, "go")}>Показать</button>
        <button className="btn grow" data-reply-open style={{justifyContent: "flex-start"}} onClick={() => setReplying(true)}>Ответить</button>
        {c.answered
          ? <><button className="btn" data-fix onClick={() => fixComment(c)}>Ещё раз</button>
            <button className="btn primary" data-resolve onClick={() => actComment(c.id, "resolve")}>Решить</button></>
          : <><button className="btn" data-resolve onClick={() => actComment(c.id, "resolve")}>Решить</button>
            <button className="btn primary" data-fix onClick={() => fixComment(c)}>Исправить</button></>}
      </div>
    </div>
  );
}

function Card({r, s, onPick}: {r: Remark; s: State; onPick: () => void}) {
  const [answer, setAnswer] = useState("");
  if (r.status === "question") {
    const go = () => { if (answer.trim()) { const t = answer.trim(); setAnswer(""); act(r.num, "answer", t); } };  // an option answers by itself
    return (
      <div className="rcard question" data-n={r.num}>
        <div className="qhead"><span>{r.question || said(r)?.[1] || r.text}</span><span className="rid">#{r.num}</span></div>
        {r.options.map((o, k) => <button key={k} className="choice" data-opt={o} onClick={() => act(r.num, "answer", o)}><span>{k + 1}</span><span><b>{o}</b></span></button>)}
        <input data-answer placeholder="Свой ответ…" value={answer} onChange={(e) => setAnswer(e.target.value)} onKeyDown={(e) => {
          if (e.key === "Escape") { setAnswer(""); e.currentTarget.blur(); e.stopPropagation(); }
          if (e.key !== "Enter" || !answer.trim()) return;
          e.stopPropagation(); e.currentTarget.blur(); go();
        }} />
        <div className="ractions"><small className="grow">{meta(r)}</small><button className="btn primary" data-answer-go disabled={!answer.trim()} onClick={go}>Ответить ↵</button></div>
      </div>
    );
  }
  if (r.status === "review") {
    const img = (kind: string, key = "") => <img src={`/api/shot?num=${r.num}&kind=${kind}&key=${key}`} alt="" />;
    const reopen = s.R.reopen === r.num, close = () => set({R: {...s.R, reopen: undefined}});
    return (
      <div className="rcard" data-n={r.num}>
        <Row r={r} extra={said(r)?.[1] || meta(r)} onPick={onPick} />
        <div className="shots">
          <figure>{r.before ? img("before") : <div className="none">нет снимка</div>}<figcaption>было</figcaption></figure>
          <figure>{r.after ? img("after", r.after) : <div className="none">снимаю…</div>}<figcaption>стало</figcaption></figure>
        </div>
        {reopen && <Field data-reopen="" placeholder="Что не так — Enter вернёт агенту" autoFocus onEscape={close} onEnter={(t) => { close(); act(r.num, "reopen", t); }} />}
        <div className="ractions"><button className="btn" data-go onClick={() => act(r.num, "go")}>Показать</button><span className="grow" />
          <button className="btn" data-back onClick={() => set({R: {...s.R, reopen: r.num}})}>Вернуть</button>
          <button className="btn primary" data-accept onClick={() => act(r.num, "accept")}>Принять A</button></div>
      </div>
    );
  }
  const txt = said(r);
  return (
    <div className="rcard" data-n={r.num}>
      <Row r={r} onPick={onPick} />
      {txt?.[1] && <div className="says">{txt[0]}: {txt[1]}</div>}
      <div className="ractions"><button className="btn" data-reject onClick={() => act(r.num, "reject")}>Отклонить</button>
        <button className="btn grow" data-ask style={{justifyContent: "flex-start"}} onClick={() => askRemark(r.num)}>Спросить</button>
        <button className="btn primary" data-fix onClick={() => fixRemark(r.num)}>Исправить ↵</button></div>
    </div>
  );
}
