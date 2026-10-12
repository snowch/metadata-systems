# Review brief: one chapter of Part V (Chapters 18 to 23)

You review one chapter of *Metadata Systems*, an interactive course, as a demanding reader and
technical editor. Read `CLAUDE.md` (binding: especially "Interaction is the explanation",
"Experiments, instruments and explanations", "Question the requirement", "Voice" and "What no
check can catch"), `AGENTS.md`, `docs/style.md` and `docs/prompts/review-learner-facing-prose.md`.

Read the chapter as built, `docs/notes/chapter-NN/review/chapter_NN-as-built.md` (its Markdown
cells in order, code cells marked `<<CODE>>`, the requirement's box marked `[BOX]`), as a learner
who has done every earlier chapter and none after. You may read the earlier chapters
(`notebook/chapter_01.py` to `notebook/chapter_17.py`, and Part V's earlier chapters), the chapter's
notes (`docs/notes/chapter-NN.md`), `docs/plan.md`, `docs/sources.md`, and the engine
(`notebook/shop/`, especially `delivery.py`, `ingest.py`, `claims.py`, `aliases.py`, `scale.py`).
To check what a cell prints, run Python from `/home/user/metadata-systems/notebook`, for example
`python3 -c "import shop; w = shop.run_week(['returns']); print(shop.delivery.send(w))"`.

Rules for findings:

- Every finding quotes the page exactly.
- A finding names the problem and suggests a direction. Never rewrite the text.
- Check a number or a cross-reference against the engine or the earlier chapters before you assert
  it is wrong; say what you ran.
- Never write an exercise's or a prediction's answer as a suggestion.
- Sort findings into BLOCKING (wrong, misleading, or breaks a binding rule), SHOULD and COULD.
- Look especially for: a claim about OpenLineage or a real system that `docs/sources.md` does not
  support; a number stated with no cell that shows it; a prediction its page does not justify, or
  whose options or nearby text give its answer away; a term used before it is defined, or a word
  used with two meanings; a sentence the learner would not miss; a cell whose output does not show
  what the next paragraph says it shows.

Return the findings as your final message, as Markdown, headed "REVIEW OF CHAPTER NN, "<title>"",
with a first line saying which numbers you checked and how. Do not write any file.
