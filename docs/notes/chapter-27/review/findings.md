REVIEW OF CHAPTER 27, "Build the query layer"

Numbers checked: I ran Python from `/home/user/metadata-systems/notebook` on `shop.run_week(["returns","source","failed"])`. The numbers are 1 of 3 and 3 of 3 for `downstream`, the 4 assets downstream of `orders.jsonl`, the 17 edges, the stale list, the failed run, `owners()` for every asset, the freshness rows, and the check output for six wrong `downstream` attempts and several wrong `owner` attempts. I also checked the cross-references against `chapter_02`, `04`, `05`, `06`, `13`, `14`, `15`, `16`, `21`, `23`, `26` and `28`, `docs/plan.md` and `docs/notes/part-6/design.md`. I read the as-built file, `chapter_27.py`, `shop/query.py`, `shop/observe.py` and `shop/lineage_graph.py`. I did not run the browser checks (phone width, dark theme), so the phone comments below come from the printed table styling, not a viewport run.

## BLOCKING

**1. "The requirement as written is met by any of them" is false for "each asset".**
- Quote: "The requirement as written is met by any of them."
- The requirement is "must answer who owns each asset". `shop.query.owners(a)` gives these results:
  - `orders.jsonl`, `clean_orders_copy.csv`: no owner under any meaning.
  - `clean_orders`, `clean_customers`, `returns`: `account` only.
  - `sales_dashboard`: `responsible` only.
  - `products.csv`: `responsible` (`s.lund`) only.
  - `daily_sales`: all three.
  - `team` exists for `daily_sales` alone.
- So no meaning meets "each asset" as written. The account meets "every table" in Chapter 2 only because the warehouse records one for every table.
- `check_owner` calls `owner("daily_sales")` only. The page's own claim that any reading passes therefore rests on one asset.
- The "Question the requirement" step 5 (does the record meet the requirement, as written and as meant) is skipped, and the sentence misleads.
- Direction: have the check or a following cell run the learner's `owner` over the shop's assets and show which assets each meaning covers. Then state coverage per meaning, not "any of them".
- A related line is "The shop holds three answers, each from its own source". For every asset except `daily_sales` it holds fewer.

**2. Wrong cross-references in the opening.**
- Quote: "Since Part III, the shop's pages have answered questions about its assets: what depends on an asset (Chapter 14), where it came from (Chapter 15), who owns it (Chapters 2, 4 and 21), how recent it is (Chapter 13) ..."
- Chapter 14 is "Data quality as metadata" (`docs/plan.md`, `chapter_14.py`). Dependency and downstream queries are Chapter 6 (`lineage.downstream`) and Chapter 16 (`shop.impact.downstream`).
- "Since Part III" contradicts the same sentence's Chapters 2, 4 and 6, which are Parts I and II. Part III is Chapters 10 to 13.
- Chapter 15 (provenance), Chapter 13 and Chapter 16 are correct.
- `docs/notes/part-6/design.md` repeats the error: "downstream of `orders.jsonl` is Chapter 14's set".
- A related reference is "as Chapter 5's traversal did". It is defensible, but Chapter 6's `downstream` and Chapter 16's are closer: they follow job-to-asset edges.

**3. "Over the same graph" is false for three of the four answers.**
- Quotes: "Read the shop's answers to the other questions over the same graph and the same week." and "Here the same questions are asked of the lineage graph that Chapter 26 built".
- In `query.answers`, only "where did `daily_sales` come from?" reads the graph, through `upstream(g, ...)`.
- Stale assets come from `observe.freshness(week)`, which reads each asset's own store clock.
- Failed runs come from `objects(normalise(week_events(week)))`.
- Column reach comes from `impact.downstream_columns(week, ...)`, which is Chapter 10's column lineage.
- A learner will reasonably conclude that their graph answers "which assets are stale". It does not, and the graph has no write times or latest-day data to answer it from.
- Direction: say which questions the graph answers and which read the week's other records. Alternatively, drop "over the same graph" from the objective and the opening.

## SHOULD

**4. The chapter's surprising result is told, not found, and its numbers have no cell.**
- Quote: "`sales_dashboard` is not among them: it was last written at 03:00:09 on Monday 14, 6 hours before. Its latest day is Saturday 12, the same as `daily_sales`'s".
- No cell prints 03:00:09, "6 hours" or the latest day. The `answers` table shows only names.
- Objective 3 is "Find an asset that is recent by when it was written and old by what it shows." The learner is handed the finding in prose.
- `observe.freshness(week)` already has `last written`, `hours before` and `latest day`. Showing it before the prose would let the learner find the discrepancy.
- "6 hours before" should say before 09:00. The true figure is 5 h 59 m 51 s, rounded.

**5. The stale prediction is nearly given away, and the follow-up text is misplaced.**
- Quotes: "`refresh_dashboard` ran after it and redrew the dashboard (Chapter 13)." and "Before you read on, write in the next cell whether that query will list `sales_dashboard`."
- The query is defined as "last written", and the sentence before the prediction says the dashboard was redrawn on Monday. The answer follows from those two sentences. The belief a learner might hold is "the dashboard shows old data, so it is stale". The setup text settles that before they commit.
- "Compare this with what you wrote." sits between two groups of bullets. The bullets after it (failed run, column reach) are not things the learner predicted.
- The bullets restate the answers table row by row: "`daily_sales` came from ...", "The failed run is ...", "A change to `clean_orders.customer_id` reaches ...". The learner would not miss them.
- The `answers` table shows four answers, but only the dashboard question has anything in front of it. Failed run and column reach are shown with no question for the learner.

