import {describe, expect, it} from "vitest";
import {parseSkillPrefs} from "./skillPrefs";

describe("saved skill preferences", () => {
  it("recovers from unavailable or malformed storage", () => {
    for (const value of [null, "{broken", "[]", '{"favorites":2,"recent":false}']) expect(parseSkillPrefs(value)).toEqual({favorites: [], recent: []});
  });
  it("keeps names unique and caps recent history", () => {
    const data = parseSkillPrefs(JSON.stringify({favorites: ["almanac", "almanac", 4, "../bad", "opendesign-example"], recent: Array.from({length: 30}, (_, i) => `skill-${i}`)}));
    expect(data.favorites).toEqual(["almanac", "opendesign-example"]);
    expect(data.recent).toHaveLength(20);
    expect(data.recent[0]).toBe("skill-0");
  });
});
