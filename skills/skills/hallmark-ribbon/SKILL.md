---
name: hallmark-ribbon
description: "Ribbon: warm off-white or blue-black night, Instrument Sans at a quiet weight over Figtree, machined parts lit from above, the hour drawn as light on a generated canvas, one signal. Fits: sleep, sound, soundscape, audio, night, rest, calm, wellness, meditation, white noise, ambient, listen, headphones, wind down, bedtime, quiet, breathing, app, subscription"
metadata:
  origin: hallmark
  category: themes
  group: style
  mode: manual
  title: Ribbon
  summary: атмосферный, светлый, уверенный акцент
  preview: "#FCF9F3 #F5F1E9 #13110F #035F5C · Instrument Sans"
---
# Ribbon — a Hallmark style

The designer chose this style for the chat. A style is a material: paper, ink, faces, rules, radius, depth, controls
and voice. It is never a layout. It was written for web pages in CSS; in FigCraft:

- **Tokens become the file's variables.** Look at the file's variables first (`variable.export`). With no colour
  collection for this style, make one named «Ribbon»: the `--color-*` tokens as colour variables without the prefix
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

The hour before sleep, set quietly: Instrument Sans at 400, upright and tightly set, for every head, Figtree in a soft grey for reading, hairline rules instead of boxes, and the night itself drawn as slow light behind a machined instrument that really sets the levels. The calm comes from light type, slow light and well-made parts. It is not a glossy wellness app and not a sky of stars and moons.

### Tokens

```css
:root {
  --color-paper: #FCF9F3; --color-paper-2: #F5F1E9; --color-paper-3: #EAE5DB;
  --color-ink: #13110F; --color-ink-2: #302D29; --color-muted: #5E5A53;
  --color-rule: #E0DCD4; --color-rule-2: #ECE9E3;
  --color-accent: #035F5C; --color-accent-soft: #D1EBE9; --color-accent-ink: #FAF8F4; --color-focus: #007974;
  --color-band: #002B2B; --color-band-ink: #EFEBE2;
  --color-slot: #B29769;
  --metal-hi: #F7F5F1; --metal-lo: #D1CDC7;
  --edge-light: inset 0 1px 0 #FFFFFF80;
  --shadow-part: 0 1px 0 #18161140, 0 10px 18px -6px #1816114C;
  --shadow-panel: 0 1px 0 #18161133, 0 24px 48px -16px #1B150B59;
  --font-display: "Instrument Sans", ui-sans-serif, system-ui, sans-serif; --font-body: "Figtree", ui-sans-serif, system-ui, sans-serif;
  --font-outlier: "JetBrains Mono", ui-monospace, monospace;
  --radius-card: 20px; --radius-part: 6px; --radius-pill: 999px; --rule-hair: 1px;
  --shadow-card: none;
  --tracking-display: -0.035em; --display-weight: 400;
}
```

One dial, the colourway, stated in the stamp (`ribbon: two-in-the-morning`). The accent is the one lit thing; `--color-slot` is the photo wash; `--color-accent-soft` is a fader's track or a pressed pill, never type.

| Colourway | Paper | Ink | Accent, metal |
| --- | --- | --- | --- |
| `dawn` (default) | `#FCF9F3` | `#13110F` | teal `#035F5C`; aluminium as above, the night drawn on `--color-band` |
| `two-in-the-morning` | blue-black `#040810`, paper-2 16.4%, rule 27% | `#EDE9E1`, muted `#9CA5B1` | a lit window, amber `#EDB980` with `#201307` text; metal `#4E5359` to `#1D2228`, shadows from black |
| `moss` | sage `#CFE1CC` | `#101F13` | ochre `#864F00`; wash deep teal `#196464` |

### Type

