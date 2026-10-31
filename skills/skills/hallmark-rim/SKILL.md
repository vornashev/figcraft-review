---
name: hallmark-rim
description: "Rim: warm black paper, warm off-white ink, Switzer 500 with Geist Mono for every measurement, square hairline surfaces, the earth photographed straight down, an orange signal and a sky-blue second. Fits: space, satellite, earth observation, orbit, imagery, ground station, telemetry, hardware, schedule, utc, infrastructure, mission, sensor, monitoring, instrument, night, dark, measured"
metadata:
  origin: hallmark
  category: themes
  group: style
  mode: manual
  title: Rim
  summary: минимализм, тёмный, уверенный акцент
  preview: "#030201 #080604 #EFEBE4 #F97C3D #6DB0F4 · Switzer"
---
# Rim — a Hallmark style

The designer chose this style for the chat. A style is a material: paper, ink, faces, rules, radius, depth, controls
and voice. It is never a layout. It was written for web pages in CSS; in FigCraft:

- **Tokens become the file's variables.** Look at the file's variables first (`variable.export`). With no colour
  collection for this style, make one named «Rim»: the `--color-*` tokens as colour variables without the prefix
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

## Genre: modern-minimal

The polished product page: SaaS, enterprise, API, platform, developer tool, infra, B2B, dashboards, billing. Minimalism with conviction, not the absence of choice. Also picked when the user names a brand colour and the rest of the prompt is restrained. The deal leans toward this genre's themes.

## Voice

- **Accent:** ink, or one hue on focus rings and one control; colour floods only under a declared posture.
- **Layout:** two-column heroes (the title and its line beside a big slot), wide product visuals, thin visible borders rather than hairlines.
- **Motion:** minimal; reveals off; the page is composed.
- **Copy:** declarative, specific, technical. "Built for X" only when X is concrete.

## Allowed here

Pill controls, filled and outlined, with an ink-filled primary beside an outlined secondary; pure white paper (gate 7b is loosened) and zero-chroma neutrals (gate 22 is loosened); a refined surface with a very subtle border and an 8px radius; large tight-set display.

## Refused here

An italic serif body; hairline-everything; asymmetric prose columns; drop caps, fleurons, ornament; overshoot easing; gradient text; glass; a code or terminal register as decoration when the product is not a developer tool; a monospace label voice (64).

## Chrome that fits

A dense balanced bar, a floating pill, a mega-menu, a visible search pill, or vast space between a wordmark and one action. Broadsheet furniture and marquee footers fight the register. Affinities, not assignments.


## The theme

An instrument at night: warm black paper, warm off-white ink, Switzer at a medium weight for every head, Geist Mono for every number that measures something, square surfaces parted by hairlines, an orange signal and a sky-blue second, and the earth shown the way an instrument sees it, from straight above. It reads as exact because every edge is hard and every time carries its zone. It is not a glowing sci-fi page of starfields and halos, and not a neon dashboard.

### Tokens

```css
:root {
  --color-paper: #030201; --color-paper-2: #080604; --color-paper-3: #010100;
  --color-ink: #EFEBE4; --color-ink-2: #CECAC3; --color-muted: #9C9890; --color-muted-2: #66635D;
  --color-rule: #24211C; --color-rule-2: #0F0D09;
  --color-accent: #F97C3D; --color-accent-ink: #070201; --color-accent-2: #6DB0F4; --color-focus: #FF9661;
  --font-display: "Switzer", ui-sans-serif, system-ui, sans-serif; --font-body: var(--font-display);
  --font-outlier: "Geist Mono", ui-monospace, monospace;
  --radius-card: 0; --radius-pill: 0; --rule-hair: 1px; --shadow-card: none;
  --tracking-display: -0.04em; --display-weight: 500;
}
```

Two colourways, both dark, stated in the stamp: `rim: night` (the block above) or `rim: station` (navy `#06122C`, rules `#223251`, the signals swapped to ice `#72DEE4` and amber `#F49752`).

### Type

