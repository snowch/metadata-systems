(A reviewer on another model, reading as a learner who has done Chapters 1 to 20; returned as text and saved here.)

REVIEW OF CHAPTER 21, "Conflicting metadata"

Numbers checked: I ran `shop.claims.claims(...)` and `shop.claims.resolve(..., rule)` for all four rules at 2026-09-14T18:00Z and 2026-09-15T09:00Z. I also listed `run_week(["returns"]).executions` to confirm that `build_daily_sales` finishes at 02:30:21 on every night from 8 to 14 September. Every number and value on the page matches the engine, with one exception: BLOCKING 1 (`as of`, Monday). Dates, weekdays and the five-claim count are correct. I read `chapter_21.py`, the as-built text, the chapter's notes, Chapters 2, 3, 4, 10, 18 to 20 and the opening of 22, `claims.py`, and the pins in `test_engine.py` and `test_words.py`. This is a read-only review.

## BLOCKING

**1. "Change `"newest"` to `"as of"` in the cell" does not say which cell, and the two cells give different answers.**
- Quote: "Change `"newest"` to `"as of"` in the cell, select it and press **Run below**. The claim whose source changed most recently wins: the owner is `etl_service` and the columns are `day, revenue_pence`, both from the warehouse."
- Two cells contain `"newest"`: the Monday 18:00 one and the Tuesday 09:00 one.
- I ran both. On Monday, `as of` gives owner `j.marsh` (records, as of 16:40, which is later than the warehouse's 02:30:21). Only the Tuesday cell gives `etl_service`.
- A learner who edits the first cell sees `j.marsh`, which contradicts the page. That cell is the one reached first when scrolling up, so this is likely.
- The same problem applies to the `ranked` and `all` instructions. "Five rows" holds on both days, but the values differ.
- Direction: name the cell, for example by its output, or give the Tuesday cell its own name.
- The summary also needs fixing. "Ordering by the time a source last changed gave the warehouse's account, because its content changes every night" is true only on Tuesday morning. It would be false if the records changed again after 02:30 on Tuesday. The page does not say that the result depends on the time.

**2. The requirement exercise skips steps of "Question the requirement" and mixes two ambiguities.**
- Quote: ""Correct" could mean three things, each needing something different." The three bullets are rules ("the newest claim", "the claim from the source trusted most for owners", "every claim, with where it came from"). They are mechanisms, not the questions the requirement could be asking.
- Chapter 2's exercise (see `chapter_02.py` near line 323) has the structure: what the rule could mean, what each reading needs, whether the record answers it. This chapter has no such structure.
- The last step is missing: which readings the shop's record meets. The paragraph on Tuesday's results is only a list of outputs.
- The paragraph "`j.marsh` names a person, `data team` a team, and `etl_service` an account" is about which meaning of "owner" each claim carries. That is a second ambiguity, separate from which claim wins.
- Quote: "A rule that keeps one claim also keeps one meaning. The requirement does not say which one it means." "Which one" could refer to the three rules or to the three meanings of "owner".
- Direction: separate the two axes. First, what "correct" asks (the newest statement, the most trusted source, every statement with its origin). Second, what "owner" means. Then say which readings the shop's rules satisfy.

## SHOULD

**3. For the owner, the conflict is partly manufactured, and the page says so only at the end.**
- Quote: "Three are about the owner: `etl_service`, `j.marsh` and `data team`."
- Chapter 4 separated `responsible` (who to ask) from the warehouse's owner (which account controls the table), and said the head's list does not count the account. Here the records' `responsible` line is relabelled "owner".
- A learner from Chapter 4 will object that these are not claims about one attribute.
- The "owner means three things" point appears only after the rules. Either flag it where the claims are introduced, or accept that the owner conflict is deliberately artificial and say so.
- Only the columns are a true conflict, since the same attribute has two different values.

**4. The prose says the shop keeps "every claim", but the model-versus-reality note says it keeps only the latest claim per source.**
- Quotes: "Every claim is kept, with its source and its two times: five rows." and "Keeping every claim with its source left the choice to you." Against: "The shop keeps the latest claim of each source for each attribute."
- The page says the team sheet is "imported every night" and "each import sends every row again", yet the table shows one sending per source.
- A learner may expect seven imports of two rows each. Say, in the first table's introduction, that the system keeps only each source's latest sending.

**5. The "ranked" order is unexplained, and "trusted" and "the role the shop gave it" are vague.**
- Quote: "the claim from the source trusted most for owners". The order is records, then the team sheet, then the warehouse.
- The team sheet ranks above the warehouse for owners, although the page has just shown it is stale. No reason is given.
- Quote: "It holds only while each source keeps the role the shop gave it." The page never introduces any "role".
- Direction: say what the order encodes, and say what would make it fail (for example, the records source stopping).

**6. The `as of` rule is the fourth rule, and it is absent from the requirement's readings.**
- The learner has just run `as of`, which gives `etl_service` and is the only rule that returns the warehouse's account.
- The readings list ("three things") leaves it out, so "On Tuesday at 09:00, the three give, in that order: `data team`; `j.marsh`; all three owners" omits the reading "the claim whose content changed last".
- The objectives say "Try three other rules for choosing", but `all` chooses nothing. "Precedence" is defined as "the rule for which claim counts", and `all` is not one.

**7. The opening map shows nothing this chapter's question needs.**
- Quote: "The platform map shows the shop's three systems and the returns desk, as Chapter 7 left them." The caption reads "The shop's three systems with the returns desk on Monday morning...".
- The text is identical in Chapters 18 to 23. The chapter never refers to the map again, and the records and the team sheet are not on it.
- The page then says "three sources", which is a different set from "three systems" and shares only the warehouse. This is a word collision between "system" and "source".
- No figure carries the five times the learner must hold in mind: 28 August, 02:30:21, 03:30, 04:00 and 16:40. Under CLAUDE.md, time is a standing job for a figure.
- Direction: replace the map with a time-ordered figure of when each claim was sent and when its source last changed, computed from `claims`. Or drop the opening.

**8. "Nobody changes anything" conflicts with a later statement.**
- Quote: "Overnight, the warehouse's catalogue is read again at 03:30, and the team sheet is imported again at 04:00. Nobody changes anything."
- Later: "The warehouse's content changes every night, at 02:30:21". Nobody edits the records or the sheet, but the table does change. State what does not change.

**9. The Tuesday claims are never shown.**
- The prediction depends on Tuesday's sent times, but only `resolve`'s output is printed for Tuesday, not the claims.
- The learner has to infer them from "imported every night at 04:00".
- Tuesday 02:30:21 is also beyond the shop's week, which ends with the night of Monday 14. The write is extrapolated by the engine, not run. The exercise is still predictable, but "A number ... the engine produced" is not quite what the pin proves.

## COULD

- "Its owner is the account that created the table, `etl_service` (Chapter 2)". Chapter 2 only says the warehouse "lists `etl_service` as the owner" and "records nothing else". "Created" comes from the PostgreSQL aside, not from the shop. Say "records as owner".
- "Your records ... sent when they change. You last changed them on Monday 14 at 16:40". The 16:40 time is stipulated and no earlier chapter establishes it. Say it is the shop's.
- "Compare this with what you wrote." is a sentence the learner would not miss (filler).
- "There are five claims. Three are about the owner: ..." restates the table the cell just printed. Keep the count and drop the list.
- "The next cell shows its choice." Personifies the rule, so the plain version is "shows the value it chooses".
- "A rule that keeps one claim also keeps one meaning." This is an aphorism with a forced contrast (AGENTS.md rules 1 and 3). Replace it with a sentence about which claim carries which meaning.
- "The head of the shop's requirement: "Show the correct owner."" is awkward, as the head is not the requirement's head. The same wording appears in Chapters 18 to 22, so it is a series-wide fix.
- After the learner edits the rule, the output sits above the paragraph "At 09:00 on Tuesday 15, the owner is `data team`", which then contradicts it. Tell the learner to change the rule back to `"newest"`, or give each rule its own cell.
- The notes (`docs/notes/chapter-21.md`) say "the options are values" and "change the time to Tuesday 09:00". The page has free-text prediction cells and a separate Tuesday cell. The notes also say "four rules", while the objectives say "three other rules".
- The word *source* appears for systems here and for other things in earlier chapters. The word *record* is used for the learner's records, for the `records` source, and for "record" in prose. The page is mostly consistent, but "its source's content" and "source" as a column value are close.
- The "Time and memory" callout numbers (9 to 12 seconds, 400 MB, 13 MB) are copied from Chapters 18 to 23. I did not check them against measurement for this chapter.

No claim about OpenLineage or a real product appears on the page, so nothing needs `docs/sources.md`. The only real-system sentence, "A real system may keep every claim it has received, with its history", is hedged. The "Originality" and "Requirements" sections of the notes exist and answer to the page.
