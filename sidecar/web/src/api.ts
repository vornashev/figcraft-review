// What the chat server (server.py) answers and sends; only the fields the page reads.

export type Seg = {
  kind: "text" | "layer" | "remark" | "remarks" | "skill" | "image" | "file" | string;
  text?: string; id?: number; num?: number; path?: string; size?: number;
  name?: string; group?: string; label?: string; icon?: string; title?: string;
};
export type Layer = {id: number; name: string; type?: string; size?: string; path?: string; more?: boolean};
export type Step = {kind: "step"; id?: string; label: string; status: "ok" | "error" | "run" | "stopped"; t0?: number; took?: number};
export type Part = Step | {kind: "text"; text: string; streaming?: boolean};
export type Changes = {steps: number; ids: number[]; undone?: boolean;
  layers?: ({id: number; removed: true} | {id: number; name: string; type?: string; top?: string; removed?: false})[]};
export type Message = {
  role: "user" | "assistant"; text?: string; segments?: Seg[]; agent?: string; model?: string;
  parts?: Part[]; running?: boolean; error?: string; changes?: Changes; saved?: string;
  marked?: {num: number; status: string}[]; denied?: {tool: string; label: string}[];
  skills?: {name: string; title: string; group: string; level: string}[];
  usage?: {input?: number; output?: number; cacheRead?: number; cacheWrite?: number; context?: number; window?: number; turns?: number};
  took?: number; cost?: number; phases?: {prep?: number; first?: number};
  times?: number; auto?: boolean;  // a message asked for ×N variants; the chat wrote it itself (the comparison)
  toLane?: {run: string; n: number; title: string};  // a message into one variant's lane
  compare?: string;  // the orchestrator's comparison of a run
  retried?: boolean;  // a lane's attempt that ran again
  variants?: {run: string; count: number; frames: number[]; axis?: string; base?: string; started?: number; ended?: number;
    picked?: Picked};  // the orchestrator started a run
  lane?: {run: string; n: number; of: number; title: string; idea?: string; style?: string | null; styleTitle?: string | null;
    frame: number; width?: number; height?: number; session?: string; axis?: string; base?: string;
    kind?: "more" | "retry" | "spread" | "adapt"; note?: string};  // one variant, drawn by its own agent
};
export type Picked = {n: number; title: string; frame: number; undone?: boolean; frames: number[]; collections: number; styles: number;
  collection?: string | null; ownStyles: number};
export type ChatSummary = {id: string; title: string; agent: string; model?: string; updated: number};
export type Chat = ChatSummary & {file?: string; messages: Message[]; skills?: string[]; autoSkills?: boolean};
export type Model = {id: string; name: string; description?: string};
export type Agent = {id: string; name: string; ok: boolean; path?: string; version?: string; account?: string; models: Model[]};
export type Skill = {name: string; title: string; summary: string; description?: string; group: string; mode: string; source: string;
  origin?: string; category?: string; style?: string; thumbnail?: string;
  resource_kind?: string; formats?: string; resource_source?: string; access?: string;
  preview?: {colors?: string[]; font?: string}};
export type SkillReferences = {images: {file: string; label: string; url: string}[]; links: {label: string; url: string}[]};
export type SkillDetail = Skill & {dir: string; body: string; files: {name: string; size: number}[]; truncated?: boolean; references?: SkillReferences};
export type Remark = {num: number; text: string; status: string; layer?: number; name?: string; page?: string;
  replies: [string, string][]; question?: string; options: string[]; before?: boolean; after?: string};
// A FigCraft comment thread (open); `answered`: its last message is an agent's, so it waits for the designer.
export type Comment = {id: number; text: string; author: string; page: string; frame: string; replies: number;
  last: [string, string] | null; answered: boolean; unread: boolean; mentions: string[]};
export type Lane = {agent: string; model: string; style?: string};
export type Axis = "style" | "structure" | "adaptive";
export type Preset = {name: string; count: number; orchestrator?: {agent: string; model: string} | null; lanes?: (Lane | null)[]; axis?: Axis};
export type VariantSettings = {count?: number; orchestrator?: {agent: string; model: string} | null; lanes?: (Lane | null)[];
  axis?: Axis; limit?: number; presets?: Preset[]};
export type Settings = {mode: string; agent?: string; model?: string; shots?: boolean; variants?: VariantSettings};
export type ServerState = {
  doc: {path?: string; name?: string; error?: string}; selection: Layer[]; stale?: boolean;
  running: {chat: string; file?: string; lane?: number}[]; chats: ChatSummary[]; modes: string[]; settings: Settings; agents: Agent[];
  skills?: Skill[]; skillDefaults?: string[]; designMd?: {exists: boolean};
  opendesign?: Download;
  update?: {version: string; url: string; auto: boolean} | null;  // a newer release; auto: the app installs it
};
// OpenDesign's import (it isn't shipped): progress of skills/opendesign.py run by the server.
export type Download = {running: boolean; done: number; total: number; error: string | null};

export async function api<T = any>(path: string, body?: unknown): Promise<T> {
  const r = await fetch(path, body ? {method: "POST", headers: {"Content-Type": "application/json"}, body: JSON.stringify(body)} : {});
  const data = await r.json();
  if (!r.ok) throw new Error(data.error || r.statusText);
  return data;
}
