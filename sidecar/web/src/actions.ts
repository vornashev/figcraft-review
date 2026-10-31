// What the page does: sending, the queue, remarks, skills, files, the server's events and the keys.
import {api, type Chat, type Comment, type Lane, type Message, type Seg, type ServerState, type Skill, type VariantSettings} from "./api";
import * as ed from "./composer";
import {CATEGORIES, EXCLUSIVE, GROUPS, REMARKS, SOURCE, commentChip, layerChip, originName, originOf, plural, remarkChip, short, skillChip} from "./lib/format";
import {agentOf, answered, autoOn, get, pinned, running, set, skillOf, waiting, type MenuKind, type State} from "./store";
import {commandKey} from "./lib/keyboard";
import {rememberSkills, skillCollection} from "./skillPrefs";
import {sourceEnabled} from "./lib/skillSources";
import {moveInSkillGrid} from "./lib/skillGrid";
import {matchesResourceKind, resourceLabels} from "./lib/designResources";

// Notices that pass: at the top, under the bar, never over the input. An action (Вернуть, Повторить) keeps one longer.
type Tone = "info" | "ok" | "danger";
export function toast(text: string, {tone = "info", action}: {tone?: Tone; action?: [string, () => void]} = {}) {
  let box = document.getElementById("toasts");
  if (!box) { box = Object.assign(document.createElement("div"), {id: "toasts"}); document.body.append(box); }
  const t = Object.assign(document.createElement("div"), {className: `toast ${tone}`, role: "status"});
  t.append(Object.assign(document.createElement("span"), {className: "grow", textContent: text}));
  if (action) {
    const b = Object.assign(document.createElement("button"), {textContent: action[0]});
    b.onclick = () => { t.remove(); action[1](); };
    t.append(b);
  }
  box.style.top = (document.getElementById("banner")?.getBoundingClientRect().bottom || 52) + 6 + "px";  // under the bar and its banner
  box.append(t);
  setTimeout(() => t.remove(), action ? 6000 : 4000);
}
const fail = (err: unknown) => toast((err as Error).message, {tone: "danger"});

export function openMenu(kind: MenuKind) { set({menu: kind, slash: null, mention: null}); }
export function closeMenu() { set({menu: null, slash: null, mention: null}); }

const lastModels: Record<string, string> = {};
export function chooseModel(agent: string, model?: string) {
  const s = get();
  if (s.S.settings.agent && s.S.settings.model) lastModels[s.S.settings.agent] = s.S.settings.model;
  if (model) lastModels[agent] = model;
  set({S: {...s.S, settings: {...s.S.settings, agent, model}}});
}
export function cycleAgent(direction: number) {
  const s = get(), agents = s.S.agents.filter((a) => a.ok);
  if (agents.length < 2) return false;
  const at = agents.findIndex((a) => a.id === s.S.settings.agent);
  const next = at < 0 ? (direction > 0 ? 0 : agents.length - 1) : (at + direction + agents.length) % agents.length;
  const a = agents[next], model = a.models.find((m) => m.id === lastModels[a.id]) || a.models[0];
  chooseModel(a.id, model?.id);
  return true;
}

// ---- sending; while the agent works, a message waits in the chat's queue ----

