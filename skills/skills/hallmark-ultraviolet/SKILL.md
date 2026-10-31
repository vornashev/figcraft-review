---
name: hallmark-ultraviolet
description: "Ultraviolet: lavender paper or a violet-black night, Outfit set lowercase over Onest, hairline pills, one saturated violet in two strengths, photographs pulled into the violet. Fits: music, audio, stems, remix, dj, producer, player, streaming, tempo, playlist, creator, app, consumer, lowercase, violet, sound, beats, recording studio"
metadata:
  origin: hallmark
  category: themes
  group: style
  mode: manual
  title: Ultraviolet
  summary: минимализм, светлый, уверенный акцент
  preview: "#F0ECFA #E7E1F6 #131019 #6B2AE3 · Outfit"
---
# Ultraviolet — a Hallmark style

The designer chose this style for the chat. A style is a material: paper, ink, faces, rules, radius, depth, controls
and voice. It is never a layout. It was written for web pages in CSS; in FigCraft:

- **Tokens become the file's variables.** Look at the file's variables first (`variable.export`). With no colour
  collection for this style, make one named «Ultraviolet»: the `--color-*` tokens as colour variables without the prefix
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

A producer's tool in one pigment: a paper tinted the same hue as the ink, one saturated violet in two strengths, Outfit set lowercase on every head and control, pills throughout, depth held to a hairline, photographs pulled into the violet. It reads quick, exact and young without raising its voice. It is not a purple-gradient startup page and not a neon club flyer.

### Tokens

```css
:root {
  --color-paper: #F0ECFA; --color-paper-2: #E7E1F6; --color-paper-3: #DED6EF;
  --color-ink: #131019; --color-ink-2: #2B2636; --color-muted: #5C5270;
  --color-rule: #CEC5E1; --color-rule-2: #A295CB;
  --color-accent: #6B2AE3; --color-accent-deep: #571DBC; --color-accent-soft: #D4C7FF;
  --color-accent-ink: #F6F4FB; --color-focus: #6B2AE3;
  --font-display: "Outfit", ui-sans-serif, system-ui, sans-serif; --font-body: "Onest", ui-sans-serif, sans-serif;
  --font-outlier: "JetBrains Mono", ui-monospace, monospace;
  --radius-card: 16px; --radius-pill: 999px; --rule-hair: 1px;
  --shadow-card: 0 1px 2px #1310190F;
  --tracking-display: -0.03em; --display-weight: 500;
}
```

Three colourways, set once per page and stated in the stamp (`ultraviolet: lavender`). A nocturnal prompt takes `night`, which may carry one band in the `record` colours.

| Colourway | Paper, ink, accent |
| --- | --- |
| `lavender` (default) | the block above |
| `record` | ground `#6B2AE3`, ink `#F0ECFA`, the accent turns white `#FCFBFF` with violet text on it, rule `#A793F4` |
| `night` | ground `#090811`, paper-2 `17.5% 0.025 290`, paper-3 `21% 0.03 290`, ink `92% 0.04 300`, ink-2 `80% 0.05 300`, muted `68% 0.06 300`, rule `28% 0.04 290`, rule-2 `44% 0.07 292`, accent `55% 0.25 290`, deep `48% 0.24 290`, soft `36% 0.09 293`, focus `62% 0.22 290` |

### Type

- **Display:** Outfit 500, lowercase, `--tracking-display`, line-height 1. Lowercase is the material: heads, nav links, buttons and pills never carry a capital.
- **Figures:** Outfit 300 at `--text-display` and over, lowercase units beside them in the label voice, tabular; the thin geometric numeral is the one place the display goes light.
- **Body:** Onest 400, sentence case, line-height 1.55. Prose is the one place a capital appears.
- **Labels, captions, table heads:** Outfit 500 a step smaller, lowercase, untracked, in `--color-muted`. Mono only inside code.

### Surfaces

