---
name: hallmark-coral
description: "Coral: warm grey paper and a felt desk, cotton stationery lit from the left, General Sans throughout with Geist Mono figures, letterpress card controls, coral pressed into the stock for the one settled state. Fits: saas, platform, billing, payments, invoicing, dashboard, b2b, startup, product, pricing, analytics, fintech, workflow, team, onboarding, trust, warm, human, calm"
metadata:
  origin: hallmark
  category: themes
  group: style
  mode: manual
  title: Coral
  summary: минимализм, светлый, сдержанный акцент
  preview: "#F8F4F1 #F1ECE8 #1D1614 #EF8B7B #BB3D31 · General Sans"
---
# Coral — a Hallmark style

The designer chose this style for the chat. A style is a material: paper, ink, faces, rules, radius, depth, controls
and voice. It is never a layout. It was written for web pages in CSS; in FigCraft:

- **Tokens become the file's variables.** Look at the file's variables first (`variable.export`). With no colour
  collection for this style, make one named «Coral»: the `--color-*` tokens as colour variables without the prefix
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

A warm, plain product voice made physical: fine stationery on a felt desk, seen from above in one daylight from the left. Records are cotton sheets, envelopes and index cards with real edges; controls are letterpress cards; one coral ink is pressed in where something is settled. General Sans throughout. Not a cream editorial page, not a skeuomorphic toy, not a blue SaaS template.

### Tokens

```css
:root {
  --color-paper: #F8F4F1; --color-paper-2: #F1ECE8; --color-paper-3: #E8E1DD;
  --color-ink: #1D1614; --color-ink-2: #312926; --color-muted: #615955;
  --color-rule: #D9D3CF; --color-rule-2: #C7BFBA;
  --color-accent: #EF8B7B; --color-accent-ink: #1D1614; --color-accent-2: #BB3D31; --color-focus: #BD3A2B;
  --color-cotton: #FDFBF8; --color-desk: #F0EBE7; --color-print: #221B19;
  --color-board: #1F1917; --color-board-type: #F6F3EF; --color-paid: #BA4A34;
  --tex-cotton: url("cotton.svg"); --tex-desk: url("felt.svg");
  --shade: 32% 0.03 50; --lit: 100% 0.005 80; --deep: 7% 0.01 40;
  --font-display: "General Sans", ui-sans-serif, system-ui, sans-serif; --font-body: var(--font-display);
  --font-outlier: "Geist Mono", ui-monospace, monospace;
  --radius-card: 8px; --radius-input: 6px; --radius-pill: 999px; --radius-stock: 8px; --rule-hair: 1px;
  --shadow-card: 0 1px 2px #1A14130D;
  --edge-stock: inset 0 1px 0 oklch(var(--lit) / 0.9), inset 0 -1px 0 oklch(var(--shade) / 0.07), 0 0 0 0.5px oklch(var(--shade) / 0.22), 0 1px 0 oklch(var(--shade) / 0.12);
  --cast-stock: 6px 5px 10px -6px oklch(var(--shade) / 0.3); --cast-stock-lift: 12px 10px 18px -8px oklch(var(--shade) / 0.3);
  --press-groove: inset 1px 1.5px 2px oklch(var(--shade) / 0.16), inset -1px -1px 0 oklch(var(--lit) / 0.9), 0 0 0 0.5px oklch(var(--shade) / 0.2);
  --tracking-display: -0.03em; --display-weight: 600;
}
```

### Type

- **Display:** General Sans 600, `--tracking-display`, line-height 1.02 to 1.08, sentence case, roman. A lone price sets at two to three times `--text-display`, tracked -0.05em, line-height 0.85, its unit beside it at `--text-title` in 500.
- **Body:** General Sans 400 and 500. On stock, `--color-print`; on board, `--color-board-type`.
- **Labels:** General Sans 500 a step smaller, sentence case, `--color-muted`.
- **Figures in a column:** Geist Mono 400 (General Sans has no tabular figures). A price in a sentence or a head stays General Sans.

### Surfaces

