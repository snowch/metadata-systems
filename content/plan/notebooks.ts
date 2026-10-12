// Copyright © 2026 Christopher Snow

// The written chapters, each a notebook: Chapters 1 to 4. Each is built from notebook/chapter_0N.py
// into the site under jupyterlite/ (notebook/jupyterlite/build.sh), and the front page's title of
// the chapter opens it; notebooks.test.ts checks each notebook's heading against the plan's title.

/** A chapter's notebook: its file in the JupyterLite site's contents, by chapter number. */
export const NOTEBOOKS: ReadonlyMap<number, string> = new Map([
  [1, "chapter_01.ipynb"],
  [2, "chapter_02.ipynb"],
  [3, "chapter_03.ipynb"],
  [4, "chapter_04.ipynb"],
]);

/** A notebook's address, under the site's base path. */
export const notebookHref = (base: string, file: string) =>
  `${base}jupyterlite/notebooks/index.html?path=${file}`;

/**
 * The chapters' former pages, by the id their address carried (#/chapter/<id>), and the chapter
 * each was: the shell sends such an address to the chapter's notebook. The pages went on 11 October
 * 2026, when the author kept only the notebooks.
 */
export const CHAPTER_PAGES: ReadonlyMap<string, number> = new Map([
  ["shop-and-platform", 1],
  ["invisible-data-system", 2],
]);
