export type SkillPrefs = {favorites: string[]; recent: string[]};
export const PREFS_KEY = "figcraft.skillPrefs";
export function parseSkillPrefs(raw: string | null): SkillPrefs {
  try {
    const data = JSON.parse(raw || "null");
    const names = (value: unknown, limit: number) => Array.isArray(value)
      ? [...new Set(value.filter((n): n is string => typeof n === "string" && /^[\w.-]{1,160}$/.test(n)))].slice(0, limit) : [];
    return {favorites: names(data?.favorites, 500), recent: names(data?.recent, 20)};
  } catch { return {favorites: [], recent: []}; }
}
