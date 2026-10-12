# Brief R: Chapter 22, "Identity across systems"

Read `docs/notes/part-5/briefs/common.md` first, and `docs/style.md`. Their rules hold here.

Terms this chapter introduces, in bold, and nowhere before the slot named: **entity resolution**
(slot D), **alias** (slot E). Terms already introduced, which you may use: precedence, identity,
qualified name, environment. Do not write: index, partition, retention, compaction.

## Facts (each checked against the shop's data)

### Slot A: objectives (a Markdown list of four, no heading)

- Read six references that six systems make to `daily_sales`, or to a thing named like it.
- Merge them by the last part of their names, and find what merged that should not.
- Merge them by qualified names, then by what each system's own configuration states.
- Question the requirement "Merge the same dataset across systems."

### Slot B: under the heading `## Six references`

- Chapter 12 tested pairs of references inside the warehouse and object storage. The shop's metadata
  system takes references from more systems than those.
- The shop's developer has started to use a transformation tool, which names each program's output as
  a model in a project: `shop_models:daily_sales`. The reporting tool names the dataset behind the
  dashboard `Daily sales`. Jo Marsh exported `daily_sales` to a CSV file in `shop-scratch`.
- The next cell lists the six references and the system each came from.

### Slot C: after that cell

- The six: the warehouse's `shop.analytics.daily_sales`; the events' namespace and name,
  `warehouse://shop-warehouse/shop.analytics.daily_sales`; the development warehouse's
  `shop_dev.analytics.daily_sales` (Chapter 12); the transformation tool's `shop_models:daily_sales`;
  the reporting tool's `dataset:Daily sales`; and object storage's `s3://shop-scratch/daily_sales.csv`.
- One rule for merging: take the last part of each name, in lower case, with spaces and hyphens read
  as underscores. References with the same last part become one.
- Before you read on, write in the next cell which references this rule will merge.

### Slot CC: the text inside that cell

One question, then `........` on its own line: which references will the rule merge? Plain text.

### Slot D: after the cell that merges by the last part

- All six become one entity. Among them are the development table, which holds other rows in another
  environment, and Jo Marsh's CSV file, a copy made at one time.
- Deciding which references name one entity is **entity resolution**. Merging too much is as much a
  fault as merging too little: the development table's runs would show in production's lineage.
- Change `"last part"` to `"qualified"` in the cell, select it and press **Run below**. This rule reads
  each warehouse name by the warehouse's rules (Chapter 12) and takes an event's namespace as the
  warehouse.
- Five entities: the warehouse's and the events' references merge; each other stays alone. The
  transformation tool's and the reporting tool's names are not warehouse names.

### Slot E: after slot D, under the heading `## What each system states`

- The transformation tool's configuration states which table each model builds: the model
  `shop_models:daily_sales` builds `shop.analytics.daily_sales`. The reporting tool's configuration
  states which table each dataset reads: `Daily sales` reads `daily_sales`.
- Another name a system uses for an asset, stated by that system, is an **alias**.
- Change the rule to `"aliases"` and press **Run below**: qualified names, then the aliases each system
  states.
- Three entities: one of four references (the warehouse, the events, the transformation tool and the
  reporting tool); the development table alone; Jo Marsh's CSV file alone.

### Slot RH: the heading of the requirement's section

Exactly `## The same dataset`. A box holding the requirement comes after this heading.

### Slot F: after the box (do not quote the requirement again)

- Before you read on, write in the next cell what "the same dataset" means to you here.

### Slot FF: the text inside that cell

One question, then `........` on its own line: what does "the same dataset" mean here? Plain text.

### Slot G: after that cell

- "The same dataset" could mean four things, each needing something different. Write them as a
  Markdown list:
  - the same name: a rule for reading names, as `last part` or `qualified`;
  - the same rows: a way to compare contents (Chapter 12);
  - the same thing to the business: someone's statement, or each system's own;
  - across environments or not: which environment holds each asset.
- `aliases` merges by what each system states it reads or builds, and keeps the environments apart. A
  reading of "the same thing to the business" might merge the development table too; a reading of
  "the same rows" might merge Jo Marsh's file on the day it was exported.
- The requirement does not say which it means.

### Slot Z: the closing (a heading `## Before Chapter 23`, a summary, a lead, three questions)

- Summary: six systems named `daily_sales`, or a thing named like it, six ways. The last part of the
  name merged all six, the development table and a copy among them. Qualified names merged two.
  Adding what each system's configuration states merged four and kept the development table and the
  copy apart.
- Chapter 23 asks what the shop's metadata system costs as the platform grows.
- Three questions, as a list: Which of your systems name the same table differently? Where does each
  state what it reads or builds? Which of your environments share table names?

Then a heading `### How this differs from a real platform` and a list:

- The transformation tool, its notation and the reporting tool's dataset are invented for the course.
- The shop's rules see six references. A real catalogue resolves thousands, and its rules are written
  per system.
