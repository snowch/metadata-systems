# Review of Chapter 10, "Column-level lineage"

I found no blocking fault. The numbers and the OpenLineage claims hold, apart from one overstatement under finding 8. The weaknesses are in how much the learner does, in four terms that mean two things each, and in a few claims the page does not support.

## SHOULD

**1. The `net` experiment never shows that `daily_sales` depends on `returns`.**
- Where: "No order of Saturday or Sunday was returned, so the rows are the same." and "13 columns. None is in `returns`."
- Problem: The week's rows are identical with and without the function. I checked: the `net` and `returns` weeks give the same seven rows. The learner takes the page's word that the function matters. The prediction ("whether the parser's answer for `revenue_pence` will include the table `returns`, and why") tests only what the shop's own parser prints. CLAUDE.md asks for independent evidence the learner could check.
- Problem, also: The prose above the prediction says the function "reads the table `returns`". That nearly gives the answer to anyone who has just read that the parser reads SQL.
- Direction: Give the learner something observable. For example, a return of a Saturday order that changes the row, so the missing record is a gap they can see. Or reframe the prediction around a belief they can test.

**2. The `source` answer describes Monday's code, not how the rows were made.**
- Where: "The next cell follows `revenue_pence` back in the week with the `source` change: 15 columns, through the copy (4), then `clean_orders` (4), to `orders.jsonl` (7)." Also "The catalogue gives the columns of `clean_orders` as they are on Monday."
- Problem: Only the catalogue is dated. The code is just as dated. In that week `build_daily_sales` read the copy for 2 of the 7 rows and `clean_orders` directly for 5 (Chapter 9: "reads `clean_orders` in 5 runs"). Chapters 6, 7 and 9 spent effort on "the code shows only what the job does now". This table silently repeats that limit and implies all revenue went through the copy.
- Direction: Say the answer is for the code as it stands, and tie it to Chapter 9's "current".

**3. "the catalogue" is used without being introduced, and clashes with Chapters 3 and 4.**
- Where: "To name them, the parser needs the columns of `daily_sales`, from the catalogue." and the line `# catalogue = warehouse`.
- Problem: Chapter 2 calls the warehouse's record `information_schema`. Chapters 3 and 4 use "catalogue" for Sam Lund's product catalogue ("Sam Lund keeps the product catalogue"). Chapter 10 never says that "the catalogue" here means the warehouse's record of its tables and columns. The common brief assumes it is defined; the page does not define it. The chapter's central edit rests on it.
- Direction: Name and define it once, where it first appears, and tie it to `information_schema`.

**4. Four words mean two things each on this page.**
- "computed". `how` has a value `computed`. The prose also says "the columns its value is computed from" for all of `copied`, `computed` and `aggregated`, and "`revenue_pence` is computed from 2 columns" while its `how` is `aggregated`. The reader sees `computed` only on `day`.
- "function". The page uses "function" for the SQL function `returned_quantity`. Chapter 9 and the map caption use it for the returns desk's two functions ("the four jobs and the two functions"). "The developer added a function to the warehouse" does not say it is a different thing.
- "reading". The objective says "by reading the programs' SQL" (an act). The body says "two readings" (an interpretation).
- "parser". Chapter 9's "Parse" stage reads event lines. This chapter's "shop's parser" reads SQL. The page never says they are different, and it first names the parser with no introduction.
- Direction: Use another verb for the generic "made from". Say what kind of function it is. Separate the act from the interpretation. Name the SQL parser as new.

**5. The page's definition of "column lineage" does not cover the second kind it then records.**
- Where: "Lineage between columns, which columns each column is made from, is **column lineage**."
- Problem: Filter and grouping columns are not "made from". The chapter then treats both kinds as column lineage.

