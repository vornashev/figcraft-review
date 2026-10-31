---
name: hallmark-halftone
description: "Halftone: butter-cream stock, brown-black ink, Ultra over Chivo, three-pixel ink rules and square wells, one vermilion printed solid and through a dot screen, photographs in full colour. Fits: drinks, soda, food brand, print shop, zine, magazine, record label, packaging, campaign, label, bottle, can, screen print, bold, one colour, retail, craft, loud, fruit, snack"
metadata:
  origin: hallmark
  category: themes
  group: style
  mode: manual
  title: Halftone
  summary: игривый, светлый, уверенный акцент
  preview: "#F9F3DB #F1E6C4 #2D160F #D01A00 · Ultra"
---
# Halftone — a Hallmark style

The designer chose this style for the chat. A style is a material: paper, ink, faces, rules, radius, depth, controls
and voice. It is never a layout. It was written for web pages in CSS; in FigCraft:

- **Tokens become the file's variables.** Look at the file's variables first (`variable.export`). With no colour
  collection for this style, make one named «Halftone»: the `--color-*` tokens as colour variables without the prefix
  (`paper`, `ink`, `accent`…), radii as numbers; bind fills, strokes and radii to them (`variable.bind`), never paste
  hex. A file that already has its own colour system keeps it: restyle it onto this one only when asked.
- **Faces.** Check each family with `text.fonts {family}`. A missing one: say so in one line and take the nearest
  installed face of the same class (slab-serif); never swap silently. Make text styles for display, body, labels
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

A loud one-colour print voice: butter-cream stock, brown-black ink, a fat Ultra slab for heads, Chivo for everything else, 3px ink rules and one vermilion that prints solid on controls and as a dot screen on a band or a well. Photographs are the only full colour, close and bright like a label's product shot. It feels screen-printed because there is one ink and its dots fade from solid to nothing, not because anything is drawn. It is not a comic-book pop-art page and not a pastel snack brand.

### Tokens

```css
:root {
  --color-paper: #F9F3DB; --color-paper-2: #F1E6C4; --color-paper-3: #E5D5AB;
  --color-ink: #2D160F; --color-ink-2: #492D24; --color-muted: #694A3D;
  --color-rule: #D2C2A6;
  --color-accent: #D01A00; --color-accent-deep: #A90000; --color-accent-ink: #FAF5E5; --color-focus: #A90000;
  --color-dot: var(--color-accent); --halftone-size: 12px; --halftone-dot: 3px;
  --font-display: "Ultra", ui-serif, Georgia, serif; --font-body: "Chivo", ui-sans-serif, sans-serif;
  --radius-card: 0; --radius-input: 3px; --radius-pill: 999px; --rule-hair: 1px; --rule-bar: 3px;
  --shadow-card: none;
  --tracking-display: 0.005em; --display-weight: 400;
}
```

Committed: the spot carries the screen, the controls and a field band. Three stocks, stated in the stamp (`halftone: cream`).

| Stock | Paper and ink | The spot |
| --- | --- | --- |
| **Cream and vermilion** (default) | the tokens above | `#D01A00` |
| **Lemon on black** | `#17130F` under `#F7F2E3` | yellow `#FBD530` with dark ink on it |
| **Blood orange** | the colour goes into the stock: `#F97C3D` under plum `#371210` | the plum ink is also the spot, so the dots print dark |

### Type

