# Review brief: Chapters 3 and 4, first read (12 October 2026)

You review one chapter of an interactive course, *Metadata Systems*, for data engineers. Each
chapter is a Jupyter notebook: prose, with cells the reader runs and changes. Read as a learner who
has done every earlier chapter and none after: a competent software or data engineer.

## What to read

- The binding rules: `CLAUDE.md` (all of it, and above all "Voice", "Interaction is the
  explanation", "Experiments, instruments and explanations", "Question the requirement" and "What
  no check can catch"), `AGENTS.md` ("The writing standard") and
  `docs/prompts/review-learner-facing-prose.md`.
- The earlier chapters as a learner met them: `docs/notes/chapter-02/review/round-17/` holds
  Chapter 1 and 2 as built (`chapter_01-after-reviews.md`, `chapter_02-after-reviews.md`). Read
  Chapter 2's last sections at least: the chapter you review continues from them.
- Your chapter as built, run in full: `chapter_0N-as-built.md` is the page after **Run all**, before
  the reader changes anything; `chapter_0N-after-the-edit.md` is the page after the change the
  chapter asks for (Chapter 3: the five lines of dots filled in from the two messages; Chapter 4:
  `Jo Marsh` and `Sam Lund` changed to `j.marsh` and `s.lund`). "[hidden code cell]" is setup the
  reader does not see. `[figure]` is a drawn diagram, with its caption.
- The source, if you need it: `notebook/chapter_0N.py`. The chapter's notes: `docs/notes/chapter-0N.md`.

## What to look for

Everything in the review prompt, and in particular:

- whether each cell the reader changes is clear about what to change, and whether the page after
  **Run all** (before the change) misleads;
- whether any prose, output or cell above a question gives its answer away, or asks for a cause
  before the effect is shown;
- whether a term is used before the page introduces it, or a word means two things on the page
  (*record*, *field*, *owner*, *model*, *check*, *schema*);
- whether a claim overstates what the evidence shows;
- sentences the learner would not miss; joins between paragraphs that repeat or break;
- whether the closing questions lead somewhere and carry no answer;
- any number or cross-reference that you can check against the outputs or the earlier chapters:
  check it before you assert it.

## How to report

Write your findings to the file named in your task, as a numbered list. Each finding: the quoted
words from the page (exactly), where they are (section), the problem in one or two sentences, and a
direction for the fix. Do not rewrite the passage: suggest a direction. Do not put an exercise's
answer in a finding. Rank the findings, most serious first, and mark each **blocking** (wrong,
misleading, or breaks a binding rule) or **minor**. End with what you read and anything you could
not check.
