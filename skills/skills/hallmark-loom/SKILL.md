---
name: hallmark-loom
description: "Loom: ecru paper with sand steps, warm near-black ink, Libre Caslon Display heads and prices over Hanken Grotesk, thin rules and one ink rule, cloth photographed close in window light, one deep indigo. Fits: weaving, textile, linen, wool, weaving studio, cloth, craft, atelier, handmade, natural, indigo, fabric, by the metre, workshop, maker, slow, commission, interiors, samples"
metadata:
  origin: hallmark
  category: themes
  group: style
  mode: manual
  title: Loom
  summary: редакционный, светлый, уверенный акцент
  preview: "#F4F0E6 #ECE4D5 #1D1713 #1D3172 #314A94 · Libre Caslon Display"
---
# Loom — a Hallmark style

The designer chose this style for the chat. A style is a material: paper, ink, faces, rules, radius, depth, controls
and voice. It is never a layout. It was written for web pages in CSS; in FigCraft:

- **Tokens become the file's variables.** Look at the file's variables first (`variable.export`). With no colour
  collection for this style, make one named «Loom»: the `--color-*` tokens as colour variables without the prefix
  (`paper`, `ink`, `accent`…), radii as numbers; bind fills, strokes and radii to them (`variable.bind`), never paste
  hex. A file that already has its own colour system keeps it: restyle it onto this one only when asked.
- **Faces.** Check each family with `text.fonts {family}`. A missing one: say so in one line and take the nearest
  installed face of the same class (roman-serif); never swap silently. Make text styles for display, body, labels
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

A weaving studio speaking quietly: ecru paper, Caslon cut for display with a book's calm over a plain Hanken Grotesk, thin rules, and one deep indigo, the colour of dyed yarn, that arrives as a band or a button and never as a wash. The cloth is photographed close in window light; nothing is drawn to stand in for it. It reads crafted because the page is ruled like a pattern book. It is not a cream-and-terracotta craft page and not a linen photograph behind everything.

### Tokens

```css
:root {
  --color-paper: #F4F0E6; --color-paper-2: #ECE4D5; --color-paper-3: #D9CCB7;
  --color-ink: #1D1713; --color-ink-2: #352F2A; --color-muted: #5E5650;
  --color-rule: #CEC6B8; --color-rule-ink: #1D1713;
  --color-accent: #1D3172; --color-accent-2: #314A94; --color-accent-ink: #F4F0E6; --color-focus: #2B46A1;
  --font-display: "Libre Caslon Display", "Libre Caslon Text", ui-serif, Georgia, serif; --font-body: "Hanken Grotesk", ui-sans-serif, system-ui, sans-serif;
  --font-outlier: "DM Mono", ui-monospace, monospace;
  --radius-card: 0; --radius-pill: 0; --rule-hair: 1px; --rule-ink: 2px;
  --shadow-card: none;
  --tracking-display: -0.01em; --display-weight: 400;
}
```

Three colourways, stated in the stamp (`loom: ecru`).

| Colourway | Paper, ink, indigo |
| --- | --- |
| `ecru` (default) | the block above |
| `indigo` | paper `#1F346B`, ink ecru `#F3EEE3`, rule `#4B6197`; the button turns ecru with indigo text |
| `oat` | paper `#E6D5BB`, ink `#0E0A07`, rules in the ink at 1px, indigo `#293F77` kept to a rule and a button |

### Type

- **Display:** Libre Caslon Display 400 for the h1, every h2 and any price or figure at 40px or more, `--tracking-display`, line-height 1.04 (1.0 on a hero head of two lines), sentence case, roman. The face has one weight and no italic; never synthesise either, and never set it under 32px, where its hairlines break up.
- **Item titles (h3):** Hanken Grotesk 500 at `--text-title`, line-height 1.25, the ink.
- **Body:** Hanken Grotesk 400 and 500 at 16 to 18px, line-height 1.5; the lead in `--color-muted`.
- **Labels, captions, tags, table heads:** Hanken Grotesk 500 a step smaller, sentence case, untracked, in `--color-muted`. DM Mono only for figures that compare in a row (widths in centimetres, grams per metre, metres on the beam) and for code.

