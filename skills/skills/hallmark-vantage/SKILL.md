---
name: hallmark-vantage
description: "Vantage: blue-black ground, a live point cloud of the real thing as the hero's light, a sweep that lights it, pale steel ink, Geologica with sharpened corners at a light weight, hairline frames with corner ticks, one lime signal for what was found. Fits: lidar, scan, survey, mapping, 3d, spatial, point cloud, robotics, autonomy, drone, construction, digital twin, geospatial, measurement, sensor, inspection, engineering, heritage, digitisation, infrastructure, reality capture, terrain"
metadata:
  origin: hallmark
  category: themes
  group: style
  mode: manual
  title: Vantage
  summary: минимализм, тёмный, сдержанный акцент
  preview: "#04090C #091015 #EBEFF2 #BCF053 · Geologica"
---
# Vantage — a Hallmark style

The designer chose this style for the chat. A style is a material: paper, ink, faces, rules, radius, depth, controls
and voice. It is never a layout. It was written for web pages in CSS; in FigCraft:

- **Tokens become the file's variables.** Look at the file's variables first (`variable.export`). With no colour
  collection for this style, make one named «Vantage»: the `--color-*` tokens as colour variables without the prefix
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

Reality capture at night: the thing itself, a site, a ridge, an object, rendered as tens of thousands of measured points on a blue-black ground, turning slowly while a sweep passes through and lights them. Around it the page is instrument-quiet: Geologica with its corners sharpened, steel-grey ink, hairline frames that only mark their corners, figures with their units. One lime signal means found, measured, live. It is not a particle network, not a neon cyber page, not a dashboard of glowing tiles.

### Tokens

```css
:root {
  --color-paper: #04090C; --color-paper-2: #091015; --color-paper-3: #111A1F;
  --color-ink: #EBEFF2; --color-ink-2: #BDC6CA; --color-muted: #89949A;
  --color-rule: #20282C; --color-rule-2: #30393F;
  --color-accent: #BCF053; --color-accent-hi: #CCFC76; --color-accent-ink: #0F1703; --color-focus: #BCF053;
  --point-lo: #3B5062; --point-mid: #86A3B3; --point-hi: #E4F6FA;
  --color-slot: #111A1F;
  --font-display: "Geologica", ui-sans-serif, system-ui, sans-serif; --font-body: "Geologica", ui-sans-serif, system-ui, sans-serif;
  --radius-card: 4px; --radius-pill: 999px; --rule-hair: 1px; --tick: 10px;
  --shadow-card: none;
  --tracking-display: -0.035em; --display-weight: 300;
}
```

Two dials, stated in the stamp (`vantage: terrain/steel`). Two Vantage pages in one run differ on both.

| Dial | Options |
| --- | --- |
| **Subject** (what the cloud is) | `terrain` (default): ground, structures and canopy from above at an oblique angle. `object`: one thing scanned whole, turning on its axis. `interior`: a room or tunnel seen from inside |
| **Colourway** | `steel` (default) as above. `sodium`: ground `#0B0604`, points from `#5E402F` to `#F9EDD9`, ink warm, the lime kept as the signal |

### Type

- **Display:** Geologica 300 with `"SHRP" 100` (its sharpened corners), `--tracking-display`, line-height 1.0, sentence case; 400 for small titles. Heads are short and sit on plain ground, never on dense points.
- **Body:** Geologica 300 at 17px with `"SHRP" 0`, line-height 1.6, `--color-ink-2`.
- **Measurements:** Geologica 400, `tabular-nums`, the unit a step smaller in `--color-muted` after a thin space; a figure at statement size takes 200. Labels Geologica 400 a step smaller, sentence case. Never mono, never tracked capitals.

### Surfaces

- **The cloud:** one generated canvas or WebGL scene of points only, no lines between them, no glow: size by distance, colour by height from `--point-lo` to `--point-hi`, a soft depth fade. A sweep plane passes every few seconds and lifts the points it touches toward white; anything found is lime. It fills the hero beside or behind the head and fades to paper at the edges.
- **Frames:** hairline `--color-rule` boxes are drawn only at their corners (`--tick` long ticks), around a measured thing or a panel; full hairline boxes only for inputs. Radius `--radius-card` at most.
- **Callouts:** a measured point carries a leader (a hairline with a 3px dot at the point) to its figure and unit; two at most on a screen.
- **Bands:** paper, and paper-2 for one quiet band; no lit or tinted bands. Flat depth, no shadows.
- **Photographs:** the real site or object in flat daylight, muted, `--radius-card`; never a sci-fi render.

### Range

- **A section cut:** one thin slice through the cloud set across the full width as a profile of points, with two or three heights called out by leader and figure.
- **A scan log as a table:** rows of captures with their date, area, points and accuracy in tabular figures, the live row marked by a lime dot.
- **Layers as working toggles:** ground, structures, canopy and found items as a ruled list of switches that really recolour or hide the cloud beside them.
- **A figure measured:** one number at statement size inside corner ticks, its tolerance under it in muted.

### Controls

- Primary pill: `--color-accent` under `--color-accent-ink`, 48px, Geologica 400; hover `--color-accent-hi`. Secondary: a hairline pill in `--color-rule-2`, ink text.
- Inputs: `--color-paper-2` wells with a hairline frame, lime caret and focus. Switches lime when on.
- Lime marks only what is found, live or primary; never a heading, never a fill larger than a pill.

### Motion

The cloud turns slowly (a revolution in two minutes, an object in seventy seconds), the sweep passes every six to eight seconds on an ease-in-out, the pointer tilts the view a few degrees. Panels and rows fade up once. Canvas pauses off screen. Reduced motion: one still frame with the sweep stopped mid-scene.

### Voice

Measured and exact: what was scanned, how big, how accurate, how soon.

### Do-nots

- Never lines joining points, never a glow or bloom, never a grid floor receding to a horizon.
- Never more than one hue on the points besides lime for found.
- Never the cloud under running text or behind a form.
- Never a monospace label; figures are tabular Geologica.

### Build hint

```css
h1, h2, h3 { font-family: var(--font-display); font-weight: var(--display-weight); font-variation-settings: "SHRP" 100; letter-spacing: var(--tracking-display); line-height: 1; }
body { font-weight: 300; font-variation-settings: "SHRP" 0; }
.num { font-variant-numeric: tabular-nums; font-weight: 400; } .num .u { color: var(--color-muted); font-size: 0.75em; }
.ticks { position: relative; } .ticks::before, .ticks::after { content: ""; position: absolute; inset: 0; pointer-events: none; border: var(--rule-hair) solid var(--color-rule-2); -webkit-mask: conic-gradient(at var(--tick) var(--tick), transparent 75%, var(--color-ink) 0) 0 0 / calc(100% - var(--tick)) calc(100% - var(--tick)); mask: conic-gradient(at var(--tick) var(--tick), transparent 75%, var(--color-ink) 0) 0 0 / calc(100% - var(--tick)) calc(100% - var(--tick)); }
.btn { min-height: 48px; padding: 0 var(--space-lg); border: 0; border-radius: var(--radius-pill); background: var(--color-accent); color: var(--color-accent-ink); font: 400 var(--text-md)/1 var(--font-body); transition: background var(--dur-short) var(--ease-out); }
.btn:hover { background: var(--color-accent-hi); }
.btn--line { background: transparent; color: var(--color-ink); box-shadow: inset 0 0 0 var(--rule-hair) var(--color-rule-2); }
```
