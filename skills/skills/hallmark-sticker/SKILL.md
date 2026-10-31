---
name: hallmark-sticker
description: "Sticker: warm off-white paper, warm black ink, Bowlby One SC over Sofia Sans, white die-cut borders on hard offset shadows, hot pink, lime and ink fills set with type. Fits: stickers, print, merch, shop, maker, creator, diy, craft, vinyl, packaging, labels, small business, ecommerce, fun, loud, pink, cut, ship, order"
metadata:
  origin: hallmark
  category: themes
  group: style
  mode: manual
  title: Sticker
  summary: игривый, светлый, полная палитра
  preview: "#F5F0E7 #EFE6D8 #1B1813 #D3036A #CAE649 · Bowlby One SC"
---
# Sticker — a Hallmark style

The designer chose this style for the chat. A style is a material: paper, ink, faces, rules, radius, depth, controls
and voice. It is never a layout. It was written for web pages in CSS; in FigCraft:

- **Tokens become the file's variables.** Look at the file's variables first (`variable.export`). With no colour
  collection for this style, make one named «Sticker»: the `--color-*` tokens as colour variables without the prefix
  (`paper`, `ink`, `accent`…), radii as numbers; bind fills, strokes and radii to them (`variable.bind`), never paste
  hex. A file that already has its own colour system keeps it: restyle it onto this one only when asked.
- **Faces.** Check each family with `text.fonts {family}`. A missing one: say so in one line and take the nearest
  installed face of the same class (display-heavy); never swap silently. Make text styles for display, body, labels
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

A print shop's material: a warm off-white sheet, warm black ink, Bowlby One SC capitals over Sofia Sans, hot pink and lime fills, every raised surface edged in a thick white die-cut on a hard offset shadow. It feels loud and handmade because the depth is printed and the colours are fills, never tints. It is not a soft pastel shop with blurred shadows, and not a cartoon toy page.

### Tokens

```css
:root {
  --color-paper: #F5F0E7; --color-paper-2: #EFE6D8; --color-paper-3: #FFFDF8;
  --color-ink: #1B1813; --color-ink-2: #312D27; --color-muted: #6A6159;
  --color-rule: #E4DCCF; --color-white: #FEFDFB;
  --color-accent: #D3036A; --color-accent-deep: #B30057; --color-accent-2: #CAE649; --color-slot: #FBE9EF;
  --color-accent-ink: #FEFDFB; --color-focus: #D3036A;
  --font-display: "Bowlby One SC", "Arial Black", sans-serif; --font-body: "Sofia Sans", ui-sans-serif, system-ui, sans-serif;
  --font-outlier: "Sofia Sans", ui-sans-serif, system-ui, sans-serif;
  --radius-card: 18px; --radius-pill: 999px; --rule-hair: 1px; --rule-bar: 2px;
  --shadow-card: 5px 6px 0 var(--color-ink); --shadow-press: 1px 1px 0 var(--color-ink);
  --tracking-display: 0.005em; --display-weight: 400;
}
```

Two colourways, stated in the stamp (`sticker: sheet`).

| Colourway | Paper, ink, fills |
| --- | --- |
| `sheet` (default) | the block above |
| `vinyl` | ground `#1B1813`, cards `#27221C`, ink `#F5F0E7`, rule `#3A342C`; pink and lime unchanged, the borders still white |

### Type

- **Display:** Bowlby One SC 400, capitals only by design, `--tracking-display`, line-height 1.02. It is wide and heavy, so the `h1` caps at 4.5rem and section heads at 3.25rem. Never a paragraph.
- **Figures:** prices, counts and step numbers set in Bowlby, and a lone figure on a fill may run to 12rem; it is the loudest thing the theme owns, so one a screen.
- **Body:** Sofia Sans 400 and 600, line-height 1.5, `tabular-nums`.
- **Labels, tags, captions, table heads:** Sofia Sans 700 a step smaller, sentence case, untracked, `--color-muted`. No third face: the outlier token is Sofia Sans.

### Surfaces