### Surfaces

- 1px rules: `--color-rule` between rows; a `--rule-ink` line in the ink above a list's first row, under a table's head and under the nav; no borders on wells.
- Square everywhere: radius 0 on wells, photographs, inputs and controls.
- Flat: depth is a paper step, `--color-paper-2` as a band or well and sand (`--color-paper-3`) as a deeper well; nothing casts a shadow.
- Bands: a `--color-paper-2` band, or one indigo band (`--color-accent` ground, `--color-accent-ink` text). Two a page at most.
- Photographs: the cloth and the loom, close and in side light from a window: the weave filling the frame, warp on the beam, a folded length, yarn on cones; the studio wide once. Colour kept true and softened a little (the `photo:` line). Square, an inset outline of ink at 8%, no shadow; captions beneath in the label style carry a fact (the fibre, the price a metre); type sits on a photograph only over an ink scrim at its calmest edge.
- No texture: the photographs carry the weave.

### Range

- **The specification as ruled rows:** fibre, width, weight, lead time and price as a pattern-book sheet, the label on the left in Hanken, the value in Caslon at title size and up, the price row set largest; an ink rule above the first row.
- **The price as a figure:** the price a metre in Caslon at display size beside the sum worked out in rows (metres, rate, total), on a sand well or on the indigo band where the order is placed.
- **Time as a ruled scale:** a lead time drawn as weeks on a hairline scale in DM Mono, the span the cloth is on the loom as a sand bar and the window it lands in as an indigo line; a chart of the prompt's own weeks, never a drawn thread.
- **A comparison in two columns:** linen beside wool, parted by one ink rule, rows aligned.

### Controls

- The pair: an indigo-filled square button in Hanken Grotesk 500 with ecru text beside a text link with a 2px bottom border in the text colour. On indigo the button turns ecru with indigo text.
- Links lift their 2px underline into `--color-accent` on hover; inputs are square with a 1px `--color-rule` border and the indigo focus ring, ecru on the indigo band.
- Indigo is a fill or a line: the primary, one band, an underline on hover, the focus ring.

### Motion

Nothing moves except state: an underline turns indigo and the primary lightens to `--color-accent-2`, over `--dur-short` on `--ease-out`, once.

### Voice

The weaver speaking plainly at the loom: the fibre, the metre, the weeks, the room the cloth is for. Prices and times said once, nothing sold hard.

### Do-nots

- Never indigo as a page wash or a tint on the ecru colourway; it is a band, a line or a fill.
- Never a mono label voice; widths and weights earn the mono, the captions do not.
- Never a ruler, a warp or a thread pattern drawn on the page; the cloth is photographed and the metre priced in type.
- Never a warm accent (rust, clay, terracotta) next to the ecru; sand is a paper, not an accent.
- Never a radius, a shadow or a soft card; Loom is rules, squares and paper steps.

### Build hint

```css
h1, h2, h3 { font-weight: 400; line-height: 1.04; font-synthesis: none; }
.num { font-family: var(--font-outlier); font-variant-numeric: tabular-nums; }
.btn { display: inline-flex; align-items: center; padding: var(--space-md) var(--space-lg); font: 500 var(--text-sm)/1 var(--font-body); background: var(--color-accent); color: var(--color-accent-ink); transition: background-color var(--dur-short) var(--ease-out); }
.btn:hover { background: var(--color-accent-2); }
.link { font-weight: 500; padding-block: var(--space-2xs); border-bottom: 2px solid currentColor; text-decoration: none; transition: border-color var(--dur-short) var(--ease-out); }
.link:hover { border-color: var(--color-accent); }
.photo img { outline: 1px solid color-mix(in oklab, var(--color-ink) 8%, transparent); outline-offset: -1px; }
.photo figcaption { margin-top: var(--space-sm); font: 500 var(--text-sm)/1.4 var(--font-body); color: var(--color-muted); }
.band--indigo { background: var(--color-accent); color: var(--color-accent-ink); }
.band--indigo .btn { background: var(--color-paper); color: var(--color-accent); }
.band--indigo :focus-visible { outline-color: var(--color-accent-ink); }
```
