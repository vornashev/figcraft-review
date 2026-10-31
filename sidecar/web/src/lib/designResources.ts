import type {Skill} from "../api";

export const RESOURCE_KINDS: Record<string, string> = {system: "Дизайн-системы", "ui-kit": "UI-киты", components: "Компоненты и блоки"};
const FORMATS: Record<string, string> = {figma: "Figma", code: "Код"};
const RESOURCE_SOURCES: Record<string, string> = {official: "Ресурсы автора", community: "Community", mixed: "Автор / community"};
const ACCESS: Record<string, string> = {free: "Бесплатно", paid: "Платно", mixed: "Бесплатно / платно"};

export const matchesResourceKind = (k: Skill, category?: string, kind?: string) =>
  category !== "design-systems" || !kind || kind === "all" || k.resource_kind === kind;

export function resourceLabels(k: Skill) {
  return [RESOURCE_KINDS[k.resource_kind || ""], ...(k.formats || "").split(/\s+/).map((f) => FORMATS[f]),
    RESOURCE_SOURCES[k.resource_source || ""], ACCESS[k.access || ""]].filter(Boolean);
}
