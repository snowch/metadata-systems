# VERDICTS ON THE CHAPTER 21 FINDINGS

Numbered findings 1 to 9: 3 upheld, 4 partly upheld, 2 rejected. The COULD list is judged item by item at the end.

I ran `shop.claims.claims` and `resolve` for all four rules at 2026-09-14T18:00Z and 2026-09-15T09:00Z. I also read `chapter_21.py`, the as-built text, `docs/notes/chapter-21.md`, `shop/claims.py`, the Chapter 21 pins in `test_engine.py` and `test_words.py`, `docs/plan.md` row 21 (chapter table and requirements table), and Chapters 2 and 4 where cited.

## BLOCKING

**1. Which cell "Change `"newest"` to `"as of"`" means. UPHELD.**
- Checked: two cells hold `"newest"`. At Monday 18:00, `as of` gives owner `j.marsh` (records, 16:40, is later than the warehouse's 02:30:21). At Tuesday 09:00 it gives `etl_service`. The page's stated results hold only for Tuesday.
- The first `resolve(held, "newest")` cell is the one a learner reaches first, so a wrong edit is likely.
- `ranked` and `all` give the same attributes and row counts on both days but different values. For `ranked`, columns and owner agree on both days. For `all`, the rows differ in `sent` and `as of`.
- Fix must achieve: the learner edits one named cell whose time is fixed at Tuesday 09:00. Either name that cell by what it shows, or give the rule experiment its own cell after the Tuesday result. The page must say which time the results are for. This also removes the COULD item about the output sitting above a paragraph that contradicts it.
- The summary sentence "Ordering by the time a source last changed gave the warehouse's account" needs its time. I checked Monday 18:00 and Monday 12:00: `as of` gives `j.marsh` and `etl_service` respectively, so the result depends on when you ask. The fix is to say "on Tuesday morning".

**2. The requirement exercise: two ambiguities mixed, last step missing. PARTLY UPHELD.**
- Rejected part: the plan (row 21 of the requirements table) fixes the three readings as "the newest claim; the claim from the most trusted system; every claim with where it came from. Chapter 2's owner returns." The page follows that decision, and "owner" is the second axis the plan expects. Do not restructure into two exercises.
- Upheld part: the exercise ends with a list of outputs and no statement of what the shop's record can and cannot settle. "A rule that keeps one claim also keeps one meaning" is a forced aphorism, and "which one" is ambiguous between rules and meanings.
- Fix must achieve:
  - say plainly which claim carries which meaning: `j.marsh` a person, `data team` a team, `etl_service` an account;
  - say that the record holds all three claims, so only keeping them all leaves the reading open;
  - say that the requirement names no reading, so no output is shown to be the correct owner.
- This is a few sentences and should not add figures.

## SHOULD

**3. "Owner" from the records is Chapter 4's `responsible`. PARTLY UPHELD.**
- Checked in `chapter_04.py` line 96: "the lines that the head's list counts are the `responsible` lines... The warehouse's owner... answers a different question". So the Chapter 4 reader will notice that Chapter 21 files `responsible` under `owner`.
- Rejected part: making the owner conflict "not a real conflict" is not the chapter's job. The plan says Chapter 2's owner returns, and the final section already names the three senses.
- Upheld part: the sources list says only "they name `j.marsh` as responsible", then the table says `owner`. Fix must achieve: one clause where the sources are introduced saying that the shop's metadata system files each source's statement of who owns the table under one attribute, `owner`, and that this is the shop's choice. Do not reveal the three-senses point there.

**4. "Every claim is kept" against "the latest claim of each source". UPHELD.**
- Checked in `claims()`: it returns the latest sending of each source's claim per attribute, so there are 5 rows and not 7 imports. The page says "each import sends every row again" and "Keeping every claim... left the choice to you", but admits the truth only in the closing note.
- Fix must achieve: where the claims are first listed, say that the shop keeps each source's latest sending of each attribute. Reword "every claim is kept" and the summary's "Keeping every claim" to match. Keep the real-system note.

**5. The `ranked` order is unexplained, and "role" is undefined. PARTLY UPHELD.**
- Upheld: "the role the shop gave it" is never introduced. The order is stated with no reason.
- Checked a failure case: at Monday 12:00, before the records source has sent anything, `ranked` gives the owner `data team` (stale team sheet) and the columns from the warehouse. So `ranked` fails exactly when the top-ranked source has nothing to say.
- Fix must achieve: replace "role" with a plain statement of what the order assumes, and what stops it holding (for example, the records not being sent). Optionally give one clause for the reason, which should be the shop's reasoning, labelled as the shop's choice. Do not add a figure.
- Not upheld: asking why a stale source outranks the warehouse. That is a design choice the page already labels as the shop's.

**6. `as of` is absent from the readings; `all` is not a rule that chooses. REJECTED.**
- The three readings come from `docs/plan.md`. `as of` is a variant of the first (a different time), and the page shows it in "Other rules". Adding a fourth reading would unbalance the exercise.
- The objective "Try three other rules for choosing, and keep track of where each claim came from" is loose about `all`, but "precedence" is defined by the first rule, and `all` appears as "every claim kept". The wording is not worth a change. If an objective edit is made anyway, "three other treatments" is enough.

**7. The opening map. REJECTED.**
- `CLAUDE.md` says the platform map "appears in every chapter". The sentence is identical in Chapters 8 to 23 (confirmed by grep). Replacing it in one chapter breaks the convention.
- A new time-ordered figure is a large engine and figure change for a table that already prints `sent` and `as of` for all five claims. Finding 9's fix covers the Tuesday gap more cheaply.
- The "systems" and "sources" collision is mild: the page never calls the platform's systems "sources", and the three sources are defined explicitly in the first section.

**8. "Nobody changes anything." UPHELD.**
- Checked: the table changes every night at 02:30:21, so the warehouse's `as of` moves. The sentence is false as written, and it is also the premise of the Tuesday prediction.
- Fix must achieve: state what does not change (your records and the team sheet are not edited). Keep it plain, so the prediction is still a real one.

**9. Tuesday's claims are never shown. PARTLY UPHELD.**
- Rejected part: showing Tuesday's claims before the prediction would give the answer away. The newest sent time would be visible, which makes the prediction "plainly right". The notes say it is predictable from the schedule, and that is the design.
- Upheld part: after the prediction, the learner sees only the resolved owner and not the sent times that explain it. Fix must achieve: show the Tuesday claims in the result (or in a cell after it) so the explanation "its import at 04:00 is now the most recent" can be checked against sent times.
- Checked: the week ends with the night of 14 September (`NIGHTS[-1] = "2026-09-14"`), so the Tuesday 02:30:21 write is the engine's extrapolation of the same schedule. It is pinned by `TheClaims`. Add one clause saying the nightly schedule continues, or accept it as the model's; no new test is needed.

## COULD items

- **"The account that created the table": UPHELD.** Chapter 2 line 238 says "lists `etl_service` as the owner"; "created" appears only in the PostgreSQL aside (line 607). Say "the account the warehouse records as owner". The `claims.py` docstring says the same and can be left.
- **16:40 not established earlier: REJECTED.** It is the shop's stipulated scenario time, stated on the page.
- **"Compare this with what you wrote.": UPHELD, cut it here.** The same sentence is in Chapters 18, 19 and 23, so flag a series-wide cut. Chapter 23 adds a sentence, so check it separately.
- **"There are five claims. Three are about the owner...": REJECTED.** The pair `day, revenue_pence` and `day, revenue` is what later prose depends on, and the cost of trimming is more than the benefit.
- **"The next cell shows its choice": UPHELD, small.** Change to "shows the value it chooses".
- **"A rule that keeps one claim also keeps one meaning": UPHELD,** covered by finding 2.
- **"The head of the shop's requirement": REJECTED here.** The wording is the series convention (Chapters 4, 9, 10, 11, 13 and others). If changed, change it everywhere.
- **Output above the contradicting paragraph after editing: covered by finding 1.**
- **Notes drift: UPHELD, notes-only.** `docs/notes/chapter-21.md` should say the prediction is a free-text cell and the rules are tried in a Tuesday cell, and should say "three other rules" or "four rules" consistently. "Gives nothing away: the options are values" does not describe a free-text prediction. After finding 1 is fixed, the notes must describe the named cell.
- **Word clashes (*source*, *record*): REJECTED.** Usage is consistent on the page, and an invented rename would cost more than it fixes.
- **Time and memory numbers: REJECTED for this review.** They are copied across Chapters 18 to 23 as measured claims. Recheck them in the series pass, not here.

Files read: `/home/user/metadata-systems/notebook/chapter_21.py`, `/home/user/metadata-systems/docs/notes/chapter-21.md`, `/home/user/metadata-systems/docs/notes/chapter-21/review/findings.md`, `/home/user/metadata-systems/docs/notes/chapter-21/review/chapter_21-as-built.md`, `/home/user/metadata-systems/notebook/shop/claims.py`, `/home/user/metadata-systems/notebook/tests/test_engine.py`, `/home/user/metadata-systems/notebook/tests/test_words.py`, `/home/user/metadata-systems/docs/plan.md`.
