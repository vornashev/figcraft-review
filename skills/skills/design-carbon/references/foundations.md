# Carbon · local foundations

Read this table before drawing. Exact native tokens, both theme maps and the pinned source are in [tokens.json](tokens.json).

These are a pinned usable baseline, not a claim about the newest release. Keep a matching project theme or component version when one exists.

Font: **IBM Plex Sans**. Local preview: IBM Plex Sans. Check installed fonts before creating text styles; report a substitution once and keep the text editable.

| Semantic purpose | Native token | Light | Dark |
|---|---|---|---|
| Canvas | `background` | `#ffffff` | `#161616` |
| Surface | `layer01` | `#f4f4f4` | `#262626` |
| Subtle | `layer02` | `#ffffff` | `#393939` |
| Text | `textPrimary` | `#161616` | `#f4f4f4` |
| Secondary text | `textSecondary` | `#525252` | `#c6c6c6` |
| Primary action | `buttonPrimary` | `#0f62fe` | `#0f62fe` |
| On primary | `textOnColor` | `#ffffff` | `#ffffff` |
| Selection | `layerSelected01` | `#e0e0e0` | `#393939` |
| On selection | `textPrimary` | `#161616` | `#f4f4f4` |
| Border | `borderSubtle01` | `#c6c6c6` | `#525252` |
| Focus | `focus` | `#0f62fe` | `#ffffff` |
| Error | `supportError` | `#da1e28` | `#fa4d56` |

## Component specimen recipe

The following px metrics define the local FigCraft specimen; use the retained component source for exact responsive, density and API variants. They are not new global design-system tokens.

| Property | Value (px) |
|---|---|
| buttonHeight | 48 |
| inputHeight | 40 |
| buttonRadius | 0 |
| inputRadius | 0 |
| panelRadius | 0 |
| bodySize | 14 |
| bodyLineHeight | 20 |
| titleSize | 28 |
| titleLineHeight | 36 |
| gap | 16 |
| rowHeight | 48 |

Keep native names when creating file variables. For dimensional values, resolve rem against the project root (the specimen uses 16px); retain unitless typography line-height as a multiplier. Preserve alias relationships where available in the upstream snapshots. Alpha colours need their alpha channel, not a darker opaque substitute.

Bind background and on-background roles as pairs. Dark mode uses the dark role map, never automatic colour inversion. Specimen layout and content are examples; build the user’s requested screen with the selected system.
