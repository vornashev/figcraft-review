# Material 3 · component rules

Material 3 baseline: keep primary/on-primary and surface/on-surface pairs. Use the selected component shape token; pill buttons do not imply pill text fields. The bundled snapshot is the Web baseline v0.192, not M3 Expressive.

| Component | Properties / anatomy | Local baseline and bindings |
|---|---|---|
| Filled button | Label, optional leading icon; enabled, hover, focus, pressed, disabled | 40px container; corner-full; primary / on-primary; label-large |
| Outlined text field | Floating label, editable value, optional leading/trailing icon, supporting/error text | 56px recipe, corner-extra-small; on-surface text; outline border; primary focus; error validation |
| Switch | Track, thumb, selected / unselected, focus, disabled | 52×32 track in the baseline source; preserve thumb/track roles and state layers |
| Checkbox | Mark inside control; checked, unchecked, indeterminate, disabled | Use source checkbox tokens; control appearance and hit area are separate dimensions |
| Navigation rail | Destination icon and label, selected indicator | 80px container width in the retained snapshot; secondary-container / on-secondary-container indicator |

Read `upstream/tokens/_md-comp-*.scss` for the exact component token mapping. Typography is in the `--md-sys-typescale-*` keys of tokens.json; shape in `--md-sys-shape-*`. Use headline-medium for the specimen's 28/36 heading, body-medium for 14/20 copy, label-large for button text. Material spacing recipes use the document's 4px-based scale rather than inventing a named upstream spacing token.

Disabled filled button: on-surface at 12% for container and 38% for label; hover/focus use the state-layer opacity tokens. Preserve opacity as an alpha channel. Create state variants for the controls the user actually needs. Material UI is a separate library; do not claim its components implement this baseline automatically.
