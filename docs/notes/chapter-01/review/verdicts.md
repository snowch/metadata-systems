# Sceptic's verdicts on Chapter 1's review findings

An independent attack on `findings.md` (R1 to R32). Nothing in the repository was changed except this
file. The reviewer's severities are quoted as "reviewer"; mine are "mine".

## How I checked

- **Read:** the sceptic brief, `findings.md`, `page.md`, `docs/notes/chapter-01.md` (the six
  changes), `facts.md`, the six briefs, `docs/style.md`, `docs/plan.md`, `docs/lab.md`,
  `docs/sources.md` and `CLAUDE.md`.
- **The lab:** read `packages/lab/src` and ran probes bundled with esbuild. The scripts and their
  output are in `scratchpad/sceptic/` (`p1.ts`: the question map and storage in all four weeks;
  `p2.ts`: last-write order, customer 108, what each program reads, a day with no orders).
- **The current build:** the site served at localhost:4173 was built at 18:39, after the 18:32 edits
  to the figures and strings. Later commits touch only an originality note, tests and docs, so its
  learner-facing text is the current source's. I drove it with Playwright at 1280 by 900 and at
  375 by 812 with touch: every change run in turn, both challenges failed and passed, every hint
  opened, both predictions committed and re-opened with "Predict again", the Lab badge clicked, layout
  measured and screenshots taken (`scratchpad/sceptic/*.mjs`, `*.png`).
- **The six changes** are numbered as in "The managing session's read": **C1** the record table's
  first column is headed "Field"; **C2** the map's evidence for "What is it made from?" and "How are
  its numbers worked out?" is no longer identical; **C3** two sources are joined with "and"; **C4**
  challenge 2's field labels are capitalised; **C5** the owner prediction no longer prints the owner
  on a line of its own; **C6** the change lab counts a query that reproduces every row the asset has.
- **Severity** is my own. High: the page says something false or self-contradictory about the
  chapter's central claims. Medium: a learner is likely to be confused, or an objective or one of the
  course's binding rules is not met. Low: polish, or a stumble most learners recover from at once.
- **Challenge answers:** none appears below. Where a finding touches a reference I say "the
  reference" and no more.

## At a glance

| ID | Verdict | Reviewer | Mine | Fix |
| --- | --- | --- | --- | --- |
| R1 | Upheld | high | high | wording, and a decision about the model |
| R2 | Already fixed (C6) | high | residual low | wording (residual) |
| R3 | Upheld | high | high | wording, or code |
| R4 | Upheld in part | medium | medium | wording |
| R5 | Upheld in part | medium | low | wording |
| R6 | Upheld in part | medium | low | wording |
| R7 | Upheld in part | medium | low | wording |
| R8 | Upheld in part | medium | low | code (CSS) |
| R9 | Upheld in part | medium | medium | both |
| R10 | Upheld in part | medium | low | wording |
| R11 | Upheld in part | medium | medium | wording |
| R12 | Upheld in part | medium | low | code or wording |
| R13 | Upheld in part | medium | medium | wording and `docs/sources.md` |
| R14 | Upheld | medium | medium | wording |
| R15 | Upheld in part | medium | medium | wording |
| R16 | Upheld in part | medium | low | wording |
| R17 | Upheld | medium | medium | both |
| R18 | Upheld in part | medium | medium | wording |
| R19 | Upheld in part | medium | medium | wording, optionally code |
| R20 | Upheld | medium | medium | wording |
| R21 | Upheld | low | low | wording |
| R22 | Upheld in part | low | low | wording |
| R23 | Upheld | low | low | wording |
| R24 | Rejected | low | none | none |
| R25 | Upheld | low | low | wording |
| R26 | Upheld | low | low | wording |
| R27 | Upheld | low | low | code (CSS) |
| R28 | Upheld in part | low | low | wording |
| R29 | Upheld in part | low | low | wording |
| R30 | Upheld in part | low | low | wording |
| R31 | Upheld in part | low | low | wording |
| R32 | Upheld in part | low | low | wording |

---

## High

### R1. The reporting tool "records nothing about where the values come from", then "keeps the query behind its chart"

**Verdict: Upheld.** Reviewer: high. Mine: high.

**Evidence.**

- Live inspector, `sales_dashboard`: "What does it show? The reporting tool records the title, Sales,
  last 7 days, and nothing about where the values come from." and "What is it made from? Storage
  records nothing that answers this."
- Section 7 (`PROSE.explanation`): "Some of the systems do keep records for their own work that you
  were not shown: the reporting tool keeps the query behind its chart, and something keeps the
  programs and their timetable."
- Section 1 (`PROSE.question`): "You can read everything the shop's storage holds."
- `facts.md` defines storage as "the three systems that hold assets, and what they keep about each".
  By the page's own definition a query kept by the reporting tool is something storage holds, and
  Section 1 says all of it can be read. The three statements cannot all be true.
