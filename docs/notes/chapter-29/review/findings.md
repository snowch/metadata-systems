# REVIEW OF CHAPTER 29, "OpenLineage in practice"

Numbers checked: I ran `shop.run_week(["returns"])` and `shop.consumers.provider`, `provider_event`, `compare`, `totals` and `check` from `/home/user/metadata-systems/notebook`. I ran them for both `order` values and for the wrong values `"event"`, `"Event time"` and `""`. I also listed the week's arrivals (`shop.collector.arrivals`) and diffed the provider event against the shop's own event from `week_events`. Every figure in the page matches: the 4 job names, the Friday START at 02:30:00 arriving 02:31:03, Thursday end 02:30:52 with 3 rows and 3 state rows, Saturday 3 rows against 2, 68 against 70 with 1 refusal each, and the check failing at `"arrival"` and passing at `"event time"`. I also read `docs/sources.md` ("Read for Part VII", Part V, Part I), `docs/notes/part-7/research/chapter-29.md`, `docs/notes/part-7/design.md`, and the earlier chapters' text on Chapters 8, 12, 20, 22 and 25. I did not run the memory and time callout; it was not in the as-built file.

## BLOCKING

**B1. The requirement section says the specification is silent where the course's own sources say it is not.**
- The page: "use a consumer that does what the specification requires: the OpenLineage specification says nothing about repeats, late events or order, so Marquez's rules and your collector both meet it". The next bullet adds: "for Friday 11 that is a choice about order the specification leaves open".
- `docs/sources.md` (Part I and Part V) records two things that contradict this. `eventType` says "It is required to issue 1 START event and 1 of [ COMPLETE, ABORT, FAIL ] event per run". The run-cycle page says that after a terminal event "no other events related to this run will be emitted". The schema and the run-cycle page also disagree about events after a terminal one. Chapter 8's closing note states that disagreement.
- So the specification does speak to Thursday's second COMPLETE with a new time, Saturday's repeat, and a START after a terminal event. It speaks about what a producer sends and the run's lifecycle. It is silent on what a consumer does with them. The "How this differs" bullet is scoped correctly ("what a consumer does"); the requirement bullets are not.
- "Both meet it" has nothing to be tested against if the specification has no consumer rules. "A choice … the specification leaves open" ignores the lifecycle text, which bears on whether a START can follow a COMPLETE.
- Direction: scope each claim to consumers and say what the specification does say. State the conflict between the schema and the run-cycle page as it is, or say what reading 2 needs if the specification has no consumer rules.

**B2. The provider-event section says the event differs from the shop's own in three ways. It also differs in a fourth, the most telling one.**
- The page: "These differ from the shop's own event:" followed by the producer, the `parent` facet, and `jobType` giving `AIRFLOW`, `BATCH` and `TASK`.
- The shop's own Friday START carries a job facet `sourceCodeLocation` (git `url` and `version` "256e271"). `provider_event` rebuilds `job.facets` with `jobType` only, so the code version vanishes from the printed event. The page never says so, and Chapter 7 built the run record around the code version.
- Nothing in `docs/sources.md` or the research note supports the claim that the provider sends no such facet. The effect is a silent claim about the real provider.
- Direction: either keep the facet, or list the loss in the differences and say which source supports it.

**B3. "As the provider would send it" overclaims.**
- The page: "The next cell shows the `START` ... as the provider would send it."
- The research note (section 4) says the provider's task events carry more than the cell shows: run facets `airflow` and `processing_engine`, and a `root` inside the `parent` facet "with the same values". It also says the Dag run sends its own events as a job named for the Dag.
- The printed event has none of these. The model-versus-reality list does not say that the event is a subset.
- Direction: say it is the shop's event with the provider's names, producer, `parent` and `jobType` applied, and name what a real event adds. Or add the facets the sources support.

## SHOULD

**S1. The check on the provider event proves less than the page lets it.**
- The page: "The event breaks none of the rules Chapter 8's check tests."
- The event is the shop's own event with values substituted by `provider_event`, so passing Chapter 8's check says nothing about what Airflow emits. A bare `[]` is the cell's output.
- Direction: say what the check does and does not establish, or say what it shows the reader about the renamed event.

