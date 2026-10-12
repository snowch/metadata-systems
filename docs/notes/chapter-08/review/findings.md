REVIEW OF CHAPTER 8

Scope: I read the as-built chapter (prose, code cells and outputs) against Chapter 7 as built, docs/sources.md, the engine (notebook/shop/openlineage.py) and the specification files in the scratchpad. I re-ran the engine for the numbers. Confirmed correct: 34 runs; the summary table (7/7/7, 7/7/7, 7/7/6/1 FAIL, 7/7/7, 5, 1); 68 events; Friday 11 reads 27 and writes 23, as in Chapter 7; the traversal gives 2 nodes before the name change and 4 after (copy_clean_orders, shop.analytics.clean_orders, build_clean_orders, orders.jsonl); the analyst's copy exists on Friday 11 at 02:15:00 and 02:15:17. No number is wrong. The faults are in design, in claims about the specification, and in the prose.

Ranked, most serious first.

1. BLOCKING. The first prediction is answered on the page before the learner commits.
Where: "What a consumer knows". The preceding section ends: "The `START` names the input and no output. The `COMPLETE` names the input again, with its row count, and adds the output." The section then asks: "write in the next cell what the consumer knows about the run after the `START` alone, and what it knows about `clean_orders`."
Problem: the page states what a START carries, and the printed JSON shows it too, immediately before the question about what the START alone gives. The learner only has to carry the sentence across. The notes block admits the outcome is "predictable from the printed events", but the prose also states it. This is the "answer in view while the learner is still choosing" fault.
Direction: cut that sentence from before the prediction, or move it after the consumer's rows. Let the learner read the two events and reason from them. The prediction should rest on something the learner has to work out, such as what the consumer can say about a dataset no event has named yet.

2. BLOCKING. The traversal prediction gives its cause before asking for the effect, and then gives the fix.
Where: "An event written by hand": "The analyst names `clean_orders` as `analytics.clean_orders` in the namespace `warehouse://shop-warehouse`, without the database." Then: "Before you read on, write in the next cell whether that traversal will reach `orders.jsonl`." Then, after the output: "change `"analytics.clean_orders"` to `"shop.analytics.clean_orders"`."
Problem: the preceding section explains that the shop's name "holds the database `shop`, the schema `analytics` and the table `clean_orders`". The setup then says the analyst's name omits the database. The prediction becomes a one-step deduction from the setup, not a belief tested against evidence. The rule is "the effect before its cause" and no option or setup text may carry the explanation. The learner is also told the exact edit, so nothing is left to find.
Direction: show the analyst's events without commenting on how the name differs, and ask the question. After the output, ask the learner what they would change, or which of the two names the consumer should treat as the shop's. Give the comparison as evidence after the result.

3. BLOCKING. The requirement section does not keep the five steps, and its verdict is unsupported and arguably wrong.
Where: the section '"Our programs must emit OpenLineage."'
- Step 3 (what information each reading needs) is missing. Chapter 7 had a needs/missing/met table. Here the bullets say what the shop does ("the jobs and the functions send events. The export and the analyst's copy do not") or what the specification says. They never say what each reading would need to be answered.
- Step 5 (does the record meet each reading) is missing per reading. The only verdict is one sentence: "As written, the shop meets the requirement for its jobs and its functions."
- "As written" is wrong or at least muddled. The words "Our programs" include the export and the analyst's copy, which the same section says send nothing. The sentence answers a narrower question than the one asked, and also says "the requirement does not say" which programs it means. Those two statements pull against each other.
- Nothing on the page shows that the events are valid. The learner's evidence cell counts events by type. It does not run the chapter's own check over the 68 events. "Emit OpenLineage" could mean conforming events, and the chapter has just built the tool that tests that.
- The summary table is printed in the same cell where the learner writes their reading. It shows which jobs sent events and which event types each sent, so it pre-answers the "which programs" and "which events" readings. It also keeps counting events by type, not conformity.
- Missing readings: where events are sent to, and whether they arrive. The chapter says "To emit an event is to send it" and never says to what. The specification is silent on delivery (sources.md), and the chapter should say so once.
Direction: put each reading beside what it needs and what the shop records, and give each a verdict. Run the check over all the events as evidence for "valid". Print the summary after the learner commits, or make the learner ask for it.

4. BLOCKING. A claim about the schema is stronger than the source supports.
Where: "Which events: the specification's schema requires one `START`, and one of `COMPLETE`, `ABORT` or `FAIL`, for each run."
Problem: in OpenLineage.json that sentence is the description of the `eventType` field ("It is required to issue 1 START event and 1 of [ COMPLETE, ABORT, FAIL ] event per run"). The same schema does not list `eventType` in `required`; only `run` and `job` (plus `eventTime`, `producer`, `schemaURL`) are required. JSON Schema cannot enforce per-run counts. The learner's own check accepts an event with no `eventType`. The page lists the check's rules without saying that `eventType` is optional. A learner may delete it, see no problem, and be confused. sources.md records the quotation correctly, but it is a field description, not a constraint.
Direction: say the field's description requires it, and that the schema does not make `eventType` mandatory on any one event.

