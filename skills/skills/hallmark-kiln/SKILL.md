---
name: hallmark-kiln
description: "Kiln: near-black ground, cream ink, Boska over Geist, smoked wells, photographs lit by the work, a heat ramp that marks temperature, one ember signal. Fits: kiln, ceramics, pottery, firing, glaze, heat, temperature, ceramics studio, craft, sensor, monitor, hardware, iot, warmth, dark, glow, schedule, workshop"
metadata:
  origin: hallmark
  category: themes
  group: style
  mode: manual
  title: Kiln
  summary: атмосферный, тёмный, полная палитра
  preview: "#0B0605 #170E0B #F2EADD #FE6A00 · Boska"
---
# Kiln — a Hallmark style

The designer chose this style for the chat. A style is a material: paper, ink, faces, rules, radius, depth, controls
and voice. It is never a layout. It was written for web pages in CSS; in FigCraft:

- **Tokens become the file's variables.** Look at the file's variables first (`variable.export`). With no colour
  collection for this style, make one named «Kiln»: the `--color-*` tokens as colour variables without the prefix
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

A dark workshop with the kiln door open a crack: a near-black ground, cream ink, Boska's cut high-contrast serif over a plain Geist, and heat only where something is hot. The photographs carry the fire; a ramp from ash through oxblood, ember and amber to white heat colours a temperature as it climbs. Warm in one place, cold everywhere else. It is not a dark luxury page with an orange button, and not a glowing gradient poster.

### Tokens

```css
:root {
  --color-paper: #0B0605; --color-paper-2: #170E0B; --color-paper-3: #221814;
  --color-ink: #F2EADD; --color-ink-2: #D5C8B9; --color-muted: #B3A192;
  --color-rule: #F5F1EA1F;
  --color-accent: #FE6A00; --color-accent-ink: #100704; --color-focus: #FF8A00;
  --heat-0: #090503; --heat-1: #34080B; --heat-2: #8A050D; --heat-3: #E13B00;
  --heat-4: #FF8A00; --heat-5: #FFCF66; --heat-6: #FFF9DB;
  --font-display: "Boska", "Iowan Old Style", Georgia, serif; --font-body: "Geist", ui-sans-serif, system-ui, sans-serif;
  --font-outlier: "Geist Mono", ui-monospace, monospace;
  --radius-card: 28px; --radius-well: 16px; --radius-pill: 999px; --rule-hair: 1px;
  --shadow-card: 0 50px 90px -30px #03010180;
  --tracking-display: -0.02em; --display-weight: 500;
}
```

Three colourways, stated in the stamp (`kiln: ember`).

| Colourway | Ground, ink, accent |
| --- | --- |
| `ember` (default) | the block above |
| `bisque` | ground `#F8F3E9`, ink `#1E130F`, accent `#B14F00` with the ground as its text; the ramp starts at `#ECDBC5`; wells turn bone |
| `reduction` | ground `#2F0A0B`, ink `#F5EEE0`, accent `#FFB876`; the ramp begins at the ground |

### Type

- **Display:** Boska 500, `--tracking-display`, line-height 1.04, sentence case, roman, one colour per head; a statement set in it may run to `--text-display` at line-height 1.0.
- **Figures:** a temperature, a firing time or the price that carries the story is Boska 500, lining and tabular, at -0.03em, its unit (°C, h, £) in the same face; a lone figure may run twice the hero head.
- **Body:** Geist 400 and 500 at 16 to 18px, line-height 1.55.
- **Labels, captions, axis ticks, table heads:** Geist 500 a step smaller, sentence case, untracked, in `--color-muted`. Geist Mono only inside code.

### Surfaces

