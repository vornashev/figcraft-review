---
name: hallmark-hum
description: "Hum: grained cream paper pulled toward pear-yellow, torn paper edges with a pale fibre core, card-stock controls that press down, blue-black ink, Chillax throughout, three accents that never blend and a mint for growth. Fits: daily, habit, streak, practice, learning, reading, curiosity, mood, energy, friendship, community, kids, family, parents, school, game, puzzle, creative, playful, alive"
metadata:
  origin: hallmark
  category: themes
  group: style
  mode: manual
  title: Hum
  summary: игривый, светлый, полная палитра
  preview: "#F7F5EC #F0EDE0 #12161C #F7D21A #0064BE · Chillax"
---
# Hum — a Hallmark style

The designer chose this style for the chat. A style is a material: paper, ink, faces, rules, radius, depth, controls
and voice. It is never a layout. It was written for web pages in CSS; in FigCraft:

- **Tokens become the file's variables.** Look at the file's variables first (`variable.export`). With no colour
  collection for this style, make one named «Hum»: the `--color-*` tokens as colour variables without the prefix
  (`paper`, `ink`, `accent`…), radii as numbers; bind fills, strokes and radii to them (`variable.bind`), never paste
  hex. A file that already has its own colour system keeps it: restyle it onto this one only when asked.
- **Faces.** Check each family with `text.fonts {family}`. A missing one: say so in one line and take the nearest
  installed face of the same class (rounded-sans); never swap silently. Make text styles for display, body, labels
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