**S2. An unsupported sentence about datasets.**
- The page: "The datasets keep the shop's names: the provider takes them from what each task reports."
- No source in `sources.md` or the research note says how the provider finds datasets. The research does not cover extractors, inlets or outlets.
- Direction: cite or drop it, or say that the shop's datasets are assumed here.

**S3. Marquez's version is never named on the page.**
- The page: "as its code states it in the version read" and "the version read". Airflow gets "version 2.20.3", but Marquez has no version or commit (`180f37b`, 12 April 2026, 0.51.2-SNAPSHOT).
- Marquez's rules are code reading only, and the research says they were not tested against a running Marquez. A reader cannot tell which Marquez.
- Direction: name the commit once, perhaps in `details`.
- Also: the provider version 2.20.3 was read from `main` at commit `7f0d50c`, not a release tag. The printed `_producer` URL names a `providers-openlineage/2.20.3` tag that I could not check exists. Say "read from the main branch" or confirm the tag.

**S4. The Marquez rules hide how Marquez treats types the specification does define.**
- The page: "`START` gives `RUNNING`, as does any type it does not know".
- `RUNNING` and `OTHER` are specification types. Research 1.3 says Marquez maps them to `RUNNING` too, so a late `OTHER` after a `COMPLETE`, which the schema explicitly allows, reopens a finished run.
- "Any type it does not know" understates that, and it is the bridge to the specification's own disagreement.
- Also: `ABORT` is in the end-time bullet but not in the state mapping (`ABORTED`).
- Direction: complete the mapping and say which are the specification's types.

**S5. The prediction's prose and cell disagree, and the output does not show what was asked.**
- The page above the cell: "write in the next cell which state Marquez's rules set for that run after every arrival".
- The cell: "Which state will Marquez's rules set for the run early on Friday 11?"
- "After every arrival" asks for a sequence. The cell asks for one state, and the table shows only the end state. The reader cannot compare what they wrote with what a cell shows.
- Direction: ask for one thing and show that thing.
- Also, "The next two cells send Chapter 25's arrivals" is ambiguous because the next cell is the [WRITE] cell.

**S6. The prediction is near-derivable from the rules just above it.**
- The page: "in the order it takes the events, without comparing their times" followed by "The `START` arrived at 02:31:03, after the `COMPLETE`."
- The reader applies a stated rule, not a belief about the shop. The stage of the investigation (is there a discrepancy?) is folded into the rule.
- Direction: consider asking for a belief about the shop that the rule list does not settle. If it stays, say what a reader who writes "I can't tell yet" should check.

**S7. The comparison table is hard to read as a pair.**
- Columns "its end" and "their end" point at different consumers by pronoun.
- Rows read "Thursday 10: its COMPLETE again, with a new time" without naming the job. Thursday's job (`build_daily_sales`) is never named anywhere, and `remove_return` is named only in the prose below.
- "`remove_return`'s" is a function introduced in Chapter 25 and is not explained here.
- Direction: name the job per row; label the end columns by consumer.

**S8. "State" and "same state" hide the two vocabularies.**
- The page: "The check below tests whether Friday 11's run is in the same state in both." Then the passing outcome: "`COMPLETED` by Marquez's rules and `COMPLETE` in your collector."
- The collector's state is an event type. Marquez's is a state name, and the page never says `COMPLETE` and `COMPLETED` are the same condition.
- Also: "your collector" is the shop's version of the reader's three pieces ("the shop's versions of your three pieces"). Wording such as "Your collector dropped the repeat" and "Compare this with what you wrote" blurs whose code ran.

**S9. A word with two meanings.**
- The page: "Putting events in order and dropping repeats are two separate jobs."
- "Jobs" means the shop's pipeline jobs everywhere else in the chapter.
- Related: "repeat" is used for Thursday's second COMPLETE with a new time, while Chapter 25 calls it a "retry". Pick one word.

