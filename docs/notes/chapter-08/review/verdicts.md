VERDICTS ON CHAPTER 8

I checked every quote against the built page and chapter_08.py. I re-ran the engine and checked the specification files. Verified: 68 events, all passing `check`; 34 runs; one broken event refused by `Consumer.send` (`consumer.refused` has length 1); upstream traversal gives 2 nodes before the name change and 4 after. The reviewer's numbers are right.

Two points about the specification change the findings below:
- OpenLineage.md (core model) says "Sending at least a START event and a COMPLETE/FAIL/ABORT event is required."
- OpenLineage.md also says "An OpenAPI spec is also provided for HTTP-based implementations."

1. PARTLY (major, not BLOCKING).
- The quote is exact, and it is line 194. "The preceding section ends" is loose, because the mapping cell and table sit between. The sentence is in the same section.
- The problem is real. The sentence restates what the printed JSON already shows, just before a question that is answered by that JSON.
- The sentence is also redundant. Lines 243-245 say the same after the output, where the learner has earned it.
- The prediction itself is the plan's own (docs/plan.md line 121: "predict what a consumer knows after a START with no outputs…"). Its answer is derivable from the events by design.
- Cutting the sentence is enough. The reviewer's suggestion to redesign the prediction around an unnamed dataset is unnecessary, because the prediction already asks about clean_orders.
- Tension with finding 7: that finding wants more explanation of the JSON, and this one wants less. Resolve by explaining fields, not by saying what changes between START and COMPLETE.
- Rule: CLAUDE.md, no text gives away a prediction's answer.

2. UPHELD (BLOCKING is fair).
- Both quotes are exact: line 287 and line 348.
- The page says the name "holds the database `shop`", then says the analyst's name is "without the database", and only then asks whether the traversal reaches orders.jsonl. The cause comes before the effect (CLAUDE.md, "The effect before its cause").
- The learner is given the exact edit afterwards, and the explanation follows the result. That removes the chapter's own surprise (plan: "two producers name the same table differently and the lineage does not join"; objective 3).
- The direction is compatible with the rules. The code cell already shows both names, so the learner can compare them.

3. PARTLY (major, not BLOCKING).
- Upheld: the bullets mix what each reading needs with what the shop does, and there is no per-reading verdict (CLAUDE.md "Question the requirement", steps 3 and 5). The learner never sees the chapter's own `check` run over all events, although the engine shows all 68 pass. The summary table is in the same cell as the reading, and the course tells the learner to Run all first, so the table is in view while the learner is choosing.
- "As written … meets for its jobs and its functions" is muddled. "Our programs" is the ambiguity the exercise is about, and the next sentence says so. It is not wrong. It would be clearer as a verdict per reading.
- Rejected: the "delivery / where events are sent" gap, as stated. The reviewer says the specification is silent on delivery. That is wrong. sources.md records silence on what a consumer does with missing, duplicate or late events, and the specification ships an HTTP API definition. Adding a "the specification is silent on delivery" sentence would break the "never invent behaviour" rule. Delivery paths belong to Chapter 18 (plan line 149). The plan's own requirement readings for Chapter 8 are events, facets, namespaces and names.

4. REJECTED (mostly; not BLOCKING).
- The reviewer is right that `eventType` is not in the JSON Schema's `required` list, and that the count rule is in the field's description.
- The page's claim is nonetheless supported by two sources: the field description, and the specification's own prose in the core model ("Sending at least a START event and a COMPLETE/FAIL/ABORT event is required").
- The page never invites the learner to delete `eventType`.
- The residual issue is the word "schema requires". "The specification requires" would be exact.

5. UPHELD (major).
- The quote is exact.
- The specification has job events and dataset events. They are not about runs (sources.md, first bullet). CLAUDE.md says a definition must hold for every case the course will meet.
- Chapter 6 rests on the design-lineage distinction, so a later job event contradicts the opening.
- The fix is one clause naming run events and saying other kinds exist.

6. UPHELD (the finding is real; severity major, and the fix is cheap).
- All quotes are exact, including "a line it cannot read".
- The engine does refuse the event, so the claim is true. But no cell shows it: the only cell calls `check(broken)`.
- The closing reports as an experimental result something the learner did not see. It also sits beside "could not show … a line it cannot read", which confuses the reader.
- "Line" is not a term this chapter has introduced.
- Either send `broken` to a Consumer and show it set aside (the `refused` attribute exists), or drop "was refused" from the closing.

7. PARTLY (major, not BLOCKING).
- Verified counts: the two events run 43 and 62 lines, and `_producer` appears 8 times.
- Upheld: jobType, processingType and integration are never explained. `_producer` is never glossed (only the `producer` field is). The event-level schemaURL is explained only in a list later.
- Rejected: "the learner must diff by eye". The learner is told what differs (line 194), so the real problem there is finding 1, not this one.
- Showing the real events fits "computed from the engine". Detail the learner does not need could go in a `details` box (CLAUDE.md "A diagram carries…"). Reducing the display to a diff is optional.

