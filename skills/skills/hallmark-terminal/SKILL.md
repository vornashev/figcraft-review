---
name: hallmark-terminal
description: "Terminal: a near-black ground with a green cast in three lightness steps, pale phosphor ink and one bright phosphor signal with a dim wash of itself, every glyph Martian Mono with heads wide and text narrow, and pictures printed in the page's own glyphs: a photograph rendered as a grid of characters taken from the product's own text, dim cells small, bright cells full, stirred by the cursor. Fits: cli, terminal, shell, command-line, tui, self-hosted, open-source, binary, ssh, sysadmin, devops, homelab, install script, package manager, repl, dotfiles, developer tool, phosphor"
metadata:
  origin: hallmark
  category: themes
  group: style
  mode: manual
  title: Terminal
  summary: атмосферный, тёмный, уверенный акцент
  preview: "#040805 #080F0A #E1F1DE #7EF473 · Martian Mono"
---
# Terminal — a Hallmark style

The designer chose this style for the chat. A style is a material: paper, ink, faces, rules, radius, depth, controls
and voice. It is never a layout. It was written for web pages in CSS; in FigCraft:

- **Tokens become the file's variables.** Look at the file's variables first (`variable.export`). With no colour
  collection for this style, make one named «Terminal»: the `--color-*` tokens as colour variables without the prefix
  (`paper`, `ink`, `accent`…), radii as numbers; bind fills, strokes and radii to them (`variable.bind`), never paste
  hex. A file that already has its own colour system keeps it: restyle it onto this one only when asked.
- **Faces.** Check each family with `text.fonts {family}`. A missing one: say so in one line and take the nearest
  installed face of the same class (mono); never swap silently. Make text styles for display, body, labels
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

The page is the terminal surface, and its pictures are printed in type. A near-black ground with a green cast, pale phosphor ink, one bright phosphor green and a dim wash of it for what is added or selected, and Martian Mono for every glyph: heads wide, text narrow. A picture is printed as a grid of characters from the product's own text. It reads as a tool made by people who live in a shell. It is not the CRT costume and not a dark product page holding a screenshot of a terminal.

### Tokens

```css
:root {
  --color-paper: #040805; --color-paper-2: #080F0A; --color-paper-3: #101A12;
  --color-ink: #E1F1DE; --color-ink-2: #B2CDAF; --color-muted: #769676;
  --color-rule: #1D2A1F; --color-rule-2: #334934;
  --color-accent: #7EF473; --color-accent-ink: #040B05; --color-focus: #7EF473;
  --color-accent-wash: #062409;
  --glyph-0: #18361B; --glyph-1: #244D26; --glyph-2: #2E6A2F; --glyph-3: #3D8B3B;
  --glyph-4: #4EAE45; --glyph-5: #62D158; --glyph-6: #7FF06D; --glyph-7: #C4FFB0;
  --font-display: "Martian Mono", ui-monospace, monospace; --font-body: var(--font-display); --font-outlier: var(--font-display);
  --radius-card: 0; --radius-pill: 0; --rule-hair: 1px; --shadow-card: none;
  --tracking-display: -0.02em; --display-weight: 500; --stretch-display: 112.5%; --stretch-body: 87.5%;
}
```

### Type

- **Every glyph is Martian Mono,** in three weights at most: 400, 500, 700. Display 500 at `--stretch-display`, line-height 1.12, `h1` at most 3.75rem in two or three lines. Body 400 at `--stretch-body`, 15 to 16px, line-height 1.65. Labels and meta a step smaller in `--color-muted`, sentence case, untracked.
- **Figures** set wide and light against the narrow text: 400 at `--stretch-display` from `--text-display-s` up, tabular, the unit or a `#` comment beneath in `--color-muted`.
- Prompt glyphs (`$`, `~ $`) in `--color-muted` mark real commands and only those; arguments in a reference take the accent.
- Martian Mono has no box-drawing or block glyphs. Diagrams are typed in `+ - |` and wordmarks printed as glyph pictures, so no fallback face slips into a line.

### Surfaces

