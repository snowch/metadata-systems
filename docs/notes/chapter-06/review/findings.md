# Review of Chapter 6, "What is lineage?" (first read, 12 October 2026)

I read it as a learner who has done Chapters 1 to 5. I checked numbers and claims against the engine in `notebook/shop` by running it. The findings are ranked, most serious first, and each is marked blocking or minor.

## Findings

**1. The developer's question is never answered, and the answer the chapter gives overstates it. Blocking.**
- Where: "The jobs' code", "What a change to `orders.jsonl` affects" and "Before Chapter 7".
- The page: the chapter opens with "Next week we rename `customer_id` in `orders.jsonl` to `customer_ref`. What does that affect?" and "That is the third question from Chapter 2."
- The prediction then asks "Which assets does a change to orders.jsonl affect, and why?" The prose answers: "Downstream of `orders.jsonl` there are 6 nodes."
- Problem 1: a column rename has become "a change to `orders.jsonl`". The chapter never returns to the rename.
- Problem 2: the 6-node walk implies the rename reaches `daily_sales` and the dashboard. The code printed on the page says otherwise. Only `build_clean_orders` names `customer_id`. `build_daily_sales` reads `clean_orders` without it.
- The chapter does say lines between tables cannot show column-level facts (the fourth reading, "Chapter 10"). It never connects that to the developer's question. The reader leaves believing the answer to the developer is "everything downstream".
- Direction: either say the walk is an upper bound for a file-level change and not an answer about the rename, or let the reader notice it. A good moment is after the downstream walk, with the code in view: which of these jobs even mentions `customer_id`? Close the opening question explicitly at the end.

**2. The prediction about `orders.jsonl` is answered by the drawing and the prose directly above it. Blocking.**
- Where: "Lineage" and "What a change to `orders.jsonl` affects".
- The page, just before the prediction: "The drawing has 3 parts: - `orders.jsonl` to `sales_dashboard` through three jobs; ...". The drawing's label says the same.
- Then: "Before you read on, write which assets a change to `orders.jsonl` affects".
- The caption and prose give the answer away just before the prediction. CLAUDE.md names this ("including one just below a prediction").
- `products.csv, which no job reads` is stated twice before its walk, so that walk is not a prediction either.
- Direction: keep the lists of parts out of the prose and out of the label. Have the drawing carry them, with a neutral label. Or move the prediction before the drawing. Then ask something the drawing does not read off, for example the effect of Jo's wrong line, or of a second input.

**3. "The records cell holds Chapter 5's records" is not true. Blocking.**
- Where: the text above the records cell, and the model cell.
- The page: "The records cell holds Chapter 5's records, with one line for each of the two files that no line described...". The model cell "adds a type, `job`, with two attributes".
- Chapter 5's records had `column ... means`, `column ... unit`, `dashboard sales_dashboard means` and the `person ... name` lines. Chapter 5's model had the matching `column means`, `column unit`, `dashboard means` and `person name`. All of these are gone from Chapter 6, and the line numbers shift.
- A reader who checks against Chapter 5 will find the claim false. The model cell's "adds" implies nothing was removed.
- Direction: say the records are a shortened version, and which lines were left out and why. Or keep them in.

**4. The page after Run all (before the dots are filled) contradicts its own hard-coded prose, and its explanation of what you will see is wrong. Blocking.**
- Where: the text above the records cell, then every result sentence below it.
- The page: "Until you do, the cells below show the dots: the check reports the two lines, and the walks stop at `clean_orders`."
- The upstream walk from `sales_dashboard` actually stops at `daily_sales`, not `clean_orders`.
- Other sentences are false as built:
  - "Downstream of `orders.jsonl` there are 6 nodes" sits under a 2-row result.
  - "Upstream of `sales_dashboard` there are 6 nodes. The farthest back is `orders.jsonl`" sits under a 2-row result.
  - "The drawing has 3 parts" is false. As built, `build_daily_sales` is a separate isolated node, so there are five parts.
  - "The comparison lists one row: Jo's line" sits under 5 rows.
  - "It finds 2 rows" sits under 4 rows.
- The dots lines are accepted silently. The records cell and the model cell show no error for `reads: ........` against `job reads: dataset`, so nothing tells the reader they are wrong.
- "The check" is a third name for the comparison. The page says "the check", "the comparison" and "compares". Use one.
- Direction: either make the result sentences conditional on the filled state, or stop the chapter being readable in the unfilled state. For example, have the records cell flag the dots, and say the numbers below are for the filled-in lines. Fix "stop at `clean_orders`".

