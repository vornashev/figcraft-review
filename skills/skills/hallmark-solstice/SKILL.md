---
name: hallmark-solstice
description: "Solstice: cream paper, warm brown ink, Yeseva One over Archivo and Archivo Narrow, gold hairlines and hard paper shadows, photographs in low warm light, one vermilion signal. Fits: farm, orchard, cider, perry, winery, harvest, seasonal, food, almanac, produce, vineyard, calendar, market, craft drink, label, bottle, rural, slow, sun, midsummer"
metadata:
  origin: hallmark
  category: themes
  group: style
  mode: manual
  title: Solstice
  summary: редакционный, светлый, сдержанный акцент
  preview: "#F6E9D5 #FBF4E6 #3A1E0E #C9212E · Yeseva One"
---
# Solstice — a Hallmark style

The designer chose this style for the chat. A style is a material: paper, ink, faces, rules, radius, depth, controls
and voice. It is never a layout. It was written for web pages in CSS; in FigCraft:

- **Tokens become the file's variables.** Look at the file's variables first (`variable.export`). With no colour
  collection for this style, make one named «Solstice»: the `--color-*` tokens as colour variables without the prefix
  (`paper`, `ink`, `accent`…), radii as numbers; bind fills, strokes and radii to them (`variable.bind`), never paste
  hex. A file that already has its own colour system keeps it: restyle it onto this one only when asked.
- **Faces.** Check each family with `text.fonts {family}`. A missing one: say so in one line and take the nearest
  installed face of the same class (high-contrast-serif); never swap silently. Make text styles for display, body, labels
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

An almanac's warmth: cream paper, warm brown ink, Yeseva One heads, Archivo for the reading and Archivo Narrow for the small print, gold hairlines doing the ruling, square surfaces on hard paper shadows, photographs taken in low late light, and one vermilion signal. It reads as seasonal and rural through the ink, the gold, a fat serif and the light in its pictures, never through drawings of produce. It is not a farmhouse script page and not a terracotta-on-cream template.

### Tokens

```css
:root {
  --color-paper: #F6E9D5; --color-paper-2: #FBF4E6; --color-paper-3: #ECD8B6;
  --color-ink: #3A1E0E; --color-ink-2: #523525; --color-muted: #78553C;
  --color-rule: #E0C69F;
  --color-accent: #C9212E; --color-accent-ink: #FBF4E6; --color-focus: #C9212E;
  --color-gold: #DE9C31; --color-gold-2: #F0C374; --color-slot: var(--color-gold);
  --font-display: "Yeseva One", ui-serif, Georgia, serif; --font-body: "Archivo", ui-sans-serif, sans-serif;
  --font-outlier: "Archivo Narrow", ui-sans-serif, sans-serif;
  --radius-card: 0; --radius-pill: 999px; --rule-hair: 1px; --rule-bar: 2px;
  --shadow-card: 10px 10px 0 var(--color-paper-3);
  --tracking-display: -0.005em; --display-weight: 400;
}
```

The signal is vermilion at hue 24, a red with warmth in it that sits with the gold and the brown, never clay; the gold rules and never fills. Three lights, stated in the stamp (`solstice: long-light`).

| Light | Paper and ink | Signal and gold |
| --- | --- | --- |
| `long-light` (default) | cream `#F6E9D5` under brown `#3A1E0E` | vermilion `#C9212E`, gold `#DE9C31` |
| `dusk` | plum brown `#3B1D13` under cream ink; raised wells stay cream | vermilion keeps `#C9212E` with cream text, gold `#E6AC3D` |
| `midwinter` | frost `#E7F0F5` under cold brown `#202938` | vermilion keeps its hue, gold goes pale `#96C6DD` |

### Type

- **Display:** Yeseva One 400, roman, line-height 1.0, `--tracking-display`, one colour per head; big figures take it too.
- **Body:** Archivo 400 and 500, 16 to 17px, line-height 1.55, in `--color-ink-2`.
- **Small print:** Archivo Narrow 600 at 12.5 to 13.5px, sentence case, untracked, the outlier, for dates, months, captions under a photograph and axis labels. Meta and table heads: Archivo 500 a step smaller, sentence case. No mono.

