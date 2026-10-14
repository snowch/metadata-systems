# Brief BQ: the words for an updated chapter and a reader's saved copy

Read `docs/style.md` for the voice: British English, active voice, short plain sentences, no em
dashes, no marketing tone, no reassurance. The reader is "you". Write each string under its own
`## BQn` heading, exactly as it will appear, and nothing else.

## Facts (every string below relies on these)

- A reader who presses Save (or whose page saves itself) keeps a copy of the chapter in this
  browser. After a reload, the page shows that saved copy.
- Until now, the saved copy was shown even after the chapter was updated. From now on, when the
  page opens, it checks for a newer version of the chapter. If there is one, the page shows the
  new version instead of the saved copy.
- If the reader had changed any cell in the saved copy, the saved copy is not lost: it is kept in
  this browser under a new name, the chapter's file name with "(your copy)" added, for example
  `chapter_05 (your copy).ipynb`.
- If the reader had changed no cell, the saved copy held only the cells' results, which running
  the cells makes again; it is replaced and nothing is kept.
- Kept copies are listed, and open, from the list of files this browser keeps.

## BQ1: a notice at the foot of the screen, shown for five seconds, when the new version replaced a saved copy with no change of the reader's
At most about 60 characters. Says the page now shows the chapter's new version. A full stop at
the end.

## BQ2: the same notice, shown for ten seconds, when the reader's changed copy was kept
At most about 110 characters. Says the page shows the chapter's new version, and that the
reader's saved copy, with their changes, is kept as `{copy}`. Write the placeholder `{copy}`
exactly as written, without backticks: the page puts the copy's file name there, as a link that
opens it.

## BQ3: the third step in the box "Running and saving the page", in every chapter
It replaces this sentence, which is no longer true:

> 3. To keep your changes, press **Save**, or press Ctrl+S (Cmd+S on a Mac). After a reload, the
> page shows your saved copy, which stays in this browser and is shown instead of the chapter,
> even after the chapter is updated.

Start with "3. To keep your changes, press **Save**, or press Ctrl+S (Cmd+S on a Mac)." word for
word. Then, in at most three short sentences: after a reload the page shows your saved copy,
which stays in this browser; when the chapter is updated, the page shows the new version instead;
if you changed a cell, your copy is kept under the chapter's name with "(your copy)" added, and
[the list of files in this browser](FILES) opens it. Keep `[the list of files in this browser](FILES)`
exactly, with `FILES` as written: the address goes in afterwards.
