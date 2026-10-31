# Contributing

Issues and pull requests are welcome. For anything bigger than a fix, open an issue first so we can agree on the approach.

## Setup

```sh
rustup target add wasm32-unknown-unknown
cargo build --release --target wasm32-unknown-unknown       # the plugin
npm --prefix sidecar/web ci && npm --prefix sidecar/web run build
```

You need FigCraft 0.13+ running with `--control 7979` to try anything end to end. [AGENTS.md](AGENTS.md) is the guide for coding agents working through remarks.

## Tests

| Suite | Command | Needs |
|---|---|---|
| Plugin | `cargo test` | — |
| Lint | `cargo fmt --check`, `cargo clippy --all-targets -- -D warnings`, `ruff check .` | — |
| CLI and chat server | `python3 -m unittest discover -s agent -p 'test_*.py'` and `… -s sidecar …` | — |
| Chat page | `npm --prefix sidecar/web test` (Vitest) | — |
| Chat in a browser | `node sidecar/test_ui.mjs [shot.png]` | Chromium (`CHROMIUM=path` for another binary) |
| With FigCraft | `FIGCRAFT_TEST_FILE=some.figcraft python3 -m unittest agent/test_review.py agent/test_plugin.py` | `figcraft-cli`, the built plugin |

CI runs everything except the last row on Linux, macOS and Windows. Run the FigCraft suite yourself before a release, or when you touch `agent/review.py`, `agent/fc.py` or the plugin.

## Style

- Match the surrounding code: its comment density, naming and idiom. Python uses the standard library only.
- Commit messages are one plain sentence saying what changed and why («Stop looking for docked panels once a FigCraft without them answers»), with no type prefixes.
- Add a line under `## [Unreleased]` in [CHANGELOG.md](CHANGELOG.md) for anything a user would notice. CI checks for one, unless the PR has the `skip-changelog` label.
- The plugin's text and the remark labels are in Russian; keep the labels' format (`#N · text`) intact.

## Releases

The version lives in `Cargo.toml`, `figcraft-plugin.json` and `sidecar/web/package.json`; `scripts/release.py` keeps them equal.

1. On an up-to-date `main` with green CI, run `python3 scripts/release.py 0.6.0` (or `0.6.0-rc.1` for a prerelease). It:
   - bumps the versions
   - moves *Unreleased* into a dated section of the CHANGELOG
   - runs the tests (the FigCraft suite too when `FIGCRAFT_TEST_FILE` is set)
   - commits «Release v0.6.0» and tags it
2. Check the commit, then push it: `git push origin main v0.6.0`.
3. The **Release** workflow builds the plugin and the chat page, then packages the plugin zip and the Linux, macOS and Windows bundles. It smoke-tests each bundle on its own OS, then publishes a GitHub release with the CHANGELOG section as notes, plus `SHA256SUMS` and build provenance.

Versions follow SemVer while still 0.x. A new feature or a change to the CLI, label or export format bumps the minor version; a fix bumps the patch.