5. BLOCKING. The definition of OpenLineage does not hold for every case.
Where: "**OpenLineage** is an open specification for events about runs of jobs."
Problem: the specification defines three kinds of event: run, job and dataset (sources.md, first bullet). The chapter's objective and everything after use only run events. The Accuracy rule says a definition must hold for every case the course will meet. sources.md also says Chapter 6's declared and observed dependencies "rest on" the runtime/design distinction. A learner who later meets a job event would find the opening wrong.
Direction: name run events, and say once that two other kinds exist, perhaps in a details box.

6. BLOCKING. The page says it showed a refusal that no cell showed.
Where: "The shop's consumer refuses an event that breaks the rules, and keeps it aside." Closing: "An event that broke two rules was refused." The notes also list "sees an event that breaks two rules refused".
Problem: the only cell in that section calls `check(broken)`, which lists two problems. No cell sends `broken` to a consumer. The refusal is asserted, not seen. The closing then also says the experiments "could not show ... what a consumer does with a line it cannot read", which sits close to the refusal claim and confuses the reader. "Line" is not a term this chapter uses for events: the events are dictionaries, and "lines" was Chapter 6's word for typed records.
Direction: either send `broken` to a consumer and show it set aside, or drop "refused" from the closing. Say plainly what Chapter 9 adds, without "line".

7. BLOCKING. The first contact with an event is a wall of JSON that the prose does not cover.
Where: the first code cell prints two near-identical events, about 60 lines each, with `_producer` printed 8 times. The explanation follows below the output, in sentences scattered over ten paragraphs. The learner must scroll back up for each one.
Problems:
- The prose never explains `jobType`, `processingType`, `integration`, the event-level `schemaURL`, `eventTime`, or what `_producer` is for and how it differs from `producer`. Its list of facets ("`inputStatistics`... `outputStatistics`... `sourceCodeLocation`... `nominalTime`") skips `jobType`, which is printed. "`schemaURL`" is checked in a later list ("`eventTime`, `producer`, `schemaURL`...") but never explained.
- The learner must diff two events by eye to see what changed between START and COMPLETE, and this is the point the next section builds on.
Direction: print the START in full and the COMPLETE as the part that differs (or hide the facets by default and show them on request). Put the explanations next to the lines they explain, or attach a details block to each. If a field is not needed for the next step, leave it out of what the learner must read.

8. MINOR. "The specification's words differ from the shop's in one place" is contradicted by the chapter itself.
Where: opening: "The specification's words differ from the shop's in one place. What a run reads are its inputs. What it writes are its outputs."
Problem: the mapping table that follows shows many renamings: `run` to `runId`, `type` to `eventType`, `time` to `eventTime`, and others. The course's own word for a thing the data lives in is "asset" (Chapter 2 and Chapter 7: "each asset"). The chapter switches to "dataset" without saying that it is the specification's word for the same thing, although Chapter 7's lineage output already used `dataset` as a node type.
Direction: either drop the sentence or name the real differences. Say that "dataset" is the specification's word for what the course called an asset.

9. MINOR. Words that mean more than one thing on this page.
- "schema": the database schema `analytics`, "the address of the facet's schema", and "the specification's schema" (the JSON Schema). CLAUDE.md lists this word by name.
- "version": a UUID "of version 7", the "code version `b178023`", the `version` facet (`datasetVersion`), `object_version`, and the version numbers inside each `_schemaURL`.
- "program": the shop's jobs and functions, and also "the address of the program that made the event" in the definition of `producer`. The `producer` value is a single address for the shop's four jobs. In the specification it is a URI identifying the producer of the metadata, i.e. the code that sent the event, not the job being run. The page's gloss makes the producer sound like the job.
- "name": job name, dataset name, facet name, and the consumer's "namespace/name" string.
Direction: pick one meaning per word, or add a short gloss where the second meaning first appears.

10. MINOR. Claims about things the learner is never shown.
- "The functions' events come from a second producer: the library of the platform the functions run on." No cell prints a function's event, and Chapter 7 said both functions "send events as the jobs do". The sentence adds a fact the chapter never uses. The effect (`+00:00` times) is not mentioned.
- The mapping row `object_version` points to `inputs[].facets.version.datasetVersion` and the three object rows point to `shop_objectChange`. The learner has seen neither. The custom facet is not explained until the last section ("It is named with the shop's prefix, as the specification asks of a facet that is not standard"), though it appears in the mapping much earlier.
- "the shop's own for its warehouse and its reporting tool": the reporting namespace is not printed anywhere.
- "That name holds the database `shop`, the schema `analytics` and the table `clean_orders`" is stated as a fact about the warehouse. Chapters 2 to 7 use only `clean_orders`, and the learner has never met a database called `shop`. The three-part name is the shop's producers' choice. That is said only later ("a warehouse like the shop's... the shop's producers must agree on one"), and the phrase "a warehouse like the shop's" is vague about what the shop's warehouse is.
- "The consumer holds 34 runs" is not visible in the output above it, which lists only FAIL rows.
Direction: print one function's event, or drop the claims. Mark the naming as the shop's choice where the name is first used.

