// Small pieces several screens share.
import type {Seg, Skill} from "../api";
import {familyOf, fileMeta, imageUrl, markGlyph} from "../lib/format";
import {ICONS, isIcon, type IconName} from "../lib/icons";

export const Icon = ({n, className = ""}: {n: IconName; className?: string}) => (
  <svg className={`g ${className}`} viewBox="0 0 24 24" aria-hidden="true"><path d={ICONS[n]} /></svg>
);

export const Mark = ({id}: {id?: string}) => {
  const g = markGlyph(id);
  return <span className={`mark ${familyOf(id)}`}>{isIcon(g) ? <Icon n={g} /> : g}</span>;
};

export function ChipMark({c}: {c: Seg}) {  // a skill's group colour, @ for a layer, a ring for a remark
  if (c.kind === "skill") return <i className="sq" />;
  if (c.kind === "layer") return <i className="at">@</i>;
  if (c.kind === "remark") return <i className="ring" />;
  if (c.kind === "remarks") return <i className="sq" style={{"--g": "var(--orange)"} as React.CSSProperties} />;
  return <i>{isIcon(c.icon) ? <Icon n={c.icon} /> : c.icon || "#"}</i>;
}
export const Chip = ({c}: {c: Seg}) => (
  <span className={`chip ${c.kind}${c.group ? " g-" + c.group : ""}`} title={c.title || c.label}><ChipMark c={c} /><span>{c.label}</span></span>
);

export const FileTile = ({s}: {s: Seg}) => <span className="filetile" title={s.path}><b>{s.label}</b><small>{fileMeta(s)}</small></span>;

export const Picture = ({s, i, onOpen}: {s: Seg; i: number; onOpen: () => void}) => (
  <button className="picture" data-picture="" data-index={i} aria-label={`Открыть ${s.label || `картинку ${i + 1}`}`} onClick={onOpen}>
    <img src={imageUrl(s.path!)} alt={s.title || s.label} />
    <span className="pic-number">{s.label?.match(/\d+$/)?.[0] || i + 1}</span>
  </button>
);

export const Swatches = ({s}: {s: Skill}) => s.preview?.colors?.length
  ? <span className="sw">{s.preview.colors.map((c, k) => <i key={k} style={{background: c}} />)}</span> : null;

export const Md = ({html, className}: {html: string; className: string}) => <div className={className} dangerouslySetInnerHTML={{__html: html || "<p></p>"}} />;
