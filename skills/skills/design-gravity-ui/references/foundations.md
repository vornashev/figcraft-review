# Gravity UI · local foundations

Read this table before drawing. Exact native tokens, both theme maps and the pinned source are in [tokens.json](tokens.json).

These are a pinned usable baseline, not a claim about the newest release. Keep a matching project theme or component version when one exists.

Font: **Inter**. Local preview: Inter. Check installed fonts before creating text styles; report a substitution once and keep the text editable.

| Semantic purpose | Native token | Light | Dark |
|---|---|---|---|
| Canvas | `--g-color-base-background` | `rgb(255 255 255)` | `rgb(34,29,34)` |
| Surface | `--g-color-base-background` | `rgb(255 255 255)` | `rgb(34,29,34)` |
| Subtle | `--g-color-base-generic` | `rgb(0 0 0 / 0.05)` | `rgb(255 255 255 / 0.1)` |
| Text | `--g-color-text-primary` | `rgb(0 0 0 / 0.85)` | `rgb(255 255 255 / 0.85)` |
| Secondary text | `--g-color-text-secondary` | `rgb(0 0 0 / 0.5)` | `rgb(255 255 255 / 0.5)` |
| Primary action | `--g-color-base-brand` | `rgb(255 190 92)` | `rgb(255 190 92)` |
| On primary | `--g-color-text-brand-contrast` | `rgb(0 0 0 / 0.85)` | `rgb(0 0 0 / 0.9)` |
| Selection | `--g-color-base-selection` | `rgb(255 190 92 / 0.3)` | `rgb(255 190 92 / 0.2)` |
| On selection | `--g-color-text-primary` | `rgb(0 0 0 / 0.85)` | `rgb(255 255 255 / 0.85)` |
| Border | `--g-color-line-generic` | `rgb(0 0 0 / 0.1)` | `rgb(255 255 255 / 0.15)` |
| Focus | `--g-color-line-focus` | `rgb(107 132 153 / 0.8)` | `rgb(96 128 156 / 0.8)` |
| Error | `--g-color-text-danger` | `rgb(233 3 58)` | `rgb(229 50 93)` |

## Component specimen recipe

The following px metrics define the local FigCraft specimen; use the retained component source for exact responsive, density and API variants. They are not new global design-system tokens.

| Property | Value (px) |
|---|---|
| buttonHeight | 28 |
| inputHeight | 28 |
| buttonRadius | 6 |
| inputRadius | 6 |
| panelRadius | 8 |
| bodySize | 13 |
| bodyLineHeight | 18 |
| titleSize | 24 |
| titleLineHeight | 28 |
| gap | 16 |
| rowHeight | 40 |

Keep native names when creating file variables. For dimensional values, resolve rem against the project root (the specimen uses 16px); retain unitless typography line-height as a multiplier. Preserve alias relationships where available in the upstream snapshots. Alpha colours need their alpha channel, not a darker opaque substitute.

Bind background and on-background roles as pairs. Dark mode uses the dark role map, never automatic colour inversion. Specimen layout and content are examples; build the user’s requested screen with the selected system.
