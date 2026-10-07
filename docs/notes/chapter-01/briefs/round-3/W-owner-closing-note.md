# Brief W: the owner in the closing note, redrafted

Read `common.md` in this directory first. Write your draft to
`docs/notes/chapter-01/drafts/round-3/W.md`.

Your draft of `modelVsRealityOwner` in brief V carried two facts the brief got wrong, and they are
corrected in `docs/notes/chapter-01/facts.md`. Not every database gives a table an owner, so "in a
real database a table's owner is an account too" said too much. In PostgreSQL, other accounts can
be given rights over a table, including the right to give rights on, so "only the owner may let
other accounts use it" said too much as well. Redraft the paragraph from these facts alone.

## modelVsRealityOwner

A new paragraph for the chapter's closing note on how the lab differs from a real platform, in
Markdown. Facts:

- In some real databases a table's owner is an account too.
- In PostgreSQL, for example, a new table's owner is normally the account that created it.
- At first only the owner (or a superuser) can do anything with the table; other accounts can use
  it once they are given the right to.
- The right to alter or drop the table comes with being its owner.
- The lab's warehouse records the owning account and models no such rights.
