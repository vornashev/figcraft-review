---
name: hallmark-brutal
description: "Brutal: near-white poster stock, near-black ink as 3px rules, boxed cells and solid fills, uppercase Libre Franklin 900 over its 400, zero radius, one acid-yellow fill. Fits: brutalist, raw, bold, high-contrast, statement, agency, design studio, portfolio, streetwear, drop, zine, type-forward, graphic design, poster, festival, collective, no-nonsense, uncompromising"
metadata:
  origin: hallmark
  category: themes
  group: style
  mode: manual
  title: Brutal
  summary: редакционный, светлый, уверенный акцент
  preview: "#F8F7F2 #ECEBE6 #040302 #F2E309 · Libre Franklin"
---
# Brutal — a Hallmark style

The designer chose this style for the chat. A style is a material: paper, ink, faces, rules, radius, depth, controls
and voice. It is never a layout. It was written for web pages in CSS; in FigCraft:

- **Tokens become the file's variables.** Look at the file's variables first (`variable.export`). With no colour
  collection for this style, make one named «Brutal»: the `--color-*` tokens as colour variables without the prefix
  (`paper`, `ink`, `accent`…), radii as numbers; bind fills, strokes and radii to them (`variable.bind`), never paste
  hex. A file that already has its own colour system keeps it: restyle it onto this one only when asked.
- **Faces.** Check each family with `text.fonts {family}`. A missing one: say so in one line and take the nearest
  installed face of the same class (grotesk-heavy); never swap silently. Make text styles for display, body, labels
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

A raw, engineered sheet: near-white poster stock, near-black ink that arrives as 3px rules, boxed cells and solid fills, Libre Franklin at its blackest in tight capitals, zero radius, and one acid yellow that only ever fills. The grid is drawn, not implied: cells share their rules, and a number or a word set big inside a box is the page's ornament. Photographs print hard in the ink. It is not a dark hacker page, not a decorated zine and not a sticker sheet of offset shadows.

### Tokens

```css
:root {
  --color-paper: #F8F7F2; --color-paper-2: #ECEBE6; --color-paper-3: #DEDCD7;
  --color-ink: #040302; --color-ink-2: #0E0D0A; --color-muted: #494843;
  --color-rule: #040302;
  --color-accent: #F2E309; --color-accent-ink: #040302; --color-focus: #61620C;
  --font-display: "Libre Franklin", ui-sans-serif, system-ui, sans-serif; --font-body: var(--font-display);
  --font-outlier: var(--font-display);
  --radius-card: 0; --radius-pill: 0; --rule-hair: 1px; --rule-bar: 3px; --shadow-card: none;
  --tracking-display: -0.03em; --display-weight: 900;
}
```

### Type

- **Display:** Libre Franklin 900, uppercase, `--tracking-display`, line-height 1.0 (the floor for capitals that wrap), one weight per head. A statement or the hero head may run to the display cap and past it; set it to fill the measure, not to sit politely inside it. Uppercase belongs to heads, the wordmark and a word or number set as a cell's whole content.
- **Body:** Libre Franklin 400 at 17 to 18px, line-height 1.5, sentence case, in ink; item titles and controls at 700, sentence case. Three weights in all: 400, 700, 900.
- **Numbers:** index numbers, counts and dates in 900 with `tabular-nums`, at `--text-section` or larger when they carry a row.
- **Labels, captions, table heads:** Libre Franklin 400 a step smaller, sentence case, in `--color-muted`; mono appears only inside code.

### Surfaces

- Two rule weights and no others: `--rule-bar` in `--color-rule` boxes a well, a table, a cell or a photograph; `--rule-hair` splits rows inside them. Neighbouring cells share one 3px rule, never two.
- Zero radius on everything. Depth is fill and border, never shadow: bordered paper, an ink fill with paper text, or the one yellow fill under ink; nothing floats above the paper.
- Bands: an `--color-ink` band with paper text, or a `--color-paper-2` band ruled top and bottom with `--rule-bar`; two a page at most. The yellow never runs as a band.
- Photographs: raw documentary of the thing in use, lit by whatever was there (stage light, flash, a street at night): the crowd from inside it, a room before doors, a stage screen; never a posed face. They print hard in the ink (the `photo:` duotone), cropped tight and flush inside a `--rule-bar` frame, or full-bleed where the page is loudest. Type meets a photograph only on a solid ink or paper block set flush against the frame; never a scrim.
- No texture, no ornament, no gradient.

### Range

- **An index as a boxed table:** rows inside one 3px box, hairlines between, the number in 900 at section size in its own cell, the entry in 700 at title size, one line in 400; the hovered or current row fills yellow under its ink.
- **A statement:** one blunt sentence in 900 capitals across all twelve columns at display size or larger, sitting on a 3px rule, nothing else on the screen but its attribution.
- **Cells as a bento:** facts set as words or numbers in 900 capitals inside boxed cells that share their rules, one lead cell twice the size, an ink cell for contrast, a photograph flush in one cell.
- **The form as the grid:** fields as boxed cells sharing their rules, a choice set as two big word cells that fill yellow when chosen, the send button an ink cell.

### Controls

- The pair: a `--rule-bar` bordered paper button beside a solid ink button with paper text, Libre Franklin 700 in sentence case, 48 to 52px; hover inverts either in one frame.
- Links are ink, underlined; hover fills yellow under the ink. Inputs: zero radius, a `--rule-bar` border, ink on paper, 52px.
- The yellow is a fill, never type, a rule or a ring: a chosen option, a `mark` in running text, a hovered row or link. Always under ink, never over a photograph, under 5% of a screen. Focus takes the deep olive `--color-focus`.

### Motion

Nothing glides. State flips in one frame: a surface inverts to ink with paper text, or fills yellow under its ink. No reveal, no bounce, no parallax.

### Voice

Blunt, declarative: capitals in the heads, sentence case everywhere else; the trade's own words, no hedging, no hype. Say the thing flat.

### Do-nots

- Never a rounded corner or a shadow, blurred or hard-offset; depth is border and fill.
- Never an ornament, a fleuron or a layered offset stack; Brutal is raw, not decorated.
- Never black paper; this is a light sheet with black structure.
- Never a second colour: photographs print in the ink, and the yellow only fills.
- Never two rules where cells meet; a doubled 6px seam reads as a mistake, not as structure.

### Build hint

```css
h1, h2, .display { font-family: var(--font-display); font-weight: var(--display-weight); text-transform: uppercase; letter-spacing: var(--tracking-display); line-height: 1; }
h3 { font-family: var(--font-display); font-weight: 700; }
.btn { border: var(--rule-bar) solid var(--color-rule); border-radius: 0; padding: var(--space-xs) var(--space-lg); background: var(--color-paper); color: var(--color-ink); font-weight: 700; transition: none; }
.btn:hover, .btn--ink { background: var(--color-ink); color: var(--color-paper); } .btn--ink:hover { background: var(--color-paper); color: var(--color-ink); }
.cells { display: grid; gap: 0; border: var(--rule-bar) solid var(--color-rule); }
.cells > * { margin: calc(var(--rule-bar) * -1) 0 0 calc(var(--rule-bar) * -1); border: var(--rule-bar) solid var(--color-rule); }
.well--ink, .band--ink { background: var(--color-ink); color: var(--color-paper); }
.is-chosen, p mark, a:hover { background: var(--color-accent); color: var(--color-accent-ink); }
.photo { display: block; border: var(--rule-bar) solid var(--color-rule); border-radius: 0; }
::selection { background: var(--color-accent); color: var(--color-accent-ink); }
```