- The lab does not model a query kept by the reporting tool. `storage.ts` (header comment: "exactly
  the fields its system keeps") gives the reporting tool a title, creator, creation time, last refresh
  and values, and no query. The SQL that fills the dashboard is the program `dashboard_refresh`
  (`programs.ts:59-68`), run as `etl_service`.
- Origin: the sentence is a fact in the managing session's brief D (item 4,
  `briefs/D-explanation-generalisation.md:19`) and in brief G. The lab does not hold it, so it was not
  checked against the lab.

**What holds.** All of it: a contradiction inside one chapter, in the claim the chapter is built on,
and the Section 7 sentence sits in the paragraph that has just said none of the three systems
recorded what made an asset.

**Fix: wording, and one decision.** Either cut the clause and say only that other records exist that
the chapter has not shown, or make the dashboard's inspector line say "not shown" instead of "nothing".
If the course wants the reporting tool to keep a query, the lab has to model it (code).

### R2. Failed night: the list says no query rebuilds `daily_sales`, the paragraph says the learner's query still rebuilds every row

**Verdict: Already fixed by C6.** Reviewer: high. Mine: the contradiction is gone; a residual wording
point is low.

**Evidence.** On the current build, after "the last night's write of daily_sales fails" runs, the list
under "Every query in the builder's choices that rebuilds daily_sales" holds one query, and the
paragraph below says "Your query still rebuilds every row daily_sales has, and gives one more:
Sunday." They agree. `ChangeLab.tsx:125` now calls `sumReconstructions(changed, data.target,
"covers")`, and the facts test pins it (`expect(sumReconstructions(w, "daily_sales",
"covers")).toHaveLength(1)`). The refunds week still lists "No query in the builder's choices
rebuilds it."; the copy week lists two. I did not state the query here.

**Residual (low, wording).** The reviewer is right that "rebuild" now has two meanings. Section 5, and
the challenge's own tests, ask for exactly the same rows. The failed-night list and both maps count a
query that reproduces every row the asset has. The same figure's table still ends "Sun 13 | 97.75 |
no row | No". `facts.md` defines rebuild as "give exactly the same rows" and then uses the second
sense in its own failed-night entry. One clause in the failed-night outcome, or in Section 5's
definition, settles it.

### R3. "From storage, a failed night looks like a night with nothing to write" is not what the lab shows

**Verdict: Upheld.** Reviewer: high. Mine: high.

**Evidence.**

- Live failed-night outcome: "From storage, a failed night looks like a night with nothing to write."
  The closing text adds "a failure made a missing row look like a quiet night." The first line of the
  same figure reads "daily_sales last written at 2026-09-13 02:30:21 UTC, not 2026-09-14 02:30:21 UTC."
- `week.ts:180-187`: the append branch calls `write(...)` with the program's finish time whether or
  not the day gave any rows. I ran the `daily_sales` SQL for a day with no orders: zero rows (`p2.ts`).
  So in the lab a night with nothing to write leaves the same rows and a fresh Monday 02:30 time, and
  a failed night is the only case that leaves the time a day stale. No week in the lab has a quiet
  night (every one of the seven days has orders), so the sentence is not computed.
- The lab's own map does not call the failed week done. `questionMap(week(["failed"]))` returns for
  "worked": `lastWritten 2026-09-13T02:30:21Z, latestRow 2026-09-12, expectedRow 2026-09-13, looksDone
  false` (`questions.ts:119-130`), which the template renders as "Last written at 2026-09-13 02:30:21
  UTC; the latest row is for Sat 12, not Sun 13." (`strings.ts`, `e.nightMissing`). The page never
  shows this map.
- Origin: the sentence is in `facts.md` (change 3) and brief C (item 4). It was not read off the lab.

**What can be defended.** From the rows alone (six rows, no Sunday) and from the dashboard alone
(refreshed Monday 03:00:09, six values) a failed night does look quiet. The inspector's own phrase,
"not whether a write was due", says the true version: storage cannot say whether a write was due. The
sentence overreaches only where it says "from storage" while the figure prints the stale time.

**Fix: wording first.** Say what is indistinguishable (six rows, no Sunday) and let the stale time be
the clue the learner must weigh. Code only if the course wants the claim computed: a week with a quiet
night.

---

## Medium

### R4. The opening question and the four motivating questions are never closed

**Verdict: Upheld in part.** Reviewer: medium. Mine: medium.

**Evidence.** "Thursday" appears in the learner-facing prose only in Sections 1 and 2 (searched the
live page text and the prose files; the other hits are the grader's case label "Thursday 10
September" and the originality note). The reviewer's data claim about Thursday's rows holds
(checked in the lab and in the live inspector). `programs.ts` reads `customers.parquet`,
`orders.parquet`, `clean_orders` and `daily_sales` and nothing else, so no program reads
`products.parquet`.

**What holds.** The frame is dropped without being closed or flagged as open. The four Section 2
questions are never placed against the inspector's eight or Section 7's five. "Can we delete
products.parquet?" has an answer in the shop that the page neither gives nor says it cannot give; the
nearest it comes is "What reads it? Storage records nothing that answers this."

**What does not.**

- "Your questions" in Section 7 is a paraphrase of five of the inspector's eight (what a number
  means, who answers, what made it, what reads it, what changed), and it covers Section 2's four as
  well. "Matches neither set" overstates; "what a number means" alone is loose.
- Chapter 1 is meant to leave Thursday's cause open. `docs/plan.md:214-215`: "Chapter 1 shows the
  symptom, Chapter 13 measures it, Chapter 14 traces it and Chapter 16 finds it." The reviewer did
  not read the plan. So the fix is to say it is open, not to answer it.

**Fix: wording.** A short passage in the Generalisation or the Reflection that returns to Thursday
(what the rows show, what no record shows) and sorts the four Section 2 questions into the three
groups.

### R5. Both predictions in Section 3 can be answered without a real expectation

**Verdict: Upheld in part.** Reviewer: medium. Mine: low.

**Evidence.** Live: the owner prediction's prompt says "The warehouse records an owner for every
table." and offers "no owner at all". The days prediction asks "On how many of the seven days" and
offers "on all seven days", "on some days but not all", "on no day". "Predict again" clears the
commitment and the radios (checked).

**What holds.**

- "No owner at all" is ruled out by the prompt itself.
- "On no day" is a near-dead option.
- "On how many" is answered with a category.

**What does not.**

- "Some but not all is the only live option" is overcalled. "On all seven days" is live for a learner
  who assumes `daily_sales` is a plain sum of the raw orders and that Thursday simply had few sales,
  which is the natural first hypothesis in this chapter. The result table (Thursday at 205.50 raw
  against 51.50) is the surprise.
- "The question presumes that `daily_sales` is built from `orders.parquet`" is wrong. It asks the
  learner to add up the raw file and compare. It claims no build relationship; Section 5 later calls
  one a candidate.
- "Picks it because it is the odd one out" is speculation. The first option is also the one an
  engineer who knows pipelines would pick on merit.
- "Predict again" is the platform primitive's design (`platform/primitives/src/PredictionChallenge.tsx`:
  "Predict, commit, see, and predict again: the controls every prediction figure shares";
  `onAgain` is a required prop). Changing it belongs in the platform repository.

**Fix: wording.** Drop "no owner at all" or take "for every table" out of the prompt. Consider asking
which days differ.

### R6. The page says both that the course tells you `etl_service` is an account and that storage records an account

**Verdict: Upheld in part.** Reviewer: medium. Mine: low.

**Evidence.** `PROSE.p1Explain` (`prose.ts:19`): "So the owner field says which login created the
table, not which person or team answers for it." The lab records an owning account and no creator
for a table (`storage.ts:89-95`; `ASSETS` holds a created time only). `facts.md` says the warehouse
"names etl_service as the owner of all three tables". The creator claim came in with brief A (item 3,
`briefs/A-question-prediction.md:71`), not from the fact sheet.

**What holds.** "Which login created the table" is unsupported by the lab. It is the premise of the
explanation's contrast, so it should say what the lab records: which account owns the table.

**What does not.** The contradiction is mostly a nit. "The warehouse records the account etl_service,
not a person or a team" and "Storage names etl_service, an account, ..." are the course's narration of
a field whose value is the name `etl_service`, written after the learner has been told what the name
is. A cheap tightening ("records the name etl_service") removes the doubt. In the same figure, "The lab
found: an account..." and "The course tells you this" name two different agents for one piece of
knowledge (see R30).

**Fix: wording.**

### R7. The Investigation hands the learner the discoveries and the absences

**Verdict: Upheld in part.** Reviewer: medium. Mine: low.

**Evidence.** `PROSE.p2Explain`: "You will find those rows in the next section." The inspector's
"Things to try" name the three anomalies. `inspectorAfter` is the figure's after-text, so it shows
from load, and it names "why some orders in orders.parquet are missing from clean_orders". For
`orders.parquet` four of the eight inspector lines read "Storage records nothing that answers this."
(counted live).

**What holds.** After a prediction result that says rows are not counted, the page walks the learner
to the three anomalies, and the closing note then restates the point.

**What does not.** The scaffold is deliberate. Forty-eight rows are a haystack, and the first
objective is what storage does not record, which the learner still has to see. "The absences are
pre-written" describes the figure's job: it shows what storage says per question, and for most
questions that is nothing. A predict-then-reveal step per question would improve it; it is not a
repair.

**Fix: wording.** One open task tied to the mismatch table; trim what the closing note repeats.

### R8. At phone width the Investigation hides the columns its tasks need

**Verdict: Upheld in part.** Reviewer: medium. Mine: low.

**Evidence (375 px, touch).**

- The rows region has `scrollWidth` 738 and `clientWidth` 307. The third column ends at 345 px
  against the region's edge at 341 px, so the table looks complete at three columns. `.data-scroll`
  has no mask, shadow or background cue (`figures.css:22-28`). The hidden columns are `quantity`,
  `price`, `status` and `ordered_at`; the tasks need the last two.
- The SQL `pre` has `scrollWidth` 526 against 307; it scrolls inside its box by design
  (`figures.css:3-4`).
- The questions block starts about 2,147 px below the top of the figure at 1280 px (the rows region
  is about 1,500 px tall) and about 2,642 px below it at 375 px.
- Screenshots show timestamps breaking at the hyphen: "at 2026-" then "09-14 01:00:41 UTC.", twice.

**What holds.** No scroll cue; two of the five tasks need hidden columns; the questions sit far below
the table at both widths; the hyphen break.

**What does not.** "A phone learner cannot complete two of the five tasks" is too strong. The
"Columns and types" table directly above lists all seven columns, and a clipped table inside a
bordered region is a pattern phone users swipe. The managing session already lists the sideways
scroll as a known gap. The SQL clip is the designed behaviour.

**Fix: code (CSS and markup).** A visible scroll cue, no break inside timestamps, and either the
questions before the rows or a capped rows region.

### R9. The failure experiment asks for predictions it cannot collect, and its heading answers the first

**Verdict: Upheld in part.** Reviewer: medium. Mine: medium.

**Evidence.** `PROSE.changeLead` (`prose.ts:41`): "Before you run each change, make a prediction.
Will storage show the change? Will your query still rebuild daily_sales?" The figure is a radio group
with "No change" preselected and a "Run the week again" button (`ChangeLab.tsx`); nothing records or
compares an expectation (checked live: pressing the button on the default runs the week). Section 3
commits predictions; the course's rule is "a prediction commits the learner to an expectation about
the lab that the lab then answers" (`CLAUDE.md`).

**What holds.**

- The instruction cannot be collected.
- The title "Three changes storage does not record" (`labels.ts:20`) answers the first question
  before it is asked.
- The first question is ambiguous. The figure's own heading is "What storage shows differently" and
  lists differences for every change, while the title and the closing note say storage does not
  record them.
- The second question is yes, no, yes-ish. It does not aim at what the copy teaches, which is how
  many queries now fit.

**What does not (fully).** That the refunds label names a reason and not an effect is part of what
makes Saturday's change a surprise. It does mean the learner cannot predict from the label.

**Fix: both.** Either a committed prediction per change (code) aimed at how many queries fit and what
storage records, with a title that does not answer it (wording); or, more cheaply, drop the
instruction and the two questions.

### R10. "What storage shows differently" is a comparison only the lab can make

**Verdict: Upheld in part.** Reviewer: medium. Mine: low.

**Evidence.** `ChangeLab.tsx:117` calls `storageDifferences(week(), changed, strings)`, comparing the
plain week with the changed one. `strings.ts`: `changedValue` "In {asset}, the row for {day} reads
{after}, not {before}."; `changedTime` "{asset} last written at {after}, not {before}." Live: "In
daily_sales, the row for Sat 12 reads 215.49, not 191.49." In the changed week, storage holds only
215.49; 191.49 is from the lab's other run.

**What holds.** The "not X" half is a two-world comparison that storage in the changed week cannot
give, the page does not say so, and the map says "Storage keeps only the current rows."

**What does not.** The lead says the figure "will run the whole week again from Monday, with that
change in place. It then shows what storage shows differently", and 191.49 is already on the page in
Section 1, so "differently" reads as against the first run. That a learner "can reasonably conclude
that storage did reveal the change" is weak.

**Better point, not the reviewer's.** The closing line "None of the three changes left anything in
storage that says what happened" is too broad. The copy leaves a new file called
`clean_orders_copy.parquet` in a bucket called `shop-scratch`, last modified at 02:15. The failed
night leaves a stale last-altered time. What none leaves is a record of the change itself, who made
it or why. That is the part to act on.

**Fix: wording.** Label the "not X" values as the lab's comparison with the first week; narrow the
closing line.

### R11. "Impossible" claims more than the lab shows, and the caveat is at the foot of the page

**Verdict: Upheld in part.** Reviewer: medium. Mine: medium.

**Evidence.**

- `PROSE.afterAll` (`prose.ts:49`): "an edit made it impossible". `PROSE.generalisation`
  (`prose.ts:57`): "The middle column holds answers the data suggests. They can be ambiguous,
  impossible or misleading." Objective 3 says the same.
- `week.ts:176`: the refunds edit applies only to days from Saturday on. A query with a date
  condition would reproduce the table, and the builder offers none.
- The change lab's own line is careful: "No query in the builder's choices rebuilds it." The model
  note ends: "'No query rebuilds it' means none of those choices." The summary lines carry no
  qualifier.
- I ran the refunds week through the map: "What is it made from?" and "How are its numbers worked
  out?" move to the right-hand group (`questions.ts:106-113`); the middle group keeps "What reads it?"
  and "Did last night's write work?". `facts.md` says so too ("it moves to the right-hand column").
  So the Section 8 sentence describes an impossible answer sitting in the middle group, a state the
  lab's map never has: an impossible answer is one that has left it.

**What holds.** Both points: the unqualified "impossible" in three places, and the Section 8
sentence's mismatch with the map.

**What does not.** The figure itself carries the qualifier beside its own claim, so the overclaim is
in the summaries only.

**Fix: wording.** "No query the builder offers rebuilds it" where the claim is made; recast Section 8
so that "impossible" means a question leaving the middle group.

### R12. The construction challenge's solution is printed in later figures for a learner who has not passed it

**Verdict: Upheld in part.** Reviewer: medium. Mine: low.

**Evidence.** Live, with nothing passed: the change lab says "You have not built a passing query yet,
so this uses the course's." and its list prints the reference's asset, rows, measure and grouping. The
Section 7 map prints it unconditionally, because `QuestionMap.tsx:90` uses the lab's search, not the
learner's work. The failure experiment's lead says so openly: "...and the course's query if it does
not." The fifth hint of each challenge is headed "THE ANSWER" and gives the answer when opened.

**What holds.** A stuck learner who scrolls on reads the solution with no test.

**What does not.** It duplicates what the fifth hint offers on demand. No completion is bypassed: the
challenge's grade still needs the tests run on the learner's own choices. "The course's query" is not
an undefined noun; the lead and the figure's note both say what it is.

**Fix: code or wording.** For an unsolved learner show the count ("one query fits") without its
settings, or accept the leak and say so.

### R13. Section 7 explains what systems record as if by necessity; the lab and the page's own note do not bear it out

**Verdict: Upheld in part.** Reviewer: medium. Mine: medium.

**Evidence.**

- `PROSE.explanation` (`prose.ts:51`): "Each system records only what it needs for its own work. The
  warehouse must know the columns and types to run a query, and the owning account to control who may
  read."
- The lab simply chooses the fields: `storage.ts` header ("exactly the fields its system keeps");
  `docs/lab.md:30` ("These records are the lab's choice of what a typical system of each kind keeps").
  The reporting tool records "Created by j.marsh" (`storage.ts:96-102`), which a chart does not need.
- The note (`prose.ts:75`): "Some warehouses record no owner and no last-altered time. Some object
  stores keep every version of a file, and logs of who read it."
- `docs/sources.md` has no entry for warehouses or object stores (searched for owner, version, access
  log, last altered). `docs/lab.md` repeats the claims, also without a source.

**What holds.**

- A design choice is stated as a necessity. `CLAUDE.md`: "The lab's own choices are labelled as the
  lab's."
- The note's own claim (some warehouses record no owner) cuts against "must know the owning account".
- The two real-system claims have no source entry, and `CLAUDE.md` makes that binding: "record the
  source in `docs/sources.md` ... Memory is not a source."

**What does not.** The principle (a system keeps what it needs to function) is a fair teaching
simplification. The access-control point is a plausible simplification, not an error. The note's
claims are probably true; they are unsourced.

**Fix: wording and `docs/sources.md`.** Present the rationale as the lab's design and soften "only"
and "must". Source the two claims or cut them.

### R14. Sentences a competent engineer must read twice

**Verdict: Upheld.** Reviewer: medium. Mine: medium (right for the first two sentences, low for the
others).

**Evidence.** Word counts (checked): the map lead (`prose.ts:53`) 40, "A platform needs three kinds"
(`prose.ts:57`) 37, "Some of the systems do keep records" (`prose.ts:51`) 33, "The lab finds each
place..." 19. The first three are a colon followed by a list of clauses (style rule 1), and the first
two carry the chapter's main distinction. "Running storage" is not something one does, and "not from a
list" points at a list the learner was never told about. The long sentences are the briefs' fact
sentences copied (brief D: the map lead's item 1, the explanation's item 4 and the
generalisation's item 4), which `CLAUDE.md` predicts: "A prose brief gets its wording
copied."

**Fix: wording.** Send the facts back as lists; name the three groups by their headings; say what the
lab does ("reads storage, then tries every query the builder offers").

### R15. The middle group's stated rule does not fit all its questions, and two of its cells repeat each other

**Verdict: Upheld in part.** Reviewer: medium. Mine: medium.

**(a) Holds.** `questions.ts:119-130` always places "worked" in the middle group, with the last-written
time and the latest row as evidence. The rule in `PROSE.mapLead` names only "a query rebuilds the
asset or another asset shows the same numbers". The question left out is the one the failed-night
experiment targets.

**(b) Already fixed by C2 (and C3).** Live: "What is it made from?" now reads "One asset rebuilds it:
..." and "How are its numbers worked out?" names the query. The copy map reads "2 assets rebuild it
equally well: clean_orders and clean_orders_copy.parquet."

**(c) Holds.** `strings.ts` `a.columns` is "Storage records {count} column names and their types, not
what they mean." (`questions.ts` `storageAnswer`, case "computed"). It is the answer to "How are its
numbers worked out?", and it is about meaning. Types belong with the units question.

**Fix: wording.** Restate the middle group's rule to cover time-and-row evidence. For (c), change the
text, or change `storageAnswer` in the lab.

### R16. "Column" means two things, and "middle column" and "right-hand column" are false at phone width

**Verdict: Upheld in part.** Reviewer: medium. Mine: low.

**Evidence.** `figures.css:329-338`: the three groups sit side by side only from 52rem. At 375 px they
stack (tops at 12439, 12574 and 12975). Sections 7 and 8 say "the middle column" and "the right-hand
column". Section 4 says "7 column names". C1 renamed the record table's first column from "Column" to
"Field", which removes one clash but not this one.

**What holds.** Both claims: positional words that do not exist on a phone, and "column" in two
senses.

**What does not.** Medium. The boxes carry their headings and keep the order, and the two senses are
sections apart. The reader recovers at once.

**Fix: wording.** Refer to the groups by their headings.

### R17. The learner never sorts a question, and the map never moves in front of them

**Verdict: Upheld.** Reviewer: medium. Mine: medium.

**Evidence.** `QuestionMap.tsx` has no state and no controls; live, neither map has any control but
the model badge. `invisible-system.ts:155-180`: the first map runs the plain week, the second
`changes: ["copy"]`, whatever the learner did in Section 6. Objective 4 ("Sort questions about an
asset...") is never asked of the learner. The refunds week, where a question leaves the middle group,
is never shown (R11), nor is the failed week, where the lab's "worked" line changes (R3). The Section 8
lead says where to look before the figure shows it. The copy result is stated in `outcomeCopy`, in the
Section 8 caption and figure, and in `map2After`.

**Fix: both.** Code: a control, or a prediction on the contested questions, and a map tied to the
weeks the learner ran. Wording: the objective and the "look at" instruction.

### R18. "Metadata" arrives as a told definition; "three kinds" is asserted, not derived; "record" now means two things

**Verdict: Upheld in part.** Reviewer: medium. Mine: medium.

**(a) Mostly does not hold.** The term follows the questions the learner could not answer, with plain
English first and the term second, as `CLAUDE.md` prescribes. What does hold: "three kinds" is stated
without a link to the eight questions, and the page does not relate its two threes (three groups,
three kinds). They do not line up: "Did last night's write work?" (whether programs worked) sits in
the middle group; "What changed in it this week?" (arguably "what happened") sits in the right-hand
group.

**(b) Holds, and is the part to act on.** The definition ("Records about assets and about the
platform, written down and kept separate from the data itself") covers what storage already keeps
(owner, last altered, sizes, types). The page does not say whether those count or what is missing, so
the learner cannot tell whether metadata means everything storage keeps or only what it lacks.

**(c) Does not hold.** "Record" is one sense, something written down. Storage records a field; a
record kept at the time is a note written then. `facts.md` defines the noun and the verb is the same
idea.

**Fix: wording.** Derive the kinds from the unanswered questions, and say that storage's own fields
are a part of the first kind and why they are not the subject.

### R19. Challenge 2 has no stated purpose, can be solved by matching a number, and its lesson is told afterwards

**Verdict: Upheld in part.** Reviewer: medium. Mine: medium.

**Evidence.** Section 9's only prose is `c2Lead` (`prose.ts:72`): "The rules appear as SQL below the
choices, with the number of rows they keep." On a pass the page shows only "All 2 tests passed"
(checked live); nothing prompts the learner to probe the controls afterwards. The Reflection
(`prose.ts:73`) delivers the challenge's lesson as a statement. The fifth hint also gives it away when
opened. The figure prints a row count (`strings.ts` `keptRows`) and the Investigation gives
`clean_orders`' row count, so a count can steer. The grader, however, compares rows as multisets
(`grade.ts`), so a count alone does not pass.

**What holds.** The section has no stated purpose. The second challenge's surprise reaches the
learner as text, not as something they did. The Reflection's claim about "your tests" is an
experience only if the learner happened to probe.

**What does not.** The heading "Recovering the rules" is not a false promise: that one rule cannot be
recovered is the design, and the heading is the task. The count shortcut is minor.

**Fix: wording, optionally code.** A lead that gives the section a purpose; an after-text that prompts
the learner to change each control and run again; optionally a prediction before the run.

### R20. The same conclusion is stated five times

**Verdict: Upheld.** Reviewer: medium. Mine: medium.

**Evidence.** The three-part conclusion is in objective 3 (`labels.ts:11`), `afterAll` (`prose.ts:49`),
`mapAfter` (`prose.ts:55`), `generalisation` paragraph 2 (`prose.ts:57`) and the Reflection's first
paragraph (`prose.ts:73`): "The data suggested where daily_sales comes from, until a copy, an edit or
a failed night." The objective is a preview, so strictly four statements in the body and one preview.
The copy result appears in `outcomeCopy`, the Section 8 caption (`labels.ts:38`) and `map2After`. The
Reflection's first sentence ("Storage gave you names, types, row counts, sizes, times and one
account.") nearly repeats `inspectorAfter`. `CLAUDE.md` names "the same argument made twice, far
apart" as something no check catches.

**Fix: wording.** State the three-part point once, where the learner has just seen it. Cut `map2After`
or the Section 8 caption. Let the Reflection add something.

---

## Low

### R21. The objectives announce the chapter's findings in terms the learner has not met

**Verdict: Upheld.** Reviewer: low. Mine: low.

**Evidence.** `labels.ts:9-12`. Objective 3 states the failure experiment's three outcomes before it
runs; objectives 2 and 4 use "a match" and "a record kept at the time" before either means anything;
"say" and "sort" are never asked of the learner (R17, R19).

**Fix: wording.** Phrase each as what the learner does, without the outcome.

### R22. Section 2's "assets, not rows" sentence does not fit its own list, and one phrase is filler

**Verdict: Upheld in part.** Reviewer: low. Mine: low.

**Evidence.** `PROSE.motivation` (`prose.ts:13`): "Wrong answers cost real things: ... Each question is
about the assets, not the rows inside them." The list's third item, "Is Thursday's figure wrong, and
since when?", is about a value inside `daily_sales` or the dashboard. "Real things" is vague (style
rules 20 and 22).

**What does not hold.** "Not matched to the questions": the two examples do match two of the four (a
deleted file to the delete question, a dashboard wrong for weeks to the Thursday question).

**Fix: wording.**

### R23. `updated_by` is a visible counter-example to "no amount of data answers who is answerable"

**Verdict: Upheld.** Reviewer: low. Mine: low.

**Evidence.** Live: `products.parquet` has the columns PRODUCT_ID, NAME, CATEGORY, LIST_PRICE,
UPDATED_BY, with staff names, and the inspector says "Who is responsible for it? Storage records
nothing that answers this." Section 8: "The right-hand column holds questions no amount of data
answers: who is answerable for each asset...". `data.ts:41-42` says the column is "data about the
product, not a record about the file (Chapter 2 asks which it is)", so the author knows. This
chapter's learner meets a loose thread that the universal "no amount of data" invites.

**Fix: wording.** One sentence on the column, or soften "no amount of data" to what the chapter shows.

### R24. Visible differences between `customers.parquet` and `clean_customers` go unused

**Verdict: Rejected.**

**Evidence.** The data claims hold (checked live and in the lab): 10 rows against 9; customer 108 has
no email and no row in `clean_customers`; 108 still has orders in `clean_orders` (7012, 7032, 7044);
customer 103's email is lower-cased. But this is not a defect. The chapter's claim is that storage does
not say why two assets differ. The customers files are one more instance, and nothing on the page says
otherwise or promises to explain them. A learner who guesses "the missing email" is doing, for
customers, what the last challenge asks for orders. The shop's data is hand-written with many properties for later
chapters (`data.ts` header; `docs/lab.md`, "The week"). The reviewer's own direction ("one more thing
storage will not explain") is an optional enhancement, not a repair.

### R25. "Eight questions" is six for the dashboard

**Verdict: Upheld.** Reviewer: low. Mine: low.

**Evidence.** `questions.ts:156-160`: `questionsFor` returns six questions for a dashboard. Counted
live: 8, 8, 8, 8, 8, 8 and 6. `PROSE.inspectorLead` says "about eight questions". The dashboard also
swaps one question's wording ("What does it show?") and has no "Did last night's write work?" or "In
what units". No test pins the count (searched the tests), although `CLAUDE.md` asks that every number
in a learner-facing string be pinned.

**Fix: wording ("up to eight") or code (ask the dashboard the same questions).**

### R26. Captions call a matching query "what builds `daily_sales`"

**Verdict: Upheld.** Reviewer: low. Mine: low.

**Evidence.** `labels.ts:35`: "Use the query builder to find what builds daily_sales." `prose.ts:31`:
"Build a query that makes `daily_sales` from another asset." Against `prose.ts:29`: "that query is a
candidate for how it was made." The caption and prompt state what the prose has just refused to claim,
in a chapter whose second objective is what a match does not prove.

**Fix: wording.**

### R27. "The 48 rows" in Challenge 2 is a hidden control that looks like a caption

**Verdict: Upheld.** Reviewer: low. Mine: low.

**Evidence.** `ChoiceEditor.tsx:72` wraps the rows in `details`; `figures.css:292-297` sets `details >
summary { display: flex; ... }`, which removes the browser's marker. Screenshots at 1280 and 375 show
"The 48 rows" as plain text under "The rules keep 48 rows."; clicking it opens a 48-row table (checked).

**Fix: code (CSS).** Restore a marker, or show a short table.

### R28. The last-write times are a partial timetable that the chapter ignores

**Verdict: Upheld in part.** Reviewer: low. Mine: low.

**Evidence.** The seven last-write times (probe `p2.ts`): 01:00:41 `orders.parquet`, 01:02:41
`customers.parquet`, 01:04:41 `products.parquet`, 02:00:38 `clean_customers`, 02:05:52 `clean_orders`,
02:30:21 `daily_sales`, 03:00:09 `sales_dashboard`. Section 1: "You cannot see anything else yet: not the
code, not the timetable, not anybody's notes."

**What holds.** An engineer will read these as an order of writes, so "not the timetable" overstates
what is hidden. What is hidden is when each write is due.

**What does not.** No new task is needed. The order of writes is an instance of "the data suggests":
it fits a chain, and it can also suggest orderings that are not dependencies. That is useful but
optional.

**Fix: wording.** Adjust "not the timetable"; optionally add a task.

### R29. Small inaccuracies and awkward phrasings in the prediction and experiment text

**Verdict: Upheld in part.** Reviewer: low. Mine: low.

- "Holds a row that daily_sales does not count" while Thursday has three: imprecise, not false ("a
  row" reads as at least one). Weak.
- "Last modified at 02:15" against the lab's 02:15:17: the fact sheet's own rule for prose is
  "Monday 14 September, 02:30", and the facts test pins "02:15". The mix of prose minutes and figure
  seconds is the fact sheet's choice. Weak.
- "The week ran with this change: No change." reads oddly (live). Holds. "From Saturday's row on, the
  program keeps every order whose status is not "refunded"" is clumsy. Holds.
- `changeLead`'s list of three items with "shows ... shows" (`prose.ts:41`). Holds.
- "Choose an asset to read, which rows to keep, what to add up, and per what." appears word for word
  in `PROSE.construction` and in `c1Task` directly below (`prose.ts:29-31`). Holds.
- Two adjacent paragraphs both naming `etl_service`: **already fixed by C5** (live: after committing
  the owner prediction, only the explanation names it).

**Fix: wording.**

### R30. "The lab" is used from Section 3 and introduced only in a note at the foot of the page

**Verdict: Upheld in part.** Reviewer: low. Mine: low.

**Evidence.** Every figure that runs the lab has a "LAB" badge that is a button
(`platform/lesson-runtime/src/LessonView.tsx:100-112`). Clicking the one on the first figure opens the
note in place ("This figure runs the Metadata Lab, a small data platform in your browser. ..."; checked
live, the note becomes visible). `page.md` is a text dump and shows only the copy at the foot, "How the
figures run", so "introduced only in a note at the foot" is partly a misreading of the platform.

**What holds.** The prose says "The lab found:" in Section 3 before saying what the lab is; the badge
is small and opt-in. "The lab found" and "The course tells you this" name two agents in one figure. The
foot note says "This figure" under the heading "How the figures run".

**Fix: wording.** One sentence where the first lab figure is used; one name for the agent that knows.

### R31. Smaller sense slips: storage, platform, copy, answer, night

**Verdict: Upheld in part.** Reviewer: low. Mine: low.

- **storage.** `facts.md` defines it as the three systems, and the figure's heading "Assets in
  storage" holds all three groups, so the sense is set. "Object storage" in Section 1 is a kind of
  system. Real but small.
- **platform.** "The platform holds seven assets" against "the platform around the data". Holds.
- **copy.** "Copies of the same order" (a challenge-2 field) against "the analyst's copy". Holds.
- **answer.** The third map group is headed "Only a record kept at the time answers it" and its first
  line reads "Storage names etl_service, an account, not who answers for it." (live). A pun in one
  figure. "Responsible", "answerable", "answers for" and "owner" name one idea. Holds.
- **night.** "Last night's write" (`labels.ts:79`, the question), "a night's work" (`prose.ts:55`), "a
  failed night" and "a failure" name one event. Holds.

**Fix: wording.** One word per idea.

### R32. Front page and last line

**Verdict: Upheld in part.** Reviewer: low. Mine: low.

**Evidence.** `apps/course/src/strings.ts:9` ("...a small data platform that really runs in your
browser."), `:23` ("Still to be written"), `:29` ("The next chapter is still to be written"). The
front page is outside the chapter's own text.

**What holds.** "Really" is an intensifier (style rule 19). The Reflection has the same word ("The
program the shop really runs"). Section 8's promise of "the next chapter" meets a last line that says
there is none.

**What does not.** The placeholders show the plan's shape while the course is built, and "still to be
written" is the true state. The last line goes when Chapter 2 exists (`docs/plan.md`: the site's
chapter list "shows which chapters exist, worked out from the lessons themselves"). "Small ...
small" is trivial.

**Fix: wording** in `strings.ts` and the Reflection; nothing for the placeholders.

---

## Clusters that share one fix

- **The map's wording:** R14, R15(a), R16, and the "look at" line in R17.
- **The failure experiment's framing:** R3, R9, R10, R11.
- **Repetition:** R20, with R4's missing close in the same two sections.
- **What systems record, and why:** R1, R13.
- **Phone layout:** R8, R27.
- **Small wording:** R21, R22, R25, R26, R29, R30, R31, R32.

## Two process notes

- R3's sentence is in `facts.md` and brief C (item 4). R6's "created the table" is in brief A (item 3)
  and not in `facts.md`. Both came from the managing session's own lists, not from Haiku, and the lab
  supports neither. `CLAUDE.md` asks that each fact be checked against the lab before a brief goes
  out.
- R1's Section 7 sentence entered the same way (brief D item 4).

## Count of verdicts by kind

| Kind | Count | IDs |
| --- | --- | --- |
| Upheld | 10 | R1, R3, R14, R17, R20, R21, R23, R25, R26, R27 |
| Upheld in part | 20 | R4, R5, R6, R7, R8, R9, R10, R11, R12, R13, R15, R16, R18, R19, R22, R28, R29, R30, R31, R32 |
| Already fixed | 1 | R2 (C6); parts of R15 (C2, C3) and R29 (C5) also fixed |
| Rejected | 1 | R24 |
| Total | 32 | |

By my severity, of the findings upheld in whole or in part: high R1, R3; medium R4, R9, R11, R13,
R14, R15, R17, R18, R19, R20; the rest are low.
