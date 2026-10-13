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

As in Chapters 29 and 30, none of them runs here. The next cell sets out, from each project's documentation and code in the version read, how metadata arrives in each, how it is modelled, where it is kept and how it is searched.

    >>> shop.platforms.architectures()
      | platform | metadata arrives | modelled as | kept in | searched through
      | DataHub | pulled by connectors on a schedule, or pushed | entities and aspects, in a schema language | a database: MySQL, PostgreSQL or Cassandra | a search index
      | OpenMetadata | pulled by connectors on a schedule, or pushed, through one API | JSON Schemas | a database: MySQL or PostgreSQL | a search index
      | Apache Atlas | pushed: messages from hooks in other systems, or calls to its API | a type system of entities | a graph store | a search index
      | Marquez | pushed: OpenLineage events, or calls to its API | namespaces, sources, datasets, jobs and runs | PostgreSQL | a search index, off unless set

## The owners of `daily_sales`

Chapter 27 found three owners of `daily_sales`: the account `etl_service`, the person responsible `j.marsh`, and the team `data team`.

Each platform has a rule for an owner, as its code states it:

- DataHub: a list of owners. Each owner is a user or a group, named by a URN, which is DataHub's form of name: `urn:li:corpuser:` and a user's name, or `urn:li:corpGroup:` and a group's name. Each owner has an ownership type, also named by a URN. DataHub defines four, from `urn:li:ownershipType:__system__technical_owner` to `urn:li:ownershipType:__system__none`, each with a name and a description, and an organisation can define more.
- OpenMetadata: a list of owners. Each is a user, or a team whose team type is `Group`. An owner has no ownership type.
- Atlas: one text value, `owner`, on each asset, which may be left empty.
- Marquez: no owner on a dataset. A namespace has one, and a namespace made from an OpenLineage event gets the owner `anonymous`.

Here the shop gives DataHub and OpenMetadata `etl_service` and `j.marsh` as users, and `data team` as a group in DataHub and a team of team type `Group` in OpenMetadata.

Before you read on, write in the next cell which platforms keep all three owners of `daily_sales`.

    [WRITE] Which platforms will keep all three owners of daily_sales?
    [WRITE] ........

    >>> shop.platforms.owners_in()
      | platform | owner | stored as | ownership type | its description
      | DataHub | etl_service | urn:li:corpuser:etl_service | urn:li:ownershipType:__system__technical_owner | Involved in the production, maintenance, or distribution of the asset(s).
      | DataHub | j.marsh | urn:li:corpuser:j.marsh | urn:li:ownershipType:__system__technical_owner | Involved in the production, maintenance, or distribution of the asset(s).
      | DataHub | data team | urn:li:corpGroup:data_team | urn:li:ownershipType:__system__technical_owner | Involved in the production, maintenance, or distribution of the asset(s).
      | OpenMetadata | etl_service | a user | None | None
      | OpenMetadata | j.marsh | a user | None | None
      | OpenMetadata | data team | a team of team type Group | None | None
      | Apache Atlas | etl_service | the text of `owner` | None | None
      | Marquez | None | no owner on a dataset | None | None

    >>> shop.platforms.kept()
      | platform | owners kept | owners told apart by ownership type
      | DataHub | 3 | 0
      | OpenMetadata | 3 | 0
      | Apache Atlas | 1 | 0
      | Marquez | 0 | 0

DataHub and OpenMetadata keep all three. Atlas keeps one, here the first, `etl_service`. Marquez keeps none.

Compare this with what you wrote.

The list of stored owners gives DataHub's three owners the same ownership type, `urn:li:ownershipType:__system__technical_owner`, with its description. So the count of owners below it shows none of DataHub's three told apart by ownership type. OpenMetadata's owners carry no ownership type at all.

The next cell holds `types`: the ownership type each of the three owners gets in DataHub. As it stands, each is `urn:li:ownershipType:__system__technical_owner`.

Change them so that each owner has its own ownership type: one of DataHub's four, or one of your own, written `urn:li:ownershipType:` followed by a name. Select the cell and press **Run below**.

The check below it tests that each ownership type is written as DataHub names one, and whether the three owners can be told apart by their ownership types.

