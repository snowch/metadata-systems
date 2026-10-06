# Chapter 1, the reading half: findings

Reviewed as the learner meets it: a competent software or data engineer, no earlier chapter, none of
the course's documents. Inputs: `review/page.md`, the nine screenshots, `facts.md`, the lab under
`packages/lab/src`, and `docs/style.md`.

## Summary

32 findings: 3 high, 17 medium, 12 low. They are ordered by severity, then by page order.

The three that matter most:

- **R2**: in the failed-night result, the figure's list says no query rebuilds `daily_sales` while the
  paragraph beside it says the learner's query still rebuilds every row it has.
- **R3**: "From storage, a failed night looks like a night with nothing to write" is not what the lab
  computes, and the figure prints the evidence against it in its first line.
- **R1**: the page says the reporting tool records nothing about where the dashboard's values come
  from, then says it keeps the query behind its chart.

Section 6 (the failure experiment) carries six findings in all (R2, R3, R9, R10, R11, R12). It is the
chapter's third objective and its strongest idea, and it is where the page is least reliable.

## Scope and limits

- **Not seen.** page.md does not show either challenge in a passing state, the five hints for each
  challenge, the feedback for a wrong prediction, or any state after a reload. I have not reviewed a
  success message or a hint, and either could repeat or leak what a finding below flags.