- 1px `--color-rule` between rows, on a well's edge and on a chart's grid; no rule brighter than that.
- Radius 28px on photographs and built screens, scaled down with the viewport; `--radius-well` on wells and inputs; pills on controls.
- Wells are smoked: `--color-paper-2` a clear step above the ground, a 1px rule edge, no shadow, never blurred, never nested. `--shadow-card`, a deep low drop, only under a built screen standing on the ground or a photograph, never with a ring.
- Heat marks temperature and nothing else: the ramp colours a firing curve in steps, each band of degrees its own colour, oxblood low to white heat at the peak, and a range track (three stops). It never fills a box, a band, a slot or the ground, and no text sits on it.
- Bands: a `--color-paper-2` band, two a page at most.
- Photographs: the work, close and in low light: a kiln at temperature, a loaded kiln, glaze, pots on a shelf, hands in clay, lit by the kiln, a bench lamp or a window, shadows falling into the ground. A 28px frame with a 1px inset ring of cream at 8%; type on one sits only on its dark side, over a paper scrim at 40 to 65%.

### Range

- A firing schedule as rows: each segment's rate and target in Boska figures, keyed by a short bar of the ramp step its target reaches.
- A reading or a warning set as a statement: Boska at `--text-display` across ten columns, cream on the ground, the hour and the kiln beside it in Geist; nothing else on the screen.
- A log as a full-width table: date, firing and cone in Geist, the peak in Boska keyed to its ramp step, a sparkline of the whole curve per row in `--color-ink-2`.
- A price or a temperature as one figure on a smoked band, the action beside it.

### Controls

- The pair: an ember pill (`--color-accent` with `--color-accent-ink` text, Geist 500), 50px tall, beside a ghost pill with a 1px inset `--color-rule` ring and cream text.
- Inputs are smoked wells at 16px radius; a range input runs a 2px track filled along the ramp under a 28px ember thumb.
- Ember is only ever a fill: the primary, a thumb, the live point on a curve, the focus ring in `--color-focus`. Every letter stays cream.

### Motion

Slow and thermal: colour changes run `--dur-long` on `--ease-out`, controls answer over `--dur-short`. Nothing pulses, flickers or glows on hover.

### Voice

Calm and physical, in a potter's words: the cone, the degrees, the hour, the load. Name the firing, never the feeling.

### Do-nots

- Never the ramp as a fill: no heat gradient behind text, on the ground, in a slot or across a band.
- Never orange type; the ember is a fill, and every letter stays cream.
- Never a brown or warm-lit ground; it stays near-black so the heat has somewhere to rise from.
- Never a bright, flat-lit photograph or a pot on white seamless.
- Never a third hue beside the ramp.
- Never a photograph on every screen: the fire lives in the curve and the figures too.

### Build hint

```css
h1, h2, h3 { font-weight: var(--display-weight); line-height: 1.04; }
.btn { display: inline-flex; align-items: center; min-height: 50px; padding: 0 var(--space-lg); border-radius: var(--radius-pill); font-weight: 500; transition: background-color var(--dur-short) var(--ease-out); }
.btn--primary { background: var(--color-accent); color: var(--color-accent-ink); }
.btn--ghost { background: transparent; color: var(--color-ink); box-shadow: inset 0 0 0 var(--rule-hair) var(--color-rule); }
.well { background: var(--color-paper-2); border: var(--rule-hair) solid var(--color-rule); border-radius: var(--radius-well); }
.figure { font-family: var(--font-display); font-weight: var(--display-weight); letter-spacing: -0.03em; font-variant-numeric: lining-nums tabular-nums; }
.photo { border-radius: min(2vw, var(--radius-card)); outline: var(--rule-hair) solid color-mix(in oklab, var(--color-ink) 8%, transparent); outline-offset: -1px; }
.scrim { background: linear-gradient(to top, color-mix(in oklab, var(--color-paper) 65%, transparent), transparent 55%); }
.range-track { background: linear-gradient(to right, var(--heat-2), var(--heat-4), var(--heat-6)); }
::selection { background: color-mix(in oklab, var(--color-accent) 35%, transparent); }
```
