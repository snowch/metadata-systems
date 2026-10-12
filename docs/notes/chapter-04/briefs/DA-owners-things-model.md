# Brief DA: Chapter 4's opening, the list of owners, the things the records describe, and the model

Chapter 4, "Metadata as a model", is a Jupyter notebook for a data engineer. The reader is "you". In
Chapter 3 you wrote records about the shop's assets: lines of text, one fact per line (`asset`, a
column if the fact is about one, a field, a colon, a value), with fields such as `means`,
`responsible` and `unit`. Write each slot below, following `docs/style.md` and `AGENTS.md`
(attached): British English, short plain sentences, no em dashes, no filler, no reassurance, nothing
that personifies a system or a record. Keep every name in backticks exactly as written. A block of
code is a "cell". The buttons are **Run all**, **Run below** and **Save**, in bold, and no other
control is named.

Words you must not use anywhere: graph, node, edge, traversal, lineage, upstream, downstream, event,
observation, freshness, identity, environment, assertion, namespace, alias, the noun "run" ("run
the cell" is fine), "lab", "engine", "simulator", "Jupyter", "Pyodide". Never refer to Jo Marsh or
Sam Lund with "he" or "she": repeat the name.

This brief introduces four terms, each where its slot says: **entity**, **attribute**,
**identifier** and **dataset**. Give the plain idea first, then the term. Do not use any of the four
before its slot.

Write the file once. Do not change it after you reply.

## Facts (each checked against the shop's data)

The opening:

- It is still Monday 14 September 2026, late in the afternoon.
- The head of the shop sends you a requirement: "Each asset has one owner. Send me the list."
- You have your records from Chapter 3. Jo Marsh, in finance, has sent the notes Jo keeps about the
  dashboard and `daily_sales`. The first cell puts both together, in Chapter 3's notation: yours
  first, then Jo's.
- Yours say who is responsible for `daily_sales` (Jo Marsh), for `clean_customers` and `clean_orders`
  (the data engineer, which is you), and for `products.csv` (Sam Lund); what `daily_sales` means; the
  unit of `revenue_pence`; and what `clean_orders` drops (orders with no customer id, and orders
  with a quantity of 0 or less, which Chapter 2 said are the rules of the job that writes it).
- Jo's say what `sales_dashboard` means (revenue per day, for the last 7 days), and that `j.marsh`
  is responsible for `sales_dashboard` and for `daily_sales`.
- The next cell lists every `responsible` line: 6 lines, 2 of them for `daily_sales` (Jo Marsh, from
  your records; `j.marsh`, from Jo's).
- Before the cell after it, you write in a cell how many people are responsible for the shop's
  assets, according to these records, and how you counted.
- That cell counts the different values of `responsible`: 4. They are: the data engineer, Jo Marsh,
  `j.marsh` and Sam Lund.
- Whether Jo Marsh and `j.marsh` are one person: the head of the shop said in Chapter 3 that Jo
  Marsh built the dashboard, and the reporting tool records `j.marsh` as the dashboard's creator.
  That supports one person. To the records, each is a piece of text, so they cannot say whether two
  pieces of text name one person. The count is of spellings, not people. As written, `daily_sales`
  has two owners.
- You ask the head of the shop for the staff list. It has two lines: `j.marsh` is Jo Marsh, in
  finance; `s.lund` is Sam Lund, in catalogue. So `j.marsh` and Jo Marsh are one person.

The things the records describe:

- To count people, the records must describe people, and each line must say what kind of thing it
  describes.
- A thing the records describe is an **entity**: a table, a file, a column, a person, a team. Each
  entity has a type.
- A named property that every entity of a type can have, such as `means` or `name`, is an
  **attribute**. A line gives the value of one attribute of one entity.
- A value that names exactly one entity of its type, and that every record uses for it, is an
  **identifier**: `j.marsh`, and not sometimes Jo Marsh. The staff logins (`j.marsh`, `s.lund`) are
  such values; so are a table's name in the warehouse and a file's key in object storage.
- Files and tables both hold rows under named columns, and the same attributes describe them: what
  they mean, who is responsible, their columns. One type covers both: a **dataset**, a file or a
  table of rows. The dashboard holds no rows of its own, so it has a type of its own, `dashboard`.
- In Chapter 4's notation each line starts with the type, then the identifier, the attribute, a
  colon and the value: `dataset daily_sales responsible: j.marsh`, `person j.marsh name: Jo
  Marsh`. A column's identifier is its table's name and its own name joined by a dot:
  `daily_sales.revenue_pence`.
- The records cell holds the same records in this notation, with the staff list added: a person for
  each login, with a name and a team, and a team for each of the two teams.

The model:

- A model says which types there are, which attributes each type has, and what each attribute's
  value is: text, or the identifier of an entity of another type.
- An attribute whose value names another entity relates the two: `responsible` relates a dataset or
  the dashboard to a person or a team. That is a relationship type. (Plain words: "a relationship
  type".)
- The model's notation: one line per attribute: the type, the attribute, a colon, and what its value
  is (`text`, or one or more type names joined by `or`). Example: `dataset responsible: person or
  team`.
- The model cell defines five types: `dataset`, `column`, `dashboard`, `person`, `team`.
- The check cell lists every line whose type or attribute the model does not have, and every value
  that should be the identifier of a person or team and is not.
- Its result: 5 problems. Four lines name no person or team the records describe: `daily_sales`
  responsible Jo Marsh; `products.csv` responsible Sam Lund; `clean_customers` and `clean_orders`
  responsible the data engineer. One line has an attribute the model does not give a dataset:
  `drops`, on `clean_orders`.
- The merge: in the records cell, change `responsible: Jo Marsh` to `responsible: j.marsh` and
  `responsible: Sam Lund` to `responsible: s.lund`, select the cell and press **Run below**. The
  check then lists 3 problems. The two `responsible` lines of `daily_sales` now give the same value,
  so `daily_sales` has one owner. The spelling Jo Marsh is kept, as the `name` of the person
  `j.marsh`.
- "The data engineer" is a role: it is not in the staff list and no record describes it. Whether it
  should name a person or a team depends on what "one owner" means, and a later section of the
  chapter returns to it.

## Slots

A. **objectives**: Chapter 4's objectives, a Markdown list of four items, each starting with a
verb, none using the four new terms: count the owners the records name, and find why the count is
not a count of people; rewrite the records so each line says what kind of thing it describes;
write a model the records can be checked against, and merge two spellings of one owner; question
the requirement "Each asset has one owner."

B. **opening**: the section "## Who owns what": the day, the head's requirement quoted as a
message, and what the first cell holds.

C. **list_lead**: one sentence before the cell that lists every `responsible` line.

D. **count_lead**: after the list: what to write in the next cell before running the cell after it.

E. **count_cell**: the text inside that cell, between triple quotes: a question asking how many
people are responsible for the shop's assets according to these records, then `........`, then
"How I counted:" (or similar) and `........`. At most about 60 characters a line. Plain text.

F. **count_after**: after the counting cell: the count and the four values; whether Jo Marsh and
`j.marsh` are one person, the evidence and its limit; the count is of spellings; as written,
`daily_sales` has two owners; then the staff list, which settles it.

G. **things**: the section "## What the records describe": introduces **entity**, **attribute** and
**identifier**, in that order, from the facts.

H. **dataset**: introduces **dataset** and the type `dashboard`.

I. **notation_lead**: Chapter 4's notation, with its examples and the column identifier, and what
the next cell holds.

J. **model_lead**: the section "## A model of the records": what a model says; a relationship type;
the notation, with its example; what the model cell defines.

K. **check_lead**: one or two sentences before the check cell.

L. **check_after**: the check's 5 problems, grouped as in the facts.

M. **merge**: what to change in the records cell, and what the check then shows; one owner for
`daily_sales`; the spelling kept as a name.

N. **role**: two sentences on "the data engineer" (facts above).

Write the slots under `## A` to `## N`, each the exact text to place.
