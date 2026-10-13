# Revision brief P31: Chapter 31, Metadata platforms

Read `rev-common.md` first. Redraft these slots: B, C, CC, D, E, G, Z. Terms: none new.

Say "ownership type" every time you mean the meaning DataHub gives an owner; never "type" alone for
it. OpenMetadata's field for a team is its "team type". Never write "the first table" or "the table
below": name what is listed ("the list of stored owners", "the count of owners", "the architectures
list").

## B

- Keep the heading `### Four platforms`.
- A metadata platform receives metadata from many systems, keeps it, and answers questions about it,
  as the shop's store, collector, graph and pages did in Part VI.
- DataHub, OpenMetadata, Apache Atlas and Marquez are four such platforms.
- As in Chapters 29 and 30, none of them runs here. The next cell sets out, from each project's
  documentation and code in the version read, how metadata arrives in each, how it is modelled,
  where it is kept and how it is searched.

## C

- The heading `### The owners of daily_sales`, with `daily_sales` in backticks.
- Chapter 27 found three owners of `daily_sales`: the account `etl_service`, the person responsible
  `j.marsh`, and the team `data team`.
- Each platform has a rule for an owner, as its code states it (a list):
  - DataHub: a list of owners. Each owner is a user or a group, named by a URN, DataHub's form of
    name: `urn:li:corpuser:` and a user's name, or `urn:li:corpGroup:` and a group's name. Each owner
    has an ownership type, also named by a URN. DataHub defines four, from
    `urn:li:ownershipType:__system__technical_owner` to `urn:li:ownershipType:__system__none`, each
    with a name and a description, and an organisation can define more.
  - OpenMetadata: a list of owners. Each is a user, or a team whose team type is `Group`. An owner
    has no ownership type.
  - Atlas: one text value, `owner`, on each asset, which may be left empty.
  - Marquez: no owner on a dataset. A namespace has one, and a namespace made from an OpenLineage
    event gets the owner `anonymous`.
- Here the shop gives DataHub and OpenMetadata `etl_service` and `j.marsh` as users, and `data team`
  as a group in DataHub and a team of team type `Group` in OpenMetadata.
- Before you read on, write in the next cell which platforms keep all three owners of `daily_sales`.

## CC

- The question: which platforms will keep all three owners of `daily_sales`? Write it as the
  question alone, then the line of eight full stops.

## D

- Keep: "DataHub and OpenMetadata keep all three. Atlas keeps one, here the first, `etl_service`. Marquez keeps none."
- Compare this with what you wrote.
- The list of stored owners gives DataHub's three owners the same ownership type,
  `urn:li:ownershipType:__system__technical_owner`, with its description. So the count of owners
  below it shows none of DataHub's three told apart by ownership type. OpenMetadata's owners carry no
  ownership type at all.
- The next cell holds `types`: the ownership type each of the three owners gets in DataHub. As it
  stands, each is `urn:li:ownershipType:__system__technical_owner`.
- Change them so that each owner has its own ownership type: one of DataHub's four, or one of your
  own, written `urn:li:ownershipType:` followed by a name. Select the cell and press **Run below**.
- The check below it tests that each ownership type is written as DataHub names one, and whether the
  three owners can be told apart by their ownership types.
- The check does not test that an ownership type of your own has been defined in DataHub, as DataHub
  would need. That is the shop's simplification.

## E

- With three different ownership types, both tests pass. Keep the words "all 3 of DataHub's owners
  told apart by ownership type" in the sentence that says what the count of owners below the check
  shows.
- The list of stored owners below that shows each owner's ownership type, and the description of
  each of DataHub's own.
- An ownership type tells the owners apart. Neither DataHub's names for its four nor their
  descriptions say which question an owner answers: `__system__business_owner` is described as
  "Principal stakeholders or domain experts associated with the asset(s).", not as the person to ask.
- An ownership type the organisation defines carries the description the organisation gives it.

## G

- "Choose a metadata platform that tracks ownership" could mean three things. Each item says what it
  needs, then which platforms meet it (a list):
  - an owner for each dataset: it needs an owner on a dataset. DataHub, OpenMetadata and Atlas can
    keep one. Marquez keeps owners only on namespaces, not on datasets;
  - whom to ask about each dataset: it needs a person, and a record that this person is the one to
    ask. DataHub can, with an ownership type defined to mean it. OpenMetadata and Atlas can hold
    `j.marsh`, but their rules keep no meaning with an owner, so the record does not show that
    `j.marsh` is the one to ask;
  - which meaning each owner holds: it needs an ownership type for each owner. Of the four, only
    DataHub keeps one.
- So DataHub can meet all three readings, OpenMetadata and Atlas the first only, and Marquez none for
  a dataset.
- The requirement does not say which it means.

## Z

- Keep the heading `### Before Chapter 32`.
- DataHub and OpenMetadata kept all three owners of `daily_sales`, Atlas one and Marquez none.
- Only DataHub's ownership types let a reader tell the three apart, and only when each had its own
  ownership type. Their names and descriptions still did not say which question each owner answers.
- Chapter 32 follows the metadata of a forecast trained on the shop's data.
- Three questions (a list, after a short line that introduces them):
  - Which meaning of "owner" does your own metadata platform keep?
  - Can a reader of it tell one owner's meaning from another's?
  - Which of your datasets have no owner at all?
- Keep the heading `### How this differs from a real platform`, then a list:
  - The architectures list and the owner rules come from each project's documentation and code in
    the version read. Each platform keeps much more than an owner.
  - DataHub names an owner's ownership type in the field `typeUrn`. The shop's check takes any name
    after `urn:li:ownershipType:` and does not check that the ownership type has been defined.
    DataHub also has an older field, `type`, that its schema marks as no longer to be used.
  - A comment in DataHub's schema says its web front end supports only users as owners. The schema
    also allows groups.
  - The shop gives OpenMetadata `etl_service` as a user. OpenMetadata's rule takes any user.
  - Atlas has room for one owner; which of the three it holds depends on what writes it.
