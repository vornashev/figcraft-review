---
name: hallmark-console
description: "Console: graphite ground in three lightness steps, pale ink, hairline panels cut from one surface, Host Grotesk 500 for reading, Atkinson Hyperlegible Mono for what was measured, amber for a person and cool blue for an instrument. Fits: lab, laboratory, protocol, experiment, notebook, science, research, observability, monitoring, version control, audit, compliance, instruments, data, devtools, engineering, telemetry, record, operations, dark, developer"
metadata:
  origin: hallmark
  category: themes
  group: style
  mode: manual
  title: Console
  summary: минимализм, тёмный, сдержанный акцент
  preview: "#0D1013 #15191C #ECEFF2 #F7B83D · Host Grotesk"
---
# Console — a Hallmark style

The designer chose this style for the chat. A style is a material: paper, ink, faces, rules, radius, depth, controls
and voice. It is never a layout. It was written for web pages in CSS; in FigCraft:

- **Tokens become the file's variables.** Look at the file's variables first (`variable.export`). With no colour
  collection for this style, make one named «Console»: the `--color-*` tokens as colour variables without the prefix
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

An instrument kept by careful people: a graphite ground stepped in three lightnesses, hairline panels cut from one surface, Host Grotesk for what a person reads, Atkinson Hyperlegible Mono for what an instrument measured, amber for a person and cool blue for an instrument. The ground is neutral so both meanings sit on it at equal weight, and nothing glows. It is not a neon terminal, a glass dashboard or a science-fiction control room.

### Tokens

```css
:root {
  --color-paper: #0D1013; --color-paper-2: #15191C; --color-paper-3: #06080B;
  --color-ink: #ECEFF2; --color-ink-2: #C3C8CC; --color-muted: #9DA2A8;
  --color-rule: #2D3135; --color-rule-2: #484E54;
  --color-accent: #F7B83D; --color-accent-ink: #1C0E00; --color-accent-soft: #38280A; --color-focus: #F7B83D;
  --color-cool: #6EBCFC; --color-cool-soft: #142E43;
  --color-ok: #61CB7C; --color-ok-soft: #162519; --color-bad: #F66D67; --color-bad-soft: #2F1A18;
  --font-display: "Host Grotesk", ui-sans-serif, system-ui, sans-serif; --font-body: var(--font-display);
  --font-outlier: "Atkinson Hyperlegible Mono", ui-monospace, monospace;
  --radius-card: 10px; --radius-pill: 6px; --rule-hair: 1px;
  --shadow-card: none;
  --tracking-display: -0.03em; --display-weight: 500;
}
```

One dial, the colourway, stated in the stamp (`console: graphite`): `graphite`, the tokens above; `paper`, ground #FAF8F4 under ink #17130F, amber #A15C00 and cool #116BB5, the paper band turning light; `amber-room`, ground #110903 under ink #F2EEE6, amber #F4B93C and the cool turned to ice #83D4D8. In every colourway amber means a person and cool means an instrument.

### Type

- **Display:** Host Grotesk 500, `--tracking-display`, line-height 1.02 to 1.05, sentence case, roman; calm at size, never 700.
- **Body:** Host Grotesk 400 at 16 to 17px, line-height 1.55, in `--color-muted`; the lede in `--color-ink-2`.
- **Labels, captions, table heads, chips:** Host Grotesk 500 a step smaller, sentence case, in `--color-muted`.
- **Measured:** Atkinson Hyperlegible Mono 400 and 500 at 14 to 15px for what an instrument or the system wrote: a reading with its unit, an id, a diff, a timestamp, every figure tabular. Its slashed zero and tailed one are the point; at display size it is the theme's loudest thing. Never a label, a head or a control.

### Surfaces

- Hairline panels: a surface is a 1px `--color-rule` with `--color-paper-2` inside, radius 10px (6px on controls). Panels that sit together are one surface divided by 1px rules; `--color-rule-2` marks the selected row or the spine of a trail.
- Three steps, no lamp: the ground, a panel one step up, the deepest step for code, logs, a changed row and photographs. No shadow, glow, bloom or spotlight.
- Bands: a `--color-paper-3` or `--color-paper-2` band, never an amber field; two a page at most.
- Photographs: one or two, of the bench and never a face (gloved hands at a pipette, a rack of tubes), dark and close, black and white from the deepest step to the ink, radius 10px, a 1px rule edge, a caption beneath.
- No texture, no gradient on a surface.

### Range

- **Diffs:** a comparison set as two versions in one panel, a gutter of plus and minus in ok and bad, the changed rows on the soft tints, the reason in the person's words beside them.
- **Readings:** a single value at display size in the measured face, the struck value it replaced above it, and who, when and why beneath in amber, cool and ink; a statement made of a record.
- **Trails:** rows as an audit trail on a 1px `--color-rule-2` spine, each entry a version, a person in amber, a time in cool, a reason in ink; a timetable or changelog reads the same way.
- **Panels:** a bento or a comparison cut from one surface with 1px seams, one panel the lead, each panel holding the product at full fidelity rather than a picture of it.

### Controls

- The pair: an amber fill with `--color-accent-ink` beside a 1px `--color-rule-2` outline on `--color-paper-2`, both at 6px, Host Grotesk 500.
- A chip carries state only: the label face inside a 1px rule at 4px radius, tinted `--color-accent-soft` or `--color-cool-soft` by meaning. A version picker is a row of such chips, the chosen pair on the cool tint. Inputs sit on `--color-paper-3` inside a 1px rule at 6px; links underline in `--color-rule-2` and turn amber on hover.
- Two meanings: amber is a person (an operator, a deviation, the current step, the one primary control); cool is an instrument (a reading, a trace, a version). Ok and bad exist for diffs and status only.

### Motion

A value changes when its source does, over `--dur-short` on `--ease-out`; a chart may draw once. No reveal, parallax or hover lift.

### Voice

A lab notebook kept by a careful person: the value, its unit, the time, who signed. A number without a unit or a time is nothing.

### Do-nots

- Never swap the meanings; an amber reading or a cool deviation is the theme lying.
- Never a floating card with a shadow under it.
- Never a third signal or a photograph in colour.
- Never mono on a label, a head or a button; mono is what an instrument wrote.
- Never a page of small panels only; one value or one record a page is set large.

### Build hint

```css
h1, h2, h3 { font-family: var(--font-display); font-weight: 500; letter-spacing: var(--tracking-display); line-height: 1.04; }
.panels { display: grid; gap: var(--rule-hair); background: var(--color-rule); border: var(--rule-hair) solid var(--color-rule); border-radius: var(--radius-card); overflow: hidden; }
.panels > * { background: var(--color-paper-2); }
.measured { font-family: var(--font-outlier); font-size: var(--text-sm); font-variant-numeric: tabular-nums slashed-zero; }
.reading { font-family: var(--font-outlier); font-size: var(--text-display); font-weight: 400; letter-spacing: -0.04em; line-height: 1; color: var(--color-ink); }
.row--minus { background: var(--color-bad-soft); } .row--plus { background: var(--color-ok-soft); }
.btn { border: var(--rule-hair) solid var(--color-rule-2); border-radius: var(--radius-pill); padding: var(--space-sm) var(--space-md); background: var(--color-paper-2); color: var(--color-ink); font-weight: 500; transition: background-color var(--dur-short) var(--ease-out); }
.btn--primary { background: var(--color-accent); border-color: var(--color-accent); color: var(--color-accent-ink); }
::selection { background: color-mix(in oklab, var(--color-accent) 25%, transparent); }
```
