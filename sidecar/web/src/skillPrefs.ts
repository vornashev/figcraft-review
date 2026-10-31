import type {Skill} from "./api";
import {get, set} from "./store";
import {PREFS_KEY, type SkillPrefs} from "./lib/skillPrefs";
import {SOURCES_KEY, type SkillSources} from "./lib/skillSources";

export function setSkillSources(sources: SkillSources) {
  try { localStorage.setItem(SOURCES_KEY, JSON.stringify(sources)); } catch { /* this window still works */ }
  set({slashSources: sources});
}

function save(prefs: SkillPrefs) {
  try { localStorage.setItem(PREFS_KEY, JSON.stringify(prefs)); } catch { /* the current window still works */ }
  set({skillPrefs: prefs});
}
export function toggleFavorite(name: string) {
  const prefs = get().skillPrefs;
  save({...prefs, favorites: prefs.favorites.includes(name) ? prefs.favorites.filter((n) => n !== name) : [...prefs.favorites, name]});
  const slash = get().slash;
  if (slash?.category === "favorites") {
    const items = skillCollection(slash.items, "favorites");
    set({slash: {...slash, items, i: Math.min(slash.i, Math.max(0, items.length - 1))}});
  }
}
export function rememberSkills(names: string[]) {
  if (!names.length) return;
  const prefs = get().skillPrefs;
  save({...prefs, recent: [...new Set([...names, ...prefs.recent])].slice(0, 20)});
}
export function skillCollection(skills: Skill[], collection?: string) {
  const prefs = get().skillPrefs;
  if (collection === "favorites") return skills.filter((s) => prefs.favorites.includes(s.name));
  if (collection === "recent") return prefs.recent.flatMap((name) => skills.filter((s) => s.name === name));
  return skills;
}
