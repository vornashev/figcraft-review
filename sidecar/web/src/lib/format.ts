// Words, numbers and chips: pure helpers with no page state.
import type {Comment, Layer, Part, Remark, Seg, Skill, Step} from "../api";

export const esc = (s: unknown) => String(s ?? "").replace(/[&<>"]/g, (c) => ({"&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;"})[c]!);
export const short = (s: unknown, n: number) => { const t = String(s || "").trim(); return t.length > n ? t.slice(0, n - 1) + "…" : t; };
export const plural = (n: number, [one, few, many]: [string, string, string]) =>
  `${n} ${n % 10 === 1 && n % 100 !== 11 ? one : [2, 3, 4].includes(n % 10) && ![12, 13, 14].includes(n % 100) ? few : many}`;

export const ICON: Record<string, string> = {FRAME: "#", TEXT: "T", INSTANCE: "◇", COMPONENT: "❖", COMPONENT_SET: "❖", GROUP: "▢", SECTION: "§",
  VECTOR: "✎", RECTANGLE: "▭", ELLIPSE: "○", LINE: "╱", IMAGE: "▨"};
export const layerChip = (n: Layer): Seg => ({kind: "layer", id: n.id, label: n.name, icon: ICON[n.type || ""] || "•",
  title: `${String(n.type || "").toLowerCase()} · ${n.size || n.path || ""} · #${n.id}`});
export const remarkChip = (r: Pick<Remark, "num" | "text">): Seg => ({kind: "remark", num: r.num, label: `#${r.num} ${short(r.text, 28)}`, icon: "alert", title: r.text});
export const commentChip = (c: Pick<Comment, "id" | "text">): Seg => ({kind: "comment", id: c.id, label: short(c.text, 30), icon: "comment", title: c.text});
export const REMARKS: Seg = {kind: "remarks", label: "Замечания", icon: "alert", title: "Открытые замечания из review.py"};

export const GROUPS: Record<string, [string, string, string?]> = {base: ["Основа", "book", "всегда в каждом ходе"], style: ["Стиль", "palette"],
  system: ["Дизайн-система", "shape", "одна на чат"], library: ["Библиотека компонентов", "puzzle", "экран из её компонентов"], platform: ["Платформа", "phone"],
  quality: ["Качество", "done"], task: ["Задачи", "fix"], other: ["Другие", "puzzle"]};
export const group = (g?: string) => GROUPS[g || ""] || GROUPS.other;
export const EXCLUSIVE = new Set(["system"]);
export const SOURCE: Record<string, string> = {builtin: "встроенный", project: "проект", mine: "мой", "pen.dev": "pen.dev"};
export const ORIGINS: Record<string, string> = {opendesign: "OpenDesign", hallmark: "Hallmark", typeui: "TypeUI", tweakcn: "tweakcn", uipro: "UI UX Pro Max", "design-resources": "Дизайн-ресурсы", builtin: "Встроенные", project: "Проект", mine: "Мои", "pen.dev": "pen.dev"};
export const CATEGORIES: Record<string, string> = {websites: "Сайты", apps: "Приложения", dashboards: "Дашборды", slides: "Презентации", graphics: "Графика", "design-systems": "Дизайн-системы", themes: "Темы"};
export const originOf = (k: Pick<Skill, "origin" | "source">) => k.origin || k.source;
export const originName = (k: Pick<Skill, "origin" | "source">) => ORIGINS[originOf(k)] || originOf(k);
export const SKILL_MODES: Record<string, string> = {always: "Всегда", manual: "Вручную", auto: "Сам"};
export const skillChip = (s: Skill): Seg => ({kind: "skill", name: s.name, group: s.group, label: s.title, icon: group(s.group)[1],
  title: `${group(s.group)[0]} · ${s.summary}`});

export const familyOf = (id?: string) => String(id || "").split(":")[0];  // claude:claude-2 is another Claude Code login
export const markGlyph = (id?: string) => ({claude: "claude", codex: "X", pi: "π"} as Record<string, string>)[familyOf(id)] || "?";

export const clock = (s: number) => `${Math.floor(s / 60)}:${String(Math.floor(s % 60)).padStart(2, "0")}`;
export const tokens = (n: number) => n >= 1e6 ? `${(n / 1e6).toFixed(1)}M` : n >= 1e3 ? `${(n / 1e3).toFixed(1)}k` : String(n);
export const duration = (s: number) => s >= 60 ? `${Math.floor(s / 60)} мин ${s % 60} с` : `${s} с`;
export const bytes = (n?: number) => n == null ? "" : n < 1024 ? `${n} Б` : n < 1 << 20 ? `${Math.round(n / 1024)} КБ` : `${(n / (1 << 20)).toFixed(1)} МБ`;
export const sizeLabel = (n: number) => n < 1024 ? `${n} Б` : `${Math.ceil(n / 1024)} КБ`;
export const fileMeta = (s: Seg) => [String(s.label || "").split(".").pop()!.toUpperCase(), bytes(s.size)].filter(Boolean).join(" · ");
export function ago(t: number, now = Date.now() / 1000) {
  const s = now - t;
  return s < 60 ? "сейчас" : s < 3600 ? `${Math.round(s / 60)} мин` : s < 86400 ? `${Math.round(s / 3600)} ч` : `${Math.round(s / 86400)} дн`;
}
export function shortPath(p?: string) {
  const s = String(p || "").replace(/^\/home\/[^/]+/, "~").split("/");
  return s.length > 5 ? [...s.slice(0, 4), "…", s[s.length - 1]].join("/") : s.join("/");
}
export const imageUrl = (p: string) => p.startsWith("/api/skill-image?") ? p : "/api/image?path=" + encodeURIComponent(p);
export const modelDescription = (m: {id: string; description?: string}) => m.description
  || ({fable: "Самая сильная, отвечает дольше", opus: "Для экранов и дизайн-системы", sonnet: "Быстрее, для правок по замечаниям", haiku: "Тексты и мелкие правки"} as Record<string, string>)[m.id.split("-")[1]] || "";

// enough Markdown for agent answers: paragraphs, lists, `code`, **bold**; the text is escaped first
const inline = (s: string) => s.replace(/`([^`]+)`/g, "<code>$1</code>").replace(/\*\*([^*]+)\*\*/g, "<b>$1</b>");
export function md(s: string) {
  const out: string[] = [];
  let list: string[] | null = null;
  for (const line of esc(s).split("\n")) {
    const m = line.match(/^\s*[-*] (.*)/);
    if (m) { (list ||= []).push(`<li>${inline(m[1])}</li>`); continue; }
    if (list) { out.push(`<ul>${list.join("")}</ul>`); list = null; }
    if (line.trim()) out.push(`<p>${inline(line)}</p>`);
  }
  if (list) out.push(`<ul>${list.join("")}</ul>`);
  return out.join("");
}

// texts as they are, runs of steps in one card each
export type Block = {kind: "steps"; list: Step[]} | Exclude<Part, Step>;
export function groupSteps(parts: Part[]): Block[] {
  const out: Block[] = [];
  for (const p of parts) {
    if (p.kind === "step") {
      const last = out.at(-1);
      if (last?.kind === "steps") last.list.push(p); else out.push({kind: "steps", list: [p]});
    } else out.push(p);
  }
  return out;
}

// what came before the last message folds into one line; while the agent works its latest steps stay open
export function splitAnswer(parts: Part[], running?: boolean) {
  const lastText = parts.findLastIndex((p) => p.kind === "text");
  const cut = Math.max(lastText >= 0 ? lastText : running ? parts.findIndex((p) => p.kind === "step") : parts.length, 0);
  const head = parts.slice(0, cut), tail = parts.slice(cut);
  return {head, tail, calls: head.filter((p) => p.kind === "step").length, says: head.filter((p) => p.kind === "text").length};
}

// a layer's type in the answer's «Изменено на холсте», as the designer says it
const TYPES: Record<string, string> = {component: "компонент", component_set: "набор вариантов", instance: "экземпляр", frame: "фрейм",
  group: "группа", text: "текст", rectangle: "прямоугольник", ellipse: "эллипс", vector: "вектор", section: "секция", line: "линия"};
export const layerType = (t?: string) => t ? TYPES[t.toLowerCase()] || t.toLowerCase() : "";
