---
name: hallmark-sport
description: "Sport: cool concrete paper, blue-black ink, uppercase Saira Condensed over Albert Sans, condensed figures and mono times, two-weight rules, one volt fill. Fits: running, marathon, race, training, fitness, gym, team, league, fixtures, standings, scoreboard, athletics, performance, splits, sportswear, club, match, tournament"
metadata:
  origin: hallmark
  category: themes
  group: style
  mode: manual
  title: Sport
  summary: редакционный, светлый, сдержанный акцент
  preview: "#F6F9FC #EBEFF2 #00082E #C8E928 · Saira Condensed"
---
# Sport — a Hallmark style

The designer chose this style for the chat. A style is a material: paper, ink, faces, rules, radius, depth, controls
and voice. It is never a layout. It was written for web pages in CSS; in FigCraft:

- **Tokens become the file's variables.** Look at the file's variables first (`variable.export`). With no colour
  collection for this style, make one named «Sport»: the `--color-*` tokens as colour variables without the prefix
  (`paper`, `ink`, `accent`…), radii as numbers; bind fills, strokes and radii to them (`variable.bind`), never paste
  hex. A file that already has its own colour system keeps it: restyle it onto this one only when asked.
- **Faces.** Check each family with `text.fonts {family}`. A missing one: say so in one line and take the nearest
  installed face of the same class (display-condensed); never swap silently. Make text styles for display, body, labels
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

## Genre: editorial (the default)

Content-led prompts: portfolios, manifestos, type specimens, agency sites, magazine pieces, podcasts, brand stories, considered consumer marketing. The silent default when no other genre signal fires. The deal leans toward this genre's themes; nothing here lists them.

## Voice

- **Accent:** one hue, held to the posture's footprint.
- **Layout:** asymmetric; hairlines, not card borders; type set large enough to hold its screen.
- **Motion:** quiet, one orchestrated entrance.
- **Copy:** specific, hand-set, slightly literary; verbs over adjectives.

## Allowed here

Hairline rules, fleurons, drop caps, double rules; italic inside running body copy; asymmetric column ratios (2:5, 3:7); photographs in the theme's treatment, captioned with facts; edge-aligned headlines; a single `<mark>` band behind the x-height.

## Refused here