Cut paper made by hand, cheerful without turning childish: cream paper with a visible grain and fibre, sheets torn along their edges so a pale core shows, card stock you can press, all lit from the top left. Chillax runs from head to label (its single-storey a and g read like an early reader's page) in a blue-black ink. Three accents never blend: pear for the action, blue for links, coral for one loud moment; mint is growth. Not a pastel nursery template, not a rainbow page, not clip-art.

### Tokens

```css
:root {
  --color-paper: #F7F5EC; --color-paper-2: #F0EDE0; --color-paper-3: #E6E1D1;
  --color-ink: #12161C; --color-ink-2: #272C32; --color-muted: #565B63;
  --color-rule: #D7D4C9;
  --color-accent: #F7D21A; --color-accent-deep: #C9A000; --color-accent-ink: #12161C;
  --color-accent-2: #0064BE; --color-accent-3: #FF5E63;
  --color-mint: #70E093; --color-mint-deep: #00713E; --color-focus: #0064BE;
  --color-card: #FCFBF6; --color-edge: #D2C6AA; --color-fringe: #FEFCF8;
  --color-kraft: #AE7D52; --color-sand: #D9AC69; --color-sugar: #C6DFEF;
  --color-hill-1: #EBF0DA; --color-hill-2: #D6EACC; --color-leaf: #36A558;
  --font-display: "Chillax", ui-rounded, ui-sans-serif, sans-serif; --font-body: var(--font-display);
  --font-outlier: "Geist Mono", ui-monospace, monospace;
  --radius-card: 24px; --radius-stock: 16px; --radius-input: 14px; --radius-pill: 999px; --rule-hair: 1px;
  --shadow-card: 0 1px 2px #12161C0F, 0 12px 28px -14px #12161C38;
  --shadow-paper: drop-shadow(0 0 0.6px #12161C52) drop-shadow(1.5px 2.5px 1.5px #12161C1A) drop-shadow(6px 14px 16px #12161C21);
  --tracking-display: -0.03em; --display-weight: 600;
  --ease-spring: cubic-bezier(0.34, 1.56, 0.64, 1); --ease-snap: cubic-bezier(0.22, 1, 0.36, 1);
}
```

### Type

- **Display:** Chillax 600, `--tracking-display`, line-height 1.02 to 1.05, sentence case. Figures at `--text-display` or larger, their unit at `--text-title`.
- **Body:** Chillax 500 at 17 to 19px, line-height 1.5; emphasis is a pear highlighter band behind the words, never inside a head. Two weights, 500 and 600.
- **Labels, captions, units:** Chillax 500 a step smaller, sentence case, `--color-muted`. Geist Mono only inside code.

### Surfaces

- The paper is generated, never a picture: two `feTurbulence` data URIs, a fine fractal grain (`--grain`) and a long turbulence fibre (`--fibre`), under every paper, card and accent fill.
- Torn edges: a band, a nav bar, a photograph or a sheet ends in a `clip-path` polygon from seeded value noise, its fibre twin (`--color-fringe`) standing a pixel proud beneath. Grounds may layer: far hills in `--color-hill-*`, soil in `--color-leaf`, a kraft strip, a blue sugar-paper mat.
- Light comes from the top left: stacked `--shadow-paper` drop shadows fall down and right on every cut sheet; a card may lift one corner in a page curl.
- Round everywhere: 24px surfaces (28 to 32px for children), 16px card stock, no square corner.
- Bands: paper-2, a torn ink sheet with paper text, or one pear field. Two a page at most.
- Photographs: bright daylight at a child's height, never a face to camera; torn on one edge, one or two a page.

### Range

- **The product as card stock:** the app's own moment built large, words as card-stock tiles on a torn kraft strip, each pressed one popping into its accent.
- **Growth set in type:** a bed of plants made of Chillax glyphs (stems of l, bracket leaves, letter heads) on torn soil, filling as the prompt's numbers say, shown in states a row of pills switches.
- **Figures on the pear field:** three or four of the prompt's numbers at display size in ink on one pear sheet, each unit beneath in 500.
- **A choice as card-stock pills:** a working control on the prompt's facts, the result a sentence with its key value in a pear highlighter band.

### Controls

- Card stock: 54px controls at `--radius-stock`, grain and fibre on the fill, an inset highlight on top and a solid 5px edge below (`--color-accent-deep` on the pear primary, `--color-edge` on the secondary card); hover raises the edge to 7px, active presses it to 1px. The spring runs on the primary only.
- Each accent owns a job: pear the primary and the one pear field; blue links and the focus ring; coral one loud fill; mint growth. A chosen pill is ink with paper type. One die-cut sticker may carry the offer.
- Inputs: 14px radius, 52px tall, a 1px `--color-muted` border, the blue focus ring.

### Motion

Spring posture declared (gate 12): `--ease-spring` on the primary control only; everything else on `--ease-snap`, never `scale()`. A word pops in its accent and its plant grows; a timer may tear off a scrap of paper as it runs, paused off screen. Reduced motion or no script: the end state.

### Voice

Warm, smart, casual, direct, written to the grown-up beside the child. Sentence case, verbs over nouns, honest numbers only.

### Do-nots

- Never a serif, never pure white paper, never a square corner.
- Never a clean vector edge on a cut sheet or a shadow that falls up or left.
- Never a gradient between two accents and never a rainbow ground.
- Never emoji, stock icons or a drawn character; type, paper and the product carry it.

### Build hint

```css
h1, h2, h3 { font-weight: var(--display-weight); }
.btn { --edge: 5px; border: 0; border-radius: var(--radius-stock); min-height: 54px; padding: 0 var(--space-lg); font-weight: 600; background: var(--grain), var(--fibre), var(--color-card); box-shadow: inset 0 0 0 1px var(--color-rule), 0 var(--edge) 0 0 var(--color-edge); transition: translate var(--dur-micro) var(--ease-snap), box-shadow var(--dur-micro) var(--ease-snap); }
.btn--primary { background: var(--grain), var(--fibre), var(--color-accent); color: var(--color-accent-ink); box-shadow: 0 var(--edge) 0 0 var(--color-accent-deep), 2px calc(var(--edge) + 4px) 10px -3px color-mix(in oklab, var(--color-ink) 32%, transparent); transition-timing-function: var(--ease-spring); }
.btn:hover { --edge: 7px; translate: 0 -2px; } .btn:active { --edge: 1px; translate: 0 4px; }
.sheet { position: absolute; filter: var(--shadow-paper); } .sheet > i { position: absolute; inset: 0; background: var(--grain), var(--fibre), var(--sheet-c, var(--color-paper-3)); }
mark { background: color-mix(in oklab, var(--color-accent) 55%, transparent); color: inherit; box-decoration-break: clone; }
a { color: var(--color-accent-2); }
```
