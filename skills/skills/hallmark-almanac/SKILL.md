---
name: hallmark-almanac
description: "Almanac: cool slate stock with a pale printed sheet, blue-black ink, Hanken Grotesk heads over Newsreader prose with mono figures, two rule weights and square corners, one chart magenta. Fits: almanac, yearbook, field guide, reference, handbook, manual, index, catalogue, encyclopedia, data, figures, tables, statistics, research, dataset, records, directory, glossary, specifications"
metadata:
  origin: hallmark
  category: themes
  group: style
  mode: manual
  title: Almanac
  summary: редакционный, средний тон, сдержанный акцент
  preview: "#C4CBD2 #BBC2C8 #060E15 #970D63 #76004B · Hanken Grotesk"
---
# Almanac — a Hallmark style

The designer chose this style for the chat. A style is a material: paper, ink, faces, rules, radius, depth, controls
and voice. It is never a layout. It was written for web pages in CSS; in FigCraft:

- **Tokens become the file's variables.** Look at the file's variables first (`variable.export`). With no colour
  collection for this style, make one named «Almanac»: the `--color-*` tokens as colour variables without the prefix
  (`paper`, `ink`, `accent`…), radii as numbers; bind fills, strokes and radii to them (`variable.bind`), never paste
  hex. A file that already has its own colour system keeps it: restyle it onto this one only when asked.
- **Faces.** Check each family with `text.fonts {family}`. A missing one: say so in one line and take the nearest
  installed face of the same class (grotesk-sans); never swap silently. Make text styles for display, body, labels
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

## Genre: editorial (the default)

Content-led prompts: portfolios, manifestos, type specimens, agency sites, magazine pieces, podcasts, brand stories, considered consumer marketing. The silent default when no other genre signal fires. The deal leans toward this genre's themes; nothing here lists them.

## Voice

- **Accent:** one hue, held to the posture's footprint.
- **Layout:** asymmetric; hairlines, not card borders; type set large enough to hold its screen.
- **Motion:** quiet, one orchestrated entrance.
- **Copy:** specific, hand-set, slightly literary; verbs over adjectives.

## Allowed here

Hairline rules, fleurons, drop caps, double rules; italic inside running body copy; asymmetric column ratios (2:5, 3:7); photographs in the theme's treatment, captioned with facts; edge-aligned headlines; a single `<mark>` band behind the x-height.

## Refused here