### Surfaces

- Rules: `--rule-bar` ink across the top of a section, `--rule-hair` in `--color-rule` between rows, a gold hairline under a head inside a well.
- Square everywhere but the control pair: no radius on a well, a photograph or an input; the buttons and the stepper take `--radius-pill`.
- Depth: a raised well takes a `--rule-bar` ink border, a 1px gold rule inset 6px and the hard `--shadow-card`, an offset in paper-3 with no blur; never a soft shadow.
- Bands: a `--color-paper-2` band, or one warm brown ink band with cream text; two a page at most, never a vermilion field.
- Photographs: the season in low, late light: fruit on the branch, long grass, a glass or a bottle on a table outside, the orchard at evening; warm, a little hazy, shadows long. Square, a 1px ink hairline at 10%, no shadow. A caption sits under the frame in the small print, one fact (the place, the month, the bottle); type on a photograph sits on its shaded side over a brown scrim at 40 to 60%.
- No texture: the cream stays clean.

### Range

- **The product built, standing in the light:** the bottle cut out at full height with its label set in live type (the name in Yeseva, the kind in vermilion small print, a gold hairline, the run), on a sky that grades from the cream down through dusk into a dark field, a low warm glow behind it.
- **The label as a ruled list:** a paper-2 well inset with a gold hairline, its facts as rows (style, bottle, run, price, release), small-print labels left and Yeseva values right, dotted gold rules between them.
- **The year on one line:** the seasons from blossom to bottle as stops on a hairline across the brown band, the months in gold small print, the stages in cream Yeseva, the present one marked in the sun's colour.
- **An order that counts:** a pill stepper beside the one vermilion button whose label carries the running total, under a statement head at display size on a cream to dusk ground.

### Controls

- The pair: a vermilion-filled pill in Archivo Narrow 600 with `--color-accent-ink` text, beside a plain one in ink over a 2px ink underline, no box.
- Links underline in ink and turn vermilion on hover; inputs square on `--color-paper-2` with a 1px ink border.
- Restrained: vermilion sits on the primary, the focus ring and one figure, under 5% of a screen; gold never colours text.

### Motion

Quiet: a tab swaps its panel and a row lights on hover, over `--dur-short` on `--ease-out`. No reveal, no counter, no loop.

### Voice

The almanac: the hour of light, the pressing day, the orchard by name. Never a toast to the good life.

### Do-nots

- Never a second warm colour; a second orange makes a fruit stand.
- Never a neutral ink; a grey-black kills the cream.
- Never a rounded card or a soft shadow; a raised well is square, ruled and hard-shadowed.
- Never a cold or flat-lit photograph: a blue noon sky or a flash turns the cream sickly.
- Never clay or terracotta in place of vermilion; past hue 28 the theme becomes the cream, serif and clay page every generator makes.

### Build hint

```css
h1, h2, h3 { font-weight: 400; line-height: 1; }
.small, figcaption { font: 600 12.5px var(--font-outlier); color: var(--color-muted); }
.btn { display: inline-flex; padding: var(--space-md) var(--space-xl); border: 0; font: 600 var(--text-sm)/1 var(--font-outlier); background: var(--color-accent); color: var(--color-accent-ink); }
.btn--secondary { background: none; color: var(--color-ink); padding: var(--space-lg) 0 var(--space-xs); border-bottom: var(--rule-bar) solid var(--color-ink); }
.well { background: var(--color-paper-2); border: var(--rule-bar) solid var(--color-ink); outline: var(--rule-hair) solid var(--color-gold); outline-offset: -7px; box-shadow: var(--shadow-card); }
.band--ink { background: var(--color-ink); color: var(--color-paper); }
.photo img { outline: var(--rule-hair) solid color-mix(in oklab, var(--color-ink) 10%, transparent); outline-offset: -1px; }
a:hover { text-decoration-color: var(--color-accent); }
::selection { background: color-mix(in oklab, var(--color-gold) 40%, transparent); }
```
