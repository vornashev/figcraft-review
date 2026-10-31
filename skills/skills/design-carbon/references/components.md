# Carbon · component rules

Use Carbon layers, type and spacing tokens with the white or g100 theme. Preserve square control geometry, strong alignment and purposeful density. Button colours come from component tokens, not the interactive text token.

| Component | Properties / anatomy | Local baseline and bindings |
|---|---|---|
| Button | kind: primary, secondary, tertiary, ghost, danger; size and optional trailing icon | lg 48px specimen, 0 radius; buttonPrimary / textOnColor; component hover/active/disabled tokens are in tokens.json |
| Text input | Label above the field, value, optional helper and validation indicator | 40px specimen, 0 radius; field01 or layer01 fill; bottom rule; focus and supportError tokens |
| Data table | Toolbar, header, rows, selection, sort indicator, pagination as needed | Choose a single density; row fill layer01, layerSelected01 for selection, borderSubtle01 for separators |
| Content switcher / tabs | Selected and unselected content modes, focus | Show selection by the documented indicator and surface; do not use an arbitrary rounded pill |

Native colours, spacing01–spacing13 and exported type styles are in tokens.json. Use body01 for 14px/20px prose, bodyCompact01 for denser 14px/18px rows, heading04 for the 28px/36px specimen heading. Unitless line-height values in Carbon's type exports multiply the font size; they are not px. Prefer IBM Plex Sans, retaining its family name and reporting an actual substitution if needed.

Create file variables using the native names, plus light/dark modes corresponding to white/g100. Layer01 and layer02 express depth; they are not interchangeable decorative greys. Button hover/active/disabled colours are retained in `upstream/button-tokens.js`; keep disabled labels and focus rings distinct from the filled surface. A screenshot is a reference, never a single flattened dashboard image.
