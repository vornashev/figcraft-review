---
name: hallmark-dose
description: "Dose: warm morning paper with a fibre grain and window light, translucent tinted plastic, green-black ink, Schibsted Grotesk over Instrument Sans with DM Mono pharmacy labels, moulded controls, one pharmacy green. Fits: health, medication, pharmacy, care, carer, family, reminders, schedule, app, mobile, medicine, patients, clinic, prescription, tracking, calm, trust, routine, elderly, parents"
metadata:
  origin: hallmark
  category: themes
  group: style
  mode: manual
  title: Dose
  summary: минимализм, светлый, уверенный акцент
  preview: "#FAF7EF #E9F8EF #0C1C16 #007948 · Schibsted Grotesk"
---
# Dose — a Hallmark style

The designer chose this style for the chat. A style is a material: paper, ink, faces, rules, radius, depth, controls
and voice. It is never a layout. It was written for web pages in CSS; in FigCraft:

- **Tokens become the file's variables.** Look at the file's variables first (`variable.export`). With no colour
  collection for this style, make one named «Dose»: the `--color-*` tokens as colour variables without the prefix
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

Translucent plastic and daylight: warm morning paper with a fine fibre grain, window light falling across it, bands of soft tinted plastic like a pill organiser, green-black ink, Schibsted Grotesk heads over Instrument Sans, and DM Mono for the time and the dose, set like a pharmacy label. One pharmacy green does every signal. It is trustworthy because it is exact and unhurried, and it lives in a kitchen, not a clinic. It is not a clinical blue portal, not a wellness pastel and not an alarm.

### Tokens

```css
:root {
  --color-paper: #FAF7EF; --color-paper-2: #E9F8EF; --color-paper-3: #D4F0E0;
  --color-ink: #0C1C16; --color-ink-2: #26342F; --color-muted: #54655D;
  --color-rule: #CBD6C9;
  --color-accent: #007948; --color-accent-deep: #005F3A; --color-accent-soft: #A9E8C6; --color-accent-ink: #F8FDFA;
  --color-focus: #006B38;
  --p-mon: #EEC1BF; --p-tue: #F2CFAF; --p-wed: #EEE4B4; --p-thu: #A8E2C2;
  --p-fri: #B1DDE6; --p-sat: #BFCAE9; --p-sun: #DAC1DE;
  --light: #FFFDF1; --glint: #FFFFFF;
  --font-display: "Schibsted Grotesk", ui-sans-serif, sans-serif; --font-body: "Instrument Sans", ui-sans-serif, sans-serif;
  --font-outlier: "DM Mono", ui-monospace, monospace;
  --radius-card: 14px; --radius-input: 10px; --radius-pill: 999px; --rule-hair: 1px;
  --shadow-card: 0 1px 2px #1F332A14, 0 24px 48px -24px #0A553D59;
  --shadow-lift: 0 1px 1px #1F332A1A, 8px 18px 28px -14px #18473552, 18px 40px 60px -30px #0A553D4C;
  --tracking-display: -0.03em; --display-weight: 700;
}
```

Committed: the paper is warm, the green tints and the plastic carry the colour, mint (`--color-accent-soft`) marks what is checked, and the accent proper stays on controls, focus, a stamp and one figure. Grounds, stated in the stamp (`dose: white`): **white** (default, the tokens above), **green** (drenched `#006B40` under white ink, surfaces white inside, mint on the ground), **night** (`#040807` under `#ECF4EF`, plastic at 40% light, mint with dark ink).

### Type

- **Display:** Schibsted Grotesk 700, `--tracking-display`, line-height 1.02, sentence case, lining tabular figures.
- **Body:** Instrument Sans 400 and 500, 16 to 18px, line-height 1.5.
- **Labels, captions, table heads:** Instrument Sans 500 a step smaller, sentence case.
- **Times, doses, pharmacy labels:** DM Mono 400 and 500 (`08:00`, `500 mg`), at text size inside a sentence, at title size where a timetable's first column is the time, and as the whole voice of a pharmacy label; never a tab, a table head or a display figure. Three weights a page: 400, 500, 700.

