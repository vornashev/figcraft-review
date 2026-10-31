---
name: hallmark-dusk
description: "Dusk: a real landscape at the turn of the light behind the hero, slate below it, the product in smoked glass with a lit top edge, Wix Madefor Display at a quiet weight over Wix Madefor Text, bone wells for light surfaces, one periwinkle signal and one apricot. Fits: treasury, banking, fintech, payments, reconciliation, ledger, accounting, close, month end, audit, balance, cash management, payouts, settlement, compliance, controller, bookkeeping, finance team, invoicing, payroll, overnight, automation"
metadata:
  origin: hallmark
  category: themes
  group: style
  mode: manual
  title: Dusk
  summary: минимализм, тёмный, уверенный акцент
  preview: "#0E1017 #151820 #F4F1ED #A0B0F4 #F4BA87 · Wix Madefor Display"
---
# Dusk — a Hallmark style

The designer chose this style for the chat. A style is a material: paper, ink, faces, rules, radius, depth, controls
and voice. It is never a layout. It was written for web pages in CSS; in FigCraft:

- **Tokens become the file's variables.** Look at the file's variables first (`variable.export`). With no colour
  collection for this style, make one named «Dusk»: the `--color-*` tokens as colour variables without the prefix
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

Money software at the calm end of the day: a real photograph of land at dusk behind the hero, the head set dark on its palest part, the product beside it in smoked glass. Below, the page turns to slate and light surfaces are bone wells. It reads as expensive and unhurried, never a neon trading screen or a dashboard of tiles.

### Tokens

```css
:root {
  --color-paper: #0E1017; --color-paper-2: #151820; --color-paper-3: #1E212A;
  --color-ink: #F4F1ED; --color-ink-2: #CACED4; --color-muted: #999FA9;
  --color-rule: #2A2E36; --color-light: #FFFFFF; --color-shade: #020309;
  --color-accent: #A0B0F4; --color-accent-ink: #0F1223; --color-accent-hi: #B9C7FF;
  --color-accent-deep: #3E4999; --color-accent-soft: #D9E0FB; --color-focus: #A9B9FF;
  --color-accent-2: #F4BA87; --color-dusk: #C882C2;
  --color-day-ink: #161A25; --color-day-muted: #3D424E; --color-fog: #F1EAE3;
  --color-well: #F3EFEA; --color-well-2: #E9E4DD; --color-well-ink: #151820; --color-well-muted: #565B64; --color-well-rule: #D9D5CF; --color-card: #FFFDFB;
  --glass: #171A2394; --glass-blur: 22px;
  --glass-hi: inset 0 1px 0 #FFFFFF1A, inset 0 0 0 1px #FFFFFF0F;
  --shadow-card: 0 1px 0 #FFFFFF0F inset, 0 40px 80px -32px #010205B2;
  --font-display: "Wix Madefor Display", ui-sans-serif, system-ui, sans-serif; --font-body: "Wix Madefor Text", ui-sans-serif, system-ui, sans-serif;
  --radius-card: 18px; --radius-inner: 10px; --radius-pill: 999px; --rule-hair: 1px;
  --tracking-display: -0.022em; --display-weight: 500;
}
```

Three dials, each stated in the stamp (`dusk: fog/periwinkle-apricot/glass`); two Dusk pages in one run differ on two.

| Dial | Options |
| --- | --- |
| **Hour** (the hero photograph) | `fog` (default): a valley of fog under an apricot sky. `shore`: water at dusk, boats or a quay. `ridge`: mountain ridges in haze at first light |
| **Signals** (matched, then open) | `periwinkle-apricot` (default). `sage-apricot`: `#97CCAE` as the first signal |
| **Product surface** | `glass` (default): smoked glass on slate. `well`: bone wells carry the hero product too, glass only over photographs |

### Type

