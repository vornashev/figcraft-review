---
name: hallmark-squeeze
description: "Squeeze: forest-green paper with real chroma, warm white ink, Gabarito 800 heads and figures over Manrope, soft rounded tiles a step lighter or deeper, fruit photographed bright and close, juicy peach controls. Fits: fruit, food box, grocer, market, delivery, weekly, seasonal, farm shop, subscription, produce, veg box, cheerful, family, treats, stall, orchard, local, fresh"
metadata:
  origin: hallmark
  category: themes
  group: style
  mode: manual
  title: Squeeze
  summary: игривый, средний тон, залит цветом
  preview: "#075930 #1B6B3E #FDFCF8 #FFB37C #F68953 · Gabarito"
---
# Squeeze — a Hallmark style

The designer chose this style for the chat. A style is a material: paper, ink, faces, rules, radius, depth, controls
and voice. It is never a layout. It was written for web pages in CSS; in FigCraft:

- **Tokens become the file's variables.** Look at the file's variables first (`variable.export`). With no colour
  collection for this style, make one named «Squeeze»: the `--color-*` tokens as colour variables without the prefix
  (`paper`, `ink`, `accent`…), radii as numbers; bind fills, strokes and radii to them (`variable.bind`), never paste
  hex. A file that already has its own colour system keeps it: restyle it onto this one only when asked.
- **Faces.** Check each family with `text.fonts {family}`. A missing one: say so in one line and take the nearest
  installed face of the same class (geometric-sans); never swap silently. Make text styles for display, body, labels
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

## Genre: playful

Pages that should feel alive rather than tidy: a prompt that asks for playful, fun, friendly or soft, or one for kids, games or a community. A consumer or family prompt without that ask stays editorial. The deal leans toward this genre's themes, which run from soft and warm to loud and retro.

## Voice