**S10. The reader is never told what Airflow, a Dag, a provider or Marquez is.**
- The page: "Suppose the shop's four nightly jobs ran as tasks of one Airflow Dag, `shop_nightly`, and sent their events through Airflow's OpenLineage provider"; "Which of your jobs would a new scheduler rename?"
- Nothing says each task is named for its job. The table's names rest on that unstated assumption. Chapter 30 is where these systems are covered.
- `Marquez` is described only as "the reference implementation of the OpenLineage API".
- Direction: one plain sentence at first use for each of Dag, provider and Marquez.

**S11. The model-versus-reality list leaves out differences that matter for "four new programs".**
- The page: "The shop's lineage would take the provider's four jobs as four new programs."
- A real provider also sends events for the Dag as a job (research section 4, `dag_started`), which would be a fifth. That is not mentioned.
- The sentence itself has no cell behind it; it rests on Chapters 12 and 22.
- Nothing is said about how Marquez would store a child job with a parent (research 1.2).
- Direction: add the Dag's own events to the list, and either point at the chapter whose graph shows the new programs or hedge the sentence.

**S12. The run ids are not disclosed where they are shown.**
- The page prints `"runId": "01a08e4c-e840-7800-af00-fc7c8d187682"`. Only the last bullet says "The provider's run ids here are the shop's own, made from the values the provider uses."
- Direction: put the disclosure beside the cell.

**S13. Marquez-specific hedges are missing in the requirement bullets.**
- The page: "the shop would hold Friday 11's run as `RUNNING` unless something sorts the events first".
- This states a real system's behaviour as fact. It is code reading only, and it does not mention the HTTP/async path.
- The same bullet's "it needs nothing more" is not a statement of what the reading needs, which is the point of the five-part structure.
- Direction: hedge with "by the code read", and state in each bullet the information the reading needs.

## COULD

- **C1.** "The page could not show Marquez itself: each result is Marquez's rules, as its code states them, applied here." This repeats "None of them runs on this page" and the last model-versus-reality bullets. It also treats the page as an agent ("the page could not show"). Say it once.
- **C2.** "Parts II to VI built the shop's own producers, its collector and its graph. Real producers and consumers of OpenLineage events follow rules of their own." The second sentence is vague ("rules of their own").
- **C3.** Objective 3: "Change the order in which the events arrive". The cell sorts the events before they reach the consumers, as the body says ("the order in which the events reach Marquez's rules"). Use one verb. Chapter 20 used the value `"event"`, while this chapter requires `"event time"`; the error message lists the valid values, so this only costs a retry.
- **C4.** "Over the week, both rejected the developer's event with no `eventTime`. Your collector stored 68 events, and Marquez's rules kept 70." The page never says that 70 − 68 is the two repeats. Say "stored" or "kept" consistently.
- **C5.** The Marquez bullet "it keeps every event it takes as a row, and nothing makes a row unique" is hard to parse. Say there is no uniqueness rule on the table of events.
- **C6.** "No Marquez document says what it does with a repeated, late or out-of-order event" is a universal negative drawn from searching a README, a CHANGELOG, the docs folder and the OpenAPI file. Scope it to the documents read.
- **C7.** Chapter 8 says "The OpenLineage documentation calls Marquez the reference implementation of its API". Chapter 29 says "OpenLineage's own README". `sources.md` records the README. Align Chapter 8. The README says "reference implementation of the OpenLineage API", while the requirement's "reference consumer" is the shop's phrase. The first bullet's gloss "the consumer the OpenLineage project names as its reference implementation" slightly stretches it.
- **C8.** "The buffer here sorted the whole week before sending anything. A real buffer can hold events only for a while, and an event later than that still arrives out of order." This is accurate and useful. Point at the shop's own numbers if possible.
- **C9.** The word "version" is used for the software version ("the version read", "version 2.20.3") and for Marquez's versions of jobs and datasets ("keeps versions of jobs and datasets").

## What reads well

The wrong-value messages for `order` name the valid values. The check line at the starting value names the disagreement (RUNNING against COMPLETE). The single change is stated and sufficient. Every number I checked matches the engine.
