// The page's state in one place: components read it with useApp(), actions change it with set().
import {useSyncExternalStore} from "react";
import {flushSync} from "react-dom";
import type {Chat, Comment, Remark, ServerState, Seg, Skill, SkillDetail} from "./api";
import {parseSkillPrefs, PREFS_KEY, type SkillPrefs} from "./lib/skillPrefs";
import {parseSkillSources, SOURCES_KEY, type SkillSources} from "./lib/skillSources";

export type MenuKind = "chats" | "plus" | "models" | "pinned" | "slash" | "mention" | "variants";
export type SkillList = Skill[] & {more?: Record<string, number>};
export type Slash = {mode: "message" | "pin"; q: string; i: number; category?: string; resourceKind?: string; sources?: SkillSources; touched?: boolean; open: Set<string>; items: SkillList};
export type MentionItem = {c: Seg; desc: string; status?: string; mauve?: boolean};
export type Mention = {q: string; i: number; items: MentionItem[]; indexing?: boolean};
export type Library = {screen: "catalog" | "card" | "help" | "add"; q: string; group: string; sources?: SkillSources; category?: string; resourceKind?: string; collection?: string; name?: string;
  detail: SkillDetail | null; error?: string | null};
export type State = {
  S: ServerState;
  chat: Chat | null;
  view: "chat" | "remarks";
  settingsOpen: boolean;
  library: Library | null;
  R: {list: Remark[]; comments: Comment[]; error: string | null; active: number; filter: string; showClosed?: boolean; reopen?: number};
  start: {pick: number; off: boolean};
  draftSkills: string[] | null;  // a chat not created yet: its pinned skills (null: the file's defaults)
  draftAuto: boolean;
  menu: MenuKind | null;
  slash: Slash | null;
  slashCategory: string;
  slashSources: SkillSources;
  slashView: "list" | "grid" | "preview";
  skillPrefs: SkillPrefs;
  mention: Mention | null;
  queued: Record<string, Seg[][]>;  // chat id → messages typed while its agent works, sent one by one when it stops
  uploads: number;
  failed: {file: File; error: string}[];  // uploads that broke; Повторить sends the file again
  gallery: {pics: Seg[]; index: number} | null;
  draft: number;  // bumps on every change of the editor's content
  dragging: number;  // files over the input: how many
  foldOpen: Set<string>;  // answers whose earlier calls and messages are unfolded
  statsOpen: boolean;
  gone: string[];  // chats deleted a moment ago: hidden while «Вернуть» can still bring them back
  escArmed: boolean;  // one Esc while the agent works: the second stops it
  times: number;  // ×N: variants the next message asks for (1: a single answer)
  target: {run: string; n: number; title: string; agent?: string; model?: string} | null;  // the next message goes into this lane
};

let statsOpen = false;
try { statsOpen = localStorage.getItem("statsOpen") === "1"; } catch { /* no storage */ }
let skillPrefs = parseSkillPrefs(null);
try { skillPrefs = parseSkillPrefs(localStorage.getItem(PREFS_KEY)); } catch { /* no storage */ }
let slashView: State["slashView"] = "list";
let slashSources: SkillSources = null;
try { slashSources = parseSkillSources(localStorage.getItem(SOURCES_KEY), localStorage.getItem("figcraft.skillOrigin")); } catch { /* no storage */ }
try {
  const saved = localStorage.getItem("figcraft.skillView");
  if (saved === "grid" || saved === "preview") slashView = saved;
} catch { /* no storage */ }

let state: State = {
  S: {doc: {}, selection: [], agents: [], chats: [], settings: {mode: "figcraft"}, running: [], modes: []},
  chat: null, view: "chat", settingsOpen: false, library: null,
  R: {list: [], comments: [], error: null, active: 0, filter: "all"},
  start: {pick: 0, off: false}, draftSkills: null, draftAuto: true,
  menu: null, slash: null, slashCategory: "all", slashSources, slashView, skillPrefs, mention: null, queued: {}, uploads: 0, failed: [], gallery: null,
  draft: 0, dragging: 0, foldOpen: new Set(), statsOpen, gone: [], escArmed: false, times: 1, target: null,
};
const listeners = new Set<() => void>();

export const get = () => state;
export function set(patch: Partial<State> | ((s: State) => Partial<State>)) {
  state = {...state, ...(typeof patch === "function" ? patch(state) : patch)};
  flushSync(() => listeners.forEach((l) => l()));  // the page is drawn by the time set() returns: key handlers read it
}
const subscribe = (l: () => void) => { listeners.add(l); return () => { listeners.delete(l); }; };
export const useApp = () => useSyncExternalStore(subscribe, get);

// derived
export const running = (s = state) => !!s.chat && s.S.running.some((r) => r.chat === s.chat!.id);
export const waiting = (s = state) => s.R.list.filter((r) => r.status === "question" || r.status === "review");
export const answered = (s = state) => s.R.comments.filter((c) => c.answered);  // comments the agent replied to
export const agentOf = (id?: string, s = state) => s.S.agents.find((a) => a.id === id);
export const modelName = (a: {models: {id: string; name: string}[]} | undefined, m?: string) => (a?.models.find((x) => x.id === m) || {name: m}).name;
export const skillOf = (n: string, s = state) => (s.S.skills || []).find((k) => k.name === n);
export const pinned = (s = state) => s.chat ? (s.chat.skills || []) : (s.draftSkills ?? s.S.skillDefaults ?? []);
export const autoOn = (s = state) => s.chat ? s.chat.autoSkills !== false : s.draftAuto;
export const remarksView = (s = state) => s.view === "remarks" && !s.settingsOpen && !s.library;