**5. The drawing's arrow convention reverses Chapter 5's, and the printed paths read against the drawing. Blocking.**
- Where: "Lineage".
- Chapter 5 said "Each arrow points from a line's entity to the entity its value names". The edge for `job build_clean_orders reads: orders.jsonl` therefore goes job to asset. The printed path agrees: `orders.jsonl <-reads- build_clean_orders`.
- Chapter 6 says "An arrow from an asset to a job means the job reads it", the reverse for `reads`. The notes say the drawing is in the order data flows.
- The convention changes without being flagged. The path strings point against the drawn arrows for reads and with them for writes.
- Direction: say plainly that this drawing runs in the direction the data flows, unlike Chapter 5's. Explain in one sentence why the path notation `<-reads-` differs, or make the two agree.

**6. The bold definition of lineage is contradicted by the chapter's own result. Blocking.**
- Where: "Lineage".
- The page: "Records of what was made from what, and by which job, are **lineage**."
- The lines record what a job's code reads now, not what was made. The chapter then shows they say nothing about what was made on any night. The definition covers neither those lines (which are claims about today's code) nor Jo's belief.
- CLAUDE.md says a definition must hold for every case the course meets.
- Direction: define it as a record of which assets a job reads and writes, and so which assets derive from which. State that what the lines say is a claim about the job, not about a particular night, and leave the per-night record to Chapter 7.

**7. Jo's belief is arbitrary and answers itself. Blocking.**
- Where: "A line from a belief".
- The page: "Jo Marsh says that the daily sales job leaves out test customers, so it reads `clean_customers`. Jo has not read the code." Then "The comparison lists one row: Jo's line. ... nothing in it leaves out test customers."
- There are no test customers in `customers.jsonl` or `clean_customers`. The reader cannot judge the belief's plausibility. The sentence "nothing in it leaves out test customers" cannot be tested against any data.
- It connects to nothing from earlier. In Chapter 5, Jo wants orders with no customer id counted, so this belief seems to appear from nowhere.
- "Jo has not read the code" tells the reader the line is probably wrong before the comparison does.
- There is no question for the reader. This is not a prediction or a decision. The page states the dashboard "seems to depend" and then states the refutation.
- Direction: pick a belief grounded in something the reader has met. Candidates are the Chapter 2 gap, orders with no customer id, or customers with no email, which `clean_customers` drops. Ask the reader whether they would record the line and what would settle it. Drop "Jo has not read the code". Let the comparison be the evidence.

**8. The analyst's script is presented as existing today, and the later "Suppose" contradicts that. Minor.**
- Where: "The jobs' code" and "A line gone stale".
- The page: "Two things that write or read the shop's files are not in the repository: ... the analyst's copy of Chapter 2, a script on the analyst's laptop."
- In the default week there is no `shop-scratch` copy at all. It exists only in the `source` change, which the reader has not run at that point. Chapter 2 presented it as one of three optional changes. The script reads a warehouse table, not a file.
- "A line gone stale" then says "Suppose that from Saturday ... is changed to read the analyst's copy", which treats it as hypothetical.
- Direction: say the analyst may keep such a script, or introduce it where the change is made. Keep "reads the shop's files" accurate.

**9. The stale section partly gives its answers, and overstates what the data shows. Minor.**
- Where: "A line gone stale".
- The prediction's second question is "Will the rows of daily_sales change?" The text just above says "It holds the same rows."
- "The data shows no change. Only the code does." overstates. Only `daily_sales` rows were compared. In the changed week the storage listing gains `s3://shop-scratch/clean_orders_copy.csv`, which the default week does not have. That is a trace in the data, though it does not show what the job reads. The warehouse's `information_schema` and the dashboard are the same in the two weeks.
- Direction: say "the rows of `daily_sales` and the dashboard do not change", and let the reader notice what else the platform shows. Do not state the premise that decides the second answer in the sentence above it.

**10. The stated reading rule is wrong for two of the four jobs. Minor.**
- Where: the text above the code cell.
- The page: "`read("...")` reads a file from object storage, a table after `FROM` is read from the warehouse".
- In `build_clean_orders` and `build_clean_customers`, `FROM raw_orders` and `FROM raw_customers` name the variable that `read` assigned, not a warehouse table.
- The reader is not told this, so the cell they fill in is easy but the rule is wrong. The code also shows `append=True, day=yesterday` and `LOWER(...)` without comment.
- Direction: state that a `FROM` name set by `read` stands for that file. Say that `append=True, day=yesterday` can be ignored for reads and writes.

**11. The "code shows only now" point is made five times. Minor.**
- Where: the opening, the end of "A line gone stale", the third bullet of the four readings, "Before Chapter 7" and the third closing question.
- The opening, "The code says what each job does now. It does not say when a job did its work, or what it did on any night", gives away the stale experiment's finding before the reader has run it.
- The third closing question ("Which nights did the job read `clean_orders`, ...? What would you need in order to find out?") carries an answer already given in the text above it.
- Direction: keep it once, after the experiment. Cut the opening sentence. Make the last question new.

