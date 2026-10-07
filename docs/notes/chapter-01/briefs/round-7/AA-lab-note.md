# Brief AA: the lab's note

Read `docs/notes/chapter-01/briefs/round-4/common.md` first, and the files it names: every rule
there holds for this brief. Write your draft to `docs/notes/chapter-01/drafts/round-7/AA.md`.

The author read the lab's note and could not tell from it what the lab is, whether its data sits
in the browser's storage, what the dates mean, or how a reader gets to the lab. This is the note
it replaces:

> Every figure in this chapter runs the Metadata Lab, a small data platform in your browser. The
> lab holds the shop's files and tables for the week of 7 to 13 September 2026. Its programs run
> in SQL over the rows you see. What a figure shows is worked out from those rows each time. The
> lab's clock is the week's own, not real time. Nothing leaves your browser.

## labNote

The note, in Markdown, names in backticks. It opens from every figure's badge, below a short note
on what that figure asks of you, and closes each chapter under the heading "How the figures run",
so it must read well in both places and say nothing about any one figure or chapter. One or two
short paragraphs, no more than 130 words. No list, no heading. The facts are in
`docs/notes/chapter-01/facts.md`, under "The Metadata Lab, as its note describes it". Carry every
one of them, in this order:

- what the lab is, that it comes with the page as code, and that it runs in your browser, with
  nothing to install, open or sign in to;
- that you use it through the figures, and the three examples of how;
- what it holds, and that it reads and runs SQL itself, with a query engine of its own, the
  queries you build included;
- that nothing about the shop is stored: each time the page loads, the lab builds the data and
  runs the whole week in memory, so the rows and times are the same for every reader on any day;
- what the week is, with its dates, and that the shop and its week are invented;
- that every date and time a figure shows comes from that week, whose last night ends early on
  Monday 14 September, never from today's date or your computer's clock;
- that your browser keeps your own work, and that nothing you do leaves your browser.

Do not:

- say how many programs there are, which asset a program reads or writes, or what any program
  does;
- say "this chapter" or "this page": the note serves every chapter;
- use these words: metadata (except in the name "the Metadata Lab"), simulate or simulation,
  schema, dataset, job, event, lineage, environment; or "run" as a noun (as a verb it is fine:
  "runs the week").
