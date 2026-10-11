## title7

What each system keeps

## explanation

Each system that holds data keeps some information about its own assets.

Object storage keeps each file's location, its size and when it was last modified. The warehouse keeps each table's column names and types, its row count, its size, when it was created and when it was last altered, and the name of the account that owns it. The reporting tool keeps the dashboard's title, who created it and when, when it last refreshed and its values.

These are the lab's choices of what each kind of system keeps. Each field is one the system uses for its own work. The warehouse uses column names and types to run a query. Object storage uses a file's location to serve it. The reporting tool uses the values to draw its chart.

None of the three keeps what your questions asked about who is responsible for an asset, what made it, what reads it or what changed in it. The programs, and when each is due to run, exist. This page has not shown you that yet. Later chapters do.

## mapLead

The map lists the eight questions about `daily_sales`. For each question, choose the group that can answer it, then check your sorting.

The three groups are:

- Storage records it.
- The data suggests it.
- Only a record kept at the time answers it.

A question goes with the data when a query rebuilds the asset, when another asset shows the same numbers, or when the last-written time and the latest row fit a write that worked. After you check, the lab places each question itself, by reading storage and trying every query the builder offers. You can run the map again on each change from the failure experiment.

## mapAfter

The data's group holds evidence, not a certainty. A change to the shop can move a question out of the data's group.

## caption

Sort the eight questions about `daily_sales` by what can answer them, then let the lab place them.

## generalisation

Look at the questions in the group "Only a record kept at the time answers it". The map tags each with the kind of record that would answer it.

There are three kinds of record:

- a record of what the asset is: who is responsible for it, the unit of its numbers;
- a record of what happened: what changed in it, when it was written, whether a write worked;
- a record of what was made from what: what it is made from, how its numbers are worked out, what reads it.

The groups say what can answer a question now. The kinds say what record would answer it for certain. The two sortings need not line up.

One column in the data names people: `updated_by` in `products.parquet` says who last edited each product's row. That is a fact about a product, not a record of who is responsible for the file.

After the edit to the program, two questions about what made `daily_sales` left the data's group.

Records about the assets and the platform, written down and kept apart from the data itself, are called **metadata**. What storage keeps (names, types, row counts, sizes, times, an owner's name) is metadata too: the part each system keeps for its own work. The questions only a record answers need the rest, and nobody keeps it unless somebody decides to.

The rest of this course builds a system that keeps all three kinds.

## figure strings

- place.storage: Storage records it.
- place.suggested: The data suggests it.
- place.record: Only a record kept at the time answers it.
- sortLegend: where each question about `{asset}` is answered.
- sortPick: choose a group.
- checkSort: check my sorting.
- sortAgain: sort again.
- sortScore: `{matching}` of `{total}` questions are where the lab places them.
- youPlaced: you placed it under `{place}`.
- movedFrom: in the week as it first ran, it was under `{place}`.
- needsRecord: a record of `{kind}` would answer it.
- recordKind.what-it-is: what the asset is.
- recordKind.what-happened: what happened.
- recordKind.made-from-what: what was made from what.
- weekLegend: week.
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
