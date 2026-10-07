# Brief AH: two labels inside the figures

Read `docs/notes/chapter-01/briefs/round-4/common.md` first, and the files it names: every rule
there holds for this brief, and `docs/style.md`'s rule "silence is preferable to filler" above all.
Write your draft to `docs/notes/chapter-01/drafts/round-12/AH.md`.

Two figures change, for the learner, and each needs one label. Both are plain text, no Markdown.

## keptAfterRun

Where it appears: in the challenge "Which rules filter orders.parquet?", under the heading
"Result", below the SQL the learner's four rule choices make, before the learner has run the tests
on the rules now chosen.

The facts:

- The learner chooses four rules that should turn `orders.parquet` into `clean_orders`.
- The SQL of their rules shows as they choose.
- The rows their rules keep, and how many, show only once they run the tests on the rules now
  chosen. The button that runs the tests is just below and says "Run tests".
- After any change to a rule, the rows wait for the tests to run again.

Write one sentence, no more than 12 words, that tells the learner what to do to see the rows
their rules keep. You may name the button's words, "Run tests".

## extraRow

Where it appears: in a table that sets the learner's query beside `daily_sales`, one row a day,
with the columns "Day", "Your result", "daily_sales" and "Match". The "Match" column says "Yes"
where the two agree and "No" where they differ. This label goes in the "Match" column instead, for
a day where the learner's query gives a row and `daily_sales` has none.

The facts:

- A query rebuilds `daily_sales` when it gives every row `daily_sales` has, with the same values.
- A row that only the learner's query gives does not stop it rebuilding `daily_sales`.
- So such a row is neither a match ("Yes") nor a difference ("No").

Write the label: no more than three words, capital first letter like "Yes" and "No", no full
stop. It says the row is one only the learner's query has.

Rules for both: subject first if it is a sentence; no reassurance, no motivation; do not use the
words metadata, schema, dataset, job, event, lineage, or "run" as a noun.
