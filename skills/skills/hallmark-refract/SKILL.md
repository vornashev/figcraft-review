---
name: hallmark-refract
description: "Refract: sunlit white plaster with real light falling across it, water caustics or prism dispersion rendered live, deep pool-blue ink, Funnel Display at a light weight over Funnel Sans, clear surfaces that cast tinted shadows, one water signal. Fits: pool, lido, swim, spa, hotel, resort, water, skincare, sunscreen, eyewear, glass, optics, light, daylight, architecture, interiors, studio, wellness, bathhouse, summer, clean, calm, product launch, hardware"
metadata:
  origin: hallmark
  category: themes
  group: style
  mode: manual
  title: Refract
  summary: атмосферный, светлый, сдержанный акцент
  preview: "#FAF9F5 #F4F3EF #0E1F2C #006C9C · Funnel Display"
---
# Refract — a Hallmark style

The designer chose this style for the chat. A style is a material: paper, ink, faces, rules, radius, depth, controls
and voice. It is never a layout. It was written for web pages in CSS; in FigCraft:

- **Tokens become the file's variables.** Look at the file's variables first (`variable.export`). With no colour
  collection for this style, make one named «Refract»: the `--color-*` tokens as colour variables without the prefix
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

White plaster in strong sun, with light doing the decorating: a net of water caustics moving across the ground, or a prism throwing a spectrum and its bright cusps over the page. Everything else is quiet: deep pool-blue ink, Funnel Display at a light weight, clear surfaces whose shadows carry a tint of the light that passed through them. It feels like a cool room on a hot afternoon. It is not a rainbow gradient, not frosted glass on a blur, not a blue tech landing page.

### Tokens

```css
:root {
  --color-paper: #FAF9F5; --color-paper-2: #F4F3EF; --color-paper-3: #EBEAE4;
  --color-ink: #0E1F2C; --color-ink-2: #2E3F4F; --color-muted: #576570;
  --color-rule: #D7DDE1; --color-rule-2: #E6EAED;
  --color-accent: #006C9C; --color-accent-hi: #005A8B; --color-accent-ink: #FCFCF9; --color-accent-soft: #DAF0F7; --color-focus: #007FB9;
  --color-shade: #ACDAE4; --color-shade-2: #77B6CA; --color-light: #FFFEFB;
  --spec-1: #FF9079; --spec-2: #EDE361; --spec-3: #52DFBF; --spec-4: #6F8BED;
  --color-slot: #ACDAE4;
  --edge-light: inset 0 1px 0 #FFFFFFE6, inset 0 0 0 1px #FFFFFF8C;
  --shadow-card: 18px 28px 48px -26px #13748D61, 2px 3px 6px -2px #294D5E1F;
  --shadow-cast: 28px 40px 70px -30px #0091A673;
  --font-display: "Funnel Display", ui-sans-serif, system-ui, sans-serif; --font-body: "Funnel Sans", ui-sans-serif, system-ui, sans-serif;
  --radius-card: 22px; --radius-inner: 12px; --radius-pill: 999px; --rule-hair: 1px;
  --tracking-display: -0.032em; --display-weight: 400;
}
```

Two dials, stated in the stamp (`refract: water/pool`). Two Refract pages in one run differ on both.

| Dial | Options |
| --- | --- |
| **Light** (the generated ground) | `water` (default): caustics from a surface of moving water, a bright net over an aqua shade. `glass`: sun through a glazed window, the pane edges split warm and cool and a prism's fan crossing the patch, falling over the product as well as the ground, slow as the sun |
| **Colourway** | `pool` (default) as above. `noon`: ink `#13161B`, accent near-black, the spectrum the only colour |

### Type

- **Display:** Funnel Display 400 (300 for a figure set at statement size), `--tracking-display`, line-height 1.02, sentence case, one colour. Heads stay calm; the light is the loud part.
- **Body:** Funnel Sans 400 at 17px, line-height 1.6, `--color-ink-2`; leads a step up in `--color-muted`.
- **Labels, table heads, times:** Funnel Sans 500 a step smaller, sentence case, `tabular-nums` on every figure. Never mono, never tracked capitals.

