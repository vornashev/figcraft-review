---
name: hallmark-pasteup
description: "Paste-up: kraft board, a fibre wash, near-black toner, League Gothic capitals over a Newsreader galley, white copy paper on paper lifts, hard ink offsets, one sheet of fluorescent yellow. Fits: zine, fair, market, festival, print fair, book fair, exhibitors, punk, diy, collective, gig, poster, workshop, night market, flea, indie, community, launch, loud, photocopy, flyer"
metadata:
  origin: hallmark
  category: themes
  group: style
  mode: manual
  title: Paste-up
  summary: игривый, средний тон, уверенный акцент
  preview: "#C4A179 #B08A62 #130E0B #ECF423 · League Gothic"
---
# Paste-up — a Hallmark style

The designer chose this style for the chat. A style is a material: paper, ink, faces, rules, radius, depth, controls
and voice. It is never a layout. It was written for web pages in CSS; in FigCraft:

- **Tokens become the file's variables.** Look at the file's variables first (`variable.export`). With no colour
  collection for this style, make one named «Paste-up»: the `--color-*` tokens as colour variables without the prefix
  (`paper`, `ink`, `accent`…), radii as numbers; bind fills, strokes and radii to them (`variable.bind`), never paste
  hex. A file that already has its own colour system keeps it: restyle it onto this one only when asked.
- **Faces.** Check each family with `text.fonts {family}`. A missing one: say so in one line and take the nearest
  installed face of the same class (display-condensed); never swap silently. Make text styles for display, body, labels
  and code from the Type section.
- **CSS in FigCraft terms.** box-shadow → drop or inner shadow effects; border → an inside stroke; border-radius →
  cornerRadius; `corner-shape: bevel` has no equivalent, use the fallback radius; gradients → gradient fills;
  `var()` and `color-mix()` → the nearest token. Hover, pressed, focus, disabled are component variants, not
  transitions. Motion does not apply to a static mockup.
- **App screens** (most work here): the style lends its palette, faces, radius and surfaces, never its layout,
  navigation or ornament. The accent marks the primary action, the selection and state, nothing else; a second
  neutral carries sidebars, toolbars and panels; controls are 32 to 40 px; the type scale steps by 1.125 to 1.2 and
  no display face sits on labels, buttons or data. Range, textures, generated fields and photographs are for pages.
- **Colours below are hex,** converted from the theme's OKLCH (an alpha is the last two digits).

## Genre: playful

Pages that should feel alive rather than tidy: a prompt that asks for playful, fun, friendly or soft, or one for kids, games or a community. A consumer or family prompt without that ask stays editorial. The deal leans toward this genre's themes, which run from soft and warm to loud and retro.

## Voice

