# Round 22 review: findings (reviewer on another model, recorded here as returned)

1. Failed night: "Each record is normal on its own. The gap shows only when you compare the
   last-altered times.", the figure's "after a failed night, each record looks normal", and the
   closing "left a failed night looking like a normal one" contradict the same paragraph's 6 rows,
   none for Sunday, and the dashboard's 6 values (engine: row_count 6 against 7). The real limit is
   that nothing records that a write was due and failed.
2. "somebody has to record those, and the second and third have to be recorded when the thing
   happens": "second and third" is hard to resolve, and wrong for "what it was made from", which
   Chapter 6 reads from the jobs' code. The definition lumps three kinds of record into one list.
3. The cleaning rules are asserted ("In the shop's design, `clean_orders` is made from
   `orders.jsonl` by four rules") before the count, so nothing is left to discover; "Your guess for
   `clean_orders` from Chapter 1 meets the same limit" never names the limit.
4. The owner table marks "which account controls it in the warehouse" "yes" though the closing note
   says the shop records "no such rights"; "looks like an account a program logs in as" sits
   against "no: it names an account, not a program"; "you did nothing to meet it" is unclear.
5. "a system records what its own work needs and nothing more" is contradicted by the owner,
   created times and `created_by` `j.marsh`; "The questions you want answered are not its work"
   has no clear referent.
6. Tuesday's, Wednesday's and Saturday's gaps (7009, 7037, the second 7015; 2999, 2400, 4500 pence,
   all correct) are asserted with no cell that shows them; "also" has no antecedent; five
   one-sentence paragraphs.
7. The first figure of stage 1 gives the gap (£154.00, 15400 pence) under the heading with no
   question first, and duplicates the dashboard, the sentence and the later box.
8. "The shop has no refunds" rests on a fact the page has not shown; "Saturday, 2026-09-12" is the
   only ISO date in the prose.
9. The check: C is the longest and lists six fields; "They have three pieces of evidence" reads as
   if the engineer holds all three; B says "dashboard's current totals" where the chapter's query
   reproduces `daily_sales`; the answers open in any order, so the reader can open C first; two
   sections restating the takeaway follow it.
10. The same conclusion in at least five places ("None of the three systems records how an asset
    came to be as it is.", "Nothing: no system records this link.", "The platform's state answers
    what exists."); the future records described three times (the figure, the paragraph after it,
    "Before Chapter 3").
11. The hypothesis bullet "On Thursday, `daily_sales` agrees with `clean_orders`, not with
    `orders.jsonl`: it is short by exactly the three orders..." states the test's result before the
    test, and mixes "agrees" and "short".
12. Stage 2's box restates the printed cells field by field; the bytes, created time and types are
    never used again.
13. The warning's time-and-memory details interrupt the story before the reader has a reason to
    care.
14. "Questions the platform cannot answer" states the conclusion early; two questions
    (`products.csv`, the renamed column) are not returned to in this chapter; the numbered list at
    the top repeats the stage headings.
15. "Compare it with the guess you wrote at the end of Chapter 1" names only `daily_sales`, though
    Chapter 1 asked about three tables.
