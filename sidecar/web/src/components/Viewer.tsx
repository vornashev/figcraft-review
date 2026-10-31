// The picture viewer: dimensions, download, ← →, zoom by buttons or wheel, fit, a strip of thumbnails.
import {useEffect, useLayoutEffect, useRef, useState} from "react";
import {imageUrl} from "../lib/format";
import {set, useApp} from "../store";
import {Icon} from "./bits";

export let zoomNow = 1;  // for the UI test

export function Viewer() {
  const {gallery} = useApp(), dialog = useRef<HTMLDialogElement>(null), img = useRef<HTMLImageElement>(null), canvas = useRef<HTMLDivElement>(null);
  const [zoom, setZoomState] = useState(1), [size, setSize] = useState<[number, number] | null>(null), [error, setError] = useState(false);
  const fitting = useRef(true);
  const s = gallery?.pics[gallery.index], index = gallery?.index ?? 0, count = gallery?.pics.length ?? 0;
  const setZoom = (z: number) => { zoomNow = Math.max(.05, Math.min(8, z)); setZoomState(zoomNow); };
  const fit = () => {
    const i = img.current!, c = canvas.current!;
    if (!i.naturalWidth) return;
    fitting.current = true; setZoom(Math.min(1, c.clientWidth / i.naturalWidth, c.clientHeight / i.naturalHeight));
  };
  const step = (d: number) => { if (gallery && index + d >= 0 && index + d < count) set({gallery: {...gallery, index: index + d}}); };

  useLayoutEffect(() => {
    const d = dialog.current!;
    if (gallery && !d.open) { d.showModal(); canvas.current?.focus(); } else if (!gallery && d.open) d.close();  // the keys go to the picture, not the first button
  }, [gallery]);
  useEffect(() => { setSize(null); setError(false); fitting.current = true; }, [s?.path]);
  useEffect(() => {
    const onResize = () => { if (dialog.current?.open && fitting.current) fit(); };
    addEventListener("resize", onResize);
    return () => removeEventListener("resize", onResize);
  }, []);
  useEffect(() => {  // the wheel zooms, not scrolls: a listener React would make passive
    const c = canvas.current;
    if (!c) return;
    const onWheel = (e: WheelEvent) => { e.preventDefault(); fitting.current = false; setZoom(zoomNow * (e.deltaY < 0 ? 1.1 : 1 / 1.1)); };
    c.addEventListener("wheel", onWheel, {passive: false});
    return () => c.removeEventListener("wheel", onWheel);
  }, [!!s]);
  useEffect(() => { document.querySelector(".viewer-strip .current")?.scrollIntoView({block: "nearest", inline: "nearest"}); }, [index]);

  return (
    <dialog className="viewer" id="viewer" aria-labelledby="viewerTitle" ref={dialog} onClose={() => set({gallery: null})}
      onKeyDown={(e) => {
        e.stopPropagation();
        if (e.key === "ArrowLeft") { e.preventDefault(); step(-1); }
        if (e.key === "ArrowRight") { e.preventDefault(); step(1); }
      }}>
      {s && <>
        <header><div><b id="viewerTitle">{s.label || `Картинка ${index + 1}`}</b><small id="viewerMeta">{size ? `${size[0]}×${size[1]} · ` : ""}{index + 1} из {count}</small></div>
          <a className="iconbtn" id="viewerDownload" title="Скачать" aria-label="Скачать" href={imageUrl(s.path!)} download={s.path!.startsWith("/api/skill-image?") ? new URL(s.path!, location.href).searchParams.get("file")?.split("/").pop() : s.path!.split("/").pop()}><Icon n="download" /></a>
          <button className="iconbtn" id="viewerClose" title="Закрыть" aria-label="Закрыть" onClick={() => set({gallery: null})}><Icon n="close" /></button></header>
        <div className="viewer-stage">
          <button id="viewerPrev" aria-label="Предыдущая картинка" disabled={index === 0} onClick={() => step(-1)}>‹</button>
          <div className="viewer-canvas" id="viewerCanvas" ref={canvas} tabIndex={-1}>
            <img id="viewerImage" ref={img} key={s.path} src={imageUrl(s.path!)} alt={s.title || s.label} hidden={!size}
              style={size ? {width: size[0] * zoom, height: size[1] * zoom} : undefined}
              onLoad={(e) => { const i = e.currentTarget; setSize([i.naturalWidth, i.naturalHeight]); fit(); }}
              onError={() => { setSize(null); setError(true); }} />
            {error && <span className="viewer-error" id="viewerError">Не удалось загрузить картинку</span>}
          </div>
          <button id="viewerNext" aria-label="Следующая картинка" disabled={index === count - 1} onClick={() => step(1)}>›</button>
        </div>
        <div className="viewer-tools">
          <button id="zoomOut" aria-label="Уменьшить" onClick={() => { fitting.current = false; setZoom(zoom / 1.25); }}>−</button>
          <output id="viewerZoom">{size ? Math.round(zoom * 100) + "%" : "…"}</output>
          <button id="zoomIn" aria-label="Увеличить" onClick={() => { fitting.current = false; setZoom(zoom * 1.25); }}>+</button>
          <button id="zoomFit" onClick={fit}>Вписать</button>
        </div>
        <div className="viewer-strip" id="viewerStrip">{gallery!.pics.map((p, i) => (
          <button key={i} className={`picture ${i === index ? "current" : ""}`} data-gallery={i} aria-label={p.label} aria-pressed={i === index}
            onClick={() => set({gallery: {...gallery!, index: i}})}><img src={imageUrl(p.path!)} alt={p.label} /></button>
        ))}</div>
        <div className="keys viewer-keys"><kbd>Esc</kbd><span>закрыть</span><kbd>← →</kbd><span>листать</span><kbd>колесо</kbd><span>масштаб</span></div>
      </>}
    </dialog>
  );
}
