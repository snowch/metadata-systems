# Chapter 29: OpenLineage in practice

A working note. Written on 13 October 2026 with Chapters 30 to 32 (`notebook/chapter_29.py`). It
opens Part VII (`docs/notes/part-7/design.md`).

## What the chapter does

Over the week with the returns desk, the reader:

- reads the names Airflow's OpenLineage provider (2.20.3) would give the shop's four nightly jobs as
  tasks of a Dag `shop_nightly` (`default/shop_nightly.build_daily_sales`), and the provider's form of
  one `START`, which passes Chapter 8's check;
- predicts the state Marquez's rules hold for the run early on Friday 11, whose `START` arrived
  after its `COMPLETE`, once all the events have arrived; finds `RUNNING`, against the collector's
  `COMPLETE`; reads Thursday's retry (end moved to 02:30:52; 3 event rows) and Saturday's repeat (3
  rows against 2); 70 events stored against 68;
- changes `order` from `"arrival"` to `"event time"`; Friday's run agrees, Thursday's end does not;
- questions "Use the reference consumer."

## What was built for it

`notebook/shop/consumers.py`: `provider`, `provider_event`, `MarquezRules`, `compare`, `totals`,
`check`, with the order as the reader's piece (`STUBS`, `REFERENCE`). Every rule is cited in
`docs/sources.md`, "Read for Part VII".

## Figures

### `platform-with-returns`

- **Role:** reference
- **Serves:** the standing map. **Why now:** every chapter opens with it.

### `provider-names` and `provider-event`

- **Role:** inspect
- **Serves:** what would a real producer call the shop's jobs? The four names, and one event with
  the provider's facets, checked by Chapter 8's check.
- **Why now:** the names show that adopting a producer renames the jobs; the event shows the real
  facets the chapter's title promises.

### `reference-consumer`

- **Role:** experiment
- **Objective:** the reader discovers that the reference implementation applies events in the order
  it takes them, so a late `START` leaves a finished run `RUNNING`, where their collector compared
  times.
- **Known before:** Chapter 20's late events; Chapter 25's collector and faults.
- **Driving question:** once all the events have arrived, which state do Marquez's rules give
  Friday 11's run?
- **The action:** write the prediction; read the comparison and the totals.
- **Why the action:** the rules are listed above the prediction; the reader applies them to the
  arrival order they know from Chapter 25.
- **Evidence:** `RUNNING` against `COMPLETE`; Thursday's end 02:30:52 against 02:30:21; 3 rows
  against 2; 70 events against 68.
- **Consequence:** "the reference" does not mean the reader's own rules; a consumer's results depend
  on the order it takes events in.
- **Predictable:** yes, from the rule "in the order it takes them" and the arrival time given.
- **Gives nothing away:** the rules are stated; the outcome for Friday is not.
- **Not knowing:** fair; the result says what settled it.
- **Next question:** would sorting the events first make them agree?

### `order`

- **Role:** experiment (completes `reference-consumer`)
- **Evidence:** with `"event time"`, Friday's run is `COMPLETED`; Thursday's end stays 02:30:52 and
  Saturday's rows stay 3: ordering and deduplication are two separate steps.

## Requirements

"Use the reference consumer." (the plan's). Readings: use Marquez, the project's named reference
implementation; use a consumer that does what the specification requires of a consumer (it needs
consumer rules the specification does not have, so it cannot choose between the two); check one's
own consumer against the reference (it needs a rule for which is right where they differ; the
specification says nothing of a late `START`). The figure that questions it is the free-text
cell after the box.

## Originality

The obvious examples are the OpenLineage and Marquez documentation's quickstarts: a sample job
posting events to a local Marquez and a lineage view. This chapter posts nothing anywhere: it
applies Marquez's rules, as its code states them, to the shop's own week with Part V's faults,
beside the reader's own collector, and the provider's names are applied to the shop's jobs. No name
or event from either project's documentation is used.

## What the prose process caught

The review's revision: briefs `part-7/briefs/rev-common.md` and `P29-rev.md`, draft
`part-7/drafts/P29-rev.md`. Every fact landed; nothing added. The draft's "Three questions:" kept.

Brief P29 (`part-7/briefs/`), draft `part-7/drafts/P29.md`. Fixed with the fewest words, as
placement edits (`place_p7.py`): a "The question:" label at the head of two of the reader's cells in
Chapters 31 and 32; a fragment introducing Chapter 31's list of rules; "sets" for "holds" of a cell in
Chapter 29; and Chapter 30's first mention of the provider, which now names it and Chapter 29. In
Chapter 32 the draft put "the forecast" for "a trained model", following the brief's rule on "model";
kept.

## The review

A reviewer on another model read the chapter as built (`chapter-29/review/findings.md`); an
independent sceptic attacked each of the 25 findings (`chapter-29/review/verdicts.md`): 11 upheld, 8
partly, 6 rejected. Read whole again after the fixes (`chapter-29/review/chapter_29-after-review.md`).
Acted on:

- the readings' claims about the specification are scoped to what a consumer does, and each reading
  says what it needs; the reality note says what the specification asks of a producer;
- the printed event is called the shop's event with the provider's names, `producer`, `parent` and
  `jobType`; the lost `sourceCodeLocation` facet is listed; a real task's extra facets and the Dag's
  own job are in the reality note; the datasets are the shop's assumption;
- the provider's version (read from main, only a release candidate tagged) and Marquez's commit are
  named;
- the state mapping is complete (`ABORT`, and the specification's `RUNNING` and `OTHER`);
- the prediction asks for the state once all events have arrived, and names the cells that answer;
- "retry" (Thursday) and "repeat" (Saturday) are kept apart; "stored" throughout; the compare
  table names each run's job and labels its end columns by consumer;
- Dag and provider are glossed at first use; "The page could not show Marquez…" is cut; Marquez's
  missing uniqueness rule is said plainly; the documents' negative is scoped to those read.

Rejected, with the sceptic: restating what the check does not test, redesigning the prediction, the
run-id disclosure's place, and Chapter 8's wording of Marquez.

## Measured

Locally, 13 October 2026, after the review's changes (`docs/notes/notebook-prototype.md`, "Chapters
29 to 32"): from Chapter 28's link, 11 files, 0.32 MB, in a new tab; Run all 8.9 to 9.5 s; peak memory
391 to 399 MB alone, 609 MB with Chapter 28 open; no error output, no console error. The browser
test (`notebook/jupyterlite/smoke.mjs`) types the reference into the chapter's cell and reads the
check.

Live, 13 October 2026, published at `c12c414`, opened alone at desktop and phone widths: Run all
11.2 to 11.4 s; peak memory 398 to 404 MB; no error output, no console error. The warning's 9 to 12 seconds and
about 400 MB hold.

## Known gaps

- The answer cells print below each prediction once **Run all** has run, as the course's
  convention has it; raised with the author at checkpoint 5.
