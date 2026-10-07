# Chapter 1: The invisible data system

A working note, kept as the chapter was built on 6 October 2026 and revised on 7 October after the
author's second round: what was built, what was reused, what the prose process caught, and what
would be changed. The chapter's fact sheet, briefs, drafts
and review are in `docs/notes/chapter-01/`.

## What the chapter does

The learner gets the shop's storage and nothing else, and tries to answer what anybody asks of a
platform they did not build. As revised after the review and the author's second round:

- a map of the platform, near the start and to hand all through the chapter: the three systems in
  the order data moves through them, the assets each holds, and between them programs the
  learner cannot see; never a link from one asset to another;
- two predictions, each between two explanations of how the platform works: whether the owner
  the warehouse records names someone you could ask (it names the programs' account), and
  whether Thursday's raw orders add up to the dashboard's low figure (they come to 205.50 against
  51.50, as much as the days around it);
- an inspector over the seven assets: exactly what their systems record, and what storage says
  about the same eight questions for every asset, before the rows;
- a construction that rebuilds `daily_sales` from another asset with a query, "rebuild" defined
  once (every row the asset has, with the same values), which ends by asking whether rebuilding it
  shows how it was made;
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
  Thursday, leaves its cause open as the plan does, and places the four questions of Section 2.

## Predictions

Every figure that takes the learner's commitment before the lab answers, held to the rule in
`CLAUDE.md`: what the learner has seen by then, the explanations its options stand for, and how
the lab's answer tells them apart. The content tests fail a prediction without a row here.

| Figure | What the learner has seen | The explanations its options stand for | How the lab tells them apart |
| --- | --- | --- | --- |
| `predict-owner` | the map; the requirement in its own words, "Every table must have an owner."; the words: programs write the tables every night; the motivation's question "Who should I ask about `daily_sales`?"; their own experience of writing such a program | a choice, not a prediction: what they would store to meet the requirement if they wrote the program that writes `daily_sales` (a person, a team, the program, or the account it logs in as), or nothing until they know what the owner is for | nothing hidden is guessed: the figure first shows the four questions the requirement could be asking, each beside what it needs stored, and only then the probe reads the warehouse's owner, `etl_service`, an account, and the table marks which question that answers, the last; no reading is called right or wrong |
| `predict-days` | the dashboard: Thursday at 51.50, far below the other days; `daily_sales` holds the same figure | Thursday was a slow day, and the raw orders show it; or the orders came in, and something on the way to `daily_sales` left some out | the probe adds up Thursday's rows of `orders.parquet`: 205.50, more than 51.50 and as much as Wednesday or Friday; the table shows every day |
| `changes` | their own query rebuilding `daily_sales`; what each change does, in its label; the statuses and rows in the inspector; "rebuild" asking only for the rows the asset has | after the change the data points to one query, to more than one, or to none | the lab runs the week with the change and searches every choice the builder offers over every asset in storage: two after the copy, none after the edit, one after the failed night |
| `map` | storage's answer to each of the eight questions in the inspector; the query that rebuilds `daily_sales`; the changes; the rule for the data's group, stated above the figure | for each question: storage records it, the data suggests it, or only a record kept at the time answers it | the lab places each question by reading storage and trying every query the builder offers, and places them again for each change |
| `predict-rules` | their own passing rules; the rows each rule keeps as they change it; the quantities in `orders.parquet` | every rule they chose decides some row this week, so theirs is the only setting that passes; or some rule decides no row, so more than one does | the lab tries all sixteen settings: two pass, differing only in the rule for a quantity of 0 or less, which no order this week has |

Before the second round, two predictions failed this rule. The owner prediction offered four
kinds of owner (a person, a team, the program, an account), a fact about how this shop set up its
warehouse that nothing on the page let a learner reason to. The days prediction asked on how many
of seven days the raw orders equal `daily_sales`, a number that depended on which days held a
cancelled order, a repeated one or orders with no customer id, none of which the learner had seen.
The change lab's edit was labelled "edited for refunds", which said nothing a learner could reason
from; its label now says what the edit keeps, from Saturday's row on. The rules prediction asked
for a count (one, two, three or more) where the question is whether every rule decided a row.

The owner question took two rounds. The second round asked whether the owner would name someone
you could ask, yes or no, and the author found it still a guess: either answer could be right, and
which one depends on how this shop happened to set up its warehouse, which nothing on the page
shows. At the author's suggestion it now asks what the learner would store as the owner of
`daily_sales` if they wrote its program, with the first version's four options, and the lab shows
the shop's `etl_service` beside their choice, marked neither right nor wrong. The figure's
`choose` mode carries this, and `CLAUDE.md` now says when to use it.

In the third round the author asked for more than a fair choice: the question should teach the
learner to question a requirement. It now gives the requirement in words, "Every table must have
an owner.", asks what the learner would store, lets them choose nothing until they know what the
owner is for, then shows the four questions the requirement could be asking before it shows the
warehouse; "Requirements", below, has the whole of it.

## Requirements

The requirement this chapter questions (`CLAUDE.md`, "Question the requirement"), and how its
figure keeps the five things apart. The content tests fail these notes without this section, and
a requirement figure it does not name.

**"Every table must have an owner."**, in Section 3, the figure `predict-owner` (kind
`requirement`):

1. What it literally says: every table has an owner.
2. What it might mean: who is responsible for `daily_sales`; which team is; which program writes
   it; which account controls it in the warehouse.
3. What each meaning needs stored: a person; a team; the program; an account.
4. What the platform records: the lab's warehouse records `etl_service`, the account all four
   programs log in as, as the owner of each of its three tables; its own meaning is the account
   that controls the table, as a table's owner is in PostgreSQL (`docs/sources.md`).
5. Whether that meets the requirement: as written, yes, every table has an owner; as meant, only
   under the fourth meaning. The motivation's "Who should I ask about `daily_sales`?" needed the
   first or the second, and the warehouse's owner names neither.

The learner commits before they see the meanings, may choose to store nothing until they know
what the owner is for, and sees the meanings before the warehouse. Nothing calls a meaning wrong;
the table marks only which question the warehouse's owner answers, in plain words, without colour.

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
