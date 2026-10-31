---
name: hallmark-overprint
description: "Overprint: grey newsprint stock, near-black ink, wide heavy Anybody capitals over Archivo, flat square fills, a teal pass and an orange pass that print moss where they cross, photographs pulled through one pass. Fits: venue, gigs, live music, festival, music, label, print studio, bar, club, poster, tickets, events, nightlife, two-colour, screenprint, punk, zine, loud, listings, door"
metadata:
  origin: hallmark
  category: themes
  group: style
  mode: manual
  title: Overprint
  summary: игривый, светлый, полная палитра
  preview: "#E6E3D9 #DAD6C9 #120F0C #00A2B9 #FB7500 · Anybody"
---
# Overprint — a Hallmark style

The designer chose this style for the chat. A style is a material: paper, ink, faces, rules, radius, depth, controls
and voice. It is never a layout. It was written for web pages in CSS; in FigCraft:

- **Tokens become the file's variables.** Look at the file's variables first (`variable.export`). With no colour
  collection for this style, make one named «Overprint»: the `--color-*` tokens as colour variables without the prefix
  (`paper`, `ink`, `accent`…), radii as numbers; bind fills, strokes and radii to them (`variable.bind`), never paste
  hex. A file that already has its own colour system keeps it: restyle it onto this one only when asked.
- **Faces.** Check each family with `text.fonts {family}`. A missing one: say so in one line and take the nearest
  installed face of the same class (grotesk-heavy); never swap silently. Make text styles for display, body, labels
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

A two-colour screenprint on cheap stock: grey newsprint, near-black ink, wide heavy Anybody capitals over a plain Archivo body, and two transparent flat inks, teal and orange, that print a deep moss where they cross. Photographs print hard through one pass, as a bill prints them. All in register, flat and square: the noise is scale and two inks, never effects. It is not a retro poster pastiche, a misregistered print or a neon flyer.

### Tokens

```css
:root {
  --color-paper: #E6E3D9; --color-paper-2: #DAD6C9; --color-paper-3: #CDC7B8;
  --color-ink: #120F0C; --color-ink-2: #2F2A26; --color-muted: #514C46;
  --color-rule: #BDB7A9;
  --color-accent: #00A2B9; --color-accent-ink: #120F0C; --color-focus: #005E78;
  --color-accent-2: #FB7500; --color-accent-2-ink: #120F0C;
  --color-mix: #024A00;
  --blend: multiply; --texture-opacity: 0.06;
  --font-display: "Anybody", ui-sans-serif, sans-serif; --font-body: "Archivo", ui-sans-serif, sans-serif;
  --font-outlier: "Archivo Narrow", ui-sans-serif, sans-serif;
  --radius-card: 0; --radius-pill: 0; --rule-hair: 1px; --rule-bar: 4px;
  --shadow-card: none;
  --tracking-display: -0.01em; --display-weight: 900; --display-stretch: 140%;
}
```

Both passes are fills under ink type, never type, and the moss is what the multiply prints where they cross, never painted. Two stocks, stated in the stamp (`overprint: newsprint`): newsprint, the tokens above; or black stock, `#15161B` under `#F1EEE7`, the blend flipped to screen so the overlap goes pale, passes in yellow `#FBD530` and aqua `#17D0D8`, focus in the aqua.

### Type

- **Display:** Anybody 900, set wide (`--display-stretch`, 130 to 150%), uppercase, line-height 1.0 to 1.02, `--tracking-display`. Figures, times and prices take it at 150% with `tabular-nums`.
- **Body:** Archivo 400 and 600, 16 to 17px, line-height 1.5, in ink.
- **Small print:** Archivo Narrow 600 a step smaller, sentence case, untracked, for days, hours and table heads: the label face. Captions are Archivo. No mono.

### Surfaces

