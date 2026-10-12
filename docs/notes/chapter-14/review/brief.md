# Review brief for Chapters 14 to 17 (Part IV)

You review one chapter of an interactive course on metadata systems. Read as a learner who has done
every earlier chapter and none after. Your job is the reading half of a review (`CLAUDE.md`,
"Reviewing a chapter"): find what is wrong, unclear, unsupported or against the course's rules.

Read first, in this order:

1. `CLAUDE.md` (the binding rules), `docs/style.md`, `docs/prompts/review-learner-facing-prose.md`.
2. The chapter as built after Run all: `docs/notes/chapter-NN/review/chapter_NN-as-built.md`
   (Markdown cells, visible code cells, and each cell's output). Its source is
   `notebook/chapter_NN.py`.
3. The chapter's notes, `docs/notes/chapter-NN.md`, which state each figure's purpose.
4. Earlier chapters as needed to check what the learner already knows (`notebook/chapter_01.py` to
   the chapter before), and the engine that computes every number (`notebook/shop/`, in particular
   `quality.py`, `provenance.py`, `impact.py`, `cause.py` and `week.py`). Run Python from
   `/home/user/metadata-systems/notebook` (`import shop; shop.run_week([...])`) to check any number
   before you assert it.

Look for, among others: a wrong or unsupported claim (a number, a run, a time, what a table holds,
what a standard says, checked against `docs/sources.md`); a prediction the page does not equip the
learner to make, or whose answer is in view or given away; an option or prompt that carries the
explanation; a cause asked for before its effect; a term used before it is introduced or defined in
a way that fails a case the course meets; a word that means two things on the page ("figure" is an
interactive box only; a number is a total, a value or a count); a definite article before something
not introduced; filler, reassurance, personification, narration of the course, signposting, slogans;
the same point made twice; a requirement section that marks a reasonable reading wrong; a closing
that does not summarise what the experiments showed and could not show; anything a phone reader
would trip on in a table or a printed output.

Rules for findings:

- Every finding quotes the page exactly.
- A finding suggests a direction; it never rewrites the text.
- Check a number or a cross-reference before you assert it; say how you checked.
- Never include an exercise's answer beyond what the page itself shows.
- Rank findings: BLOCKING (wrong, misleading, or breaks a rule), then SHOULD, then COULD. Be
  sparing: a finding you are unsure of is a COULD.

Write your findings to `docs/notes/chapter-NN/review/findings.md`, headed
`REVIEW OF CHAPTER NN, "<title>" (read as a learner who has done Chapters 1 to NN-1)`, then a
sentence on whether the numbers are right, then the findings, numbered, each with **Where**,
**Problem** and **Direction**. Write only that file. Do not edit anything else. Send no messages.
