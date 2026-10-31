// Display the platform's modifier; use physical keys so shortcuts survive a layout change.
export const shortcut = (key: string, platform = navigator.platform) => /Mac|iPhone|iPad/.test(platform) ? `⌘${key}` : `Ctrl+${key}`;
export const commandKey = (e: Pick<KeyboardEvent, "ctrlKey" | "metaKey">, platform = navigator.platform) => /Mac|iPhone|iPad/.test(platform) ? e.metaKey : e.ctrlKey;
