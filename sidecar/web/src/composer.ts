// The input: text with chips inline, each chip one character for the caret. The editor is a contenteditable React
// never re-renders; these functions edit it and bump `draft` so the rest of the composer follows.
import {api, type Layer, type Remark, type Seg} from "./api";
import {CATEGORIES, EXCLUSIVE, esc, layerChip, originName, originOf, remarkChip, skillChip} from "./lib/format";
import {iconSvg, isIcon} from "./lib/icons";
import {get, pinned, set, skillOf, type MentionItem, type SkillList} from "./store";
import {rememberSkills, setSkillSources, skillCollection} from "./skillPrefs";
import {skillOrigins, sourceEnabled, type SkillSources} from "./lib/skillSources";
import {matchesResourceKind, resourceLabels} from "./lib/designResources";

let ed: HTMLDivElement = document.createElement("div");
let caret: Range | null = null;
export const editor = () => ed;
export function focusEditor() {
  const saved = caret?.cloneRange();
  ed.focus();
  if (saved && ed.contains(saved.startContainer)) placeCaret(saved);
}
export function mountEditor(el: HTMLDivElement) {
  ed = el;
  for (const ev of ["keyup", "mouseup", "input"]) ed.addEventListener(ev, keepCaret);
}
function keepCaret() {
  const s = getSelection()!;
  if (s.rangeCount && ed.contains(s.anchorNode)) caret = s.getRangeAt(0).cloneRange();
}
document.addEventListener("selectionchange", keepCaret);

export function chipMarkHtml(c: Seg) {  // a skill's group colour, @ for a layer, a ring for a remark
  if (c.kind === "skill") return `<i class="sq"></i>`;
  if (c.kind === "layer") return `<i class="at">@</i>`;
  if (c.kind === "remark") return `<i class="ring"></i>`;
  if (c.kind === "remarks") return `<i class="sq" style="--g:var(--orange)"></i>`;
  return `<i>${isIcon(c.icon) ? iconSvg(c.icon) : esc(c.icon || "#")}</i>`;
}
function chipEl(c: Seg) {
  const s = document.createElement("span");
  s.className = "chip " + c.kind + (c.group ? " g-" + c.group : "");
  s.contentEditable = "false";
  const d = s.dataset;
  if (c.name) d.name = c.name;
  if (c.group) d.group = c.group;
  d.kind = c.kind;
  if (c.id != null) d.id = String(c.id);
  if (c.num != null) d.num = String(c.num);
  if (c.path) d.path = c.path;
  if (c.size != null) d.size = String(c.size);
  d.label = c.label || "";
  d.icon = c.icon || "";
  s.title = c.title || c.label || "";
  s.innerHTML = `${chipMarkHtml(c)}<span>${esc(c.label)}</span>`;
  return s;
}
export function placeCaret(r: Range) { const s = getSelection()!; s.removeAllRanges(); s.addRange(r); caret = r.cloneRange(); }
export function focusAtCaret() { ed.focus(); if (caret) placeCaret(caret); }
export function insertText(t: string) { document.execCommand("insertText", false, t); changed(); }

export function insertChips(list: Seg[]) {
  insertNodes(list.flatMap((c) => [chipEl(c), document.createTextNode(" ")]));
}

// A copied message (see copyMessage): its segments ride the clipboard beside the plain text, so a paste gets
// the chips, pictures and files back, not their labels.
export const CLIP = "application/x-figcraft-segments";
export function pasteSegments(dt: DataTransfer | null) {
  let list: Seg[];
  try { list = JSON.parse(dt?.getData(CLIP) || ""); } catch { return false; }
  if (!Array.isArray(list) || !list.length || !list.every((c) => c && typeof c.kind === "string")) return false;
  insertNodes(list.map((c) => c.kind === "text" ? document.createTextNode(c.text || "") : chipEl(c)));
  return true;
}

