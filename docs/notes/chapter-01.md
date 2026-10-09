# Chapter 1: The invisible data system

A working note, kept as the chapter was built on 6 October 2026 and revised on 7 October through
the author's second to fifth rounds: what was built, what was reused, what the prose process
caught, and what would be changed. The chapter's fact sheet, briefs, drafts
and review are in `docs/notes/chapter-01/`.

## What the chapter does

The learner gets the shop's storage and nothing else, and tries to answer what anybody asks of a
platform they did not build. As it stands after the author's fifth round, in the page's order:

- a map of the platform, near the start and to hand all through the chapter: the three systems in
  the order data moves through them, the assets each holds, and between them programs the
  learner cannot see; never a link from one asset to another;
- the dashboard, with Thursday far below the other days, and the head of the shop asking why;
- a requirement questioned, "Every table must have an owner.": the learner chooses what to store,
  sees the four questions the requirement could be asking, then the warehouse's account,
  `etl_service`, which answers only one of them;
- a prediction of what Thursday's raw orders add up to, with "I can't tell yet" offered: 205.50,
  against 51.50 in `daily_sales`, so there is a difference to explain;
- an investigation in the order the author's fifth round gives: where to look first, a decision
  whose choice opens the inspector; the inspector over the seven assets, exactly what their
  systems record and what storage says about the same eight questions for every asset; then an
  explanation of Thursday to test;
- a construction that rebuilds `daily_sales` from another asset with a query, "rebuild" defined
  once (every row the asset has, with the same values), which ends by asking whether rebuilding it
  shows how it was made; once the rebuild passes, a check reads Thursday's orders against the
  rows it keeps, beside the explanation the learner chose;
- a failure experiment that answers that question: it opens once the learner's own query passes,
  and runs the week again with each of three changes after a committed prediction of what the
  data will then say about where `daily_sales` comes from (more than one query, none, one);
- a sort: the learner places the eight questions about `daily_sales` in three groups, then the lab
  places them, tags each question only a record answers with the kind of record that would, and
  moves them as the learner switches between the changed weeks;
- the three kinds of record derived from that sort, and *metadata* introduced by them, as
  information about an asset or the platform that can live inside a system, inside a file, or in a
  system of its own;
- a challenge that recovers the cleaning rules of `clean_orders`, then, once the rules pass, a
  prediction of whether the learner's setting is the only one that passes (it is not: this week's
  data cannot show the quantity rule);
- a reflection that opens with what storage and the data could and could not tell, returns to
  Thursday, names what the left-out orders have in common and leaves open whether anybody meant
  it, and places the four questions of Section 2.

## Figures

Chapter 1 is written as a book: the prose carries the investigation, and a figure appears only
where the story needs the learner's own hands or eyes. Every figure on the page, in its order,
with its role (`CLAUDE.md`, "Experiments, instruments and explanations"). An experiment answers
twelve questions; an instrument or a reference answers two. The content tests fail a figure
without a role, without a block, or with a question unanswered.

### `platform`

- **Role:** reference
- **Serves:** every question in the chapter that needs to know which systems hold which assets, in
  the order data moves through them. It draws no asset made from another: that is what the chapter
  shows the systems cannot tell. Under its systems it counts what it shows (3 files + 3 tables +
  1 dashboard = 7 assets), and the sentence under it gives the word "asset".
- **Why now:** the story's first morning needs the ground under it before the head of the shop's
  line arrives.

### `week`

- **Role:** reference
- **Serves:** every question that needs to place a day or a time: which days the dashboard shows,
  when each night's work happened, and where the learner stands. It shows when the nights were,
  from the lab's own week, and nothing about what a night wrote.
- **Why now:** the story happens on a Monday morning after a first week; the view carries the
  dates the prose no longer needs to.

### `explore`

- **Role:** inspect
- **Serves:** the learner's first meeting with the four assets the chapter works through: the raw
  file, the cleaned orders, the daily totals, the reporting view. Opening a card shows a small
  head of its rows - or, for the dashboard, the reporting view itself - with the asset's true row
  count in the caption. Nothing is asked or scored.
- **Why now:** the investigation names these four assets from the first discrepancy onward;
  meeting them with no question attached makes what follows readable instead of a tour of names.

### `dashboard`

- **Role:** inspect
- **Serves:** the discrepancy itself: Thursday at 51.50 against the days either side. Its own
  last-refreshed record is on it, which the failed night later makes important.
- **Why now:** the head of the shop's one line points here; the learner needs to see what the
  shop's management sees each morning.

### `build-daily-sales`

- **Role:** experiment
- **Objective:** reconstruct the reported total from the data, and feel what a reconstruction
  establishes: a query that gives every row, with the same values.
- **Known before:** the discrepancy's shape; the inspector's record of each asset; the four
  assets' contents from the exploration cards.
- **Driving question:** can another asset give `daily_sales` exactly?
- **The action:** build the query in the builder: source, rows to keep, measure, per what.
- **Why the action:** the reconstruction is the chapter's pivot; doing it with the learner's own
  hands is what makes the next section's three failures theirs.
- **Evidence:** the builder's SQL and result, the day-by-day tests, and the kept-rows table the
  check reads.
