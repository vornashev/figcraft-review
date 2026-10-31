# Simple Design System · local foundations

Read this table before drawing. Exact native tokens, both theme maps and the pinned source are in [tokens.json](tokens.json).

These are a pinned usable baseline, not a claim about the newest release. Keep a matching project theme or component version when one exists.

Font: **Inter**. Local preview: Inter. Check installed fonts before creating text styles; report a substitution once and keep the text editable.

| Semantic purpose | Native token | Light | Dark |
|---|---|---|---|
| Canvas | `--sds-color-background-default-secondary` | `#f5f5f5` | `#2c2c2c` |
| Surface | `--sds-color-background-default-default` | `#ffffff` | `#1e1e1e` |
| Subtle | `--sds-color-background-default-secondary` | `#f5f5f5` | `#2c2c2c` |
| Text | `--sds-color-text-default-default` | `#1e1e1e` | `#ffffff` |
| Secondary text | `--sds-color-text-default-secondary` | `#757575` | `#ffffffb2` |
| Primary action | `--sds-color-background-brand-default` | `#2c2c2c` | `#f5f5f5` |
| On primary | `--sds-color-text-brand-on-brand` | `#f5f5f5` | `#1e1e1e` |
| Selection | `--sds-color-background-brand-tertiary` | `#f5f5f5` | `#444444` |
| On selection | `--sds-color-text-brand-default` | `#2c2c2c` | `#f5f5f5` |
| Border | `--sds-color-border-default-default` | `#d9d9d9` | `#444444` |
| Focus | `--sds-color-border-brand-default` | `#2c2c2c` | `#f5f5f5` |
| Error | `--sds-color-text-danger-default` | `#900b09` | `#fdd3d0` |

## Component specimen recipe

The following px metrics define the local FigCraft specimen; use the retained component source for exact responsive, density and API variants. They are not new global design-system tokens.

| Property | Value (px) |
|---|---|
| buttonHeight | 40 |
| inputHeight | 40 |
| buttonRadius | 8 |
| inputRadius | 8 |
| panelRadius | 8 |
| bodySize | 16 |
| bodyLineHeight | 24 |
| titleSize | 32 |
| titleLineHeight | 38 |
| gap | 16 |
| rowHeight | 48 |

Keep native names when creating file variables. For dimensional values, resolve rem against the project root (the specimen uses 16px); retain unitless typography line-height as a multiplier. Preserve alias relationships where available in the upstream snapshots. Alpha colours need their alpha channel, not a darker opaque substitute.

Bind background and on-background roles as pairs. Dark mode uses the dark role map, never automatic colour inversion. Specimen layout and content are examples; build the user’s requested screen with the selected system.
