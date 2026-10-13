# Sceptic's brief: one chapter of Part VI

A reviewer read one chapter of *Metadata Systems* and wrote findings
(`docs/notes/chapter-NN/review/findings.md`). Reviewers over-call. Your job is to attack each finding
independently, and decide whether it should be acted on.

Read `CLAUDE.md` (binding), `AGENTS.md` and `docs/style.md`; the chapter as built
(`docs/notes/chapter-NN/review/chapter_NN-as-built.md`) and its source (`notebook/chapter_NN.py`);
its notes (`docs/notes/chapter-NN.md`); and whatever earlier chapter, engine module
(`notebook/shop/`) or source (`docs/sources.md`) a finding cites. Run Python from
`/home/user/metadata-systems/notebook` to check any claim about what a cell prints
(`python3 -c "import shop; ..."`).

For each finding, in order, give one verdict:

- UPHELD: the finding is right and matters; say what the fix must achieve (a direction, not wording).
- PARTLY UPHELD: say exactly which part stands and which does not, and why.
- REJECTED: say why (wrong, already handled on the page, against a decision recorded in
  `docs/plan.md` or the notes, a convention every chapter keeps, or not worth its cost).

Check every factual claim a finding makes before you uphold it: say what you ran or read. Prefer the
smallest change that meets the course's rules. Where a finding asks for a new figure or a new engine
feature, weigh whether the chapter needs it or whether a sentence does the job. Never write an
exercise's answer as a fix.

Return the verdicts as your final message, as Markdown, headed "VERDICTS ON THE CHAPTER NN FINDINGS",
with a first line counting upheld, partly upheld and rejected. Do not write any file.