11. MINOR. The objective and the narration do not match what the learner does.
Where: objective "Write an event by hand"; section "An event written by hand"; closing: "two names for one table did not join until the analyst changed one".
Problem: the analyst's events are already written in the cell. The learner only edits one string. In the closing it was the learner who changed the name, not the analyst. The learner never writes an event.
Direction: change the objective to match what they do, or have them write the fields.

12. MINOR. The additive claim sits next to behaviour that is the shop's choice.
Where: "The `COMPLETE` named the input again, and the consumer did not list it twice. The specification says that events about one run add to each other. In its words: 'All metadata is additive.'"
Problem: the quotation is accurate. But the specification's example only says a producer need not re-emit earlier inputs. It does not say how a repeated input merges, or that datasets match by namespace and name. The consumer's matching is the shop's code. The facet-replacement sentence is also the specification's, yet the shop's consumer replaces only run facets. The chapter's own rule (CLAUDE.md, "Never invent behaviour for an open standard") asks for a separation.
Direction: say what the specification states, then say that the matching of a repeated input is the shop's choice.

13. MINOR. Inconsistency in how the consumer names things.
Where: "The consumer writes each name as its namespace, then `/`, then the name."
Problem: the `runs()` table shows jobs as `shop/build_clean_orders`, and datasets with the full namespace. The `upstream()` table shows jobs without a namespace (`copy_clean_orders`, `build_clean_orders`) and datasets with it. A job called `x` in two namespaces would be one node in the traversal, which is the failure the chapter is teaching about names.
Direction: either make the lineage show the namespace or note the difference.

14. MINOR. FAIL and ABORT, and Chapter 7's open question.
Chapter 7 closes with "In your design, which events exist for a program that stops before it finishes?" Chapter 8 mentions only FAIL in the prose ("A run that fails sends `FAIL` in place of `COMPLETE`"). ABORT appears first in a bullet of the requirement section, never explained. Chapter 7's question is left unanswered. Say in one sentence what ABORT is for and what the shop does about a program that just stops.

15. MINOR. The code version.
`sourceCodeLocation` has `"type": "git"` and a `version` the page calls "the code version, `b178023`". In Chapter 7, `code_version` is "the first seven characters of a hash of the program's code". The specification says the version field is "the git sha | Svn: the revision number". The shop's value is a code hash, not a commit. The URL `.../blob/b178023/...` makes it look like a commit. Say that the shop fills the field with its own hash.

16. MINOR. Prose faults (style.md and CLAUDE.md).
- Signposting: "The requirement comes back at the end."
- Unclear sentence: "A tool written elsewhere would have to learn those names, and the names of every other place where it is used." It is not clear what "every other place" is.
- Vague: "Further metadata comes in a facet: a named object." Also "It holds `_producer`, then `_schemaURL`..." reads as if the order mattered.
- Personification: heading "What a consumer knows", "It knows that the run began", "It knows nothing about `clean_orders`", "It cannot tell". Prefer what the consumer holds or has recorded.
- Meta-filler: "The platform map shows the shop's three systems and the returns desk, as Chapter 7 left them." The figure is not used by any question in the chapter. The standing rule says a figure carries something the prose would make the learner hold, and this one carries nothing the chapter needs.
- Awkward: "`orders.jsonl` has the name `orders.jsonl` in the namespace `s3://shop-raw`, which is its bucket." The mapping row "eventType: START, or COMPLETE or FAIL" has a stray comma.
- The paragraph about the Snowflake name warns "of the same failure" without saying which failure. The supporting text exists (naming.md); the page should state it.

17. MINOR. The "How this differs from a real platform" note.
- "The specification's schema and its page on the run cycle disagree on one point." This implies it is the only disagreement; sources.md records only that one. `OTHER` events have never been introduced to the learner, and the "run cycle page" is not introduced either. The note is a statement about the specification, not a difference between the shop and a real platform.
- It says little about the real differences: a real producer is a client library, not a shop-written function; events travel over a transport to a backend; the specification is silent on duplicates, order and late events (sources.md); and the shop's consumer takes a run's state from the event it received last, not from the event time. The last of these matters for the closing question about a START that never gets a successor.

What is sound: the numbers; the Marquez and Chapter 29 references; the UUIDv7 and naming-page claims; the custom facet prefix; the Snowflake warning; the quote "All metadata is additive"; the engine-checked traversal results (2 and 4 nodes); the "34 runs"; and the Chapter 7 continuity of Friday 11 (27 read, 23 written).
