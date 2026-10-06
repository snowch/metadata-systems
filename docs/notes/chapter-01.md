# Chapter 1: The invisible data system

A working note, kept as the chapter was built on 6 October 2026: what was built, what was reused,
what the prose process caught, and what would be changed. The chapter's fact sheet, briefs, drafts
and review are in `docs/notes/chapter-01/`.

## What the chapter does

The learner gets the shop's storage and nothing else, and tries to answer what anybody asks of a
platform they did not build. As revised after the review:

- two predictions: what the warehouse names as an owner, among four candidates of one kind; and
  on how many days the raw orders add up to `daily_sales`, as a count (most learners expect six;
  the lab finds three);
- an inspector over the seven assets: exactly what their systems record, and what storage says
  about the same eight questions for every asset, before the rows;
- a construction that rebuilds `daily_sales` from another asset with a query, "rebuild" defined
  once (every row the asset has, with the same values);
- a failure experiment that opens once the learner's own query passes, and runs the week again
  with each of three changes after a committed prediction of how many of the builder's queries
  will rebuild `daily_sales` (two, none, one);
- a sort: the learner places the eight questions about `daily_sales` in three groups, then the lab
  places them, tags each question only a record answers with the kind of record that would, and
  moves them as the learner switches between the changed weeks;
- the three kinds of record derived from that map, and *metadata* introduced by them;
- a challenge that recovers the cleaning rules of `clean_orders`, then, once the rules pass, a
  prediction of how many settings pass (two: this week's data cannot show the quantity rule);
- a reflection that returns to Thursday, leaves its cause open as the plan does, and places the
  four questions of Section 2.

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

## The review

A reviewer on another model read the built chapter as its learner (`review/brief.md`,
`review/findings.md`): 32 findings, 3 high, 17 medium, 12 low. An independent sceptic attacked each
one against the lab, the source and the current build (`review/sceptic-brief.md`,
`review/verdicts.md`): 10 upheld, 20 upheld in part, 1 already fixed (R2, by change 6 above), 1
rejected (R24). The sceptic's severities are the ones acted on.

Three of the false statements came from this session's own briefs, not from the drafting: that a
failed night looks like a quiet one (R3), that the reporting tool keeps the query behind its chart
(R1), and that the owner field says which login created a table (R6). Each was a fact written into
a brief without being read off the lab. The redraft's fact lists are probed from the lab first, and
the facts test pins what they state.

What each finding gets:

| Finding | Verdict | The fix |
| --- | --- | --- |
| R1 (high) | upheld | Section 7 no longer says the reporting tool keeps a query: in the lab it keeps a title, a creator, times and values, and a program fills the dashboard. |
| R2 | already fixed | "Rebuild" gets one meaning everywhere: the query gives every row the asset has, with the same values. |
| R3 (high) | upheld | The failed night says what the lab computes: six rows and no Sunday; `daily_sales` a day older than `clean_orders` and the dashboard; the dashboard's own record looking up to date; nothing in storage saying a write was due or failed. The fact sheet and the plan's Chapter 1 row say the same. |
| R4 | in part | The Reflection returns to Thursday, says what the rows show and that nothing says why, leaving the cause to later chapters as the plan does, and places the four questions of Section 2. |
| R5 | in part | The owner prediction loses "no owner at all" and its options become four of one kind; the days prediction asks for a count with options that can be wrong informatively, answered by the lab. |
| R6 | in part | "Records the name `etl_service`"; "which login created the table" is gone. |
| R7 | in part | One open task tied to the days that differ; the inspector's closing note and the prediction's explanation no longer hand over the rows. |
| R8 | in part | A visible cue on every region that scrolls sideways; times that do not break at a hyphen; the inspector's questions before the rows. |
| R9 | in part | A committed prediction per change, how many of the builder's queries will rebuild `daily_sales`, answered by the lab; a title that does not answer it. |
| R10 | in part | Storage's view of the changed week stated as it stands, the comparison with the first run labelled as the lab's, and a closing line that says what was left (a new file, a stale time) and what was not (any record of the change, who made it, or why). |
| R11 | in part | "No query the builder offers rebuilds it" wherever the claim is made; the map's week selector shows the question leaving the middle group. |
| R12 | in part | The failure experiment starts once the learner's own query passes; the map names a query and its source only after a pass. |
| R13 | in part | Section 7's reason is given as the lab's design, without "only" or "must"; the note's two unsourced claims are replaced by Iceberg's snapshots and Delta Lake's table history, recorded in `docs/sources.md`. |
| R14 | upheld | The long sentences split; their facts sent to Haiku as lists. |
| R15 | in part | The middle group's rule includes the times and the latest row; "How are its numbers worked out?" is answered with what storage lacks, the calculation. |
| R16 | in part | The groups are named by their headings, never by position. |
| R17 | upheld | The map becomes a sort: the learner places the eight questions, commits, and the lab places them; a week selector runs the map on each change. |
| R18 | in part | The kinds of record come from the questions: the map tags each question the data cannot answer with the record it needs, and the page says storage's own fields are metadata too. |
| R19 | in part | The challenge gets a purpose, and after a pass a prediction (how many settings of the rules pass), answered by the lab, replaces the Reflection's statement. |
| R20 | upheld | The three-part conclusion is stated once, after the experiment; the second map goes. |
| R21 | upheld | The objectives say what the learner does, not what they will find. |
| R22 | in part | Section 2's sentence about rows fixed; "real things" cut. |
| R23 | upheld | One sentence on `updated_by`: who last edited a product row, not who is responsible for the file. |
| R24 | rejected | Nothing: the customers files are one more case of storage not saying why. |
| R25 | upheld | The dashboard is asked the same eight questions. |
| R26 | upheld | The caption and the task say "rebuild", as the prose does. |
| R27 | upheld | The disclosure shows a marker. |
| R28 | in part | "Not the timetable" becomes "not when each program is due"; a task asks what the order of last writes suggests. |
| R29 | in part | The four phrasings that hold, corrected. |
| R30 | in part | The lab is introduced in a sentence where its first figure is used, and it is the one agent that knows. |
| R31 | in part | One word per idea: platform, a repeated order, responsible, the last night's write. |
| R32 | in part | "Really" cut on the front page and in the Reflection; the Generalisation's promise is about the course. The placeholders stay. |

## The revision's prose

After the code, five fact briefs (`briefs/revision/H` to `L`, with `common.md`) went to Haiku in
parallel, drawn from a fact sheet rewritten from the lab's own output. What came back:

| Draft | Wrong, sent back | Dropped, restored with the fewest words |
| --- | --- | --- |
| H (objectives, Sections 1 to 3) | none | what an asset is; that "storage" means all three systems |
| I (Sections 4 and 5, the inspector's words) | the inspector's closing note said storage leaves all "eight questions" unanswered | what the builder does with the choices |
| J (the failure experiment) | none | none |
| K (Sections 7 and 8, the map's words) | the explanation said none of the systems keeps what "your eight questions" asked, and that "the programs create these assets" (the files come from the export) | none |
| L (Sections 9 and 10, the notes, the front page) | the fourth hint added "the two rules that matter most", which is false | none |

The whole-chapter read, from a dump of the built page in every state (`scratchpad`, not kept),
sent three things back for style: the failure experiment's caption, which no brief had asked for
and which still described the old figure; the closing summary's "each change changed"; and the
closing note's first paragraph, a colon followed by two clauses. It fixed four joins with the
fewest words: a pronoun ("shown them"); "Once you have checked your sorting" before the
generalisation's reference to the map's tags, which appear only after the check; quotation marks
round a group's name and the dashboard's title inside a sentence; and "The column" before an
identifier that opened a sentence. The duplicated caption under the change lab's own heading is
hidden visually and kept for a screen reader.

## Known gaps

- The bundle is about 860 kB minified, most of it the runtime's Markdown and maths rendering,
  which this course does not use; the digital-design inventory recorded the same for that course.
  Making maths optional in the runtime is a platform change for both courses.
- The table of an asset's rows still scrolls sideways on a phone (its columns are the file's own),
  but now says so above the table.
- Settled at checkpoint 1: a committed prediction, a committed sort and a change's prediction now
  stay, with no "Predict again" or "Sort again"; "start this chapter again", at the foot of the
  chapter, clears everything after a second press (labels drafted from brief N).
- The lab models one week. Later chapters add weeks and changes as they need them.
