# Changelog

All notable changes to this project are documented here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and the project uses [Semantic Versioning](https://semver.org/). The `#N · text` annotation label and the Markdown export are public formats: changes to them go under **Changed**.

## [Unreleased]

First public release.

### Added

- Remarks as native FigCraft annotations: `#N · text`, with the status as the category (Открыто, Вопрос, Проверь, Готово, Отклонено) and replies from the agent.
- `agent/review.py`:
  - Markdown export of the open remarks for a coding agent, with optional context screenshots
  - the agent's loop: `next`, `show`, `done`, `ask` with options, `reject`, `reply`
  - the designer's side: `accept`, `reopen`
  - `annotate` and `--copy` for hotkeys
- FigCraft plugin (plugin API 3): a **Review** widget on the canvas and a **Remark…** panel.
- Agent chat (`sidecar/`) for Claude Code, Codex and pi:
  - context from the selection, @-mentions, remarks and images
  - one history per file, with undo per answer
  - agents in several files at once, each in its own headless FigCraft
  - variants (×N) with an orchestrator
  - a **Замечания** tab and FigCraft comment threads
- Design skills for the chat's agents:
  - Hallmark's 50 themes
  - better-*
  - seven design systems (Material 3, Fluent 2, Carbon, Gravity UI, Material UI, shadcn/ui, Figma Simple Design System)
  - TypeUI, tweakcn and UI UX Pro Max styles
  - a skill library with search, sources, favourites and reference previews
- `skills/opendesign.py` imports OpenDesign's prompt bundles into your own skills; the chat's **Источники** popup runs it with **Скачать** / **Обновить** and shows the progress.
- The FigCraft Review app for Windows (a per-user setup `.exe`) and macOS (a `.dmg` for Apple silicon and Intel), with its own Python:
  - one click starts FigCraft with its control port, imports or updates the plugin, starts the chat and opens it
  - a tray / menu-bar icon: open the chat, copy the remarks, add a remark, start FigCraft, updates
  - updates from GitHub Releases in one click, checked against `SHA256SUMS`; the chat shows a banner when one is out
  - on macOS, `figcraft-cli` for the installed FigCraft is downloaded once
- Linux, macOS and Windows support:
  - clipboard, dialogs, notifications and process handling per OS (`agent/desktop.py`)
  - a Python launcher for the chat (`sidecar/launch.py`) with `figcraft-agent` / `figcraft-agent.cmd` wrappers
  - install scripts in the release bundles

### Fixed

- Windows: agents, figcraft-cli and the MCP bridge no longer open console windows.
- Windows: the chat's agents got no FigCraft tools ("No such tool available") because the MCP bridge wrote in the system code page and crashed on the first non-ASCII tool description (in 0.5.0-rc.1).

[Unreleased]: https://github.com/vornashev/figcraft-review/commits/main
