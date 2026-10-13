# VERDICTS ON THE CHAPTER 31 FINDINGS

4 upheld, 8 partly upheld, 4 rejected.

What I ran or read:
- I ran `shop.platforms.owners_in()`, `kept()` and `check()` for the starting types, three distinct built-ins, `a`/`a`/`b`, `CUSTOM`/`x`/`y` and an empty dict.
- I read `sceptic-brief.md`, the findings, the as-built file, `notebook/chapter_31.py`, `shop/platforms.py`, `docs/notes/chapter-31.md`, the Part VII research note and "Read for Part VII" in `docs/sources.md`.
- I read `docs/notes/part-7/design.md` and `docs/authoring.md` ("Predictions").
- I compared Chapters 12, 27, 29 and 30.
- I fetched DataHub `Owner.pdl` and `ownership-types.yaml` at `40287ac`, and `Owner.pdl` at `2f2dcd4`. I fetched Marquez `SearchConfig.java` and `OpenLineageDao.java` at `180f37b`.

## BLOCKING

**1. PARTLY... no: UPHELD.** "Each platform meets some of these readings" contradicts the three bullets above it.
- Marquez "keeps none on a dataset". It is not in the "whom to ask" bullet, and "only DataHub keeps" the type. By the page's own list it meets none. `docs/notes/chapter-31.md` repeats the claim, and `design.md` also says "Each platform meets some".
- The first bullet also says Atlas "does" keep an owner for each dataset, but the page says Atlas's `owner` "may be left empty". "Can" is accurate.
- The fix must make the closing sentence true of the list, for example by saying what Marquez meets (only a namespace's owner, which is not a dataset's). Correct the notes and `design.md` in the same edit. Check whether `test_words.py` pins the sentence.

**2. UPHELD.** The check states a DataHub rule that the source does not support.
- `Owner.pdl` is identical at `40287ac` and `2f2dcd4`. `type: OwnershipType` is `@deprecated`, and `typeUrn: optional Urn` carries the relationship to an `ownershipType` entity.
- The `OwnershipType` enum documents `CUSTOM` as "set when ... a new one is specified as an ownership type entity for which we have no enum value". The check's message "DataHub does not accept `CUSTOM`" is therefore false of DataHub.
- `ownership-types.yaml` confirms the built-ins are entities, for example `urn:li:ownershipType:__system__technical_owner`. The page folds two fields into one value and accepts any `urn:li:ownershipType:x`. That is the shop's reading, and nothing on the page labels it as such.
- I could not confirm from the PDL that a `typeUrn` must name an existing entity. It carries only a relationship annotation. The fix must not assert "must exist" unless that is read from DataHub's code.
- The fix must achieve all of the following.
  - Stop attributing the rejection of `CUSTOM` to DataHub: either drop it from the rejected set or say the shop's check does not take it.
  - Say in "How this differs" that the shop folds `type` and `typeUrn` into one value and does not check that a custom type exists.
  - Explain `urn`, `corpuser` and `corpGroup` in a clause, since the "stored as" column prints them.
  - Record the URN forms and the two fields in `docs/sources.md`.
  - Update the pins in `test_engine.py` (around line 1020) and `test_words.py` (around line 1781) if any message changes.

**3. REJECTED. I come down against moving the cells, for this chapter.**
- The facts are true. The page's own box says "Run every cell first: press **Run all**", and `owners_in()` and `kept()` sit directly under the `[WRITE]` cell. After Run all the learner sees 3, 3, 1, 0.
- The structure is the course's convention, not this chapter's choice.
  - Chapters 12, 27, 29 and 30 print their answer cells directly below the prediction cell in the same way. For example, Chapter 12 puts its prediction at line 84 and the result cell at line 102.
  - `docs/authoring.md` ("Predictions") prescribes exactly this: "Put the question before the cell that answers it, and say in the prose to write the expectation down before running on."
