// Copyright © 2026 Christopher Snow

// The written chapters, each a notebook: Chapters 1 to 23. Each is built from notebook/chapter_NN.py
// into the site under jupyterlite/ (notebook/jupyterlite/build.sh), and the front page's title of
// the chapter opens it; notebooks.test.ts checks each notebook's heading against the plan's title.

/** A chapter's notebook: its file in the JupyterLite site's contents, by chapter number. */
export const NOTEBOOKS: ReadonlyMap<number, string> = new Map([
  [1, "chapter_01.ipynb"],
  [2, "chapter_02.ipynb"],
  [3, "chapter_03.ipynb"],
  [4, "chapter_04.ipynb"],
  [5, "chapter_05.ipynb"],
  [6, "chapter_06.ipynb"],
  [7, "chapter_07.ipynb"],
  [8, "chapter_08.ipynb"],
  [9, "chapter_09.ipynb"],
  [10, "chapter_10.ipynb"],
  [11, "chapter_11.ipynb"],
  [12, "chapter_12.ipynb"],
  [13, "chapter_13.ipynb"],
  [14, "chapter_14.ipynb"],
  [15, "chapter_15.ipynb"],
  [16, "chapter_16.ipynb"],
  [17, "chapter_17.ipynb"],
  [18, "chapter_18.ipynb"],
  [19, "chapter_19.ipynb"],
  [20, "chapter_20.ipynb"],
  [21, "chapter_21.ipynb"],
  [22, "chapter_22.ipynb"],
  [23, "chapter_23.ipynb"],
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
