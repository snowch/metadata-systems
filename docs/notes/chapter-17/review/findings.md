REVIEW OF CHAPTER 17, "Root-cause analysis" (read as a learner who has done Chapters 1 to 16)

(The reviewer returned this as text: its Write was refused. Saved as returned, its formatting kept.)

The numbers are right: Thursday 5150, 5150, 5150, 20550 (`run-028`, `run-015`, `run-014`); Saturday 21549, 21549, 19149, 19149 (`run-023`, `run-022`); Tuesday 16225 at every step; 2400 is order 7037 (2 × 1200, cancelled); 7009 cancelled on Tuesday 8; `build_clean_orders`'s code identical on all seven nights; the diff as printed.

## BLOCKING

### 1. The page says the cell's code measures every step the way `build_daily_sales` defines it. That is not what the search does.
**Where:** "At each step, the code in the cell measures Thursday's revenue the way `build_daily_sales` defines it: price times quantity over the day's completed orders, each order once."
**Problem:** Steps 1 and 2 read the stored values; only steps 3 and 4 compute. In the refunds week `build_daily_sales` no longer defines revenue as completed orders; the measure keeps the old definition, which is what makes Saturday's step 2 differ.
**Direction:** Say what the search does, and for Saturday that the measure is the definition before the change, and why that is the yardstick.

### 2. Saturday treats the cancelled order as a rival explanation, while Thursday treats two joint conditions as two causes
**Where:** "Two explanations fit…", "A cancelled order alone did not change the total… The change to the code explains Saturday's total.", "A day with the same kind of order and no change ruled out the other explanation.", the root cause definition, and the objective "Find two causes that each explain a total, and tell them apart."
**Problem:** On Saturday the code change and a cancelled order are both necessary, as on Thursday. Tuesday shows the order is not sufficient; it does not rule it out. Under the chapter's definition the cancelled order would also be a root cause.
**Direction:** Say what Tuesday shows; use one word, "cause" or "explanation"; weaken "ruled out"; fix the objective.

### 3. Claims that the data or the checkout "changed" are not supported by anything the shop records
**Where:** "the shop's records show that the data changed and the code did not", "the checkout's change is outside them", "why either the checkout or the code changed".
**Problem:** Nothing shows the checkout changed; the orders are in the file because they were placed on Thursday. The last sentence reads as if the code changed in both cases.
**Direction:** Say what the records show; whether the checkout's behaviour changed is outside them; keep the two days apart.

## SHOULD

### 4. "Root cause" is defined without a source, and the definition does not discriminate
**Direction:** Source it, or present it as the shop's working definition and say what it leaves open.

### 5. The commitments come after the answer is given, or are never revisited
**Problem:** (a) Nothing after the search refers back to where the learner would look. (b) The cause of Thursday is asked after "Two causes" names both, and the learner knows it from Chapters 2, 14 and 15. The search repeats Chapter 15's four steps without saying what it adds.
**Direction:** Move the commitment, or ask something unanswered; close (a); say what this adds to Chapter 15.

### 6. The Saturday prediction is partly answered by the paragraph above it, and "too high" has no stated yardstick
**Direction:** Ask first whether Saturday's total is wrong, and against what; then where the difference appears; describe the code change after.

### 7. The output has a numbered step 5 for the checkout, but the prose says the steps end at the file
**Direction:** Mark the last row as outside the records, or drop it; one name for what feeds the file.

### 8. The requirement section never states which readings the records meet
**Problem:** Reading 2 for Thursday says "none in the shop's records" though `run-014`'s count of 3 is such a record; "no decision exists" and "no decision recorded" are different.
**Direction:** For each reading and day, what the records satisfy and what they do not.

### 9. The "no reason recorded" point is made four times
**Direction:** Say it once, after the code diff.

### 10. The opening figure shows a week the chapter never uses
**Direction:** Use the map for what the search needs, or drop the returns desk from it here.

## COULD

11. "Change either, and the total would have counted the three orders" is asserted, not shown; "a rule that was in its code all week" rests on the code recorded per run, unsaid.
12. "09-11" in the table reads as 9 November.
13. "2 sets of brake pads": the catalogue names product 2 "Brake pads, pair".
14. "The next week" is the same week.
15. Six-column tables with long cells and headers on a phone; blank cells read as missing.
16. Small wording: the reality note's first bullet is filler; "fault" appears only in the definition; "for the work early on Sunday 13" is vague; "cause", "thing" and "explanation" for one idea.
17. The "Time and memory" figures are not yet measured for this chapter.