let draftEpoch = 0;  // uploads that finish after the draft was sent or dropped don't come back into it
const sendBody = (segs: Seg[]) => {
  const s = get();
  return {chat: s.chat?.id, segments: segs, agent: s.S.settings.agent, model: s.S.settings.model,
          ...(s.times > 1 ? {variants: s.times} : {}), ...(s.chat ? {} : {skills: pinned(), autoSkills: s.draftAuto})};
};
const sent = (chat: Chat) => set({chat, draftSkills: null, draftAuto: true, times: 1});  // ×N is for one message
export function clearDraft() { draftEpoch++; set({uploads: 0, failed: []}); ed.clearEditor(); }
export async function send() {
  if (get().uploads) return toast("Дождись загрузки файлов");
  const segs = ed.segments();
  if (!segs.length) return;
  const t = get().target;
  if (t) {  // VF: into one variant's lane — beside the run's other lanes, so never queued
    try { set({chat: await laneAct({run: t.run, n: t.n, kind: "more", segments: segs}), target: null}); clearDraft(); } catch (err) { fail(err); }
    return;
  }
  if (running()) {
    const id = get().chat!.id;
    set((s) => ({queued: {...s.queued, [id]: [...(s.queued[id] || []), segs]}}));
    rememberSkills(segs.filter((s) => s.kind === "skill" && s.name).map((s) => s.name!));
    return clearDraft();
  }
  try { sent(await api("/api/send", sendBody(segs))); rememberSkills(segs.filter((s) => s.kind === "skill" && s.name).map((s) => s.name!)); clearDraft(); } catch (err) { fail(err); }
}
export const stop = () => { set({escArmed: false}); return api("/api/stop", {chat: get().chat!.id}).catch(fail); };
// a broken turn goes on in the same chat: the agent keeps what it did
export const continueTurn = () => handoff([{kind: "text", text: "Продолжи с того места, где остановился: не повторяй сделанное"}]);
export const unqueue = (k: number) => set((s) => ({queued: {...s.queued, [s.chat!.id]: s.queued[s.chat!.id].filter((_, i) => i !== k)}}));
let flushing = false;
export async function flushQueue() {  // the next queued message once no agent works in this file
  const s = get();
  if (flushing || s.S.running.some((r) => r.file === s.S.doc.path || r.chat === s.chat?.id)) return;
  const id = Object.keys(s.queued).find((k) => s.queued[k].length && s.S.chats.some((c) => c.id === k));
  if (!id) return;
  flushing = true;
  const [segs, ...rest] = s.queued[id];
  set((st) => ({queued: {...st.queued, [id]: rest}}));
  try {
    const c = await api("/api/send", {chat: id, segments: segs, agent: s.S.settings.agent, model: s.S.settings.model});
    if (get().chat?.id === id) set({chat: c});
  } catch (err) { set((st) => ({queued: {...st.queued, [id]: [segs, ...(st.queued[id] || [])]}})); fail(err); }
  finally { flushing = false; }
}
export function newChat() {
  set({chat: null, view: "chat", start: {pick: 0, off: false}, draftSkills: null, draftAuto: true, menu: null, slash: null, mention: null, target: null});
  clearDraft(); ed.editor().focus();
}
// A chat whose context grew big goes on in a new one: its last answer, which says what was done, opens the draft.
export function freshChat(msg: Message) {
  const title = get().chat?.title || "чата";
  const said = (msg.parts || []).filter((p) => p.kind === "text").map((p) => (p as {text: string}).text).join("\n").trim();
  newChat();
  ed.insertText(`Продолжаем «${short(title, 60)}». Что сделано в прошлом чате:\n${short(said, 2000)}\n\nДальше: `);
}
export async function openChat(id: string) {
  try { set({chat: await api("/api/chat?id=" + id), view: "chat", menu: null, target: null}); ed.editor().focus(); } catch (err) { fail(err); }
}
// Deleting waits while «Вернуть» is on screen; only then does the server forget the chat.
export function deleteChat(id: string) {
  const s = get(), title = s.S.chats.find((c) => c.id === id)?.title || "Чат", wasOpen = s.chat?.id === id;
  set((st) => ({gone: [...st.gone, id], chat: wasOpen ? null : st.chat, menu: null}));
  const timer = setTimeout(() => api("/api/delete", {chat: id}).catch(fail).finally(() => set((st) => ({gone: st.gone.filter((x) => x !== id)}))), 6000);
  toast(`Чат «${short(title, 32)}» удалён`, {action: ["Вернуть", () => {
    clearTimeout(timer);
    set((st) => ({gone: st.gone.filter((x) => x !== id)}));
    if (wasOpen) openChat(id);
  }]});
}
export async function renameChat(id: string, title: string) {
  if (!title.trim()) return;
  try {
    const c: Chat = await api("/api/rename", {chat: id, title: title.trim()});
    set((s) => ({S: {...s.S, chats: s.S.chats.map((x) => x.id === id ? {...x, title: c.title} : x)}, chat: s.chat?.id === id ? c : s.chat}));
  } catch (err) { fail(err); }
}
export async function copyChat(id: string) {  // the conversation as Markdown: what was asked, what the agent said
  try {
    const c: Chat = await api("/api/chat?id=" + id);
    const said = (m: Chat["messages"][number]) => m.role === "user"
      ? (m.segments || [{kind: "text", text: m.text}]).map((x) => x.kind === "text" ? x.text : x.label ? `[${x.label}]` : "").join("")
      : (m.parts || []).filter((x) => x.kind === "text").map((x) => x.text).join("\n\n");
    const md = `# ${c.title}\n\n` + c.messages.map((m) => `**${m.role === "user" ? "Вы" : "Агент"}:** ${said(m)}`).join("\n\n") + "\n";
    await navigator.clipboard.writeText(md);
    toast("Чат скопирован как Markdown", {tone: "ok"});
  } catch (err) { fail(err); }
}

