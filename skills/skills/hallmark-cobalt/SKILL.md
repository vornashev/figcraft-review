---
name: hallmark-cobalt
description: "Cobalt: cool near-white paper, blue-grey ink and hairlines, Familjen Grotesk over IBM Plex Sans, a generated ASCII field on an 8 by 16 cell, keycaps and cut-corner panels, JetBrains Mono on graphite, one electric cobalt signal. Fits: api, sdk, cli, dev tool, developer platform, docs, documentation, infrastructure, backend, database, observability, webhooks, events, type-safe, open source, ship, deploy, developer experience, technical"
metadata:
  origin: hallmark
  category: themes
  group: style
  mode: manual
  title: Cobalt
  summary: минимализм, светлый, сдержанный акцент
  preview: "#F8FBFE #EFF3F8 #111825 #0462D3 #75B4FF · Familjen Grotesk"
---
# Cobalt — a Hallmark style

The designer chose this style for the chat. A style is a material: paper, ink, faces, rules, radius, depth, controls
and voice. It is never a layout. It was written for web pages in CSS; in FigCraft:

- **Tokens become the file's variables.** Look at the file's variables first (`variable.export`). With no colour
  collection for this style, make one named «Cobalt»: the `--color-*` tokens as colour variables without the prefix
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

An exact, technical register: cool near-white paper ruled with hairlines, Familjen Grotesk heads over IBM Plex Sans, and a ground made of characters, a generated ASCII field snapped to an 8 by 16 cell that shows the product's own traffic in cobalt tints. Panels are cut on two opposite corners, buttons are keycaps with a real bottom edge, code runs on graphite. It is precise because every edge is a hairline or a cut and every glyph means something; it is not a dark developer page or a terminal costume.

### Tokens

```css
:root {
  --color-paper: #F8FBFE; --color-paper-2: #EFF3F8; --color-paper-3: #E3E8EF;
  --color-ink: #111825; --color-ink-2: #363E49; --color-muted: #5D646E;
  --color-rule: #DADEE4; --color-rule-2: #C2C8CF;
  --color-graphite: #121823; --color-graphite-2: #1E2532; --color-graphite-ink: #E3E8EE; --color-graphite-muted: #939CA9;
  --color-accent: #0462D3; --color-accent-2: #75B4FF; --color-accent-wash: #E3F0FF; --color-accent-ink: #F8FBFE; --color-focus: #0462D3;
  --color-accent-deep: #0040BB; --color-accent-edge: #003D98;
  --color-glyph-1: #D0DCEB; --color-glyph-2: #AEC3DE; --color-glyph-3: #7BA1D3; --color-glyph-4: #4A81CC;
  --color-graphite-glyph-1: #2D3645; --color-graphite-glyph-2: #3A4B66; --color-graphite-glyph-3: #466CA5;
  --color-key-face: #FCFDFF; --color-key-edge: #B7BEC8;
  --font-display: "Familjen Grotesk", system-ui, sans-serif; --font-body: "IBM Plex Sans", system-ui, sans-serif;
  --font-outlier: "JetBrains Mono", ui-monospace, monospace;
  --radius-card: 8px; --radius-input: 6px; --radius-pill: 999px;
  --cell-w: 8px; --cell-h: 16px; --cut: 8px; --cut-l: 16px;
  --rule-hair: 1px; --shadow-card: 0 1px 2px #1118250F;
  --shadow-key: 0 3px 0 0 var(--color-key-edge), 0 6px 8px -4px #11182547, inset 0 1px 0 #FFFFFFE6;
  --shadow-key-accent: 0 3px 0 0 var(--color-accent-edge), 0 6px 8px -4px #01286873, inset 0 1px 0 #FFFFFF38;
  --shadow-key-press: inset 0 1px 2px #11182524;
  --tracking-display: -0.028em; --display-weight: 600;
}
```

### Type

- **Display:** Familjen Grotesk 600 on heads and figures, 500 on item titles, `--tracking-display`, line-height 1.02, sentence case, tabular figures; a count at 60px and over is the loudest type.
- **Body:** IBM Plex Sans 400 and 500.
- **Labels, table heads, status:** Familjen Grotesk 500 a step smaller, `--color-muted`. Never mono.
- **Code and glyphs:** JetBrains Mono for code, machine values and the field; never a label, head or chip.

