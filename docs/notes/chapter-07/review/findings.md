REVIEW OF CHAPTER 7

Method: I read the as-built chapter, the source, the author's notes and Chapter 6 as the learner met it. I re-ran the engine for the figures below. Every number in the tables matches the engine. The 0/0/1/4/4/4/4 left-out series, the 14 events, the 6 function runs, `256e271` and `c715bde` on the right nights, the 6-node and 1-node traversals, and the `readings` table for the default `yours` all check out. The findings are about what the page claims from those numbers, what it gives away, and continuity.

Ranked, most serious first.

1. BLOCKING. The headline answer to Jo is stated as if the events showed it, and they show only counts.
- Where: "How many orders, each night", after the grouped table.
- Quotes: "The run on Thursday 10 left out 1 row: the export's second copy of order 7015", "left out 3 more: Thursday's three orders with no customer id", and "The answer to Jo's question: 3 orders, all placed on Thursday".
- Problem: the events carry `rows_read` and `rows_written`, so subtraction gives 0, 0, 1, 4, 4, 4, 4 and nothing more. Which rows, and why, comes from Chapter 2's rules and Chapter 3's finding. The learner already knows that Thursday has three orders with no customer id, so "3, Thursday" adds little to what they know. The page never says what the events cannot tell: which orders were left out, or that the rule did it.
- Overstatement: "nothing on the platform keeps what an earlier night did" is also too strong. The raw file still holds every order, and one query on it counts the null customer ids.
- What the events add: independent evidence of what the job did, on which run, and how the count moved. The experiment's value sits there.
- Direction: separate what the events show (counts per run, the step on Friday 11) from what the learner attributes using earlier chapters. Say that the events cannot name the orders. Reword the "nothing keeps" claim around what the job did each night, not what can be recomputed.

2. BLOCKING. The prediction on Wednesday 9 is nearly answered by the sentences above it.
- Where: "Telling runs apart", the cell `expected_wednesday`.
- Quote just above: "Grouping by `job` and `day` gave one row for each night, because each job runs once a night."
- Problem: the sentence names the grouping key and the cadence that made it work. The next line gives two creates on one day. The author's own notes say "Predictable: yes, from the two times given." The prediction asks for the count and its reason in one go, and the reason is a restatement of the rule just given.
- Direction: take the "because each job runs once a night" clause out, or state the cadence only after the result. Consider asking for what the learner would expect to see for the two runs, not the row count plus a reason.

3. BLOCKING. The conclusion of the "without reads" experiment is self-contradictory and not backed by anything the learner has seen.
- Where: "What each run read", after the traversal.
- Quote: "Events that list nothing read do not show that the run read nothing. `remove_return` really read nothing, and its events look the same as events that leave `reads` out."
- Problems:
  - The example is a run that did read nothing, which supports the opposite reading of the first sentence.
  - Nobody has seen `remove_return`'s `reads` value. The earlier table has `rows_read` 0 but no `reads` column. In the engine its `reads` is empty (None), while `record_return` shows a file. The traversal in this section is built on `week`, which has no functions at all.
  - The prediction before it ("what that traversal would reach if the events carried no `reads`") is answerable from Chapter 6 alone: no `reads` means no edges. It does not test the idea the experiment is meant to teach.
- Direction: say plainly that a run with an empty `reads` and a run whose events leave `reads` out give the same graph. Show `remove_return`'s `reads` somewhere before the claim, or drop the example. Ask the prediction about the empty-versus-absent case.

4. BLOCKING. Continuity with Chapter 6 is unexplained on the one question this section claims to answer.
- Chapter 6: "from Saturday, `build_daily_sales` is changed to read the copy".
- Chapter 7: "The runs on Sunday 13 and Monday 14 read `s3://shop-scratch/clean_orders_copy.csv`", and Saturday 12's run still reads `clean_orders`.
- Why the dates differ: the code uses `day >= 2026-09-12`. The run at 02:30 on Sunday 13 writes Saturday's row, which is why Sunday is the first night on the copy.
- Problem: the chapter explains this convention once ("the run on Friday 11, which read the orders up to Thursday") and then drops it. A careful reader sees "Saturday" in Chapter 6 and "Sunday" here and may think one is wrong.
- Direction: one sentence tying the first copy night to Saturday's row.