// The designer's message, to send again (to another model, say): pasted into the input it keeps its chips, pictures
// and files; anywhere else it is text, a layer as @name and a skill as /name.
export function copyMessage(segs: Seg[]) {
  const plain = segs.map((x) => x.kind === "text" ? x.text : x.kind === "layer" ? `@${x.label}` : x.kind === "skill" ? `/${x.label}`
    : x.kind === "image" || x.kind === "file" ? "" : `[${x.label}]`).join("").trim();
  const put = (e: ClipboardEvent) => { e.preventDefault(); e.clipboardData!.setData("text/plain", plain); e.clipboardData!.setData(ed.CLIP, JSON.stringify(segs)); };
  document.addEventListener("copy", put);
  const ok = document.execCommand("copy");  // the copy event is the only way to put a type of our own on the clipboard
  document.removeEventListener("copy", put);
  if (ok) toast("Сообщение скопировано", {tone: "ok"});
  else navigator.clipboard.writeText(plain).then(() => toast("Скопирован текст сообщения", {tone: "ok"}), fail);
}

// ---- an empty chat: three ways to start, or anything else in the input ----

export function startChoices(s = get()) {
  const open = s.R.list.filter((r) => r.status === "open").length + s.R.comments.filter((c) => !c.answered).length;
  const w = waiting(s).length + answered(s).length;
  const sel = (s.S.selection || []).filter((n) => !n.more);
  return [
    {title: "Пройти по замечаниям", desc: open || w ? `${open} открыто · ${w} ждёт ответа` : "Открытых замечаний нет — агент проверит файл",
     segs: (): Seg[] => [REMARKS, {kind: "text", text: " Поправь макет по открытым замечаниям"}]},
    {title: "Проверить выделенное", desc: sel.length ? `Выделено: ${short(sel[0].name, 28)}${sel.length > 1 ? ` +${sel.length - 1}` : ""}` : "Ничего не выделено — агент спросит, что смотреть",
     segs: (): Seg[] => [{kind: "text", text: "Проверь выделенное: что не так и что поправить "}, ...sel.map(layerChip)]},
    {title: "Привести к токенам", desc: "Цвета и тексты — к переменным и стилям файла",
     segs: (): Seg[] => [{kind: "text", text: "Приведи цвета и тексты к переменным и стилям файла "}, ...sel.map(layerChip)]},
  ];
}
export const startShown = (s = get()) => s.view === "chat" && !s.settingsOpen && !s.library && !s.start.off && !s.chat?.messages?.length && !ed.filled();
export async function startPicked(k = get().start.pick) {
  const c = startChoices()[k];
  if (!c) return;
  try { sent(await api("/api/send", sendBody(c.segs().filter((x) => x.kind !== "text" || x.text!.trim())))); set({start: {pick: 0, off: false}}); }
  catch (err) { fail(err); }
}

// ---- remarks ----

