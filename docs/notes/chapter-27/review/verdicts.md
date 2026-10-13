# VERDICTS ON THE CHAPTER 27 FINDINGS

Count: 5 upheld, 6 partly upheld, 1 rejected, plus 7 COULD items (3 upheld, 1 partly upheld, 3 rejected).

I read `notebook/chapter_27.py`, `notebook/shop/query.py`, `observe.py`, `interface.py`, `docs/notes/chapter-27.md`, `docs/notes/part-6/design.md`, and the cited cells of Chapters 4, 13, 21, 23, 26 and 28. I ran `shop.query.owners` over nine assets, `observe.freshness`, `query.answers`, `len(query.graph(week))` and `check_downstream` with two wrong attempts.

## BLOCKING

**1. "Met by any of them" is false for "each asset": UPHELD.**
- Verified with `owners()`:
  - `orders.jsonl`, `clean_orders_copy.csv` and `customers.jsonl`: all three meanings are None.
  - `clean_orders`, `clean_customers` and `returns`: account only.
  - `sales_dashboard` and `products.csv`: responsible only.
  - `daily_sales`: all three.
- `check_owner` tests `daily_sales` alone, so the page's claim rests on one asset.
- Chapter 4 (line 94) records "the data engineer" as responsible for `clean_orders` and `clean_customers`. `RESPONSIBLE` omits both, so the true coverage is wider than the engine says (see 11).
- The fix must achieve three things:
  - Correct the sentence so it no longer claims any meaning covers each asset.
  - Show, from the engine (a Rows over the shop's assets, after the learner's check), which assets each meaning has an owner for. This supplies step 5 of "Question the requirement".
  - Scope "The shop holds three answers" to `daily_sales`.
- Do not state the coverage in prose before that table. Pin the table's numbers in a test.
- Sequence: fix the engine data (11) first, so the table does not understate `responsible`.

**2. Wrong cross-references: UPHELD.**
- Chapter 14 is "Data quality as metadata". Downstream is introduced in Chapter 6 (`lineage.downstream`) and followed in Chapter 16 (line 117).
- "Since Part III" is wrong: Chapters 2, 4 and 6 are Parts I and II, and Part III is Chapters 10 to 13.
- Chapters 13, 15 and 16 are right.
- "As Chapter 5's traversal did" is defensible (Chapter 5 introduces traversal) but Chapter 6's `downstream` is closer. Name Chapter 6.
- `design.md` repeats "Chapter 14's set". Fix that in the note too.

**3. "Over the same graph": UPHELD.**
- In `query.answers`, only the upstream question reads the graph.
- Stale assets come from `observe.freshness`, failed runs from the normalised week events, and column reach from `impact.downstream_columns`.
- The fix must make the objective and the opening say which questions the graph answers and which read the week's other records.
- The notes' sentence "reads ... over the same graph" needs the same correction.

## SHOULD

**4. The surprising result is told, not found: PARTLY UPHELD.**
- Stands: no cell prints 03:00:09, the latest day or the hours. `answers` shows names only, and I confirmed this. `observe.freshness(week27)` already holds all three fields (last written 03:00:09, 6.0 hours, latest day 2026-09-12). Show that table before the prose that interprets it, so objective 3 is found rather than handed over.
- Does not stand: the rounding objection. The table prints 6.0 and Chapter 13 uses the same one-decimal convention.
- Say "before 09:00" in the prose, so "6 hours before" has a reference.