5. MINOR. The returns-desk figure is ambiguous and disagrees with the next section.
- Caption: "the platform with the returns desk on Monday morning: three return files in object storage".
- What it shows: `r-201`, `r-202`, `r-204`, which is the state on Monday 14 after the week. The week's runs start on Tuesday 8 and the learner has only met "Monday 14" as the last night. The next section says the desk created `r-202` and `r-203` on Wednesday 9, and `r-203` is not in the figure.
- Side effect: the figure also reveals that a deletion happened, before the page introduces it.
- Direction: date the figure, or draw it at a time that matches what the prose is about to discuss. The flow label "jobs nightly; functions at any hour" sits on both arrows and does not say what the functions move.

6. MINOR. The requirement section keeps the five steps only loosely.
- Staging: the prose says "The cell sets your design against four readings" before the learner commits. The table then shows the readings, what each needs, and whether each is met, all at once. The bullets after it repeat the table, so the same argument is made twice.
- Step 4: "what the platform records, and by which meaning" is not distinct from the learner's own list. The page never asks what a field's name means. For example, `time` is "when the program sent the event", which is not the moment the data was written. The reading "know when each asset was last written" claims that `time` and `writes` suffice.
- Quote: "As written, any design meets 'Record every run.' if each run sends events." This sits badly beside the chapter's own finding that, without `run`, two runs merge into one row. A design of `job` and `type` alone records events but cannot tell the runs apart. I confirmed `readings(['job','type'])` returns "no" on every row.
- The `needs` lists omit `job`. A design of `run` and `code_version` is marked "met" for "know which version of the code each run used", yet nothing says which program that run belongs to.
- "find the runs that failed: `run`, `status`" is marked met. The learner has never seen a `status` value, and the week used has no failed run. Chapter 6 promised "whether it succeeded" and Chapter 2 asked about the failed night.
- A program that stops before its finish event sends no `status` at all. The reflective question 2 hints at this, but the readings table does not.
- Direction: let the learner commit before the readings are named. Question what `time` and `status` mean in the reading that uses them. Qualify "any design" with the `run` point. Show at least one `status` value.

7. MINOR. The objective overstates what the learner does.
- Objective: "Design the messages a program sends as it works". The first design, `with_run` and `with_reads` are all given. The learner designs only `yours`, which feeds nothing afterwards.
- Reflective question 2, "In your design, which events exist for a program that stops before it finishes?", speaks of events, but the design is a list of fields.
- Direction: reword the objective, or give the learner a decision that changes a later result.

8. MINOR. Two engine rows are shown without comment.
- Wednesday 9's merged row shows `rows_read` 1 and `rows_written` 1, but its two runs read one row each. The merge deduplicates equal values, so the count is hidden. The page discusses only the times and the objects.
- The `remove_return` row has `rows_written` 1 for a removal, while "rows_written" is defined as "how many rows the program wrote".
- Direction: either mention the first (the merge hides a count) or accept it deliberately. Explain the second in a clause.

9. MINOR. Numbers and wording.
- "two runs, merged into one that seems to last five and a half hours". 10:05:02 to 15:40:05 is 5 h 35 m, and the engine did not produce "five and a half". Use the two times alone, or compute the span.
- Personification and overstatement: "`daily_sales` seems to be made from nothing" (twice, including the closing summary). Say what the graph holds: no input is shown for `daily_sales`. "Each run recorded what it read" and "The runs recorded which nights" give agency to runs.
- Vague closing: "Nothing here shows how a program the shop did not write would know what each field means." Name the limit. "...in the form an open standard sets, which programs the shop did not write can read" has an ambiguous "which".
- "The three systems, in the order data moves through them each night." is a fragment standing as a label.

10. MINOR. Terms and tables.
- "program", "job" and "function" are used loosely. "The shop's programs" is never defined as jobs plus functions until later. The field `job` holds function names, such as `record_return`.
- "runs the week" (verb) sits beside "a run" (noun) and the grouping function `runs`.
- The fields table lists `object`, `object_version` and `object_change` ("for a program started by a change to a file") before any such program exists.
- Object storage versions are never introduced. Overwriting gives a new `object_version` and deleting gives one too. The "How this differs" section does not say that real buckets need versioning switched on.
- The "What each run read" table adds `returns` to the week. That puts five empty object columns beside `build_daily_sales`, a wide table nobody chose for this question. The `lineage` cell uses `week`, so the graph omits the copy the learner has just found, and the page does not say so.
- The `time` and `run` argument is stronger than the evidence. The two Wednesday runs do not overlap, so pairing each start with the next finish would also work. Nothing in the chapter shows a case where only `run` suffices, such as overlapping runs or a missing finish.
- The `started` and `finished` columns appear without a definition.

Not found: em dashes, "lab" or engine mentions, bad cross-references (Chapters 19 and 20 match the plan), forward-term violations, or numbers contradicting the outputs.
