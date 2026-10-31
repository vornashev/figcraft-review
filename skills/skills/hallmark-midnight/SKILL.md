---
name: hallmark-midnight
description: "Midnight: midnight-blue ground to every edge, cool white ink, Mona Sans expanded at 300 over its normal width, square-cut surfaces in lightness steps, photographs as moonlight, one azure signal. Fits: render, 3d, animation, vfx, film, video, frames, pipeline, generative, ai tool, model playground, dark mode, nocturnal, late-night, after-hours, overnight, moody, cinematic, cerebral, calm, technical, midnight"
metadata:
  origin: hallmark
  category: themes
  group: style
  mode: manual
  title: Midnight
  summary: атмосферный, тёмный, уверенный акцент
  preview: "#02071D #071129 #E7F0F9 #6BCBF7 #3483AD · Mona Sans"
---
# Midnight — a Hallmark style

The designer chose this style for the chat. A style is a material: paper, ink, faces, rules, radius, depth, controls
and voice. It is never a layout. It was written for web pages in CSS; in FigCraft:

- **Tokens become the file's variables.** Look at the file's variables first (`variable.export`). With no colour
  collection for this style, make one named «Midnight»: the `--color-*` tokens as colour variables without the prefix
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

A cold, calm night instrument whose blue is the ground itself: deep midnight blue to every edge, cool white ink, Mona Sans at an expanded 300 for the heads like titles on a film, the same family at its normal width for reading, surfaces cut square in steps of lighter blue, one azure signal. Photographs arrive as moonlight, shadows in the ground's blue and highlights in the ink. It is not a neon dark mode, not frosted glass, and not a black page with a blue button.

### Tokens

```css
:root {
  --color-paper: #02071D; --color-paper-2: #071129; --color-paper-3: #0F1C37;
  --color-ink: #E7F0F9; --color-ink-2: #BDDCF7; --color-muted: #98A9C1;
  --color-rule: #1C2A48; --color-rule-2: #364868;
  --color-accent: #6BCBF7; --color-accent-2: #3483AD; --color-accent-ink: #040C22; --color-focus: #6BDAFF;
  --font-display: "Mona Sans", ui-sans-serif, system-ui, sans-serif; --font-body: var(--font-display); --font-outlier: var(--font-display);
  --radius-card: 0; --radius-pill: 0; --rule-hair: 1px;
  --shadow-card: 0 24px 48px -24px #000007B2;
  --tracking-display: -0.015em; --display-weight: 300; --display-stretch: 125%;
}
```

### Type

- **Display:** Mona Sans 300 at the expanded width on `h1` and `h2`, `--tracking-display`, line-height 1.04, sentence case, roman. The wide light cut is the voice; a long head steps down to `--text-display-s` rather than closing up. Item titles take 500 at the normal width.
- **Figures that are the point:** the display cut at 300, tabular, from `--text-display` up to twice it, tracking -0.03em, the unit beside it at the normal width 400 in `--color-ink-2`.
- **Body:** Mona Sans 400 at the normal width, line-height 1.6. One family at two widths: the cold comes from the ground and the ink, never from a second face.
- **Labels, table heads, meta, status:** 500 a step smaller, sentence case, untracked, `--color-muted`. Tabular figures wherever numbers compare; no mono anywhere.

### Surfaces

- Depth is a step of lightness from paper to paper-2 to paper-3, cut square at radius 0 like a frame; a lifted surface takes `--shadow-card` in the ground's own dark. No outline around a surface; a 1px `--color-rule` parts rows in a table or a list and nothing else.
- Bands: `--color-paper-2` or `--color-paper-3`, two a page at most; never an azure field and never a light band.
- Photographs: low-key light after dark, architecture at night, a lit stairwell, a long corridor; one subject held still, cropped wide or tall. The duotone runs from paper to ink-2, so a daylight picture turns to a pale sheet: pick night. Square frames, a 1px inset outline of ink at 8%, a label-style caption giving the hour or the frame.
- No texture, no glass, no blur, no bloom.

### Range

- **A figure as the statement:** one real number in the display cut at up to twice `--text-display`, alone on the ground with its unit and one line; the wide light cut makes a price read like a title card.
- **The product from another angle:** a detail of the interface cropped large on a paper-2 well (a job sheet, a meter, a contact sheet), stepped in lightness, never framed in a drawn window.
- **Steps or a night log:** an `<ol>` of stages or hours, each head in the expanded cut, figures tabular, the current one in ink and the rest in muted; the meter (a 2px `--color-rule-2` track, an `--color-accent-2` or azure fill) is the only line that moves.
- **Rows and forms on the ground:** hairline rows with expanded titles on the left and the normal width on the right; a calculator on a paper-2 band whose answer is a display-cut figure.

### Controls

- The pair: a solid azure rectangle with `--color-accent-ink` text beside a secondary outlined in `--color-rule-2`, both square, 500. A segmented choice is the same square, filled ink when chosen.
- Links take an azure underline on hover; inputs sit on the paper with a 1px `--color-muted` edge, square.
- The azure stays under 5%: the one primary control, a link's hover, one meter value or one figure. Never a field, a gradient or a second light.

### Motion

One settle: the hero's text fades from 0.6 to 1 over `--dur-long` on `--ease-out`, once, from a visible default. Hover steps a surface one lightness up. A value changes when its source does; nothing slides, loops or follows the cursor.

### Voice

Cool and spare, the night shift's register: the hour, the count, the cost. Short declaratives; a number always carries its unit or its time. Never hype.

### Do-nots

- Never a warm accent; the light here is cold.
- Never a heavy display weight or a head at the normal width; the expanded 300 is the face.
- Never a lamp: no radial glow, no halo, no lit edge on a card.
- Never a rounded corner or a light section; dark and square end to end.
- Never a photograph in its own colours beside the duotone, and never a daylight scene.

### Build hint

```css
h1, h2 { font-weight: var(--display-weight); font-stretch: var(--display-stretch); line-height: 1.04; }
h3 { font-weight: 500; }
.fig { font-weight: var(--display-weight); font-stretch: var(--display-stretch); letter-spacing: -0.03em; line-height: 0.9; font-variant-numeric: tabular-nums; }
.well { background: var(--color-paper-2); border-radius: var(--radius-card); }
.well--raised { background: var(--color-paper-3); box-shadow: var(--shadow-card); }
.btn { border: var(--rule-hair) solid transparent; background: none; border-radius: var(--radius-pill); padding: var(--space-sm) var(--space-lg); font-weight: 500; color: var(--color-ink); transition: background-color var(--dur-short) var(--ease-out); }
.btn--primary { background: var(--color-accent); color: var(--color-accent-ink); }
.btn--secondary { border-color: var(--color-rule-2); }
.btn--secondary:hover { background: var(--color-paper-2); }
.meter { height: 2px; background: var(--color-rule-2); } .meter > span { display: block; height: 100%; background: var(--color-accent); }
a:hover { text-decoration-color: var(--color-accent); }
.settle { animation: settle var(--dur-long) var(--ease-out) both; }
@keyframes settle { from { opacity: 0.6; } }
```
