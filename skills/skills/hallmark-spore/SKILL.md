---
name: hallmark-spore
description: "Spore: coffee-ground black with a warm grain, parchment ink, Young Serif over Instrument Sans, soft pills and grained wells, photographs lit by lamps and candles, one oyster pink. Fits: grower, mushroom, fungi, farm, food, producer, fermentation, wine, natural wine, wine bar, bottle shop, cellar, preserves, dark, culture, night market, harvest, subscription, small batch"
metadata:
  origin: hallmark
  category: themes
  group: style
  mode: manual
  title: Spore
  summary: атмосферный, тёмный, уверенный акцент
  preview: "#0F0A06 #19120E #EFE7D8 #E89F92 #F6C3BA · Young Serif"
---
# Spore — a Hallmark style

The designer chose this style for the chat. A style is a material: paper, ink, faces, rules, radius, depth, controls
and voice. It is never a layout. It was written for web pages in CSS; in FigCraft:

- **Tokens become the file's variables.** Look at the file's variables first (`variable.export`). With no colour
  collection for this style, make one named «Spore»: the `--color-*` tokens as colour variables without the prefix
  (`paper`, `ink`, `accent`…), radii as numbers; bind fills, strokes and radii to them (`variable.bind`), never paste
  hex. A file that already has its own colour system keeps it: restyle it onto this one only when asked.
- **Faces.** Check each family with `text.fonts {family}`. A missing one: say so in one line and take the nearest
  installed face of the same class (roman-serif); never swap silently. Make text styles for display, body, labels
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

## Genre: atmospheric

The AI-creative and after-dark product page: generative music, video, image, voice, model playgrounds, anything the prompt calls moody, cinematic or nocturnal. A canvas first, then a tool. The deal leans toward this genre's themes, light-paper exceptions included.

## Voice

- **Accent:** one hue, used in the canvas treatment, on focus rings and on small tags; never on display text unless the theme's type names an accented word (Lumen).
- **Layout:** a centred hero is the normal answer when the type is the visual (a Poster or Banner posture); with a visual, it stands beside the text (44c). The canvas is the design and the type sits on it.
- **Motion:** fade only; the atmosphere does the work.
- **Copy:** direct, slightly poetic, specific: *Make a house song about quitting your job.*

## Allowed here

At most two fixed radial blooms on the body, each 20 to 30% of the canvas in size, never animated (gate 29 is loosened this far and no further); the nav pill on a backdrop blur over the canvas, the one glass licence; a centred hero (gate 6b loosened); pill controls with an accent fill; elevated cards by lightness step (`--color-paper-2`, `-3`) instead of hairlines; display up to 6rem.

## Refused here

A coloured glow shadow, a radial spotlight behind the hero, or a mesh gradient (the bloom is the one licence); light sections sneaking into a dark build; a third hue; glass panels or cards; gradient text.

## Chrome that fits

A floating pill on a blur backdrop, an edge-aligned bar, a command palette, a statement footer. Dense link furniture fights the register. Affinities, not assignments.


## The theme

A cellar at night: coffee-ground black warmed toward brown, a warm grain on its wells, parchment Young Serif over Instrument Sans, soft pills, photographs lit only by lamps and candles, and one oyster-mushroom pink. It feels close and handmade because the warmth sits in the ground, the grain, the figures and one soft colour, never in drawn light. It is not a dark-mode template with a glow, nor a wellness label.

### Tokens

```css
:root {
  --color-paper: #0F0A06; --color-paper-2: #19120E; --color-paper-3: #271D17;
  --color-ink: #EFE7D8; --color-ink-2: #D3C9BB; --color-muted: #9D9388;
  --color-rule: #372F28;
  --color-accent: #E89F92; --color-accent-2: #F6C3BA; --color-accent-ink: #0F0A06; --color-focus: #F6C3BA;
  --font-display: "Young Serif", Georgia, serif; --font-body: "Instrument Sans", ui-sans-serif, system-ui, sans-serif;
  --font-outlier: "Instrument Sans", ui-sans-serif, system-ui, sans-serif;
  --radius-card: 14px; --radius-pill: 999px; --rule-hair: 1px;
  --shadow-card: 0 16px 40px #03010166;
  --tracking-display: -0.012em;
  --grain: 0.15; --display-weight: 400;
}
```

One dial, the colourway, stated in the stamp (`spore: cellar`).

| Colourway | Ground | Ink | Accent |
| --- | --- | --- | --- |
| `cellar` (default) | `#0F0A06`, grain screened at 15% | parchment `#EFE7D8` | pink `#E89F92` |
| `lab` | cream `#F1EADC`, grain multiplied at 6% | `#140E09` | pink `#C86556` |
| `head-torch` | `#080504`, grain at 15% | `#F1E7D2` | ochre `#D5A13C` |

