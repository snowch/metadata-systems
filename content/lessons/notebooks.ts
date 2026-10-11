// Copyright © 2026 Christopher Snow

// The chapters that are also notebooks: Chapter 1 as two Jupyter notebooks, built from
// notebook/chapter_01_part_1.py and _part_2.py into the site under jupyterlite/
// (notebook/jupyterlite/build.sh). The front page links each under its chapter's line; the
// content tests check each title against its notebook's own heading.

export interface ChapterNotebook {
  /** The notebook's title, as its heading gives it after "Chapter N, part M: ". */
  readonly title: string;
  /** The notebook's file in the JupyterLite site's contents. */
  readonly file: string;
}

export const NOTEBOOKS: ReadonlyMap<number, readonly ChapterNotebook[]> = new Map([
  [
    1,
    [
      { title: "The shop and its platform", file: "chapter_01_part_1.ipynb" },
      {
        title: "Thursday's revenue and what the platform cannot say",
        file: "chapter_01_part_2.ipynb",
      },
    ],
  ],
]);

/** A notebook's address, under the site's base path. */
export const notebookHref = (base: string, notebook: ChapterNotebook) =>
  `${base}jupyterlite/notebooks/index.html?path=${notebook.file}`;