- **Display:** Wix Madefor Display 500, `--tracking-display`, line-height 1.02 to 1.1, sentence case. Heads stay modest; the photograph and the product are the loud parts.
- **Body:** Wix Madefor Text 400 and 500 at 17px, line-height 1.55; leads in `--color-ink-2` or `--color-muted`.
- **Figures:** the same faces, `tabular-nums`; cents in `--color-muted` at the same size, never raised. A figure set as a statement goes to Display 500 at 34 to 44px with its cents at 0.6em.
- **Labels, column heads, status:** Text 500 a step smaller, sentence case, `--color-muted`. Never mono, never tracked capitals.

### Surfaces

- **The hour:** a library photograph of land at the turn of the light fills the hero, the head in `--color-day-ink` on its palest part over a fog scrim (`--color-fog` at 40 to 78%, radial, behind the text only), the product in glass on its darker side, the foot fading to `--color-paper`. A second photograph of the same hour may close the page behind the form; two at most.
- **Glass:** the product's surface, `--glass` blurred, `--glass-hi` for the lit edge, `--shadow-card`. Rows inside split on `--color-light` at 7%; inner parts sit on it at 4 to 6% with `--radius-inner`.
- **Wells:** a light surface is a bone well at 5:4 holding one white `--color-card`; the caption sits under it, a title and one muted line.
- **Slate:** every band below the hero is `--color-paper`; the nav turns to slate glass once it leaves the photograph.

### Range

- **A run as an account list:** accounts with a round initial, line counts in muted, a status word with its icon, balances right-aligned with muted cents; the open item closes the list as an apricot strip with its action.
- **A tour as a list beside one pane:** four jobs in a ruled list, the chosen one marked by a periwinkle dot and opened to one line, one glass pane beside it that changes with it.
- **A month as a strip of nights:** one slim rounded bar a day in periwinkle, its height the work done, a flagged day marked by an apricot dot above its bar, the open day in apricot, days still to come hatched; a ruled tally of four figures under it.
- **A hand-off in a well:** the note or message the product sends, set as the real card on bone.

### Controls

- One periwinkle pill (`--color-accent` under `--color-accent-ink`, a light inset top edge); hover lifts to `--color-accent-hi` with a soft periwinkle ring. A ghost pill beside it in `--color-light` at 4%.
- An email field and its button share one pill: frosted fog over a photograph, smoked glass on slate.
- Tabs are a ruled list with a dot, never boxed segments. Switches are periwinkle when on.
- Two signals, two jobs: periwinkle is done, matched, on and focused; apricot is open, waiting or owed. Neither is ever a large fill.

### Motion

The hero photograph drifts 6% over 48 seconds; the product's rows rise in once, staggered; the open dot breathes; panes cross-fade; bars grow from their feet when seen. Reduced motion: all still.

### Voice

Calm and exact: what ran, when, what is left.

### Do-nots

- Never a drawn or generated sky, and never text on the busy part of a photograph.
- Never a gradient button, a third signal colour or a red debit.
- Never a grid of stat tiles; figures live in rows, lists and one ruled tally.
- Never glass on glass, never a glow behind glass, never glass without its lit edge.

### Build hint

```css
h1, h2, h3 { font-family: var(--font-display); font-weight: var(--display-weight); letter-spacing: var(--tracking-display); }
.num { font-variant-numeric: tabular-nums; } .num .c { color: var(--color-muted); }
.glass { background: var(--glass); border-radius: var(--radius-card); -webkit-backdrop-filter: blur(var(--glass-blur)) saturate(1.35); backdrop-filter: blur(var(--glass-blur)) saturate(1.35); box-shadow: var(--glass-hi), var(--shadow-card); }
.btn { min-height: 48px; padding: 0 var(--space-lg); border: 0; border-radius: var(--radius-pill); background: var(--color-accent); color: var(--color-accent-ink); font: 600 0.9375rem/1 var(--font-body); box-shadow: inset 0 1px 0 color-mix(in oklab, var(--color-light) 35%, transparent); }
.btn:hover { background: var(--color-accent-hi); }
.hero__photo { position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }
.hero__scrim { position: absolute; inset: 0; background: radial-gradient(ellipse 50% 58% at 20% 56%, color-mix(in oklab, var(--color-fog) 78%, transparent), transparent 78%), linear-gradient(to bottom, transparent 72%, var(--color-paper)); }
```
