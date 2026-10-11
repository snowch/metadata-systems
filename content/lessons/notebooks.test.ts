// Copyright © 2026 Christopher Snow

// The chapters' notebooks: each is built from the source file of its number, and is headed with its
// chapter's number and the plan's title.

import { readFileSync } from "node:fs";
import { describe, expect, it } from "vitest";

import { NOTEBOOKS, notebookHref } from "./notebooks";
import { PLAN } from "./plan";

describe("the chapters' notebooks", () => {
  for (const [chapter, file] of NOTEBOOKS) {
    it(`chapter ${chapter}'s notebook is headed with the plan's title`, () => {
      const stem = `chapter_${String(chapter).padStart(2, "0")}`;
      expect(file).toBe(`${stem}.ipynb`);
      const title = PLAN.find((c) => c.number === chapter)?.title;
      const source = readFileSync(`notebook/${stem}.py`, "utf8");
      expect(source).toContain(`# Chapter ${chapter}: ${title}\n`);
    });
  }

  it("links under the site's base path", () => {
    expect(notebookHref("/metadata-systems/", "chapter_01.ipynb")).toBe(
      "/metadata-systems/jupyterlite/notebooks/index.html?path=chapter_01.ipynb",
    );
  });
});
