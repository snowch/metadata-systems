# Brief BM: the editing pass (the author's second look at round 22)

Read `BK-common.md` first; its rules hold. The author found the chapter's structure right and
asked for an editing pass: cut prose that paraphrases evidence or a summary the reader has just
read, and make each what-if answer a distinct question, show the evidence that changes, and state
its conclusion, with nothing the result already makes obvious. Write each slot under its own
`## BMn` heading in your draft file, exactly as it should appear on the page. Shorter than what it
replaces, every time.

## BM1: the lead of stage 3 (replaces its first paragraph)

Now: "Nothing on the platform records how `daily_sales` was made. The usual move is to infer it:
find a query over another asset that gives the same rows. The hypothesis below comes with the
evidence for each part. Compare it with your guess for `daily_sales` at the end of Chapter 1."

Stage 2 has just shown that nothing records how an asset was made: do not say it again.
1. The usual move is to infer how `daily_sales` was made: find a query over another asset that
   gives the same rows.
2. The hypothesis below comes with the evidence for each part. Compare it with your guess for
   `daily_sales` at the end of Chapter 1.

## BM2: the lead of the what-ifs (replaces its three paragraphs; the collapsible note after it stays)

1. Keep word for word: "The query shows how `daily_sales` **could have been** made, not how it
   **was** made."
2. Three what-ifs test the difference: keep the words "three small changes to the shop". None of
   them happened in the week you have read.
3. Each cell below runs the week again with one change and prints Monday morning's records in
   three columns: `the week as it ran`, `with the change`, and `changed`, which says `yes` where the
   two differ. Name each column once.
Do not ask a question here: each what-if asks its own.

## BM3: the first what-if, the analyst's copy

Before its cell (the bold first sentence and the sentence after it stay as they are; write only
what follows them):
1. One question, as a sentence ending in a question mark: can a query that fits tell two possible
   sources apart?

After its cell, at most three sentences:
2. Two records change: object storage has a new file, `s3://shop-scratch/clean_orders_copy.csv`,
   and the last row lists a second query that fits, over the copy.
3. No record says which of the two the job that writes `daily_sales` reads. A query that fits is
   evidence for every source it fits. Keep those last nine words word for word.
4. Only a record of what the job read would settle it.

## BM4: the second what-if, the edit

Before its cell (the bold first sentence and the sentence after it stay): one question, as a
sentence: does an edit to a job leave a trace in the platform's records?

After its cell, at most four sentences:
1. Two records change: the dashboard shows £215.49 instead of £191.49 for Saturday 12 September,
   and no query in the set fits any more (the last row says `none`). Keep the words "£215.49
   instead of £191.49".
2. Why Saturday changes: the shop has no refunds, since every order's `status` is `completed` or
   `cancelled`, so from Saturday cancelled orders count too.
3. The row count, 7, and the last-altered time do not change. No record says the job was edited.
4. Only a record of which version of the job's code ran each night would show it.

## BM5: the third what-if, the failed night

Before its cell (the bold first sentence and the sentence after it stay): one question, as a
sentence: does a job that fails show up as a failure?

After its cell, at most four sentences:
1. Three records change: `daily_sales` has 6 rows, none for Sunday; it was last altered on Sunday
   at 02:30, a day earlier than `clean_orders`; and the dashboard shows 6 values.
2. The dashboard still refreshed at 03:00 on Monday, and the query over `clean_orders` still fits,
   with one row more, for Sunday.
3. The shortfall is there to see if you expect 7 rows or compare the last-altered times, but no
   record says a write was due and did not happen.
4. Only a record of whether each night's write succeeded would.

## BM6: the owner's subsection (replaces its heading and its first two paragraphs)

Now the heading is "### What each system records about assets, and why", and under it: "Each of the
shop's systems records what its own work needs. The warehouse keeps column names and types so that
it can run a query. Object storage keeps a file's key so that it can serve the file. The reporting
tool keeps the values so that it can draw the chart. The warehouse and the reporting tool also keep
a little more: an owner, created times and who created the dashboard. None of it says what an asset
means or how it was made." and "The owner the warehouse records shows how far that goes. "Who
should I ask about `daily_sales`?" wants a person or a team."

The box above it has just said what the records hold and what they do not. Keep only the reason
and the turn to the owner:
1. A heading starting `### ` that names the subject: the owner the warehouse records.
2. Why each system records what it does, in one sentence: what its own work needs, such as column
   types to run a query, a key to serve a file, the values to draw a chart.
3. Keep word for word: "\"Who should I ask about `daily_sales`?\" wants a person or a team."
