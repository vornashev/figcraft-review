# Gravity UI · component rules

Use the --g-* token namespaces and the matching UIKit 8 snapshot. Keep compact service controls and the actual yellow brand contrast pair. Existing project branding overrides this default through the same roles.

| Component | Properties / anatomy | Local baseline and bindings |
|---|---|---|
| Button | view: normal, action, outlined, flat; size xs / s / m / l / xl; optional icon | Heights 20 / 24 / 28 / 36 / 44px in the retained CSS; m radius uses --g-border-radius-m 6px |
| TextInput | size, value, placeholder, label/helper outside the input, validation, clear control | m 28px recipe; --g-color-text-primary; --g-color-line-generic; --g-color-line-focus |
| Table | Header, row data, sorting, selection, toolbar when needed | Compact 40px row specimen; --g-color-base-selection for selected rows; preserve column alignment |
| Label / status | Text plus optional icon; status tone | Use matching base/text status roles: danger, positive, warning, info; do not assign the brand yellow to every status |

The complete resolved theme snapshot is local in tokens.json; original aliases are in `upstream/default.css`. Common typography is Inter, body-1 13px/18px, body-short 13px/16px; the specimen uses header-1 24px/28px. Radii are xs=3, s=5, m=6, l=8, xl=10px. Check `upstream/Button.css` and `upstream/TextInput.css` for all size and interaction rules.

Use `--g-color-base-brand` with `--g-color-text-brand-contrast`, preserving the dark text on yellow in both bundled modes. Input focus, selected list rows and hover each have separate tokens. For code, read the project's installed @gravity-ui package version before using APIs; version 8 migration may change names or theming entrypoints. Additional chart/navigation packages are separate from UIKit.