- **Display:** Ultra 400, its only weight, roman, sentence case, line-height 1.08 (Ultra's descenders touch the next line any tighter), `--tracking-display`; one colour per head. Ultra's figures are its loudest letters: a number at 200px and over may print solid in the spot, tracked -0.02em, line-height 0.9 when it stands alone on its line.
- **Body:** Chivo 400, 17px, line-height 1.55, in `--color-ink-2`; Chivo 700 on controls and on the names in a label panel.
- **Labels, tags, table heads, captions:** Chivo 500 a step smaller, sentence case, untracked; the 3px rules give them authority. No mono.

### Surfaces

- Rules do the work of borders: `--rule-bar` in ink across the top of a section, a table or a list, `--rule-hair` in `--color-rule` between rows.
- A well is the one boxed surface: `--color-paper-2` inside a `--rule-bar` ink border, square, with nothing boxed inside it. No shadow anywhere.
- Radii: 3px on buttons and inputs, a full pill on a chip; wells, tags and photographs are square.
- Bands: `--color-paper-2`, a spot field with cream type knocked out of it, or `--color-ink` with cream text. Two a page at most. `--color-accent-deep` is the spot pressed: hover, the focus ring and any spot type under 24px.
- Photographs: the product and what goes into it, close and bright (a cut lemon, a knuckle of ginger, bubbles in a glass), hard daylight on a plain light ground. The page's only full colour; square, a 1px ink hairline, a caption beneath naming what is in it. The spot never tints a picture.
- The screen (`texture.md` § Halftone): a `--halftone-dot` dot on a `--halftone-size` cell in the spot, masked to fade from solid to nothing, on a band or a well; one screened field per section, never under or across type or a photograph.

### Range

- **A figure as a poster:** one real number (the calories, the size, the price) in Ultra at 240px and over, solid spot on the cream, its unit and its one line in Ultra ink at section size beside it.
- **The label as a panel:** a 3px ink rule over full-width rows, the name in Chivo 700, the value in Ultra at item size, hairlines between, the way a can's back reads; never shrunk into a box.
- **The order on the spot:** a spot band with a cream knockout head, a stepper and its running total in Ultra, the screen fading in from one edge behind the empty side.
- **A statement knocked out:** one blunt sentence in Ultra at display size, cream out of the ink or the spot, nothing else on the field but its links.

### Controls

- A spot-filled button in Chivo 700 at 3px beside a plain `--rule-bar` spot underline with no box.
- Links in ink with a spot underline; inputs at 3px, 1px ink border.
- The spot sits on controls, the screen, a field band and the focus ring; never on body type.

### Motion

State only, `--dur-short` on `--ease-out`: a button darkens one step. The screen never moves.

### Voice

The label: the fruit, the calories, the size of the can, the price of the box. Blunt, sweet and specific; never a lifestyle.

### Do-nots

- Never a second ink; one spot does dots, buttons and fields, and a blue link on the cream is a different printer.
- Never a gradient that is not dots; a fade is a screen from solid to nothing.
- Never dots under or across type or a photograph.
- Never a synthesised bold Ultra, a soft shadow or a rounded well.
- Never spot type smaller than a section head on the cream; it prints weak, so small spot type takes the deep spot.

### Build hint

```css
h1, h2, h3 { font-weight: var(--display-weight); line-height: 1.08; }
.poster { font: 400 clamp(10rem, 22vw, 20rem)/0.9 var(--font-display); letter-spacing: -0.02em; color: var(--color-accent); font-variant-numeric: tabular-nums; }
.btn { padding: var(--space-md) var(--space-lg); border-radius: var(--radius-input); font: 700 var(--text-sm) var(--font-body); background: var(--color-accent); color: var(--color-accent-ink); }
.btn--secondary { background: none; color: var(--color-ink); padding: var(--space-md) 0 var(--space-xs); border-radius: 0; border-bottom: var(--rule-bar) solid var(--color-accent); }
.well { border: var(--rule-bar) solid var(--color-ink); background: var(--color-paper-2); }
.ruled { border-top: var(--rule-bar) solid var(--color-ink); } .ruled > * { border-bottom: var(--rule-hair) solid var(--color-rule); }
.photo { outline: var(--rule-hair) solid var(--color-ink); outline-offset: calc(-1 * var(--rule-hair)); }
.halftone { position: relative; isolation: isolate; }
.halftone::before { content: ""; position: absolute; inset: 0; z-index: -1; pointer-events: none;
  background: radial-gradient(var(--color-dot) var(--halftone-dot), transparent calc(var(--halftone-dot) + 0.5px)) 0 0 / var(--halftone-size) var(--halftone-size);
  mask: linear-gradient(110deg, transparent 45%, var(--color-ink) 95%); }
::selection { background: color-mix(in oklab, var(--color-accent) 30%, transparent); }
```
