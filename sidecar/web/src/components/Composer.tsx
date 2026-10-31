// The input: one line when empty; attachments, text and a bottom row once there is something.
import {useEffect, useRef, useState} from "react";
import * as A from "../actions";
import * as ed from "../composer";
import {clock, layerChip, modelDescription, plural} from "../lib/format";
import {agentOf, get, modelName, pinned, running, set, useApp} from "../store";
import {Chip, FileTile, Icon, Mark, Picture} from "./bits";

const MODES: Record<string, string> = {figcraft: "Только FigCraft", terminal: "Как в терминале"};
const SHOWN = 4;  // pictures in the tray before the rest fold into «+N»

export function Composer() {
  const s = useApp(), edRef = useRef<HTMLDivElement>(null), drag = useRef(0);
  useEffect(() => { ed.mountEditor(edRef.current!); edRef.current!.focus(); }, []);
  const busy = running(s), segs = ed.segments(), live = ed.suggested();
  const pics = segs.filter((x) => x.kind === "image" && x.path), files = segs.filter((x) => x.kind === "file");
  const skillsN = segs.filter((x) => x.kind === "skill").length, layersN = segs.filter((x) => x.kind === "layer").length;
  const text = segs.filter((x) => x.kind === "text").map((x) => x.text).join("");
  const menuOpen = s.menu === "slash" || s.menu === "mention";
  const el = edRef.current;
  // one line while there is only text of one line; the attachments, chips and a bottom row once there is more
  const compact = !pics.length && !files.length && !s.uploads && !s.failed.length && !menuOpen && !el?.querySelector(".chip") && (el?.scrollHeight ?? 0) <= 24 && !/\n/.test(text);
  const pins = pinned(s).map(ed.skillName);
  const a = agentOf(s.S.settings.agent, s) || s.S.agents[0];
  const model = a?.models.find((m) => m.id === s.S.settings.model);
  const counts = [pics.length && plural(pics.length, ["картинка", "картинки", "картинок"]), files.length && plural(files.length, ["файл", "файла", "файлов"]),
                  skillsN && plural(skillsN, ["навык", "навыка", "навыков"]), layersN && plural(layersN, ["слой", "слоя", "слоёв"])].filter(Boolean);
  const queues = busy && !s.target && segs.length > 0;  // a message into a lane goes at once
  const boxHint = compact ? (queues ? "↵ в очередь" : "")
    : menuOpen ? "Esc закрыть меню" : s.uploads ? "Отправка после загрузки" : queues ? "↵ в очередь" : counts.join(" · ");
  const hint = compact ? "" : "Shift+Enter новая строка";
  const fold = pics.length > SHOWN + 1 ? pics.length - SHOWN : 0;
  const toggle = (kind: "plus" | "models" | "variants") => (e: React.MouseEvent) => { e.stopPropagation(); s.menu === kind || (kind === "models" && s.menu) ? A.closeMenu() : A.openMenu(kind); };

  const onKeyDown = (e: React.KeyboardEvent) => {
    if (e.nativeEvent.isComposing) return;
    const st = get();
    if (st.slash?.mode === "message" && st.menu === "slash" && A.slashKeys(e)) return;
    if (st.mention && st.menu === "mention") {
      const m = st.mention, n = m.items.length;
      if ((e.key === "ArrowDown" || e.key === "ArrowUp") && n) { e.preventDefault(); set({mention: {...m, i: (m.i + (e.key === "ArrowDown" ? 1 : n - 1)) % n}}); return; }
      if ((e.key === "Enter" || e.key === "Tab") && n) { e.preventDefault(); return ed.chooseMention(m.i); }
      if (e.key === "Escape") { e.preventDefault(); e.stopPropagation(); return ed.closeMention(); }
    }
    if (A.startShown() && !e.shiftKey) {  // the start card: 1–3 or ↑↓ pick, Enter starts, Esc hides it
      const pick = st.start.pick;
      const k = /^[1-3]$/.test(e.key) ? +e.key - 1 : e.key === "ArrowDown" ? (pick + 1) % 3 : e.key === "ArrowUp" ? (pick + 2) % 3 : null;
      if (k != null) { e.preventDefault(); set({start: {...st.start, pick: k}}); return; }
      if (e.key === "Enter") { e.preventDefault(); A.startPicked(); return; }
      if (e.key === "Escape") { e.preventDefault(); e.stopPropagation(); set({start: {...st.start, off: true}}); return; }
    }
    if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); A.send(); }
    else if (e.key === "Enter") { e.preventDefault(); document.execCommand("insertLineBreak"); ed.changed(); }
    else if (e.key === "Tab" && !e.ctrlKey && !e.altKey && !e.metaKey && !st.menu) {
      if (!e.shiftKey && ed.suggested().length) { e.preventDefault(); ed.insertSelection(); }
      else if (A.cycleAgent(e.shiftKey ? -1 : 1)) e.preventDefault();
    }
  };
  const dragFiles = (e: React.DragEvent) => [...(e.dataTransfer?.types || [])].includes("Files");

  return (
    <div className="composer" id="composer"
      onDragEnter={(e) => { if (!dragFiles(e)) return; e.preventDefault(); if (drag.current++) return; set({dragging: [...e.dataTransfer.items].filter((i) => i.kind === "file").length || -1}); }}
      onDragLeave={() => { if (drag.current && !--drag.current) set({dragging: 0}); }}
      onDragOver={(e) => e.preventDefault()}
      onDrop={(e) => { e.preventDefault(); drag.current = 0; set({dragging: 0}); A.addFiles(e.dataTransfer); }}>
      {(
        <div className={`pinned${s.menu === "pinned" ? " open" : ""}`} id="pinnedBtn" hidden={!pins.length}>
          <span>Закреплено в чате</span>
          <b title="Навыки этого чата" onClick={(e) => { e.stopPropagation(); s.menu === "pinned" ? A.closeMenu() : A.openMenu("pinned"); }}>{pins.join(" · ")}</b>
          <span className="chev" onClick={(e) => { e.stopPropagation(); s.menu === "pinned" ? A.closeMenu() : A.openMenu("pinned"); }}>{s.menu === "pinned" ? "⌄" : "⌃"}</span>
        </div>
      )}
      {live.length > 0 && (
        <button className="selection-suggestion" id="selectionSuggestion" title="Добавить выделенные слои в сообщение"
          onMouseDown={(e) => e.preventDefault()} onClick={() => ed.insertSelection()}>
          <span className="caption grow">Выделено в FigCraft</span><span className="caption"><kbd>Tab</kbd> вставить</span>
          <span className="selection-layers">{live.map((n) => <Chip key={n.id} c={layerChip(n)} />)}</span>
        </button>
      )}
      {busy && <Working armed={s.escArmed} chat={s.chat!.id} lanes={s.S.running.filter((r) => r.chat === s.chat!.id && r.lane).length} />}
      {s.target && (  // VF: the next message goes into this lane — its agent, session and frame
        <div className="target" id="laneTarget"><Icon n="branch" /><b className="grow">В вариант {s.target.n} · {s.target.title}</b>
          {s.target.agent && <Mark id={s.target.agent} />}<small>{modelName(agentOf(s.target.agent, s), s.target.model)}</small>
          <button aria-label="Писать оркестратору" title="Писать в чат — Esc" onClick={() => { set({target: null}); ed.editor().focus(); }}>×</button></div>
      )}
      <div className={`box${compact ? " compact" : ""}`} id="box">
        <div className="attachments" id="attachments">
          {pics.slice(0, fold ? SHOWN : pics.length).map((p, i) => (
            <div className="attachment" key={p.path! + i}><Picture s={p} i={i} onOpen={() => A.openViewer(pics, i)} />
              <button className="remove-image" data-remove={i} aria-label={`Убрать ${p.label}`} onClick={() => ed.removeChip("image", i)}>×</button></div>
          ))}
          {fold > 0 && <button className="more-tile" data-picture-more title="Все картинки" onClick={() => A.openViewer(pics, SHOWN)}><b>+{fold}</b><small>{plural(fold, ["картинка", "картинки", "картинок"]).replace(/^\d+ /, "")}</small></button>}
          {files.map((f, i) => (
            <div className="attachment" key={f.path! + i}><FileTile s={f} />
              <button className="remove-image" data-remove-file={i} aria-label={`Убрать ${f.label}`} onClick={() => ed.removeChip("file", i)}>×</button></div>
          ))}
          {Array.from({length: s.uploads}, (_, i) => <div key={"u" + i} className="attachment uploading" role="status" aria-label="Загрузка"><span /></div>)}
          {s.failed.map((f, i) => (
            <div className="failed" key={"f" + i}><div className="uploading">!</div>
              <div><b>{f.file.name || "Файл"} не загрузился</b><small>{f.error}. <button data-retry={i} onClick={() => A.retryUpload(i)}>Повторить</button> · <button data-drop={i} onClick={() => set((st) => ({failed: st.failed.filter((_, k) => k !== i)}))}>Убрать</button></small></div></div>
          ))}
        </div>
        <div className="editor blank" id="input" ref={edRef} contentEditable spellCheck={false} suppressContentEditableWarning data-placeholder={s.chat?.messages?.length ? "Уточнить. @слои. /навыки." : "Задача. @слои. /навыки."}
          onInput={() => { ed.changed(); ed.updateMention(); ed.updateSlash(); }}
          onKeyDown={onKeyDown}
          onPaste={(e) => { e.preventDefault(); if (!ed.pasteSegments(e.clipboardData) && !A.addFiles(e.clipboardData)) ed.insertText(e.clipboardData.getData("text/plain")); }} />
        <span id="boxHint">{boxHint}</span>
        <button className="send" id="sendBtn" title={busy && !s.target ? "В очередь — Enter" : "Отправить — Enter"}
          disabled={!segs.length || s.uploads > 0} onClick={() => A.send()}>↑</button>
        {s.dragging !== 0 && (
          <div className="drop" id="drop"><span>Отпустите, чтобы прикрепить {s.dragging > 0 ? plural(s.dragging, ["файл", "файла", "файлов"]) : "файлы"}</span><small>Картинки и любые файлы — без ограничений</small></div>
        )}
      </div>
      <div className="modelrow">
        <button className="plus" id="attachBtn" title="Добавить в сообщение" onClick={toggle("plus")}>+</button>
        <span className="model-control">
          <button className={`picker${s.menu === "models" ? " open" : ""}`} id="pickerBtn" aria-label="Выбрать модель и агента"
            aria-describedby={a && !s.menu ? "modelTooltip" : undefined} aria-expanded={s.menu === "models"} aria-haspopup="dialog" onClick={toggle("models")}
            onKeyDown={(e) => { if (e.key === "Tab" && !s.menu && !e.ctrlKey && !e.altKey && !e.metaKey && A.cycleAgent(e.shiftKey ? -1 : 1)) e.preventDefault(); }}>
            {a ? <><Mark id={a.id} /><b>{modelName(a, s.S.settings.model) || a.name}</b><Icon n="chevron" className="chev" /></> : "нет агентов"}
          </button>
          {a && !s.menu && <span className="model-tooltip" id="modelTooltip" role="tooltip">
            <b>{modelName(a, s.S.settings.model) || a.name}</b><span className="caption">{a.name}</span>
            {model && modelDescription(model) && <span>{modelDescription(model)}</span>}
            {s.S.settings.model && <span className="model-id">{s.S.settings.model}</span>}
            {s.S.agents.filter((a) => a.ok).length > 1 && <span className="model-shortcuts"><span><kbd>Tab</kbd> следующий агент</span><span><kbd>Shift+Tab</kbd> предыдущий агент</span></span>}
            <span className="caption">Нажмите, чтобы открыть список моделей и агентов</span>
          </span>}
        </span>
        <button className="mode" id="modeBtn" title="Доступ агента" onClick={toggle("models")}>{MODES[s.S.settings.mode] || ""}</button>
        <span className="hint" id="hint">{hint}</span>
        <button className={`times${s.times > 1 ? " on" : ""}${s.menu === "variants" ? " open" : ""}`} id="timesBtn"
          title="Варианты: оркестратор и дорожки" aria-haspopup="dialog" aria-expanded={s.menu === "variants"}
          onClick={toggle("variants")}><Icon n="branch" />×{s.times}</button>
      </div>
    </div>
  );
}

// X: while the agent works, ↵ and the round button queue a message; stopping is this row's own button, or Esc twice
const started: Record<string, number> = {};
function Working({armed, chat, lanes}: {armed: boolean; chat: string; lanes: number}) {
  const [, tick] = useState(0);
  started[chat] ??= Date.now();
  useEffect(() => { const t = setInterval(() => tick((n) => n + 1), 1000); return () => { clearInterval(t); delete started[chat]; }; }, [chat]);
  return (
    <div className="working" id="working">
      <span className="spin" /><span className="grow">{lanes ? `Работают ${plural(lanes, ["дорожка", "дорожки", "дорожек"])}` : "Работает"} · {clock((Date.now() - started[chat]) / 1000)}</span>
      <button className={`stopbtn${armed ? " armed" : ""}`} id="stopBtn" onClick={A.stop}>
        <i />{armed ? "Esc ещё раз — остановить" : "Остановить"}<kbd>Esc Esc</kbd></button>
    </div>
  );
}