function insertNodes(nodes: Node[]) {
  if (!nodes.length) return;
  const live = getSelection()!;
  let r: Range | null = document.activeElement === ed && live.rangeCount && ed.contains(live.anchorNode) ? live.getRangeAt(0)
    : caret && ed.contains(caret.startContainer) ? caret : null;
  ed.focus();
  if (!r) { r = document.createRange(); r.selectNodeContents(ed); r.collapse(false); }
  r.deleteContents();
  const frag = document.createDocumentFragment();
  const before = r.startContainer.nodeType === 3 ? (r.startContainer as Text).data.slice(0, r.startOffset) : "";
  if (before && !/\s$/.test(before)) frag.append(document.createTextNode(" "));
  frag.append(...nodes);
  let last = nodes[nodes.length - 1];
  if (last.nodeType !== 3) { last = document.createTextNode(" "); frag.append(last); }  // the caret can't sit in a chip
  r.insertNode(frag);
  const after = document.createRange();
  after.setStart(last, (last as Text).length);
  after.collapse(true);
  placeCaret(after);
  changed();
}

export function segments(): Seg[] {
  const out: Seg[] = [];
  const push = (t: string) => {
    if (!t) return;
    const l = out[out.length - 1];
    if (l?.kind === "text") l.text += t; else out.push({kind: "text", text: t});
  };
  const walk = (n: Node) => {
    for (const c of n.childNodes) {
      const d = (c as HTMLElement).dataset;
      if (c.nodeType === 3) push((c as Text).data.replace(/​/g, ""));
      else if (d?.kind) out.push({kind: d.kind, id: d.id ? +d.id : undefined, num: d.num ? +d.num : undefined, path: d.path,
                                  size: d.size ? +d.size : undefined, name: d.name, group: d.group,
                                  label: d.label, icon: d.icon, title: (c as HTMLElement).title});
      else if (c.nodeName === "BR") push("\n");
      else { if (c.nodeName === "DIV" && out.length) push("\n"); walk(c); }
    }
  };
  walk(ed);
  const last = out[out.length - 1], first = out[0];
  if (last?.kind === "text") last.text = last.text!.replace(/\s+$/, "");
  if (first?.kind === "text") first.text = first.text!.replace(/^\s+/, "");
  return out.filter((s) => s.kind !== "text" || s.text);
}
export const filled = () => segments().length > 0;
const inEditor = () => new Set(segments().filter((s) => s.kind === "layer").map((s) => s.id));
export const suggested = () => (get().S.selection || []).filter((n) => !n.more && !inEditor().has(n.id));
export const insertSelection = () => insertChips(suggested().map(layerChip));

export function changed() {
  ed.classList.toggle("blank", !ed.textContent && !ed.querySelector(".chip"));
  if (ed.innerHTML === "<br>") ed.innerHTML = "";
  set((s) => ({draft: s.draft + 1}));
}
export function clearEditor() { ed.innerHTML = ""; caret = null; changed(); }
export function removeChip(kind: string, k: number) { ed.querySelectorAll(`[data-kind="${kind}"]`)[k]?.remove(); changed(); }

// ---- @ and / : what the text just before the caret asks for ----

type At = {node: Text; start: number; end: number; q: string};
function queryAt(re: RegExp): At | null {
  const s = getSelection()!;
  if (!s.rangeCount || !s.isCollapsed) return null;
  const n = s.anchorNode, o = s.anchorOffset;
  if (n?.nodeType !== 3 || !ed.contains(n)) return null;
  const m = (n as Text).data.slice(0, o).match(re);
  return m ? {node: n as Text, start: o - m[2].length - 1, end: o, q: m[2]} : null;
}
const mentionAt = () => queryAt(/(^|\s)@([^\s@]{0,40})$/);
const slashAt = () => queryAt(/(^|\s)\/([^\s/]{0,40})$/);

let mentionTimer: ReturnType<typeof setTimeout> | undefined;
export function updateMention() {
  const at = mentionAt();
  if (!at) return closeMention();
  clearTimeout(mentionTimer);
  mentionTimer = setTimeout(async () => {
    const r = await api("/api/search?q=" + encodeURIComponent(at.q)).catch(() => null);
    const cur = mentionAt();
    if (!r || !cur || cur.q !== at.q) return;
    const items: MentionItem[] = [
      ...r.remarks.map((x: Remark) => ({c: remarkChip(x), desc: x.name || x.page || "", status: x.status})),
      ...r.layers.map((l: Layer) => ({c: layerChip(l), desc: [String(l.type || "").toLowerCase(), l.size || l.path].filter(Boolean).join(" · "),
                                      mauve: /^(COMPONENT|COMPONENT_SET|INSTANCE)$/.test(l.type || "")}))];
    set({menu: "mention", slash: null, mention: {q: cur.q, i: 0, items, indexing: r.indexing}});
    if (r.indexing) setTimeout(updateMention, 800);
  }, 120);
}
export function closeMention() {
  clearTimeout(mentionTimer);
  const s = get();
  if (s.mention || s.menu === "mention") set({mention: null, menu: s.menu === "mention" ? null : s.menu});
}
export function chooseMention(k: number) {
  const c = get().mention?.items[k]?.c, at = mentionAt();
  closeMention();
  if (!c || !at) return;
  const r = document.createRange();
  r.setStart(at.node, at.start); r.setEnd(at.node, at.end);
  ed.focus(); placeCaret(r);
  insertChips([c]);
}

