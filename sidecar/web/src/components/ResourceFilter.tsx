import type {Skill} from "../api";
import {RESOURCE_KINDS, resourceLabels} from "../lib/designResources";

export function ResourceFilter({skills, value, onChange, composer = false}: {
  skills: Skill[]; value?: string; onChange: (kind: string) => void; composer?: boolean;
}) {
  const resources = skills.filter((k) => k.category === "design-systems");
  return <div className="tabs resource-filters" role="group" aria-label="Вид дизайн-ресурса">
    {[["all", "Все"], ...Object.entries(RESOURCE_KINDS)].map(([id, label]) =>
      <button key={id} className="tab" data-resource-kind={id} aria-pressed={(value || "all") === id} tabIndex={composer ? -1 : undefined}
        onMouseDown={composer ? (e) => e.preventDefault() : undefined} onClick={() => onChange(id)}>
        {label}<small>{id === "all" ? resources.length : resources.filter((k) => k.resource_kind === id).length}</small>
      </button>)}
  </div>;
}

export function ResourceTags({skill}: {skill: Skill}) {
  const labels = resourceLabels(skill);
  return labels.length ? <span className="resource-tags">{labels.map((label) => <span key={label}>{label}</span>)}</span> : null;
}