**12. `app_title` is a copy of Chapter 5's. Minor.**
- Where: `notebook/chapter_06.py` line 8, `app_title="Metadata as a graph"`.
- This appears in the browser tab and anywhere the app title is shown. It should name Chapter 6 ("What is lineage?").

**13. Terms are used before they are defined, or inconsistently. Minor.**
- "walks" appears in "the walks stop at `clean_orders`" before `downstream` and `upstream` are introduced. Chapter 5's term was "traversal". Chapter 6 never links `downstream` and `upstream` to it.
- The comparison is "the check", "the comparison" and "compares".
- "line" and "record" are both used for one thing, "your lines" and "Chapter 5's records".
- The definitions "What is made from an asset in this way is **downstream** of it" and "What an asset is made from in this way is **upstream** of it" cover jobs too, but jobs are not "made from" an asset.
- Direction: say once that these are traversals along `reads` and `writes`, and fix the wording.

**14. The last section has a few weaknesses. Minor.**
- Where: `## "Record the lineage of daily_sales."`.
- "The head of the shop's requirement is ..." appears without the head of the shop having said it anywhere earlier in the chapter.
- The fourth reading, "Which tables, or which columns, `daily_sales` is made from", combines two questions. The first is what the lines already answer.
- "Your lines meet the requirement as written, and agree with the code today." leaves out the first reading, the belief line.
- The section is a requirement exercise but the page does not mark the other readings against what each needs.
- Direction: introduce the requirement with its situation. Split tables from columns. Say which readings the lines satisfy.

**15. The repository appears from nowhere. Minor.**
- Where: "The jobs' code".
- The page: "The head of the shop gives you access to the repository where the last engineer kept the jobs' code."
- Chapter 1 said "nothing about it is written down" and that you cannot see the jobs. The page gives no reason for the repository appearing now.
- Direction: one clause saying what changed, or that the head of the shop found it.

**16. Smaller points. Minor.**
- The page shows a placeholder in the "after the edit" build. The warning box reads `WARNING TO BE MEASURED` and has no "Time and memory" details. The source and "as built" files are fine. If this is the shipped build, it is a bug. If it is only the review copy, ignore it.
- Timings: the warning says "9 to 12 seconds, ... about 420 MB". The notes' "Measured" section says "Run all 8.0 to 9.3 s; peak memory 398 to 418 MB". The 9 to 12 range is not what was measured. I cannot check the published page.
- Objective 4, "Find what happens to such lines when a job's code changes", reads as if the lines are the belief lines. The stale section is about lines written from code.
- The fill-in step is a transcription of two values the code shows directly. The harder judgement (what counts as a read) is done for the reader in the other jobs. This is an observation, not a defect.
- `"Downstream ... nothing reads products.csv means only that the lines know of no reader"` is right. But the export writes files and does not read them, and the analyst's script reads `clean_orders`. The chapter never says that either could read `products.csv`. The caveat is stated in general terms.

## Checked and fine

- The 6-node counts are right for the filled-in state: downstream of `orders.jsonl` (3 jobs and 3 assets), upstream of `sales_dashboard`, and downstream of `customers.jsonl` with Jo's line.
- "The drawing has 3 parts" is right for the filled-in state.
- The "2 rows" and "1 row" comparison counts are right for the filled-in state.
- `True` for the `daily_sales` rows: the two weeks' `daily_sales`, `information_schema` and dashboard are equal.
- Chapter 2's third question and the "Does anything still read it?" quotation are accurate.
- Chapter 5's closing promise ("Chapter 6 gives you the jobs' code and records what each job reads and writes") is kept.
- The writing is plain, with no em dashes and no "lab" language.

## What I read, and what I could not check

I read:
- the brief;
- `chapter_06-as-built.md` and `chapter_06-after-the-edit.md` (with a diff between them);
- `chapter_05-as-built.md`;
- Chapter 2 and Chapter 1 as they stand after review (round 17);
- `notebook/chapter_06.py`;
- `docs/notes/chapter-06.md`;
- the plan's Chapter 5/6 decisions;
- `shop/graph.py` and `shop/week.py`.

I also ran the engine to check the unfilled-dots graph, the default and `source` weeks' storage listings, the warehouse tables and dashboard in both weeks, and the customer data.

I could not check:
- the drawings, which appear only as labels, so the arrow direction and the isolated-node claim in findings 4 and 5 rest on the code and the prose and not on the pictures;
- the platform figure, the hidden cells and phone widths;
- Chapters 3 and 4, which I did not read, so the Chapter 5 records I compared are Chapter 5's own;
- the wording of `docs/prompts/review-learner-facing-prose.md` and `AGENTS.md`, which I did not open;
- the published page's measured run time and memory.