### Type

- **Display:** Young Serif 400, `--tracking-display`, line-height 1.02, sentence case, roman, one colour per head. Its one weight is the voice: hierarchy comes from size, never from bolding.
- **Figures:** prices, days, hours and counts are Young Serif, lining, and may run past `--text-display` when one number is the section's reason; a price is the one figure that takes pink.
- **Body:** Instrument Sans 400 and 500, line-height 1.55, in `--color-ink-2`. A second name after a product's (a grape, a vintage, a Latin name) is Instrument Sans italic, the outlier and the only italic.
- **Labels, captions, table heads:** Instrument Sans 500 a step smaller, sentence case, `--color-muted`.

### Surfaces

- 1px `--color-rule` between rows; a 1.5px `--color-ink-2` edge on fields. Nothing else has a border.
- Radii: pills on controls and chips, `--radius-card` on wells and photographs; inputs square.
- Depth is the ground's three steps: paper, a grained `--color-paper-2` well, a `--color-paper-3` band. A state that is live now (tonight, the chosen row) lifts one step and takes a pink chip. `--shadow-card` only under a well that overlaps a photograph.
- Photographs: the place after dark, close: racks, a pour, a candlelit counter, a glass; low warm light into shadow, never flash or daylight. `--radius-card` with a 1px ink ring at 8%; type on one sits on its dark side over a paper scrim at 45 to 65%.
- Grain: the speck grain of `texture.md` § 1, screened at `--grain`, on wells and bands only; never under running text in a column or over a photograph.

### Range

- **One figure as the section:** a count or a price in Young Serif at two to four times `--text-display` on a grained well, its plain label beneath, beside two or three hairline rows that say what the number means.
- **The week as a timetable:** Rows of day names in Young Serif at `--text-title`, the hours beside them, closed days dropped to muted, tonight's row lifted to paper-3 with its pink chip; a head block on columns 1 to 4 beside them.
- **A list or price list:** ruled rows with the name in Young Serif, the second name in italic, the price flush right in pink; set three or five columns deep and it reads as the shelf.
- **A grained band that holds a form:** paper-3 with the speck grain, the price large in pink beside square fields and the pink pill; or a statement in Young Serif at `--text-display` across ten columns.

### Controls

- The pair: a pink-filled pill with `--color-accent-ink` text, lightening to `--color-accent-2` on hover, beside a pill outlined in 1.5px `--color-ink-2`. Chips are pills; the chosen one fills pink.
- Links are parchment with an underline that turns pink on hover; inputs are square with the 1.5px edge and the `--color-focus` ring.

### Motion

State only, in one frame: a chip selects, a row lifts, a pill lightens. Nothing reveals, nothing grows, nothing loops.

### Voice

A maker's log: the name, the day, the hour, the vintage, the price. No wellness, no mystique, no "curated".

### Do-nots

- Never a second hue; a green for "in stock" makes a garden centre.
- Never drawn light as the mood (a beam, a pool, a glow behind a head); the light lives in the photographs.
- Never a neutral or blue-black ground; every dark step tints toward hue 60.
- Never pink running text or a pink outline; pink is a fill, a price or the focus.
- Never photograph after photograph; between two pictures a figure, a timetable or a list in Young Serif.

### Build hint

```css
h1, h2, h3 { font-family: var(--font-display); font-weight: 400; letter-spacing: var(--tracking-display); line-height: 1.02; }
.btn { border-radius: var(--radius-pill); padding: var(--space-sm) var(--space-lg); font-weight: 600; transition: background-color var(--dur-micro) var(--ease-out); }
.btn--primary { background: var(--color-accent); color: var(--color-accent-ink); }
.btn--primary:hover { background: var(--color-accent-2); }
.btn--secondary { background: transparent; color: var(--color-ink); box-shadow: inset 0 0 0 1.5px var(--color-ink-2); }
.well { background: var(--color-paper-2); border-radius: var(--radius-card); }
.figure { font-family: var(--font-display); font-variant-numeric: lining-nums; line-height: 0.86; }
.grained { position: relative; isolation: isolate; }
.grained::after { content: ""; position: absolute; inset: 0; z-index: var(--z-base); border-radius: inherit; pointer-events: none; opacity: var(--grain); mix-blend-mode: screen;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='200' height='200'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='2'/%3E%3CfeColorMatrix values='0 0 0 0 0.6 0 0 0 0 0.55 0 0 0 0 0.45 0 0 0 0.35 0'/%3E%3C/filter%3E%3Crect width='200' height='200' filter='url(%23n)'/%3E%3C/svg%3E"); }
```
