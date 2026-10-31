import {describe, expect, it} from "vitest";
import {parseSkillSources, sourceEnabled, toggleSkillSource} from "./skillSources";

describe("source chip preferences", () => {
  it("migrates the old single-source choice and preserves all vs none", () => {
    expect(parseSkillSources(null, "pen.dev")).toEqual(["pen.dev"]);
    expect(parseSkillSources(null, "all")).toBeNull();
    expect(parseSkillSources("[]", "hallmark")).toEqual([]);
    expect(parseSkillSources("null", "hallmark")).toBeNull();
    expect(parseSkillSources('{broken')).toBeNull();
    expect(parseSkillSources('["hallmark","hallmark",4,"../bad","typeui"]')).toEqual(["hallmark", "typeui"]);
  });
  it("independently enables sources and can disable the last one", () => {
    const available = ["hallmark", "typeui", "pen.dev"];
    const enabled = toggleSkillSource(null, "pen.dev", available);
    expect(enabled).toEqual(["hallmark", "typeui"]);
    expect(toggleSkillSource(enabled, "hallmark", available)).toEqual(["typeui"]);
    expect(toggleSkillSource(["typeui"], "typeui", available)).toEqual([]);
    expect(toggleSkillSource([], "typeui", available)).toEqual(["typeui"]);
    expect(toggleSkillSource([], "all", available)).toBeNull();
  });
  it("keeps disabled and future sources distinct after saving", () => {
    expect(sourceEnabled(parseSkillSources(JSON.stringify(["hallmark", "typeui"])), "pen.dev")).toBe(false);
    expect(sourceEnabled(parseSkillSources("[]"), "hallmark")).toBe(false);
    expect(sourceEnabled(parseSkillSources("null"), "new-source")).toBe(true);
  });
});
