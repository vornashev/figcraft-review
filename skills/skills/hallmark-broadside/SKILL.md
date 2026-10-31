---
name: hallmark-broadside
description: "Broadside: grained buff stock, near-black ink, Six Caps and Bevan wood capitals over Archivo Narrow, ink rules at one point or five, one vermilion. Fits: auction, sale, market, fair, event, one night, announcement, town, notice, poster, bill, lots, machinery, tools, festival, fete, hammer, date, venue, tickets"
metadata:
  origin: hallmark
  category: themes
  group: style
  mode: manual
  title: Broadside
  summary: редакционный, светлый, уверенный акцент
  preview: "#ECE4D0 #E2D8C2 #15100E #C12B09 · Six Caps"
---
# Broadside — a Hallmark style

The designer chose this style for the chat. A style is a material: paper, ink, faces, rules, radius, depth, controls
and voice. It is never a layout. It was written for web pages in CSS; in FigCraft:

- **Tokens become the file's variables.** Look at the file's variables first (`variable.export`). With no colour
  collection for this style, make one named «Broadside»: the `--color-*` tokens as colour variables without the prefix
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

A printer's bill: grained buff stock, near-black ink, Six Caps fitted to the measure over Bevan, Archivo Narrow small print, rules at one point or five, one vermilion. It is loud because the capitals are tall and the rules heavy, never because anything is drawn; photographs print plainly in the ink, like the plate on a sale bill. Not a western pastiche, nor a soft cream editorial page.

### Tokens

```css
:root {
  --color-paper: #ECE4D0; --color-paper-2: #E2D8C2; --color-paper-3: #D8CDB4;
  --color-ink: #15100E; --color-ink-2: #332C29; --color-muted: #584E45;
  --color-rule: #B7AD9A;
  --color-accent: #C12B09; --color-accent-ink: #F5F0E3; --color-focus: #C12B09;
  --font-display: "Six Caps", "Impact", sans-serif; --font-display-2: "Bevan", Georgia, serif;
  --font-body: "Archivo Narrow", "Arial Narrow", ui-sans-serif, sans-serif;
  --font-outlier: var(--font-body);
  --radius-card: 0; --radius-pill: 0; --rule-hair: 1px; --rule-bar: 5px; --rule-frame: 3px;
  --shadow-card: none;
  --tracking-display: 0.02em; --display-weight: 400;
  --grain: 0.08;
}
```

One dial, the colourway, stated in the stamp (`broadside: bill`).

| Colourway | Stock | Ink | Accent |
| --- | --- | --- | --- |
| `bill` (default) | the block above | ink | vermilion |
| `inked` | #130E0B, grain screened | buff #ECE4D0 | vermilion at #E55033; paper band dark |
| `red-bill` | the vermilion | buff #F5F0E3, 5.5:1 | buff; posture drenched |

### Type

- **Six Caps** 400, uppercase, line-height 0.88, `--tracking-display`, for the h1, big figures and fitted lines. It is fitted, not stepped: each line its own element that never wraps (`white-space: nowrap`, the 55b guard), its size set from its measured width in `cqi` so it fills its column exactly; lines stacked in one block differ in size, as type set by hand does.
- **Bevan** 400 for section heads, item titles, the wordmark and short lines of fact; uppercase, untracked, line-height 1.
- **Archivo Narrow** 400 and 600, line-height 1.5, for everything read; labels, table heads, captions and meta in its 500 a step smaller, sentence case, untracked, `--color-muted`. Figures are Six Caps, or Archivo Narrow tabular in a row.
- Three families, no outlier: one case of wood type, the gothic for scale and the slab for weight.

### Surfaces

- Rules: `--rule-bar` in ink above a section, a table or between two columns of a bill, `--rule-hair` in ink under a running head, `--rule-hair` in `--color-rule` between rows. Nothing between one and five.
- Square corners everywhere, no shadow. A frame is a double rule, a `--rule-frame` ink border with a 1px ink keyline 3px inside it, round a well or a photograph.
- Bands: `--color-paper-2`, ink with buff type, or one vermilion band with buff type; two a page at most.
- Photographs: plain daylight documentary at eye level, the thing for sale whole and side-on, a detail at arm's length; nobody facing the lens. Printed in the ink on the stock (the `photo:` duotone), square, in the double-rule frame; type never sits on one, and a caption under it carries a fact.
- Grain, the only texture: the speck layer (`texture.md` § 1) at `--grain`, multiplied on buff and screened on ink, on bands, wells and photograph frames, never under running text.

### Range

- A timetable as a bill: each day a column under a five-point rule, its name fitted in Six Caps to the column, the hour in Bevan, the small print under a 1pt rule; columns parted by a five-point vertical rule.
- A count or a date fitted to the full measure in Six Caps, the one vermilion line of its screen, its small print beneath.
- Particulars as rows: a Bevan label on the left, the fact in Archivo Narrow 600 on the right, hair rules between, a five-point rule over the first; a fact not yet known prints as a muted fill, never invented.
- A form on the vermilion band: buff fields with an ink keyline, the ink block as its action, the head in Bevan.

### Controls

- An ink-filled block in Archivo Narrow 600, untracked capitals (legal under an uppercase display), beside the same block as an unfilled double-rule frame; square, 48px, one fill a page.
- Links in ink, underlined, vermilion on hover; inputs square, 48px, a 1px ink border.
- Vermilion sets one whole display line (its own element, never part of a head) or one figure a screen, on buff or `--color-paper-2`.

### Motion

Printed, so still: a live figure updates in place, a fitted line fits once when the fonts load. No marquee, no hover growth, no reveal.

### Voice

A sale bill read aloud: the date, the place, the lot and the hour, each said once. Shouted in capitals, explained in the small print, in the words of the trade it sells to.

### Do-nots

- Never a ragged big line; a Six Caps line that does not fill its measure is fitted or cut.
- Never a fourth face outside code: the case is Six Caps, Bevan and the narrow.
- Never a rounded corner; frames, controls and photographs are square.
- Never a second colour, in type or in a picture; photographs print in the ink.
- Never a drawn gavel, star or ornament; the capitals and the photograph are the loud things.
- Never a photograph on every fold; half the bill is type, and the type is the loud half.

### Build hint

```css
h1, .display { font-family: var(--font-display); font-weight: 400; text-transform: uppercase; line-height: 0.88; letter-spacing: var(--tracking-display); }
.fit { display: block; white-space: nowrap; }
h2, h3, .wordmark { font-family: var(--font-display-2); font-weight: 400; text-transform: uppercase; line-height: 1; letter-spacing: 0; }
.rule-bar { border-top: var(--rule-bar) solid var(--color-ink); }
.frame, .btn--frame { border: var(--rule-frame) solid var(--color-ink); box-shadow: inset 0 0 0 3px var(--color-paper), inset 0 0 0 4px var(--color-ink); }
.frame { padding: var(--space-lg); } .frame--photo { padding: var(--space-2xs); }
.btn { display: inline-flex; align-items: center; min-height: 48px; padding: 0 var(--space-xl); border: 3px solid var(--color-ink); background: var(--color-ink); color: var(--color-paper); font: 600 var(--text-sm)/1 var(--font-body); text-transform: uppercase; }
.btn--frame { background: transparent; color: var(--color-ink); }
.grained { position: relative; isolation: isolate; }
.grained::after { content: ""; position: absolute; inset: 0; pointer-events: none; opacity: var(--grain); mix-blend-mode: multiply; } /* the speck SVG, texture.md § 1 */
::selection { background: color-mix(in oklab, var(--color-accent) 30%, transparent); }
```