- **Read from screenshots.** The front-page text and the last line of the chapter ("The next chapter is
  still to be written.") are not in page.md; I read them from the screenshots.
- **How I checked.** I ran the lab from the scratchpad (bundled with esbuild; nothing under the
  repository was changed) to check every number and the behaviours that R2, R3, R11, R17, R24 and R29
  rely on. To confirm what controls exist and when text appears I read the source of five figures
  (ChangeLab, QuestionMap, ChoiceEditor, StorageInspector, LabPrediction). I grepped `docs/sources.md` for the
  real-system claims in the note at the foot of the page. I did not read `docs/plan.md`.
- **Timing.** page.md and the screenshots come from the build of 18:27. The source was edited at 18:32
  (ChangeLab, QuestionMap, LabPrediction, StorageInspector, strings, labels) and the site was rebuilt at
  18:39. Where the current source touches a finding I say so (R2, R15, R29). Nothing here has been checked
  on the rebuilt page.
- **Challenge answers.** No finding states a solution of either challenge. R12 describes where the
  first challenge's solution is exposed without repeating it, and R19 does not state the second's.

## Checked and fine

- Every number I checked matches the lab: the storage records of all seven assets (rows, sizes, times),
  the daily totals, the three matching days and which they are, the failure-experiment lines (the new
  file, Saturday's value, the six-row table and its stale time), the test feedback (3 of 7, 5 of 7, 48 and
  42 rows, the orders named) and the weekdays.
- None of the words the fact sheet forbids appears on the page. "Metadata" first appears in Section 8, apart from the
  site name and the note at the foot of the page.
- No em dashes or en dashes anywhere in the page text.
- The closing note of the failure experiment appears only after all three changes have run
  (ChangeLab.tsx), so its presence under "No change" in page.md is the script's order, not a premature
  reveal. I did not count it.

---

## High

### R1. The reporting tool "records nothing about where the values come from", then "keeps the query behind its chart"

- **Where**: Section 4 (Investigation), inspector with sales_dashboard chosen; Section 7 (Explanation),
  third paragraph; Section 1 (Question), last paragraph.
- **Quote**: Section 4, under "What does it show?": "The reporting tool records the title, Sales, last 7
  days, and nothing about where the values come from." Under "What is it made from?": "Storage records
  nothing that answers this." Section 7: "None of the three systems recorded these because they were not
  needed to store or serve the data. Some of the systems do keep records for their own work that you were
  not shown: the reporting tool keeps the query behind its chart, and something keeps the programs and
  their timetable." Section 1: "You can read everything the shop's storage holds."
- **Problem**: The chapter's central claim is that no system records what made an asset. For the
  dashboard the page says first that the reporting tool records nothing about where its values come
  from. It then says, in the paragraph that opens by saying none of the three systems recorded what made
  an asset, that the reporting tool keeps the query behind its chart. That query is a record of exactly
  what made it. The learner cannot tell which statement is true, and an engineer who has used any
  reporting tool will doubt the first before reaching the second. The lab models neither sentence as
  written: its storage view of the dashboard holds the title, creator, creation time, last refresh and
  values and no query (storage.ts), and the SQL that fills the dashboard is the fourth program,
  dashboard_refresh (programs.ts), run by etl_service, not a record the reporting tool keeps. The fact
  sheet lists what each system records "and nothing else", and the reporting tool's list has no query,
  so the Section 7 sentence has no support there either. "That you were not shown" also sits badly with
  Section 1's promise that everything storage holds can be read.
- **Severity**: high.
- **Direction**: Decide what the lab's reporting tool keeps and make the Section 4 lines, the Section 7
  paragraph and the Section 1 promise say the same thing. If a record exists but this chapter does not
  let the learner read it, the inspector has to say it is not shown, not that nothing is recorded. Or
  remove the reporting-tool sentence from Section 7 and introduce the query where a later chapter first
  shows it.

### R2. Failed night: the list says no query rebuilds daily_sales, the paragraph says the learner's query still rebuilds every row

- **Where**: Section 6 (Failure experiment), the change "the last night's write of daily_sales fails",
  after running. The term is defined in Section 5 (Construction).
- **Quote**: The list under "EVERY QUERY IN THE BUILDER'S CHOICES THAT REBUILDS DAILY_SALES": "No query in
  the builder's choices rebuilds it." The outcome paragraph below it: "Your query still rebuilds every
  row daily_sales has, and gives one more: Sunday." The table beside them has, for Sun 13, your
  result 97.75, daily_sales "no row" and the match "No". Section 5: "If a query over another asset
  gives exactly the same rows as daily_sales, that query is a candidate for how it was made."
- **Problem**: The figure contradicts its own text in the same panel. Underneath it is a word used in two
  senses: "rebuild" means exactly the same rows in Section 5 and every row the asset has, plus perhaps
  more, in the outcome paragraph. The learner cannot tell whether the failed night broke the match,
  which is the thing the experiment exists to show.
- **Severity**: high.
- **Direction**: Choose one meaning of "rebuild" and use it everywhere. For this change say what is true
  in plain terms: the query reproduces the six rows that exist and adds a seventh that does not. Make the
  list agree with that sentence. Source note: ChangeLab.tsx was edited after this page was generated and
  now counts a query that reproduces every row the asset has as a rebuild (the lab's "covers" rule, and
  its code comment describes this very case). If the rebuilt page lists the query for this change, the
  list and the paragraph agree, but the list now uses the second meaning while Section 5 states the
  first, so the wording still has to be reconciled.

### R3. "From storage, a failed night looks like a night with nothing to write" is not what the lab shows

- **Where**: Section 6, the failed-night outcome and the closing note; Section 7, the map's row "Did last
  night's write work?".
- **Quote**: "From storage, a failed night looks like a night with nothing to write." The first line of
  the same figure: "daily_sales last written at 2026-09-13 02:30:21 UTC, not 2026-09-14 02:30:21 UTC."
  Closing note: "a failure made a missing row look like a quiet night." Section 7, plain week: "Did last
  night's write work? Last written at 2026-09-14 02:30:21 UTC, with a row for Sun 13."
- **Problem**: In the lab a night with nothing to write does not look like this. A day with no orders
  gives the program zero rows, and week.ts still stamps the table with the program's finish time, so a
  quiet night moves the last-written time to Monday 02:30. A failed night is the only case that leaves
  the time a day stale, while clean_orders (02:05) and the dashboard (03:00) were rewritten that same
  morning. So storage does show a difference, and the figure prints it in its first line. The chapter's
  own rule for "Did last night's write work?" (last-written time plus the latest row) would not say
  "worked" for this week either: the lab's question map for the failed week reports the latest row as
  Sat 12 against an expected Sun 13. The sentence is true of the rows alone. It is the chapter's one
  example of misleading evidence, and the closing note repeats it. The fact sheet states the same claim,
  but a figure must show what the lab computes, and the lab computes otherwise.
- **Severity**: high.
- **Direction**: Say what is actually indistinguishable (six rows, no Sunday) and let the stale time be
  the clue the learner has to notice and weigh. If the lesson is that the evidence is weaker than it
  looks, the lab needs a quiet-night week so that the claim is computed; otherwise cut the comparison
  with a quiet night. The inspector's own phrase, "not whether a write was due", already says the true
  thing.

---

## Medium

### R4. The opening question and the four motivating questions are never closed

- **Where**: Section 1 (Question); Section 2 (Motivation); Sections 5 to 10 (where it is missing);
  Section 7 (Explanation).
- **Quote**: "Thursday is far lower than other days. The head of the shop asks you why." Section 2 lists
  "Can we delete products.parquet?", "What stops working if the checkout renames a column in
  orders.parquet?", "Is Thursday's figure wrong, and since when?" and "Who should I ask about
  daily_sales?". Section 7: "Your questions were about the platform around the data: what a number
  means, who answers for an asset, what made it, what reads it, what changed."
- **Problem**: The chapter is framed by Thursday and never returns to it: after Section 2 the word
  appears only in a test-feedback label. A learner who finishes has every piece (three Thursday orders
  with no customer id are in orders.parquet and not in clean_orders) but is never told that this accounts
  for the gap, nor that whether dropping them is a mistake or a decision is something no record shows.
  The refunds change gets exactly that framing ("Nothing says whether Saturday is a mistake or a
  decision."); the question the learner came with does not. The other three Section 2 questions are
  dropped as well. In the lab no program reads products.parquet (programs.ts), so "Can we delete
  products.parquet?" has an answer in the shop; the page neither gives it nor says why the learner
  cannot find it. And "Your questions" in Section 7 matches neither set: the learner has worked through
  the eight questions in the inspector, which the prose never lists, and "what a number means" is not
  one of them.
- **Severity**: medium.
- **Direction**: Close the arc in the Generalisation or the Reflection: return to Thursday (what the data
  shows and the part it cannot show) and place the four Section 2 questions in the three groups. List the
  eight inspector questions once, early, and say how the four relate to them.

### R5. Both predictions in Section 3 can be answered without a real expectation

- **Where**: Section 3 (Prediction), both figures.
- **Quote**: "The warehouse records an owner for every table. What will it name as the owner of
  daily_sales?" with the options "an account that programs log in as", "a person", "a team, such as
  finance", "no owner at all". And "On how many of the seven days will your total equal daily_sales?"
  with "on all seven days", "on some days but not all", "on no day".
- **Problem**: First prediction: the prompt says the warehouse records an owner for every table, so "no
  owner at all" is ruled out by the question itself. Three options are generic categories; the first is
  a specific mechanism (what programs do) that the page has not introduced and Section 1 only hints at
  ("Programs you cannot see yet write the tables"). A learner picks it because it is the odd one out, not
  because they expect it, and the explanation then says the course tells them this. Second prediction:
  after a set-up built around a low Thursday, "some days but not all" is the only live option, and "on no
  day" cannot be taken seriously. The question asks "on how many" but the options are categories, so the
  learner commits to nothing numeric. The question also presumes that daily_sales is built from
  orders.parquet, which Section 5 later presents as something to test. "Predict again" lets the learner
  re-answer after seeing the result.
- **Severity**: medium.
- **Direction**: Make the options parallel in kind, drop the option the prompt rules out, and ask for
  something the learner can get wrong in an informative way (which days differ, or by how much) instead
  of a three-way category. Do not build the hypothesis into the question.

### R6. The page says both that the course tells you etl_service is an account and that storage records an account

- **Where**: Section 3 (after the first prediction); Section 4 (inspector, the three warehouse tables);
  Section 7 (map, right-hand group).
- **Quote**: "etl_service is the account the shop's programs log in as. The course tells you this;
  storage does not. So the owner field says which login created the table, not which person or team
  answers for it." Inspector: "The warehouse records the account etl_service, not a person or a team."
  Map: "Storage names etl_service, an account, not who answers for it."
- **Problem**: Section 3 says storage does not tell the learner that etl_service is an account. Section 4
  and the map say storage records or names an account. The difference between what a field holds (a name)
  and what the course knows about it is the lesson of the first prediction, and the later text breaks
  it. Separately, "says which login created the table" is not supported by the fact sheet or the lab:
  the lab records the account as the table's owner and records nobody as its creator.
- **Severity**: medium.
- **Direction**: In the inspector and the map say the warehouse records the name etl_service (and, where
  useful, that the course knows it is the programs' account). Drop "which login created the table" or
  replace it with what the lab supports, which is which account owns it.

### R7. The Investigation hands the learner the discoveries and the absences

- **Where**: Section 3 (end of the second prediction); Section 4 (Investigation).
- **Quote**: "On each of those days, orders.parquet holds a row that daily_sales does not count. You will
  find those rows in the next section." "Things to try": "In orders.parquet, find the rows whose
  customer_id is NULL, and their day." / "Find an order_id that appears twice." / "Find the orders whose
  status is cancelled." Inspector, four of the eight lines for orders.parquet: "Storage records nothing
  that answers this." Closing note: "It does not say which program wrote an asset, from what, or why some
  orders in orders.parquet are missing from clean_orders."
- **Problem**: The finding is handed over three times before the learner makes it. The prediction result
  says rows are missing; the "Things to try" name the three anomalies (a NULL, a repeated id, a status);
  and the closing note, which shows while orders.parquet is open and before the learner has compared the
  row counts, states the conclusion. The absences are pre-written too: for each asset the learner reads
  "Storage records nothing that answers this" instead of looking for an answer and not finding one. The
  chapter's own principle is that the learner discovers what data cannot say.
- **Severity**: medium.
- **Direction**: Replace the three prescriptions with one open task tied to the mismatch table (find what
  accounts for a day's gap). Let the learner say where each question might be answered before the
  inspector replies. Move the closing note after the learner has made the comparison, or cut what it
  repeats.

### R8. At phone width the Investigation hides the columns its tasks need

- **Where**: Section 4 inspector (phone-dark-storage.png); Section 5 builder
  (phone-dark-build-daily-sales.png).
- **Quote**: The tasks ask for "the rows whose customer_id is NULL, and their day" and "the orders whose
  status is cancelled". The phone screenshot shows the 48-row table stopping after its third column
  (ORDER_ID, CUSTOMER_ID, PRODUCT_ID); quantity, price, status and ordered_at are off-screen with no
  visible cue. In the builder the first line of the SQL reads "SELECT CAST(ordered_at AS DATE) AS day,
  SUM" and stops at the edge. In the inspector text a timestamp breaks at a hyphen: "at 2026-" then
  "09-14 01:00:41 UTC."
- **Problem**: Unless the learner thinks to swipe the table, a phone learner cannot complete two of the five
  tasks, because the day and the status are in the hidden columns. They also cannot see the part of the
  query that changes with the "Measure" control. The eight questions the figure exists for sit below the
  whole 48-row table, so the point of the figure is the hardest thing to reach.
- **Severity**: medium.
- **Direction**: Give wide tables a visible scroll cue or let them reflow; put the questions before the
  long table or let the learner jump to them; wrap the SQL; stop dates breaking at hyphens.

### R9. The failure experiment asks for predictions it cannot collect, and its heading answers the first

- **Where**: Section 6 (Failure experiment), figure before running.
- **Quote**: Heading: "Three changes storage does not record". Prose: "Before you run each change, make a
  prediction. Will storage show the change? Will your query still rebuild daily_sales?" The figure is
  four radio buttons (default "No change") and "Run the week again".
- **Problem**: Section 3 has committed predictions (choose, then "Check my prediction"). Section 6 is the
  chapter's third objective and has none: nothing records what the learner expects, and the learner can
  press "Run the week again" on the default and read the result with no expectation formed. The first
  question is answered by the heading above it. The second does not aim at the point: for the copy it is
  a yes, and the interesting result is that a second query also matches. The "refunds" option names a
  reason for the edit, not what the edit does, so there is nothing to predict from.
- **Severity**: medium.
- **Direction**: Add a committed prediction per change before the result shows, aimed at what the
  experiment teaches (how many queries now match; whether anything in storage says what happened). Retitle
  the section so the heading does not state the outcome.

### R10. "What storage shows differently" is a comparison only the lab can make

- **Where**: Section 6, all three changes; Section 7, right-hand group.
- **Quote**: Under "WHAT STORAGE SHOWS DIFFERENTLY": "In daily_sales, the row for Sat 12 reads 215.49, not
  191.49." and "daily_sales last written at 2026-09-13 02:30:21 UTC, not 2026-09-14 02:30:21 UTC." Against
  Section 7: "What changed in it this week? Storage keeps only the current rows." And the closing note:
  "None of the three changes left anything in storage that says what happened."
- **Problem**: Each line pairs the new value with the old one ("not 191.49"). In the changed week storage
  holds only 215.49; the old value exists only in the lab's other, unchanged week. The figure therefore
  shows exactly what the chapter says storage cannot show, under a heading that says storage shows it.
  A learner can reasonably conclude that storage did reveal the change.
- **Severity**: medium.
- **Direction**: Label the comparison as the lab's view across two weeks. Better, show first what an
  engineer in the changed week sees (one set of values and times, no "before"), then reveal the
  comparison as something only the lab can compute. Make the heading and the closing note agree.

### R11. "Impossible" claims more than the lab shows, and the caveat is at the foot of the page

- **Where**: Section 6 closing note; Section 8 (Generalisation), second paragraph; the model-versus-
  reality note at the end.
- **Quote**: "A copy made the answer ambiguous, an edit made it impossible, and a failure made a missing
  row look like a quiet night." Section 8: "The middle column holds answers the data suggests. They can
  be ambiguous, impossible or misleading." The note: "The lab's search covers only the query builder's
  choices. "No query rebuilds it" means none of those choices."
- **Problem**: After the edit, no choice the builder offers rebuilds daily_sales; a query with a date
  condition would, and so does the real program's own query. "Impossible" claims more
  than the builder's menu can show. An engineer will think of the date condition at once, and the page
  admits the limit only in a note after the Reflection. In the lab's own map the edit does not leave an
  impossible answer in the middle group either: "What is it made from?" leaves the middle group for the
  right-hand one (I confirmed this with the lab), so the Section 8 sentence describes a state the map
  never shows.
- **Severity**: medium.
- **Direction**: Say what is shown: no query the builder offers matches, and nothing in the data would
  suggest trying a rule that changes on a date. Put the limit next to the claim. Reword Section 8 so
  that "impossible" describes a question leaving the middle group.

### R12. The construction challenge's solution is printed in later figures for a learner who has not passed it

- **Where**: Section 6 (the list under "EVERY QUERY IN THE BUILDER'S CHOICES THAT REBUILDS DAILY_SALES");
  Section 7 (two cells of the middle group).
- **Quote**: "You have not built a passing query yet, so this uses the course's." Section 6 prose: "It uses
  your query from the construction section if it passes its tests, and the course's query if it does
  not."
- **Problem**: A learner stuck on Section 5 can press "Run the week again", or scroll to Section 7, and
  read, in words, the asset, the rows kept, the measure and the grouping that solve it. The challenge's
  own tests refuse a wrong attempt, but these figures hand over the answer with no test. The map shows it
  unconditionally. This also removes the discovery that the second objective depends on. "The course's
  query" is a noun the page never introduces.
- **Severity**: medium.
- **Direction**: Gate the wording behind a pass. For an unsolved learner show the count ("one query
  matches") without its settings, or run the experiment on a fixed description that is not the
  challenge's solution.

### R13. Section 7 explains what systems record as if by necessity; the lab and the page's own note do not bear it out

- **Where**: Section 7 (Explanation), second paragraph; the model-versus-reality note; the inspector for
  sales_dashboard.
- **Quote**: "Each system records only what it needs for its own work. The warehouse must know the columns
  and types to run a query, and the owning account to control who may read." Note: "Some warehouses record
  no owner and no last-altered time." Inspector: the dashboard's fields "Created" and "Created by
  j.marsh".
- **Problem**: This is the chapter's reason why metadata is missing, stated as fact. The lab simply
  chooses which fields each system keeps (storage.ts); it does not model need. The page's own evidence
  cuts against the claim: the reporting tool records who created the dashboard, which it does not need to
  draw a chart, and the note says some warehouses record no owner at all, which they cannot then "need"
  for access control. An engineer may also object that access control rests on grants and roles rather
  than on a recorded owner. The two real-system claims in the note (no owner or last-altered time in some
  warehouses; versions and read logs in some object stores) are supported by neither the fact sheet nor
  the lab, and `docs/sources.md` has no entry for them.
- **Severity**: medium.
- **Direction**: Present the explanation as the lab's design (these are the fields the lab's systems
  keep), or ground the "need" argument in something the learner can see. Drop "must" and the
  access-control rationale, or source them. Source or cut the real-system claims in the note.

### R14. Sentences a competent engineer must read twice

- **Where**: Section 7 (the lead into the map and the third paragraph); Section 8, third paragraph.
- **Quote**: "The lab places each question in one of three columns: storage records it; the data suggests
  it because a query rebuilds the asset or another asset shows the same numbers; or only a record kept
  at the time answers it." (40 words) / "A platform needs three kinds: what each asset is (its meaning, the
  units it uses, who is answerable for it); what happened (what programs ran, when they ran, whether they
  worked); and what was made from what." (37 words) / "Some of the systems do keep records for their own
  work that you were not shown: the reporting tool keeps the query behind its chart, and something keeps
  the programs and their timetable." (33 words) / "The lab finds each place by running storage and
  trying queries in the query builder, not from a list."
- **Problem**: Each packs a list of clauses behind a colon (style rule 1); the first two add a clause
  inside a clause or nested parentheses. The first carries the chapter's main distinction. "Running
  storage" is not something one does, and "not from a list" points at a list the learner was never told
  about.
- **Severity**: medium.
- **Direction**: Split each. Put the three groups in a list with one line each. Say what the lab does (it
  reads storage, then tries every query the builder offers) and cut "not from a list" unless the learner
  has met the list.

### R15. The middle group's stated rule does not fit all its questions, and two of its cells repeat each other

- **Where**: Section 7, the sentence before the map and the map's middle group; the inspector's line for
  "How are its numbers worked out?".
- **Quote**: "the data suggests it because a query rebuilds the asset or another asset shows the same
  numbers". The middle-group cells for "What is it made from?" and "How are its numbers worked out?"
  carry the same "One query rebuilds it: ..." sentence. "Did last night's write work?" reads "Last
  written at 2026-09-14 02:30:21 UTC, with a row for Sun 13." Inspector: "How are its numbers worked out?
  Storage records 7 column names and their types, not what they mean."
- **Problem**: (a) "Did last night's write work?" sits in the middle group because of its last-written
  time and its latest row, which the stated rule does not mention. (b) Two questions the learner is meant
  to see as different carry an identical answer, so the second reads as a repeat. (c) In the inspector,
  "How are its numbers worked out?" is answered with "not what they mean": the answer is about meaning,
  not derivation. Section 7 then lists "what a number means" among the learner's questions, which the
  eight do not contain.
- **Severity**: medium.
- **Direction**: State the rule so that it covers every question in the group (what the data, together
  with storage's times, lets you infer). Give "made from" and "worked out" visibly different answers (the
  source, then the calculation). Make the inspector's answer say something about the calculation. Source
  note: QuestionMap.tsx was edited after this page was generated and now words "made from" differently
  ("One asset rebuilds it: ..."), which addresses (b); confirm on the rebuilt page.

### R16. "Column" means two things, and "middle column" and "right-hand column" are false at phone width

- **Where**: Sections 4, 7 and 8; phone-dark-map.png.
- **Quote**: "Storage records 7 column names and their types, not what they mean." (a table's columns)
  against "The lab places each question in one of three columns", "The middle column is evidence, not an
  answer." and "The right-hand column holds questions no amount of data answers: who is answerable for
  each asset, what unit a number uses, what changed."
- **Problem**: Two senses of "column" within one section. In the phone screenshot the three groups stack
  as three boxes, so "middle" and "right-hand" refer to nothing; the learner has to work out that
  "middle" means the second box. These sentences carry the chapter's main distinction.
- **Severity**: medium.
- **Direction**: Name the three groups by what they are ("what storage records", "what the data
  suggests", "what only a record kept at the time answers") and refer to them by those names. Keep
  "column" for table columns.

### R17. The learner never sorts a question, and the map never moves in front of them

- **Where**: Section 7 (map figure); Section 8 (second map); the fourth objective.
- **Quote**: Objective: "Sort questions about an asset by what can answer them: storage, the data, or
  only a record kept at the time." Section 7: "The lab places each question in one of three columns" and
  "The lab finds each place by running storage and trying queries in the query builder, not from a
  list." Section 8: "Look at the middle column for "What is it made from?"."
- **Problem**: The figure shows the finished sort in both places and has no control. "Computed, not from
  a list" is asserted in words and the learner cannot see it: the map is fixed to the plain week and to
  the copy week, whatever the learner did in Section 6. The most telling case, where the edit makes "What
  is it made from?" leave the middle group for the right-hand one, is never shown (the lab computes it).
  The second map replays the copy result a third time (see R20) and tells the learner where to look
  before showing it.
- **Severity**: medium.
- **Direction**: Have the learner place the contested questions before the lab does (a prediction per
  question or per group), then show the lab's placement. Tie the map to the weeks the learner ran, so the
  question visibly moves. Drop the "look at" instruction.

### R18. "Metadata" arrives as a told definition; "three kinds" is asserted, not derived; "record" now means two things

- **Where**: Section 8 (Generalisation), third paragraph; the headings of the Section 7 map.
- **Quote**: "Records about assets and about the platform, written down and kept separate from the data
  itself, are called metadata. A platform needs three kinds: what each asset is (its meaning, the units
  it uses, who is answerable for it); what happened (what programs ran, when they ran, whether they
  worked); and what was made from what." Map headings: "Storage records it" and "Only a record kept at
  the time answers it".
- **Problem**: (a) The course's principle is that the term arrives from questions the learner could not
  answer. Here it arrives by definition, and "three kinds" has no visible link to the eight questions or
  the three groups the learner has just used. The two threes (three groups, three kinds) share a section
  with no stated relation and do not line up: "Did last night's write work?" is "what happened" but sits
  in the middle group; "what changed" is "what happened" and sits in the right-hand one. (b) By this
  definition what storage already keeps (column names, types, sizes, times, owning account) is also
  "records about assets ... kept separate from the data", so the learner cannot tell whether metadata
  means everything storage keeps or only what it lacks. (c) "Record" is a verb for the fields storage
  keeps and a noun for the note someone must write at the time, and the Section 7 headings put both in one
  figure.
- **Severity**: medium.
- **Direction**: Derive the kinds from the questions: mark each unanswered question with the kind of
  record that would answer it, then name the kinds. Say whether storage's own fields count and why they are
  not the subject. Keep one sense for "record", or give the two senses different words.

### R19. Challenge 2 has no stated purpose, can be solved by matching a number, and its lesson is told afterwards

- **Where**: Section 9 (Challenge) and Section 10 (Reflection).
- **Quote**: Section 9's only prose: "The rules appear as SQL below the choices, with the number of rows
  they keep." Heading: "Recovering the rules of clean_orders". Figure: "The rules keep 48 rows."
  Reflection: "No order this week had one, so both answers to that rule passed your tests, and no rebuilding
  from this week's data could find the rule."
- **Problem**: The section describes the figure but does not say why the learner is recovering these
  rules or what to notice. The figure prints how many rows the rules keep, and the Investigation has
  already given the learner clean_orders' row count, so the challenge can be solved by turning controls
  until the numbers agree, without asking why any rule is there. The point of the challenge (a match does
  not identify the rule) reaches the learner only as a statement in the Reflection, and "both answers to
  that rule passed your tests" is true only if the learner happened to try both, which nothing prompts.
  The heading promises recovery of "the rules" while the Reflection says a rule cannot be recovered. The
  second objective asks the learner to say what a match does and does not prove; the page states it in
  the Reflection instead.
- **Severity**: medium.
- **Direction**: Give the section a purpose and a prediction (for example, whether any other setting
  could also pass). After a pass, prompt the learner to change each control in turn and watch whether the
  tests still pass. Retitle the section so it does not promise recovery.

### R20. The same conclusion is stated five times

- **Where**: Objectives; Section 6 closing note; Section 7 last paragraph; Section 8 (second paragraph and
  the figure); Section 10, first paragraph.
- **Quote**: "...how evidence from data becomes ambiguous, impossible or misleading." / "A copy made the
  answer ambiguous, an edit made it impossible, and a failure made a missing row look like a quiet
  night." / "The failure experiment showed it: the evidence can change when an analyst adds a copy, when a
  program is edited, or when a night's work fails." / "They can be ambiguous, impossible or misleading." /
  "The data suggested where daily_sales comes from, until a copy, an edit or a failed night."
- **Problem**: One three-part point appears five times in near-identical form. The analyst's copy result
  (two sources, cannot tell which) also appears in Section 6, then again in the Section 8 figure's
  caption, its cell and its closing paragraph. What storage records is summarised three times as well
  (Section 4's closing note, Section 7's first paragraph, the Reflection's first sentence). The learner
  starts to skim, and the Reflection, which should add something, repeats.
- **Severity**: medium.
- **Direction**: State the triple once, where the learner has just seen it. Let Sections 7 and 8 build on
  it. Cut the Section 8 closing paragraph or the figure's caption. In the Reflection, add what the chapter
  has not said.

---

## Low

### R21. The objectives announce the chapter's findings in terms the learner has not met

- **Where**: Objectives, top of the page.
- **Quote**: "Show, with three changes to the shop, how evidence from data becomes ambiguous, impossible
  or misleading." / "Sort questions about an asset by what can answer them: storage, the data, or only a
  record kept at the time." / "Rebuild an asset from another asset with a query, and say what a match
  does and does not prove."
- **Problem**: The first thing the learner reads names the three outcomes of the failure experiment and
  the three groups of the map, and uses "a match" and "a record kept at the time" before either is
  meaningful. Several objectives ask the learner to "say", "sort" or "show"; no step has the learner do
  any of these in their own words, and the lab does the sorting (see R17 and R19).
- **Severity**: low.
- **Direction**: Phrase each objective as what the learner will do, without the outcome. Check that every
  objective is something the chapter has the learner do.

### R22. Section 2's "assets, not rows" sentence does not fit its own list, and one phrase is filler

- **Where**: Section 2 (Motivation).
- **Quote**: "Wrong answers cost real things: a deleted file that a program still reads, or a dashboard
  that stays wrong for weeks before anybody notices. Each question is about the assets, not the rows
  inside them." The list includes "Is Thursday's figure wrong, and since when?".
- **Problem**: "Is Thursday's figure wrong" is about a value inside daily_sales, so the sentence is untrue
  of its own list. "Real things" is vague (style rules 19, 20 and 22): the sentence goes on to say what is
  at stake, so the phrase adds nothing. Two examples are given for four questions, and they are not
  matched to them.
- **Severity**: low.
- **Direction**: Fix or cut the "not the rows" sentence, drop "real things", and match each example to a
  listed question.

### R23. `updated_by` is a visible counter-example to "no amount of data answers who is answerable"

- **Where**: Section 4, products.parquet; Section 8, first paragraph.
- **Quote**: "The right-hand column holds questions no amount of data answers: who is answerable for each
  asset, what unit a number uses, what changed." The products.parquet rows carry an UPDATED_BY column
  (k.adeyemi, r.novak, s.lund) and the inspector says "Who is responsible for it? Storage records nothing
  that answers this."
- **Problem**: A learner who opens products.parquet sees staff names in the data and will wonder whether
  that answers "who should I ask". The page never mentions the column, and the universal "no amount of
  data" invites the counter-example. (data.ts notes that Chapter 2 is meant to take this up.)
- **Severity**: low.
- **Direction**: Say in one sentence that the column names who last edited a product row, which is not
  who answers for the file, or soften "no amount of data" to what the chapter shows.

### R24. Visible differences between customers.parquet and clean_customers go unused

- **Where**: Section 4 (customers.parquet and clean_customers).
- **Quote**: customers.parquet, "The 10 rows", has a NULL email for customer 108 and
  "SOFIA.MARINO@example.net"; clean_customers, "The 9 rows", has "sofia.marino@example.net" and no row for
  108.
- **Problem**: A learner who opens the customers files, or applies the "compare row counts" task to them, finds
  a dropped row and a changed value and has nowhere to take them. Customer 108 still has orders in clean_orders
  (for example 7012 and 7032 on the page), and clean_customers lacks that customer: an open thread the
  chapter neither uses nor dismisses.
- **Severity**: low.
- **Direction**: Say these are for later, use them as one more thing storage will not explain, or choose
  data that does not raise the question this early.

### R25. "Eight questions" is six for the dashboard

- **Where**: Section 4 intro; the sales_dashboard inspector.
- **Quote**: "...and what storage says about eight questions." The sales_dashboard panel lists six: "When
  was it last written?", "What does it show?", "Who is responsible for it?", "What is it made from?",
  "What reads it?" and "What changed in it this week?"
- **Problem**: The count is wrong for one of the seven assets (the lab asks the dashboard six questions).
  The dashboard also swaps "How are its numbers worked out?" for "What does it show?" and drops "Did last
  night's write work?" and "In what units are its numbers?", although revenue is shown there. Rated
  low because the consequence is small, although it is a count that the figure contradicts.
- **Severity**: low.
- **Direction**: Say "up to eight" or just "the questions", or ask the dashboard the same eight.

### R26. Captions call a matching query "what builds daily_sales"

- **Where**: Section 5, the figure's caption and prompt.
- **Quote**: "Use the query builder to find what builds daily_sales." and "Build a query that makes
  daily_sales from another asset."
- **Problem**: Section 5's prose is careful: a matching query is "a candidate for how it was made". The
  caption and the prompt say the opposite: the query is what builds or makes it. The second objective is
  to say what a match does not prove, and this wording says it proves everything.
- **Severity**: low.
- **Direction**: Use the prose's wording (a query that gives its rows) in the caption and the prompt.

### R27. "The 48 rows" in Challenge 2 is a hidden control that looks like a caption

- **Where**: Section 9, under "RESULT" (phone-dark-build-rules.png; the desktop screenshot).
- **Quote**: "The rules keep 48 rows." followed by "The 48 rows".
- **Problem**: "The 48 rows" is a collapsed disclosure (a details element in ChoiceEditor.tsx) and the
  screenshots show no marker, so it reads as a caption above a table that is not there. The learner
  cannot see which rows their rules keep unless they click text that looks static.
- **Severity**: low.
- **Direction**: Show a marker, or show the rows (a short table with the dropped rows marked).

### R28. The last-write times are a partial timetable that the chapter ignores

- **Where**: Section 1; Section 4.
- **Quote**: "You cannot see anything else yet: not the code, not the timetable, not anybody's notes."
- **Problem**: The inspector's seven last-write times run in the order of the pipeline: 01:00:41,
  01:02:41 and 01:04:41 for the three files, then 02:00:38 clean_customers, 02:05:52 clean_orders,
  02:30:21 daily_sales and 03:00:09 the dashboard. An engineer is likely to use these as evidence of
  order and dependency. The page says the timetable cannot be seen and never says what these times can
  and cannot tell.
- **Severity**: low.
- **Direction**: Add a task that puts the assets in last-write order, with a sentence on what that order
  fits and what it would not tell apart.

### R29. Small inaccuracies and awkward phrasings in the prediction and experiment text

- **Where**: Section 3 (results); Section 6 (outcomes and intro).
- **Quote and problem**:
  - "On each of those days, orders.parquet holds a row that daily_sales does not count." Thursday has
    three such rows.
  - "A new file appears in storage: clean_orders_copy.parquet in bucket shop-scratch, last modified at
    02:15". Every other time on the page reads like "2026-09-14 02:30:21 UTC"; the lab's value is
    02:15:17.
  - "From Saturday's row on, the program keeps every order whose status is not "refunded"" is hard to
    parse, and "The week ran with this change: No change." reads oddly.
  - "It then shows what storage shows differently, your query's rows against the new daily_sales, and
    every query in the builder's choices that rebuilds it." The three items are different shapes and
    "shows ... shows" collides.
  - "Choose an asset to read, which rows to keep, what to add up, and per what." appears word for word in
    the Section 5 prose and in the figure's prompt directly below it.
  - The first prediction's result gives two adjacent paragraphs that both name etl_service as the
    owner (of daily_sales, then of all three tables). Source note: LabPrediction.tsx was edited after this page was generated and no longer prints
    the first of them.
- **Severity**: low.
- **Direction**: Correct each in place.

### R30. "The lab" is used from Section 3 and introduced only in a note at the foot of the page

- **Where**: Section 3 (result lines), Section 7, and the note at the end.
- **Quote**: "You predicted: an account that programs log in as. The lab found: an account that programs log
  in as." / "The lab places each question in one of three columns" / "This figure runs the Metadata Lab,
  a small data platform in your browser."
- **Problem**: A definite article before a noun the chapter has not introduced: "the lab" finds and places
  things four sections before the note says what it is. The note says "This figure" although it follows
  the whole chapter. The page also says "the course" for the same agent ("The course tells you this").
- **Severity**: low.
- **Direction**: Introduce the lab in one sentence where the first figure uses it, and make the note
  about the figures in the plural. Use one name where the page says what knows or tells.

### R31. Smaller sense slips: storage, platform, copy, answer, night

- **Where**: Throughout.
- **Quote and problem**:
  - "storage": "Three files sit in object storage." (one of three systems) against "You can read
    everything the shop's storage holds." and "Storage records nothing that answers this." (all three,
    including the reporting tool). The page never says "storage" now means all three, and a reporting
    tool is not storage in the ordinary sense.
  - "platform": "The platform holds seven assets." (the whole thing) against "Your questions were about
    the platform around the data" and "Records about assets and about the platform" (what is not the
    data).
  - "copy": "copies of the same order" (Challenge 2, duplicate rows) against "an analyst copies
    clean_orders every night" and "the analyst's copy" (a file).
  - "answer": "only a record kept at the time answers it" (supplies information) against "who answers
    for an asset" and "not who answers for it" (is accountable). "Responsible", "answerable" and "owner"
    also name the same idea.
  - The event is named four ways: "last night's write", "the last night's write", "a night's work" and
    "a failed night".
- **Severity**: low.
- **Direction**: Pick one word per idea and keep it. Define "storage" once as the three systems, or say
  "the three systems" where all three are meant.

### R32. Front page and last line

- **Where**: Front page (phone-dark-front.png); end of Chapter 1.
- **Quote**: "You build a small metadata system inside a small data platform that really runs in your
  browser." The contents list has 31 rows reading "Still to be written". Section 8: "starting with the
  first records in the next chapter." Last line of the chapter: "The next chapter is still to be written."
- **Problem**: "Really" is an intensifier (style rule 19) and "small ... small" repeats. The contents are
  31 identical placeholders. The chapter promises "the next chapter" and its last line then says it is
  not written.
- **Severity**: low.
- **Direction**: Cut "really". Collapse the unwritten chapters into one line. Make the promise about the
  course, not the next page, until the next page exists.