- **Consequence:** `clean_orders`, completed only, price times quantity, per day, reproduces
  `daily_sales` exactly - and the query, the learner now knows, is evidence and not proof.
- **Predictable:** from the evidence: the raw file's rows that fail the tests point at the
  cleaned table.
- **Gives nothing away:** the hints ladder from concept to full solution, one rung at a time.
- **Not knowing:** no "I can't tell yet" here; the builder's result table shows every attempt.
- **Next question:** what does that reconstruction prove about how the table was made? The
  failure experiment tests it.
- **An experiment:** yes: the learner builds, the lab grades day by day, and the pass is the
  learner's own.

### `changes`

- **Role:** experiment
- **Objective:** break the reconstruction's evidence three ways - ambiguity (a copy), erasure
  (an edit), and staleness (a failed night) - and discover that a rebuild is evidence, never
  proof, and that the systems record no change itself.
- **Known before:** the learner's own passing query; the pattern of matching and differing days.
- **Driving question:** after each change, how many of the builder's queries still reproduce the
  new `daily_sales`?
- **The action:** predict the count, run the week with the change, read what the systems hold.
- **Why the action:** each prediction commits the learner to what their evidence is worth;
  each run shows it breaking in a way reading alone would not.
- **Evidence:** the queries that still fit, the Monday-morning state, the learner's own rows
  against the new table - all from the lab's rerun of the week.
- **Consequence:** a copy fits equally; an edit leaves nothing that fits; a failed night looks
  current while stale. In no changed week does any system record the change itself.
- **Predictable:** yes, from the learner's own query and the change's description - which is
  what makes the wrong predictions instructive.
- **Gives nothing away:** the outcome text describes the state, never the lesson; the closing
  paragraph is the chapter's, after all three.
- **Not knowing:** offered in the prediction; the lab answers with the count it found.
- **Next question:** why did the evidence fail? The explanation section answers: the systems
  keep only what they need.
- **An experiment:** yes: three perturbations, each a different failure of the same evidence.

### `build-rules`

- **Role:** experiment
- **Objective:** recover rules that are not written anywhere readable, and meet
  underdetermination: two settings pass, because this week's data never exercises the rule the
  shop's program really has.
- **Known before:** the two files' rows, from the inspector and the exploration cards; the
  duplicate order and the missing customer ids.
- **Driving question:** which rows do the cleaning rules keep?
- **The action:** choose four rules, run the tests against `clean_orders`, read the SQL.
- **Why the action:** the recovery is the chapter's last act of reading state as if it were
  history - and its last failure of exactly that.
- **Evidence:** the kept rows the rules produce, compared with `clean_orders` row by row.
- **Consequence:** a setting that fits the data can be wrong about rules the data never
  exercises: two pass, differing only where no order this week goes.
- **Predictable:** from the row-by-row comparison, which the inspector and the cards make
  possible - the underdetermination is the discovery, not the difficulty.
- **Gives nothing away:** the hints ladder; the last rung still names the quantity rule's
  freedom, which the learner has earned by then.
- **Not knowing:** not offered; the comparison is the work.
- **Next question:** none: the reflection closes the morning.
- **An experiment:** yes: the learner chooses, the lab grades rows, and the passing pair is the
  lesson.

## Requirements

None, by design. Chapter 1's owner figure began as a requirement, "Every table must have an
owner.", shown to the learner; the redesign removed it. The requirement told the learner that
ownership was recorded before they had looked, and asked them to guess what the shop happened to
store, which no evidence on the page could support. The figure is now an evidence-driven
prediction (kind `lab-prediction`) placed directly after the storage inspector: the learner
reads the warehouse's record for `daily_sales` first, then commits to a conclusion that record
could support, and the lab says which it does. The requirement survives here, in the authoring
notes, as the implementation constraint it always was: the lab's warehouse records an owner for
every table, so the record exists to be found.
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

## The author's second round, 7 October 2026

The author's consolidated feedback kept the chapter's design and asked for five things, in this
order. What each became:

1. **Every prediction asks for a belief the learner can hold.** The audit and the changes are in
   "Predictions" above; the rule is in `CLAUDE.md`, `docs/authoring.md` and `docs/style.md`, and a
   content test fails a prediction the notes do not account for.
2. **A small map of the platform, to hand all through the chapter.** The author's sketch drew
   arrows from asset to asset (`orders.parquet` to `clean_orders` to `daily_sales`). The map does
   not: those arrows are what the chapter shows storage cannot tell, they would answer the
   construction's first choice before the learner makes it, and the failure experiment's copy
   shows the data cannot choose between two sources. The map draws what the learner is told:
   the systems, in the order data moves through them, their assets, and between systems programs
   the learner cannot see. It is the lab's `platformMap`, computed from the storage view and the
   programs' systems, and its test checks that a flow names two systems and nothing else. Once the
   learner scrolls past it, a button at the foot of the window opens it over the page. The
   question map's figure is no longer called a map on the page: "map" means this one.
3. **"Asset" and "metadata" made precise.** An asset is defined with the map, in the author's
   sense: something in the platform that can be stored, described, changed, related to other
   assets, or depended on. Metadata is information about an asset or the platform, and the page
   no longer says it is kept apart from the data: it says where it can live, inside the system that
   holds the data, inside the file (a Parquet file's own column names and types, checked against
   the Parquet format specification and recorded in `docs/sources.md`), or in a system of its own.
   Section 7 now says where the inspector found a file's columns.