let slashOff: {node: Text; start: number} | null = null;  // where Esc closed the menu, so typing on doesn't reopen it there
export const inMessage = () => [...ed.querySelectorAll<HTMLElement>(".chip.skill")].map((c) => c.dataset.name!);
export const slashOrigins = () => skillOrigins((get().S.skills || []).filter((k) => k.mode !== "always"));
export function slashCategories(sources = get().slashSources) {
  const skills = (get().S.skills || []).filter((k) => k.mode !== "always" && sourceEnabled(sources, originOf(k)));
  return [{id: "all", label: "Все", count: skills.length},
    {id: "recent", label: "Недавние", count: skillCollection(skills, "recent").length},
    {id: "favorites", label: "Избранное", count: skillCollection(skills, "favorites").length},
    ...Object.entries(CATEGORIES).map(([id, label]) => ({id, label, count: skills.filter((k) => k.category === id).length})),
    {id: "general", label: "Общие", count: skills.filter((k) => !k.category || !CATEGORIES[k.category]).length}].filter((c) => ["all", "recent", "favorites"].includes(c.id) || c.count > 0);
}
export const slashCategory = (category = get().slashCategory, sources = get().slashSources) => slashCategories(sources).some((c) => c.id === category) ? category : "all";
export function filterSlash(category: string) {
  const s = get(), slash = s.slash;
  if (!slash) return;
  const sources = slash.sources === undefined ? get().slashSources : slash.sources;
  category = slashCategory(category, sources);
  const open = new Set<string>();
  set({slashCategory: category, slash: {...slash, category, resourceKind: "all", sources, i: 0, open, items: slashItems(slash.q, open, category, sources, "all")}});
}
export function filterSlashResourceKind(resourceKind: string) {
  const slash = get().slash;
  if (!slash) return;
  const open = new Set<string>();
  set({slash: {...slash, resourceKind, open, i: 0, items: slashItems(slash.q, open, slash.category, slash.sources, resourceKind)}});
}
export function filterSlashSources(sources: SkillSources) {
  const slash = get().slash;
  if (!slash) return;
  const active = slash.items[slash.i]?.name;
  const category = slashCategory(slash.category, sources), open = new Set<string>();
  const items = slashItems(slash.q, open, category, sources);
  setSkillSources(sources);
  set({slashCategory: category, slash: {...slash, sources, category, open, items, i: Math.max(0, items.findIndex((k) => k.name === active))}});
}
export function setSlashView(view: "list" | "grid" | "preview") {
  const slash = get().slash, active = slash?.items[slash.i]?.name;
  try { localStorage.setItem("figcraft.skillView", view); } catch { /* the current window still works */ }
  set({slashView: view});
  if (!slash) return;
  const open = new Set([...slash.open, ...slash.items.map((k) => k.group)]);
  const items = slashItems(slash.q, open, slash.category, slash.sources);
  set({slash: {...slash, open, items, i: Math.max(0, items.findIndex((k) => k.name === active))}});
}
export function slashItems(q: string, open = new Set<string>(), category = slashCategory(), sources = get().slashSources, resourceKind = get().slash?.resourceKind): SkillList {  // without a query a big group shows a few, the chosen ones and «ещё N»
  q = q.toLowerCase();
  const all = skillCollection(get().S.skills || [], category).filter((s) => s.mode !== "always"
    && sourceEnabled(sources, originOf(s))
    && matchesResourceKind(s, category, resourceKind)
    && (["all", "recent", "favorites"].includes(category) || (category === "general" ? !s.category || !CATEGORIES[s.category] : s.category === category))
    && (!q || `${s.name} ${s.title} ${s.summary} ${originName(s)} ${CATEGORIES[s.category || ""] || ""} ${s.style || ""} ${resourceLabels(s).join(" ")} ${q.length > 2 ? s.description || "" : ""}`.toLowerCase().includes(q)));
  if (q || category === "recent" || category === "favorites") return all;
  const keep = new Set([...inMessage(), ...pinned()]), out: SkillList = [];
  out.more = {};
  for (const g of new Set(all.map((s) => s.group))) {
    const of = all.filter((s) => s.group === g);
    const shown = get().slashView === "list" && of.length > 7 && !open.has(g) ? of.filter((s, k) => k < 5 || keep.has(s.name)) : of;
    out.push(...shown);
    if (shown.length < of.length) out.more[g] = of.length - shown.length;
  }
  return out;
}
export function expandSlash(group?: string) {
  const slash = get().slash;
  if (!slash?.items.more) return;
  const groups = group ? [group] : Object.keys(slash.items.more);
  if (!groups.some((g) => slash.items.more?.[g])) return;
  const active = slash.items[slash.i]?.name, open = new Set([...slash.open, ...groups]);
  const items = slashItems(slash.q, open, slash.category, slash.sources);
  set({slash: {...slash, open, items, i: Math.max(0, items.findIndex((s) => s.name === active))}});
}
export function updateSlash() {
  const cur = get().slash;
  if (cur?.mode === "pin") return;
  const at = slashAt();
  if (!at || (slashOff?.node === at.node && slashOff.start === at.start)) return closeSlash();
  const open = cur?.open || new Set<string>();
  const sources = cur?.sources === undefined ? get().slashSources : cur.sources, category = slashCategory(cur?.category, sources);
  set({menu: "slash", mention: null, slash: {mode: "message", q: at.q, category, resourceKind: cur?.resourceKind, sources, i: cur && cur.q === at.q ? cur.i : 0, touched: cur?.touched, open, items: slashItems(at.q, open, category, sources)}});
}
export function closeSlash(dropQuery?: boolean) {
  const s = get().slash;
  if (!s) return;
  if (dropQuery && s.mode === "message") {
    rememberSkills(inMessage());
    const at = slashAt();
    if (at) { const r = document.createRange(); r.setStart(at.node, at.start); r.setEnd(at.node, at.end); r.deleteContents(); placeCaret(r); changed(); }
  }
  set((st) => ({slash: null, menu: st.menu === "slash" ? null : st.menu}));
}
function dropChip(c: Element, keep?: Node) {  // a chip and the space after it, unless that text is `keep` (the caret is in it)
  const n = c.nextSibling;
  if (n?.nodeType === 3 && n !== keep && (n as Text).data.startsWith(" ")) { (n as Text).data = (n as Text).data.slice(1); if (!(n as Text).data) n.remove(); }
  c.remove();
}
export function toggleSlash() {  // the chosen skill in or out of the message; its chip goes just before the /query
  const slash = get().slash, s = slash?.items[slash.i], at = slashAt();
  if (!slash || !s || !at) return;
  set({slash: {...slash, touched: true}});
  const mine = [...ed.querySelectorAll<HTMLElement>(".chip.skill")];
  const had = mine.filter((c) => c.dataset.name === s.name);
  if (had.length) had.forEach((c) => dropChip(c, at.node));
  else {
    if (EXCLUSIVE.has(s.group)) mine.filter((c) => c.dataset.group === s.group).forEach((c) => dropChip(c, at.node));
    const tail = at.node.splitText(at.start);
    tail.before(chipEl(skillChip(s)), document.createTextNode(" "));
    const r = document.createRange();
    r.setStart(tail, at.end - at.start); r.collapse(true);
    placeCaret(r);
  }
  changed();
  updateSlash();
}
export function dropSkillChip(name: string) { ed.querySelectorAll<HTMLElement>(".chip.skill").forEach((c) => c.dataset.name === name && dropChip(c, slashAt()?.node)); }
export function escapeSlash() {
  if (get().slash?.mode === "message") { const at = slashAt(); slashOff = at && {node: at.node, start: at.start}; }
  closeSlash(false); ed.focus();
}
export function openSlashInText() {
  focusAtCaret();
  slashOff = null;
  insertText(ed.textContent && !/\s$/.test(ed.textContent) ? " /" : "/");
  updateSlash();
}
export const skillName = (n: string) => skillOf(n)?.title || n;
