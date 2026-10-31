# Fluent 2 · component rules

Use semantic alias tokens over global colour values. The bundled webLightTheme/webDarkTheme represent Fluent 2 web; do not combine Fluent 1 assets or mobile measurements with them.

| Component | Properties / anatomy | Local baseline and bindings |
|---|---|---|
| Button | appearance: primary, secondary, subtle; small / medium / large; optional icon; disabled | Medium 32px recipe, borderRadiusMedium 4px; primary uses colorBrandBackground / colorNeutralForegroundOnBrand |
| Input | Label is a separate field element; value, placeholder, validation; outline / underline / filled treatment | Medium 32px, small 24px, large 40px; colorNeutralForeground1, colorNeutralStroke1; retain branded bottom focus treatment |
| Field | Label, required indicator, control, validation message | Keep label and validation attached to the control; error uses colorPaletteRedForeground1 |
| Tab / navigation item | Icon, label, selected state, focus | Selected colour roles are colorBrandBackground2 / colorBrandForeground1; selection and hover are different variants |

Read `upstream/Button.styles.js` and `upstream/Input.styles.js` for the shipped component styling and states. Font and spacing keys are in tokens.json: fontSizeBase300 14px, lineHeightBase300 20px, fontWeightSemibold 600, spacingHorizontalM 12px, borderRadiusMedium 4px. Larger headings use fontSizeHero700 / lineHeightHero700 (28/36).

The intended UI font is Segoe UI. Local previews use Roboto, an explicit fallback in Fluent's published font stack; do not rename it Segoe UI in the design. For primary hover/pressed/disabled states use their named semantic tokens rather than changing brightness. Keyboard focus uses colorStrokeFocus1 / colorStrokeFocus2. Keep the focus indicator visible independently of selection.