export async function loadRemarks() {
  const s = get();
  if (!s.S.doc.name || s.S.stale) return;
  try {
    const got = await api("/api/remarks");
    set((st) => ({R: {...st.R, list: got.remarks || [], comments: got.comments || [], error: null}}));
  }
  catch (err) { set((st) => ({R: {...st.R, error: (err as Error).message}})); }
}
export const act = (num: number, action: string, text?: string) => api("/api/remark", {num, action, text}).catch(fail);
export const actComment = (id: number, action: string, text?: string) => api("/api/comment", {id, action, text}).catch(fail);
export const fixComment = (c: Comment) => handoff([commentChip(c), {kind: "text", text: " Поправь по этому комментарию"}]);
export function showRemarks() { set({view: "remarks", menu: null}); loadRemarks(); }
export async function handoff(segs: Seg[] = [REMARKS, {kind: "text", text: " Поправь макет по открытым замечаниям"}]) {  // to the agent, in the current chat of this file or a new one
  try { sent(await api("/api/send", sendBody(segs))); set({view: "chat"}); } catch (err) { fail(err); }
}
export const fixRemark = (n: number) => { const r = get().R.list.find((x) => x.num === n); if (r) handoff([remarkChip(r), {kind: "text", text: " Поправь это замечание"}]); };
export function askRemark(n: number) {  // the remark into the input, for a question of one's own
  const r = get().R.list.find((x) => x.num === n);
  if (!r) return;
  set({view: "chat"});
  ed.insertChips([remarkChip(r)]);
}
export function remarkOrder(s = get()) {
  const by = (st: string[]) => s.R.list.filter((r) => st.includes(r.status));
  const groups = ([["open", "Открыто", by(["open"])], ["question", "Ждёт вашего ответа", by(["question"])], ["review", "Проверь", by(["review"])]] as const)
    .filter(([k, , list]) => list.length && (s.R.filter === "all" || s.R.filter === k));
  return {groups, order: groups.flatMap(([, , list]) => list), closed: by(["done", "rejected"]), by};
}
const typing = () => document.activeElement?.tagName === "INPUT" && document.activeElement.closest("#remarks");
function remarkKeys(e: KeyboardEvent) {  // ↑ ↓ move; 1–9 picks an option; Enter fixes, answers or accepts the selected one; A accepts
  const {order} = remarkOrder(), R = get().R;
  if (!order.length || typing() || e.ctrlKey || e.altKey || e.metaKey) return;
  const active = Math.min(R.active, order.length - 1), r = order[active];
  if (e.key === "ArrowDown" || e.key === "ArrowUp") {
    set({R: {...R, active: (active + (e.key === "ArrowDown" ? 1 : order.length - 1)) % order.length}});
    requestAnimationFrame(() => document.querySelector("#remarks .rcard")?.scrollIntoView({block: "nearest"}));
  } else if (r?.status === "question" && /^[1-9]$/.test(e.key) && r.options[+e.key - 1]) act(r.num, "answer", r.options[+e.key - 1]);
  else if (r?.status === "review" && (e.key === "Enter" || e.key.toLowerCase() === "a" || e.key.toLowerCase() === "ф")) act(r.num, "accept");
  else if (r?.status === "review" && (e.key.toLowerCase() === "r" || e.key.toLowerCase() === "к")) set({R: {...R, reopen: r.num}});
  else if (r?.status === "open" && e.key === "Enter") fixRemark(r.num);
  else return;
  e.preventDefault();
}

// ---- skills: / attaches some to a message, the chat pins some for every message ----

