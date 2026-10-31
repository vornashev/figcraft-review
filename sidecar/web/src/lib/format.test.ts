import {describe, expect, it} from "vitest";
import type {Part} from "../api";
import {ago, bytes, fileMeta, groupSteps, md, plural, splitAnswer, tokens} from "./format";

const step = (label: string): Part => ({kind: "step", label, status: "ok"});
const text = (t: string): Part => ({kind: "text", text: t});

describe("words and numbers", () => {
  it("picks the Russian plural", () => {
    const f: [string, string, string] = ["слой", "слоя", "слоёв"];
    expect([1, 2, 5, 11, 21, 22, 112].map((n) => plural(n, f))).toEqual(["1 слой", "2 слоя", "5 слоёв", "11 слоёв", "21 слой", "22 слоя", "112 слоёв"]);
  });
  it("shortens sizes and tokens", () => {
    expect([bytes(900), bytes(4100), bytes(3 << 20), bytes(undefined)]).toEqual(["900 Б", "4 КБ", "3.0 МБ", ""]);
    expect([tokens(42), tokens(17100), tokens(2200000)]).toEqual(["42", "17.1k", "2.2M"]);
    expect(fileMeta({kind: "file", label: "tokens.json", size: 4100})).toBe("JSON · 4 КБ");
    expect([ago(100, 130), ago(0, 7200), ago(0, 3 * 86400)]).toEqual(["сейчас", "2 ч", "3 дн"]);
  });
  it("renders a little Markdown, escaped", () => {
    expect(md("Готово: `x`\n- **a**\n- <b>")).toBe("<p>Готово: <code>x</code></p><ul><li><b>a</b></li><li>&lt;b&gt;</li></ul>");
  });
});

describe("an answer", () => {
  it("puts runs of steps in one card", () => {
    expect(groupSteps([step("a"), step("b"), text("t"), step("c")]).map((b) => b.kind === "steps" ? b.list.length : b.text)).toEqual([2, "t", 1]);
  });
  it("folds what came before the last message", () => {
    const parts = [step("a"), text("смотрю"), step("b"), text("готово")];
    const {head, tail, calls, says} = splitAnswer(parts);
    expect([head.length, tail.length, calls, says]).toEqual([3, 1, 2, 1]);
  });
  it("keeps the latest steps open while the agent works", () => {
    const {head, tail} = splitAnswer([step("a"), step("b")], true);
    expect([head.length, tail.length]).toEqual([0, 2]);
  });
});