**5. Prediction nearly given away and misplaced follow-up: PARTLY UPHELD.**
- Stands:
  - "`refresh_dashboard` ran after it and redrew the dashboard" sits before the prediction and, with the query's definition, settles the answer. The notes call the prediction "predictable from Chapter 13", so the redraw belongs in the result, not the setup.
  - "Compare this with what you wrote." sits mid-list, between the stale bullets and the failed-run and column-reach bullets, which were not predicted. Move it so it follows only the stale result.
  - Bullets 1, 3 and 4 restate `answers` rows. Cut them; keep only what adds to the table (the dashboard's time and latest day).
- Rejected: the complaint that the failed-run and column-reach answers have no learner question. Design.md says the other questions are "shown answering". Cheaper to leave them in the table than to invent questions.

**6. Owner step framing: PARTLY UPHELD.**
- Stands:
  - The bullets name sources, not the questions. Chapter 21 line 262 already frames them as questions: a person responsible, a team, the account the warehouse records. Chapter 26 does the same with "now". Frame each reading as the question it answers, with what it needs, as in "Question the requirement".
  - "The cell after the list holds it" is wrong. The next cell after the list is `owners("daily_sales")`; the `owner` stub is the one after. Reword.
  - "A team that still exists" is unsupported. Chapter 21 says only that the sheet is unedited since 28 August. Remove it.
- The doubled closing sentences ("The requirement as written is met by any of them" and "The requirement does not say which meaning it wants") resolve themselves once 1 is fixed. Keep the final sentence once, as Chapter 26 does.

**7. "Every asset" in the stale query: PARTLY UPHELD.**
- Stands: `observe.freshness` covers a fixed set (`orders.jsonl`, `clean_orders`, `daily_sales`, `sales_dashboard`, plus `returns` when the week has it). It omits the copy, `customers.jsonl`, `products.csv` and `clean_customers`. Reword to the assets the shop measures.
- Rejected: asking for a comment that `returns` is "stale". Chapter 13 line 343 already makes that point, and a nightly threshold on a table written at any hour is not this chapter's question.

**8. Return value and check messages: PARTLY UPHELD.**
- Stands: the page never says what `downstream` returns. One sentence is enough: asset names, each once, without the start asset.
- I confirmed the duplicate-output case prints readably ("daily_sales, daily_sales ... Expected ...").
- Rejected: catching `None`, a bare string or a non-dict in the checks. No other Part VI check catches the learner's exceptions (grep over collector, lineage_graph, store and interface), so a raw traceback is the part's convention. A tailored message per mistake costs more than it teaches.
- Rejected: the phone-width complaint. `white-space:nowrap` and the `ms-scroll` wrapper are the shared table styling in `platform.py`, used by every chapter, and the smoke test covers it.

**9. "The shop's version" unexplained: PARTLY UPHELD.**
- Chapter 26 line 78 already says its file has "the shop's own versions of your three pieces". Chapter 27's bare phrase does not.
- Add one sentence saying this page builds the graph with the shop's own version of Chapter 26's `add`, so the learner's cells there are not used.
- The reviewer's suggestion to name `lineage_graph.REFERENCE` is not needed. That is engine detail the learner never sees.

**10. Model-versus-reality notes: PARTLY UPHELD.**
- Stands (Chapter 23): lines 121 and 158 say the traversal followed to the end passes the limit at 10,000,000 assets, and one limited to 4 steps never does. The learner's `downstream` is the unbounded one. "Chapter 23 projected what such questions read" is vague. Say which.
- Stands (times): `downstream` ignores the edges' first and last times, so it answers for the whole week (for example, the copy's path appears whatever the date). Say so in one line.
- Rejected: "17 edges appear in no cell". `test_words` already pins 17 edges by job, and a model-versus-reality figure need not have a cell.

**11. Engine issue behind the owner step: PARTLY UPHELD.**
- Rejected: the `s.lund` versus "Sam Lund" inconsistency. Chapter 4 (lines 188, 204) establishes that the logins `j.marsh` and `s.lund` are identifiers for those people, so using logins is consistent.
- Stands: `RESPONSIBLE` is hard-coded and omits the two records Chapter 4 line 94 gives ("the data engineer" for `clean_orders` and `clean_customers`). The docstring claim "from its own source" is true only for `team`.
- Fix the data to match Chapter 4's records, or narrow the docstring and the page. Do it before 1, because Chapter 28's `owner` section and 1's coverage table both read `owners()`. Update any test that pins the old values.

## COULD

- **"The head of the shop's requirement:" fragment: REJECTED.** The identical opener is used in Chapters 24 to 28, and Chapter 4 uses a full sentence only at its own cell. A part-wide convention, not this chapter's fault.
- **Heading "The other questions": UPHELD (minor).** Rename it to a subject (stale assets, failed runs and column reach).
- **Closing summary on the owner query: UPHELD.** It will change with 1 anyway. State that the check passed for any of the three meanings, and that "the owner query" is the learner's `owner`.
- **Reflective question wording: REJECTED.** It is plain and grammatical.
- **"A query ... cannot see that the dashboard shows old data": UPHELD (minor).** Say what the query does not hold: the dashboard's latest day.
- **Map caption "three return files": REJECTED.** The figure draws `run_week(["returns"])`, so the caption matches its figure, and it is the same as Chapter 13's.
- **Prediction cells assign to unused variables: REJECTED.** Shared across Part VI.

## Process note

The notes block `answers` also claims "reads ... over the same week". Update the notes when 3 is fixed, and add the coverage table to the `owners` figure block, with its Requirements paragraph, when 1 is done.