export const withSkill = (names: string[], s: Skill) => [...names.filter((n) => n !== s.name && !(EXCLUSIVE.has(s.group) && skillOf(n)?.group === s.group)), s.name];
export async function setPinned(names?: string[], auto?: boolean) {
  const added = (names || []).filter((n) => !pinned().includes(n));
  const chat = get().chat;
  if (chat) set({chat: await api("/api/skills", {chat: chat.id, skills: names, auto})});
  else set((s) => ({draftSkills: names ?? s.draftSkills, draftAuto: auto ?? s.draftAuto}));
  rememberSkills(added);
}
export function togglePin(s: Skill) {
  const now = pinned();
  return setPinned(now.includes(s.name) ? now.filter((n) => n !== s.name) : withSkill(now, s));
}
export function addSkillToMessage(skill: Skill) {
  set({library: null, settingsOpen: false, menu: null, mention: null, slash: null});
  if (!ed.inMessage().includes(skill.name)) {
    if (EXCLUSIVE.has(skill.group)) {
      ed.inMessage().filter((name) => skillOf(name)?.group === skill.group).forEach(ed.dropSkillChip);
    }
    ed.insertChips([skillChip(skill)]);
    rememberSkills([skill.name]);
  }
  ed.focusEditor();
}
export const toggleAuto = () => setPinned(undefined, !autoOn()).catch(fail);
export async function saveDefaults() {
  try { const r = await api("/api/skill-defaults", {skills: pinned()}); set((s) => ({S: {...s.S, skillDefaults: r.skillDefaults}})); } catch (err) { fail(err); }
}
export function openPinSkills() { const sources = get().slashSources, category = ed.slashCategory(undefined, sources); set({menu: "slash", mention: null, slash: {mode: "pin", q: "", i: 0, category, sources, open: new Set(), items: ed.slashItems("", new Set(), category, sources)}}); }
export function pinSlash() {
  const slash = get().slash, s = slash?.items[slash.i];
  if (!slash || !s) return;
  if (slash.mode === "message") ed.dropSkillChip(s.name);
  togglePin(s).then(() => {
    const cur = get().slash;
    if (!cur) return;
    if (cur.mode === "pin") set({slash: {...cur, items: ed.slashItems(cur.q, cur.open, cur.category, cur.sources)}}); else ed.updateSlash();
  }).catch(fail);
}
export function slashKeys(e: {key: string; shiftKey?: boolean; ctrlKey?: boolean; metaKey?: boolean; altKey?: boolean; nativeEvent?: {isComposing?: boolean}; preventDefault(): void; stopPropagation(): void}) {  // Tab changes type; ↑ ↓ move; Space ticks; Ctrl/Command+Enter pins; Enter done
  let slash = get().slash!, n = slash.items.length;
  if (e.nativeEvent?.isComposing) return false;
  if (e.altKey && !e.ctrlKey && !e.metaKey && !e.shiftKey && ["ArrowLeft", "ArrowRight"].includes(e.key)) {
    const button = document.querySelector<HTMLButtonElement>('[data-source-trigger="slash"]');
    if (!button) return false;
    e.preventDefault();
    button.click();
    return true;
  }
  if (e.key === "Enter" && commandKey({ctrlKey: !!e.ctrlKey, metaKey: !!e.metaKey}) && !e.altKey && !e.shiftKey) {
    e.preventDefault(); if (n) pinSlash(); return true;
  }
  if (e.ctrlKey || e.metaKey || e.altKey) return false;
  if (e.key === "Tab") {
    const types = ed.slashCategories(slash.sources), i = types.findIndex((c) => c.id === (slash.category || "all"));
    if (types.length < 2) return false;
    e.preventDefault();
    ed.filterSlash(types[(i + (e.shiftKey ? -1 : 1) + types.length) % types.length].id);
    return true;
  }
  if (get().slashView === "grid" && ["ArrowLeft", "ArrowRight", "ArrowUp", "ArrowDown"].includes(e.key) && n) {
    e.preventDefault();
    const cards = [...document.querySelectorAll<HTMLElement>('.menu[data-kind="slash"] [data-k]')];
    const i = moveInSkillGrid(cards.map((c) => c.getBoundingClientRect()), slash.i, e.key);
    set({slash: {...slash, i}});
    return true;
  }
  if ((e.key === "ArrowDown" || e.key === "ArrowUp") && n) {
    e.preventDefault();
    const current = slash.items[slash.i];
    if (e.key === "ArrowDown" && current && slash.items.more?.[current.group]
      && slash.items.slice(0, slash.i + 1).filter((s) => s.group === current.group).length >= 5) {
      ed.expandSlash(current.group); slash = get().slash!; n = slash.items.length;
    }
    set({slash: {...slash, i: (slash.i + (e.key === "ArrowDown" ? 1 : n - 1)) % n}});
    return true;
  }
  if (e.key === "Escape") { e.preventDefault(); e.stopPropagation(); ed.escapeSlash(); return true; }
  if (slash.mode === "pin") {
    if (e.key === "Enter" && n) { e.preventDefault(); pinSlash(); }
    return e.key === "Enter";
  }
  if (e.key === " " && n) { e.preventDefault(); ed.toggleSlash(); return true; }
  if (e.key === "Enter") {
    e.preventDefault();
    if (!slash.touched && n) ed.toggleSlash();
    ed.closeSlash(true);
    return true;
  }
  return false;
}

// ---- the skill library ----

