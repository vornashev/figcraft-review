import type {Skill} from "../api";
import {ORIGINS, originOf} from "./format";

export type SkillSources = string[] | null; // null: all (including newly installed sources); []: none
export const SOURCES_KEY = "figcraft.skillSources";
export const sourceEnabled = (sources: SkillSources, id: string) => sources === null || sources.includes(id);
const valid = (id: unknown): id is string => typeof id === "string" && /^[\w.-]{1,100}$/.test(id) && id !== "all";
export function parseSkillSources(raw: string | null, legacy: string | null = null): SkillSources {
  if (raw === null) return valid(legacy) ? [legacy] : null;
  try {
    const data = JSON.parse(raw);
    return Array.isArray(data) ? [...new Set(data.filter(valid))].slice(0, 100) : null;
  } catch { return null; }
}
export function skillOrigins(skills: Skill[]) {
  const ids = [...new Set(skills.map(originOf))];
  const ordered = [...Object.keys(ORIGINS).filter((id) => ids.includes(id)), ...ids.filter((id) => !ORIGINS[id]).sort()];
  return ordered.map((id) => ({id, label: ORIGINS[id] || id, count: skills.filter((k) => originOf(k) === id).length}));
}
export function toggleSkillSource(sources: SkillSources, id: string, available: string[]): SkillSources {
  if (id === "all") return null;
  const enabled = sources === null ? available : sources;
  return enabled.includes(id) ? enabled.filter((value) => value !== id) : [...enabled, id];
}
