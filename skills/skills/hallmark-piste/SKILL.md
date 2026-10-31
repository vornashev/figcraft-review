---
name: hallmark-piste
description: "Piste: snow-white paper, cold near-black ink, Barlow Condensed 800 caps over Barlow, square edges on 2px ink rules, one cobalt for signal and field. Fits: ski, mountain, resort, snow, winter, outdoor, sport, trail, lift, race, alpine, tickets, season pass, conditions, weather, club, active, bold"
metadata:
  origin: hallmark
  category: themes
  group: style
  mode: manual
  title: Piste
  summary: игривый, светлый, уверенный акцент
  preview: "#F8FAFE #EDF0F6 #0A0D12 #1F50F5 · Barlow Condensed"
---
# Piste — a Hallmark style

The designer chose this style for the chat. A style is a material: paper, ink, faces, rules, radius, depth, controls
and voice. It is never a layout. It was written for web pages in CSS; in FigCraft:

- **Tokens become the file's variables.** Look at the file's variables first (`variable.export`). With no colour
  collection for this style, make one named «Piste»: the `--color-*` tokens as colour variables without the prefix
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

A mountain morning in print: snow-white paper, cold near-black ink, Barlow Condensed 800 in capitals for every head and figure, square edges on 2px ink rules, and one cobalt doing all the colour work, from the primary control to a full field. Photographs bring the mountain in, crisp and in full colour, cut square, and the paper is the snow they open onto. It reads bold because the type is loud and the colour one cold blue; it is not a lens-flare resort brochure, a sporty gradient or a rounded app.

### Tokens

```css
:root {
  --color-paper: #F8FAFE; --color-paper-2: #EDF0F6; --color-paper-3: #DDE1E8;
  --color-ink: #0A0D12; --color-ink-2: #2A2E35; --color-muted: #585E67;
  --color-rule: #D4D8DE;
  --color-accent: #1F50F5; --color-accent-deep: #1633B1; --color-accent-ink: #F8FAFD; --color-focus: #DF2321;
  --color-field: var(--color-accent);
  --font-display: "Barlow Condensed", ui-sans-serif, sans-serif; --font-body: "Barlow", ui-sans-serif, sans-serif; --font-outlier: var(--font-display);
  --radius-card: 0; --radius-pill: 0; --rule-hair: 1px; --rule-bar: 2px;
  --shadow-card: none;
  --tracking-display: -0.005em; --display-weight: 800;
}
```

Committed: cobalt is `--color-field` and may fill a band; on controls and links it is the signal, `--color-accent-deep` its hover and pressed step. Three grounds, stated in the stamp (`piste: snow`): `snow` (the block above), `blue-run` (the page is the cobalt field under white ink; white takes the controls and focus) and `night-piste` (`#07090D` under white ink, 2px white rules, cobalt at 56%, focus red at 60%).

### Type

- **Display:** Barlow Condensed 800, uppercase, roman, `--tracking-display`; line-height 1.0 on any head that can wrap, 0.9 only on a single line that cannot. Condensed, so it sets one step larger than the shared scale: a section head at `--text-display-s` and up, the hero head up to 8rem.
- **Figures:** the display face at 800, tabular, from `--text-display` to twice it; a figure on paper takes cobalt, a figure on the field takes paper. The label beneath is Barlow 500.
- **Body:** Barlow 400 and 500, 17 to 19px, line-height 1.5; it is read outdoors, so never lighter.
- **Buttons:** Barlow Condensed 800 in capitals at 18px, untracked (legal under 67 on an uppercase display). Nav links, table heads, captions: Barlow 500 a step smaller, sentence case.

### Surfaces

- Rules: `--rule-bar` ink above a list, a figure row or a table's head, and under a floating bar; `--rule-hair` in `--color-rule` between rows. Ruled, never boxed.
- Radius 0 on everything: wells, photographs, inputs, controls and tags are cut square. Depth is flat: a raised surface is a paper step or the cobalt field, never a shadow.
- Bands: the cobalt field with `--color-accent-ink` type, or `--color-paper-2` under a form or a dense table; two a page at most.
- Photographs: the mountain in daylight and colour: a group on a slope seen from behind, a line of children after an instructor, skis standing in fresh snow, a lift against the sky; crisp and high-key, never a dusk grade or a flare. Cut square with an inset ink hairline at 8%. Ink sits straight on bright snow; paper sits on sky only over a cold ink scrim.
- No texture, no gradient but a scrim, no blur.

### Range

- **A figure row as a lift board:** the prompt's numbers in the condensed face at up to twice `--text-display`, cobalt on snow, under a `--rule-bar` ink rule and parted by hairlines, each with one Barlow line.
- **Statement on the field:** one short line in condensed capitals at display size and beyond, paper on cobalt edge to edge, the line the morning report would shout.
- **Steps or a timetable:** an `<ol>` with each numeral in the condensed face at `--text-display` in cobalt over a 2px ink rule, a capital title and one line; or a ruled table of times and groups with the head rule in ink.
- **Forms as a ticket desk:** square 52px inputs and ink steppers on paper-2, the cobalt primary the only colour on the band.

### Controls

- The pair: a cobalt fill with `--color-accent-ink` text beside a 2px inset ink outline, both square, in condensed capitals; on a scrim or the field the outline turns paper. Hover takes `--color-accent-deep`; active takes ink.
- Links are ink and underlined, cobalt on hover; inputs square, 52px, a 1px ink border; a stepper is two square ink-bordered buttons around a tabular count.
- Cobalt sits on the primary, a link's hover, a field band and figures; red is the focus ring and nothing else.

### Motion

Still. A control steps one shade on hover over `--dur-micro` on `--ease-out`; nothing draws in, loops or follows the scroll.

### Voice

The morning report: the hour, the group, the week booked, called across the snow. Never a slogan about freedom or powder.

### Do-nots

- Never lowercase display or a light condensed; Barlow Condensed at 800.
- Never a rounded corner, a pill or a soft card.
- Never a second accent hue, never cobalt on running text or as a card fill on snow paper.
- Never a sky gradient, a sunset grade, or a drawn mountain, snowflake or piste map.

### Build hint

```css
h1, h2, h3 { font-weight: 800; text-transform: uppercase; line-height: 1; }
h2 { font-size: var(--text-display-s); }
.fig { font: 800 var(--text-display)/0.9 var(--font-display); color: var(--color-accent); font-variant-numeric: tabular-nums; }
.btn { display: inline-flex; align-items: center; min-height: 52px; padding: 0 var(--space-lg); border: 0; font: 800 var(--text-lg)/1 var(--font-display); text-transform: uppercase; }
.btn--primary { background: var(--color-accent); color: var(--color-accent-ink); }
.btn--primary:hover { background: var(--color-accent-deep); }
.btn--secondary { background: none; box-shadow: inset 0 0 0 var(--rule-bar) var(--color-ink); color: var(--color-ink); }
.band--field { background: var(--color-field); color: var(--color-accent-ink); }
.photo { outline: 1px solid color-mix(in oklab, var(--color-ink) 8%, transparent); outline-offset: -1px; }
th { border-bottom: var(--rule-bar) solid var(--color-ink); font: 500 var(--text-sm) var(--font-body); text-align: left; }
td { border-bottom: var(--rule-hair) solid var(--color-rule); }
::selection { background: color-mix(in oklab, var(--color-accent) 30%, transparent); }
```
