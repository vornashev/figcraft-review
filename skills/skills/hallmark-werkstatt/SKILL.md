---
name: hallmark-werkstatt
description: "Werkstatt: warm putty ground with a lighter well, near-black ink, Jost 700 capitals and numerals over Karla, square 2px and 3px ink rules that box cells, flat ultramarine, vermilion and yellow primaries. Fits: school, programme, workshop, maker, course, bootcamp, academy, apply, admissions, tuition, timetable, bauhaus, craft, design education, design school, residency, cohort, prospectus"
metadata:
  origin: hallmark
  category: themes
  group: style
  mode: manual
  title: Werkstatt
  summary: игривый, средний тон, полная палитра
  preview: "#D2C9B9 #C6BBA8 #14110E #1949C5 #D93411 · Jost"
---
# Werkstatt — a Hallmark style

The designer chose this style for the chat. A style is a material: paper, ink, faces, rules, radius, depth, controls
and voice. It is never a layout. It was written for web pages in CSS; in FigCraft:

- **Tokens become the file's variables.** Look at the file's variables first (`variable.export`). With no colour
  collection for this style, make one named «Werkstatt»: the `--color-*` tokens as colour variables without the prefix
  (`paper`, `ink`, `accent`…), radii as numbers; bind fills, strokes and radii to them (`variable.bind`), never paste
  hex. A file that already has its own colour system keeps it: restyle it onto this one only when asked.
- **Faces.** Check each family with `text.fonts {family}`. A missing one: say so in one line and take the nearest
  installed face of the same class (geometric-sans); never swap silently. Make text styles for display, body, labels
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

A design school's printed prospectus: a warm putty ground, near-black ink, heavy Jost capitals over a plain Karla body, square 2px and 3px ink rules, and three flat primaries, blue, red and yellow, each with one job. Its photographs are black and white records of the shops at work. It reads taught and sure of itself, like a programme pinned to a workshop wall: facts boxed in ruled cells, dates and numbers set as large as heads. It is not a toy-box palette and not a pattern of confetti shapes.

### Tokens

```css
:root {
  --color-paper: #D2C9B9; --color-paper-2: #C6BBA8; --color-paper-3: #E2DCCF;
  --color-ink: #14110E; --color-ink-2: #2A2522; --color-muted: #4B433E;
  --color-rule: #83786C;
  --color-accent: #1949C5; --color-accent-2: #D93411; --color-accent-2-deep: #B71C07; --color-accent-3: #F4C929;
  --color-accent-ink: #F6F1E9; --color-focus: #1949C5;
  --font-display: "Jost", "Futura", sans-serif; --font-body: "Karla", ui-sans-serif, system-ui, sans-serif;
  --font-outlier: "JetBrains Mono", ui-monospace, monospace;
  --radius-card: 0; --radius-pill: 0; --rule-hair: 1px; --rule-bar: 2px; --rule-box: 3px;
  --shadow-card: none;
  --tracking-display: -0.005em; --display-weight: 700;
}
```

Three colourways, set once per page and stated in the stamp (`werkstatt: putty`).

| Colourway | Ground, ink, primaries |
| --- | --- |
| `putty` (default) | the block above |
| `blackboard` | ground `#110F0D`, ink `#E3DDD3`, rule `#47413D`, primaries a step brighter; putty returns as a well colour |
| `blue` | ground `#2351DE`, ink `#EEE7D9`, rule `#6288E1`; the yellow does the accent's work |

### Type

- **Display:** Jost 700, uppercase, `--tracking-display`, line-height 1.02, at the shared steps. Capitals are the material: every head is set in them. Numerals and dates take the same face at display size and up, tabular, inside their cell.
- **Body:** Karla 400, line-height 1.5.
- **Labels, captions, tags, table heads:** Karla 600 a step smaller, sentence case, untracked, in `--color-muted`. Small figures and prices in Karla with `tabular-nums`; mono only inside code.
- **Controls:** Karla 600 in capitals, following the display (the case gate 67 allows on an uppercase page), untracked.