- One hue, a ramp of lightness: ground, `--color-paper-2` for a session or an install well, `--color-paper-3` for hover and selection. Raised surfaces take a 1px `--color-rule` border, square, never a shadow; `--color-rule-2` is the firmer line under a table head or a diff's file header.
- Rules: 1px `--color-rule` between sections, rows and tabs.
- **Pictures as glyphs:** a picture with a strong silhouette on black, reduced to a grid of brightness levels (about 130 columns, cells 1.85 times as tall as wide) and drawn on a canvas, each lit cell one character of the product's text in `--glyph-0` to `--glyph-7`, dim cells at 62% size; a static `<pre>` stands in without script. One or two a page, big.
- When a glyph grid cannot be made, one photograph stands in, in the `photo:` duotone with a 1px `--color-rule` border: the machines themselves, never a screen showing an interface.
- No scanline, glow, bezel, title bar or traffic lights.

### Range

- **A comparison as a diff:** a unified diff across ten or twelve columns, a `--- a/` and `+++ b/` header over a `--color-rule-2` line, removed lines in `--color-muted` behind `-`, added lines in ink on `--color-accent-wash` behind a green `+`, a gutter of line numbers in `--color-rule-2`.
- **Figures as a tool's output:** three or four of the prompt's numbers at display size, wide and light, parted by vertical rules, each labelled by a `# comment` beneath, as `wc` or `du` would print them.
- **The session at size:** a session in a `--color-paper-2` well across eight columns or more, typed once, its output lighting a `+ - |` diagram beside it.
- **A reference as rows:** a command per row at `--text-title`, wide, its arguments in the accent, its line on the right, like a man page's synopsis; or a table of hosts, flags or exit codes.

### Controls

- Primary: an accent block with `--color-accent-ink` text, square. Secondary: a 1px `--color-ink-2` border. Hover and state switch in `steps(1)`.
- Install lines: a `--color-paper-2` well with tabs (brew, cargo, curl) underlined in the accent, the command at `--text-lg`, and a 16px copy icon at the right that turns into a tick in the accent for 1.4s.
- Links in `--color-ink-2`, underlined dotted, accent on hover; a selected row or tab takes `--color-accent-wash`.

### Motion

Stepped where it is state, alive where it is a picture: a glyph picture resolves row by row from noise over about 1.5s, once, and under the cursor its cells flare to the accent, then settle. A session types itself once when it enters the view. A caret blinks five times and holds. Reduced motion shows every final state.

### Voice

Commands, flags, paths and exit codes. Declarative and short: name the command, never the adjective.

### Do-nots

- Never a proportional face, and never a box-drawing glyph from a fallback font.
- Never a second hue: no amber, no cyan, no red for a removed line.
- Never a rounded corner, a pill or a soft card, and never a light section.
- Never more than one photograph, and only where glyphs cannot be made.

### Build hint

```css
body { font-stretch: var(--stretch-body); font-variant-numeric: tabular-nums; }
h1, h2, h3 { font-weight: var(--display-weight); font-stretch: var(--stretch-display); letter-spacing: var(--tracking-display); line-height: 1.12; }
.figure { font-weight: 400; font-stretch: var(--stretch-display); font-size: var(--text-display); line-height: 1; }
.art { position: relative; } .art canvas { position: absolute; inset: 0; }
.btn--primary { background: var(--color-accent); color: var(--color-accent-ink); border-radius: 0; transition: background-color var(--dur-micro) steps(1); }
.well { background: var(--color-paper-2); border: var(--rule-hair) solid var(--color-rule); }
.diff .add { background: var(--color-accent-wash); color: var(--color-ink); } .diff .add::before { content: "+"; color: var(--color-accent); }
.diff .del { color: var(--color-muted); } .diff .del::before { content: "-"; }
```

To make a glyph picture: crop the subject, autocontrast, resize to `cols` by `round(cols * h / w / 1.85)`, quantise brightness to levels 0 to 8 (0 is blank), and ship the rows as strings; the canvas sets each lit cell's glyph from the product text in order and its colour from `--glyph-(level - 1)`.