- Two passes: everything coloured is pass 1 or pass 2, a flat fill at `mix-blend-mode: var(--blend)`, so where the two cross the stock prints `--color-mix`; type never sits on the moss.
- Rules: the 4px ink `--rule-bar` across the top of a list, a table, a figure row or the nav; `--rule-hair` in `--color-rule` between rows.
- Radius 0, no shadow, no gradient but a photograph's scrim: depth by overprint, never a lift.
- Bands: `--color-paper-2`, the ink with paper type, or one pass field with ink type; two a page.
- Photographs: the night, close or from behind, in the light it was played under (a crowd under one wash, hands on a fretboard, the bar at doors); never posed, never a face to the lens. Grey and hard, multiplied onto one pass field so lights print teal or orange and shadows ink; square, full-bleed or to a column edge, no frame. Type sits beside a picture, or knocks out to the stock over its darkest part on an ink scrim.
- Texture: grain (`texture.md` § 1) at `--texture-opacity` on a band, a pass field or a photograph, never under running text.

### Range

- **Figures as a bill:** the prompt's own times, capacity or price set at poster scale in wide Anybody, each figure on its own pass field; two fields cross by a column so the overlap prints moss, and no letter stands in it.
- **The listing as a ruled table:** under the 4px bar, heads in Archivo Narrow, the act in wide capitals at title size, nights and prices in tabular figures; an on-sale cell takes pass 1, a sold-out cell pass 2.
- **Steps as numbered bills:** a process as three or four cells under the bar, each numeral wide and heavy, each cell flooded in one pass, alternating.
- **A band of ink:** the black field with stock type and grain, holding one statement in wide capitals or a form with a pass-1 control.

### Controls

- The control pair: a pass-1 fill with `--color-accent-ink` type in Archivo Narrow 600 capitals, untracked (67 allows it under an uppercase display), beside a 2px inset ink outline (paper on the ink).
- Pass 1 takes the primary and an open state; pass 2 the closed state (sold out). Links are ink with a 2px pass-1 underline that turns ink on hover; inputs square in the 2px inset ink outline.

### Motion

The press does not tween: hover pulls the primary through the other pass (teal to orange) at once, press darkens it by an ink step, and nothing reveals, floats or loops.

### Voice

The bill on the wall: who plays, which night, doors, the price, and whether it has sold out.

### Do-nots

- Never a third ink; the moss is printed by the overlap, never mixed into a fill, a control or a letter.
- Never out of register or set apart: no echo, no offset copy, no recoloured word, no ghosted second head.
- Never a photograph in colour, or one printed through both passes.
- Never shapes drawn to show the overprint off; the passes print surfaces the page already has.
- Never lowercase or narrow display; the heavy grotesk is shouted and wide.

### Build hint

```css
h1, h2, h3 { font-weight: 900; font-stretch: var(--display-stretch); text-transform: uppercase; line-height: 1.02; }
.btn { border: 0; border-radius: 0; padding: var(--space-md) var(--space-lg); font: 600 var(--text-sm) var(--font-outlier); text-transform: uppercase; }
.btn--primary { background: var(--color-accent); color: var(--color-accent-ink); } .btn--primary:hover { background: var(--color-accent-2); }
.btn--secondary { box-shadow: inset 0 0 0 2px var(--color-ink); color: var(--color-ink); }
.pass-1 { background: var(--color-accent); color: var(--color-accent-ink); mix-blend-mode: var(--blend); }
.pass-2 { background: var(--color-accent-2); color: var(--color-accent-2-ink); mix-blend-mode: var(--blend); }
.pass-1 > img, .pass-2 > img { filter: grayscale(1) contrast(1.3); mix-blend-mode: var(--blend); }
.figure { font: 900 var(--text-display)/1 var(--font-display); font-stretch: 150%; font-variant-numeric: tabular-nums; }
.grain { position: relative; isolation: isolate; }
.grain::after { content: ""; position: absolute; inset: 0; pointer-events: none; opacity: var(--texture-opacity); background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='200'%3E%3Cfilter id='g'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.85' numOctaves='2' stitchTiles='stitch'/%3E%3CfeColorMatrix values='0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 9 -4'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23g)'/%3E%3C/svg%3E") 0 0 / 200px; }
::selection { background: color-mix(in oklab, var(--color-accent-2) 40%, transparent); }
```
