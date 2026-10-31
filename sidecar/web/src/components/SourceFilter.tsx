import {useEffect, useLayoutEffect, useRef, useState} from "react";
import {createPortal} from "react-dom";
import {sourceEnabled, toggleSkillSource, type SkillSources} from "../lib/skillSources";
import {Icon} from "./bits";

type Origin = {id: string; label: string; count: number};
export function SourceFilter({options, value, onChange, scope, back}: {options: Origin[]; value: SkillSources;
  onChange(value: SkillSources): void; scope: "slash" | "library"; back?(): void}) {
  const [open, setOpen] = useState(false), [position, setPosition] = useState({left: 12, top: 12});
  const trigger = useRef<HTMLButtonElement>(null), panel = useRef<HTMLDivElement>(null);
  const ids = options.map((o) => o.id), enabled = options.filter((o) => sourceEnabled(value, o.id));
  const all = value === null || options.length > 0 && enabled.length === options.length;
  const summary = all ? `Все ${options.length}` : `${enabled.length}/${options.length}`;
  const close = (restore = true) => { setOpen(false); if (restore) back ? back() : trigger.current?.focus(); };

  useLayoutEffect(() => { if (open) panel.current?.querySelector<HTMLInputElement>('input[type="checkbox"]')?.focus(); }, [open]);

  useLayoutEffect(() => {
    if (!open) return;
    const move = () => {
      const button = trigger.current?.getBoundingClientRect(), box = panel.current?.getBoundingClientRect();
      if (!button || !box) return;
      const next = {left: Math.max(12, Math.min(button.left, innerWidth - box.width - 12)),
        top: Math.max(12, Math.min(button.bottom + 6, innerHeight - box.height - 12))};
      setPosition((old) => old.left === next.left && old.top === next.top ? old : next);
    };
    move();
    window.addEventListener("resize", move); window.addEventListener("scroll", move, true);
    return () => { window.removeEventListener("resize", move); window.removeEventListener("scroll", move, true); };
  }, [open, value, options.length]);
  useEffect(() => {
    if (!open) return;
    const outside = (event: PointerEvent) => {
      if (panel.current?.contains(event.target as Node) || trigger.current?.contains(event.target as Node)) return;
      close(false);
      if ((event.target as Element).closest?.('.menu[data-kind="slash"]')) back?.();
    };
    const escape = (event: KeyboardEvent) => {
      if (event.key !== "Escape" || event.isComposing) return;
      event.preventDefault(); event.stopPropagation(); close();
    };
    document.addEventListener("pointerdown", outside, true); document.addEventListener("keydown", escape, true);
    return () => { document.removeEventListener("pointerdown", outside, true); document.removeEventListener("keydown", escape, true); };
  }, [open]);

  return <>
    <button ref={trigger} className="source-trigger" data-source-trigger={scope} data-filtered={!all}
      aria-haspopup="dialog" aria-expanded={open} aria-controls={`source-panel-${scope}`}
      title={`Источники: ${all ? "все" : enabled.length ? enabled.map((o) => o.label).join(", ") : "выключены"} · Alt+←/→`}
      onMouseDown={(e) => e.preventDefault()} onClick={() => open ? close() : setOpen(true)}>
      <Icon n="puzzle" /><span>Источники</span><small>{summary}</small><Icon n="chevron" />
    </button>
    {open && createPortal(<div ref={panel} className="source-popover" id={`source-panel-${scope}`} data-source-options={scope}
      role="dialog" aria-label="Источники навыков" style={position} onClick={(e) => e.stopPropagation()}
      onKeyDown={(e) => {
        if (e.ctrlKey || e.metaKey || !["ArrowDown", "ArrowUp", "ArrowLeft", "ArrowRight"].includes(e.key)) return;
        const rows = [...panel.current!.querySelectorAll<HTMLInputElement>('input[type="checkbox"]')];
        if (!rows.length) return;
        e.preventDefault();
        const at = rows.indexOf(document.activeElement as HTMLInputElement), forward = e.key === "ArrowDown" || e.key === "ArrowRight";
        rows[at < 0 ? (forward ? 0 : rows.length - 1) : (at + (forward ? 1 : rows.length - 1)) % rows.length].focus();
      }}>
      <div className="source-popover-head"><strong>Источники</strong><span>{enabled.length} из {options.length}</span></div>
      <div className="source-options">{options.map((o) => <label className="source-option" key={o.id}>
        <input type="checkbox" data-source-scope={scope} data-origin={o.id} checked={sourceEnabled(value, o.id)}
          onChange={() => onChange(toggleSkillSource(value, o.id, ids))}
          onKeyDown={(e) => { if (e.key === "Enter" && !e.ctrlKey && !e.metaKey && !e.altKey) {
            e.preventDefault(); onChange(toggleSkillSource(value, o.id, ids));
          } }} />
        <span>{o.label}</span><small>{o.count}</small>
      </label>)}</div>
      <div className="source-popover-actions">
        <button className="btn" data-origin="all" onClick={() => onChange(null)}>Все</button>
        <button className="btn" data-source-none onClick={() => onChange([])}>Ни одного</button>
        <button className="btn" data-source-done onClick={() => close()}>Готово</button>
      </div>
      <div className="source-popover-note">Изменения сохраняются сразу</div>
    </div>, document.body)}
  </>;
}