- `CLAUDE.md` lists "a printed table that gives away the answer to the question above it" as something to read for. It also recognises that a notebook shows output once a cell has run. The two documents are reconciled by order plus an instruction, and this chapter gives the instruction: "Before you read on, write in the next cell...".
- Moving the cells or holding their output is not possible inside one chapter. It would need a part-wide or course-wide mechanism, such as answer cells that Run all does not run.
- The harm here is small. The rules bullets already state the answer (see finding 4), so hiding the tables would protect little.
- There is a real tension: the chapter's own opening box tells the learner to run everything first. It should go to the author as a course-wide decision on amending `authoring.md` and `CLAUDE.md`. No Chapter 31 edit.

## SHOULD

**4. REJECTED.** The rules list does answer the prediction, and that is the design.
- `CLAUDE.md` asks for a belief the learner can already hold. Here the learner applies stated rules to three owners.
- A learner can still be wrong. They may expect Atlas to keep all three, or Marquez's namespace owner to count, or OpenMetadata to refuse the account.
- The design's "and which meaning each holds" is carried by the types experiment, so the omission from this cell loses nothing.
- Making the prediction harder would need a new figure, and the chapter does not need one.

**5. REJECTED.** "Keep all three" means three owners kept as separate owner entries.
- Atlas's `owner` is one `string` (research 3.12), so "keeps one" is accurate.
- The last differences bullet already says "which of the three it holds depends on what writes it", which labels "here the first" as the shop's choice.
- The sentence names `etl_service`, the account from Chapter 27's list, so "the first" is not left unexplained.

**6. PARTLY UPHELD.**
- What stands: the lead-in says "which platforms meet it", but the second bullet says only that platforms "can hold" `j.marsh`. Holding a person is not meeting "whom to ask". The first bullet lacks "needs", and the three bullets are not parallel.
- What does not stand: there is no contradiction with the BUSINESS_OWNER sentence. The bullet does not say DataHub's type answers "whom to ask".
- The fix must make the three bullets parallel (what it needs, then which platforms meet it). It must stop "can hold" standing in for "meets".

**7. PARTLY UPHELD.**
- What stands: "type" carries several senses on the page. `owners_in()` prints "a team of type Group" beside an ownership type of None. The `kept` column reads "owners told apart by type", and the OpenLineage sentence has "optional type". OpenMetadata's field is `teamType` (research 2.11).
- The fix must use "ownership type" wherever the meaning is meant, and call the team's field something else, such as "team type". Output strings are pinned by tests.
- What does not stand: "only DataHub keeps one" is not false because of Atlas's `hive_db.ownerType`. That field is the owner's principal kind (USER, ROLE, GROUP), not a meaning. The claim holds once "ownership type" is used. No Atlas change is needed.

**8. PARTLY UPHELD.**
- What stands: the sentence "A type the organisation defines can carry its own description" implies the built-ins have none. `ownership-types.yaml` gives each a name and a description, for example "Involved in the production, maintenance, or distribution of the asset(s)." The fix must remove the implication, either by saying the built-ins carry descriptions too or by cutting the sentence.
- What does not stand: stating "DataHub's own names do not say which question each owner answers" after the experiment is the chapter's conclusion, not a pre-empted question. `CLAUDE.md` allows prose that names a conclusion more exactly than an interaction can. The descriptions do not say "whom to ask" either. No change.

**9. PARTLY UPHELD.**
- What stands, both engine fixes, both verified.
  - `kept(types)` counts uniqueness without validity. With `CUSTOM`/`x`/`y` the check fails its first test while `kept` reports 3 told apart. `kept` should count only types the check accepts.
  - The "does not accept" line lists `` `a`, `a`, `b` `` without saying which owner has which value. For a missing key it prints `None`, `None`, `None`. It should name the owner for each bad value.
- What does not stand: the claim that the check is hollow because it passes any three distinct valid strings. The chapter's point is the next sentence, that distinct types tell the owners apart but do not say which question each answers. A semantic check on type names would not be robust. The design's "says which meaning the reader can recover" overreached, and I would not build to it.

