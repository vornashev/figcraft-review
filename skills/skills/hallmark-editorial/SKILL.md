---
name: hallmark-editorial
description: "Editorial: warm white uncoated stock, printed black ink with a cool tilt, Bricolage Grotesque condensed at 800 over Source Serif 4, square corners, a heavy ink rule over 1px hairlines, one printer's green. Fits: magazine, editorial, feature, culture, fashion, design annual, interview, longform, publication, issue, contemporary, art direction, profile, lookbook, brand story, journal, considered, travel, city guide, guide"
metadata:
  origin: hallmark
  category: themes
  group: style
  mode: manual
  title: Editorial
  summary: редакционный, светлый, сдержанный акцент
  preview: "#F7F5F0 #EEEBE4 #0C0D12 #007439 · Bricolage Grotesque"
---
# Editorial — a Hallmark style

The designer chose this style for the chat. A style is a material: paper, ink, faces, rules, radius, depth, controls
and voice. It is never a layout. It was written for web pages in CSS; in FigCraft:

- **Tokens become the file's variables.** Look at the file's variables first (`variable.export`). With no colour
  collection for this style, make one named «Editorial»: the `--color-*` tokens as colour variables without the prefix
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

A contemporary magazine voice: warm white uncoated stock, a printed black with a faint cool tilt that runs through the reading text too, Bricolage Grotesque at 800 squeezed to width 75 for every head, Source Serif 4 for reading and the standfirst, square corners, a heavy ink rule over 1px hairlines, one printer's green. The condensed head, the serif standfirst and the rule carry it, not ornament. It is not a serif literary journal, not cream with terracotta, and not a gallery of captioned photographs.

### Tokens

```css
:root {
  --color-paper: #F7F5F0; --color-paper-2: #EEEBE4; --color-paper-3: #E5E1D9;
  --color-ink: #0C0D12; --color-ink-2: #2A2B31; --color-muted: #615D57;
  --color-rule: #D0CDC7; --color-rule-2: #8F8C85;
  --color-accent: #007439; --color-accent-ink: #FAF8F5; --color-focus: #067E3F;
  --font-display: "Bricolage Grotesque", ui-sans-serif, sans-serif; --font-body: "Source Serif 4", ui-serif, Georgia, serif;
  --radius-card: 0; --radius-pill: 0; --rule-hair: 1px; --rule-heavy: 4px; --shadow-card: none;
  --tracking-display: -0.012em; --display-weight: 800;
}
```

### Type

- **Display:** Bricolage Grotesque 800 with `"wdth" 75, "opsz" 96`, `--tracking-display`, sentence case, roman. Line-height 0.92 at hero size, 1.0 for heads. Condensed, it takes one step up: a section head may run at `--text-display-s`, a lone hero word at twice `--text-display`. One weight and one colour per head.
- **Body:** Source Serif 4 400 and its italic at 18px, optical size automatic, line-height 1.55, oldstyle figures in running text, in `--color-ink-2`. The standfirst (the line under a head, or a statement) is the same face at `--text-lead` up to `--text-display-s`, ink, line-height 1.2 at the large end. A quotation takes the italic; italic never enters a head.
- **Labels, captions, nav links, controls, table heads, bylines:** Bricolage Grotesque 500 at `"opsz" 12`, full width, a step smaller, sentence case, untracked; captions in `--color-muted`. Figures set in the display face take lining tabular numerals. No mono on the page.

### Surfaces

