import {describe, expect, it} from "vitest";
import {moveInSkillGrid} from "./skillGrid";

const cards = (columns: number, count: number) => Array.from({length: count}, (_, i) => ({left: (i % columns) * 240, top: Math.floor(i / columns) * 300, width: 220}));

describe("skill grid keyboard movement", () => {
  it("moves horizontally and wraps between the first and last card", () => {
    const grid = cards(3, 8);
    expect(moveInSkillGrid(grid, 2, "ArrowRight")).toBe(3);
    expect(moveInSkillGrid(grid, 0, "ArrowLeft")).toBe(7);
    expect(moveInSkillGrid(grid, 7, "ArrowRight")).toBe(0);
  });
  it("moves by visual rows and chooses the closest column in a partial row", () => {
    const grid = cards(3, 8);
    expect(moveInSkillGrid(grid, 1, "ArrowDown")).toBe(4);
    expect(moveInSkillGrid(grid, 5, "ArrowDown")).toBe(7);
    expect(moveInSkillGrid(grid, 4, "ArrowUp")).toBe(1);
    expect(moveInSkillGrid(grid, 1, "ArrowUp")).toBe(7);
  });
  it("handles changed column counts and gaps between skill groups", () => {
    expect(moveInSkillGrid(cards(2, 6), 1, "ArrowDown")).toBe(3);
    const grid = [...cards(2, 2), {left: 0, top: 360, width: 220}];
    expect(moveInSkillGrid(grid, 1, "ArrowDown")).toBe(2);
    expect(moveInSkillGrid(cards(1, 3), 0, "ArrowDown")).toBe(1);
    expect(moveInSkillGrid([], 0, "ArrowDown")).toBe(0);
  });
});