**10. PARTLY UPHELD.**
- What stands, both verified.
  - "Each keeps its metadata in a database and searches it through an index" is overstated. The table itself says Marquez's index is optional. `SearchConfig.ENABLED = false` supports "optional". DataHub's research note 1.9 lists Cassandra among its primary stores, against the cell "a relational database".
  - The paragraph after the table restates its cells, so the two prose paragraphs should be cut or reduced to what the table cannot show.
- What does not stand: adding a question or a new figure. The comparison of the four architectures is the plan's Chapter 31 content and the first objective, so an instrument with no question is acceptable here. Fix the DataHub storage cell to match the source.

**11. UPHELD.** This is documentation work and costs nothing on the page.
- I checked `docs/sources.md`. It has no Marquez storage, model, optional-search or "no owner on a dataset" entry. The Marquez entry covers events and `anonymous` only.
- The DataHub entry delegates storage and search to "research note for Chapter 31".
- The DataHub commit is `40287ac` in `sources.md` and `design.md`, but `2f2dcd4` in the research note. `Owner.pdl` is identical at both, so the table can be recorded against `40287ac`. State that.
- Record:
  - Marquez's PostgreSQL, the default-off search (`SearchConfig.ENABLED`), its model and "no owner on a dataset";
  - DataHub's storage and index;
  - Atlas's search-engine requirement (research 3.10);
  - the URN forms (see 2);
  - the `Owner.pdl` caveat "only corpuser is currently supported in the frontend". The `entityTypes` list still includes `corpGroup`, so the page's "a user or a group" holds. Recording the caveat in `sources.md` is enough.

**12. PARTLY UPHELD.**
- What stands: "The first table gives DataHub's three owners..." follows three printed tables (architectures, `owners_in`, `kept`). "The table and the rules come from each project's documentation" does not say which table. "The table below the check" is a fourth use.
- The fix must name the thing: "the list of stored owners", "the architectures list".
- What does not stand: the map caption's "the table `returns`". That caption is shared text from Chapters 7 and 8 and uses a warehouse table in the shop's sense.

## COULD

**13. UPHELD.** Cut the OpenLineage facet sentence.
- Chapter 8 (line 420) already presents the `ownership` facet and what it does not say.
- The sentence leaves open whether Marquez keeps the facet. The sources do not settle that. `OpenLineageDao.java` has no ownership-facet handling, but I read only that file, so it is not conclusive. The page must not invent behaviour.
- It also feeds finding 7 through "optional type".

**14. REJECTED.**
- Part VII's requirement sections all run the same way (compare Chapters 29 and 30): a free-text cell, then readings each with what it needs, then "The requirement does not say which it means." Nothing compares the free text afterwards in those chapters either.
- The step of saying what each platform records, and which readings it meets, is the bullet list.
- Chapter 27's argument was about one platform's own fields. This chapter's is about four platforms' fields, so it is not the same argument made twice. The parallel-bullets fix in finding 6 improves it enough.

**15. PARTLY UPHELD.**
- What stands: "Which meaning of 'owner' does your platform keep?" is ambiguous. It could mean the learner's work platform or the metadata store they built in Part VI. Name it ("your own metadata platform").
- What does not stand: the closing order. Chapter 30's closing has the same shape (summary, "The page could not show...", the next-chapter sentence, questions). "Each platform keeps much more than an owner" is a model-versus-reality statement, not filler.

**16. PARTLY UPHELD.**
- Upheld:
  - The Atlas arrival cell ("pushed, by hooks' messages or the API") is awkward. Its fix is a wording change in `architectures()` and its pins.
  - Explain `urn`, `corpuser` and `corpGroup` (see 2).
  - "Four platforms" does not cover the owner experiment, so a heading before the owners list is cheap.
  - Deduplicating owners in the message (see 9).
- Rejected:
  - The `types` keys are tied to Chapter 27's three owners by the account/responsible/team wording just above them.
  - The standing map being unused by a question is the course's convention (`CLAUDE.md`, "Every figure is computed from the shop").

## Not in the findings (unverified)

The research note (2.11) says OpenMetadata's owner is "never a service account", yet the engine stores `etl_service` as "a user". The note calls this inferred. It is worth one check of how OpenMetadata treats bot users before the page says OpenMetadata keeps all three.
