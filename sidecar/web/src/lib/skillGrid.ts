type Rect = {left: number; top: number; width: number};

// Use actual card positions: column count can change on resize and groups have headings between them.
export function moveInSkillGrid(rects: Rect[], current: number, key: string) {
  if (!rects.length) return 0;
  const at = Math.max(0, Math.min(current, rects.length - 1));
  if (key === "ArrowLeft" || key === "ArrowRight") return (at + (key === "ArrowRight" ? 1 : -1) + rects.length) % rects.length;
  if (key !== "ArrowUp" && key !== "ArrowDown") return at;
  const rows = [...new Set(rects.map((r) => Math.round(r.top)))].sort((a, b) => a - b);
  const row = rows.indexOf(Math.round(rects[at].top));
  const target = rows[(row + (key === "ArrowDown" ? 1 : -1) + rows.length) % rows.length];
  const x = rects[at].left + rects[at].width / 2;
  let best = at, distance = Infinity;
  rects.forEach((r, i) => {
    if (Math.round(r.top) !== target) return;
    const delta = Math.abs(r.left + r.width / 2 - x);
    if (delta < distance) { distance = delta; best = i; }
  });
  return best;
}
