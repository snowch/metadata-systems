# Review brief: one chapter of Part VI (Chapters 24 to 28)

You review one chapter of *Metadata Systems*, an interactive course, as a demanding reader and
technical editor. Read `CLAUDE.md` (binding: especially "Interaction is the explanation",
"Experiments, instruments and explanations", "Question the requirement", "Voice" and "What no
check can catch"), `AGENTS.md`, `docs/style.md` and `docs/prompts/review-learner-facing-prose.md`.

Read the chapter as built, `docs/notes/chapter-NN/review/chapter_NN-as-built.md`: its Markdown
cells in order, each code cell's code marked `>>>` followed by what it prints after **Run all**, the
cells the reader writes in marked `[WRITE]`, and the requirement's box marked `[BOX]`. Read it as a
learner who has done every earlier chapter and none after. In Part VI the reader writes code: each
piece's cell starts as a version that runs and answers wrong, and the outputs in the file are from
those starting versions. The page then says what to change and what the check shows after. The
finished versions are `REFERENCE` in the chapter's module; run them to check what the page says the
check shows after the change. You may read the earlier chapters
(`notebook/chapter_01.py` to `notebook/chapter_23.py`, and Part VI's earlier chapters), the chapter's
notes (`docs/notes/chapter-NN.md`), `docs/plan.md`, `docs/sources.md`, and the engine
(`notebook/shop/`, especially `store.py`, `collector.py`, `lineage_graph.py`, `query.py`, `interface.py`, and `docs/notes/part-6/design.md`).
To check what a cell prints, run Python from `/home/user/metadata-systems/notebook`, for example
`python3 -c "import shop; w = shop.run_week(['returns']); print(shop.delivery.send(w))"`.

Rules for findings:

- Every finding quotes the page exactly.
- A finding names the problem and suggests a direction. Never rewrite the text.
- Check a number or a cross-reference against the engine or the earlier chapters before you assert
  it is wrong; say what you ran.
- Never write an exercise's or a prediction's answer as a suggestion.
- Sort findings into BLOCKING (wrong, misleading, or breaks a binding rule), SHOULD and COULD.
- Ask whether each piece of code the reader writes is the right size for a phone, whether the page
  says clearly what to change without giving the code, and whether the check's lines tell a reader
  whose code is wrong what to look at.
- Look especially for: a claim about OpenLineage or a real system that `docs/sources.md` does not
  support; a number stated with no cell that shows it; a prediction its page does not justify, or
  whose options or nearby text give its answer away; a term used before it is defined, or a word
  used with two meanings; a sentence the learner would not miss; a cell whose output does not show
  what the next paragraph says it shows.

Return the findings as your final message, as Markdown, headed "REVIEW OF CHAPTER NN, "<title>"",
with a first line saying which numbers you checked and how. Do not write any file.