let skillRequest = 0;
export function openLibrary() {
  const slash = get().slash, category = slash?.category, sources = slash?.sources === undefined ? get().slashSources : slash.sources;
  if (get().slash?.mode === "message") ed.closeSlash(true);
  set({menu: null, slash: null, mention: null, library: {screen: "catalog", q: "", group: "all", sources, collection: category === "recent" || category === "favorites" ? category : "all", category: category && CATEGORIES[category] ? category : "all", resourceKind: slash?.resourceKind, detail: null}});
}
export function libraryBack() {
  const lib = get().library!;
  if (lib.screen !== "catalog") { skillRequest++; set({library: {...lib, screen: "catalog", detail: null}}); }
  else { set({library: null}); if (!get().settingsOpen) ed.editor().focus(); }
}
export function librarySkills(s = get()) {
  const lib = s.library!, q = lib.q.toLowerCase().trim();
  const matching = skillCollection(s.S.skills || [], lib.collection).filter((k) => (lib.group === "all" || k.group === lib.group)
    && sourceEnabled(lib.sources ?? null, originOf(k))
    && matchesResourceKind(k, lib.category, lib.resourceKind)
    && (!lib.category || lib.category === "all" || k.category === lib.category)
    && (!q || `${k.name} ${k.title} ${k.summary} ${k.description || ""} ${SOURCE[k.source] || k.source} ${originName(k)} ${CATEGORIES[k.category || ""] || k.category || ""} ${k.style || ""} ${resourceLabels(k).join(" ")}`.toLowerCase().includes(q)));
  return lib.collection === "recent" ? matching : Object.keys(GROUPS).flatMap((g) => matching.filter((k) => k.group === g));
}
function stepSkill(delta: number) {
  const list = librarySkills(), index = list.findIndex((s) => s.name === get().library!.name);
  if (index >= 0 && list[index + delta]) openSkill(list[index + delta].name);
}
export async function openSkill(name: string) {
  const seq = ++skillRequest;
  set((s) => ({library: {...s.library!, screen: "card", name, detail: null, error: null}}));
  try {
    const detail = await api("/api/skill?name=" + encodeURIComponent(name));
    const lib = get().library;
    if (lib?.screen === "card" && lib.name === name && seq === skillRequest) set({library: {...lib, detail}});
  } catch (err) { const lib = get().library; if (lib && seq === skillRequest) set({library: {...lib, error: (err as Error).message}}); }
}
export async function changeSkillMode(name: string, mode: string) {
  try { const r = await api("/api/skill-mode", {name, mode}); set((s) => ({S: {...s.S, skills: r.skills}})); } catch (err) { fail(err); }
}
export async function importSkill(folder: string) {
  const r = await api("/api/skill-import", {folder});
  set((s) => ({S: {...s.S, skills: r.skills}, library: {...s.library!, group: "all", q: ""}}));
  openSkill(r.name);
}

// ---- files: any file of any size; pictures show as thumbnails, the rest as tiles ----

export async function addFile(file: File) {
  const epoch = draftEpoch, image = file.type.startsWith("image/");
  set((s) => ({uploads: s.uploads + 1}));
  try {
    const data = await new Promise<string>((ok, no) => { const f = new FileReader(); f.onload = () => ok(f.result as string); f.onerror = () => no(new Error("Не удалось прочитать файл")); f.readAsDataURL(file); });
    const up = await api("/api/upload", {data, type: file.type, name: file.name || ""});
    if (epoch !== draftEpoch) return;
    if (image) {
      const used = [...(get().chat?.messages || []).flatMap((m) => m.segments || []), ...ed.segments()].filter((s) => s.kind === "image");
      const n = Math.max(0, ...used.map((s, i) => +(s.label?.match(/\d+$/)?.[0] || i + 1))) + 1;
      ed.insertChips([{kind: "image", path: up.path, label: `Картинка ${n}`, icon: "image", title: file.name || "Вставленная картинка"}]);
    } else ed.insertChips([{kind: "file", path: up.path, label: file.name || "файл", size: up.size ?? file.size, icon: "attach", title: file.name}]);
  } catch (err) {
    if (epoch === draftEpoch) { set((s) => ({failed: [...s.failed, {file, error: (err as Error).message || "Связь оборвалась"}]})); fail(err); }
  } finally { if (epoch === draftEpoch) set((s) => ({uploads: Math.max(0, s.uploads - 1)})); }
}
export function addFiles(dt: {files?: FileList | File[] | null} | null) {
  const files = [...(dt?.files || [])];
  if (!files.length) return false;
  const epoch = draftEpoch;
  files.reduce((p, f) => p.then(() => { if (epoch === draftEpoch) return addFile(f); }), Promise.resolve());
  return true;
}
export function retryUpload(k: number) { const f = get().failed[k]; set((s) => ({failed: s.failed.filter((_, i) => i !== k)})); addFile(f.file); }
export function pickFiles() {
  const f = Object.assign(document.createElement("input"), {type: "file", multiple: true});
  f.onchange = () => addFiles(f);
  f.click();
}
export const openViewer = (pics: Seg[], index: number) => set({menu: null, slash: null, mention: null, gallery: {pics, index}});

// ---- the plus menu's tasks ----

