# VERDICTS ON THE CHAPTER 29 FINDINGS

11 upheld, 8 partly upheld, 6 rejected (25 findings).

What I ran or read: `shop.consumers.compare` and `check` with `"arrival"`, `"event time"` and the wrong value `"event"`; `provider_event` and `openlineage.check`; the shop's own Friday START (`week_events`); `git ls-remote --tags https://github.com/apache/airflow 'providers-openlineage/*'`. I read `consumers.py`, `chapter_29.py`, the as-built file, `docs/notes/chapter-29.md`, `docs/notes/part-7/research/chapter-29.md`, `docs/sources.md` (Part I, Part V, Part VII, Marquez), `docs/authoring.md` (the "output answers only after the learner runs it" rule), and Chapters 8, 25 and 30. The prediction-cell convention is honoured on the page: both [WRITE] cells sit above the cells that answer them.

## BLOCKING

**B1. PARTLY UPHELD.**
- The finding is right that the requirement bullets overreach. "The OpenLineage specification says nothing about repeats, late events or order" is not scoped to consumers. `sources.md` Part I records "required to issue 1 START event and 1 of [COMPLETE, ABORT, FAIL] per run" and the run-cycle line that nothing follows a terminal event. Those are rules on what a producer sends.
- "So Marquez's rules and your collector both meet it" is vacuous. With no consumer rule on these cases, the specification cannot be met or missed on them.
- The last bullet in "How this differs" is already scoped to consumers. Chapter 25's closing note is scoped the same way.
- What does not stand: the chapter need not restate the schema versus run-cycle disagreement. Chapter 8 (line 456) carries it, and Chapter 29's cells do not turn on it.
- Fix: scope both reading bullets to "what a consumer does with". Reading 2 should say what it needs, which is consumer rules in the specification, and that for these cases it has none, so it cannot choose between the two consumers. Reading 3's "a choice about order the specification leaves open" should likewise say that the specification does not say what a consumer does.

**B2. UPHELD.**
- Confirmed by running it: the shop's Friday START has a job facet `sourceCodeLocation` (git, version `256e271`). `provider_event` rebuilds `job.facets` with `jobType` only, so the printed event silently loses the code version.
- The code version is Chapter 7's run-record field and the subject of Chapter 8's facet, so a learner comparing with Chapter 8 will see it go. The page lists three differences and omits this one.
- The research note (section 4) lists the provider's job facets as `jobType`, plus `documentation`, `ownership` and `tags` when present, plus whatever an operator's extractor returns. So absence is supportable.
- Fix: add the loss to the list of differences, worded as "the provider's own job facets do not include it". Add the supporting line to `sources.md`. Do not add the facet back.

**B3. UPHELD.**
- "As the provider would send it" overclaims. Research section 4 says a task event also carries the run facets `airflow` and `processing_engine`, and a `root` inside `parent` with the same values. The printed event has none of them.
- Fix: say the event is the shop's event with the provider's names, producer, `parent` and `jobType` applied. Add one bullet to "How this differs" saying a real task event carries more (named facets), and that the Dag's own run sends events as a job named `shop_nightly` (this covers S11's one valid point).
- If a sentence goes beside the cell, "the run ids are the shop's own" can go there at no cost (see S12).

## SHOULD

**S1. REJECTED.**
- The sentence is true and says only what the check tests: "breaks none of the rules Chapter 8's check tests". It does not claim that real Airflow events pass.
- `[]` is Chapter 8's normal output.
- Adding what the check does not establish costs words for a risk the sentence already avoids.

**S2. UPHELD.**
- "The provider takes them from what each task reports" has no support. Research does not cover extractors, inlets or outlets.
- Fix: drop the clause, or say the datasets are the shop's assumption because which datasets a real task reports depends on its operator. Record this in the "How this differs" list, as Chapter 30's list does for the shop's assumptions.

**S3. PARTLY UPHELD.**
- Stands: the page never names the versions read. Airflow's 2.20.3 comes from `__init__.py` on `main` at 7f0d50c.
- I checked the tag. `git ls-remote` finds only `providers-openlineage/2.20.3rc1` and no final `2.20.3` tag. So the printed `_producer` URL names a tag that does not exist today. The string itself is what the provider's code builds at that version, so the engine is right.
- Fix: in "How this differs", say the provider was read from its main branch, where the version reads 2.20.3 (a release candidate is tagged). Name Marquez once (commit 180f37b, 12 April 2026, 0.51.2-SNAPSHOT). Both are already in `sources.md`.
- Not needed: moving this into `details`, or changing the printed URL.
- Folds in C9: "the commit read" in place of "the version read" removes the clash with Marquez's "versions of jobs and datasets".

**S4. PARTLY UPHELD.**
- Stands: `RUNNING` and `OTHER` are specification types. Marquez has no case for them and falls through to `RUNNING` (research 1.1 and 1.3), so "any type it does not know" understates what it does with specification types.
- Also stands: `ABORT` to `ABORTED` is missing from the mapping bullet, though it is in `STATES` and in the end-time bullet.
- Fix: complete the mapping in one bullet, naming `RUNNING` and `OTHER` as specification types that give `RUNNING`, and add `ABORT`.
- Not needed: any cell showing a late `OTHER` reopening a run. The sentence does the job.

**S5. UPHELD.**
- "After every arrival" asks for a sequence. The cell asks for one state, and the table shows only the end state. "The next two cells send…" is ambiguous because the [WRITE] cell comes first.
- The answer-below convention is not at issue.
- Fix: ask for the state once all the events have arrived. Name the two cells that follow the writing cell ("the two cells after it").

**S6. REJECTED.**
- The notes record the design: the rules are the stated mechanism, the outcome is not, and it is "predictable: yes".
- It is a free-text commitment with no options. The learner's own belief (the reference consumer will match their collector) is what the result tests.
- Redesigning costs a new exercise for a modest gain. "I can't tell yet" does not apply when the listed rules settle it.

**S7. PARTLY UPHELD.**
- Stands: the end columns "its end" and "their end" are ambiguous pronouns. The Thursday row names no job (it is `build_daily_sales` in `FAULTED`).
- Fix: name the job in each row label, and label the end columns by consumer. This changes `compare`'s column names, so `test_engine.py` (lines 987-991) and `test_words.py` (line 1760) must change with it.
- Rejected sub-point: `remove_return` needs no explanation. Chapters 20 and 25 already use it the same way.

**S8. REJECTED.**
- The mapping bullet already shows `COMPLETE` gives `COMPLETED`, and Chapter 25 says a run's state is its latest event.
- The page states once that "your collector" is the shop's versions of the reader's three pieces.
- The remaining drift is minor and not worth words.

**S9. UPHELD.**
- "Two separate jobs" clashes with "job" as the shop's pipeline program. Replace it with "steps" or "problems".
- The second point is stronger than the finding says. Chapter 25 keeps two words: "repeat" (the same event, Saturday) and "retry" (a new time, Thursday). Chapter 29 calls Thursday's "the repeat" ("Your collector dropped the repeat…", "a repeat with a new time", "does not drop a repeat with a new time").
- Fix: use "retry" for Thursday and "repeat" for Saturday throughout.

**S10. PARTLY UPHELD.**
- Stands: Dag and provider are used with no gloss, and nothing says each task is named for its job. The plan puts Airflow in Chapter 30, but Chapter 29 uses it first.
- Fix: one plain sentence at first use covering what a Dag is and what the provider does (it sends an OpenLineage event for each task), and that each task is named for its job.
- Not needed for Marquez. Chapter 8 introduced it, and the section opens with its README quotation.

**S11. PARTLY UPHELD.**
- Stands: the Dag's own events as a job named `shop_nightly` are a real omission. Add them to the B3 bullet.
- Rejected: hedging "four new programs" (it already says "would") and Marquez's storage of a child job (research 1.2), which this chapter never uses.

**S12. REJECTED.**
- The disclosure is in the model-versus-reality list, where the course puts such notes.
- Run ids are opaque and nothing compares them. The B3 fix may carry the clause for free.

**S13. PARTLY UPHELD.**
- Stands: bullet 1 contradicts itself. "It needs nothing more" sits beside "unless something sorts the events first", which is a further need. Bullets 1 and 2 state results instead of what each reading needs.
- Fix: say in each bullet what the reading needs, and hedge the Friday claim as "by the rules above".
- Rejected: the HTTP/async detail, which does not bear on the chapter's results.

## COULD

**C1. UPHELD.** "The page could not show Marquez itself…" repeats "None of them runs on this page" and the first "How this differs" bullet, and has the page acting. Cut it.

**C2. UPHELD.** "Follow rules of their own" is empty, and "Parts II to VI built…" is a recap. Say what the rules cover: names, ids and facets for producers, and what a consumer does with repeated or late events.

**C3. UPHELD for the objective only.** Objective 3 says "the order in which the events arrive", but the arrival times do not change, only the order they reach the consumers. Use "reach", as the body does. Rejected sub-point: the `"event"` retry cost. `check` names the valid values. A side note: `compare` with an unknown `order` silently prints the arrival table (I ran `"event"`), but the check line above it names the valid values.

**C4. PARTLY UPHELD.** Use one verb ("stored" or "kept") for the 68 and 70. The 70 minus 68 gap is two lines above and easy to read, so no new sentence.

**C5. UPHELD.** "Nothing makes a row unique" is hard to parse. Say Marquez has no uniqueness rule on its table of events.

**C6. UPHELD.** The universal negative needs scoping. `sources.md` says the same, and the search covered README, CHANGELOG, `docs/docs` and the OpenAPI file. Scope it to the documents read, on the page and in `sources.md`.

**C7. REJECTED.** Chapter 8's wording is supported by `sources.md` ("Marquez" section: the Marquez site and the openlineage.io docs front page, 6 October). Chapter 29's README quotation is supported too. Neither contradicts the other. "Consumer" glosses an API implementation without distorting it.

**C8. REJECTED.** The reviewer calls it accurate. No defect, and no shop number to point at without extra material.

**C9. UPHELD, folded into S3.** Use "commit read" in place of "version read".
