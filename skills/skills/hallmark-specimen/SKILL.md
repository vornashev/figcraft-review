---
name: hallmark-specimen
description: "Specimen: warm oat paper, warm near-black ink, razor-hairline Bodoni Moda over Geist, square 1px rules, one ink-blue signal that also draws the metric guides. Fits: typography, type specimen, foundry, letterform, portfolio, editorial, magazine, essay, type studio, agency, brand story, print, publication, craft, considered, literary"
metadata:
  origin: hallmark
  category: themes
  group: style
  mode: manual
  title: Specimen
  summary: редакционный, светлый, сдержанный акцент
  preview: "#F9F3E8 #F1E8DB #130E0A #144BB7 · Bodoni Moda"
---
# Specimen — a Hallmark style

The designer chose this style for the chat. A style is a material: paper, ink, faces, rules, radius, depth, controls
and voice. It is never a layout. It was written for web pages in CSS; in FigCraft:

- **Tokens become the file's variables.** Look at the file's variables first (`variable.export`). With no colour
  collection for this style, make one named «Specimen»: the `--color-*` tokens as colour variables without the prefix
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

A foundry's material: warm oat paper, warm near-black ink, Bodoni Moda 400 pinned at its highest optical size so the hairlines thin to a razor against the stems, a Geist body beneath it, square 1px rules and one ink-blue signal. It reads as hand-set and exact because all the contrast lives inside the letters, none in colour or depth. It is not a cream luxury page with a terracotta accent, and not a fashion masthead in bold Didone.

### Tokens

```css
:root {
  --color-paper: #F9F3E8; --color-paper-2: #F1E8DB; --color-paper-3: #E4D9CA;
  --color-ink: #130E0A; --color-ink-2: #2E2722; --color-muted: #665F58;
  --color-rule: #C5BCB1; --color-rule-2: #9A9085;
  --color-accent: #144BB7; --color-accent-ink: #F9F5EC; --color-focus: #235BC8;
  --color-guide: #3A6CCE80;
  --font-display: "Bodoni Moda", ui-serif, Georgia, serif; --font-body: "Geist", ui-sans-serif, system-ui, sans-serif;
  --font-outlier: "Geist Mono", ui-monospace, monospace;
  --radius-card: 0; --radius-pill: 0; --rule-hair: 1px;
  --shadow-card: none;
  --tracking-display: -0.02em; --display-weight: 400; --display-optical: 96;
}
```

`--color-guide` is the blue's second strength: a translucent hairline for a metric guide (cap height, x-height, baseline) drawn under a word, never a fill. `--color-rule-2` is the darker hairline for a control's track or a table's head.

### Type

- **Display:** Bodoni Moda 400, `--tracking-display`, line-height 1.02, sentence case, roman. `h1` and `h2` take `"opsz" 96`, where the hairline nearly vanishes against the stem and that contrast is the graphic; an `h3` lets the axis follow its size, since a razor hairline breaks at 25px. A word set as a poster may run to 20vw.
- **Body:** Geist 400 at 17px, line-height 1.55; the plain sans under the Didone is the tension. Bodoni Moda italic stays inside running text or a sample, never a head.
- **Labels, captions, table heads:** Geist 500 a step smaller, sentence case, `--color-muted`. Geist Mono only on figures that compare (a size, a weight, a code point), tabular.

### Surfaces

- 1px `--color-rule` hairlines on divisions, table rows and between cells; a 3px `double` rule heads the one table that matters, once a page.
- No depth: nothing lifts, nothing casts a shadow, nothing is rounded. A well is a paper step (`--color-paper-2`) inside a hairline.
- Bands: a `--color-paper-2` band, or one `--color-ink` band with oat type, where the Didone reads sharpest; two a page at most, never a blue one.
- Photographs: one at most, the face's world: a reading room, a book open on a desk, metal sorts in a case; it prints in ink on oat (the duotone) as a plate, square, inside a hairline, eight columns or the full container. Its caption names the setting beneath it; type never sits on it.
- No texture, no mesh, no gradient behind type: the oat is a colour, not a paper scan.

### Range

- **Statement with guides:** one word or line at poster size with `--color-guide` hairlines at its real cap height, x-height and baseline, each named in the label style.
- **Rows as a waterfall:** one line falling through sizes, each row its size in Geist Mono at left, hairlines between, every line cut to fit its row.
- **Grid as a character set:** hairline cells across twelve columns, one lead cell four wide holding a glyph at display size; the current cell fills ink.
- **Comparison and price list:** roman beside italic on the ink band, one passage each at reading size; the licence as a ruled table under the double rule, the price in Didone at `--text-display-s`.

### Controls

- The pair: an ink-filled rectangle with oat text beside a 1px ink-outlined one, both square, Geist 500, 48px tall.
- A range is a 1px `--color-rule-2` track with a square ink thumb; a toggle is two square cells inside one ink hairline, the pressed one paper with a 2px ink rule beneath, so the ink fill stays the primary's. Inputs are square with the `--color-focus` ring.
- Links carry a 1px ink-blue underline at 0.18em that thickens on hover. The blue stays under 5% of a screen: a link, the focus ring, the guides, one figure.

### Motion

Nothing moves except state: an underline thickens, a cell fills, a sample takes the size and weight it was given. No reveal, no loop, nothing on arrival.

### Voice

Editorial, hand-set, lightly literary. Verbs over adjectives; name the face, the size, the number.

### Do-nots

- Never a heavy display head; bold turns the Didone into a fashion masthead. Heavier weights appear only as samples of a family.
- Never an optical size under 72 on an `h1` or `h2`; fat hairlines are this theme's most common failure.
- Never a warm accent, never cool paper: the signal is ink blue, the warmth comes from the oat.
- Never a drawn book, page or device to show text; set the text itself at its size.

### Build hint

```css
h1, h2, h3 { font-family: var(--font-display); font-weight: var(--display-weight); letter-spacing: var(--tracking-display); line-height: 1.02; }
h1, h2 { font-variation-settings: "opsz" var(--display-optical); }
h3 { font-optical-sizing: auto; line-height: 1.15; }
.btn { min-height: 48px; border: var(--rule-hair) solid var(--color-ink); border-radius: var(--radius-card); padding: 0 var(--space-lg); font-weight: 500; }
.btn--primary { background: var(--color-ink); color: var(--color-paper); }
.btn--secondary { background: transparent; color: var(--color-ink); }
.guide { border-top: var(--rule-hair) solid var(--color-guide); }
.rule--double { border: 0; border-top: 3px double var(--color-rule-2); }
input[type="range"] { appearance: none; height: 1px; background: var(--color-rule-2); }
input[type="range"]::-webkit-slider-thumb { appearance: none; width: 16px; height: 16px; background: var(--color-ink); border-radius: 0; }
.photo > img { outline: var(--rule-hair) solid var(--color-rule); outline-offset: -1px; }
a { text-decoration-color: var(--color-accent); text-underline-offset: 0.18em; }
a:hover { text-decoration-thickness: 2px; }
```
