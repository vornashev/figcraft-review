# FigCraft Review

[![CI](https://github.com/vornashev/figcraft-review/actions/workflows/ci.yml/badge.svg)](https://github.com/vornashev/figcraft-review/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/vornashev/figcraft-review?include_prereleases)](https://github.com/vornashev/figcraft-review/releases)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

AI-first design remarks for [FigCraft](https://github.com/storytold/figcraft). Point at a layer and say what's wrong. One keystroke copies every open remark for a coding agent, and you watch the agent tick them off right where you left them. A chat beside FigCraft lets Claude Code, Codex or pi edit the design directly.

Runs on Linux, macOS and Windows. The interface and remark labels are in Russian.

A remark is a native FigCraft annotation (Dev Mode, Shift+D):

```
#7 · Кнопка налезает на край          the number and the text
↳ Claude: увеличил padding до 16      replies
```

Its category is the status: **Открыто** (open), **Вопрос** (question), **Проверь** (the agent says it's fixed: check it), **Готово** (the designer accepted it) or **Отклонено** (rejected). The categories are created on first use. Nothing is kept outside the document, so the remarks survive without this tool.

## What's inside

| Part | What it is |
|---|---|
| **Plugin** (`src/`, Rust → wasm) | A **Review** widget on the canvas that lists the open remarks, and a **Remark…** panel for adding them |
| **CLI** (`agent/review.py`) | Exports remarks as Markdown for an agent; the agent's side of the loop (`next`, `done`, `ask`…) |
| **Agent chat** (`sidecar/`) | A chat window with Claude Code, Codex or pi that edits the open file over MCP: context from the selection, undo per answer, variants, a remarks tab |
| **Design skills** (`skills/`) | About 250 style, design-system and quality skills the chat's agents use (see [THIRD_PARTY.md](THIRD_PARTY.md)) |

## Install

### Windows and macOS: the app

1. Install [FigCraft](https://github.com/storytold/figcraft/releases) **0.13** or newer, and at least one agent CLI: [Claude Code](https://docs.anthropic.com/en/docs/claude-code), [Codex](https://github.com/openai/codex) or pi.
2. From [Releases](https://github.com/vornashev/figcraft-review/releases), download:
   - Windows: `FigCraftReview-Setup-vX.Y.Z.exe`
   - macOS: `FigCraftReview-vX.Y.Z-macos-arm64.dmg` (Apple silicon) or `-x64.dmg` (Intel)
3. Run it:
   - Windows: run the setup. It installs for you alone, without admin rights.
   - macOS: drag **FigCraft Review** to Applications.
4. Open **FigCraft Review**. It does the rest:
   - starts FigCraft with its control port
   - imports the plugin, and updates it later
   - starts the chat
   - adds an icon to the tray (menu bar on macOS) with the quick actions: open the chat, copy the remarks, add a remark

The builds aren't signed yet, so the first start needs one extra step:
- **Windows** says «Windows protected your PC»: click **More info ▸ Run anyway**.
- **macOS** says the app can't be opened: open **System Settings ▸ Privacy & Security** and click **Open Anyway** beside FigCraft Review.

**Updates.** The app checks GitHub once a day. When there's a new version, the tray menu and the chat offer **Обновить** (Update). The app downloads the new version, checks it against the release's `SHA256SUMS`, installs it and restarts. The extra first-start step isn't needed again.

FigCraft has to run with the control port: start it from FigCraft Review, not from its own icon. If it's already open without the port, the app tells you to close it and press **Запустить FigCraft** (Start FigCraft) in the tray.

What's bundled: the app carries its own Python, so there's nothing else to install. On macOS it downloads `figcraft-cli` for your FigCraft version once.

### Requirements for the other ways

- [FigCraft](https://github.com/storytold/figcraft/releases) **0.13** or newer, started with the control channel: `figcraft --control 7979`
- `figcraft-cli` on `PATH`, or set `FIGCRAFT_CLI`. It comes with the Linux and Windows packages; on macOS download `figcraft-cli-<v>-macos-universal.zip`
- Python **3.11+** (standard library only; `pystray` and `Pillow` add the tray icon)
- For the chat: at least one agent CLI ([Claude Code](https://docs.anthropic.com/en/docs/claude-code), [Codex](https://github.com/openai/codex) or pi) and a Chromium-family browser (Chrome, Edge, Chromium or Brave) for the app window. Without one, the chat opens in the default browser
- Node.js 20+ only when building from source

### Linux, or from a terminal

Download the bundle for your OS from [Releases](https://github.com/vornashev/figcraft-review/releases) and unpack it:

```sh
# Linux / macOS
tar xzf figcraft-review-v0.5.0-linux.tar.gz && cd figcraft-review && ./install.sh
```

```powershell
# Windows
Expand-Archive figcraft-review-v0.5.0-windows.zip .; cd figcraft-review
powershell -ExecutionPolicy Bypass -File install.ps1
```

The install script puts `figcraft-review` (the CLI) and `figcraft-agent` (the chat) on your `PATH`. It then shows where the plugin's manifest is. Import it in FigCraft with **Plugins ▸ Development ▸ Import plugin from manifest…**.

If you only want the plugin, `figcraft-review-plugin-vX.Y.Z.zip` has the manifest and the `.wasm` module. It's the same for every OS.

### From source

```sh
git clone https://github.com/vornashev/figcraft-review && cd figcraft-review
rustup target add wasm32-unknown-unknown
cargo build --release --target wasm32-unknown-unknown   # the plugin
npm --prefix sidecar/web ci && npm --prefix sidecar/web run build   # the chat page
```

Then import `figcraft-plugin.json` in FigCraft. Re-import it after every rebuild.

## Loop

1. **Annotate.** Select a layer and run `review.py annotate` (bind it to a key, see [docs/hotkeys.md](docs/hotkeys.md)). Type the remark and press Enter. The **Remark…** panel works too, and so does a plain annotation in Dev Mode: it gets the next number.
2. **Copy.** `review.py --copy` copies the open remarks. Pasted, they look like this:

   ```
   # FigCraft — design · 2 замечания
   Поправь макет в FigCraft по этим замечаниям. Значения бери из дизайн-системы файла … Сделал — `review.py done N "что сделано"` …
   ---
   ## 1. Сделать заголовок крупнее
   - **Слой:** `TEXT` «Title» · #812
   - **Путь:** Сцена · Обычное › ◇Окно › Header › Title
   - **Компонент:** Окно · обычное
   - **Текст:** "Mihomo"
   - **Размер:** 120×24
   ```

   An agent with FigCraft access can also run `agent/review.py` itself (see [AGENTS.md](AGENTS.md)).
3. **The agent fixes and reports.** `review.py done N "what changed"` moves the remark to «Проверь». `ask N "question" --option A --option B` moves it to «Вопрос». The status and the reply show on the widget, in the panel and in Dev Mode. The next export leaves both out, because they wait for you.
4. **Check.** Use the chat's **Замечания** tab: pick an answer to a question (1, 2…), compare «было/стало» (before/after), then **Принять** (Enter) or **Вернуть** with a comment. You can also run `review.py accept N` / `reopen N "…"`, or click a badge on the widget to tick a remark off or reopen it.

## CLI (`agent/review.py`)

| Command | Does |
|---|---|
| `review.py [--all] [--shots] [--copy]` | Prints the open remarks as the Markdown above (`--all`: every remark; `--shots`: a PNG of each remark's context in the temp folder; `--copy`: to the clipboard as well). Numbers new annotations |
| `review.py annotate` | Asks for a remark on the selection in a dialog and adds it |
| `review.py list` | One line per remark |
| `review.py next` / `show N` | The first open remark / one remark in full. An agent's loop is next → fix → done |
| `review.py add [ID] TEXT` | Adds a remark on layer ID or on the selection |
| `review.py done\|ask\|reject\|reopen\|reply\|accept N TEXT [--as NAME] [--option X…]` | Sets the status and adds a reply (default author: Claude). done → Проверь, ask → Вопрос (with options), accept → Готово, reopen → Открыто |

The CLI attaches to the running app through `figcraft-cli mcp --attach` (port `FIGCRAFT_PORT`, 7979 by default). Other variables:

- `FIGCRAFT_FILE=x.figcraft`: open that file headless instead (nothing is saved)
- `FIGCRAFT_DOCUMENT=<path or id>`: act on that open file, whatever tab is in front
- `FIGCRAFT_AGENT=<name>`: who FigCraft says acts (comments are signed «<name> (agent)»)

Clipboard, dialogs and notifications use the system's own tools: `pbcopy`/`osascript` on macOS, PowerShell on Windows, `wl-copy`/`xclip` and `zenity`/`kdialog` with `notify-send` on Linux.

## Plugin

A FigCraft plugin built on the same annotations (Rust → `wasm32-unknown-unknown`, plugin API 3).

- **Review** widget (Plugins menu): a card on the canvas with a row per open remark. Each row shows the number badge in the status colour, the layer, the text and the last reply (a question in yellow).
  - Clicking a badge switches the remark between done and open; clicking a row goes to its layer.
  - **Готовые N** shows the closed remarks; ↻ redraws.
  - `review.py` clicks ↻ on every Review widget after a change, so the agent's ticks appear there.
- **Remark…** panel:
  - shows the selected layer, the text and **Добавить #N**
  - lists the remarks, open first; picking one goes to its layer
  - **Готово** / **Вернуть в работу**, **Удалить**

  A panel gets no selection events, so it reads the selection again when you type or press ↻.

Plugins have no clipboard access or hotkeys of their own. That's why copying and quick annotating are done by `review.py`, bound to keys.

## Agent chat (`sidecar/`)

`figcraft-agent` (`figcraft-agent.cmd` on Windows) starts the chat's server if needed and opens the chat window. You can talk to Claude Code, Codex or pi with this context:

- the selection, @-mentioned layers and remarks, pasted images
- one history per file

The agent edits the design through MCP. Each answer's changes are shown and undone in one click. Agents can work in several files at once: each file gets its own headless FigCraft in the app's live session, so FigCraft can stay out of sight. The chat also has a **Замечания** tab for answering and accepting remarks. See [sidecar/README.md](sidecar/README.md).

More skills: **Скачать** beside OpenDesign in the chat's **Источники** popup (or `python3 skills/opendesign.py`) imports OpenDesign's 230 prompt bundles into your own skills (`~/.config/figcraft-agent/skills`). They aren't licensed for redistribution, so they don't ship here.

## Development

See [CONTRIBUTING.md](CONTRIBUTING.md) for the test suites, the changelog and how releases are made. The concept screens live on the «Агент» page of `design/review-ux.figcraft`; `design/*.py` draws them.

## License

MIT, see [LICENSE](LICENSE). The bundled design skills keep their own licences: see [THIRD_PARTY.md](THIRD_PARTY.md).