- **Display:** Instrument Sans 400, upright, `--tracking-display`, line-height 1.04, sentence case, one colour; 500 for small titles (a panel's name, the wordmark). Big figures and levels take the display face too, lining and tabular.
- **Body:** Figtree 400 at 17px, line-height 1.6, in `--color-muted`; Figtree 500 for a part's name and value.
- **Labels:** Figtree 500 a step smaller, sentence case, untracked, `--color-muted`, tabular figures on values.

### Surfaces

- The hero ground is the hour drawn as light on one generated canvas (in dawn, on `--color-band`): fine slow streaks for rain, long soft lines for wind, a far row of lit points on a low horizon, whatever the prompt's sounds are, over a CSS sky-to-land gradient. Never a photograph behind the head, never a star or a moon.
- Machined parts lit from above: panels in a top-to-bottom gradient with `--edge-light` and `--shadow-panel`; a recessed bed (inset shadow) holding vertical faders with knurled caps (`--metal-hi` to `--metal-lo`, fine striped grip, a lit accent index line), a sunk slot whose glow fills to the level, tick scales either side; a draggable curve for anything timed, with a metal handle.
- Texture is generated: a 160px canvas noise tile set as `--grain` by script, `soft-light` at 0.35 to 0.55, on the night and in panels only.
- Rules, not boxes, in reading sections: 1px `--color-rule` hairlines. Radius: controls pill, parts `--radius-part`, panels `--radius-card`.
- Photographs: the night held still and close (a window, a lamp, a far train); low light, no person. `--radius-card`, no border.

### Range

- **The instrument as the hero:** the product's controls built as a machined panel that really works, beside a one-line head, over the drawn night.
- **Rows as a list of levels:** each part's name in the display face on hairlines, its line in Figtree, its level as a display figure; the same panel in the app's frame beside it, synced.
- **Time as a drawn curve:** what changes over the night drawn as lines falling together across the width, columns marking the moments, levels in tabular Figtree beneath.
- **Price under the horizon:** the figure in the display face at 8 to 10rem over the same land and lit row, one Figtree line, the lit pill.

### Controls

- Machined pills, 52px: a top-to-bottom gradient with `--edge-light` and `--shadow-part`, a 1px border; the primary is the accent, lit from inside with an inset highlight. Active presses 1px down. A switch is a pill track with a metal knob that lights the accent when on.
- Faders and curves are real inputs (`role="slider"`, keyboard steps). Sound plays only after a press of Listen, and Stop or Esc ends it.
- The accent sits on the primary, the focus ring, fader glows, the index lines and one figure.

### Motion

Slow and breathing, `--dur-long` on `--ease-in-out`. One ambient canvas and one CSS loop at most, both paused off screen; levels ease, never jump. Reduced motion and no script: a still night, every part at its sample level.

### Voice

Calm and specific: the hour, the sound, how loud. Never a promise of perfect sleep.

### Do-nots

- Never an italic or a heavy head; the display stays upright at 400 and 500.
- Never a starfield, a moon, a navy-to-violet gradient or a stock sleeper.
- Never a plastic or flat control on the instrument; parts are machined, lit from above, one light.
- Never a drawn waveform or equaliser; levels live on faders and lines.

### Build hint

```css
h1, h2, h3 { font-weight: 400; font-synthesis: none; line-height: 1.04; }
.btn { min-height: 52px; padding: 0 var(--space-lg); border: var(--rule-hair) solid var(--color-rule); border-radius: var(--radius-pill); background: linear-gradient(var(--color-paper-2), var(--color-paper-3)); box-shadow: var(--edge-light), var(--shadow-part); color: var(--color-ink); font: 500 var(--text-md)/1 var(--font-body); }
.btn--primary { background: var(--color-accent); border-color: var(--color-accent); color: var(--color-accent-ink); }
.btn:active { transform: translateY(1px); }
.panel { border-radius: var(--radius-card); background: linear-gradient(var(--color-paper-2), var(--color-paper-3)); box-shadow: var(--edge-light), var(--shadow-panel); }
.cap { border-radius: var(--radius-part); background: linear-gradient(var(--metal-hi), var(--metal-lo)); box-shadow: var(--edge-light), var(--shadow-part); }
.grain { background-image: var(--grain); background-size: 160px; mix-blend-mode: soft-light; opacity: 0.4; }
a:hover { text-decoration-color: var(--color-accent); }
```