Gradient-filled pills; a centred-everything hero (the genre is left-biased or asymmetric, unless the theme's material is a centred bill); glass (the medium is paper); pure black or white paper and ink.

## Chrome that fits

A masthead, a quiet edge-aligned bar, a colophon, a letter close. A marquee footer or a floating blur pill fights the register. Affinities, not assignments: gate 42 only asks that a default be named in the stamp rather than arrived at by reflex.


## The theme

A results-sheet material: cool concrete paper, blue-black ink, Saira Condensed 800 in capitals over an Albert Sans body, big condensed figures and JetBrains Mono times, hairlines and one heavier bar rule, and volt as the only colour. Volt is a fill: ink sits on it, and it never sets a letter on paper. Photographs print in the ink, like a race programme. It reads fast because of the condensed caps, the numbers and the action, never a slant or a gradient; it is not a sportswear advert and not a neon gaming page.

### Tokens

```css
:root {
  --color-paper: #F6F9FC; --color-paper-2: #EBEFF2; --color-paper-3: #DFE3E7;
  --color-ink: #00082E; --color-ink-2: #071A36; --color-muted: #5B646F;
  --color-rule: #B4B8BC; --color-rule-2: #273E5C;
  --color-accent: #C8E928; --color-accent-ink: #00082E; --color-accent-deep: #678802;
  --color-focus: #678802; --color-slot: #96B3DE;
  --font-display: "Saira Condensed", sans-serif; --font-body: "Albert Sans", ui-sans-serif, sans-serif;
  --font-outlier: "JetBrains Mono", ui-monospace, monospace;
  --radius-card: 4px; --radius-pill: 4px; --rule-hair: 1px; --rule-bar: 2px;
  --shadow-card: none;
  --tracking-display: -0.015em; --display-weight: 800;
}
```

### Type

- **Display:** Saira Condensed 800, uppercase, `--tracking-display`, line-height 1.02, upright, roman. A true condensed design, so the caps stack without crowding, even at poster scale over a photograph; the speed is in the caps, never a slant.
- **Body:** Albert Sans 400 and 500, sentence case.
- **Figures:** at statement size (a distance, a field size, a price, a date) Saira Condensed 800 with `tabular-nums`, from `--text-display-s` up, the label in Albert Sans beneath. In columns and live data (times, splits, bibs) JetBrains Mono 500, a step or more larger than its label. Mono is a stopwatch, never a label or a head.
- **Labels, captions, table heads, units:** Albert Sans 500 a step smaller, sentence case, untracked, `--color-muted`; on a volt fill every word is the ink.

### Surfaces

- Two rule weights, never boxed cards: `--rule-hair` in `--color-rule` rules rows and grids; the `--rule-bar` in `--color-rule-2` opens and closes a table and breaks a section.
- Radius 4px on controls, inputs and photographs; no pills.
- Depth from rules and paper steps, never shadows: a well is `--color-paper-2` under a bar rule.
- Bands: a `--color-paper-2` band, or one `--color-ink` band with paper type; two a page at most, never a volt band.
- Photographs: race photography at the runner's eye or lower: a pack mid-stride, legs and shoes on tarmac, a road climbing a valley side, a number being pinned on; hard daylight, the motion sharp, cropped tight, nobody posing. Printed in the ink on the paper (the `photo:` duotone), 4px radius, an inset ink hairline at 8%. Type on a photograph is paper over an ink scrim from its edge; a volt figure may hold a frame's corner with a fact (the mile, the time).
- No texture, no gradient but a photograph's scrim, no hard-offset shadow.

### Range

- **The race in figures:** three or four of the prompt's numbers in condensed caps at display size under the bar rule, parted by hairlines, one at most sitting on a volt fill.
- **A working control on the race's facts:** a pace or time planner on the ink band, the chosen time in mono at display size, every mile in a ruled grid that changes in place, the finish cell in volt.
- **Results as a sheet:** the bar rule opening and closing a table of bibs and times in mono, the followed runner's row lifted a paper step and its latest split in volt.
- **The course as stages:** start to finish as numbered stages on one bar rule, a condensed-cap title and one line each, the live stage on volt.

### Controls

- The control pair: a volt-filled block with ink text beside one bordered 2px in ink, both 4px, set in the display face's capitals with no added tracking; on a photograph the second takes paper.
- Links grow a `--color-accent-deep` underline on hover (3:1 on paper); inputs are 4px with a 1px `--color-rule` border and the `--color-focus` ring.
- The volt is always a fill under ink and under 5% of a screen: the primary control, an active row, one highlighted figure.

### Motion

Nothing moves except state and live data: a deep-volt underline grows under a link on hover, a row lifts one paper step, a live split changes in place, never counting up. No reveal, no parallax.

### Voice

Race-briefing plain: the distance, the time, the place, as a marshal calls them. Imperative heads in capitals, sentence case below, numerals over words, verbs over adjectives.

### Do-nots

- Never slant or italicise the display; the upright condensed cap is the speed.
- Never loosen the display tracking past zero, or tighten it until two capitals touch.
- Never warm paper; the ground is cool concrete, hue 250.
- Never volt type, a volt hairline on paper or a second accent; photographs print in the ink, never in their own colour.
- Never a medal, trophy, podium or jersey texture, drawn or photographed; the race is the road and the runners.

### Build hint

```css
h1, h2, h3 { font-family: var(--font-display); font-weight: var(--display-weight); letter-spacing: var(--tracking-display); text-transform: uppercase; line-height: 1.02; }
.figure { font: var(--display-weight) var(--text-display)/0.9 var(--font-display); font-variant-numeric: tabular-nums; }
.time { font: 500 var(--text-2xl)/1 var(--font-outlier); font-variant-numeric: tabular-nums; }
.btn { border: var(--rule-bar) solid transparent; border-radius: var(--radius-card); padding: var(--space-sm) var(--space-lg); font: var(--display-weight) var(--text-md)/1.25 var(--font-display); text-transform: uppercase; }
.btn--primary { background: var(--color-accent); color: var(--color-accent-ink); }
.btn--secondary { border-color: var(--color-ink); color: var(--color-ink); }
.well { background: var(--color-paper-2); border-top: var(--rule-bar) solid var(--color-rule-2); }
.rule { border-top: var(--rule-bar) solid var(--color-rule-2); }
th, td { border-top: var(--rule-hair) solid var(--color-rule); }
.photo { border-radius: var(--radius-card); outline: 1px solid color-mix(in oklab, var(--color-ink) 8%, transparent); outline-offset: -1px; }
.scrim { background: linear-gradient(to top, color-mix(in oklab, var(--color-ink) 70%, transparent), transparent 60%); color: var(--color-paper); }
a:hover { text-decoration-color: var(--color-accent-deep); }
::selection { background: var(--color-accent); color: var(--color-ink); }
```
