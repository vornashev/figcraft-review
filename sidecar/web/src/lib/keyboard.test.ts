import {describe, expect, it} from "vitest";
import {commandKey, shortcut} from "./keyboard";

describe("platform shortcuts", () => {
  it("uses readable Ctrl on Linux and Windows, Command on macOS", () => {
    expect([shortcut(",", "Linux x86_64"), shortcut("N", "Win32"), shortcut(",", "MacIntel")]).toEqual(["Ctrl+,", "Ctrl+N", "⌘,"]);
    expect(commandKey({ctrlKey: true, metaKey: false}, "Linux x86_64")).toBe(true);
    expect(commandKey({ctrlKey: false, metaKey: true}, "MacIntel")).toBe(true);
    expect(commandKey({ctrlKey: false, metaKey: true}, "Win32")).toBe(false);
  });
});