- Two rule weights: a `--rule-heavy` ink rule opens a section or a table, the head flush under it; 1px `--color-rule` hairlines part rows, columns and figures, `--color-rule-2` under a table head. Nothing is boxed, nothing casts a shadow.
- Radius 0 on everything: controls, tags, inputs, wells and photographs are sharp rectangles.
- Depth is a paper step: a well is `--color-paper-2` under a `--color-rule-2` hairline, never a raised card.
- Bands: a `--color-paper-2` well and one `--color-ink` band with `--color-paper` type, two a page at most; never a green band.
- Photographs: seen close: hands at work, an object on a bench, a room in daylight, printed pages. Soft window light, people from behind, never a face to the lens; a little quieter than life, square, an inset ink outline at 8%, full-bleed or cut to a column edge. A head crosses a photograph only as a cover line, once a page, over an ink scrim. Two or three big pictures below the first screen; the material carries the rest.
- No texture, no grain, no mesh.

### Range

- **Contents as rows:** under the heavy rule, three to six hairline rows, a title in the condensed head at about 40px on the left, its standfirst in the serif on the right, a page or date in the display face at the far edge.
- **The standfirst as a statement:** one or two sentences in Source Serif at `--text-display-s`, ink across ten columns under the heavy rule; the serif at size is as much this theme as the head.
- **Figures reversed out:** on the ink band, three or four of the prompt's numbers in the condensed head at `--text-display`, parted by hairlines, labels beneath.
- **The order as a spec sheet:** a form on the paper-2 well, its facts in a ruled table beside the fields, the total in the display face, updated as the quantity changes.

### Controls

- An ink-filled square block (`--color-paper` on `--color-ink`) beside a 1px ink-outlined block, both in the label face, 48px tall; a tag may be the one filled green rectangle.
- Links carry a hairline underline that turns green on hover; inputs and selects are square, 52px tall, with a 1px `--color-rule-2` border that turns ink on focus.
- Green stays under 5% of a screen: a hover, one tag, the focus ring.

### Motion

State only: a green underline grows under a link over `--dur-short` on `--ease-out`, a block darkens one step, a total changes in place. No reveal, nothing on scroll.

### Voice

Contemporary, lightly literary, exact. Name the issue, the page count, the date; a head reads like a cover line, a standfirst says the argument in one breath.

### Do-nots

- Never a serif head; Source Serif 4 sets reading text, standfirsts and quotations, never an `h1` to `h3`.
- Never Bricolage at its default width; without `"wdth" 75` the head loses the magazine proportion.
- Never a rounded corner, a pill, a shadow, or a rule in green.
- Never two picture sections in a row; follow each with rows, a standfirst or the figures.
- Never an all-caps shout; sentence case, tight, magazine-modern.

### Build hint

```css
body { color: var(--color-ink-2); font-optical-sizing: auto; font-variant-numeric: oldstyle-nums; }
h1, h2, h3 { font-weight: var(--display-weight); font-variation-settings: "wdth" 75, "opsz" 96; color: var(--color-ink); font-variant-numeric: lining-nums tabular-nums; }
small, figcaption, th, nav, label, .btn, .tag { font-family: var(--font-display); font-weight: 500; font-variation-settings: "opsz" 12; }
.standfirst { font: 400 var(--text-display-s)/1.2 var(--font-body); color: var(--color-ink); }
.opens { border-top: var(--rule-heavy) solid var(--color-ink); padding-top: var(--space-lg); }
.btn { border: var(--rule-hair) solid var(--color-ink); border-radius: 0; min-height: 48px; padding: 0 var(--space-lg); }
.btn--primary { background: var(--color-ink); color: var(--color-paper); }
.btn--secondary { background: none; color: var(--color-ink); }
.tag { background: var(--color-accent); color: var(--color-accent-ink); padding: var(--space-3xs) var(--space-xs); }
.well { background: var(--color-paper-2); border-top: var(--rule-hair) solid var(--color-rule-2); }
.photo > img { outline: 1px solid color-mix(in oklab, var(--color-ink) 8%, transparent); outline-offset: -1px; }
a { text-decoration-color: var(--color-rule-2); text-underline-offset: 0.2em; } a:hover { text-decoration-color: var(--color-accent); }
::selection { background: color-mix(in oklab, var(--color-accent) 22%, transparent); }
```
