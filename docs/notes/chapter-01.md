# Chapter 1: The invisible data system

A working note, kept as the chapter was built on 6 October 2026: what was built, what was reused,
what the prose process caught, and what would be changed. The chapter's fact sheet, briefs, drafts
and review are in `docs/notes/chapter-01/`.

## What the chapter does

The learner gets the shop's storage and nothing else, and tries to answer what anybody asks of a
platform they did not build. Two predictions (what the warehouse names as an owner; on how many
days the raw orders add up to `daily_sales`); an inspector over the seven assets and exactly what
their systems record; a construction that rebuilds `daily_sales` from another asset with a query;
a failure experiment that runs the week again with three changes storage does not record; a
computed map of which questions storage, the data, or only a record can answer; and a challenge
that recovers the cleaning rules of `clean_orders` from its input and output, with a rule this
week's data cannot reveal. *Metadata* is introduced at the end, by the questions the learner could
not answer.

## What was built for it

- **The lab** (`packages/lab`): typed values with money as whole pennies; the course's SQL subset
  (lexer, parser, executor with SQL's NULL rules, formatter); the shop's hand-written week, assets
  and four programs; the night-by-night simulation with three changes; the storage view; the
  inference searches (sums that rebuild an asset, cleaning rules that rebuild `clean_orders`,
  assets showing the same numbers); the chapter's questions and the probes behind its predictions.
- **The figures** (`packages/views`): the dashboard, the prediction, the storage inspector, the
  change lab, the question map, the choice editor and the grader.
- **The course**: the shell, the front page over the whole plan, the pager, the design tokens
  (IBM Plex in three cuts, a teal ink accent, one colour per kind of asset).

## What was reused, and what was extracted

- From the platform: the schema, the runtime and three primitives (`PredictionChallenge`,
  `FaultInjector`, `StateInspector`). The move to `snowch/learning-platform` and its three
  generalisations are recorded there (`docs/adoption.md`) and in `docs/platform.md` here.
- Nothing was extracted into the platform from this chapter: no figure here has a second consumer
  yet. Two candidates to watch under the rule of two: the scrolling data table (`DataTable`) and
  the choice editor, which Chapter 2's record editor may share.

## What the prose process caught

Six briefs (A to F) went to Haiku drafting agents in parallel, then one brief (G) of returns.
The fact check found the profile the digital-design course records:

| Draft | Dropped facts, restored with the fewest words | Wrong, sent back |
| --- | --- | --- |
| A (question, motivation, predictions) | the year; "its online store"; "yet"; "before you open storage"; "every row"; the owner prediction's last sentence | none |
| B (investigation, construction) | none | the builder's field labels came back as their keys; the inspector's lead said storage gives "answers" to the questions (drift, corrected) |
| C (failure experiment) | what the figure shows and whose query it uses; "the shop has no refunds"; "the same 7 rows and the same last-written time"; "nothing says whether Saturday is a mistake or a decision" | none |
| D (explanation, generalisation) | two systems' purposes; "evidence, not an answer" | the explanation's list of questions was invented; "what changed" became "what rows were deleted" (corrected) |
| E (challenge, reflection, labels) | none | the reflection said storage showed who owns `daily_sales`, the opposite of the chapter's point, added a claim and used a long dash |
| F (figure labels, shell) | "not what they mean", "not a person or a team", "not who answers for it now" and "in the builder's choices", each the point of its label; "again" | an em dash as the text for "no row"; a slot not in the brief |

G's redrafts were right on the first return. Joins between drafts that read badly once placed
("The week ran with an analyst copies…", "per the day the order was placed", "You predicted on
some days…") got the fewest words that make them read.

## The managing session's read

Read from a dump of the built page (`docs/notes/chapter-01/review/page.md`), start to finish,
before the reviewer's report:

1. The record table's first column was headed "Column" while listing fields such as Location and
   Rows: *column* in two senses on one page. Now "Field", which is also the owner prediction's
   word.
2. The question map gave "What is it made from?" and "How are its numbers worked out?" the same
   evidence line. The first now names the asset or assets; the second the query.
3. Two sources were joined with a comma ("from clean_orders, clean_orders_copy.parquet"); now with
   "and".
4. The second challenge's field labels were lower-case where the first's were capitalised.
5. The owner prediction printed the owner on a line of its own directly above an explanation that
   opens with the same fact; the line is gone.
6. **A figure contradicted its text.** After the failed night, the change lab listed no query that
   rebuilds `daily_sales`, while the outcome below it said the query "still rebuilds every row
   `daily_sales` has". The figure asked for an exact match; the question map, rightly, asks
   whether every existing row is rebuilt. The change lab now asks the same, and the browser test
   pins the count after each change (two, none, one).

## Known gaps

- The bundle is about 860 kB minified, most of it the runtime's Markdown and maths rendering,
  which this course does not use; the digital-design inventory recorded the same for that course.
  Making maths optional in the runtime is a platform change for both courses.
- The table of an asset's rows scrolls sideways on a phone; its columns are the file's own.
- The lab models one week. Later chapters add weeks and changes as they need them.
