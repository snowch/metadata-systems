# Sceptic's brief: Chapter 1's review findings

A reviewer read Chapter 1 as its learner and wrote `findings.md`. Reviewers over-call. Your job is
to attack each finding before anybody acts on it.

## What to read

- `docs/notes/chapter-01/review/findings.md`: the findings, R1 onwards.
- `docs/notes/chapter-01/review/page.md`: the page as the reviewer saw it.
- To check a claim: `docs/notes/chapter-01/facts.md`, the lab under `packages/lab/src`, the
  chapter's data under `content/lessons/invisible-system*.ts`, the figures under
  `packages/views/src`, and the style checklist `docs/style.md`.

Note: since the reviewer's page was dumped, the managing session changed six things, listed under
"The managing session's read" in `docs/notes/chapter-01.md`. A finding those changes already fix is
"already fixed", not "rejected".

## For each finding, decide

- **Upheld**: the problem is real, for this chapter's learner, and the finding's severity is right.
- **Upheld in part**: real, but smaller or different than stated; say what part holds and the right
  severity.
- **Already fixed**: by one of the six changes above; name it.
- **Rejected**: not a problem, or the reviewer misread the page or the lab; say why, with evidence.

Verify every factual claim yourself, against the lab's code or the chapter's data, not against the
reviewer's word. Quote what you checked. Never include a challenge's answer.

Write `docs/notes/chapter-01/review/verdicts.md`: one entry per finding (R1, R2, ...) with the
verdict, the evidence, and, for an upheld finding, what kind of fix it needs (code, wording, or
both). End with a count of verdicts by kind.