- **Accent:** soft and low-chroma by default; a declared Full-palette or Drenched posture lifts chroma to 0.24 across three or four named roles, each with a job.
- **Layout:** rounded surfaces (12px cards, 8px inputs, pills, unless the theme sets its radius), soft offset shadows, tinted alternating bands.
- **Motion:** responsive to the pointer; one small entrance on the page, its one reveal (`craft.md` § 5); a spring only under a declared spring posture, on the primary CTA and one character moment (gate 12's exception).
- **Copy:** warm, direct, specific; no quirk for its own sake.

## Allowed here

Soft drop shadows with an offset; hover lifts on cards; a hard-offset shadow when the theme declares it as material; a single character moment; emoji inside a sentence, never as an ornament or icon.

## Refused here

Saturated consumer pinks and violets without a declared posture; Comic-style faces; bounce on anything but the declared moments; glass; gradient text; decorative status dots and sticker-style pills stamped on every element (63, 66).

## Chrome that fits

A heavy slab bar, a dense bar with rounded knobs, a banner, a marquee footer. A masthead or a blurred pill fights the register; a solid pill does not. Affinities, not assignments.


## The theme

A market stall in colour: a forest-green ground with real chroma, warm white ink, Gabarito's round, heavy heads and figures over a sturdy Manrope, soft tiles a step lighter or deeper, fruit photographed bright and close, juicy peach controls and one warm-white card. It is cheerful because the green is the whole surface and the fruit is the colour on it; a price or a day set huge in Gabarito is as much the material as a crate of fruit. It is not a neutral grocery template with a green button, and not an organic label in serif and kraft.

### Tokens

```css
:root {
  --color-paper: #075930; --color-paper-2: #1B6B3E; --color-paper-3: #004523;
  --color-ink: #FDFCF8; --color-ink-2: #E9EDDF; --color-muted: #D1E4D4; --color-rule: #3C8256;
  --color-accent: #FFB37C; --color-accent-2: #F68953; --color-accent-ink: #4A2010; --color-focus: #FFD060;
  --color-card: #F9F5EC; --color-card-ink: #032617;
  --font-display: "Gabarito", ui-sans-serif, system-ui, sans-serif; --font-body: "Manrope", ui-sans-serif, system-ui, sans-serif;
  --font-outlier: var(--font-display);
  --radius-card: 24px; --radius-control: 16px; --radius-pill: 999px; --rule-hair: 1px; --rule-bar: 2px;
  --shadow-card: 0 14px 32px -16px #00211280;
  --tracking-display: -0.025em; --display-weight: 800;
}
```

### Type

- **Display:** Gabarito 800, `--tracking-display`, line-height 1.0, sentence case, one colour per head. Round, compact and heavy, so it takes the shared display scale without a cap; never under 700.
- **Figures:** prices, dates and days in Gabarito 800 with tabular, lining numerals; a single figure may run three to four times the section head, tracked to -0.04em, with its unit at the same weight.
- **Body:** Manrope 500, line-height 1.55, in `--color-muted`; links and row titles at 700. Three weights in all: 800, 700, 500.
- **Labels, captions, table heads, meta:** Manrope 700 a step smaller, sentence case, untracked. Never mono, never uppercase.

### Surfaces

- Tiles, not cards: a tile is the ground one step lighter (`--color-paper-2`) at `--radius-card`, no border, no shadow; a sunk well takes `--color-paper-3`. A tile a visitor can choose sinks to `--color-paper-3` when chosen and takes a 3px `--color-accent` ring.
- The one raised surface is the warm-white card (`--color-card`, `--color-card-ink` type, `--shadow-card`), once a page, for the thing a visitor pays for; inside it the focus ring takes `--color-card-ink`.
- Rules at `--rule-bar` in `--color-rule`; only a rule between list rows is `--rule-hair`.
- Bands: the page is green, so a band is the lighter or the deeper green (`--color-paper-2`, `--color-paper-3`); two a page at most, never a white, grey or peach band.
- Photographs: fruit close in daylight, a crate from above, fruit held out, a heap on a stall; bright, the fruit filling the frame. `--radius-card`, no ring, no shadow; captions under in the label style; type on a photograph sits over a `--color-paper-3` scrim at 45 to 65%.
- No texture: the green is a flat colour.

### Range

- A price, a size or a day set as one figure at statement size: Gabarito 800 in ink straight on the green, its unit at full weight, the head and one line beside it on the remaining columns. The green and the figure carry the screen alone.
- A timetable of real dates as tiles or full-width rows: each date big in Gabarito, the weekday in the label style, the chosen one sunk to `--color-paper-3` and ringed in peach; a stall's chalkboard that works as a control.
- A promise set as a statement on the deeper green band, Gabarito at display size across ten columns, one action under it.
- Questions or plain terms as rows: Gabarito titles on the left, Manrope answers on the right, hair rules in `--color-rule` between.

### Controls

- The control pair: a peach-filled primary with `--color-accent-ink` text beside a 2px ink-outlined secondary, both at `--radius-control`, Manrope 700. Tags and chips are pills; nav links may be `--color-paper-2` pills.
- Links are ink at 700, the underline turning peach on hover; inputs take a 2px `--color-rule` border at `--radius-control` and the `--color-focus` ring.
- Peach stays on controls: the primary, a chosen chip or tile ring, a link's hover; `--color-accent-2` is the primary's pressed and hover step only. Never peach type and never a peach field.

### Motion

Cheerful and quick, state only: a control presses 1px down at `--dur-micro`, a chosen tile rings at `--dur-short` on `--ease-out`, a choosable tile steps a green lighter on hover. No reveal, no parallax, no loop; nothing that cannot be pressed reacts.

### Voice

The stall-holder's, out loud on a Thursday morning: the fruit, the day it comes, what ripe feels like in the hand. Short, warm sentences with the price said plainly; never gourmet, never a wellness pitch.

### Do-nots

- Never a neutral ground. White is for the one card; grey does not exist. The page is green.
- Never a dull or greyed green; the ground keeps its chroma, or it turns to army surplus.
- Never a weight under 500, a serif, or a mono figure: numbers are Gabarito.
- Never a hairline border; a 1px rule lives only between list rows.
- Never a dim photograph, and never one on every screen: the fruit is brightest when the green and the type get screens of their own.

### Build hint

```css
h1, h2, h3 { font-family: var(--font-display); font-weight: var(--display-weight); letter-spacing: var(--tracking-display); }
h1, h2 { line-height: 1; }
.figure { font: var(--display-weight) clamp(7rem, 16vw, 15rem)/0.85 var(--font-display); letter-spacing: -0.04em; font-variant-numeric: lining-nums tabular-nums; }
.tile { background: var(--color-paper-2); border-radius: var(--radius-card); }
.tile:has(:checked) { background: var(--color-paper-3); box-shadow: inset 0 0 0 3px var(--color-accent); }
.card { background: var(--color-card); color: var(--color-card-ink); border-radius: var(--radius-card); box-shadow: var(--shadow-card); }
.btn { border: var(--rule-bar) solid var(--color-ink); border-radius: var(--radius-control); padding: var(--space-sm) var(--space-lg); font: 700 var(--text-md)/1.25 var(--font-body); color: var(--color-ink); transition: translate var(--dur-micro) var(--ease-out), background-color var(--dur-micro) var(--ease-out); }
.btn--primary { background: var(--color-accent); color: var(--color-accent-ink); border-color: var(--color-accent); }
.btn--primary:hover { background: var(--color-accent-2); border-color: var(--color-accent-2); }
.btn:active { translate: 0 1px; }
.photo img { border-radius: var(--radius-card); }
::selection { background: color-mix(in oklab, var(--color-accent) 45%, transparent); color: var(--color-card-ink); }
```
