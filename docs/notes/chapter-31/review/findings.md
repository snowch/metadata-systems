REVIEW OF CHAPTER 31, "Metadata platforms"

Checked: I ran `shop.platforms.architectures()`, `owners_in()`, `kept()` and `check()` from `/home/user/metadata-systems/notebook`. That covered the starting value, `REFERENCE`, and wrong values (shared types, bare names, `CUSTOM`, lower case, an empty custom URN, a missing key, three equal invalid types). The only number the page states, "3 of DataHub's owners told apart", holds for `REFERENCE`. The 3, 3, 1, 0 kept and the 0s at the starting value match the as-built file. I compared the cells with `notebook/chapter_31.py`, `docs/plan.md` and `docs/sources.md`, and with Chapters 7, 27, 29 and 30. I re-read three upstream sources at the pinned commits: DataHub `Owner.pdl`, `OwnershipType.pdl` and `ownership-types.yaml` at master, OpenMetadata `validateOwners` at `18294ee`, and Marquez `SearchConfig.java` at main. The map caption ("three return files") is the same text as Chapters 7 and 8. I did not run the page in a browser.

## BLOCKING

1. **"Each platform meets some of these readings" contradicts the page's own list.**
   - Quote: "Each platform meets some of these readings. The requirement does not say which it means."
   - By the three bullets above it, Marquez meets none: it "keeps none on a dataset", it is not listed under "whom to ask", and "only DataHub keeps" the type.
   - `docs/notes/chapter-31.md` repeats the claim. Either the namespace owner has to be brought in as a reading, or the sentence has to change.

2. **The check states DataHub's rule for ownership types, and the sources do not support it.**
   - Quotes: "Each type is one DataHub accepts.", "DataHub does not accept `CUSTOM`...", and "A type of your own is written `urn:li:ownershipType:` followed by a name."
   - In `Owner.pdl` (master) the enum field `type` is marked `@deprecated`. The current field is the optional `typeUrn`, which must refer to an existing `ownershipType` entity.
   - The enum has a `CUSTOM` value, which the check rejects. The built-in types are themselves entities, for example `urn:li:ownershipType:__system__technical_owner`.
   - The page and the engine fold two fields into one value, and any `urn:li:ownershipType:x` is "accepted". That is the shop's rule, not DataHub's.
   - `docs/sources.md` records only "with a type, or a `typeUrn`". It says nothing on the URN forms, or on `urn:li:corpuser` and `urn:li:corpGroup` as printed in the "stored as" column.
   - Direction: say which field the learner is setting, say that a custom type is an entity that must exist, and say that the check is the shop's reading. Then record the URN forms in `docs/sources.md`.

3. **The printed tables give away the prediction directly beneath it.**
   - The prediction is "write in the next cell which platforms keep all three owners of `daily_sales`".
   - After **Run all**, `owners_in()` and `kept()` are printed straight below the `[WRITE]` cell, and the page tells the learner to run all first. `kept()` shows "owners kept" as 3, 3, 1, 0.
   - `CLAUDE.md` lists exactly this fault: "a printed table that gives away the answer to the question above it".
   - Direction: put the answer's cells where they do not sit under the prediction, or hold them until the learner has written.

## SHOULD

4. **The rules list also answers the prediction.**
   - The bullets "a list of owners" (DataHub), "a list of owners" (OpenMetadata), "one text value" (Atlas) and "no owner on a dataset" (Marquez) say it before the cell asks.
   - `docs/notes/chapter-31.md` calls this "Predictable: yes, from the rules listed". It is a reading exercise, not a prediction of anything the learner could be wrong about.
   - `docs/notes/part-7/design.md` asked "which platforms keep all three owners and which meaning each holds?". The built cell dropped the second half.

5. **"Keep all three" is not defined, and Atlas's answer is the shop's choice.**
   - Quote: "Atlas keeps one, here the first, `etl_service`."
   - A text value could carry three names. The page presents "one" as Atlas's behaviour. Only the last differences bullet says "depends on what writes it".
   - "The first" is not said to mean the account.

6. **Reading 2 conflicts with the section above it.**
   - Quote: "keeps whom to ask: it needs a person. DataHub and OpenMetadata can hold `j.marsh` as a user".
   - Holding `j.marsh` is not telling a reader that he is the one to ask. OpenMetadata's untyped list cannot, and the page says `BUSINESS_OWNER` "does not say 'whom to ask'".
   - "Can hold" and "meets" are being conflated. Item 1 also has no "needs", though the lead-in says "Each item below says what it needs and which platforms meet it".