export function insertTask(a: "vars" | "design") {
  if (a === "vars") { ed.focusAtCaret(); ed.insertText("Сделай 2–3 варианта по variations.md: другой визуальный язык, те же сценарии и состояния. Что поменять: "); return; }
  clearDraft(); ed.editor().focus();
  ed.insertText(get().S.designMd?.exists
    ? "Обнови DESIGN.md по product-context.md: что изменилось в продукте и макете. "
    : "Составь DESIGN.md для этого проекта по product-context.md: посмотри макет и файлы проекта, неизвестное отметь TODO с вопросом.");
}
export function insertMention() { ed.focusAtCaret(); ed.insertText(" @"); ed.updateMention(); }
// ×N: the orchestrator and the lanes are kept for every chat; a lane left unset draws with the orchestrator's agent
// ---- variants after the run (VF–VI): a lane goes on or runs again, one is taken, the run compared again ----

export const laneAct = (body: {run: string; n: number; kind: "more" | "retry" | "spread" | "adapt"; segments?: Seg[]; agent?: string; model?: string}) =>
  api<Chat>("/api/lane", {chat: get().chat!.id, ...body});
export async function runAct(path: "/api/lane" | "/api/pick" | "/api/compare", body: Record<string, unknown>, done?: string) {
  try { set({chat: await api<Chat>(path, {chat: get().chat!.id, ...body})}); if (done) toast(done); } catch (err) { fail(err); }
}
export function aimAt(t: State["target"]) {  // «Доработать»: the next message goes into this lane
  set({target: t, menu: null});
  ed.editor().focus();
}
export function mixDraft(lanes: {n: number; title: string}[]) {  // «Смешать…»: the orchestrator gets what to take from where
  ed.clearEditor();
  ed.insertText(`Смешай варианты в новой рамке: ${lanes.map((l) => `из ${l.n} «${l.title}» — …`).join("; ")}`);
  set({target: null});
  ed.editor().focus();
}
export function savePreset() {  // the lanes as they are now, named after who draws them
  const s = get(), v = s.S.settings.variants || {}, n = s.times;
  const orch = v.orchestrator || {agent: s.S.settings.agent || "claude", model: s.S.settings.model || ""};
  const lanes = Array.from({length: n}, (_, i) => v.lanes?.[i] || null);
  const who = [...new Set(lanes.map((l) => agentOf((l || orch).agent, s)?.name.split(" ")[0] || (l || orch).agent))];
  const name = `${who.join(" + ")} ×${n}`;
  const presets = [...(v.presets || []).filter((p) => p.name !== name), {name, count: n, orchestrator: v.orchestrator || null, lanes, axis: v.axis}];
  return saveVariants({presets: presets.slice(-10)});
}
export function applyPreset(name: string) {
  const s = get(), p = (s.S.settings.variants?.presets || []).find((x) => x.name === name);
  if (!p) return;
  set({times: p.count});
  return saveVariants({orchestrator: p.orchestrator, lanes: p.lanes, axis: p.axis});
}
export const dropPreset = (name: string) => saveVariants({presets: (get().S.settings.variants?.presets || []).filter((p) => p.name !== name)});
export function saveVariants(patch: Partial<VariantSettings>) {
  const v = get().S.settings.variants || {};
  return saveSettings({variants: {...v, ...patch}});
}
export function setLane(i: number, lane: Lane | null) {
  const lanes = [...(get().S.settings.variants?.lanes || [])];
  while (lanes.length <= i) lanes.push(null);
  lanes[i] = lane;
  return saveVariants({lanes});
}
export async function saveSettings(patch: Record<string, unknown>) {
  try { const r = await api("/api/settings", patch); set((s) => ({S: {...s.S, settings: {...s.S.settings, ...r}}})); } catch (err) { fail(err); }
}

// ---- the server's events ----