### Surfaces

- The ground is generated, never a picture: the paper takes a fractal-noise fibre grain (an `feTurbulence` data URI under the paper colour), and the hero takes window light, four blurred panes of `--light` skewed across the paper, drifting over 90 seconds.
- Plastic is the surface: a tint (`--p-*`, never a state) at about 62% alpha, a `--glint` line along the top edge, a deeper inner shade at the foot, and the coloured light it lets through pooled and blurred on the paper below. It makes bands, trays and compartments; CSS 3D may turn a set of them three-quarter on the paper.
- A label is paper on plastic: grained white, 10px radius, a tear-off stub on a dashed rule, DM Mono throughout, a confirmation as a double-ringed green stamp rotated 2 degrees naming the time and who; missed or due is the same in grey.
- Radii read as an app: 10px controls, 14px surfaces, 999 on tags, a phone screen at about 28px. White surfaces lift on `--shadow-lift`; one green-black ink band may carry a statement.
- Photographs: the home where a dose is given, hands and rooms in soft daylight, never a face to camera or a clinic; 14px radius, captions beneath.

### Range

- **A sequence as plastic bands:** each stage a full-width band in its own tint, the number in Schibsted at display size, two phone screens of the product on it, the minute each happened in DM Mono beside its line.
- **A record as labels:** the photograph beside two pharmacy labels, one stamped given in green, one missed in grey, each stating the dose, time and person.
- **Statement on the ink band:** one plain sentence in Schibsted 700 at `--text-display`, one line in mint beneath it.
- **A first step in a tray:** the form on a sunken plastic tray, choices as plastic keys, the product's screen beside it answering live.

### Controls

- Moulded plastic: a 52px control at 10px with a 1px rim, a 3px rim below, a bevel of `--glint` on top and a soft cast shadow; it sinks 3px on press. The primary is green plastic, the secondary clear.
- Choices are plastic keys, mint when checked. Links underline in green on hover. Inputs: 52px at 10px with a 1px `--color-muted` border.

### Motion

Light drifts over 90 seconds and pauses off screen. Once in view: a lid lifts, a label rises, its stamp lands and a tick ripples to whoever else sees it. Reduced motion or no script: the end state, light still.

### Voice

A pharmacist's plainness, spoken by a family: the name, the dose, the time, who gave it, in the words a son or daughter uses (Mum, your brother). Never a journey, never a warning in red.

### Do-nots

- Never red or amber for a missed or late state; it is grey.
- Never a plastic tint as a signal or a second brand colour; the green does every signal.
- Never clinical stock: spilled pills, blister packs in close-up, white coats.
- Never glossy toy plastic: tints stay pale, light is daylight, no gradients beyond the glint and the shade.

### Build hint

```css
h1, h2, h3 { font-family: var(--font-display); font-weight: 700; letter-spacing: var(--tracking-display); line-height: 1.02; }
.btn { height: 52px; padding: 0 var(--space-lg); border: 0; border-radius: var(--radius-input); font: 500 var(--text-md) var(--font-body); box-shadow: inset 0 1px 0 var(--glint), 0 0 0 1px var(--color-rule), 0 3px 0 var(--color-rule); transition: transform var(--dur-micro) var(--ease-out); }
.btn--primary { background: linear-gradient(var(--color-accent), var(--color-accent-deep)); color: var(--color-accent-ink); box-shadow: 0 0 0 1px var(--color-accent-deep), 0 3px 0 var(--color-accent-deep); }
.btn:active { transform: translateY(3px); }
.plastic { --t: var(--p-thu); position: relative; border-radius: var(--radius-card); background: linear-gradient(color-mix(in oklab, var(--glint) 32%, transparent), transparent 18%), color-mix(in oklab, var(--t) 62%, transparent); box-shadow: inset 0 1.5px 0 var(--glint), inset 0 -24px 36px -28px color-mix(in oklab, var(--t) 45%, var(--color-ink)); }
.dose, .label { font-family: var(--font-outlier); font-variant-numeric: tabular-nums; }
.band--ink { background: var(--color-ink); color: var(--color-paper); }
```