- The die-cut: a raised surface (a card, a fill that holds a fact, a tag, a photograph, the primary control) carries a 6px `--color-white` border and `--shadow-card`, a hard offset with no blur. Surfaces that are the sheet itself (a table, a band) stay borderless, parted by the dashed rule.
- A raised surface may tilt between -6 and 6 degrees, never all one way; tables and inputs stay square.
- Radii: `--radius-card` on cards, 22px on photographs, pills on controls and tags; a `--rule-bar` dashed `--color-rule` is the divider and the edge of a drop zone.
- Bands: a `--color-paper-2` band, a `--color-ink` band with paper type, or one lime field with ink type; two a page at most.
- Photographs: the product in use or held to the lens, close, colour kept loud; 22px radius inside the white die-cut, one a screen tilted 3 degrees or less. A tag may overlap a corner with a fact; type never sits on a picture.
- No texture, no gradient behind type: depth is the hard offset alone.

### Range

- **Facts as die-cut fills:** a Bento whose tiles are pink, lime, ink and white fills, each one fact in Bowlby with one Sofia line, edged white on the hard shadow and tilted a degree or two in alternate directions; the lead tile carries the lone figure.
- **Steps as stuck-down cards:** three or four `<ol>` cards in a row, the numeral in Bowlby on a lime disc, the cards tilted against each other and overlapping the dashed rule they sit on.
- **A working control on the lime field:** a stepper, a running total in Bowlby and a bar that fills toward a threshold the prompt gave, on a white die-cut card beside a dashed price ladder.
- **A statement in Bowlby on the ink band**, ten columns wide, with one pink or lime tag stuck across its corner carrying the fact it argues.

### Controls

- The control pair: a pink pill with a 5px white ring and `--shadow-card`, beside a ghost pill with an inset 2px ink border. Chips are pills with a 2px inset rule, the chosen one ink-filled.
- Links are ink with a pink underline on hover; inputs take a 2px ink edge at `--radius-card`.
- Colour in thirds: pink for the fills that act (the primary, a price), lime for the fills that mark (a tag, a count, a highlight), ink for the type.

### Motion

Sticker physics: a hover lifts a clickable raised surface 2px and turns it a degree; a press pushes it onto its shadow. `--dur-micro` on `--ease-out`, nothing on scroll.

### Voice

Cheerful and exact: the price, the quantity, the size, the ship day. It sounds like the person at the cutter.

### Do-nots

- Never a soft blurred drop under a raised surface; the shadow is a hard offset or there is no shadow.
- Never a die-cut border thinner than 4px, or in any colour but white.
- Never pink text on the paper; pink is a fill with white on it.
- Never a drawn sticker, mascot or doodle; the die-cut edges a real surface, a fact or a photograph, never a shape drawn to stand for a design.
- Never a photograph that only stands near the subject (a bottle, a stapler, a pencil pot); without the product's own pictures, the fills carry the page.

### Build hint

```css
h1, h2, h3 { font-family: var(--font-display); font-weight: 400; letter-spacing: var(--tracking-display); line-height: 1.02; }
h1 { font-size: min(var(--text-display), 4.5rem); } h2 { font-size: min(var(--text-section), 3.25rem); }
.diecut { border: 6px solid var(--color-white); border-radius: var(--radius-card); box-shadow: var(--shadow-card); }
.diecut--photo { border-radius: 22px; overflow: hidden; background: var(--color-slot); }
.btn { display: inline-flex; align-items: center; height: 52px; padding: 0 var(--space-lg); border-radius: var(--radius-pill); font-weight: 700; font-size: var(--text-md); color: var(--color-ink); box-shadow: inset 0 0 0 2px var(--color-ink); }
.btn--primary { background: var(--color-accent); color: var(--color-accent-ink); box-shadow: 0 0 0 5px var(--color-white), 5px 6px 0 var(--color-ink); transition: translate var(--dur-micro) var(--ease-out), box-shadow var(--dur-micro) var(--ease-out); }
.btn--primary:hover { background: var(--color-accent-deep); }
.btn--primary:active { translate: 4px 5px; box-shadow: 0 0 0 5px var(--color-white), var(--shadow-press); }
.fill { border: 6px solid var(--color-white); border-radius: var(--radius-card); box-shadow: var(--shadow-card); background: var(--color-accent); color: var(--color-accent-ink); }
.rule { border-top: var(--rule-bar) dashed var(--color-rule); }
::selection { background: var(--color-accent-2); color: var(--color-ink); }
```
