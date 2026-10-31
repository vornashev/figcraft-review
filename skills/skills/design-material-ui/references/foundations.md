# Material UI · local foundations

Read this table before drawing. Exact native tokens, both theme maps and the pinned source are in [tokens.json](tokens.json).

These are a pinned usable baseline, not a claim about the newest release. Keep a matching project theme or component version when one exists.

Font: **Roboto**. Local preview: Roboto. Check installed fonts before creating text styles; report a substitution once and keep the text editable.

| Semantic purpose | Native token | Light | Dark |
|---|---|---|---|
| Canvas | `palette.background.default` | `#fff` | `#121212` |
| Surface | `palette.background.paper` | `#fff` | `#121212` |
| Subtle | `palette.action.hover` | `rgba(0, 0, 0, 0.04)` | `rgba(255, 255, 255, 0.08)` |
| Text | `palette.text.primary` | `rgba(0, 0, 0, 0.87)` | `#fff` |
| Secondary text | `palette.text.secondary` | `rgba(0, 0, 0, 0.6)` | `rgba(255, 255, 255, 0.7)` |
| Primary action | `palette.primary.main` | `#1976d2` | `#90caf9` |
| On primary | `palette.primary.contrastText` | `#fff` | `rgba(0, 0, 0, 0.87)` |
| Selection | `palette.action.selected` | `rgba(0, 0, 0, 0.08)` | `rgba(255, 255, 255, 0.16)` |
| On selection | `palette.text.primary` | `rgba(0, 0, 0, 0.87)` | `#fff` |
| Border | `palette.divider` | `rgba(0, 0, 0, 0.12)` | `rgba(255, 255, 255, 0.12)` |
| Focus | `palette.primary.main` | `#1976d2` | `#90caf9` |
| Error | `palette.error.main` | `#d32f2f` | `#f44336` |

## Component specimen recipe

The following px metrics define the local FigCraft specimen; use the retained component source for exact responsive, density and API variants. They are not new global design-system tokens.

| Property | Value (px) |
|---|---|
| buttonHeight | 36 |
| inputHeight | 56 |
| buttonRadius | 4 |
| inputRadius | 4 |
| panelRadius | 4 |
| bodySize | 14 |
| bodyLineHeight | 20 |
| titleSize | 24 |
| titleLineHeight | 32 |
| gap | 16 |
| rowHeight | 52 |

Keep native names when creating file variables. For dimensional values, resolve rem against the project root (the specimen uses 16px); retain unitless typography line-height as a multiplier. Preserve alias relationships where available in the upstream snapshots. Alpha colours need their alpha channel, not a darker opaque substitute.

Bind background and on-background roles as pairs. Dark mode uses the dark role map, never automatic colour inversion. Specimen layout and content are examples; build the user’s requested screen with the selected system.