Gradient-filled pills; a centred-everything hero (the genre is left-biased or asymmetric, unless the theme's material is a centred bill); glass (the medium is paper); pure black or white paper and ink.

## Chrome that fits

A masthead, a quiet edge-aligned bar, a colophon, a letter close. A marquee footer or a floating blur pill fights the register. Affinities, not assignments: gate 42 only asks that a default be named in the stamp rather than arrived at by reflex.


## The theme

The register of a reference book: cool slate stock, blue-black ink, Hanken Grotesk heads over Newsreader prose, figures in mono lined up to the decimal, rules in two weights, and one deep magenta, the colour a sea chart prints its lights in, kept small. It reads as exact because the rules and the numerals hold the authority, not colour or ornament. It is not a dashboard on grey and not a warm editorial page.

### Tokens

```css
:root {
  --color-paper: #C4CBD2; --color-paper-2: #BBC2C8; --color-paper-3: #AEB5BB;
  --color-ink: #060E15; --color-ink-2: #182027; --color-muted: #3B434B;
  --color-rule: #A1A9AF; --color-rule-2: #2B343B;
  --color-accent: #970D63; --color-accent-2: #76004B; --color-accent-ink: #F2F6F9; --color-focus: #9D0367;
  --color-sheet: #E5EAEF;
  --font-display: "Hanken Grotesk", ui-sans-serif, system-ui, sans-serif;
  --font-body: "Newsreader", ui-serif, Georgia, serif;
  --font-outlier: "IBM Plex Mono", ui-monospace, monospace;
  --radius-card: 0; --radius-pill: 2px; --rule-hair: 1px; --rule-bar: 2px; --shadow-card: none;
  --tracking-display: -0.02em; --display-weight: 600;
}
```

### Type

- **Display:** Hanken Grotesk 600 for every head, `--tracking-display`, line-height 1.05, sentence case, roman; the hero head tightens to -0.035em at line-height 0.95. The grotesk sets structure; the serif never sets a head.
- **Body:** Newsreader 400 and 500 with optical sizing, line-height 1.55; italic is in-paragraph emphasis only.
- **Labels, captions, table heads, meta:** Newsreader 500 a step smaller, sentence case, `--color-muted`. Never mono.
- **Figures:** IBM Plex Mono 400 and 500 with `tabular-nums`, right-aligned in a column, decimals lined up. Mono sets numerals and nothing else; a lone figure (a price, a count) may run to `--text-display` in Plex Mono 500 at -0.04em.

### Surfaces

- Two rule weights: `--rule-hair` in `--color-rule` parts rows and divisions; `--rule-bar` in `--color-rule-2` draws one firm line under a head or a table head. Nothing heavier.
- Square corners on every surface, 2px at most on a control. No boxed cards, no shadows: depth is a rule and a paper step (`--color-paper-2` on a well or an alternate row).
- The sheet: `--color-sheet` is the printed page, a pale stock laid on the slate with a 2px ink rule at its head and hairlines inside; the product's own pages and tables sit on it, never a paragraph.
- Bands: a `--color-paper-2` band, or one `--color-ink` band with paper text and mono in the sheet colour. Two bands a page at most; never a magenta field.
- Photographs: the subject at working distance (a harbour at low water, a slipway, the sea under weather), mid to far, flat overcast or first light, no face to the lens. Square, an inset 1px `--color-rule-2` outline, full-bleed or across ten columns; a caption beneath carries a fact; type never sits on a photograph.
- No texture: ruled paper, never a card surface.

### Range

- **The page itself:** a table set as the printed book sets it, on the sheet: a dated head over a 2px rule, the row names in Newsreader, times and heights in Plex Mono right-aligned, one row in magenta where the page points; it carries a hero or a split on its own.
- **One chart, set large:** a single series in magenta at 2px across twelve columns, the night or the off-hours shaded in paper steps, every turning point labelled in mono; with a control it becomes the page's one working thing.
- **The file on the ink band:** a header row and a handful of sample lines in Plex Mono in the sheet colour, the column names in magenta, a caption that says what the full file holds.
- **A comparison of editions or plans:** a Table of two or three columns, the firm rule under the head, prices as mono figures, the actions in the last row.

### Controls

- A magenta filled control (`--color-accent-ink` on `--color-accent`) beside a hairline-outlined control in ink, both Hanken Grotesk 500 at the 2px radius.
- Links in ink with a 1px magenta underline at a 0.15em offset that thickens on hover; inputs square with a 1px `--color-muted` edge.
- Magenta stays under 5% of a screen: the filled control, link underlines, the one series a chart argues from.

### Motion

Nothing moves except state: a row that links tints on hover, a link's underline thickens. No reveal, no count-up, no marquee.

### Voice

Declarative, dated, exact: cite the figure, the edition, the source, the unit. Never a hype adjective.

### Do-nots

- Never a hot pink or a violet; the magenta holds at L 44, hue 350, deep enough to read as a chart's print.
- Never warm or white paper; slate at hue 245, always tinted.
- Never a boxed card or a drop shadow; two rule weights carry every surface.
- Never a giant count as the hero, a page of small charts, or one mark for each day or port: one chart, set large, carries the data.
- Never a decorative wave or line drifting behind the type; a curve appears only as a chart with its axes.
- Never proportional figures in a column; numerals that compare are Plex Mono, tabular, right-aligned.

### Build hint

```css
body { color: var(--color-ink-2); }
h1, h2, h3 { font-weight: 600; color: var(--color-ink); }
.num, td.num { font-family: var(--font-outlier); font-variant-numeric: tabular-nums; text-align: right; }
thead th, .rule-firm { border-bottom: var(--rule-bar) solid var(--color-rule-2); }
th { font: 500 var(--text-sm)/1.3 var(--font-body); color: var(--color-muted); text-align: left; }
td { border-top: var(--rule-hair) solid var(--color-rule); }
.btn { border: var(--rule-hair) solid var(--color-ink); border-radius: var(--radius-pill); padding: var(--space-sm) var(--space-lg); font: 500 var(--text-sm)/1 var(--font-display); color: var(--color-ink); background: transparent; }
.btn--primary { background: var(--color-accent); border-color: var(--color-accent); color: var(--color-accent-ink); } .btn--primary:hover { background: var(--color-accent-2); }
.well { background: var(--color-paper-2); border-top: var(--rule-bar) solid var(--color-rule-2); }
.sheet { background: var(--color-sheet); border-top: var(--rule-bar) solid var(--color-ink); }
.band--ink { background: var(--color-ink); color: var(--color-paper); }
.chart .series { fill: none; stroke: var(--color-accent); stroke-width: 2; }
.photo > img { outline: var(--rule-hair) solid var(--color-rule-2); outline-offset: -1px; }
a { color: var(--color-ink); text-decoration-color: var(--color-accent); text-underline-offset: 0.15em; } a:hover { text-decoration-thickness: 2px; }
```
