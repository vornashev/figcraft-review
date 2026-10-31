# Hotkeys

FigCraft plugins can't use the clipboard or register their own hotkeys. So the quick actions are commands, and you bind them to keys in your desktop:

| Action | Command | Suggested key |
|---|---|---|
| Add a remark to the selection | `figcraft-review annotate` | Super+Alt+N |
| Copy the open remarks for an agent | `figcraft-review --copy` | Super+Alt+A |
| Open the agent chat | `figcraft-agent` | Super+Alt+I |

From a source checkout, use `python3 agent/review.py` and `sidecar/figcraft-agent` instead of the installed names.

## Linux

**Hyprland** (`hyprland.conf`):

```ini
bind = SUPER ALT, N, exec, figcraft-review annotate
bind = SUPER ALT, A, exec, figcraft-review --copy
bind = SUPER ALT, I, exec, figcraft-agent
```

FigCraft answers only while it gets frames. On Hyprland a window on a hidden workspace gets none, so keep it drawing:

```ini
windowrule = render_unfocused, class:ai.storyteller.figcraft
```

With a Lua config (`hyprland.lua`):

```lua
hl.window_rule({ name = "figcraft-render", match = { class = "ai.storyteller.figcraft" }, render_unfocused = true })
```

`figcraft-agent` moves the chat window to FigCraft's workspace when `hyprctl` is there.

**GNOME**: Settings ▸ Keyboard ▸ Custom Shortcuts, one entry per command. **KDE**: System Settings ▸ Shortcuts ▸ Add New ▸ Command.

## macOS

Use Shortcuts.app: a new shortcut with **Run Shell Script** (`/bin/zsh -lc 'figcraft-review --copy'`), then **Add Keyboard Shortcut** in its details. Or use [skhd](https://github.com/koekeishiya/skhd) (`~/.skhdrc`):

```
cmd + alt - n : figcraft-review annotate
cmd + alt - a : figcraft-review --copy
cmd + alt - i : figcraft-agent
```

The first dialog or notification asks for the Automation permission for `osascript`.

## Windows

With [AutoHotkey v2](https://www.autohotkey.com/) (`figcraft.ahk`):

```autohotkey
#!n::Run "figcraft-review.cmd annotate", , "Hide"
#!a::Run "figcraft-review.cmd --copy", , "Hide"
#!i::Run "figcraft-agent.cmd", , "Hide"
```

Or right-click a shortcut to the `.cmd` file ▸ Properties ▸ Shortcut key.
