# Fluent 2 · local foundations

Read this table before drawing. Exact native tokens, both theme maps and the pinned source are in [tokens.json](tokens.json).

These are a pinned usable baseline, not a claim about the newest release. Keep a matching project theme or component version when one exists.

Font: **Segoe UI**. Local preview: Roboto (fallback from Fluent font stack). Check installed fonts before creating text styles; report a substitution once and keep the text editable.

| Semantic purpose | Native token | Light | Dark |
|---|---|---|---|
| Canvas | `colorNeutralBackground2` | `#fafafa` | `#1f1f1f` |
| Surface | `colorNeutralBackground1` | `#ffffff` | `#292929` |
| Subtle | `colorNeutralBackground3` | `#f5f5f5` | `#141414` |
| Text | `colorNeutralForeground1` | `#242424` | `#ffffff` |
| Secondary text | `colorNeutralForeground2` | `#424242` | `#d6d6d6` |
| Primary action | `colorBrandBackground` | `#0f6cbd` | `#115ea3` |
| On primary | `colorNeutralForegroundOnBrand` | `#ffffff` | `#ffffff` |
| Selection | `colorBrandBackground2` | `#ebf3fc` | `#082338` |
| On selection | `colorBrandForeground1` | `#0f6cbd` | `#479ef5` |
| Border | `colorNeutralStroke2` | `#e0e0e0` | `#525252` |
| Focus | `colorStrokeFocus2` | `#000000` | `#ffffff` |
| Error | `colorPaletteRedForeground1` | `#bc2f32` | `#e37d80` |

## Component specimen recipe

The following px metrics define the local FigCraft specimen; use the retained component source for exact responsive, density and API variants. They are not new global design-system tokens.

| Property | Value (px) |
|---|---|
| buttonHeight | 32 |
| inputHeight | 32 |
| buttonRadius | 4 |
| inputRadius | 4 |
| panelRadius | 8 |
| bodySize | 14 |
| bodyLineHeight | 20 |
| titleSize | 28 |
| titleLineHeight | 36 |
| gap | 16 |
| rowHeight | 44 |

Keep native names when creating file variables. For dimensional values, resolve rem against the project root (the specimen uses 16px); retain unitless typography line-height as a multiplier. Preserve alias relationships where available in the upstream snapshots. Alpha colours need their alpha channel, not a darker opaque substitute.

Bind background and on-background roles as pairs. Dark mode uses the dark role map, never automatic colour inversion. Specimen layout and content are examples; build the user’s requested screen with the selected system.
