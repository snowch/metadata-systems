// Copyright © 2026 Christopher Snow

// The front page's notebook links name the notebooks the site builds: each title is its
// notebook's own heading, and each file is what the build writes from that source file.

import { readFileSync } from "node:fs";
import { describe, expect, it } from "vitest";

import { NOTEBOOKS, notebookHref } from "./notebooks";

describe("the chapters' notebooks", () => {
  for (const [chapter, notebooks] of NOTEBOOKS) {
    notebooks.forEach((notebook, i) => {
      it(`chapter ${chapter}'s notebook ${i + 1} is titled as its heading says`, () => {
        const stem = `chapter_${String(chapter).padStart(2, "0")}_part_${i + 1}`;
        expect(notebook.file).toBe(`${stem}.ipynb`);
        const source = readFileSync(`notebook/${stem}.py`, "utf8");
        expect(source).toContain(`# Chapter ${chapter}, part ${i + 1}: ${notebook.title}\n`);
      });
    });
  }

  it("links under the site's base path", () => {
    const [first] = NOTEBOOKS.get(1) ?? [];
    expect(first && notebookHref("/metadata-systems/", first)).toBe(
      "/metadata-systems/jupyterlite/notebooks/index.html?path=chapter_01_part_1.ipynb",
    );
  });
});