### Surfaces

- Rules: `--rule-box` ink lines box and cross a grid, `--rule-bar` ink runs under a nav and over every table, `--rule-hair` in `--color-rule` between rows. No card has a background; a cell is what the rules enclose.
- Zero radius and zero shadow everywhere.
- Bands: a `--color-paper-2` band, an `--color-ink` band with paper text in the `blackboard` colours, or one blue field with `--color-accent-ink` text; two bands a page at most. `--color-paper-3` is a well inside a ruled cell, never a band.
- Photographs: the shops at work, documentary and plain, at bench height or from just above: a bench and its tools, hands at a plane, a press or a wheel, wood, type and clay close enough to read the grain; daylight, nobody facing the lens. Printed black and white (the `photo:` mono) so the primaries stay the only colour; square, in a `--rule-bar` ink border, flush with the cells around them. A shop's primary runs as the flat cell or bar beside or under its picture and carries the caption; it never tints the photograph, and type never sits on one.
- No texture, and no gradient anywhere.

### Range

- **Figures in boxed cells:** the prompt's real numbers in Jost 700 at display size, each in its own `--rule-box` cell across the twelve columns, the label in Karla beneath; no primary, since a set of one kind takes no colour.
- **Dates as a ruled schedule:** the deadline and the term set as rows of capitals as large as a section head, the day left, what happens right, a `--rule-bar` over the first row.
- **The categories as a coded grid:** each shop, track or room in its primary cell, flush with its neighbours, with a black and white photograph or a list of what it covers above the fill.
- **Forms as a ruled sheet:** fields boxed in a grid of cells like an entry form, the category choice in its primaries, the submit an ink block at the foot.

### Controls

- A transparent `--rule-bar` ink-bordered button beside an ink-filled one, both square; on an ink band the pair inverts: the filled one turns putty with ink type, never a primary, since the primaries code categories.
- Links carry a 2px ink underline that thickens to 3px on hover; inputs are square with a `--rule-bar` ink border.
- The primaries are flat fills, never type and never tints. Each codes one category, the same one wherever it appears (a cell, a tag, a band, a nav link), and a set of one kind takes no colour. Blue and red fills take `--color-accent-ink`, the red deepened to `--color-accent-2-deep`; a yellow fill takes ink. Blue also rings focus.

### Motion

Static, like a printed prospectus: a link's underline thickens on hover, and nothing else moves, reveals or loops.

### Voice

Plain school prose: the shop, the week, the tuition, the deadline, each said once and plainly.

### Do-nots

- Never a fourth colour, a tint of a primary, a primary used as type, or a photograph in colour.
- Never a radius on a container, a button or an image; Werkstatt is square.
- Never mixed-case display; Jost here is capitals.
- Never the primaries as confetti or a pattern; each fill means a category.

### Build hint

```css
h1, h2, h3 { font-weight: 700; line-height: 1.02; text-transform: uppercase; }
small, th, figcaption { font-weight: 600; color: var(--color-muted); }
.btn { display: inline-flex; align-items: center; gap: var(--space-xs); padding: var(--space-md) var(--space-lg); border: var(--rule-bar) solid currentColor; font: 600 var(--text-sm)/1 var(--font-body); text-transform: uppercase; color: inherit; background: transparent; }
.btn--primary { background: var(--color-ink); border-color: var(--color-ink); color: var(--color-paper); }
.band--ink { background: var(--color-ink); color: var(--color-paper); }
.band--ink .btn--primary { background: var(--color-paper); border-color: var(--color-paper); color: var(--color-ink); }
.ruled { border-block: var(--rule-box) solid var(--color-ink); }
.photo { border: var(--rule-bar) solid var(--color-ink); border-radius: 0; }
table { border-top: var(--rule-bar) solid var(--color-ink); } td { border-bottom: var(--rule-hair) solid var(--color-rule); }
a { text-decoration-thickness: 2px; } a:hover { text-decoration-thickness: 3px; }
::selection { background: var(--color-accent-3); color: var(--color-ink); }
```
