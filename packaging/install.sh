#!/bin/sh
# Puts figcraft-review (the CLI) and figcraft-agent (the chat) on PATH as links into this folder,
# so keep the folder where it is. PREFIX defaults to ~/.local (links in ~/.local/bin).
set -eu
HERE=$(cd "$(dirname "$0")" && pwd)
BIN="${PREFIX:-$HOME/.local}/bin"
mkdir -p "$BIN"
cat >"$BIN/figcraft-review" <<SH
#!/bin/sh
exec python3 "$HERE/agent/review.py" "\$@"
SH
chmod +x "$BIN/figcraft-review"
ln -sf "$HERE/sidecar/figcraft-agent" "$BIN/figcraft-agent"
echo "Installed figcraft-review and figcraft-agent in $BIN"
case ":$PATH:" in *":$BIN:"*) ;; *) echo "Add $BIN to your PATH." ;; esac
command -v python3 >/dev/null || echo "python3 (3.11+) is needed."
command -v figcraft-cli >/dev/null || ls "$HOME"/Applications/figcraft-*.AppImage >/dev/null 2>&1 || echo "figcraft-cli not found: put it on PATH or set FIGCRAFT_CLI."
echo
echo "Plugin: in FigCraft, Plugins > Development > Import plugin from manifest... and pick"
echo "  $HERE/plugin/figcraft-plugin.json"
echo "Start FigCraft with its control channel: figcraft --control 7979"