7. **"Type" is used in several senses, and the output contradicts itself.**
   - Senses: "a team whose type is `Group`", "ownership type", "told apart by type", "a type the organisation defines", the OpenLineage owner's "optional type", and Atlas's "type system".
   - The `owners_in()` output prints "a team of type Group" for OpenMetadata's third owner. The `kept()` column "owners told apart by type" then gives OpenMetadata 0.
   - Quote: "Of the four, only DataHub keeps one." Atlas's `hive_db` has an `ownerType`, which research note 3.14 records. The claim is true only for a meaning-type, and the page does not say so.
   - Direction: use "ownership type" throughout, and rename the team's "type".

8. **Built-in types do carry descriptions.**
   - Quote: "A type the organisation defines can carry its own description."
   - `ownership-types.yaml` gives each built-in type a name and a description, for example "Involved in the production, maintenance, or distribution of the asset(s)". The sentence suggests built-ins have none.
   - Quote: "DataHub's own names do not say which question each owner answers". The page also says this before the learner has been asked what the types prove. That is the "what did that prove" step stated in prose.

9. **The type experiment does not exercise anything the page then concludes.**
   - The check passes for any three distinct valid strings. That includes `NONE`, `BUSINESS_OWNER`, `DATA_STEWARD`, for which "so a reader can tell the three apart" is hollow.
   - The page admits afterwards that distinct types do not say whom to ask.
   - The design said the check "says which meaning the reader can recover". The built check does not.
   - A wrong-value message is also thin. The "does not accept" line lists `` `a`, `a`, `b` `` without naming which owner has which value. `kept(types)` reports "3 told apart" for types the check rejects.

10. **The architectures table is an instrument with no question, and the prose repeats it.**
    - The paragraph after it ("DataHub and OpenMetadata take metadata both ways...", "Each keeps its metadata in a database...") restates the table's cells.
    - Nothing connects arrival, modelling, storage or search to the owner experiment.
    - "Each keeps its metadata in a database and searches it through an index" overstates two cases. Marquez's index is "optional". `SearchConfig.ENABLED` is `false` by default, which supports "optional". DataHub's primary store can also be Cassandra (research note 1.9), which is not relational.

11. **Several sourcing gaps in `docs/sources.md`.** I found these by grep.
    - It has nothing for Marquez's PostgreSQL, its optional OpenSearch, its model (namespaces, sources, datasets, jobs, runs) or "no owner on a dataset". Its Marquez entry covers events and `anonymous` only.
    - DataHub's storage and search facts are delegated to "research note for Chapter 31".
    - The DataHub commit in `sources.md` (`40287ac`) differs from the one in the research note (`2f2dcd4`). Say which one the table was checked against.
    - `Owner.pdl` carries the comment "only corpuser is currently supported in the frontend". The page says DataHub keeps the group `data team` without mentioning it.

12. **"Table" has three meanings.**
    - "The first table gives DataHub's three owners the same ownership type" is ambiguous. The architectures table comes before it.
    - "The table and the rules come from each project's documentation" does not say which table.
    - The map caption also says "the table `returns`", a warehouse table.

## COULD

13. **The OpenLineage facet sentence dangles.**
    - Quote: "OpenLineage has a facet for a dataset's owners too: each owner has a name and an optional type, both as text."
    - It leaves open whether Marquez keeps what the facet carries, and a reader may infer that it drops it. The page does not say.
    - The facet's text type sits beside the ownership types in the same sentence, which also feeds point 7.

14. **The requirement repeats Chapter 27's argument.**
    - Chapter 27's requirement was "The query layer must answer who owns each asset", with the same three meanings.
    - The readings here ("an owner for each dataset", "whom to ask", "which meaning") are not tied to Chapter 27's three. The page never says which of them each platform's field answers.
    - The "as written and as meant" step reduces to "The requirement does not say which it means".
    - The free-text answer is not compared with anything afterwards.

15. **The closing is out of order and partly redundant.**
    - The sentence naming Chapter 32 sits between the summary and the reflective questions. The questions do not lead into Chapter 32.
    - "The page could not show the platforms themselves..." duplicates the "How this differs" note. "Each platform keeps much more than an owner" is filler.
    - "Which meaning of 'owner' does your platform keep?" is ambiguous. "Your platform" could be the learner's work platform or the store they built.

16. **Small items.**
    - "pushed, by hooks' messages or the API" is awkward.
    - "urn", "corpuser" and "corpGroup" are printed but never explained.
    - The `types` keys (`account`, `responsible`, `team`) are not tied in the text to the three owners.
    - The section "Four platforms" holds the owner experiment, so its heading does not cover it.
    - The standing map is used by no question in this chapter.
    - In `shop.platforms.check`, the owner-by-owner duplicates in the "does not accept" line could be deduplicated.