**6. The second reading's answer ("all 7") separates nothing.**
- Where: "All 7 decide which rows count. `build_clean_orders` keeps one row of each set of equal rows (`distinct`), so every column takes part"
- Problem: DISTINCT puts every input column in the answer, so the second reading returns the whole file. The closing verdict picks out only `customer_id` ("The first reading leaves out `customer_id`"). It does not say that the first reading also leaves out `order_id`, `status` and `ordered_at`.
- Problem, also: The page does not mention that `quantity > 0` removed no row this week (Chapter 2), so its inclusion rests on code and not on data.
- Direction: Say what "all 7" means for the requirement, or show which of the 7 changed rows this week.
- Related wording: "Each of the week's three oddities reached the revenue through a column that decides which rows count". Chapter 2 never uses "oddities". It lists four rules, and a cancelled order is not an anomaly there. "Reached" is loose.

**7. The interaction is thin, and the notes overclaim.**
- Where: the only action beyond reading is "delete the `# ` at the start of the line `# catalogue = warehouse`".
- Problem: The result is told first: "Then the parser names them `day` and `revenue_pence`." The notes call this an experiment and say "Gives nothing away: the cell's output shows the unnamed columns; the prose explains them". That is false, since the prose gives the answer beforehand.
- Problem: The learner never gives the parser SQL of their own. No edit to a WHERE, SELECT or catalogue shows the lineage changing.
- Problem: Neither prediction is returned to. "Before you read on, write in the next cell…" is never followed by a comparison with what the learner wrote. The experiments are therefore "commit, run, compare" in name only.
- Direction: Let the learner change a query and re-run the parser. Make the catalogue edit something they predict before the prose tells them. Close the loop on what they wrote.

**8. The first prediction is mostly answered by Chapter 9's last page.**
- Where: Chapter 9 ends: "Chapter 6 noted that `revenue_pence` is made from `price_pence` and `quantity`". Chapter 10 then asks "which columns of `orders.jsonl` you expect `revenue_pence` to depend on, and why".
- Problem: A learner writes `price_pence` and `quantity` from memory and is right under reading 1. Nothing contradicts them. The experiment's surprise rests on the learner also writing more, and nothing prompts that.
- Direction: Ask something that Chapter 9's last page did not answer.

**9. The `SELECT *` section is an instrument with no question in front of it.**
- Where: "The next cell gives that code to the parser without the catalogue; the cell after it, with it."
- Problem: The learner reads two tables and a stated limit: "A record made from Monday's catalogue does not say which columns an earlier run copied, if they were different then." The limit is asserted, not felt. The shop has no change that alters `clean_orders`' columns. Chapter 11 changes `orders.jsonl`, and `build_clean_orders` lists its columns explicitly. "Chapter 11 changes a dataset's columns" therefore does not follow up this case.
- Direction: Put a question first, or let the learner see the record go wrong.

**10. The facet section has no problem in front of it, and two claims are loose.**
- No problem is posed. The section opens "OpenLineage defines a facet for column lineage". CLAUDE.md asks for the problem first and the standard second.
- "Each input carries a transformation `type`". In the specification `transformations` is optional. `type` is required only inside a transformation (`docs/sources.md`, "Read for Part III"). That is a spec claim overstated.
- "so a program that receives it can answer either reading of the requirement". This is true for one program only. The facet for `daily_sales` names `clean_orders`' columns and cannot go back to `orders.jsonl`. The earlier text separated that scope: "or go back through every program".
- The reality note says "The shop writes it as `INDIRECT` with no subtype". The facet printed on the page has no DISTINCT in it, so the note refers to something the learner never saw. The code also adds a `description: "SELECT DISTINCT"`.

**11. The "Time and memory" box states measurements nobody made for Chapter 10.**
- Where: "less than 1 MB when opened from Chapter 9's link… (measured on a computer)", "9 to 12 seconds", "about 410 MB".
- Problem: These are copied from Chapter 9. `docs/notes/chapter-10.md` says "Measured: See `docs/notes/notebook-prototype.md`, 'Chapters 10 to 13'". No such section exists. The prototype notes stop at Chapter 9.
- Direction: Measure it or soften the claim.