### Surfaces

- **The light:** one generated canvas or shader, never a photograph of a texture and never a gradient blob. In `water` the shade is `--color-shade` with the net in `--color-light` and a faint split into `--spec-*` at the brightest seams; in `glass` the ground stays paper and bands of `--spec-*` fall at a low angle with a white cusp along one edge. The light lands on the side of the hero away from the head and fades to paper under the text, so the head always sits on plain paper.
- **Clear surfaces:** panels are white at 72 to 86% over the light with `--edge-light`, never blurred; their shadow falls down and right from one sun (`--shadow-card`), tinted by the water. A second, larger cast (`--shadow-cast`) only under the one lead object on a page.
- **Rules:** hairlines in `--color-rule`, horizontal only, in tables and lists. Radius `--radius-card` on panels, `--radius-inner` inside them, pills for controls.
- **Bands:** paper and paper-2; one band may take the light again (the close or a statement), never more than two lit grounds a page.
- **Photographs:** bright, sunlit, hard shadows, water or white architecture or the product in sun; no people posing. Square corners on full-bleed, `--radius-card` inside the container. No duotone.

### Range

- **Times to book as lanes:** when the visitor picks a session, the sessions as long ruled rows, the time in display figures, a status pill at the right edge, the next open row lit by a thin band of the light behind it.
- **A figure in sun:** one number at statement size in Funnel Display 300 with the light falling across the space beside it, its unit and source in one muted line.
- **The day as light:** a strip of hours as slim bars whose height is the light or the demand, the present hour marked by an accent dot, the rest in `--color-shade`.
- **The product on the table:** the product's real screen as a clear panel lying in the light, its cast shadow tinted, one working control that moves the light itself.

### Controls

- Primary pill: `--color-accent` under `--color-accent-ink`, a white inset top edge, 48px; hover darkens to `--color-accent-hi`. Secondary pill: white at 80% with `--edge-light` and a hairline.
- Inputs are white wells with a hairline and `--radius-inner`; focus ring in `--color-focus`.
- The accent sits on the primary, focus, the present marker and links on hover; the spectrum lives only in the light.

### Motion

Water moves at swimming-pool speed (a full pattern change in about 12 seconds); glass drifts as the sun does, a band crossing in 60 seconds. Panels lift 2px on hover with their shadow lengthening. Light pauses off screen. Reduced motion: one still frame of the light.

### Voice

Bright and plain, a little sensory: the temperature, the hour, what the light does.

### Do-nots

- Never a rainbow on type, a gradient button or a spectral border on more than one object.
- Never frosted glass or a backdrop blur; clear surfaces stay clear.
- Never the light under running text, and never two lit grounds in a row.
- Never a grey drop shadow; every shadow carries the light's tint and falls from one sun.

### Build hint

```css
h1, h2, h3 { font-family: var(--font-display); font-weight: var(--display-weight); letter-spacing: var(--tracking-display); line-height: 1.02; }
.clear { background: color-mix(in oklab, var(--color-light) 80%, transparent); border-radius: var(--radius-card); box-shadow: var(--edge-light), var(--shadow-card); }
.btn { min-height: 48px; padding: 0 var(--space-lg); border: 0; border-radius: var(--radius-pill); background: var(--color-accent); color: var(--color-accent-ink); font: 500 var(--text-md)/1 var(--font-body); box-shadow: var(--shadow-card); transition: background var(--dur-short) var(--ease-out); }
.btn:hover { background: var(--color-accent-hi); }
.btn--clear { background: color-mix(in oklab, var(--color-light) 80%, transparent); color: var(--color-ink); box-shadow: var(--edge-light), var(--shadow-card); }
.light { position: absolute; inset: 0; width: 100%; height: 100%; pointer-events: none; -webkit-mask-image: linear-gradient(to right, transparent 30%, var(--color-ink) 62%); mask-image: linear-gradient(to right, transparent 30%, var(--color-ink) 62%); }
```