The check does not test that an ownership type of your own has been defined in DataHub, as DataHub would need. That is the shop's simplification.

    >>> types = {
    >>>     "account": "urn:li:ownershipType:__system__technical_owner",
    >>>     "responsible": "urn:li:ownershipType:__system__technical_owner",
    >>>     "team": "urn:li:ownershipType:__system__technical_owner",
    >>> }

    >>> shop.platforms.check(types)
      | test | passes
      | Each ownership type is written as DataHub names one: `urn:li:ownershipType:` and a name. | yes
      | `etl_service`, `j.marsh` and `data team` share the ownership type `urn:li:ownershipType:__system__technical_owner`, so a reader cannot tell them apart. | no

    >>> shop.platforms.kept(types)
      | platform | owners kept | owners told apart by ownership type
      | DataHub | 3 | 0
      | OpenMetadata | 3 | 0
      | Apache Atlas | 1 | 0
      | Marquez | 0 | 0

    >>> shop.platforms.owners_in(types)
      | platform | owner | stored as | ownership type | its description
      | DataHub | etl_service | urn:li:corpuser:etl_service | urn:li:ownershipType:__system__technical_owner | Involved in the production, maintenance, or distribution of the asset(s).
      | DataHub | j.marsh | urn:li:corpuser:j.marsh | urn:li:ownershipType:__system__technical_owner | Involved in the production, maintenance, or distribution of the asset(s).
      | DataHub | data team | urn:li:corpGroup:data_team | urn:li:ownershipType:__system__technical_owner | Involved in the production, maintenance, or distribution of the asset(s).
      | OpenMetadata | etl_service | a user | None | None
      | OpenMetadata | j.marsh | a user | None | None
      | OpenMetadata | data team | a team of team type Group | None | None
      | Apache Atlas | etl_service | the text of `owner` | None | None
      | Marquez | None | no owner on a dataset | None | None

With three different ownership types, both tests pass. The count of owners below the check shows all 3 of DataHub's owners told apart by ownership type.

The list of stored owners below that shows each owner's ownership type, and the description of each of DataHub's own ownership types.

An ownership type tells the owners apart. Neither DataHub's names for its four nor their descriptions say which question an owner answers: `__system__business_owner` is described as "Principal stakeholders or domain experts associated with the asset(s).", not as the person to ask.

An ownership type the organisation defines carries the description the organisation gives it.

## A platform that tracks ownership

[BOX] The head of the shop's requirement: "Choose a metadata platform that tracks ownership."

Before you read on, write in the next cell what "tracks ownership" means to you here.

    [WRITE] What does "tracks ownership" mean here?
    [WRITE] ........

"Choose a metadata platform that tracks ownership" could mean three things. Each item says what it needs, then which platforms meet it:

- an owner for each dataset: it needs an owner on a dataset. DataHub, OpenMetadata and Atlas can keep one. Marquez keeps owners only on namespaces, not on datasets;
- whom to ask about each dataset: it needs a person, and a record that this person is the one to ask. DataHub can, with an ownership type defined to mean it. OpenMetadata and Atlas can hold `j.marsh`, but their rules keep no meaning with an owner, so the record does not show that `j.marsh` is the one to ask;
- which meaning each owner holds: it needs an ownership type for each owner. Of the four, only DataHub keeps one.

So DataHub can meet all three readings, OpenMetadata and Atlas the first only, and Marquez none for a dataset.

The requirement does not say which it means.

## Before Chapter 32

DataHub and OpenMetadata kept all three owners of `daily_sales`, Atlas one and Marquez none.

Only DataHub's ownership types let a reader tell the three apart, and only when each had its own ownership type. Their names and descriptions still did not say which question each owner answers.

Chapter 32 follows the metadata of a forecast trained on the shop's data.

Three questions:

- Which meaning of "owner" does your own metadata platform keep?
- Can a reader of it tell one owner's meaning from another's?
- Which of your datasets have no owner at all?

### How this differs from a real platform

- The architectures list and the owner rules come from each project's documentation and code in the version read. Each platform keeps much more than an owner.
- DataHub names an owner's ownership type in the field `typeUrn`. The shop's check takes any name after `urn:li:ownershipType:` and does not check that the ownership type has been defined. DataHub also has an older field, `type`, that its schema marks as no longer to be used.
- A comment in DataHub's schema says its web front end supports only users as owners. The schema also allows groups.
- The shop gives OpenMetadata `etl_service` as a user. OpenMetadata's rule takes any user.
- Atlas has room for one owner; which of the three it holds depends on what writes it.

[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 30](chapter_30.ipynb) · [Next: Chapter 32](chapter_32.ipynb)

---

Everything runs in your browser. Nothing is sent anywhere. © 2026 Christopher Snow

