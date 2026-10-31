---
name: hallmark-darkroom
description: "Darkroom: warm print-black ground, a fine light grain, fibre-white ink, hairline Sofia Sans Extra Condensed capitals over Barlow, zero radius, black-and-white photographs printed deeper than the ground, one amber safelight. Fits: photographer, photography, film, analogue, darkroom, prints, portfolio, exhibition, gallery, edition, commission, cinematographer, negative, archive, monochrome, lab, moody, black and white, night, print shop, travel, places, landscape, portrait, photo studio"
metadata:
  origin: hallmark
  category: themes
  group: style
  mode: manual
  title: Darkroom
  summary: атмосферный, тёмный, сдержанный акцент
  preview: "#090604 #100C0A #E9E4DC #EC8D38 · Sofia Sans Extra Condensed"
---
# Darkroom — a Hallmark style

The designer chose this style for the chat. A style is a material: paper, ink, faces, rules, radius, depth, controls
and voice. It is never a layout. It was written for web pages in CSS; in FigCraft:

- **Tokens become the file's variables.** Look at the file's variables first (`variable.export`). With no colour
  collection for this style, make one named «Darkroom»: the `--color-*` tokens as colour variables without the prefix
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

## Genre: atmospheric

The AI-creative and after-dark product page: generative music, video, image, voice, model playgrounds, anything the prompt calls moody, cinematic or nocturnal. A canvas first, then a tool. The deal leans toward this genre's themes, light-paper exceptions included.

## Voice

- **Accent:** one hue, used in the canvas treatment, on focus rings and on small tags; never on display text unless the theme's type names an accented word (Lumen).
- **Layout:** a centred hero is the normal answer when the type is the visual (a Poster or Banner posture); with a visual, it stands beside the text (44c). The canvas is the design and the type sits on it.
- **Motion:** fade only; the atmosphere does the work.
- **Copy:** direct, slightly poetic, specific: *Make a house song about quitting your job.*

## Allowed here

At most two fixed radial blooms on the body, each 20 to 30% of the canvas in size, never animated (gate 29 is loosened this far and no further); the nav pill on a backdrop blur over the canvas, the one glass licence; a centred hero (gate 6b loosened); pill controls with an accent fill; elevated cards by lightness step (`--color-paper-2`, `-3`) instead of hairlines; display up to 6rem.

## Refused here

A coloured glow shadow, a radial spotlight behind the hero, or a mesh gradient (the bloom is the one licence); light sections sneaking into a dark build; a third hue; glass panels or cards; gradient text.

## Chrome that fits

A floating pill on a blur backdrop, an edge-aligned bar, a command palette, a statement footer. Dense link furniture fights the register. Affinities, not assignments.


## The theme

A print room with the lights off: a warm black ground a step lighter than a print's own black, so a photograph sits on it as an object; fibre-white ink; hairline extra-condensed capitals over Barlow; one amber safelight. Photographs are black and white, printed deep and large, and the type carries the rest. It is not a film-strip costume, a moody gradient, flat screen black or a white-matted gallery.

### Tokens

```css
:root {
  --color-paper: #090604; --color-paper-2: #100C0A; --color-paper-3: #1B1613;
  --color-ink: #E9E4DC; --color-ink-2: #C2BDB5; --color-muted: #918B85;
  --color-rule: #2F2A27;
  --color-accent: #EC8D38; --color-accent-deep: #934E1E; --color-accent-ink: #090604; --color-focus: #EC8D38;
  --font-display: "Sofia Sans Extra Condensed", ui-sans-serif, sans-serif; --font-body: "Barlow", ui-sans-serif, sans-serif;
  --font-outlier: var(--font-body);
  --radius-card: 0; --radius-pill: 0; --rule-hair: 1px; --shadow-card: none;
  --tracking-display: -0.005em; --display-weight: 200; --grain: 0.07;
}
```

Three colourways, stated in the stamp (`darkroom: amber`).

| Colourway | Ground, ink, signal |
| --- | --- |
| **amber** (default) | the tokens above |
| **red** | signal `#E14C33`, deep `#971D08` |
| **fibre paper** | ground `#F2EEE7`, ink `#0B0807`, muted `#5D5753`, signal `#BA0D01`, rule `#C4BCB4`; dark specks at 0.12 |

### Type