8. PARTLY (minor).
- The quote is exact. "Differ in one place" is contradicted by the mapping table (run/runId, type/eventType, time/eventTime). Drop or rewrite the sentence.
- The "dataset vs asset" half is rejected. "Dataset" is already the course's own word (Chapter 6's model has a `dataset` type, and Chapter 7's lineage table has dataset nodes). The plan's Chapter 8 terms do not include it.

9. PARTLY (minor).
- "Schema" is real: `analytics` as a database schema, a facet's schema, and the specification's schema. CLAUDE.md lists the word.
- "Version" is partly real: the UUID version, the code version, datasetVersion and the version in each _schemaURL.
- "Program" is partly real. The `producer` gloss "the program that made the event" sounds like the job. In the shop it is one address shared by the four jobs.
- "Name" is over-called. A namespace plus a name is the specification's own term.

10. PARTLY (minor).
- Upheld: the "second producer" sentence is unused and unshown. The functions' producer is https://example.org/shop/functions/runtime/v2 and their times end +00:00. Either show one function event or cut the sentence. The database `shop` is not met in Chapters 2-7 (grep finds no `analytics` or database in them). The naming is the shop's choice and should be marked as such where first used. "34 runs" is not visible above; it can only be summed from the table below.
- Rejected: the mapping rows pointing to unseen facets (the mapping cell exists to list them). "Reporting namespace not printed" is true but the page does not rely on it.

11. UPHELD (minor). The objective says "Write an event by hand". The learner edits one string, and the closing says "until the analyst changed one" when it is the learner who changes it. Change the objective or the learner's task.

12. PARTLY (minor).
- The repeated-input merge ("did not list it twice") is the shop's code, and the page does not say so. The specification's example only says a producer need not re-emit.
- Dataset identity by namespace plus name is not purely the shop's choice: the object model gives a dataset a unique name within a namespace.
- The consumer's facet replacement applies to run facets only. The page states the replacement as the specification's, which is accurate.

13. UPHELD (minor to major, an engine inconsistency).
- The page says "The consumer writes each name as its namespace, then `/`, then the name."
- `runs()` prints shop/build_clean_orders, but `lineage()` drops the job namespace (`r["job"].split("/",1)[1]`), so the upstream() output shows copy_clean_orders. A same-named job in two namespaces would collapse into one node, which is the failure the chapter teaches.
- Fix in the engine. It affects Chapter 9's pinned tests.

14. PARTLY (minor).
- Chapter 7's closing question is reflective, about the learner's own design. It does not promise an answer.
- "ABORT" appears unexplained in a bullet. A one-clause gloss is warranted.
- The shop sends no ABORT, and Chapter 8's own closing question covers a run that never ends.

15. UPHELD (minor).
- Chapter 7 says code_version is "the first seven characters of a hash of the program's code".
- The facet has "type": "git" and a /blob/b178023/ URL. This looks like a commit; the specification says the value is the deployed version.
- One sentence saying the shop fills it with its own hash is enough.

16. PARTLY (minor).
- Upheld: "The requirement comes back at the end." (signposting); "…and the names of every other place where it is used." (unclear); "`orders.jsonl` has the name `orders.jsonl`…" (awkward); "as Chapter 7 left them." (filler).
- Rejected: the platform map being unused (CLAUDE.md says it appears in every chapter); the "knows" personification (it is the chapter's and the plan's framing, "what a consumer knows"; rewording is optional); the stray comma in "START, or COMPLETE or FAIL" (marginal); the Snowflake "same failure" (clear enough from context).

17. PARTLY (minor to major).
- "Disagree on one point" implies the only disagreement. sources.md records exactly one, which cannot support "only". The plan itself requires the course to say so, so keep the point.
- OTHER has not been introduced, except in the requirement bullet.
- Upheld: the note lacks real shop-versus-real differences. A real producer is a client library. The specification defines an HTTP API, which the shop does not use. The specification is silent on duplicates, late events and ordering. The shop's consumer takes a run's state from the last event received (`r["state"] = event.get(...)`).
- Do not write "the specification is silent on delivery".

ACT ON FIRST
1. Fix 2 first, then 1 (one sentence cut). Do 7 only for fields the learner needs, so it does not reintroduce the 1 problem.
2. Fix 6 (send `broken` to a consumer, or correct the closing).
3. Fix 13 (engine, namespaced job nodes).
4. Fix 5 and 3. Correct the delivery claim in the 3 direction: say nothing that implies the specification is silent on transport.
5. Then the minor wording fixes: 12, 15, 14, 8, 11, 10, 16, 9, 17.
6. Reject 4 apart from changing the wording "schema requires" to "the specification requires".