export function connect() {
  const es = new EventSource("/api/events");
  es.onmessage = (m) => {
    const e = JSON.parse(m.data), s = get();
    if (e.type === "state") {
      const next: ServerState = e.state;
      const docChanged = s.S.doc.path !== next.doc.path;
      if (s.S.settings.agent) next.settings = {...next.settings, agent: s.S.settings.agent, model: s.S.settings.model};
      next.selection ||= [];
      set({S: next});
      if (docChanged) {
        skillRequest++;
        set((st) => ({library: st.library && {...st.library, screen: "catalog", detail: null}, gallery: null, chat: null,
                      draftSkills: null, draftAuto: true, R: {...st.R, list: []}}));
        clearDraft(); loadRemarks();
      }
      const chat = get().chat;
      if (chat && !next.chats.some((c) => c.id === chat.id)) set({chat: null});
    } else if (e.type === "selection") set((st) => ({S: {...st.S, selection: e.selection || []}}));
    else if (e.type === "running") { set((st) => ({S: {...st.S, running: e.running}})); flushQueue(); }
    else if (e.type === "skills") set((st) => ({S: {...st.S, skills: e.skills}}));
    else if (e.type === "remarks") loadRemarks();
    else if (e.type === "chat") {
      const c: Chat = e.chat, sum = {id: c.id, title: c.title, agent: c.agent, model: c.model, updated: c.updated};
      set((st) => {
        const chats = [...st.S.chats], i = chats.findIndex((x) => x.id === c.id);
        if (c.file === st.S.doc.path) { if (i >= 0) chats[i] = sum; else chats.unshift(sum); }
        return {S: {...st.S, chats}, chat: st.chat?.id === c.id ? c : st.chat};
      });
    }
  };
  es.onerror = () => { es.close(); setTimeout(connect, 2000); };
  setInterval(() => { if (!document.hidden) loadRemarks(); }, 8000);  // the agent changes them through review.py
}

// ---- keys for the whole page ----

export function onKey(e: KeyboardEvent) {
  const s = get();
  if (e.defaultPrevented || e.isComposing) return;
  if (s.library) {
    if (e.key === "Escape") { e.preventDefault(); libraryBack(); }
    else if (s.library.screen === "card" && ["ArrowLeft", "ArrowRight"].includes(e.key)
      && !e.defaultPrevented && !e.isComposing && !e.altKey && !e.ctrlKey && !e.metaKey && !e.shiftKey
      && !(e.target as Element).closest?.("input, textarea, select, [contenteditable=true]")) {
      e.preventDefault(); stepSkill(e.key === "ArrowRight" ? 1 : -1);
    }
    return;
  }
  if (commandKey(e) && !e.shiftKey && !e.altKey && (e.code === "KeyN" || (!e.code && ["n", "т"].includes(e.key.toLowerCase())))) { e.preventDefault(); return newChat(); }
  if (commandKey(e) && !e.shiftKey && !e.altKey && (e.code === "Comma" || (!e.code && [",", "б"].includes(e.key)))) { e.preventDefault(); return set({settingsOpen: !s.settingsOpen, menu: null}); }
  if (s.menu === "chats" && ["ArrowDown", "ArrowUp", "Enter"].includes(e.key)) return chatsKeys(e);
  if (e.key !== "Escape") { if (s.view === "remarks" && !s.settingsOpen && !s.menu) remarkKeys(e); return; }
  if (s.menu) closeMenu();
  else if (s.settingsOpen) set({settingsOpen: false});
  else if (s.target) set({target: null});  // the next message goes to the chat again
  else if (s.view === "remarks") { set({view: "chat"}); ed.editor().focus(); }
  else if (running()) {  // one Esc is easy to press by chance: the second, within a moment, stops the agent
    if (s.escArmed) return stop();
    set({escArmed: true});
    clearTimeout(escTimer);
    escTimer = setTimeout(() => set({escArmed: false}), 1500);
  }
}
let escTimer: ReturnType<typeof setTimeout> | undefined;
function chatsKeys(e: KeyboardEvent) {  // ↑ ↓ through the remarks and the chats in the open menu, Enter opens
  e.preventDefault();
  const rows = [...document.querySelectorAll<HTMLElement>(".menu [data-remarks], .menu [data-id]")], i = rows.findIndex((r) => r.classList.contains("on"));
  if (e.key === "Enter") return rows[i]?.querySelector<HTMLElement>(".grow")?.click();
  rows[i]?.classList.remove("on");
  rows[(i + (e.key === "ArrowDown" ? 1 : rows.length - 1)) % rows.length]?.classList.add("on");
}
export const remarksCount = () => {
  const s = get(), open = s.R.list.filter((r) => r.status === "open").length + s.R.comments.filter((c) => !c.answered).length;
  return `${open} открыто · ${waiting(s).length + answered(s).length} ждёт ответа`;
};
export const pinnedCount = () => plural(pinned().length, ["закреплён", "закреплено", "закреплено"]);
