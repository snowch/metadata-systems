[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 30](chapter_30.ipynb) · [Next: Chapter 32](chapter_32.ipynb)

# Chapter 31: Metadata platforms

**Objectives**

- Compare four metadata platforms: how metadata arrives, how it is modelled, where it is kept and how it is searched.
- Put the three owners of `daily_sales` into each platform, under its rule for an owner.
- Choose DataHub's ownership types for the three owners, and find what a reader can tell from them.
- Question the requirement "Choose a metadata platform that tracks ownership."

The platform map shows the shop's three systems and the returns desk, as Chapter 7 left them.

## Four platforms

A metadata platform receives metadata from many systems, keeps it, and answers questions about it, as the shop's store, collector, graph and pages did in Part VI.

DataHub, OpenMetadata, Apache Atlas and Marquez are four such platforms.

As in Chapters 29 and 30, none of them runs here. The next cell sets out, from each project's documentation and code, how metadata arrives, how it is modelled, where it is kept and how it is searched.

    >>> shop.platforms.architectures()
      | platform | metadata arrives | modelled as | stored in | searched through
      | DataHub | pulled by connectors on a schedule, or pushed | entities and aspects, in a schema language | a relational database | a search index
      | OpenMetadata | pulled by connectors on a schedule, or pushed, through one API | JSON Schemas | a relational database | a search index
      | Apache Atlas | pushed, by hooks' messages or the API | a type system of entities | a graph store | a search index
      | Marquez | pushed, as OpenLineage events or API calls | namespaces, sources, datasets, jobs and runs | PostgreSQL | an optional search index

DataHub and OpenMetadata take metadata both ways: connectors pull it on a schedule, and other systems push it. Atlas takes it pushed, from hooks inside other systems or through its API. Marquez takes OpenLineage events, as in Chapter 29.

Each keeps its metadata in a database and searches it through an index. Atlas keeps it as a graph.

Chapter 27 found three owners of `daily_sales`: the account `etl_service`, the person responsible `j.marsh`, and the team `data team`.

Each platform has a rule for an owner, as its code states it:

- DataHub: a list of owners. Each is a user or a group, and has an ownership type: `TECHNICAL_OWNER`, `BUSINESS_OWNER`, `DATA_STEWARD`, `NONE`, or a type the organisation defines.
- OpenMetadata: a list of owners. Each is a user, or a team whose type is `Group`. An owner has no ownership type.
- Atlas: one text value, `owner`, on each asset, which may be left empty.
- Marquez: no owner on a dataset. A namespace has one, and a namespace made from an OpenLineage event gets the owner `anonymous`.

Before you read on, write in the next cell which platforms keep all three owners of `daily_sales`.

    [WRITE] Which platforms will keep all three owners of daily_sales?
    [WRITE] ........

    >>> shop.platforms.owners_in()
      | platform | owner | stored as | ownership type
      | DataHub | etl_service | urn:li:corpuser:etl_service | TECHNICAL_OWNER
      | DataHub | j.marsh | urn:li:corpuser:j.marsh | TECHNICAL_OWNER
      | DataHub | data team | urn:li:corpGroup:data_team | TECHNICAL_OWNER
      | OpenMetadata | etl_service | a user | None
      | OpenMetadata | j.marsh | a user | None
      | OpenMetadata | data team | a team of type Group | None
      | Apache Atlas | etl_service | the text of `owner` | None
      | Marquez | None | no owner on a dataset | None

    >>> shop.platforms.kept()
      | platform | owners kept | owners told apart by type
      | DataHub | 3 | 0
      | OpenMetadata | 3 | 0
      | Apache Atlas | 1 | 0
      | Marquez | 0 | 0

DataHub and OpenMetadata keep all three. Atlas keeps one, here the first, `etl_service`. Marquez keeps none.

Compare this with what you wrote.

The first table gives DataHub's three owners the same ownership type, `TECHNICAL_OWNER`, so the second table shows that none of them can be told from the others by its type. OpenMetadata's owners carry no type at all.

The next cell holds `types`: the ownership type each of the three owners gets in DataHub. As it stands, each is `TECHNICAL_OWNER`.

Change them so that each owner has its own type. A type of your own is written `urn:li:ownershipType:` followed by a name. Select the cell and press **Run below**.

The check below it holds each type to DataHub's rule, and asks whether the three owners can be told apart.

    >>> types = {
    >>>     "account": "TECHNICAL_OWNER",
    >>>     "responsible": "TECHNICAL_OWNER",
    >>>     "team": "TECHNICAL_OWNER",
    >>> }

    >>> shop.platforms.check(types)
      | test | passes
      | Each type is one DataHub accepts. | yes
      | `etl_service`, `j.marsh` and `data team` share the type `TECHNICAL_OWNER`, so a reader cannot tell them apart. | no

    >>> shop.platforms.kept(types)
      | platform | owners kept | owners told apart by type
      | DataHub | 3 | 0
      | OpenMetadata | 3 | 0
      | Apache Atlas | 1 | 0
      | Marquez | 0 | 0

With three different types, both tests pass, and the table below the check shows all 3 of DataHub's owners told apart by type.

A type tells the owners apart, but DataHub's own names do not say which question each owner answers: `BUSINESS_OWNER` does not say "whom to ask". A type the organisation defines can carry its own description.

OpenLineage has a facet for a dataset's owners too: each owner has a name and an optional type, both as text.

## A platform that tracks ownership

[BOX] The head of the shop's requirement: "Choose a metadata platform that tracks ownership."

Before you read on, write in the next cell what "tracks ownership" means to you here.

    [WRITE] What does "tracks ownership" mean here?
    [WRITE] ........

It could mean three things. Each item below says what it needs and which platforms meet it:

- keeps an owner for each dataset: DataHub, OpenMetadata and Atlas do; Marquez keeps none on a dataset.
- keeps whom to ask: it needs a person. DataHub and OpenMetadata can hold `j.marsh` as a user, and Atlas can hold one name as text.
- keeps which meaning each owner holds: it needs a type for each owner. Of the four, only DataHub keeps one.

Each platform meets some of these readings. The requirement does not say which it means.

## Before Chapter 32

DataHub and OpenMetadata kept all three owners of `daily_sales`, Atlas one and Marquez none.

Only DataHub's ownership types let a reader tell the three apart, and only when each had its own type.

The page could not show the platforms themselves: each result is a platform's rule, as its code states it, applied here.

Chapter 32 follows the metadata of a forecast trained on the shop's data.

- Which meaning of "owner" does your platform keep?
- Can a reader of your platform tell one owner's meaning from another's?
- Which of your datasets have no owner at all?

### How this differs from a real platform

- The table and the rules come from each project's documentation and code in the version read. Each platform keeps much more than an owner.
- DataHub's list of ownership types here leaves out six that its schema marks as no longer to be used.
- Atlas has room for one owner; which of the three it holds depends on what writes it.

[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 30](chapter_30.ipynb) · [Next: Chapter 32](chapter_32.ipynb)

---

Everything runs in your browser. Nothing is sent anywhere. © 2026 Christopher Snow

