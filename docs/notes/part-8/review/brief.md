# Review brief: Chapter 33, "Build the whole thing"

You review the course's last chapter of *Metadata Systems*, an interactive course, as a demanding
reader and technical editor. Read `CLAUDE.md` (binding: especially "Interaction is the
explanation", "Experiments, instruments and explanations", "Question the requirement", "Voice" and
"What no check can catch"), `AGENTS.md`, `docs/style.md` and
`docs/prompts/review-learner-facing-prose.md`.

Read the chapter as built, `docs/notes/chapter-33/review/chapter_33-as-built.md`: its Markdown cells
in order, each code cell's code marked `>>>` followed by what it prints after **Run all**, the cells
the reader writes in marked `[WRITE]`, and the requirements' boxes marked `[BOX]`. The figure of the
ferry's four systems is drawn before anything runs and is not in that file: read
`notebook/shop/figures.py` (`ferry_platform`, `FERRY_FLOWS`) and its caption in
`notebook/chapter_33.py`. Read as a learner who has done every earlier chapter (1 to 32) and none
after.

The chapter gives the reader a second platform, an island ferry's, invented for the course: no real
system runs or is described. The reader changes two cells, `inputs(change)` and `suspect(run)`,
each starting with code whose check fails; the outputs in the file come from that starting code,
and the page says what to change and what the check shows after. The finished code is `REFERENCE`
in `notebook/shop/ferry.py`; run it to check what the page says.

You may read the earlier chapters (`notebook/chapter_01.py` to `notebook/chapter_32.py`), the
chapter's notes (`docs/notes/chapter-33.md`), `docs/plan.md`, `docs/sources.md` (especially "Read for
Part VIII"), `docs/notes/part-8/design.md`, and the engine (`notebook/shop/ferry.py`, `collector.py`,
`lineage_graph.py`). To check what a cell prints, run Python from
`/home/user/metadata-systems/notebook`, for example
`python3 -c "import shop; f = shop.ferry.run(); print(shop.ferry.compare_counts(f, '2026-09-24', 'island'))"`.

Rules for findings:

- Every finding quotes the page exactly.
- A finding names the problem and suggests a direction. Never rewrite the text.
- Check a number or a cross-reference against the code or the earlier chapters before you assert it
  is wrong; say what you ran.
- Never write an exercise's or a prediction's answer as a suggestion.
- Sort findings into BLOCKING (wrong, misleading, or breaks a binding rule), SHOULD and COULD.
- Ask whether the page says clearly what to change, whether the check's lines tell a reader whose
  code is wrong what to look at, whether each prediction is a belief the reader can hold from what
  the page has shown, and whether the three requirements are each questioned before the page builds
  to them.
- Look especially for: a claim about OpenLineage that `docs/sources.md` does not support; a number
  stated with no cell that shows it; a prediction whose page or nearby output gives its answer away
  beyond the course's convention that answer cells print below the prediction after **Run all**; a
  term used before it is defined, or a word used with two meanings (*run*, *version*, *batch*,
  *record*, *table*); a sentence the learner would not miss; a cell whose output does not show what
  the next paragraph says it shows; a passage that only holds after the reader's change, read
  before it.
- As the last chapter, ask whether it asks for almost everything at once, as `docs/plan.md` says:
  model, instrument, capture, ingest, schemas, quality, a failure, an impact and a provenance.

Return the findings as your final message, as Markdown, headed "REVIEW OF CHAPTER 33, "Build the
whole thing"", with a first line saying which numbers you checked and how. Do not write any file.