- **Accent:** soft and low-chroma by default; a declared Full-palette or Drenched posture lifts chroma to 0.24 across three or four named roles, each with a job.
- **Layout:** rounded surfaces (12px cards, 8px inputs, pills, unless the theme sets its radius), soft offset shadows, tinted alternating bands.
- **Motion:** responsive to the pointer; one small entrance on the page, its one reveal (`craft.md` § 5); a spring only under a declared spring posture, on the primary CTA and one character moment (gate 12's exception).
- **Copy:** warm, direct, specific; no quirk for its own sake.

## Allowed here

Soft drop shadows with an offset; hover lifts on cards; a hard-offset shadow when the theme declares it as material; a single character moment; emoji inside a sentence, never as an ornament or icon.

## Refused here

Saturated consumer pinks and violets without a declared posture; Comic-style faces; bounce on anything but the declared moments; glass; gradient text; decorative status dots and sticker-style pills stamped on every element (63, 66).

## Chrome that fits

A heavy slab bar, a dense bar with rounded knobs, a banner, a marquee footer. A masthead or a blurred pill fights the register; a solid pill does not. Affinities, not assignments.


## The theme

A hand-made flyer: kraft board, near-black toner, League Gothic capitals at poster size over a Newsreader galley, white copy paper on real paper shadows, controls on hard ink offsets, one sheet of fluorescent yellow. Photographs come off the copier, black and white, the greys crushed. The paste-up lives in the paper, the tilt and the lift, never in props. It is not a grunge texture pack, a scrapbook of stickers and tape, or a clean modern poster.

### Tokens

```css
:root {
  --color-paper: #C4A179; --color-paper-2: #B08A62; --color-paper-3: #F7F5EF;
  --color-ink: #130E0B; --color-ink-2: #241E19; --color-muted: #32261C;
  --color-rule: #785D41; --color-rule-2: #CECAC2;
  --color-accent: #ECF423; --color-accent-ink: #130E0B; --color-focus: #130E0B;
  --font-display: "League Gothic", Impact, sans-serif; --font-body: "Newsreader", Georgia, serif;
  --radius-card: 0; --radius-pill: 999px; --rule-hair: 1px;
  --shadow-card: 0 1px 0 #15110D33, 0 4px 10px #15110D1F;
  --shadow-sheet: 0 14px 30px #15110D42, 0 2px 4px #15110D24;
  --tracking-display: 0.01em; --display-weight: 400;
}
```

The fluorescent is a paper, not an ink: it carries toner type and is never type itself. Three boards, stated in the stamp (`pasteup: kraft`): kraft, the tokens above, fibre at 0.5 multiply; black wall, ground `#1D1713`, toner `#EEEBE2`, muted `#A39E94`, fibre at 0.35 screen; sugar paper, ground `#BBD1BF`, toner `#121E17`, muted `#3F5247`, fibre at 0.4 multiply.

### Type

- **Display:** League Gothic 400, uppercase, `--tracking-display`, never under 28px, so item titles (`h3`) set in Newsreader 500 instead. It is a poster face: a flyer head or a figure takes up to twice `--text-display` at line-height 0.92; a section head takes one step up from `--text-section` at 1.0.
- **Body:** Newsreader 400 and 500 at 18px, line-height 1.5; italic is emphasis in running text only. On a sheet, text sits on copy white; on the board it takes `--color-ink`, never `--color-muted`, under 18px.
- **Labels, captions, table heads, meta, controls:** Newsreader 500 a step smaller, sentence case, untracked. No mono.

### Surfaces

- Paper lifts, not boxes: a well is a sheet of copy paper (`--color-paper-3`) on `--shadow-card`, a raised sheet takes `--shadow-sheet`. Radius 0; hairlines in `--color-rule` part rows on the board, `--color-rule-2` on a sheet.
- Tilt is the paste: a sheet or a photograph may sit 0.5° to 2° off square, three tilted surfaces a screen at most; inputs, tables and long reading stay square.
- The fluorescent sheet fills the primary control and one sheet a screen, with toner type on it; never a band, a head or a word on the board.
- Bands: `--color-paper-2` (a deeper kraft) or the toner with board-coloured type; two a page at most.
- Photographs: zines, hands, copiers, staplers and fair tables, close and flat-lit, a crowd from behind at most; through the copier (the `photo:` line), hard black and white. Printed multiply on a copy sheet with a 10 to 16px margin and lifted, or straight onto the board so the kraft shows through the whites; never colour, never full-bleed. A caption sits on the sheet's foot.
- Texture: the fibre wash (`texture.md` § 1, a low-frequency tan tint) on a kraft band at the board's opacity and blend, never on a sheet or under running text.

### Range

- **The facts as a wall of flyers:** the prompt's date, count, price and deadline each on its own sheet in League Gothic at poster size, mixed spans and heights, overlapping by a few pixels, two or three tilted, one on the fluorescent; no photograph among them.
- **A typed sheet:** a timetable, a price list or the where-and-when as a ruled table on one copy sheet at a slight tilt, the left column in League Gothic, the rest in Newsreader.
- **The toner band:** one line in League Gothic at `--text-display` or larger, board-coloured on toner, across ten columns.
- **The form as a sheet:** fields on copy paper, square, on a hard offset, beside its head and the deadline set big on the board.

### Controls

- The control pair: a fluorescent primary with toner type on a hard `4px 4px 0` ink offset, beside a copy-paper secondary on the same offset, both Newsreader 500 at 15px.
- Links are toner with a 1px underline, thicker on hover; inputs are copy paper, square, a 1px ink border; the focus ring is toner.

### Motion

Paper physics only: a button drops 1px into its offset on hover and 4px on press over `--dur-micro`. Nothing floats, nothing reveals.

### Voice

Flyer voice: the date, the door, the price, the table number.

### Do-nots

- Never paste-up props: no tape, stickers, stamps or scrawled notes.
- Never a word set apart in a head: no cut-out word, no yellow word, no italic word.
- Never a soft shadow on a control; controls sit on a hard ink offset.
- Never a grunge overlay, a torn edge or a photograph in colour.

### Build hint

```css
h1, h2 { font-weight: 400; text-transform: uppercase; line-height: 1; } h1 { line-height: 0.92; }
h3 { font: 500 var(--text-title)/1.2 var(--font-body); }
.btn { border: 0; border-radius: 0; padding: var(--space-sm) var(--space-md); font: 500 15px/1.2 var(--font-body); color: var(--color-ink); box-shadow: 4px 4px 0 var(--color-ink); transition: translate var(--dur-micro) var(--ease-out), box-shadow var(--dur-micro) var(--ease-out); }
.btn:hover { translate: 1px 1px; box-shadow: 3px 3px 0 var(--color-ink); }
.btn:active { translate: 4px 4px; box-shadow: none; }
.btn--primary { background: var(--color-accent); color: var(--color-accent-ink); }
.btn--secondary { background: var(--color-paper-3); }
.sheet { background: var(--color-paper-3); box-shadow: var(--shadow-sheet); rotate: var(--r, 0deg); }
.sheet--fluoro { background: var(--color-accent); color: var(--color-accent-ink); }
.sheet img { mix-blend-mode: multiply; filter: grayscale(1) contrast(1.3); }
.fibre { position: relative; isolation: isolate; }
.fibre::before { content: ""; position: absolute; inset: 0; z-index: -1; opacity: 0.5; mix-blend-mode: multiply; pointer-events: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='300' height='300'%3E%3Cfilter id='p'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.02 0.03' numOctaves='3' seed='7'/%3E%3CfeColorMatrix values='0 0 0 0 0.55 0 0 0 0 0.45 0 0 0 0 0.3 0 0 0 0.28 0'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23p)'/%3E%3C/svg%3E"); }
::selection { background: color-mix(in oklab, var(--color-accent) 70%, transparent); color: var(--color-ink); }
```
