// Copyright © 2026 Christopher Snow

// The chapters that are also notebooks: Chapters 1 and 2. Each is built from
// notebook/chapter_0N.py into the site under jupyterlite/ (notebook/jupyterlite/build.sh). The
// front page links each under its chapter's line, or from the line of a chapter with no page; the
// content tests check each notebook's heading against the plan's title.

/** A chapter's notebook: its file in the JupyterLite site's contents, by chapter number. */
export const NOTEBOOKS: ReadonlyMap<number, string> = new Map([
  [1, "chapter_01.ipynb"],
  [2, "chapter_02.ipynb"],
]);

/** A notebook's address, under the site's base path. */
export const notebookHref = (base: string, file: string) =>
  `${base}jupyterlite/notebooks/index.html?path=${file}`;