**12. No figure carries the chapter's graph.**
- The chapter derives a column graph through three or four programs, in tables only. Chapter 9 ended with a drawing.
- The learner has to hold the chain `orders.jsonl`, `clean_orders`, the copy, `daily_sales` in their head. They must also hold which program decides which rows.
- The one figure is the standing map, which cannot carry any of it.
- `build_clean_orders`' code (DISTINCT, `customer_id IS NOT NULL AND quantity > 0`) is the basis of the headline finding and is not printed. The page only restates it.
- Direction: Add a figure computed from the parser's result, or print that program's code.

## COULD

- **"the shop's developer".** The phrase is new and close to Chapter 6's "checkout's developer". "The developer added a function" then leaves it unclear whether the checkout or the shop wrote it.
- **"Jo Marsh is checking the checkout's data".** This gives no clear reason for the question.
- **Personification and vague phrases:**
  - "A function hid the table it reads" and "See what a function in a query hides": the parser cannot read inside the function.
  - "The shop's parser records both kinds": it derives them from code and stores nothing.
  - "`*` names no column, and the parser does not guess one."
  - "Either reading can stop at the program…"
  - "the column behind Thursday's low revenue."
  - The closing "It could not show what happens…": "It" has no clear referent.
- **"A record that the function reads `returns` has to come from somewhere other than the query: from whoever wrote the function, or from the warehouse as the query runs."**
  - The claim is overbroad: a function's body can sometimes be read.
  - It is unsupported in `docs/sources.md`.
  - It sits against the reality note "The shop's warehouse keeps no record of which columns a query read while it ran."
- **The `WITH` clause.** It is added to the same example but gets no teaching role. The intermediate name `lines` is not visible in the printed answer.
- **Where the trace starts.** The objective says "the dashboard's revenue", but the trace starts at `daily_sales`. The dashboard hop works: `upstream(..., "sales_dashboard", "revenue_pence")` runs.
- **Fields and columns.** Jo says "fields of `orders.jsonl`", while the page says "columns" for a JSON-lines file. Chapter 11 draws the file/table distinction ("For a file, it records the fields").
- **"The head of the shop's requirement:".** The phrase is ambiguous in its grammar. It repeats Chapter 9's form.
- **Trailing blank lines.** The printed code is followed by blank lines.
- **The notes for the `select-star` and `the-facet` blocks.** They give a "Serves:" line but no question.

## Checked

I ran the engine for the plain, `source`, `net` and `returns` weeks.

**Numbers I confirmed:**
- The table shapes: `column 1` and `column 2` without the catalogue, `day` and `revenue_pence` with it.
- The `revenue_pence` rows listed in the bullets.
- 11 columns (4 + 7), 15 (4 + 4 + 7), 13.
- 7 rows for the copy with the catalogue.
- All 7 raw columns carrying a `rows` reason.
- The oddities in the data:
  - order 7015 duplicated on Wednesday 9 September;
  - orders 7021, 7023 and 7025 with no `customer_id` on Thursday;
  - the cancelled orders 7009 on Tuesday and 7037 on Saturday;
  - no `quantity <= 0`.
- The `net` week's rows equal the plain week's.
- The `net` week's `build_daily_sales` events name only `clean_orders` as input.
- The `net` code and the function's behaviour (`COALESCE(SUM(quantity), 0)` over `returns`).
- The `INSERT INTO … SELECT` position rule.
- The facet's content.
- No em dash and no "lab", "engine" or "simulator" in the page.
- Chapter 10's pinned numbers in `tests/test_words.py` (11, 15, the oddities). I did not run the suite.

**Sources:**
- The OpenLineage facts match `docs/sources.md`: `fields`/`dataset`, `DIRECT`/`INDIRECT` and the subtypes, no DISTINCT subtype, the Rust SQL parser listing `sqlite`.

**Requirement section:**
- It meets the five steps in outline, but its evidence for step 4 is the parser's output, not a stored record.

**Continuity:**
- Chapters 2, 3, 6, 9 and 11 were read for the points raised above.

**Not checked:**
- I did not run the built site or check phone widths.
- I did not run the full test suite.
