# shadcn/ui · local foundations

Read this table before drawing. Exact native tokens, both theme maps and the pinned source are in [tokens.json](tokens.json).

These are a pinned usable baseline, not a claim about the newest release. Keep a matching project theme or component version when one exists.

Font: **Geist**. Local preview: Geist. Check installed fonts before creating text styles; report a substitution once and keep the text editable.

| Semantic purpose | Native token | Light | Dark |
|---|---|---|---|
| Canvas | `background` | `oklch(1 0 0)` | `oklch(0.145 0 0)` |
| Surface | `card` | `oklch(1 0 0)` | `oklch(0.205 0 0)` |
| Subtle | `muted` | `oklch(0.97 0 0)` | `oklch(0.269 0 0)` |
| Text | `foreground` | `oklch(0.145 0 0)` | `oklch(0.985 0 0)` |
| Secondary text | `muted-foreground` | `oklch(0.556 0 0)` | `oklch(0.708 0 0)` |
| Primary action | `primary` | `oklch(0.205 0 0)` | `oklch(0.922 0 0)` |
| On primary | `primary-foreground` | `oklch(0.985 0 0)` | `oklch(0.205 0 0)` |
| Selection | `accent` | `oklch(0.97 0 0)` | `oklch(0.269 0 0)` |
| On selection | `accent-foreground` | `oklch(0.205 0 0)` | `oklch(0.985 0 0)` |
| Border | `border` | `oklch(0.922 0 0)` | `oklch(1 0 0 / 10%)` |
| Focus | `ring` | `oklch(0.708 0 0)` | `oklch(0.556 0 0)` |
| Error | `destructive` | `oklch(0.577 0.245 27.325)` | `oklch(0.704 0.191 22.216)` |

## Component specimen recipe

The following px metrics define the local FigCraft specimen; use the retained component source for exact responsive, density and API variants. They are not new global design-system tokens.

| Property | Value (px) |
|---|---|
| buttonHeight | 36 |
| inputHeight | 36 |
| buttonRadius | 8 |
| inputRadius | 8 |
| panelRadius | 14 |
| bodySize | 14 |
| bodyLineHeight | 20 |
| titleSize | 24 |
| titleLineHeight | 32 |
| gap | 16 |
| rowHeight | 48 |

Keep native names when creating file variables. For dimensional values, resolve rem against the project root (the specimen uses 16px); retain unitless typography line-height as a multiplier. Preserve alias relationships where available in the upstream snapshots. Alpha colours need their alpha channel, not a darker opaque substitute.

Bind background and on-background roles as pairs. Dark mode uses the dark role map, never automatic colour inversion. Specimen layout and content are examples; build the user’s requested screen with the selected system.
