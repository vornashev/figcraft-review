---
name: hallmark-bloom
description: "Bloom: warm off-white paper with grain and a generated working grid, two quiet terracotta blooms, warm umber ink, Ranade with one roman Gambarino figure, rubber and cased parts lit from above, part tones on rounded clips. Fits: generative, ai creative, music, song, video, image, voice, art, make, create, compose, render, imagine, prompt, creative studio, playground, expressive, warm, daylight, consumer creative, portrait, headshot, selfie, retouch"
metadata:
  origin: hallmark
  category: themes
  group: style
  mode: manual
  title: Bloom
  summary: атмосферный, светлый, уверенный акцент
  preview: "#F9F4EE #F3ECE4 #221510 #AF4529 #C18154 · Ranade"
---
# Bloom — a Hallmark style

The designer chose this style for the chat. A style is a material: paper, ink, faces, rules, radius, depth, controls
and voice. It is never a layout. It was written for web pages in CSS; in FigCraft:

- **Tokens become the file's variables.** Look at the file's variables first (`variable.export`). With no colour
  collection for this style, make one named «Bloom»: the `--color-*` tokens as colour variables without the prefix
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

Daylight on a working sheet: warm off-white paper with a faint grain, the medium's own grid (a piano roll, a timeline, a ruler) printed into the ground and fading out from the stage, umber ink, Ranade with one roman Gambarino moment. The making happens on the grid in rounded clips; the parts you touch are physical: a rubber cap in a bezel, cases slid from a stack. It is not a dark generative canvas with neon glows, not a cream editorial page, not a terracotta poster.

### Tokens

```css
:root {
  --color-paper: #F9F4EE; --color-paper-2: #F3ECE4; --color-paper-3: #EBE1D8;
  --color-ink: #221510; --color-ink-2: #3A2D27; --color-muted: #6A5E56;
  --color-rule: #DED6CE; --color-sheet: #FDFAF6;
  --color-accent: #AF4529; --color-accent-2: #C18154; --color-accent-soft: #AF45291C;
  --color-accent-ink: #FEF9F4; --color-focus: #AF4529;
  --lane-1: #765E4E; --lane-2: #8F433B; --lane-3: #CA9246; --lane-4: #BD7981;
  --grid-16: #22151009; --grid-beat: #22151013; --grid-bar: #22151026; --grid-row: #2215100B;
  --rubber: #B84930; --rubber-hi: #D17652; --rubber-lo: #872E21;
  --umber: #3B2921; --bezel: #EDE5DD; --case: #EFE8E1;
  --hi: #FFFDF9BF; --shade-1: #22151014; --shade-2: #22151029; --shade-3: #47221547;
  --font-display: "Ranade", ui-sans-serif, system-ui, sans-serif; --font-body: var(--font-display);
  --font-outlier: "Gambarino", Georgia, serif; --font-code: "Geist Mono", ui-monospace, monospace;
  --radius-card: 18px; --radius-inner: 10px; --radius-clip: 6px; --radius-pill: 999px; --rule-hair: 1px;
  --shadow-card: 0 1px 2px #2215100F, 0 18px 36px -18px #22151042;
  --shadow-lift: 0 2px 4px #22151012, 0 36px 72px -32px #833F2757;
  --tracking-display: -0.024em; --display-weight: 600;
}
```

### Type

- **Display:** Ranade 600 for every head, `--tracking-display`, line-height 1.04 to 1.08, sentence case, one colour: the ink.
- **Body:** Ranade 400 at 17 to 18px, line-height 1.55; 500 for labels and controls. Three weights in all.
- **The serif moment:** Gambarino 400, roman, once a page: one figure at 160px or more, or one lede. Never a head, never italic.
- **Labels:** Ranade 500 a step smaller, sentence case, `--color-muted`. Geist Mono only for a ruler's fine numerals and timecodes inside the built product.

### Surfaces