- Hairlines: 1px `--color-rule` between rows; pills and outlined controls carry 1.5px of `--color-rule-2`. No borders on cards; a surface is a step to `--color-paper-2`.
- Radius: `--radius-pill` on every control and tag, 16px on surfaces, screens and photographs; nothing square.
- Depth: none on paper, the whisper `--shadow-card` under a raised surface. No blur, no glow, no gradient.
- Bands: a `--color-paper-2` band, an ink band, or one violet field in the `record` colours; two a page at most.
- The product sits plain on `--color-paper-2` or bleeds off its edge, never in a bezel; a waveform is real line work, its played part in the violet, its rest in `--color-accent-soft`.
- Photographs: the night around the music (hands on a mixer, a booth, a crowd lit from the stage seen from behind), tinted violet, 16px radius, a 1px inset ring of ink at 8%; type over one only on an ink scrim. Faces never lead. No texture.

### Range

- **Lanes as the picture:** the product's own waveforms across ten or twelve columns, one stem to a row under hairlines, a bar ruler above in the label voice; the played part violet, the rest soft. It carries a section with no photograph and no frame.
- **Figures in light Outfit:** the prompt's real numbers at display size in the 300, parted by hairlines, one of them in the violet, each unit lowercase beside it.
- **A table of uses:** a full-width Table in lowercase, the use at title size, the stems it takes as small pills, one line of what you hear; a price list takes the same rows.
- **The record field:** one band in the violet holding a working drop zone or a form, the white pill its only fill.

### Controls

- A violet-filled pill (`--color-accent-ink` on `--color-accent`, `--color-accent-deep` on hover) beside an inset-outlined one (1.5px of `--color-ink`), both Outfit 500 lowercase; inside a violet field the filled pill turns white with violet text.
- Links underline in violet on hover; inputs are pills with a 1.5px `--color-rule-2` inset ring that turns ink on focus. Toggles (solo, mute) are small pills that fill violet when pressed.
- The violet is one pigment: one filled control, the focus ring, a link's hover, a progress fill, a played waveform, one figure.

### Motion

Quick and dry: `--dur-micro` colour transitions on pills over `--ease-out`, a lane that dims or lights as a toggle moves, and at most one settle on load over `--dur-long` from an already-visible default. Nothing spins or loops.

### Voice

Lowercase, short, exact: the stem, the bar, the minute, the track count. It talks like a producer, not a label.

### Do-nots

- Never a capital in a head, a nav link or a button.
- Never a second chromatic colour, in a photograph either; the violet is the only one.
- Never a purple-to-pink gradient, a mesh behind text or a glow.
- Never square controls or 4px radii; Ultraviolet is round.

### Build hint

```css
h1, h2, h3 { font-weight: 500; line-height: 1; text-transform: lowercase; letter-spacing: var(--tracking-display); }
.figure { font: 300 var(--text-display)/0.9 var(--font-display); font-variant-numeric: tabular-nums; }
.btn, .pill { display: inline-flex; align-items: center; border-radius: var(--radius-pill); font: 500 var(--text-sm)/1 var(--font-display); text-transform: lowercase; transition: background-color var(--dur-micro) var(--ease-out); }
.btn { min-height: 48px; padding: 0 var(--space-lg); } .pill { padding: var(--space-xs) var(--space-md); box-shadow: inset 0 0 0 1.5px var(--color-rule-2); }
.btn--primary { background: var(--color-accent); color: var(--color-accent-ink); }
.btn--primary:hover { background: var(--color-accent-deep); }
.btn--secondary { box-shadow: inset 0 0 0 1.5px currentColor; color: inherit; }
.well { background: var(--color-paper-2); border-radius: var(--radius-card); }
.band--violet { background: var(--color-accent); color: var(--color-accent-ink); }
.wave__rest { fill: var(--color-accent-soft); } .wave__played { fill: var(--color-accent); }
::selection { background: color-mix(in oklab, var(--color-accent) 25%, transparent); }
```
