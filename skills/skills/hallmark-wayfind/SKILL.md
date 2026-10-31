---
name: hallmark-wayfind
description: "Wayfind: cool grey paper, blue-black ink, Chivo Mono throughout, square 2px ink borders, ink plates, cobalt for what is live, amber for figures on ink. Fits: transit, metro, rail, station, wayfinding, departures, timetable, live, map, commute, city, platform, signage, logistics, status, operations, schedule, mobility, travel, trip, journey, itinerary, booking, flights, airport"
metadata:
  origin: hallmark
  category: themes
  group: style
  mode: manual
  title: Wayfind
  summary: минимализм, светлый, уверенный акцент
  preview: "#EDF0F4 #DDE2E7 #0A0D13 #2055E1 #F4B522 · Chivo Mono"
---
# Wayfind — a Hallmark style

The designer chose this style for the chat. A style is a material: paper, ink, faces, rules, radius, depth, controls
and voice. It is never a layout. It was written for web pages in CSS; in FigCraft:

- **Tokens become the file's variables.** Look at the file's variables first (`variable.export`). With no colour
  collection for this style, make one named «Wayfind»: the `--color-*` tokens as colour variables without the prefix
  (`paper`, `ink`, `accent`…), radii as numbers; bind fills, strokes and radii to them (`variable.bind`), never paste
  hex. A file that already has its own colour system keeps it: restyle it onto this one only when asked.
- **Faces.** Check each family with `text.fonts {family}`. A missing one: say so in one line and take the nearest
  installed face of the same class (mono); never swap silently. Make text styles for display, body, labels
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

Public signage set as a page: cool grey paper, blue-black ink, every glyph in Chivo Mono (a sober grotesk cut to the fixed cell of a departure board), square 2px ink borders, ink plates that carry a sign, cobalt for what is live and amber for figures. The mono is the board's face and the borders mark the way. It reads in daylight, at a glance, from three metres; it is not a developer tool, not a dark terminal and not a retro departures pastiche.

### Tokens

```css
:root {
  --color-paper: #EDF0F4; --color-paper-2: #DDE2E7; --color-paper-3: #FBFEFF;
  --color-ink: #0A0D13; --color-ink-2: #282B32; --color-muted: #565B64;
  --color-rule: #B9BEC5; --color-ink-rule: #34383F;
  --color-accent: #2055E1; --color-accent-2: #F4B522; --color-accent-ink: #FCFEFF; --color-focus: #2055E1;
  --font-display: "Chivo Mono", ui-monospace, monospace; --font-body: var(--font-display); --font-outlier: var(--font-body);
  --radius-card: 0; --radius-pill: 999px; --rule-hair: 1px; --rule-bar: 2px;
  --shadow-card: 0 24px 40px -24px #01020399;
  --tracking-display: -0.03em; --display-weight: 800;
}
```

Three colourways, set once per page and stated in the stamp (`wayfind: platform`).

| Colourway | Paper, ink, rule |
| --- | --- |
| `platform` (default) | the block above |
| `night` | paper `#080B10`, ink `#EFF2F5`, rule `#2C3038`, cobalt lifts to `#457CFD` |
| `signal` | paper `#2055E1` cobalt, ink white, rule `#87ADFA`; the cobalt button becomes the ink one |

### Type

- **Display:** Chivo Mono 800, `--tracking-display`, line-height 0.98, sentence case. A mono line runs wide, so `h1` caps at 4.75rem and a head stays short enough to read in one look.
- **Body:** Chivo Mono 400, line-height 1.55, `tabular-nums` on everything. Mono is the material here (waive 64): the board's face sets the whole page. Three weights: 400, 500 and 800.
- **Figures:** minutes, platforms and exits in 800, at `--text-display-s` or larger when a figure is the section's reason; amber on ink, ink on paper.
- **Labels, table heads, pills, buttons:** Chivo Mono 500 a step smaller (buttons 800), sentence case, untracked; the signage reads through the mono and the borders, never through capitals.