4. **A short summary at the end.** The reflection opens with what storage tells (what exists now),
   what the data can suggest and cannot prove, and what neither tells; the generalisation's "nobody
   keeps it unless somebody decides to" moved into it, so the point is made once.
5. **The core left as it was,** with one turn: the construction now ends by asking whether a query
   that rebuilds `daily_sales` shows how it was made, and the failure experiment's closing words
   answer it. The four questions of Section 2 still close the chapter.

### The second round's prose

Four fact briefs (`briefs/round-2/O` to `R`, with `common.md`) went to Haiku in parallel, from the
fact sheet updated against the lab. What came back:

| Draft | Wrong, sent back | Dropped, restored with the fewest words |
| --- | --- | --- |
| O (Sections 1 and 3, the map's words) | "That is close to" could be read as the 51.50, not Thursday's raw total; the arrow's label had ten words where the brief allowed eight; the map's button said "open map", wrong once the map is open | none |
| P (Sections 4 to 6) | the edit's label came back as two sentences beside two one-phrase labels; the lead asserted "your query rebuilds `daily_sales`" above a figure that may still be waiting for it | none |
| Q (Sections 7 and 8) | none | none |
| R (Section 9's prediction, Section 10) | none | "Your rules pass"; the options' answers ("yes, because", "no, because"); "in the builder", without which "no matching query" claims more than the lab searched; "for certain", without which storage would be said to tell nothing of what happened, when it showed a stale time |
| T (the owner question as a choice) | none | none; one sentence it was to keep came back changed ("storage does not show") and was restored |
| U (a choice's two labels) | the button said "Show the shop's choice", a choice nothing in the lab records | none; the second draft, "Show the warehouse", names this question's subject, so each choice now brings its own button label and only the legend is shared |

Placing them kept the old text wherever a brief kept it: P and Q had merged paragraphs and
recased a list they were asked to leave alone, and the old layout stands. The arrow's label lost
"here", which the arrow itself says.

The whole-chapter read, from a dump of the built page in every state, found three things, all
fixed:

1. **A correct prediction printed its option twice.** Now that an option is an explanation, "You
   predicted: no, because… The lab found: no, because…" repeated a long sentence. A prediction
   that matches now says so after the learner's own option; the lab's option is named only when
   it differs. The same in the failure experiment.
2. **The map's button never came after a jump.** The dump went from the top of the page to a
   prediction below the map in one move, the map never entered the window, and the window's
   watcher never fired. The watched area now runs far below the window, so the map can leave it
   only upwards, however the learner moves; the browser test makes the same jump.
3. **The edit's outcome opened by repeating its label**, now the third time on screen. Brief S
   sent its first sentence back to Haiku with the one fact the label lacks: before the edit, the
   program kept completed orders only.

The screenshots at both widths and in both themes showed the map's lists wrapping two names to a
line where the names were short; each system now lists its assets one to a line.

After the merge, the author's screenshot at a tablet's width, about 830 pixels, showed the map in
its row with every name broken mid-word. Each arrow took a fixed 7rem for its words, which left
the first two systems too narrow and the last, with no arrow beside it, too wide; and the names
were allowed to break anywhere. The arrows now take only their own width, one line under the row
says what they mean, every system in the row gets the same width, and no name breaks. Between the
phone's layout and the row, each system lists its assets across, on one line. A browser test holds
the names whole and the systems even at thirteen widths from 320 to 1280 pixels; run against the
old styles, it fails as the screenshot did. The phone and desktop screenshots this round took had
missed it: neither is a width where the row is crowded.

## The author's third round, 7 October 2026

The author asked for a principle for the whole book, not only a fix: some exercises should carry a
requirement that is deliberately underspecified, and teach the learner to ask what it means before
building to it, keeping apart what it says, what it might mean, what each meaning needs, what the
platform records and whether that meets it. "There is not enough information to choose yet" can
be the right outcome. What it became:

1. **The principle, bound for every chapter.** `CLAUDE.md` has a section, "Question the
   requirement", with this chapter's owner as its standing example, and a line under "What no
   check can catch": a field's name taken for its meaning. `docs/plan.md` adds the habit to what
   the learner can do at the end, and a table with a candidate requirement for every chapter. Each
   chapter's notes now have a "Requirements" section, and a content test fails notes without one.
2. **The owner question, rebuilt on a new figure, `requirement`.** It shows the requirement in its
   own words and asks what the learner would store, with a fifth option to store nothing until
   they know what the owner is for. Once they choose, it shows the four questions the requirement
   could be asking, each beside what it needs stored, their own row marked; at a second press the
   lab reads the warehouse's owner, `etl_service`, and the same table marks which question it
   answers. The probe now also counts the warehouse's tables and those with an owner, so "every
   table has an owner" is the lab's to say. Both presses are kept, as a prediction is, and "start
   this chapter again" clears them.
3. **The closing note** says what a table's owner is in PostgreSQL, from its own documentation,
   and that the lab's warehouse models none of its rights.

### The third round's prose

Two fact briefs (`briefs/round-3/V` and `W`, with `common.md`) went to Haiku, from the fact sheet
updated against the lab and against PostgreSQL's documentation. What came back:

| Draft | Wrong, sent back | Dropped, restored with the fewest words |
| --- | --- | --- |
| V (the owner requirement, and the closing note's owner paragraph) | the closing note's paragraph faithfully carried two facts the brief had wrong: that a table in a real database has an owner (not every database gives a table one), and that only the owner may let other accounts use a table (PostgreSQL lets a right be given on); the fact sheet was corrected and the paragraph sent back as W | the first button said "Show what this means", one meaning where the figure shows four: "could" restored; "the four choices" with five on screen: "first"; the pointer to the table of questions: "listed below"; and "in the table" went, beside "the table" meaning a warehouse's |
| W (the closing note's owner paragraph) | none | none; its sentence on the lab came first, before the rights it calls "such", and moved to the end, with no word changed |

The whole-chapter read, from the built page at 320, 390 and 1280 pixels in both themes, before
the choice, after it and after the second press, found three things:

1. **The warehouse's owner said twice in a row.** The figure's own line ("records `etl_service`
   as the owner of `daily_sales` and an owner for 3 of its 3 tables") was followed by the
   explanation's "The warehouse records `etl_service` as the owner of all three tables". The
   explanation's sentence was cut; the paragraph now opens with the account all four programs log
   in as, and the facts test pins the line the figure computes instead.
2. **The table's headings began in lower case,** where the course's headings are in sentence case.
3. **At 320 pixels the table is 9 pixels wider than its box,** held open by `daily_sales` in the
   first column and "warehouse's" in the third heading, so the cue says it scrolls sideways. It
   fits from 360 pixels, the width the change lab's table was held to in the styling review, and a
   heading word may hyphenate where the browser can. Left so.

## The author's fourth round, 7 October 2026

The author gave a quality test for every interactive question: a prediction starts from what the
learner should learn, asks for a result the learner can observe and never for the explanation the
result is about to give, establishes an effect before asking for its cause, tests a belief against
independent evidence, and offers "I can't tell yet" where nothing seen settles the question. What
it became:

1. **The rule, bound.** `CLAUDE.md` ("Interaction is the explanation") now builds every prediction
   around its objective and keeps the stages of an investigation apart; `docs/authoring.md` and
   `docs/style.md` say how an option is written. Each prediction's notes answer eight questions,
   and a content test fails a prediction whose block misses one; the table "Predictions" had
   asked four.
2. **The audit of Chapter 1's five commitments.** The Thursday prediction failed: its "no" said
   that something on the way to `daily_sales` left orders out, a cause asked for before the
   learner had seen the effect. It now asks what Thursday's orders add up to, with 51.50, a
   different total, or "I can't tell yet", each with the belief behind it; the lab's 205.50 shows
   the difference, and only then does the explanation ask what might explain it, which the
   investigation answers. The rules prediction failed too: its options named a rule that decides
   no row, the explanation its result gives; they now say only whether another setting can match
   every row. The owner requirement, the change lab and the sort passed; their blocks say why.
3. **"I can't tell yet" in the prediction figure.** An `undecided` option that stands for no
   answer: it is marked neither right nor wrong, and its line says what the lab found.

### The fourth round's prose

One fact brief (`briefs/round-4/X`, with `common.md`) went to Haiku, from the fact sheet updated
against the lab. What came back:

| Draft | Wrong, sent back | Dropped, restored with the fewest words |
| --- | --- | --- |
| X (Thursday's prediction, the rules' options) | none | "I", lower-cased to "i" with the other options' lower case, restored. The draft also named the four days whose totals differ, which the brief had not listed: checked against the lab (Tuesday, Wednesday, Thursday and Saturday) and kept, and the facts test pins it |

The read of the built page, at 1280 pixels in the light theme and 390 in the dark, with each of
the three options committed, found the investigation's first task, to find the rows that make
Thursday's total differ, now answering the question the result ends on, and nothing to change.

## Thursday's cause, tested by the learner, 7 October 2026

Asked to do what is best for the learning, the Thursday difference now gets the second half of an
investigation, as the author's fourth round describes it: once the effect is seen, the learner
investigates the cause instead of being told it.

1. **A choice of explanation to test**, `why-thursday`, opens the investigation section, before
   the inspector: some of Thursday's orders are not counted, they are counted at lower values, or
   some are counted on another day. It keeps the choice and reveals nothing; its line says how to
   test it, with the inspector and then the query builder.
2. **A check after the learner's own work**, `why-thursday-check`, follows the rebuild challenge
   and stays locked until it passes, so it names no source before the construction is solved. At
   a press, the lab's new `day-gap` probe reads Thursday's orders against the rows the rebuild
   keeps: 4 of 7 kept at the same price and quantity on the same day, 3 not kept, worth 154.00,
   the whole difference, none lower and none on another day. The table marks the explanation the
   rows support, beside the learner's choice. It never says why the three were left out: the rules
   challenge finds that, and a content test fails either figure if it mentions a customer id.
3. **The reflection** no longer gives the numbers, which the check gave; it names what the three
   have in common, after the rules challenge has found it.

### Its prose

One fact brief (`briefs/round-5/Y`) went to Haiku, from the fact sheet's new section "Testing an
explanation for Thursday". What came back:

| Draft | Wrong, sent back | Dropped, restored with the fewest words |
| --- | --- | --- |
| Y (the choice, its check, the investigation's first task, the reflection's Thursday) | none | the investigation's first task came back capitalised, with a full stop and a semicolon inside it, in a list of lower-case items ending in semicolons: recased and repunctuated, no word changed; the check's button came back as nine words where the brief allowed five, and was cut to its first three, "Read Thursday's rows" |

The read of the built page, at 1280 pixels in the light theme and 390 in the dark, through the
choice, the locked check, the rebuild and the check, found two things, both fixed: the slot in
"You will test {choice}" holds a whole clause, so the line read "You will test some of Thursday's
orders are counted on another day", and a colon now introduces it, in both lines; and the check's
table was named by its own column heading, where it now takes the figure's caption.

## The author's fifth round, 7 October 2026

The author gave a guide to designing effective labs: every lab has a learning job and an action
that causes the learning; an interaction explains, lets the learner inspect, or is an experiment,
and a lab should be an experiment; everything shown has a purpose; an investigation runs in order;
the system is the learner's instrument; and an experiment has a consequence and teaches a skill
that outlives the course. The author singled out the difference between showing information,
inspecting it and experimenting for this site. What it became:

1. **The rule, bound.** `CLAUDE.md` gains "Experiments, instruments and explanations". A figure
   is a reference, an instrument or an experiment, says which in its badge, and should be the
   last where it can; an instrument always has a question in front of it. The page says
   "experiment" where the guide says "lab", because "the lab" is the Metadata Lab. "Predictions"
   in these notes became "Figures": a block for every figure, in the page's order, with twelve
   answers for an experiment (they take in the eight a prediction answered), two for an
   instrument or a reference, and "Part of" for a check that completes an experiment. The content
   tests fail a figure without a role or a block, or with an answer missing.
2. **The role on the page.** The platform (`snowch/learning-platform` at 8cd655b) lets a figure
   declare a role; the badge names it ("Experiment", "Inspect", "Reference") where every badge
   said "Lab", and its note says what the role asks before the lab's note.
3. **The audit of the thirteen figures.** The map is a reference, the dashboard and the inspector
   are instruments, and the other ten are experiments. The inspector failed: its caption, "Browse
   the seven assets and what storage records about each.", presented an instrument as the
   activity, the guide's own example. The investigation now opens with a decision, `where-first`:
   which asset to inspect first for Thursday's difference, and what to look for there. Each option
   is an asset and the evidence sought; after the choice, a line says what that asset can show,
   from its shape; and the inspector opens on that asset, as the instrument for the question. The
   choice of an explanation, `why-thursday`, moved after the inspector, so the investigation runs
   in the guide's order: is there a discrepancy (the Thursday prediction), where is it (the
   decision and the inspector), what could explain it (the choice of an explanation), which
   explanation fits (the check after the rebuild). The `hypothesis` figure became `decision`,
   which serves both.
4. **A giveaway the read found.** The figure just below the Thursday prediction is in view while
   the learner is still choosing, on a laptop and on a phone. Since Thursday's cause became the
   learner's to test (above), that figure had stated the prediction's result, 205.50; and since
   the second round, the inspector's first task, just below it, had said that Thursday's total
   differs. Each decision now waits for the answer before it (`waits`): the decision on where to
   look for the Thursday prediction, the choice of an explanation for that decision; until then,
   one line stands in its place. The decision's caption and the words above the inspector no
   longer mention the difference. A content test fails a figure below a prediction that states
   its result without waiting for it, and a caption, lead, after-text, task or section prose
   below it that states it.

### The fifth round's prose

Three fact briefs (`briefs/round-6/Z`, its send-back `Z2`, and `Z3`) went to Haiku. What came
back:

| Draft | Wrong, sent back | Dropped, restored with the fewest words |
| --- | --- | --- |
| Z (the roles' badges and notes, the decision, the inspector's caption and lead, the end of the Thursday prediction's explanation) | the lines on what `orders.parquet` and `clean_orders` can show said each keeps "one row per order": the brief's own fact, and false for `orders.parquet`, where order 7015 appears twice; the fact sheet was corrected and the two lines sent back as Z2. The inspector's list of things to try came back with three of its four items replaced by tasks the brief had not given, one of them the source the rebuild challenge asks for ("add up `clean_orders` per day"): the brief's items were restored | a full stop dropped from the badge's spoken name, and a colon put before `{choice}` in the learner's line, as the brief asked; the options' semicolons, copied from the brief's own list of facts, made the commas its instruction asked for; "It shows" and "opens on it", whose "it" could be read as another asset, became "The inspector shows" and "opens on the asset you chose". The caption came back with a purpose the brief had not given, "to find where Thursday's total became 51.50", which the read then found gave the prediction away: cut |
| Z2 (the two lines) | none | the lines came back lower-cased, as the brief listed them: capitalised |
| Z3 (the line in place of a figure that waits) | none | the curly quotes round the caption, which the brief asked for, and the fact that the earlier figure is above: restored, as “{caption}”, above |

The read of the built page, at 1280 pixels in the light theme and 390 in the dark, on load, with
each of the decision's four options committed and the inspector opened on each, and through the
choice of an explanation, found the giveaway above. Its fix was code and two cuts: the inspector's
first task and the question that opened its words ("where could Thursday's difference have
entered?"), both of which said the totals differ. The line after the decision now sends the
learner to the asset they chose, which that first task had done. The restatement of 205.50 and
51.50 in the choice of an explanation, after the long inspector, stays: each decision states the
facts its question needs.

## The lab's note, 7 October 2026

The author read the lab's note ("Every figure in this chapter runs the Metadata Lab, a small data
platform in your browser...") and could not tell from it what the lab is, whether its data sits in
the browser's storage, what the dates mean, or how a reader gets to the lab. The note now says:
the lab is a small data platform written for the course, which comes with the page as code and
runs in the browser; you use it through the figures, each of which asks it something; it holds the
shop, and runs the shop's SQL and yours with a query engine of its own; nothing about the shop is
stored, because each load builds the data and runs the week in memory; the week is the shop's
first week online, invented, and every date and time a figure shows comes from it; and the browser
keeps the learner's work, none of which leaves it. It serves every chapter, so it names no
figure and no chapter. A Playwright test now holds the last claim: while a learner works through
the chapter, the page asks only for the course's own files and sends nothing.

| Draft | Wrong, sent back | Dropped, restored with the fewest words |
| --- | --- | --- |
| AA (the note) | "programs that run each night and write them" said the programs write the files, which the shop's export writes; and the draft dropped seven facts, among them the shop's first week online, the answer to what the dates mean, and wrote "Nothing leaves it", which the page's own requests make untrue. Sent back as AA2, with the limit raised from 130 words to 170 | none |
| AA2 (the note again) | none | "the shop's" and "with real rows" (what the lab holds), "query" (its engine), "open" (nothing to open), and the sentence that the browser keeps your predictions, choices and answers, which AA2 dropped and AA had: AA's own sentence was put back. The note came to 203 words, over the 170 the brief allowed; each sentence carries one of the facts the author asked about, and the badge holds it behind a press, so it stays |

The read of the built page, at 1280 pixels in the light theme and 390 in the dark, in the map's
and the Thursday prediction's badges and at the foot of the chapter, found one repeat at the
foot: the note's last two sentences and, two paragraphs later, the line before "Start this
chapter again", which also says the browser keeps your work. The second names what starting again
clears, and the badges show the first without it, so both stay.

The author then found the note unclear: its second paragraph said the lab "runs the week again"
and that programs "run each night" before the third said what the week is, and "A query you
build, the lab runs." put its object first. The fault was brief AA's, which listed how you use the
lab before what it holds; the read had missed a definite article in front of a noun the note had
not introduced. The facts were put in the order a reader needs them (what the lab is, what it
holds, the week, how it runs, how you use it, what your browser keeps) and redrafted from brief
AB, which also asked for every sentence's subject first. The facts test now fails a note that
uses "the week" or "each night" before it gives the week's dates.

| Draft | Wrong, sent back | Dropped, restored with the fewest words |
| --- | --- | --- |
| AB (the note, reordered) | none | "small", "open", what the programs write, "invented for the course", "of its own" (the query engine), and a comma that keeps "a query you build, with the same query engine" from reading as one phrase. Haiku went on editing its file after the check had read it, and cut its draft to 200 words by dropping more facts ("as code", "itself", "date"); the note keeps the fuller version it wrote first, saved as `drafts/round-7/AB-first.md`. It comes to 225 words |

## Silence is preferable to filler, 7 October 2026

The author found filler on the page, "You have what you were told about the platform, kept to
hand. It asks nothing of you.", the line every reference figure's badge opened, and gave a rule:
every sentence must tell the learner something concrete, change what they should do, explain why
something matters, or set up a prediction or a decision; write for the learner's next action, not
for narrative flow; and remove any sentence the learner would not miss. `CLAUDE.md` ("Voice") and
`docs/style.md` bind it, and a content test fails the commonest forms the author named.

The whole chapter's text, 598 sentences, went to an independent reviewer on another model with the
rule, which found 13 clear cases and 25 doubtful. Each was judged in its context, by the same test:

- **Cut, 12 places.** The prediction section's preview of the two figures under it, which their
  captions and questions already say; "Now there is a difference to explain." and "First, where to
  look: the next section starts there."; after the check, "If you chose another explanation, the
  rows have ruled it out. The first explanation you test need not be the right one.", which the
  check's table already shows and which reassured; the inspector's "The inspector is your
  instrument for the question above." and its two sentences naming panels the learner can see;
  its after-text, which the construction's first sentence repeats; "This page has not shown them
  yet. Later chapters do."; "Back to Thursday." and "The course comes back to Thursday later.";
  "Real systems keep different things.", where the heading says it; and the reference line itself,
  so a reference figure's badge opens the lab's note alone. Each is a cut, with words moved only to
  keep a sentence whole ("It asks" became "The inspector asks", "Some keep" "Some real systems
  keep").
- **Redrafted, 2.** The experiment and instrument lines carried filler too ("the lab's evidence
  answers", "What you take away is..."). Brief AC asked for the next action only; Haiku returned
  "Commit to a prediction, a choice or a query you build. Compare what the lab shows with what you
  expected." and "Use this to answer the question just above. Look for the evidence the question
  needs.", and the check restored "first" ("Commit first"), because the order is the instruction.
  It dropped "it shows what the platform holds", which the figure shows, and that stays out.
- **Kept, the rest**, because removing each would lose a fact or an instruction: "The lab tells you
  this; storage does not." (where a fact comes from is the chapter's point); "How much can you find
  out from what storage holds?" (the chapter's question); "The data might." (the construction's
  hypothesis); "Both fit equally well." and "Storage shows the new file." (the reason, and the noun
  the next sentence needs); the lab note's lines the author asked for; and the pointer to the
  challenge that finds what the left-out orders share.

## The lab, explained once, 7 October 2026

The author found the lab named in the chapter's opening without being explained ("Every figure on
this page runs the Metadata Lab: a small data platform that holds the shop and runs in your
browser."), and then explained in full behind every figure's badge and again at the foot of the
page: since figures took roles, a badge's note was its role's line followed by the model's note,
and every figure here runs the same model.

- **The platform** (`snowch/learning-platform` at 3af8a81): a figure badged by its role opens its
  role's line alone, and a role with no line, here `reference`, has a badge that opens nothing. A
  book may give no note for a model, and the foot then states none.
- **The course** gives no note for the lab. The opening explains it once, where the chapter first
  names it: after the paragraphs on the shop's systems, assets and nights, and before the map.
  `CLAUDE.md`'s list of what no check catches gains the fault: a thing named before the page
  explains it, or explained again wherever it appears.

| Draft | Wrong, sent back | Dropped, restored with the fewest words |
| --- | --- | --- |
| AD (the lab's paragraphs) | "You have the shop", where the lab holds the shop; "Nothing is stored on a server", which turns the author's question about the browser's storage into a different answer (nothing about the shop is stored anywhere); and four dropped facts: that every figure runs the lab, that it comes with the page as code, that there is nothing to install, open or sign in to, and its query engine. Sent back as AD2 | none |
| AD2 (again) | none | none. Two repeats were cut: "Each night of that week the programs run", which the paragraph above says, and "the page sends none of it anywhere" after "Nothing you do leaves your browser". Haiku rewrote its file after the check had read it, cutting to 170 words by dropping facts ("real rows", "first week", "night by night"); the opening keeps the version it wrote first, saved as `drafts/round-8/AD2-first.md`, at 195 words |

The read of the built page, at 1280 pixels in the light theme and 390 in the dark: the opening
names the lab, then explains it, then shows the map; the map's badge opens nothing; the
dashboard's and the experiments' badges open one line each; the foot holds the model-versus-reality
note and nothing on the lab. The line before "Start this chapter again" still says the browser
keeps your work, because it names what starting again clears.

## The lab's mark, 7 October 2026

The author asked for the lab to be clear on the page, by a coloured box or an icon. Both were
mocked on the built page at phone width: the tinted box washed out the figures' own tinted notes
and outcomes and nearly hid a faded button, so the figures keep their white ground and every
figure that runs the lab carries a mark above its badge, a flask and the name "Metadata Lab"
(`docs/plan.md`). A Playwright test holds that every lab figure carries it, under the name the
opening explains.

## The author's cut to the lab's paragraph, 7 October 2026

The author cut "It comes with the page, as code," from the opening: the lab's paragraph now
says "It runs in your browser: there is nothing to install, open or sign in to." The words are
the author's, so no brief went to Haiku; `facts.md` follows.

## The opening in short steps, 7 October 2026

An agent's guide the author passed on found the opening right in what it said and wrong in how: a
long block of prose before the learner did anything (`docs/plan.md` has the decision). The opening
now reaches the first question in short steps: the situation and the lab; how the lab runs,
behind "About the Metadata Lab", a control the reader opens; the map, with the lab's count under
it and what an asset is under that; the shop's first week (`week`); then the dashboard's
question. The guide's architecture diagram drew an arrow along one row of assets, which reads as
one asset made from another, so the map keeps its arrows between systems. Its fourth diagram, the
lab as an instrument, was not built (`docs/plan.md` says why).

| Draft | Wrong, sent back | Dropped, restored with the fewest words |
| --- | --- | --- |
| AE (the opening) | none sent back. The control's label, "Lab engine; what your browser keeps", said neither in plain words, so the control carries the label the author's guide gave it, "About the Metadata Lab". Haiku changed two of fact 3's wordings, both kept: "kept between page loads" for "stored anywhere", since "stored" on this page means the chapter's storage, and "Nothing you do leaves your browser" alone for the page sending nothing | that the map shows the systems in the order data moves through them ("The map shows them") |

The second pass, on the built page at 1280 pixels in the light theme and 390 in the dark, with the
lab's details closed and open, cut three repeats of what a figure beside them shows: "Programs
move data between them." above the map, whose arrows say it; "The files, tables and dashboard on
the map are the shop's seven assets." under the map's count; and, in the week's key, what a
night's work does, which the sentence above the figure says.

## The lab, from the learner's side first, 7 October 2026

A second agent's guide the author passed on found the lab still explained in technical terms
before the learner was told what they do with it (`docs/plan.md` has the decision, and which of
the guide's words were not taken). The lab's paragraphs now say what the figures are for and what
happens when you use one, in the plain model every chapter uses: you ask, the lab checks, it shows
you, you work out what it means. How the lab is built moved behind the control, now "How the lab
is built". The map's lead lost "You cannot see the programs.", which the lab's paragraph says. The
facts test now fails the opening's own prose if it names the lab's insides (SQL, a query, an
engine, memory, a page load, code), and holds them in the details.

| Draft | Wrong, sent back | Dropped, restored with the fewest words |
| --- | --- | --- |
| AF (the lab, learner's side first) | none sent back. One wrong word put right: the lab runs the shop's first week "nightly", which says every night; it runs it night by night, at each page load. Haiku shortened fact 3 to its cap ("The shop is invented", "dashboard values" for the dashboard's rows, which is the more exact) and flagged that "a small data platform" names the lab as the shop's own platform is named; kept, since the lab is that platform and the author's guide uses the word | "The ... on this page" in "The figures on this page let you investigate the shop." |

The second pass, on the built page with the details closed and open, cut "You work out what it
means.", which the paragraph's last sentence says again.

## Which figures you read, and how you ask, 7 October 2026

The author read "You ask the lab a question by using a figure." and asked how, since the first
figure asks nothing. Both points held, read off the built page: the map, the shop's week and the
dashboard have no control, and the page never said how one asks in the others. The paragraph now
says the first three only show you the shop, and that in the others you choose an answer or the
parts of a query and press a button. `CLAUDE.md`'s plain model is now the model of a figure the
learner uses; a figure they only read shows what the lab works out. The facts test holds the
first three figures and the words for them, and the browser test that they have no control
outside their captions.

| Draft | Wrong, sent back | Dropped, restored with the fewest words |
| --- | --- | --- |
| AG (which figures you read) | none sent back. Haiku flagged "asset" used before the page defines it, under the map: ", an asset" was cut, and the sentence still holds, since in the inspector the button you press is an asset's name. "Query" stays: it is plain to the learner, and not a rationed term | "The first three figures," which says where the map, the week and the dashboard are, before the page has shown them |

## For the learner: the rules' rows after a run, and an extra row, 7 October 2026

The author passed on a second review, built from the internal review's findings before the
revision; nearly all of it was already fixed (`review/verdicts.md`, and "The review" above), and
its new proposals broke the course's rules (an owner option naming `etl_service`, exact numbers
as Thursday's options, metadata "kept separately from the data") or the lab (a stale time "could
mean a quiet night": in the lab a quiet night still writes, and updates the time). Two points held,
and the author said to do the right thing for the learner:

- **The rules' rows wait for a run.** The challenge on `clean_orders` showed how many rows the
  learner's rules keep while they chose them, and only one setting keeps the 44 rows
  `clean_orders` has, so the count could be matched without reading a row (R19's part the revision
  kept). The editor now shows the SQL as the learner chooses, and the rows the rules keep, with
  their count, only once the tests have run on the rules on screen; the verdict beside them names
  the orders the rules drop or keep wrongly. The query challenge keeps its live result: comparing
  its daily totals with `daily_sales` is how the learner finds the query, and its hints use it.
- **An extra row is extra.** After the failed night, Sunday's row is the learner's alone, and the
  table marked it "No" beside the words "Your query still rebuilds `daily_sales`". A row only the
  learner's result has does not stop a rebuild, which needs every row the target has; the change
  experiment's table now marks it "Only your query", in no colour (`matchCell`). The Thursday
  prediction's table keeps "No" for a missing day: there the question is whether two totals are
  equal day by day, and a missing day is a difference.

| Draft | Wrong, sent back | Dropped, restored with the fewest words |
| --- | --- | --- |
| AH (two labels) | none | none. "Only your query" went only where a query is set beside the asset it rebuilds, as the brief described; the first placing in the Thursday prediction's table too was this session's slip, put right before it was committed |

## "Figure" names a box; the action list stays internal, 8 October 2026

The author passed on an agent's design rule for the interactions, and then its own reply to this
session's reading of it. What held: on the page "figure" meant an interactive box in nine places
("The first three figures", "What this figure asks of you") and a number in five ("Is Thursday's
figure wrong", "Saturday's figure", "the same figure"), a word with two meanings on one page
(`CLAUDE.md`, "What no check can catch"). The five now say "total". What was kept as it was: "the
lab" is the Metadata Lab and nothing else, so the interactions are not called labs; the three
badges stay, and the agent's six actions (show, inspect, predict, test, investigate, experiment)
are a lens for designing and reviewing a figure, written into `CLAUDE.md` and `docs/authoring.md`
for the notes, never a label on the page. The author also asked that every block's objective say
what the learner should understand or discover, not what the figure displays: read against that,
all nine objectives above do (recognise that a requirement's word does not fix its meaning; see
that rebuilding an output does not identify the rules that made it), and the reference and
inspect figures' "Serves" lines name the question each serves. A content test now fails an
objective written as what the figure shows, and "figure" used for a number, as backstops.

| Draft | Wrong, sent back | Dropped, restored with the fewest words |
| --- | --- | --- |
| AI (five sentences, "total") | none | none |

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
- The map's button is this course's own, built in `packages/views`. If the digital-design course
  wants a figure that stays to hand, it is a candidate for the platform under the rule of two.