- One light, from the left: each paper object takes a lit edge top and left, a shade edge bottom and right, and a cast falling right (`--edge-stock`, `--cast-stock`).
- The hero ground is a desk: `--color-desk` under a daylight radial from the left and a generated felt texture. Records the product handles are built as stationery on it: invoices, letters and statements on cotton sheets, a window envelope with glassine showing the address, replies as correspondence index cards, a groove pressed into a card. Each is CSS on `--color-cotton`, sized from one unit so it scales whole.
- Texture is generated, never a picture: the build writes `cotton.svg`, a 360px tile of two stitched feTurbulence layers (cloud 0.011, grain 0.92, warm and faint) with short fibre strokes, under a lit-to-shade gradient on every paper object; `felt.svg` the same at 0.018. Sections stay plain.
- The settled state (paid, signed, booked) is pressed into the stock: the word in General Sans 600 in `--color-paid`, through an SVG filter that offsets a shade wall into the letterforms and lets a noise mask leave the ink uneven, tilted a few degrees.
- One `--color-ink` band, the board; stationery on it casts from `--deep`.
- Photographs are rare: work at arm's length in daylight, muted; built stationery answers first.

### Range

- **The job played as paperwork:** the product's task told in its own documents on the desk (a sheet into an envelope, a reply card tucked under, the outcome pressed in), built in the hero and reused below.
- **Records as an index:** replies, bookings or clients as cotton index cards stacked with offset tabs, beside their record on a full sheet.
- **The price on the board:** the lone figure huge in paper beside a ruled list of what it pays for; the action sits on stationery laid on the band (an envelope flap, a card).
- **The other side:** what the recipient sees, built on cotton, a groove control rewriting it live.

### Controls

- Letterpress cards, not pills: 8px radius, 48px tall, cotton stock with `--edge-stock` and `--cast-stock` and the label pressed in (a lit text shadow below it); the primary is ink board with the label pressed the other way. Hover lifts 1px into `--cast-stock-lift`; active presses 1px down.
- A choice of two to four is a groove pressed into cotton (`--press-groove`, 12px radius) with a cotton card riding in it to the chosen stop.
- Inputs 48px, 6px radius, 1px `--color-muted` border, deep coral focus. Status is an ink outline; coral is spent only on the pressed settled state, link underlines and focus.

### Motion

Once, after fonts load and in view: the job plays on the desk in about six seconds, transforms and opacity only, paused off screen, then still. Reduced motion and no script show the finished state.

### Voice

Plain, warm second-person sentences about the work and the money: who, how much, when, what the product did. Never cute.

### Do-nots

- Never cool paper, a blue signal or a second light; every shadow falls right.
- Never a pill button or a flat square button; controls are pressed cards.
- Never a photograph of paper; stationery is built in CSS.
- Never coral as a band, a fill behind text or a head; it is the pressed ink of one settled state.

### Build hint

```css
h1, h2, h3 { font-weight: var(--display-weight); }
.desk { background-color: var(--color-desk); background-image: radial-gradient(90% 120% at 0% 30%, var(--color-cotton), transparent 62%), var(--tex-desk); }
.stock { background-color: var(--color-cotton); background-image: linear-gradient(100deg, var(--color-cotton), transparent 45%), var(--tex-cotton); color: var(--color-print); box-shadow: var(--edge-stock), var(--cast-stock); }
.btn { min-height: 48px; padding: 0 var(--space-lg); border: 0; border-radius: var(--radius-stock); font-weight: 500; transition: transform var(--dur-short) var(--ease-out); }
.btn--card { background-color: var(--color-cotton); background-image: var(--tex-cotton); color: var(--color-print); text-shadow: 0.5px 0.75px 0 var(--color-cotton); box-shadow: var(--edge-stock), var(--cast-stock); }
.btn--ink { background: var(--color-board); color: var(--color-board-type); text-shadow: 0 -0.75px 0 var(--color-ink); box-shadow: var(--cast-stock); }
.btn:hover { transform: translateY(-1px); box-shadow: var(--edge-stock), var(--cast-stock-lift); } .btn:active { transform: translateY(1px); }
.fig { font-family: var(--font-outlier); font-variant-numeric: tabular-nums; }
a:hover { text-decoration-color: var(--color-accent-2); }
```
