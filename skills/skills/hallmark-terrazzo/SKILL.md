---
name: hallmark-terrazzo
description: "Terrazzo: off-white paper, white card surfaces ruled in ink over a hard offset, wide Syne heads over Onest, JetBrains Mono for codes and millimetres, surfaces photographed flat-on in true colour, rust the one signal. Fits: materials, library, architects, samples, catalogue, surfaces, stone, timber, terrazzo, ceramic, tile, interiors, interiors studio, showroom, specification, swatches, supplier, drawer, photography, tactile"
metadata:
  origin: hallmark
  category: themes
  group: style
  mode: manual
  title: Terrazzo
  summary: минимализм, светлый, сдержанный акцент
  preview: "#F5F1EB #E9E4DC #0F0D0B #B14420 · Syne"
---
# Terrazzo — a Hallmark style

The designer chose this style for the chat. A style is a material: paper, ink, faces, rules, radius, depth, controls
and voice. It is never a layout. It was written for web pages in CSS; in FigCraft:

- **Tokens become the file's variables.** Look at the file's variables first (`variable.export`). With no colour
  collection for this style, make one named «Terrazzo»: the `--color-*` tokens as colour variables without the prefix
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

A materials library's specification voice: off-white paper, near-black ink, wide Syne heads over a plain Onest body, JetBrains Mono for the codes and the millimetres, and white card surfaces ruled in 2px ink over a hard offset, holding the surfaces themselves photographed flat-on and close. Controls are ink; colour arrives only in aggregate, in the stone, timber, terrazzo and glaze the photographs show, with rust as the one signal. It is organised like a sample drawer and reads like a spec sheet. It is not a pastel lifestyle page and not confetti.

### Tokens

```css
:root {
  --color-paper: #F5F1EB; --color-paper-2: #E9E4DC; --color-paper-3: #DBD5CC;
  --color-plate: #FEFDFB;
  --color-ink: #0F0D0B; --color-ink-2: #292624; --color-muted: #5C5753;
  --color-rule: #C5C0B8;
  --color-accent: #B14420; --color-accent-soft: #F6DBCF; --color-accent-ink: #FEFDFB; --color-focus: #AA3606;
  --font-display: "Syne", ui-sans-serif, sans-serif; --font-body: "Onest", ui-sans-serif, sans-serif;
  --font-outlier: "JetBrains Mono", ui-monospace, monospace;
  --radius-card: 0; --radius-pill: 0; --rule-hair: 1px; --rule-bar: 2px;
  --shadow-card: 14px 14px 0 var(--color-paper-3); --shadow-card-hover: 14px 14px 0 var(--color-ink);
  --tracking-display: -0.025em; --display-weight: 700;
}
```

Three colourways, stated in the stamp (`terrazzo: off-white`).

| Colourway | Paper and ink | Signal and controls |
| --- | --- | --- |
| **Off-white** (default) | the tokens above | rust; ink controls |
| **Black** | `#0B0907` under bone ink `#F5F1EA`; cards stay white | rust lifted to `#DF7752`; bone controls with ink text |
| **Stone** | warm grey `#D2CDC5` under the same ink | rust; ink controls |

### Type

- **Display:** Syne 700, `--tracking-display`, line-height 1.0, sentence case. The face sets wide, so heads stay short rather than drop a step; 800 turns clumsy and is never used. A figure at display size takes -0.04em.
- **Body:** Onest 400 and 500, line-height 1.5. Three weights a page: 400, 500, 700.
- **Labels, captions, table heads:** Onest 500 a step smaller, sentence case, untracked.
- **Codes and measures:** JetBrains Mono 500 for a sample code (`ST-0412`), a size in millimetres, a count in a table; the size of the text beside it, never a label or a head.

### Surfaces

- Rules: `--rule-bar` ink on the top of a table, along a band's edge and around a card; `--rule-hair` in `--color-rule` between rows. Radius 0 everywhere.
- Cards: `--color-plate` inside a `--rule-bar` ink border over the hard `--shadow-card` (paper-3, no blur), the page's one container; nothing else casts. A linked card swaps its offset to ink on hover.
- Bands: a `--color-ink` band with paper text, or a `--color-paper-2` band; never a coloured field, two a page at most.
- Photographs: the surface itself, flat-on and close in even daylight, so grain, chips, veins and joints read near one to one; a set of four runs as a true set at one ratio. True colour, a little sharpened. Each sits in a card, edge to edge with its caption beneath naming the family and the finish; type never sits on a photograph.
- No texture and nothing drawn on the paper: the surfaces in the photographs are the pattern.

### Range

- **Specification table:** the stock as a full-width table under a `--rule-bar` ink rule: the code and the size in mono, the surface's name in Onest 500 at title size, family and finish in muted; a hovered or selected row takes `--color-accent-soft` and a rust code.
- **Figure on the ink band:** the library's one big number in Syne at twice `--text-display`, paper on ink, with the families or the terms set beside it as a short ruled list.
- **Steps on rules:** a real ordered list hung from hairlines, each numeral in Syne at section size, the stage in Onest 500 and one line beside it.
- **Form as a request card:** the booking on a white card with its hard offset, inputs square on the plate colour, choices as square cells joined edge to edge, the checked cell ink with paper text.

### Controls

- An ink-filled primary with paper text beside a `--rule-bar` inset ink outline, both square, Onest 500. On the ink band the primary turns plate with ink text.
- Links are ink with a hairline underline that turns rust on hover; inputs are square on `--color-plate` with a 1px ink border.
- Rust reaches a code, a selected row or chip, a hover underline and the focus ring; colour otherwise comes only from the photographs.

### Motion

Still. A linked card swaps its offset from paper-3 to ink over `--dur-micro`; a filtered row leaves without animation.

### Voice

A catalogue's plainness: the family, the finish, the code, the size at one to one. Never sells the feeling of stone.

### Do-nots

- Never a drawn chip, speck or confetti; a surface's colour comes from its photograph.
- Never a photograph as a background or under type; it lives in a card.
- Never a coloured primary on off-white paper; controls are ink.
- Never a rounded corner, on a card, a control or a photograph.

### Build hint

```css
h1, h2, h3 { font-weight: 700; line-height: 1; }
.btn { border-radius: 0; padding: var(--space-md) var(--space-lg); font-weight: 500; color: inherit; }
.btn--primary { background: var(--color-ink); color: var(--color-paper); }
.btn--secondary { box-shadow: inset 0 0 0 var(--rule-bar) currentColor; }
.card { background: var(--color-plate); border: var(--rule-bar) solid var(--color-ink); box-shadow: var(--shadow-card); }
a.card { transition: box-shadow var(--dur-micro) var(--ease-out); }
a.card:hover { box-shadow: var(--shadow-card-hover); }
.band--ink { background: var(--color-ink); color: var(--color-paper); }
.band--ink .btn--primary { background: var(--color-plate); color: var(--color-ink); }
.spec { border-top: var(--rule-bar) solid var(--color-ink); } .spec tr:hover { background: var(--color-accent-soft); }
.code { font-family: var(--font-outlier); font-weight: 500; font-variant-numeric: tabular-nums; }
::selection { background: color-mix(in oklab, var(--color-accent) 25%, transparent); }
```