- **Display:** Sofia Sans Extra Condensed in capitals, 200 on the hero, section heads and figures, 400 on an item title and a control, line-height 1.0, `--tracking-display`, roman. The hairline at scale is the look: being extra-condensed, every display step may set one step above the shared scale, and the hero head runs to poster size across eight columns.
- **Body:** Barlow 400 for prose at 17px and 1.6, so the reading text holds on the dark; Barlow 300 only at lead size and above.
- **Labels, captions, table heads:** Barlow 400 a step smaller, sentence case, untracked, in `--color-muted`; a plate number and a month are this voice. Figures are tabular. No mono.

### Surfaces

- Depth is lightness, never light: ground 12.5, well 16, surface 20.5. No vignette, no bloom, no shadow; a print's blacks sit below the ground, which is what makes it read as a print.
- Rules: 1px `--color-rule`, run full width between rows of a sheet and as vertical hairlines between figures; radius 0 everywhere.
- Bands: a `--color-paper-2` well, grained, for the sections that carry no picture; two a page at most, never an amber field.
- Photographs: the work. Black and white, printed deep (open highlights, full blacks, the film's grain); a subject at a distance with room around it, or close and flat. Radius 0, no frame, no mat; full-bleed or held to the columns, never thumbnail size, a caption beneath with the plate number. Type crosses a photograph only over its darkest third, on a scrim of the ground at 40 to 70%.
- Texture: the speck grain of `texture.md` § 1 at `--grain`, on a well; never over a photograph.

### Range

- **Figures as an edition:** the prompt's real numbers (plates, prints of each, the run) in the 200 hairline at 12rem and over on a grained well, vertical hairlines between them, each with a muted Barlow line beneath; the size is the drama, the colour stays ink.
- **A collector's sheet:** Rows under full-width hairlines, the label in muted Barlow on the left and the value in display capitals at title size on the right: series, subject, negative, paper, edition, sizes.
- **A process as a contact strip:** Steps across the twelve columns, each stage a hairline numeral at section size over a short line (exposed, developed, printed, editioned), parted by verticals; nothing drawn.
- **A choice set as numerals:** a working picker of plates or sizes in 1px rule cells, each a display numeral at title size, the chosen one lit by the safelight, beside a plain form on the ground.

### Controls

- The pair: a 1px ink-outlined secondary beside an amber-filled primary in `--color-accent-ink`, both display capitals at 400, untracked, radius 0, 48px tall.
- Links are ink, underlined in `--color-rule`; the underline turns amber on hover. Inputs: radius 0, a 1px `--color-muted` border on the ground, a steady outline on focus.
- The safelight is scarce: the one filled control, a selected plate, a caption on hover; `--color-accent-deep` is the quieter fill under ink text.

### Motion

Still as a print. A photograph may rise once from the ground over `--dur-long`, as in the tray, from a visible default; hover on a linked plate turns its number amber. Nothing else moves.

### Voice

Lab notes and a collector's sheet: series, plate, place, month, edition, paper. Exact numbers, short lines, no adjectives about light or soul.

### Do-nots

- Never an amber wash, band, glow or amber head; the safelight lights a control or a number, never a section.
- Never a sprocket hole, a film strip, a grease-pencil ring or a drawn frame.
- Never Sofia Sans Extra Condensed above 400 for a head, and never a figure in anything but the 200.
- Never sepia, duotone or a tint on a picture, and never flat screen black under the prints.

### Build hint

```css
h1, h2, .figure { font-family: var(--font-display); font-weight: 200; text-transform: uppercase; line-height: 1; letter-spacing: var(--tracking-display); }
h3 { font-family: var(--font-display); font-weight: 400; text-transform: uppercase; line-height: 1; }
.btn { min-height: 48px; padding: 0 var(--space-lg); border: var(--rule-hair) solid var(--color-ink); border-radius: 0; background: transparent; color: var(--color-ink); font: 400 var(--text-lg)/1 var(--font-display); text-transform: uppercase; }
.btn--primary { background: var(--color-accent); border-color: var(--color-accent); color: var(--color-accent-ink); }
.well { background: var(--color-paper-2); }
.grained { position: relative; isolation: isolate; }
.grained::after { content: ""; position: absolute; inset: 0; z-index: -1; pointer-events: none; opacity: var(--grain); background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='200'%3E%3Cfilter id='g'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='2' stitchTiles='stitch'/%3E%3CfeColorMatrix values='0 0 0 0 1 0 0 0 0 1 0 0 0 0 1 0 0 0 9 -4'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23g)'/%3E%3C/svg%3E") 0 0 / 200px 200px; }
::selection { background: color-mix(in oklab, var(--color-accent) 35%, transparent); }
```
