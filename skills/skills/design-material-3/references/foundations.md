# Material 3 · local foundations

Read this table before drawing. Exact native tokens, both theme maps and the pinned source are in [tokens.json](tokens.json).

These are a pinned usable baseline, not a claim about the newest release. Keep a matching project theme or component version when one exists.

Font: **Roboto**. Local preview: Roboto. Check installed fonts before creating text styles; report a substitution once and keep the text editable.

| Semantic purpose | Native token | Light | Dark |
|---|---|---|---|
| Canvas | `--md-sys-color-surface` | `#fef7ff` | `#141218` |
| Surface | `--md-sys-color-surface-container-lowest` | `#fff` | `#0f0d13` |
| Subtle | `--md-sys-color-surface-container` | `#f3edf7` | `#211f26` |
| Text | `--md-sys-color-on-surface` | `#1d1b20` | `#e6e0e9` |
| Secondary text | `--md-sys-color-on-surface-variant` | `#49454f` | `#cac4d0` |
| Primary action | `--md-sys-color-primary` | `#6750a4` | `#d0bcff` |
| On primary | `--md-sys-color-on-primary` | `#fff` | `#381e72` |
| Selection | `--md-sys-color-secondary-container` | `#e8def8` | `#4a4458` |
| On selection | `--md-sys-color-on-secondary-container` | `#1d192b` | `#e8def8` |
| Border | `--md-sys-color-outline-variant` | `#cac4d0` | `#49454f` |
| Focus | `--md-sys-color-primary` | `#6750a4` | `#d0bcff` |
| Error | `--md-sys-color-error` | `#b3261e` | `#f2b8b5` |

## Component specimen recipe

The following px metrics define the local FigCraft specimen; use the retained component source for exact responsive, density and API variants. They are not new global design-system tokens.

| Property | Value (px) |
|---|---|
| buttonHeight | 40 |
| inputHeight | 56 |
| buttonRadius | 9999 |
| inputRadius | 4 |
| panelRadius | 12 |
| bodySize | 14 |
| bodyLineHeight | 20 |
| titleSize | 28 |
| titleLineHeight | 36 |
| gap | 16 |
| rowHeight | 52 |

Keep native names when creating file variables. For dimensional values, resolve rem against the project root (the specimen uses 16px); retain unitless typography line-height as a multiplier. Preserve alias relationships where available in the upstream snapshots. Alpha colours need their alpha channel, not a darker opaque substitute.

Bind background and on-background roles as pairs. Dark mode uses the dark role map, never automatic colour inversion. Specimen layout and content are examples; build the user’s requested screen with the selected system.
