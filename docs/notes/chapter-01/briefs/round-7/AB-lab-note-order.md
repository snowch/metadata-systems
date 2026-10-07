# Brief AB: the lab's note, in the order a reader needs it

Read `docs/notes/chapter-01/briefs/round-4/common.md` first, and the files it names: every rule
there holds for this brief. Write your draft to `docs/notes/chapter-01/drafts/round-7/AB.md`.

The author found the note on the page unclear. This is the note now:

> The Metadata Lab is a small data platform written for this course. It comes as code with the
> page and runs in your browser: nothing to install, open or sign in to.
>
> You use it through figures, each asking the lab something and showing its answer. A figure
> showing storage reads what the lab records. A query you build, the lab runs. You change the
> shop and the lab runs the week again. The lab holds the shop's files, tables and a dashboard,
> with real rows. Programs written in SQL run each night and write the tables and dashboard. The
> lab reads and runs that SQL with its own query engine, and your queries the same way.
>
> Nothing about the shop is stored. Each time the page loads, the lab builds the data and runs
> the whole week in memory. Rows and times are the same for every reader. The week is the shop's
> first week online: Monday 7 to Sunday 13 September 2026, invented for the course. Every date and
> time a figure shows comes from that week, ending early Monday 14 September, not today or your
> clock. Your browser keeps your predictions, choices and answers. Nothing you do leaves your
> browser.

What is wrong with it:

- "the week" and "each night" appear in the second paragraph, and the reader learns what the week
  is only in the third. A reader cannot follow a sentence about something not yet introduced. The
  fault was the first brief's: it put the examples of using the lab before what the lab holds.
- "A query you build, the lab runs." puts the object first, and a reader stumbles on it.
- How you use the lab is mixed into the same paragraph as what it holds.

## labNote

The note, in Markdown, names in backticks. It opens from every figure's badge, below a short note
on what that figure asks of you, and closes each chapter under the heading "How the figures run",
so it must read well in both places and say nothing about any one figure or chapter. Three short
paragraphs, no list, no heading, no more than 200 words.

The facts are in `docs/notes/chapter-01/facts.md`, under "The Metadata Lab, as its note describes
it", numbered 1 to 6. Carry every one of them, in that order:

- first paragraph: facts 1, 2 and 3, what the lab is, what it holds, and the week;
- second paragraph: fact 4, how it runs;
- third paragraph: facts 5 and 6, how you use it and what your browser keeps.

Rules for this note:

- Name each thing before a sentence uses it with "the": the shop, the programs, the week, the
  query engine. No sentence may say "the week" or "each night" before the sentence that says what
  the week is.
- Put the subject first in every sentence. Write each of the three examples in fact 5 as its own
  sentence, with the lab or the figure as its subject.

Do not:

- say how many programs there are, which asset a program reads or writes, or what any program
  does;
- say "this chapter" or "this page": the note serves every chapter;
- use these words: metadata (except in the name "the Metadata Lab"), simulate or simulation,
  schema, dataset, job, event, lineage, environment; or "run" as a noun (as a verb it is fine).
