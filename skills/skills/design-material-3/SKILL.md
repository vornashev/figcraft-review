---
name: design-material-3
description: "Create and edit interfaces within Material 3 when selected for a chat or message. Use bundled light/dark tokens, typography, component recipes and previews; preserve project-specific theme overrides."
metadata:
  group: "system"
  category: "design-systems"
  origin: "design-resources"
  mode: "manual"
  title: "Material 3"
  summary: "Google: семантические токены, компоненты и Material 3 Design Kit"
  resource_kind: "system"
  formats: "figma code"
  resource_source: "official"
  access: "free"
---

# Material 3

When this skill is selected for a chat, apply it to subsequent turns; when attached to a message, apply it to that turn. Complete the requested interface in this system. The local specification is available without a network connection or a Figma account.

## Read before designing

- [Foundations](references/foundations.md): semantic role bindings, typography and local specimen metrics.
- [Component rules](references/components.md): anatomy, sizes, variants and state treatment for this system.
- [Token snapshot](references/tokens.json): exact native names and resolved light/dark values; use it when creating or binding variables.
- [Visual previews](references.json): open the matching light or dark image to understand the component finish. Images are locally rendered specimens, not upstream screenshots or finished screen templates.

Material 3 baseline: keep primary/on-primary and surface/on-surface pairs. Use the selected component shape token; pill buttons do not imply pill text fields. The bundled snapshot is the Web baseline v0.192, not M3 Expressive.

## Apply in FigCraft

Inspect the target frame, existing variables, text styles and components. Reuse those that belong to the selected system. If this is a new screen without foundations, create a named **Material 3** variable collection with light/dark modes from the needed native tokens, text styles from the local type roles, and reusable components for repeated controls. Bind values instead of scattering raw colours and sizes. Keep variable names traceable to tokens.json.

Compose the user's actual content and workflow using these controls. Use auto-layout, constraints, editable text, component properties and variants. Create the required default, hover, focus, pressed, disabled, selected and error states as applicable to each control; do not invent every possible variant. An existing project theme belonging to this system wins over the bundled default. A different established system should be replaced only where the user's request calls for it.

Check installed fonts and report a substitution once. Preserve colour-space and opacity semantics when converting tokens to file values. The preview's layout and sample content are illustrative: do not paste it as one image or force every task into its composition. Code snippets and upstream source are implementation references; a FigCraft screen does not need a web framework to be drawn.

Before finishing, inspect the rendered frame at its target size: text fits, spacing follows the chosen scale, theme pairs retain contrast, controls use consistent density, and focus/validation are visible. Check bindings and component instances, not just the screenshot. When also editing code, match the project's installed package version and local wrappers before applying APIs from the pinned snapshot.

## Sources

The local baseline and retained original files are documented in [ATTRIBUTION.md](ATTRIBUTION.md). Consult external sources only for components or versions not covered locally:

- [Документация Material 3](https://m3.material.io/)
- [Material 3 Design Kit · Figma](https://www.figma.com/community/file/1035203688168086460/material-3-design-kit)
- [Токены](https://m3.material.io/foundations/design-tokens/overview)
