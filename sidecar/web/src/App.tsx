// The window: the top bar, then the chat, the remarks, the settings or the skill library.
import {useEffect} from "react";
import {closeMenu, handoff, newChat, onKey, remarkOrder, toast} from "./actions";
import {api} from "./api";
import {plural} from "./lib/format";
import {shortcut} from "./lib/keyboard";
import {answered, remarksView, set, useApp, waiting, type State} from "./store";
import {Icon} from "./components/bits";
import {Composer} from "./components/Composer";
import {Library} from "./components/Library";
import {Menus} from "./components/Menus";
import {Messages} from "./components/Messages";
import {RemarkTabs, Remarks} from "./components/Remarks";
import {Settings} from "./components/Settings";
import {Viewer} from "./components/Viewer";

export function App() {
  const s = useApp();
  useEffect(() => {
    const click = (e: MouseEvent) => { if (!(e.target as Element).closest?.(".menu")) closeMenu(); };
    document.addEventListener("keydown", onKey);
    document.addEventListener("click", click);
    return () => { document.removeEventListener("keydown", onKey); document.removeEventListener("click", click); };
  }, []);
  const rv = remarksView(s), chatView = !s.settingsOpen && !s.library && s.view === "chat";
  return <>
    {!s.settingsOpen && !s.library && <TopBar s={s} />}
    {rv && <RemarkTabs />}
    <div id="banner"><Banner s={s} /></div>
    {chatView && <Messages />}
    {rv && <>
      <Remarks />
      <RemarkKeys s={s} />
    </>}
    {s.settingsOpen && <Settings hidden={!!s.library} />}
    {s.library && <Library />}
    {/* the input stays mounted: its text is the draft */}
    <div hidden={!chatView} style={{display: "contents"}}><Composer /></div>
    <Menus />
    <Viewer />
  </>;
}

// T: what the keys do for the selected remark, and the way back to the chat
function RemarkKeys({s}: {s: State}) {
  const {order} = remarkOrder(s), r = order[Math.min(s.R.active, Math.max(order.length - 1, 0))];
  const pairs: [string, string][] = [["↑↓", "выбрать"], ...(r?.status === "open" ? [["↵", "исправить"]] as [string, string][]
    : r?.status === "question" ? [[`1–${Math.min(r.options.length, 9) || 1}`, "ответить"]] as [string, string][]
    : r?.status === "review" ? [["A", "принять"], ["R", "вернуть"]] as [string, string][] : []), ["Esc", "к чату"]];
  return <div className="rfoot" id="rfoot">{order.length ? pairs.map(([k, v]) => [<kbd key={k}>{k}</kbd>, <span key={k + v} className="caption">{v}</span>])
    : [<kbd key="e">Esc</kbd>, <span key="c" className="caption">к чату</span>]}</div>;
}

// The file on a quiet first line, the chat on the second; the whole width up to «+» opens the chats.
function TopBar({s}: {s: State}) {
  const rv = remarksView(s), n = waiting(s).length + answered(s).length;
  return (
    <div className="top" id="top">
      <button className={`chats${s.menu === "chats" ? " open" : ""}`} id="chatsBtn" title="Чаты и замечания файла"
        onClick={(e) => { e.stopPropagation(); set({menu: s.menu === "chats" ? null : "chats", slash: null, mention: null}); }}>
        <span className="lines">
          <small id="docName">{s.S.doc.name ? s.S.doc.name + (s.S.doc.path ? "" : " · не сохранён") : "FigCraft не открыт"}</small>
          <b id="chatTitle">{rv ? "Замечания" : s.chat ? s.chat.title : "Новый чат"}</b>
        </span>
        <span className="wait" id="badge" title={`${n} ждёт ответа`} hidden={!n || rv}>{n}</span>
        <Icon n="chevron" className="chev" />
      </button>
      <button className="btn primary" id="fixAll" hidden={!rv || !s.R.list.some((r) => r.status === "open")} onClick={() => handoff()}>Исправить все</button>
      <button className="iconbtn" id="newBtn" title={`Новый чат — ${shortcut("N")}`} aria-label="Новый чат" hidden={rv} onClick={newChat}><Icon n="plus" /></button>
    </div>
  );
}

// What stays until it changes: under the bar, with the reason and what to do.
function Banner({s}: {s: State}) {
  if (s.settingsOpen) return null;
  const elsewhere = new Set(s.S.running.filter((r) => r.file && r.file !== s.S.doc.path).map((r) => r.file)).size;
  const b = (tone: string, title: string, text: string) => <div className={`banner ${tone}`}><i /><div><b>{title}</b><span>{text}</span></div></div>;
  if (s.S.stale || s.S.doc.error) return b("danger", "FigCraft не отвечает", "Окно свёрнуто, на другом рабочем столе или запущено без --control 7979. Агенты ждут, пока окно видно.");
  if (s.S.doc.name && !s.S.doc.path) return b("warn", "Сохраните файл", "Чаты хранятся рядом с файлом — у несохранённого их негде держать.");
  if (elsewhere) return b("info", `Агенты работают ещё в ${plural(elsewhere, ["файле", "файлах", "файлах"])}`, "Откройте файл в FigCraft, чтобы увидеть чат. Когда закончат — придёт уведомление.");
  const up = s.S.update;
  if (up) return <div className="banner info" data-update={up.version}><i /><div><b>Доступна версия {up.version}</b>
    <span>{up.auto ? "Скачается и установится, приложение перезапустится." : "Скачайте её на странице релиза."}</span>
    <div className="row"><button className="btn" data-update-install onClick={() => api("/api/update", {}).catch((e) => toast(e.message))}>
      {up.auto ? "Обновить" : "Открыть релиз"}</button></div></div></div>;
  return null;
}
