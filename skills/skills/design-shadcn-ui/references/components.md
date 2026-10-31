# shadcn/ui · component rules

The local baseline is Neutral / New York v4, with editable component source. Existing components.json, local components and CSS variables define the project; do not overwrite them to match a newer generic style.

| Component | Properties / anatomy | Local baseline and bindings |
|---|---|---|
| Button | variant: default, destructive, outline, secondary, ghost, link; size; optional icon | default 36px, sm 32px, lg 40px; default radius 8px from rounded-md; primary / primary-foreground |
| Input | Value/placeholder, validation, disabled, focus; label and helper are separate | 36px source height; input border; ring focus; destructive invalid state |
| Card | Header/title/description, content, optional footer | card / card-foreground, border; rounded-xl = 14px with the snapshot's base radius 10px |
| Tabs / table / block | Reuse actual local implementations; selected surface and content roles | accent / accent-foreground, muted / muted-foreground and semantic border; keep keyboard behavior from the chosen primitive library |

Native theme values use OKLCH. Keep that colour space or convert it through a real colour conversion when binding FigCraft colours; do not interpret OKLCH channels as RGB. Background/foreground and primary/primary-foreground are pairs. Base radius is 0.625rem (10px at 16px); rounded-md is radius minus 2px and rounded-xl is radius plus 4px in this baseline.

The specimen uses bundled Geist for readable 14/20 copy; font choice is a local recipe, not a universal shadcn requirement. Read the retained button.tsx, input.tsx and card.tsx to match the actual variant names, sizes and focus classes. Newer base styles and alternative primitive libraries can differ; compare the installed component source before implementation. Community Figma kits are optional references, not a prerequisite for using the skill.
