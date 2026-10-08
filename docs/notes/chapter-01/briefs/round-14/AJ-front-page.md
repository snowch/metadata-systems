# Brief AJ: the front page's words

Read `docs/notes/chapter-01/briefs/round-4/common.md` first, and the files it names: every rule
there holds for this brief, and `docs/style.md`'s rule "silence is preferable to filler" above all.
Write your draft to `docs/notes/chapter-01/drafts/round-14/AJ.md`.

The front page is being rebuilt. At the top, a band holds the course's title, one line that says
what you do, a paragraph, the button into Chapter 1, and a line on what the course assumes of you;
beside them, a real figure from the course: the shop's dashboard, as Chapter 1 shows it. Under
the band, the course's eight parts in reading order, each with one line on what you do in it. Then
the contents, by part. Every string below is plain text: no Markdown, no backticks.

Facts about the course, from `docs/plan.md`:

- The learner is a working software or data engineer.
- The course assumes the learner can read a short SQL query (a SELECT with a WHERE and a GROUP
  BY) and has used files, database tables and a dashboard. It assumes nothing about metadata,
  lineage or any product: every term arrives where the course needs it.
- Everything runs in the browser; there is nothing to install or sign in to.
- The dashboard figure shows the shop's revenue per day for the shop's first week, Monday 7 to
  Sunday 13 September 2026, as it stands on Monday morning, 14 September. Thursday's total is far
  lower than every other day's. The head of the shop asks you why. Chapter 1 starts from that
  question. Do not say why Thursday is low, or anything about what the learner will find.
- The eight parts, with their chapters and what the learner does in each:
  1. Why metadata exists (chapters 1 to 4): meet a data platform that keeps its data and almost
     nothing about it; build the first records about its assets; give the records a model, then
     a graph.
  2. Lineage (5 to 8): record what was made from what, through the programs that make it;
     design the event a program's run should emit; meet OpenLineage, an open standard for such
     events; turn events into a graph.
  3. Deeper lineage (9 to 12): follow lineage column by column; follow schemas that change;
     decide when two references name the same asset; record what a run leaves behind.
  4. Metadata becomes operational (13 to 16): use the records to check data quality, trace a
     number back to its rows, say what a change would break, and find where a fault entered.
  5. When the simple model breaks (17 to 22): events that go missing, repeat, arrive late or
     contradict each other; metadata at the scale of millions of assets.
  6. Building a metadata platform (23 to 27): build the store, the collector, the lineage graph,
     the query layer and the interface, each against tests.
  7. Real systems (28 to 31): OpenLineage in practice; where Airflow, Spark, dbt and Trino get
     their metadata; the architectures of OpenMetadata, DataHub, Apache Atlas and Marquez
     compared; metadata for ML and AI.
  8. The complete system (32): take a second, unfamiliar platform and do all of it.

## promise

One line in bold under the title, no more than 14 words: what you do in this course. The fact:
you build a small metadata system inside a data platform that runs in your browser.

## assumes

One or two sentences, no more than 40 words, on what the course assumes of you: the SQL, the
files, tables and dashboard, and that it assumes nothing about metadata or lineage.

## figureCaption

The caption under the dashboard figure's badge, no more than 30 words: what the figure shows
(the dashboard, Monday morning, the first week's revenue per day), that Thursday is far lower,
and that Chapter 1 starts from the head of the shop's question. Keep the dates: "7 to 13
September".

## partsHeading

A heading for the eight parts, no more than 6 words. Not a question.

## partsLead

One sentence under that heading, no more than 25 words: the parts come in reading order, and
each builds on the last inside the same lab.

## parts

A Markdown list of eight items, each `name: ` then one line of no more than 22 words on what you
do in that part, in the order above, written from the facts. Use the parts' names exactly as
given, before the colon. Start each line with a verb.

## partChapters

Two plain-text templates for the chapters a part covers, with the slots kept exactly:
- one: for a part with one chapter, with the slot `{from}`
- other: for a part with several, with the slots `{from}` and `{to}`

## partCount

Two plain-text templates for the line beside a part's name in the contents, slots kept exactly:
- some: `{written}` of the part's `{total}` chapters are written (the written ones can be read)
- none: none of the part's `{total}` chapters is written yet

Rules: no reassurance or motivation ("exciting", "journey"); nothing that gives the lab or the
course a wish or a mood; do not use the words simulate, simulation, instrument, artifact, engine;
use "metadata" and "lineage" only as the names of the parts need them.
