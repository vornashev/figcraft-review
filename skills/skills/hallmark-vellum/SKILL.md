---
name: hallmark-vellum
description: "Vellum: parchment paper, a long tan fibre wash on bands, umber ink, Grenze Gotisch heads over Hanken Grotesk with Grenze roman for statements, hairline and double rules, one ultramarine pigment. Fits: roastery, coffee, bakery, wine, cellar, apothecary, bookshop, press, letterpress, guild, heritage, artisan, manuscript, parchment, edition, tasting, vintage, craft, old world, slow"
metadata:
  origin: hallmark
  category: themes
  group: style
  mode: manual
  title: Vellum
  summary: редакционный, светлый, уверенный акцент
  preview: "#F3EADA #E9DCC7 #261A12 #2942AB · Grenze Gotisch"
---
# Vellum — a Hallmark style

The designer chose this style for the chat. A style is a material: paper, ink, faces, rules, radius, depth, controls
and voice. It is never a layout. It was written for web pages in CSS; in FigCraft:

- **Tokens become the file's variables.** Look at the file's variables first (`variable.export`). With no colour
  collection for this style, make one named «Vellum»: the `--color-*` tokens as colour variables without the prefix
  (`paper`, `ink`, `accent`…), radii as numbers; bind fills, strokes and radii to them (`variable.bind`), never paste
  hex. A file that already has its own colour system keeps it: restyle it onto this one only when asked.
- **Faces.** Check each family with `text.fonts {family}`. A missing one: say so in one line and take the nearest
  installed face of the same class (blackletter); never swap silently. Make text styles for display, body, labels
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

An old printing house: a parchment ground, umber ink, Grenze Gotisch for the heads, its roman sibling Grenze for a sentence set large, a plain Hanken Grotesk for everything read, hairlines and double rules, and ultramarine as the one pigment. The gothic face carries the age, so nothing else is ornamented: no tavern, no distressed pastiche, no cream-and-serif editorial page.

### Tokens

```css
:root {
  --color-paper: #F3EADA; --color-paper-2: #E9DCC7; --color-paper-3: #DECFB7;
  --color-ink: #261A12; --color-ink-2: #3A2D24; --color-muted: #62554A;
  --color-rule: #BCAB96;
  --color-accent: #2942AB; --color-accent-deep: #1B2E87; --color-accent-soft: #D1DBF3; --color-accent-ink: #F5EEE0;
  --color-focus: #3856C8; --color-field: var(--color-accent);
  --font-display: "Grenze Gotisch", ui-serif, Georgia, serif; --font-body: "Hanken Grotesk", ui-sans-serif, sans-serif;
  --font-outlier: "Grenze", ui-serif, Georgia, serif;
  --radius-card: 2px; --radius-pill: 2px; --rule-hair: 1px; --rule-double: 4px; --shadow-card: none;
  --tracking-display: -0.01em; --display-weight: 600; --fibre: 0.5;
}
```

Three colourways, stated in the stamp (`vellum: parchment`).

| Colourway | Ground, ink, pigment |
| --- | --- |
| **parchment** (default) | the tokens above |
| **oxblood, reversed** | ground `#490C13`, ink `#F2EADD`, pigment gold `#EBC573` texted in the ground, rule `#793F40`, fibre at 0.25 |
| **indigo, the ledger** | ground `#E1E9EF`, ink `#171F30`, the same ultramarine, rule `#A8B2BE`, fibre at 0.14 |

### Type

- **Display:** Grenze Gotisch 600 for `h1` and `h2`, line-height 0.92, `--tracking-display`, sentence case. It closes up below 30px, so `h3` and smaller set in Hanken Grotesk 600.
- **Outlier, Grenze 400:** the roman sibling, for one sentence set at `--text-display-s` and for figures at display size, line-height 1.02. Never for running text.
- **Body:** Hanken Grotesk 400 and 500, line-height 1.55; nav links at 600. Three weights a page at most: 400, 500, 600.
- **Labels, captions, table heads, meta:** Hanken Grotesk 500 a step smaller, sentence case, untracked. Figures that a table compares (weights, lots, dates) take Hanken's tabular figures, right-aligned.

### Surfaces

