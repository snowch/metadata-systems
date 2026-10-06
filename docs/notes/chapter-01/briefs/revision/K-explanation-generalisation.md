# Brief K: Sections 7 and 8, and the map's words

Read `common.md` in this directory first. Write your draft to
`docs/notes/chapter-01/drafts/revision/K.md`. Read the fact sheet's "What each storage system
records" and "The three groups of questions" closely. Two statements an earlier draft made here
were not the lab's and must not come back: that the reporting tool keeps the query behind its
chart (it keeps no query), and that a system "must" or "needs to" keep a field.

## title7

Section 7's title, plain text, a few words: what each system keeps.

## explanation

Section 7's prose, above the map. Facts:

- Object storage keeps each file's location, its size and when it was last modified.
- The warehouse keeps each table's column names and types, its row count, its size, when it was
  created and last altered, and the name of an owning account.
- The reporting tool keeps the dashboard's title, who created it and when, when it last
  refreshed, and its values.
- These are the lab's choices of what each kind of system keeps. Each is a field the system uses
  for its own work: the warehouse uses column names and types to run a query; object storage
  uses a file's location to serve it; the reporting tool uses the values to draw its chart.
- None of the three keeps what your questions asked: who is responsible for an asset, what made
  it, what reads it, what changed.
- The programs, and when each is due to run, exist, but this page has not shown them. Later
  chapters do.

## mapLead

Shown above the map, before the learner sorts. It must not say where any question goes. Facts:

- The map lists the eight questions about `daily_sales`. For each, choose the group that can
  answer it, then check your sorting.
- The three groups (use these headings exactly, in quotation marks or as a list):
  "Storage records it", "The data suggests it", "Only a record kept at the time answers it".
- A question goes with the data when a query rebuilds the asset, when another asset shows the
  same numbers, or when the last-written time and the latest row fit a write that worked.
- After you check, the lab places each question itself, by reading storage and trying every query
  the builder offers. You can then run the map on each change from the failure experiment.

## mapAfter

Shown under the map from the moment the page loads, so it must not say where any question goes.
One or two sentences. Facts: the data's group holds evidence, not answers; a change to the shop
can move a question out of it.

## caption

The map's caption, plain text, one sentence ending with a full stop: sort the eight questions
about daily_sales by what can answer them, then let the lab place them.

## generalisation

Section 8's prose, after the map. It has no figure of its own; it reads what the learner has just
seen on the map. Facts, in this order:

- Look at the questions in the group "Only a record kept at the time answers it". The map tags
  each with the kind of record that would answer it.
- There are three kinds (a Markdown list, one line each):
  - a record of what the asset is: who is responsible for it, the unit of its numbers;
  - a record of what happened: what changed in it, when it was written, whether a write worked;
  - a record of what was made from what: what it is made from, how its numbers are worked out,
    what reads it.
- The groups say what can answer a question now. The kinds say what record would answer it for
  certain. The two sortings need not line up.
- One column names people: `updated_by` in `products.parquet` says who last edited each
  product's row. That is a fact about a product, not a record of who is responsible for the file.
- After the edit to the program, two questions about what made `daily_sales` left the data's
  group. (Do not restate the other two changes: the failure experiment already summed them up.)
- Records about the assets and the platform, written down and kept apart from the data itself,
  are called **metadata**. Put **metadata** in bold here, once: this is where the word is
  introduced, and it must not appear earlier.
- What storage keeps (names, types, row counts, sizes, times, an owner's name) is metadata too:
  the part each system keeps for its own work. The questions only a record answers need the
  rest, and nobody keeps it unless somebody decides to.
- The rest of this course builds a system that keeps all three kinds.

## figure strings

The map's words, as a Markdown list with the key before a colon. Plain text. Keep every `{slot}`
and add none. Write slots without backticks.

- place.storage: the first group's heading: Storage records it.
- place.suggested: the second group's heading: The data suggests it.
- place.record: the third group's heading: Only a record kept at the time answers it.
- sortLegend: the heading above the eight choices: where each question about `{asset}` is
  answered.
- sortPick: the empty choice in each list: choose a group.
- checkSort: the button that commits the sort: check my sorting.
- sortAgain: the button that clears the sort to try again.
- sortScore: a sentence: `{matching}` of `{total}` questions are where the lab places them.
- youPlaced: a sentence under a question the learner placed elsewhere: you placed it under
  `{place}`.
- movedFrom: a sentence under a question that moved when a change is shown: in the week as it
  first ran, it was under `{place}`.
- needsRecord: a sentence under a question only a record answers: a record of `{kind}` would
  answer it.
- recordKind.what-it-is: the noun phrase: what the asset is.
- recordKind.what-happened: the noun phrase: what happened.
- recordKind.made-from-what: the noun phrase: what was made from what.
- weekLegend: the name of the group of week choices, one word.
- e.time: last written at `{time}`.
- e.oneQuery: one query rebuilds it: `{query}`.
- e.oneQueryHidden: one query in the builder's choices rebuilds it (no query named).
- e.oneSource: one asset rebuilds it: `{source}`.
- e.oneSourceHidden: one asset rebuilds it (no asset named).
- e.manySources: `{count}` assets rebuild it equally well: `{sources}`.
- e.manySourcesHidden: `{count}` assets rebuild it equally well (no assets named).
- e.manyQueries: `{count}` queries rebuild it, from `{sources}`.
- e.manyQueriesHidden: `{count}` queries in the builder's choices rebuild it.
- e.noQuery: none of the builder's choices rebuilds it.
- e.readers: `{assets}` shows the same numbers.
- e.noReaders: no other asset shows the same numbers.
- e.nightDone: last written at `{time}`, with a row for `{day}`.
- e.nightMissing: last written at `{time}`; the latest row is for `{latest}`, not `{expected}`.
- e.account: storage records the name `{role}`, not who is responsible.
- e.types: `{column}` is `{type}`, with no unit.
- e.currentOnly: storage keeps only the current rows.

Each e.* line is one sentence ending with a full stop.
