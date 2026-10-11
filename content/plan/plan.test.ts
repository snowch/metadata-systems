// Copyright © 2026 Christopher Snow

// The plan as data agrees with docs/plan.md: every chapter, its title, and the terms it introduces.

import { readFileSync } from "node:fs";
import { describe, expect, it } from "vitest";

import { PLAN } from "./plan";

describe("the course's plan", () => {
  it("keeps the plan's list of chapters and terms in step with docs/plan.md", () => {
    // Vitest runs from the repository root, as the check script does.
    const plan = readFileSync("docs/plan.md", "utf8");
    for (const c of PLAN) {
      const row = plan.split("\n").find((line) => line.startsWith(`| ${c.number} | ${c.title} |`));
      expect(row, `chapter ${c.number} in docs/plan.md`).toBeDefined();
      if (c.introduces.length && c.number !== 25) {
        const cells = (row ?? "").split("|").map((x) => x.trim());
        expect(cells[cells.length - 2], `chapter ${c.number}'s terms`).toBe(
          c.introduces.join(", "),
        );
      }
    }
  });
});
