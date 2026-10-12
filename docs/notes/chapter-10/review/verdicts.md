Verdicts on the findings for Chapter 10, "Column-level lineage". I did not edit any file. I checked the page, the notes, `docs/plan.md`, `docs/sources.md`, `docs/lab.md`, Chapters 2, 6, 9 and 11, and the engine. I ran Python from /home/user/metadata-systems/notebook where noted.

**Summary:** upheld 2, 3, 5, 11. Partly upheld 1, 4, 6, 7, 9, 10, 12. Rejected 8.

**SHOULD**

**1. `net` never shows `daily_sales` depends on `returns`: PARTLY UPHELD.**
- Reject the second half. The sentence "It reads the table `returns`" states a fact the learner needs before predicting. Without it the prediction has no content.
- Uphold the first half. The week's rows are identical, so the dependency is invisible. The prediction is about what the shop's own parser prints, which is an implementation behaviour. The page never says beforehand that a parser cannot read a function's body.
- I ran the `net` week. `returned_quantity` returns 1 for orders 7004 and 7008, whose returns are in `returns`. A cell calling it on those orders makes the dependency observable.
- Reject the reviewer's suggestion of an engine change that returns a Saturday order. It is too costly.
- Fix: add one cell showing `returned_quantity` is non-zero for a returned order, so the learner can see `returns` matters. Keep the prediction.

**2. The `source` answer describes the code as it stands: UPHELD.**
- `programs()` holds one version of `build_daily_sales`, the one that reads the copy.
- The page says "from Saturday's row on" earlier. But "15 columns, through the copy (4)" then reads as the answer for all revenue.
- Chapter 9 says the job reads `clean_orders` in 5 runs and the copy in 2.
- Fix: one sentence saying the 15 columns are for the code as it stands, and that the earlier rows were written by code that read `clean_orders` directly.

**3. "the catalogue" is undefined: UPHELD.**
- `docs/notes/chapter-10/briefs/common.md` defines it as "the warehouse's record of its tables and columns". The page does not.
- Chapter 2 calls that record `information_schema`. Chapters 1, 3 and 4 use "catalogue" for Sam Lund's product catalogue.
- Chapter 11 reuses the bare term.
- Fix: define it once at "from the catalogue" as the warehouse's record of its tables' columns, Chapter 2's `information_schema`.

**4. Words that mean two things: PARTLY UPHELD.**
- "computed": upheld, and the clearest case. `how = computed` is only `day`. The prose says "computed from" for all `value` rows, including `revenue_pence`, whose `how` is `aggregated`.
- "function": upheld. The figure on this page is captioned "functions at any hour", the returns desk's functions from Chapter 9. The page's `returned_quantity` is a SQL function in the warehouse.
- "parser": upheld lightly. "the shop's parser" appears with a definite article and no introduction. Chapter 9's "parse" is an ingestion stage that reads event lines.
- "reading": rejected. The objective's act ("by reading the programs' SQL") and the "two readings" of the requirement do not collide in context. Chapter 9 already uses "reading" for requirement meanings.
- Fix:
  - Use "made from" for the generic relation and reserve `computed` for the `how` value.
  - Say "SQL function" or "warehouse function" at its introduction.
  - Introduce the parser in one clause as a program that reads SQL.

**5. The definition of "column lineage" omits the rows kind: UPHELD.**
- The page says "which columns each column is made from". It then records `filter`, `grouping` and `distinct` as column lineage too.
- CLAUDE.md says a definition must hold for every case the course meets.
- Fix: define it to cover both kinds, for example the columns each column is made from and the columns that decide which rows it has.

**6. "All 7" separates nothing: PARTLY UPHELD.**
- The mechanism is on the page: `distinct` makes every column take part. The verdict's pick of `customer_id` is the right hook. The first reading also leaves out `order_id`, `status`, `ordered_at` and `product_id`, but that follows from the lists above it.
- Chapter 2 says no quantity is 0 or less. That makes the `quantity > 0` filter code-only evidence, which the page does not claim otherwise. No fix is needed there.
- "three oddities" is genuinely a problem. The word appears in no other chapter and has no antecedent on the page. Chapter 2 lists four cleaning rules. "Reached the revenue through a column" is also loose.
- Fix: replace "oddities" with the three named cases, and say the first two were removed by `build_clean_orders` and the cancelled orders by the `status` filter. Optionally add one clause that `distinct` alone makes the second reading return every column.