### Surfaces

- Rules: `--rule-bar` ink borders on every surface (wells, plates, buttons, the underside of a nav, a table's head rule); row dividers `--rule-hair` in `--color-rule`, or `--color-ink-rule` on ink.
- Radius 0 everywhere except pills. Depth is borders; `--shadow-card` only under a surface that floats over another.
- The plate: a square field of ink (or amber under ink text) inside a 2px border, holding one instruction and its figure, the way a sign holds a platform number.
- Bands: `--color-paper-2`, an `--color-ink` band where figures turn amber, or one cobalt field in the `signal` colours; two bands a page at most.
- Photographs: the network at eye level: platforms, tiled walls, a train in, stairs up to daylight; people only from behind and moving. Square, inside the 2px ink border; type never sits on the picture, only on a plate inside the frame. Captions name the station or the line. A phone screen built from the product takes a 9:19.5 frame in that border, never a drawn bezel.
- No texture, no gradient.

### Range

- **A departure board as a Table** on the ink band: destination in 500, the line as a small square in the network's own colour, minutes in 800 amber at title size or larger, a late row as an amber fill under ink text, a 2px paper head rule.
- **A route as Steps:** the way out as three or four plates in a row, each a 2px bordered square holding one instruction (carriage, stairs, exit) and its figure, joined by a 2px ink rule like a corridor sign.
- **Status as Rows:** each line or service a full-width row, its swatch, its name in 800, its ends in 400, its state at the right edge; one cobalt live dot on the row that just changed.
- **A figure as a sign:** one number in 800 at display size inside a bordered plate, its unit beside it, and a station picker of square cells joined edge to edge that changes it.

### Controls

- A cobalt-filled button beside a transparent one with a `--rule-bar` ink border, both square, Chivo Mono 800, sentence case, 48 to 52px.
- A choice set is square cells sharing 2px borders; the chosen cell fills ink with paper text. Links are ink, underlined, cobalt on hover; inputs are square, 2px ink border on `--color-paper-3`.
- Cobalt is for what is live (the current stop, a clock, the primary action); amber colours figures only on ink or as a fill under ink text.

### Motion

Departure-board stiff: `--dur-micro` colour changes in `steps(1)`, rows updating in place, no reveal on scroll. A live dot blinks once when a row updates; it never loops.

### Voice

Signage: the platform, the exit, the minute, the carriage. Imperative and short; a head reads in one look.

### Do-nots

- Never a proportional face anywhere, not even for prose.
- Never amber as a text colour on the paper; it belongs on ink or under ink text.
- Never a third bright colour, except a network's own line colours as small squares beside their names.
- Never rounded cards or soft shadows on cards; Wayfind is bordered.
- Never a drawn platform, train or carriage row standing in for the place; photograph the station, build the screen.

### Build hint

```css
body { font-variant-numeric: tabular-nums; }
h1, h2, h3 { font-weight: 800; line-height: 0.98; }
h1 { font-size: min(var(--text-display), 4.75rem); }
small, th, figcaption { font-weight: 500; color: var(--color-muted); }
.btn { display: inline-flex; align-items: center; gap: var(--space-xs); padding: var(--space-md) var(--space-lg); border: var(--rule-bar) solid currentColor; font: 800 var(--text-sm)/1 var(--font-body); color: inherit; transition: background-color var(--dur-micro) steps(1); }
.btn--primary { background: var(--color-accent); border-color: var(--color-accent); color: var(--color-accent-ink); }
.plate { border: var(--rule-bar) solid var(--color-ink); background: var(--color-ink); color: var(--color-paper); }
.plate .figure { font-weight: 800; color: var(--color-accent-2); }
.band--ink { background: var(--color-ink); color: var(--color-paper); }
th { border-bottom: var(--rule-bar) solid currentColor; } td { border-bottom: var(--rule-hair) solid var(--color-rule); }
::selection { background: var(--color-accent-2); color: var(--color-ink); }
```