- **Display:** Switzer 500, `--tracking-display` on the hero head and -0.03em on section heads, line-height 1.02, sentence case, roman. Medium, never bold; one colour per head.
- **Body:** Switzer 400 at 16 to 17px, line-height 1.55, in `--color-ink-2`; labels, captions and table heads are 500 a step smaller in `--color-muted`, sentence case, untracked, never mono.
- **Measurements (mono as material):** Geist Mono 400, tabular, for every time, coordinate, area, price and duration. A time always carries its zone, UTC by default. A measurement that is the point sets at `--text-display-s` to `--text-display` at -0.03em, its unit or zone at half the size in `--color-muted`. Mono never sets a head, a label or a paragraph.

### Surfaces

- Hairlines do the dividing: 1px `--color-rule` above every section head, around wells and under a table's head; rows on `--color-rule-2`.
- Zero radius on everything; nothing on the page is round. Depth by lightness only: `--color-paper-2` lifts a well, `--color-paper-3` sinks one. No shadow, glass, blur or halo.
- A well or a photograph may drop its border for two 12px corner ticks, 1px L shapes in `--color-muted` at opposite corners, set just outside the frame.
- Bands: `--color-paper-2` or `--color-paper-3`, edged by hairlines; two a page at most, never a light band.
- Photographs: the earth straight down at the scale a capture delivers: a field, a coastline, roofs, a river mouth, sharp edge to edge, with no horizon, no sky and no planet. Square, a 1px inset ring of ink at 8%. Its measurements (the site, the pass, the delivery) ride on a strip of `--color-paper` at 78% along its foot, in Geist Mono with the zone.

### Range

- **Measurements as figures:** two to four real quantities in Geist Mono at display size across the twelve columns, parted by vertical hairlines, the unit half size in muted: a range, a window, a price.
- **A diagram of real time:** a horizontal UTC axis in hairlines with ticks, the window as a 10px sky-blue band and each event a 1px pin in its signal with its time in mono beside it; a chart of the system, never decoration.
- **The product built:** the order or the queue on a `--color-paper-2` well with corner ticks, fields in mono, the chosen row on `--color-paper-3` with an orange square.
- **Ruled rows and a form-first close:** hairline rows with a Switzer title on the left and the line on the right; a form on paper-2 whose values type in mono.

### Controls

- The pair: a square orange-filled primary with `--color-accent-ink` text beside a square secondary outlined in 1px `--color-rule`, both Switzer 500.
- Links are ink, underlined on hover; inputs square on `--color-paper` with a 1px `--color-muted` border, a value that measures typed in Geist Mono.
- Orange marks the action and the current state, sky-blue the second state or a window; nothing else is coloured.

### Motion

Steady and exact: a state changes over `--dur-short` on `--ease-out`; a live time ticks once a minute. Nothing pulses, loops or reveals.

### Voice

Measured and exact: the site, the pass, the time in UTC, the area in square kilometres. No wonder, no frontier.

### Do-nots

- Never anything round: no pill, no avatar circle, no rounded button or frame.
- Never a bare time; `09:30` without a zone is the theme lying.
- Never bold display; Switzer 500 is the ceiling and the black does the weight.
- Never the planet from space, a starfield, a glow or an orbit traced round a globe.

### Build hint

```css
h1, h2, h3 { font-weight: var(--display-weight); line-height: 1.02; }
h2 { letter-spacing: -0.03em; }
.measure { font-family: var(--font-outlier); font-variant-numeric: tabular-nums; }
.btn { border-radius: 0; padding: var(--space-sm) var(--space-md); border: var(--rule-hair) solid var(--color-rule); background: none; color: var(--color-ink); font-weight: 500; }
.btn--primary { background: var(--color-accent); border-color: var(--color-accent); color: var(--color-accent-ink); }
.well { position: relative; background: var(--color-paper-2); }
.photo { outline: var(--rule-hair) solid color-mix(in oklab, var(--color-ink) 8%, transparent); outline-offset: -1px; }
.ticks::before, .ticks::after { content: ""; position: absolute; width: 12px; height: 12px; border: 0 solid var(--color-muted); pointer-events: none; z-index: var(--z-raised); }
.ticks::before { top: calc(-1 * var(--space-xs)); left: calc(-1 * var(--space-xs)); border-width: 1px 0 0 1px; }
.ticks::after { right: calc(-1 * var(--space-xs)); bottom: calc(-1 * var(--space-xs)); border-width: 0 1px 1px 0; }
::selection { background: color-mix(in oklab, var(--color-accent) 35%, transparent); color: var(--color-ink); }
```
