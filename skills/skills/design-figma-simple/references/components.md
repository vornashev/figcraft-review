# Simple Design System · component rules

Use Figma SDS semantic aliases and its simple component anatomy. The local light/dark snapshot includes the official React/CSS source as well as the Figma kit link; components can be drawn without first connecting a remote library.

| Component | Properties / anatomy | Local baseline and bindings |
|---|---|---|
| Button | variant: primary, neutral, subtle; size small / medium; optional icon | Medium 40px specimen from 16px label + 12px vertical padding; radius-200 8px; background-brand-default / text-brand-on-brand |
| ButtonDanger | danger-primary / danger-subtle; small / medium | Use the danger component's semantic background/text/border roles; keep destructive actions explicit |
| Input / InputField | Label, optional description, input, error text; invalid / disabled / focus | 40px local recipe; radius-200; default background/text/border; danger border on invalid |
| Card / content panel | Heading, body, optional actions | Background-default-default with border-default-default; space-400/600 for local content rhythm |

Exact CSS values and both alias maps are in tokens.json, with original declarations in `upstream/src/theme.css`. The font is Inter; body-base is 16px, heading is 24px, title-hero is larger. The specimen's 32px page title is a local layout choice. Spacing aliases space-100/200/300/400/600 are 4/8/12/16/24px; radius-100/200/400 are 4/8/16px.

Preserve data-disabled, data-invalid and data-focus-visible states from the source components. Focus uses border-brand-secondary; invalid uses border-danger-default. A linked Figma library receives upstream updates; duplicated files are independent. For FigCraft, build editable variables/styles/variants from this local snapshot rather than waiting for Figma access. React Aria behavior in the code is a reference for accessible controls, not a requirement to put a web runtime into a FigCraft canvas.