- Rules: 1px `--color-rule` hairlines between rows, 1px ink along a section's top, and a `--rule-double` double ink rule where a printer would double one: over a table's head, under the masthead, along the top of a band.
- Radius 2px everywhere, no pills, no shadows: the page is printed flat.
- Bands: a `--color-paper-2` band carrying the fibre wash, and one ultramarine `--color-field`; two a page at most, never touching.
- Photographs: the trade in its own light (the drum, the cooling tray, sacks, the counter, hands at the bench), close, no face to the lens; warmed, 2px radius, a 1px `--color-rule` edge. Captions beneath carry a fact; a head sits on one only over an umber scrim.
- Texture, the fibre wash: long tan fibres of SVG turbulence, stitched so they never tile, multiplied at `--fibre` (`texture.md`, the low-frequency wash), on a band or a well only.

### Range

- **Table as a day book:** the week's list as a full-width ruled table under a double rule, pigment numerals indexing the rows, the name in Hanken 600 at title size, values in tabular figures; a hovered row takes `--color-accent-soft`.
- **Statement with figures:** one sentence of the prompt in Grenze 400 across nine or ten columns on the fibre band, and beneath it, parted by a hairline, the prompt's own numbers in Grenze Gotisch at display size in pigment with a plain label under each.
- **Form on the field:** the ultramarine band holding a working choice (a size, a frequency) as square cells joined edge to edge, the running answer in Grenze Gotisch at section size.
- **Rows as an index:** three to five ruled rows, the title in Grenze Gotisch at section size, one line of Hanken beside it: terms, visits, ways to buy.

### Controls

- A pigment-filled primary (`--color-accent-ink` on `--color-accent`) that deepens to `--color-accent-deep` on hover, beside a ghost with a 1px ink border, both 2px radius, Hanken Grotesk 500.
- Links underline in pigment on hover; inputs take 2px radius and a 1px ink border.
- Ultramarine is the one pigment: the primary, a link's hover, the focus ring, the numerals that index a list, the figures, one band.

### Motion

Still. A hover underline in pigment, a row's soft wash and the primary deepening over `--dur-micro`; no reveal, no parallax.

### Voice

Ledger-plain and dated: the item, the weight, the year, the town, as a clerk would enter them. Never *artisanal*, *curated*, or a story the prompt did not give.

### Do-nots

- Never clay, terracotta or oxblood as the pigment on parchment; oxblood is a ground only.
- Never Grenze Gotisch below 30px, at paragraph length, or opening a head on a capital I, which reads as J.
- Never a deckled edge, a vignette, a coffee ring, a burn or a second texture.
- Never the founding year alone as the hero's head; it sits in a sentence, a row or a figure with its label.

### Build hint

```css
h1, h2 { font-weight: 600; line-height: 0.92; }
h3 { font-family: var(--font-body); font-weight: 600; }
.statement { font: 400 var(--text-display-s)/1.02 var(--font-outlier); }
.btn { border: var(--rule-hair) solid currentColor; border-radius: var(--radius-card); padding: var(--space-sm) var(--space-lg); font-weight: 500; color: inherit; background: transparent; transition: background-color var(--dur-micro) var(--ease-out); }
.btn--primary { background: var(--color-accent); border-color: var(--color-accent); color: var(--color-accent-ink); }
.btn--primary:hover { background: var(--color-accent-deep); border-color: var(--color-accent-deep); }
.band--pigment { background: var(--color-field); color: var(--color-accent-ink); }
.rule-double { border-top: var(--rule-double) double var(--color-ink); }
.ledger tbody tr:hover { background: var(--color-accent-soft); }
.fibre { position: relative; isolation: isolate; }
.fibre::before { content: ""; position: absolute; inset: 0; z-index: -1; opacity: var(--fibre); mix-blend-mode: multiply; pointer-events: none;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='400' height='400'%3E%3Cfilter id='p' x='0' y='0' width='100%25' height='100%25'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.004 0.02' numOctaves='4' seed='4' stitchTiles='stitch'/%3E%3CfeColorMatrix values='0 0 0 0 0.62 0 0 0 0 0.52 0 0 0 0 0.36 0 0 0 0.3 0'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23p)'/%3E%3C/svg%3E"); }
```
