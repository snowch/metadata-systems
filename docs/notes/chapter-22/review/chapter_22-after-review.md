[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 21](chapter_21.ipynb) · [Next: Chapter 23](chapter_23.ipynb)

# Chapter 22: Identity across systems

**Objectives**

- Read six references to `daily_sales`, or to a table or file named like it, and where each comes from.
- Merge them by the last part of their names, and find what merged that should not.
- Merge them by qualified names, then by what two systems' configurations declare.
- Question the requirement "Merge the same dataset across systems."

The platform map shows the shop's three systems and the returns desk, as Chapter 7 left them.

## Six references

A reference is the name one system uses for an asset. Chapter 12 tested pairs of references inside the warehouse and object storage. The shop's metadata system takes references from more places than those.

The shop's developer has started using a transformation tool. The tool names each program's output as a model in a project. The project is `shop_models`, so the output `daily_sales` is `shop_models:daily_sales`.

The reporting tool names the dataset behind the dashboard `Daily sales`, written with the prefix `dataset:`.

Jo Marsh exported `daily_sales` to a CSV file in `shop-scratch`.

The events name a dataset by a namespace and a name (Chapter 8). The development table is Chapter 12's, in `shop_dev`, a second database of the warehouse.

The next cell lists the six references, and where each came from.

    >>> shop.aliases.references()
      | system | reference
      | warehouse | shop.analytics.daily_sales
      | events | warehouse://shop-warehouse/shop.analytics.daily_sales
      | development warehouse | shop_dev.analytics.daily_sales
      | transformation tool | shop_models:daily_sales
      | reporting tool | dataset:Daily sales
      | object storage | s3://shop-scratch/daily_sales.csv

This is the rule for merging: take the last part of each name, in lower case, with spaces and hyphens read as underscores, and a file's extension left off. References with the same last part become one.

Before you read on, write in the next cell which references this rule will merge.

    [WRITE] Which of the six references will this rule merge?
    [WRITE] ........

    >>> shop.aliases.merge("last part")
      | entity | references | systems
      | 1 | 6 | warehouse, events, development warehouse, transformation tool, reporting tool, object storage

Under that rule, all six become one entity. Among them are the development table, which holds other rows in another environment (Chapter 12), and Jo Marsh's CSV file, a copy made at one time.

Compare this with what you wrote.

Deciding which references name one entity is **entity resolution**.

If it merges too much, the development table's runs show in production's lineage (Chapter 12). If it merges too little, the model, the reporting tool's dataset and the table stay three entities, and what each system records about one is not joined to what the others record.

In the cell, change `"last part"` to `"qualified"`. Select the cell and press **Run below**. The qualified rule reads each warehouse name by the warehouse's rules (Chapter 12), and it takes an event's namespace as the warehouse.

The result has five entities. The warehouse's reference and the events' reference merge into one.

The other four each stay alone: the development table is in another database; the CSV file's name is an object's key in storage, not a warehouse name; the transformation tool's and the reporting tool's names are not warehouse names.

## What each system states

The transformation tool's configuration declares that the model `shop_models:daily_sales` stands for the table `shop.analytics.daily_sales`. The reporting tool's configuration declares that the dataset `Daily sales` stands for the table `daily_sales`.

Taking those declarations to name the table itself is the shop's choice.

Another name a system declares for an asset is an **alias**.

A dataset that filtered the table's rows, or added them up, would not be an alias of the table. A rule that merged it with the table would merge two different assets.

In the cell, change the rule to `"aliases"`. Select the cell and press **Run below**. The `aliases` rule merges by qualified names first, then by the aliases each system declares.

The result has three entities. One of them holds four references: the warehouse's, the events', the transformation tool's and the reporting tool's. The development table is alone. Jo Marsh's CSV file is alone.

## The same dataset

[BOX] The head of the shop's requirement: "Merge the same dataset across systems."

Before you read on, write in the next cell what "the same dataset" means to you here.

    [WRITE] What does "the same dataset" mean here?
    [WRITE] ........

"The same dataset" could mean four things, and each needs different information.

- The same name: it needs a rule for reading names. Met for warehouse names, by the qualified rule. The other references' names alone do not merge.
- The same rows: it needs a comparison of contents (Chapter 12). No rule here compares contents, so this reading is not tested.
- The same thing to the business: it needs a statement of what each name stands for. Met only as far as the two configurations declare it, which is the shop's choice.
- The same across environments: it needs to know which environment holds each table. The `aliases` rule keeps the development table apart.

The requirement does not say which it means.

## Before Chapter 23

Six references name `daily_sales`, or a table or file named like it. The last part of each name merged all six, the development table and the copy among them. Qualified names merged two. Adding what two configurations declare merged four, and kept the development table and the copy apart.

The rules decided from names and from what two configurations declare. Nothing compared contents, and nothing checked that the configurations are right.

Chapter 23 asks what the shop's metadata system costs as the platform grows.

- Which of your systems name the same table differently?
- Where does each of your systems declare what a name stands for?
- Which of your environments share table names?

### How this differs from a real platform

- The transformation tool, its notation, the reporting tool's dataset and Jo Marsh's export are invented for the course.
- A real catalogue resolves references with rules written for each system. A producer can also state other names for a dataset in its events: OpenLineage defines a `symlinks` dataset facet for these.

[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 21](chapter_21.ipynb) · [Next: Chapter 23](chapter_23.ipynb)

---

Everything runs in your browser. Nothing is sent anywhere. © 2026 Christopher Snow

