---
name: hallmark-blueprint
description: "Blueprint: prussian-blue sheet, white line ink, Chakra Petch capitals over IBM Plex Sans with mono measurements, square double keylines and dimension strings, photographs printed as cyanotypes, the white line as the only signal. Fits: architecture, architect, engineering, construction, structural, interiors, planning, surveying, cad, drafting, fabrication, prefab, developer, technical, spec, permit, renovation, build, drawings, architecture studio, timber"
metadata:
  origin: hallmark
  category: themes
  group: style
  mode: manual
  title: Blueprint
  summary: минимализм, средний тон, залит цветом
  preview: "#0D3970 #062F61 #EEF6FD #EEF6FD · Chakra Petch"
---
# Blueprint — a Hallmark style

The designer chose this style for the chat. A style is a material: paper, ink, faces, rules, radius, depth, controls
and voice. It is never a layout. It was written for web pages in CSS; in FigCraft:

- **Tokens become the file's variables.** Look at the file's variables first (`variable.export`). With no colour
  collection for this style, make one named «Blueprint»: the `--color-*` tokens as colour variables without the prefix
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

A drafting sheet as a material: Prussian-blue paper, a white line for ink, Chakra Petch drafted capitals over IBM Plex Sans, mono measurements with their units, keylines instead of cards, and photographs printed as cyanotypes, the sheet's blue in the shadows and its white in the light. It reads technical because everything is a line, a dimension or a print on one ground and the line is the only signal. It is not a dark product page with a blue gradient, not a neon wireframe.

### Tokens

```css
:root {
  --color-paper: #0D3970; --color-paper-2: #062F61; --color-paper-3: #012352;
  --color-ink: #EEF6FD; --color-ink-2: #D0E1EE; --color-muted: #A6C2D9;
  --color-rule: #DCEAF4D9; --color-rule-2: #DCEAF452;
  --color-grid: #EFF6FB17; --color-grid-2: #EFF6FB33;
  --color-accent: #EEF6FD; --color-accent-ink: #06346A; --color-focus: #EEF6FD;
  --font-display: "Chakra Petch", ui-sans-serif, sans-serif; --font-body: "IBM Plex Sans", ui-sans-serif, sans-serif;
  --font-outlier: "IBM Plex Mono", ui-monospace, monospace;
  --radius-card: 0; --radius-pill: 0; --rule-hair: 1px; --rule-heavy: 2px; --shadow-card: none;
  --tracking-display: -0.012em; --display-weight: 600; --sheet-inset: 20px; --tick: 14px;
}
```

Three sheets, stated in the stamp (`blueprint: cyanotype`).

| Sheet | Ground, line, muted |
| --- | --- |
| **cyanotype** (default) | the tokens above |
| **whiteprint** | ground `#F3F7FA`, ink `#0D3970`, muted `#4D6B91` |
| **brownline** | ground `#E1CEB0`, ink `#3C2111`, muted `#6B4E3A`, a red pencil `#A50002` for annotation only |

### Type

- **Display:** Chakra Petch 600 for every head, `--tracking-display`, roman, one weight a head: the h1 and h2 uppercase at line-height 1.02 (55a), the h3 in sentence case.
- **Body:** IBM Plex Sans 400 for prose and 500 for labels and controls; reversed on the sheet, nothing lighter than 400.
- **Labels, captions, table heads, meta:** IBM Plex Sans 500 a step smaller, sentence case. IBM Plex Mono 500 sets a measurement with its unit, a stage or drawing number, a year on a dimension string and code, nothing else.

### Surfaces

- Lines only: 1px `--color-rule` keylines on every surface, and a second keyline in `--color-rule-2` 5px inside on a figure or a photograph. Radius 0, no shadows; depth is a second line, a `--rule-heavy` line or a one-step darker ground.
- The dimension string: a hairline with a 45° tick (`--tick` long) at each end and short extension lines, its value set above it. It measures something real, never a decoration.
- The grid: 24px minor lines in `--color-grid`, 120px major in `--color-grid-2`, offset by `--sheet-inset`, only under a drawing, a schedule or a chart of real data.
- Bands: `--color-paper-2` or `--color-paper-3`, two a page at most; the sheet is already the colour (drenched), so there is no other field.
- Photographs: structures built and building, shot square-on so they read like drawings (a frame going up, a roof from below, a model on a table), printed as cyanotypes inside the double keyline; pick frames with a real white and a real shadow, since grey prints flat. Type over one sits on a `--color-paper-3` scrim from its edge.

### Range

- **Figures as dimensions:** the prompt's one number in Chakra Petch at display size, set on a dimension string that spans ten or twelve columns between its two real ends (a first year and now, a smallest and largest span), the ends in mono.
- **Tables as drawing registers:** a stage schedule, a deliverables list or a price list as a keylined table, stage numbers in mono in their own column, the row title one weight heavier, a `--rule-heavy` line under the head row; on `--color-paper-2` it reads as the register sheet of a set.
- **Forms as a title block:** fields set as cells of a keylined block, each label at the cell's top left, the cells sized by what they hold, the submit in the ink fill at the block's foot.
- **Comparisons and steps as elevations:** two options side by side as columns parted by one heavy line, or stages as a run along one long dimension string with a tick at each stage, each stage a numeral, a title and a line.

### Controls

- An ink-filled primary with sheet-coloured text beside a 1px-outlined secondary in ink, both square, 48px, IBM Plex Sans 500.
- Links in ink with a 1px underline that clears on hover; inputs square, 48px, a 1px `--color-rule` keyline on `--color-paper-2`, the white focus ring, never a glow.
- The line is the accent: white on blue, in rules, the primary fill and the focus ring.

### Motion

Static, drafted. A rule or a dimension string may draw itself once a page (scaleX from its left tick over `--dur-long` on `--ease-out`); hover on a keylined surface that links darkens its ground one step.

### Voice

Specification voice: the building type, the stage, the year, the format, a unit on every figure; nothing a drawing note could not carry.

### Do-nots

- Never a filled card, a blur or a lifted panel; the sheet has lines, not layers.
- Never a second colour on the cyanotype, in type or in a photograph; the red pencil belongs to the brownline sheet.
- Never a building, frame or section drawn to stand in for a project, and never a dimension string with an invented value; a drawing is real project data or it is absent.
- Never the grid as wallpaper behind prose, and never a lowercase h1 or h2.
- Never a rounded corner, anywhere.

### Build hint

```css
h1, h2, h3 { font-weight: 600; }
h1, h2 { text-transform: uppercase; line-height: 1.02; }
.num { font-family: var(--font-outlier); font-weight: 500; }
.fig { position: relative; border: var(--rule-hair) solid var(--color-rule); }
.fig::after { content: ""; position: absolute; inset: 5px; z-index: 2; border: var(--rule-hair) solid var(--color-rule-2); pointer-events: none; }
.dim { position: relative; height: var(--rule-hair); background: var(--color-rule); }
.dim::before, .dim::after { content: ""; position: absolute; top: calc(var(--tick) / -2); width: var(--rule-hair); height: var(--tick); background: var(--color-rule); transform: rotate(45deg); }
.dim::before { left: 0; } .dim::after { right: 0; }
.btn { border: var(--rule-hair) solid var(--color-rule); border-radius: 0; background: transparent; color: var(--color-ink); padding: var(--space-sm) var(--space-lg); font-weight: 500; }
.btn--primary { background: var(--color-ink); border-color: var(--color-ink); color: var(--color-accent-ink); }
```
