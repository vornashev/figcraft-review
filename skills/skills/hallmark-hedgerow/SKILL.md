---
name: hallmark-hedgerow
description: "Hedgerow: deep leaf-green paper, cream ink, Prata heads over Manrope, low-key photographs in true colour, square flat surfaces with pill controls, one chartreuse signal with a moss strength for cream. Fits: distillery, gin, brewery, forager, botanicals, nature reserve, walking, trail, seeds, plants, nursery, hedge, countryside, field guide, provenance, harvest, batch, seasonal, map, miles"
metadata:
  origin: hallmark
  category: themes
  group: style
  mode: manual
  title: Hedgerow
  summary: редакционный, тёмный, залит цветом
  preview: "#032615 #001B0D #EEE7D8 #CAE430 #DDF18A · Prata"
---
# Hedgerow — a Hallmark style

The designer chose this style for the chat. A style is a material: paper, ink, faces, rules, radius, depth, controls
and voice. It is never a layout. It was written for web pages in CSS; in FigCraft:

- **Tokens become the file's variables.** Look at the file's variables first (`variable.export`). With no colour
  collection for this style, make one named «Hedgerow»: the `--color-*` tokens as colour variables without the prefix
  (`paper`, `ink`, `accent`…), radii as numbers; bind fills, strokes and radii to them (`variable.bind`), never paste
  hex. A file that already has its own colour system keeps it: restyle it onto this one only when asked.
- **Faces.** Check each family with `text.fonts {family}`. A missing one: say so in one line and take the nearest
  installed face of the same class (high-contrast-serif); never swap silently. Make text styles for display, body, labels
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

A dark page that reads as green, not night: a deep leaf-green ground, cream ink, Prata's sharp high-contrast names over a quiet Manrope, plants photographed close in shade, and one chartreuse that marks the controls and the few lines the page draws. It feels botanical, exact and fresh, like a field guide opened on a bench. It is not black luxury with a gold accent, and not a rustic kraft-paper page.

### Tokens

```css
:root {
  --color-paper: #032615; --color-paper-2: #001B0D; --color-paper-3: #143423;
  --color-ink: #EEE7D8; --color-ink-2: #B2C8B5; --color-muted: #88A48D;
  --color-rule: #224230;
  --color-accent: #CAE430; --color-accent-2: #DDF18A; --color-accent-deep: #446401; --color-accent-ink: #012111; --color-focus: #DDF18A;
  --font-display: "Prata", Georgia, serif; --font-body: "Manrope", ui-sans-serif, system-ui, sans-serif;
  --font-outlier: "IBM Plex Mono", ui-monospace, monospace;
  --radius-card: 0; --radius-pill: 999px; --rule-hair: 1px;
  --shadow-card: none;
  --tracking-display: -0.005em; --display-weight: 400;
}
```

One dial, the colourway, stated in the stamp (`hedgerow: hedge`). `--color-accent-deep` is the moss strength of the signal: it takes the chartreuse's place on the cream band, where chartreuse vanishes.

| Colourway | Ground | Ink | Accent |
| --- | --- | --- | --- |
| `hedge` (default) | #032615 | cream #EEE7D8 | chartreuse #CAE430 |
| `sloe` | plum #2E1733 | #F2EADD | straw #F6D653 |

### Type

- **Display:** Prata 400, its only weight, `font-synthesis: none`; line-height 1.08, sentence case, roman. Item titles take Prata too, never under 22px, where its hairlines thin out. Figures at statement size are Prata, lining.
- **Body:** Manrope 400 at 17px, line-height 1.6, in `--color-ink-2`; 500 for labels, 700 only on controls.
- **Labels, captions, table heads:** Manrope 500 a step smaller, sentence case, untracked, `--color-muted`. A plant's Latin name sits beside its common one in this style, roman. IBM Plex Mono only inside code.

### Surfaces

