# Third-party content

FigCraft Review's own code is MIT (see [LICENSE](LICENSE)). The design skills under `skills/skills/` are adapted from other projects; each folder has an `ATTRIBUTION.md` with the exact source and revision, and a `LICENSE` where the upstream one applies.

| Skills | Source | License |
|---|---|---|
| `hallmark`, `hallmark-*` (51) | [nutlope/hallmark](https://github.com/nutlope/hallmark) @ `8f6969f`, themes and preview pictures | MIT |
| `better-*` (7) | [jakubkrehel/skills](https://github.com/jakubkrehel/skills) @ `d01493b` | MIT |
| `tweakcn-*` (42) | [jnsahaj/tweakcn](https://github.com/jnsahaj/tweakcn) @ `a3b47b3`, theme presets | Apache-2.0 |
| `typeui-*` (67) | [bergside/awesome-design-skills](https://github.com/bergside/awesome-design-skills) @ `f631a09` | MIT |
| `uipro-*` (79) | [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) @ `28b3b8d` | MIT |
| `design-*` (7) | Own instructions; theme values from the design systems' npm packages (`@carbon/themes`, `@fluentui/tokens`, `@gravity-ui/uikit`, `@material/web`, `@mui/material`), named with versions in each `ATTRIBUTION.md` | upstream license in `references/upstream/LICENSE` |
| fonts in `design-*/assets/fonts` | Inter, IBM Plex Sans, Roboto, Geist via [Fontsource](https://fontsource.org) | OFL-1.1 (`assets/fonts/LICENSE`) |

Not in this repository:

- **OpenDesign** prompts and reference images are not licensed for redistribution. `python3 skills/opendesign.py` imports them into your own skills (`~/.config/figcraft-agent/skills`).

The Windows and macOS installers carry a Python runtime from [python-build-standalone](https://github.com/astral-sh/python-build-standalone) (CPython: PSF-2.0, with the licences of its bundled libraries in `python/`), and the tray app's packages: [pystray](https://github.com/moses-palmer/pystray) (LGPL-3.0, unmodified; its source is on PyPI), [Pillow](https://github.com/python-pillow/Pillow) (MIT-CMU), six (MIT) and, on macOS, [PyObjC](https://github.com/ronaldoussoren/pyobjc) (MIT). On macOS the app downloads `figcraft-cli` from [storytold/figcraft](https://github.com/storytold/figcraft) (Apache-2.0) when it first runs.

The chat page (`sidecar/web`) bundles React and React DOM (MIT), `@mdi/js` (Apache-2.0), and Golos Text and JetBrains Mono (OFL-1.1) from Fontsource. The plugin links [figcraft-plugin-sdk](https://github.com/storytold/figcraft).
