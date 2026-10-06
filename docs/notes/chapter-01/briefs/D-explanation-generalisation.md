# Brief D: explanation and generalisation

Attach: `common.md`, `../facts.md`, `docs/style.md`. Write to `docs/notes/chapter-01/drafts/D.md`.
This is the one place the word "metadata" may appear, in `generalisation`, where it is introduced.

## titles.explanation
A heading of three to six words: what each system records, and why.

## explanation
Two or three short paragraphs. Facts:
1. Each system records what it needs for its own work. Object storage needs a file's location,
   size and time to find it and serve it. The warehouse needs columns, types and an owning account
   to run queries and control who may read. The reporting tool needs a title, values and a
   refresh time to draw its chart.
2. Your questions are about the platform around the data: what a number means, who answers for an
   asset, what made it, what reads it, what changed.
3. None of the three systems needed those answers to store or serve the data, so none recorded
   them.
4. Some of the systems do keep records for their own work that you were not shown: the reporting
   tool keeps the query behind its chart, and something keeps the programs and their timetable.
   You will see them in later chapters.

## mapCaption
One sentence caption: each question about `daily_sales`, placed by what can answer it.

## mapLead
Shown above the figure. Two sentences. Facts:
1. The lab places each question in one of three columns: storage records it; the data suggests
   it, because a query rebuilds the asset or another asset shows the same numbers; or only a
   record kept at the time answers it.
2. The lab works out each place by running storage and the query builder's search, not from a
   list.

## mapAfter
Shown below the figure. One or two sentences. Facts: the middle column is evidence, not an answer.
The failure experiment showed the evidence change with a copy, an edit and a failed night.

## titles.generalisation
A heading of three to six words: data, and the records about it.

## generalisation
Two or three short paragraphs. Facts, in order:
1. The right-hand column holds questions no amount of data answers: who is responsible, what a
   number's unit is, what changed.
2. The middle column holds answers the data suggests. They can be ambiguous, impossible or
   misleading.
3. Records about assets and about the platform, kept apart from the data, are called
   **metadata**. (Introduce the word here, in bold, once.)
4. A platform needs three things written down: what each asset is (its meaning, its units, who
   answers for it); what happened (what ran, when, and whether it worked); and what was made from
   what. Do not give the three kinds names.
5. The rest of the course builds a system that keeps them, starting with the first records in the
   next chapter.

## map2Caption
One sentence caption: the same questions with the analyst's copy in storage.

## map2Lead
Shown above the figure. One or two sentences. Facts: the figure runs the week with the analyst's
copy. Look at the middle column for "What is it made from?".

## map2After
Shown below the figure. One or two sentences. Facts: two assets now fit as the source of
`daily_sales`. The data suggests both. It cannot decide between them.