### Surfaces

- A 1px `--color-rule` edges every surface and splits every row; neutrals tilt to hue 250 to 260.
- Panels, chips and fields are cut on two opposite corners: `border-radius: var(--cut-l) 4px` with `corner-shape: bevel round bevel round` inside `@supports`, `--cut` on small parts, plain 8px and 6px radius as the fallback. Depth is `--shadow-card` and a paper step; only keys have an edge.
- The ground is a generated ASCII field on one canvas, never a picture: noise sampled per 8 by 16 cell into a character ramp, tinted `--color-glyph-1` to `-4` with `--color-accent-deep` for the densest cells, shaped by the product's own flow (raw on one side, resolved on the other). It sits behind the hero; one divider row and one graphite panel (graphite glyph tints) may repeat it, four places at most; a dot grid on the cell stands in without script.
- Graphite is the dark material: `--color-graphite` under `--color-graphite-ink`, `--color-graphite-2` for a selected line or header strip, `--color-graphite-muted` for comments. Syntax takes `--color-accent-2`, never a rainbow. Two bands a page at most, one graphite.
- Photographs are rare: one at most, a real system seen from a distance, in the duotone, no type on it.

### Range

- **A table that is the API:** ruled full width, machine values in mono, one row on the cobalt wash.
- **A mapping:** two graphite panes, input and output, matched lines joined by hairline elbows.
- **A timeline as a ruler:** real seconds on one hairline, attempts as notched ticks with their status in Familjen 600 at display size, waits as dimension lines, failure in the error colour.
- **A working control on the prompt's numbers:** its result as one large figure over a meter of fifty mono cells.

### Controls

- Keycaps: a key-face button on a 3px bottom edge that lifts 1px on hover and sinks on press; the one primary is a solid cobalt key. Options are keys on a sunken paper-3 tray, the chosen one pressed.
- A command is a cut chip with a working copy key. Links take a cobalt underline on hover. Inputs are cut, `--color-muted` border, cobalt focus.
- Status is text with one icon, never a filled chip. Cobalt stays under 5% of a screen outside the field.

### Motion

The field runs at 30 fps with a pointer lens, pauses off screen, and is one composed still under reduced motion. Keys travel over `--dur-micro`; connectors draw in once. No bounce, no parallax.

### Voice

Declarative and specific, like a good changelog: the event, the endpoint, the status code. No hype adjectives.

### Do-nots

- Never a warm accent, a pill or a gradient button.
- Never noise for its own sake: the field maps traffic or state the product has, and no type sits on its densest cells.
- Never fake code: a snippet compiles or returns; with no host in the prompt, call `example.com`.

### Build hint

```css
h1, h2, h3 { font-family: var(--font-display); font-weight: 600; letter-spacing: var(--tracking-display); color: var(--color-ink); } h3 { font-weight: 500; }
.key { border: var(--rule-hair) solid var(--color-rule-2); border-radius: var(--radius-input); padding: 0 var(--space-lg); min-height: 48px; background: var(--color-key-face); color: var(--color-ink); font: 500 var(--text-md)/1 var(--font-display); box-shadow: var(--shadow-key); transition: transform var(--dur-micro) var(--ease-out), box-shadow var(--dur-micro) var(--ease-out); }
.key:hover { transform: translateY(-1px); } .key:active { transform: translateY(3px); box-shadow: var(--shadow-key-press); }
.key--primary { background: var(--color-accent); border-color: var(--color-accent-edge); color: var(--color-accent-ink); box-shadow: var(--shadow-key-accent); }
.cut { border: var(--rule-hair) solid var(--color-rule); border-radius: var(--radius-card); background: var(--color-paper); }
@supports (corner-shape: bevel) { .cut { border-radius: var(--cut-l) 4px var(--cut-l) 4px; corner-shape: bevel round bevel round; } }
.graphite { background: var(--color-graphite); color: var(--color-graphite-ink); } .graphite .token { color: var(--color-accent-2); }
a { text-decoration-color: var(--color-rule-2); text-underline-offset: 0.2em; } a:hover { text-decoration-color: var(--color-accent); }
```
