# Findings, round 17 (reviewer on another model; saved verbatim by the managing session)

Count: 1 high, 10 medium, 8 low. Numbers checked against the outputs by the reviewer: Thursday
20550 - 5150 = 15400; the days that match (Mon, Fri, Sun) and differ (Tue, Wed, Thu, Sat);
Saturday 21549 vs 19149 and £215.49 vs £191.49; the catalogue facts.

## High

1. Chapter 1's written guesses are never picked up. Chapter 1, "Your guesses about the warehouse
   tables": "write down which file or table you think it is made from ... Keep what you wrote.
   Chapter 2 asks what evidence like this can establish." Chapter 2 never mentions the guesses;
   "Reconstruction" covers `daily_sales` only, so two of the three guesses are never tested, and
   "Before Chapter 3" does not return to them. Direction: decide what Chapter 2 does with the
   guesses, or take the promise out of Chapter 1.

## Medium

2. "Reconstruction" narrates every result before the learner can reach it: "One does: read
   `clean_orders` ... It reproduces `daily_sales` exactly, all seven rows" comes before the cell,
   and three paragraphs give the three changes' numbers (21549 vs 19149, 6 rows) before the menu
   that produces them. The menu has no question before it and no "what did that prove?" after it.
   The columns `source | keep | measure | per | sql` and `fit="covers"` are not explained.
3. Thursday's explanation is asserted without an evidence cell: "three of Thursday's orders
   arrived with no customer id ... worth 15400 pence". No cell shows those orders; "since when?"
   is never answered; 15400 is the whole gap only if Thursday had no cancelled orders, which the
   page does not say; Tuesday (2999) and Wednesday (4500) are not explained.
4. The narrator states facts Chapter 1 says the learner cannot see: "the account that all four of
   the shop's jobs log in as" (Chapter 1 never counts the jobs), "The last rule is in the job", and
   "`daily_sales` is built from the completed orders in `clean_orders`, and the dashboard reads
   `daily_sales`". Also "a few rules" against "four cleaning rules". Mark them as the shop's design,
   or let a cell show them.
5. "Run below" is taught again, in "Thursday" and at the menu, though Chapter 1's box teaches it;
   Chapter 2's box omits Save, though the handover note is a text box a reload could lose.
6. The warning box: "Chapter 1's link opens this page in a new tab, and Chapter 1 stays open in its
   own tab" is not in Chapter 1 and the page does not say why it matters; the 40-word sentence on
   "opened from Chapter 1's link, in a browser that had opened Chapter 1" is convoluted.
7. Names in the code Chapter 1 did not introduce: `storage.records`, `files={"raw_orders": ...}`,
   `shop.run_week`, `shop.queries_that_rebuild`, `shop.cleaning_rules_that_fit(week)`, `change`,
   `changed`, `week`, `fit="covers"`, "bucket", "key", `information_schema`, mostly unexplained;
   `shop.` is the engine's package name (CLAUDE.md, "No lab on the page"). The closing note's
   "searching for queries" has no earlier hint that anything searched.
8. "catalogue" means two things: the shop's products and "checkout and catalogue" in Chapter 1,
   the warehouse's own record ("from its catalogue") in Chapter 2, "What the platform holds".
9. "What the fields are for" says "in most real ones, a system records what its own work needs and
   nothing more"; the closing paragraphs say real platforms keep query logs, snapshots and audit
   trails. Restrict the first claim to the shop.
10. "Every table must have an owner" is declared met but never stated: "The requirement that every
    table has an owner is met, and your question is not." Only two of the four readings in
    CLAUDE.md's standing example appear.
11. The raw total is treated as the truth: "15400 pence ... went missing" assumes the raw sum is
    right, but it includes cancelled orders. "Same" reads as right and "different" as wrong.

## Low

12. Chapter 1 sentences repeated: "`orders.jsonl` holds every order the shop took, as the checkout
    sent it"; "`daily_sales` holds one row per day, with amounts in pence"; "The shop, its people
    and its data are invented for the course"; "All times are UTC"; the "Monday morning" recap;
    "You have looked round the shop's platform in Chapter 1" is filler.
13. The week is no longer drawn in Chapter 2, though the failed night and the Saturday edit ask the
    learner to hold the nights' sequence.
14. "Everything the platform records looks like a normal morning with one row fewer" follows
    details (last altered a day earlier, 6 rows) that are not normal.
15. "Records made at the time": "three kinds of record, none of which the platform keeps" is
    followed by "Some of it the systems already keep"; "about the platform" is undefined.
16. "The handover" follows the section that already lists what a note should hold.
17. No reflective questions at the end; "Before Chapter 3" repeats the "Reconstruction" argument.
18. Wording: "Questions like the head of the shop's arrive"; "somebody" twice; "None of them is
    answered by the rows a table holds today"; "Start with the arithmetic."; "The platform has a
    complete picture of its own state"; "records as much about a file"; "location" vs "key";
    "code cell" vs "cell"; the "How this differs" paragraph and "'No simple query reproduces it'
    means ...".
19. The dashboard's `values` print as a run-on: "£147.00day: 2026-09-08 ...".