**6. The owner step does not frame the readings as questions, and one claim is unsupported.**
- Quote: "each answers a different question. The next cell lists them:" followed by a bulleted list of sources.
- The bullets name sources (account, person, team sheet), not the questions a reading of "owner" could ask (who do I ask; which team; which account controls the table). Chapter 26's "now" step does this.
- "The next cell lists them" is followed by a prose list, then instructions, then the actual `owners("daily_sales")` cell. The cell repeats the bullets. "The cell after the list" is ambiguous.
- Quote: "needs `responsible`, or a team that still exists." Nothing in Chapters 2, 4 or 21 says the data team stops existing. Chapter 21 says the sheet is unedited since 28 August. "Still exists" is unsupported and may confuse. It also leans toward marking one reading as the right one.
- Two closing lines repeat each other: "The requirement as written is met by any of them." and "The requirement does not say which meaning it wants." The last line is a slogan.
- "A query that names its meaning lets whoever reads the answer tell which question it answered." is fine as a single statement.

**7. "Every asset" in the stale-asset query overstates it.**
- Quote: "lists every asset last written more than 24 hours before 09:00 on Monday 14."
- `observe.freshness` covers a fixed list of five assets (`orders.jsonl`, `clean_orders`, `daily_sales`, `sales_dashboard`, `returns`). It does not cover the copy, `customers.jsonl`, `products.csv` or `clean_customers`.
- `returns` is listed as stale with no comment, although Chapter 13 made the point that a nightly threshold does not describe a table written at any hour. The "How this differs" note says only that "The 24 hours ... are the shop's choice."

**8. What the learner writes and what the check prints.**
- The page says what to change in words ("follows `next_assets` from each asset it finds, until no new asset turns up") and gives no code. That is good, and the cells are the right size for a phone: 2 lines in the stub, 8 in the reference.
- The page never says what `downstream` returns: asset names, each once, not including the start asset.
- Wrong attempts and their check lines, which I ran:
  - **Recursion with no visited set** gives "daily_sales, daily_sales, sales_dashboard, sales_dashboard". The reader sees duplicates but is not told to look for them.
  - **Including the start asset** gives "returns. Expected none." and "orders.jsonl" in the list. This one is readable.
  - **Returning `None`** gives a raw `TypeError: 'NoneType' object is not iterable`.
  - **Returning a single string** gives an `IndexError` from the attempt itself, not from the check.
  - **`owner` returning a bare string** gives `AttributeError: 'str' object has no attribute 'get'`.
- Direction: state the return value. Catch a non-collection and a non-dict in the check and say what was expected.
- The check table uses `white-space:nowrap`. The "Expected ..." part of a failing line is about 110 characters and is the part that tells the reader what to look at. On a 360 px phone it sits behind a horizontal scroll. Please check this in the browser.

**9. "The shop's version" is never explained.**
- Quote: "the lineage graph that Chapter 26 built: the shop's version."
- A notebook cannot read another notebook's cells. The design note says each chapter states once that it uses the engine's reference pieces. Here the phrase is bare. The learner who wrote `add` in Chapter 26 is not told why their graph is not used. The engine builds it from `lineage_graph.REFERENCE["add"]`.

**10. The model-versus-reality notes miss two things.**
- The 17 edges appear in no cell. I confirmed `len(graph)` is 17.
- Quote: "Chapter 23 projected what such questions read at 10,000,000 assets." Chapter 23 says the traversal followed to the end is the one that passes the limit at 10,000,000 assets, and one limited to 4 steps never does. The learner's `downstream` is the unbounded one. The note should say so.
- Chapter 26's edges carry first and last times and the three readings of "now". `downstream` ignores them: "From Sunday 13, the analyst's copy is an input to `build_daily_sales`", yet the downstream of `orders.jsonl` includes the copy's path at all times. The page does not say that the traversal answers for the whole week.

**11. Engine issue behind the owner step.**
- `query.owners` takes `ACCOUNT = "etl_service"` and `RESPONSIBLE = {...}` from constants. Only `team` is read from `claims`. Its docstring says "Each meaning's owner ... from its own source".
- `RESPONSIBLE` gives `products.csv` as `s.lund`, but Chapter 4's records (pinned in `test_words.py`) hold "Sam Lund", "Jo Marsh" and `j.marsh` as distinct strings.
- Chapter 28 shows `owners` for each asset, so the inconsistency will surface there. CLAUDE.md requires every figure to be computed from the shop.

## COULD

- **"The head of the shop's requirement: ..."** is a fragment, and the head of the shop is a person. The same phrase opens the box in Chapters 24 to 28, so this is part-wide. It matches Chapter 4's "The head of the shop's requirement is ...", which is a full sentence.
- **Heading "The other questions"** names the cell's position, not its subject. Something like stale assets, failed runs and column reach says what the section contains.
- **Closing summary: "The owner query passed only when it said which meaning it gave."** It omits the fact that matters, which is that any meaning passed. It also calls the check's result "the owner query".
- **Reflective question: "Which of your metadata system's answers say which question they answer?"** reads awkwardly. The other two questions are good.
- **"A query that asks when an asset was last written cannot see that the dashboard shows old data"** personifies the query slightly. It could say what the query does not hold: the dashboard's latest day.
- **The map caption** says "three return files" for the `["returns"]` week, while the chapter's week is `["returns","source","failed"]`. The caption is the same as Chapter 13's, so this is low priority.
- **The prediction cells** assign to unused variables, and the page never shows the learner's own text back at "Compare this with what you wrote." The pattern is shared across Part VI.

Beyond the four areas above, I found no unsupported OpenLineage or product claim: the chapter makes none.