**7. The interaction is thin and the notes overclaim: PARTLY UPHELD.**
- Reject "close the loop on what they wrote". The write-in cell with no return is the course's pattern in Chapters 6 and 9. The comparison happens against the next output.
- Reject "let the learner give the parser their own SQL" as a requirement. It widens the chapter and needs test changes, because `test_words` pins `SOURCE[10]`.
- Uphold that the page tells the result before the action: "Then the parser names them `day` and `revenue_pence`." The notes call `the-catalogue` an experiment and say "Gives nothing away", which is false.
- Fix: delete the pre-told sentence so the learner sees the names by running. Change the notes' role for `the-catalogue` to the truth, or keep it an experiment only after that deletion.

**8. The first prediction is answered by Chapter 9: REJECTED.**
- Chapter 9's last page does say `revenue_pence` is made from `price_pence` and `quantity`.
- That is the intended design. The notes say "a reader who writes `price_pence` and `quantity` commits to the first reading without knowing it". CLAUDE.md's "Question the requirement" says "the learner commits first… where a familiar word invites a quick answer".
- The surprise is the second reading. Prompting for more columns would give the answer away.

**9. The `SELECT *` section is an instrument with no question: PARTLY UPHELD.**
- Upheld: no question is posed before the two tables.
- Upheld on the limit: it is asserted, not felt.
- Chapter 11 says "Under every change, `clean_orders` has 1 version." So the closing "Chapter 11 changes a dataset's columns" misleads as a follow-up to this case.
- Fix: put one question before the cells, such as which columns of the copy the parser will name. Reword the limit as a limit that the shop's week does not show, and drop the pointer to Chapter 11.

**10. The facet section: PARTLY UPHELD.**
- "Each input carries a transformation `type`": upheld. `docs/sources.md` says `transformations` is optional and `type` is required only inside one. Fix: "An input can carry transformations, each with a `type`".
- "can answer either reading": upheld. It holds for this one program's facet only. Fix: add "for this program".
- The reality note on `DISTINCT`: upheld lightly. The printed facet has no `DISTINCT`. In the code the shop adds `description: "SELECT DISTINCT"`, which the note does not mention. Fix: either print `clean_orders`' facet or move or cut the note.
- No problem posed before the standard: low weight. Chapter 8 introduced facets. A one-line problem is cheap: the parser's answer is in a cell and a consumer has no parser.

**11. Measurements: UPHELD, being fixed.** The page copies figures from Chapter 9, and the notes point to a section that does not exist.

**12. No figure carries the graph: PARTLY UPHELD.**
- Reject a new column-graph figure. It needs new engine and figure work, which the plan does not include. The `upstream` table already groups rows by dataset, and the chain is only three datasets.
- Uphold printing the code of `build_clean_orders`. The headline claim, that `distinct` plus the `customer_id IS NOT NULL AND quantity > 0` filter decide which rows count, rests on code the page never shows. Chapter 6 printed it, but it is a chapter away.
- Fix: print `build_clean_orders`' code in the cell that runs `upstream`, or just before.

**COULD items, one line each**
- "the shop's developer": REJECTED. It distinguishes the shop's developer from "the checkout's developer".
- "Jo Marsh is checking the checkout's data": REJECTED. It continues Chapters 5 to 7.
- Personification and vague phrases:
  - UPHELD for "A function hid the table it reads" and "the parser does not guess one". Say what the SQL does not hold.
  - UPHELD for "It could not show…" (no clear referent).
  - REJECTED for "the column behind Thursday's low revenue" (Chapter 2 sets that up) and "Either reading can stop at the program…".
- The claim "A record… has to come from somewhere other than the query": UPHELD. It is overbroad and unsourced, because real warehouses can store a function's body. Scope it to the shop, whose function is a registered callable with no stored body.
- The `WITH` clause: REJECTED. The plan lists it (a name made inside the query), and the page says the parser followed `lines`.
- Where the trace starts: UPHELD as a one-word fix. The objective says "the dashboard's revenue" but the trace starts at `daily_sales`. I ran `upstream(w, "sales_dashboard", "revenue_pence", ...)` and it works and gives the same 11 columns. Either start from the dashboard or change the objective.
- Fields versus columns for a file: REJECTED. Chapter 11 draws that distinction.
- "The head of the shop's requirement:": REJECTED. It repeats Chapter 9's form.
- Trailing blank lines: REJECTED. It is the same `print(code)` pattern as in Chapters 6 and 9.
- Notes for `select-star` and `the-facet` without a question: UPHELD for the notes only. Add the question served, as Finding 9 asks.