- The ground is the medium's grid in CSS: stacked linear gradients for bars, beats, sixteenths and rows (black-key rows tinted every octave for a piano roll), on `--color-sheet` behind the stage, then continued faintly past it and masked to fade out radially. The grid returns in small crops beside steps and at the close.
- On the grid, the work: four part lanes in `--lane-*` tones as rounded clips (`--radius-clip`, a tinted gradient, an inset hairline in the lane tone, a lit top edge) carrying bar waveforms or notes; a hairline playhead; a key strip and a fine-numeral ruler.
- Texture is generated: a 180px feTurbulence grain at 5% over the paper, and at 30% soft-light on rubber.
- Light from above on every part. Two warm blooms stay, quieter: `--color-accent` near 8% top right, `--color-accent-2` near 5% bottom left, fixed.
- Raised warm surfaces, never hairline boxes: `--shadow-card`, `--shadow-lift` for the one that matters. Two bands at most, never terracotta.
- Photographs: daylight at home, hands, an instrument by a window; never a studio at night.

### Range

- **The input becoming the output on one grid:** what the user gives (a hum, a sketch, a line) drawn as a trace that settles onto the grid, the result growing in lanes beneath, and Play really plays it.
- **Choices as cased spines:** options as a stack of cases (a colour band striped with light, a card label, pips for its parts); the chosen one slides out and the grid re-arranges.
- **One figure in the serif** beside three steps, each with a small crop of the grid.
- **The result as one clip** on the grid at the close, downloadable.

### Controls

- The primary is a rubber cap in a recessed bezel: a domed `--rubber` radial gradient lit from the top, grain, set in a `--bezel` well with an inset shade; it sits at the left of a `--color-sheet` pill with its label, and its ring breathes while the product listens. Press sinks it 1px.
- Secondary: a sheet pill with a shade ring and a lit top edge, or an `--umber` pill.
- Links in terracotta, underlined on hover; inputs 52px pills with a 1px `--color-muted` edge.

### Motion

Once, in view: the input draws in (about 3 s), notes settle, the playhead glides home, lanes grow. Transforms and opacity, paused off screen. Reduced motion or no script: the finished arrangement, playhead at the start. The blooms never move.

### Voice

Warm, daylight, specific: the verb (hum, make, listen), the output (song, part, scene), and where.

### Do-nots

- Never a dark canvas, a neon glow or a third bloom.
- Never a terracotta field or card; terracotta is rubber, a link, a lane.
- Never a grid at full strength across a whole section; it fades from the stage.
- Never an italic serif, and never the serif in a head or in two places.

### Build hint

```css
h1, h2, h3 { font-weight: var(--display-weight); color: var(--color-ink); }
.roll { --beat: 40px; --row: 14px; background-color: var(--color-sheet); background-image: linear-gradient(to right, var(--grid-bar) 1px, transparent 1px), linear-gradient(to right, var(--grid-beat) 1px, transparent 1px), linear-gradient(to right, var(--grid-16) 1px, transparent 1px), linear-gradient(to bottom, var(--grid-row) 1px, transparent 1px); background-size: calc(var(--beat) * 4) 100%, var(--beat) 100%, calc(var(--beat) / 4) 100%, 100% var(--row); }
.clip { --c: var(--lane-1); border-radius: var(--radius-clip); background: linear-gradient(color-mix(in oklab, var(--c) 18%, var(--color-sheet)), color-mix(in oklab, var(--c) 28%, var(--color-sheet))); box-shadow: inset 0 0 0 1px color-mix(in oklab, var(--c) 42%, transparent), inset 0 1px 0 var(--hi); }
.rec { border-radius: 50%; background: radial-gradient(circle at 50% 30%, var(--bezel), var(--color-paper-3)); box-shadow: inset 0 2px 3px var(--shade-2), 0 1px 0 var(--hi); }
.rec__cap { border-radius: 50%; background: radial-gradient(120% 110% at 50% 18%, var(--rubber-hi), var(--rubber) 48%, var(--rubber-lo)); box-shadow: inset 0 1px 0.5px var(--hi), 0 5px 9px -3px var(--shade-3); }
.pill { border-radius: var(--radius-pill); background: var(--color-sheet); box-shadow: 0 0 0 1px var(--shade-1), 0 8px 18px -10px var(--shade-2), inset 0 1px 0 var(--hi); font-weight: 500; }
a { color: var(--color-accent); text-underline-offset: 0.2em; }
```