- 1px rules: `--color-rule` between rows, `--color-muted` where two sections part, a 1.5px chartreuse rule heading the one list that matters most.
- Square and flat: radius 0 on wells, photographs and inputs; no shadow, no blur, no gradient but a photograph's scrim. Depth is a paper step: a well in `--color-paper-3`, a band in `--color-paper-2`.
- Bands: a `--color-paper-2` band, and one cream band (`--color-ink` ground, `--color-paper` text, moss line work, hedge-green controls) for the densest section. Two a page at most.
- Photographs: plants as a forager meets them, close and low-key: one plant at arm's length in shade, a hedge along a lane, the land at first light, the still, a glass on a dark bench. Square, a 1px cream ring at 8%, colour kept true, never toned green. A caption names the plant under the frame; type on a photograph only over a hedge-green scrim at 45 to 70%.
- Line work only for a chart or a map of real places, 1.2px chartreuse strokes, unfilled. No texture.

### Range

- **Index as a field guide:** Rows with the common name in Prata at `--text-2xl` or larger, the Latin name in the label style, then one line, under the chartreuse rule; the plants carry a section with no picture.
- **Figures as a bottle label:** the batch, the count, the price, the distance in Prata at `--text-display-s` and up, parted by `--color-rule` verticals on a `--color-paper-2` band; one figure in chartreuse.
- **Statement in cream:** one Prata sentence at display size on the green, or the cream band holding a working control (a quantity and its running total in Prata) with moss rules.
- **Table as a still log:** batch, date bottled, count and price as ruled rows, numerals tabular, the current row's rule chartreuse.

### Controls

- The pair: a chartreuse pill in Manrope 700 with `--color-accent-ink` text beside a pill outlined in 1.5px chartreuse. The primary lightens to `--color-accent-2` on hover. On the cream band both turn hedge green.
- Links are cream with a 1px chartreuse underline; inputs are square, a 1px `--color-muted` border on `--color-paper-2`, the ring in `--color-focus`.

### Motion

Still. State only, over `--dur-short` on `--ease-out`: the primary lightens, an underline thickens, a row's rule turns chartreuse. No growth, no drift, no scroll reveal.

### Voice

A field guide's: the plant and where it grows, then how far and when, only where the prompt knows; never invent a distance or a month. Provenance as a sentence, never a badge.

### Do-nots

- Never a second accent; sold out is muted, not red.
- Never a black or blue-black ground; the dark is leaf green, or plum on `sloe`.
- Never a bright, high-key photograph: a berry on white or a sunny meadow reads as a hole in the green.
- Never chartreuse running text, a chartreuse band, or chartreuse on cream.

### Build hint

```css
h1, h2, h3 { font-weight: 400; line-height: 1.08; font-synthesis: none; }
.btn { border: 1.5px solid var(--color-accent); border-radius: var(--radius-pill); padding: var(--space-sm) var(--space-lg); font-size: var(--text-sm); font-weight: 700; transition: background-color var(--dur-short) var(--ease-out); }
.btn--primary { background: var(--color-accent); color: var(--color-accent-ink); }
.btn--primary:hover { background: var(--color-accent-2); border-color: var(--color-accent-2); }
.btn--secondary { background: transparent; color: var(--color-accent); }
.band--cream { background: var(--color-ink); color: var(--color-paper); --color-rule: color-mix(in oklab, var(--color-paper) 22%, var(--color-ink)); }
.band--cream .btn { border-color: var(--color-paper); color: var(--color-paper); }
.band--cream .btn--primary { background: var(--color-paper); color: var(--color-ink); }
.band--cream .figure { color: var(--color-accent-deep); }
.index { border-top: 1.5px solid var(--color-accent); }
.index > li { border-bottom: var(--rule-hair) solid var(--color-rule); }
.photo img { outline: var(--rule-hair) solid color-mix(in oklab, var(--color-ink) 8%, transparent); outline-offset: -1px; }
.figure { font-family: var(--font-display); font-variant-numeric: lining-nums tabular-nums; }
a { text-decoration-color: var(--color-accent); }
```
