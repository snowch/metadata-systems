# Brief DC: Chapter 4, revised after its review

Chapter 4, "Metadata as a model", was reviewed by a reader on another model, and a sceptic checked
each finding (`docs/notes/chapter-04/review/findings.md`, `verdicts.md`). The cells changed too.
Revise the slots below. The current text of each slot is in `docs/notes/chapter-04/drafts/DA.md`
and `DB.md` (the slot letters there are given in brackets). Keep every sentence that the notes do
not touch, word for word; change only what the notes ask, in the same plain style. Follow
`docs/style.md` and `AGENTS.md` (attached): British English, short plain sentences, no em dashes, no
filler, nothing that personifies a system, a record, a cell, a check or a model, no narration of
what the chapter does. Keep every name in backticks exactly as written. The buttons are **Run
all**, **Run below** and **Save**.

Words you must not use: graph, node, edge, traversal, lineage, upstream, downstream, event,
observation, freshness, identity, environment, assertion, namespace, alias, provenance, data
quality, the noun "run", "lab", "engine", "Jupyter". Never refer to Jo Marsh or Sam Lund as "he" or
"she". The four terms of this chapter (entity, attribute, identifier, dataset) may not appear before
the section "What the records describe".

**One word, one meaning.** *Records* means the whole set of lines in a cell; one of them is a
*line*. Never say "a record" for one line. *Owner* is the head of the shop's word; the records'
field is `responsible`.

Write the file once. Do not change it after you reply.

## Facts (checked against the shop's data)

The first cell, now:

- It holds two sets of lines in Chapter 3's notation, each headed by a `#` note saying where its
  lines come from: your record of `daily_sales` from Chapter 3 (its five lines, with Jo Marsh as
  responsible); three lines from the head of the shop's message in Chapter 3 (the data engineer is
  responsible for `clean_customers` and `clean_orders`; Sam Lund for `products.csv`); one line from
  the orders Chapter 2 found missing on Thursday (`clean_orders drops: orders with no customer
  id`); then Jo Marsh's notes (what `sales_dashboard` means; `j.marsh` responsible for
  `sales_dashboard` and for `daily_sales`).
- The list's word is the head's, "owner"; the lines it counts are the `responsible` lines, which
  Chapter 3 defined as who to ask about an asset. The warehouse's owner, the account `etl_service`
  that Chapter 2 found, answers a different question (which account controls a table) and is not
  what the head's list asks for.
- The next cell lists every line whose field is `responsible`: 6 lines; `daily_sales` has 2 (Jo
  Marsh, from your record; `j.marsh`, from Jo's notes).
- The expectation cell asks: will the count of different `responsible` values be the number of
  people responsible, more than it, or fewer, or can you not tell yet? And how you decided.
- The count is of different values: 4 (the data engineer, Jo Marsh, `j.marsh`, Sam Lund). A count of
  values is a count of spellings. Whether Jo Marsh and `j.marsh` are one person: the head said in
  Chapter 3 that Jo Marsh built the dashboard, and the reporting tool records `j.marsh` as its
  creator. That supports one person; no line says so.
- You ask the head of the shop who `j.marsh` and `s.lund` are: `j.marsh` is Jo Marsh, in finance;
  `s.lund` is Sam Lund, in catalogue. You started today and have no line of your own yet.

What the records describe:

- An entity is a thing the records describe: a table, a file, a column, the dashboard, a person, a
  team. Each has a type. An asset (Chapter 1's word) is an entity of type `dataset` or
  `dashboard`.
- An attribute is a named property every entity of a type can have, such as `means` or `name`. A
  line gives the value of one attribute of one entity.
- An identifier is a value that names exactly one entity of its type and is used for it in every
  line. In these records Jo Marsh is named two ways; `j.marsh`, the staff login, becomes Jo Marsh's
  identifier once every line uses it. A table's name and a file's key are the identifiers of the
  shop's tables and files.
- A dataset is a file or a table: something that holds rows under named columns. Columns are
  entities of their own, of type `column`, and a column's identifier joins its dataset's identifier
  and its own name with a dot, `daily_sales.revenue_pence`. The dashboard shows values but has no
  columns, so no column belongs to it: it has its own type, `dashboard`.
- In this chapter's notation each line starts with a type, then the identifier, the attribute, a
  colon and the value. The records cell, the one that starts `records = shop.typed_records`, holds
  the first cell's lines in this notation, with the head's answer about the two logins as two
  people and their two teams.

The model and the check:

- Unchanged from the current text: what a model says; a relationship type; the model's notation and
  example; the five types.
- Before your change, the check lists 5 problems: four lines whose `responsible` value names no
  person or team the records describe (`daily_sales` Jo Marsh; `products.csv` Sam Lund;
  `clean_customers` and `clean_orders` the data engineer), and one line whose attribute the model
  does not give a dataset (`drops`).
- The merge: in the records cell (the one that starts `records = shop.typed_records`), change
  `responsible: Jo Marsh` to `responsible: j.marsh` and `responsible: Sam Lund` to
  `responsible: s.lund`, select the cell and press **Run below**. The check then lists 3 problems.
  `daily_sales` now has two identical lines, `dataset daily_sales responsible: j.marsh`: one fact,
  stated twice, so one owner. The spelling Jo Marsh stays, as the `name` of the person `j.marsh`.
- A new cell after the check counts the different `responsible` values in these records: before
  your change 4, after it 3 (`j.marsh`, `s.lund`, the data engineer): one value for each person or
  role.
- "The data engineer" is a role, not one of the two people on the head's list, and no line describes
  it. The requirement's section makes it a person or a team, by your choice.

The fact the model has no type for:

- After the merge, the check still lists the line `dataset clean_orders drops: orders with no
  customer id`. It is the rule Chapter 2 found behind Thursday's missing orders. The model gives a
  dataset no attribute `drops`.
- Two choices: leave the model as it is, and the line is refused and lost from records kept to the
  model; or add the line `dataset drops: text` to the model cell and press **Run below**: the check
  then lists 2 problems, and the model accepts the line as text. Then any dataset can have any text
  about what it drops, and no check can say whether the text is true or whether the job applies the
  rule.
- Whoever writes the model decides which facts the records can hold, and which of those a check can
  test. (Do not name a later chapter here.)

The requirement:

- The head of the shop's requirement: "Each asset has one owner."
- First, before the readings: you write in a cell what you would send the head, and what you take
  "one owner" to mean.
- Then the readings, each mapped to a column of the next cell's table:
  - as written, `one_owner`: exactly one `responsible` value for the asset;
  - one person to ask, `one_person`: exactly one value, and it names a person;
  - one team that answers for it, `one_team`: exactly one team, named directly or as the team of
    the person named.
  Each needs identifiers, so that two spellings of one owner count once.
- The cell applies your two changes if you have not made them, and makes the data engineer either a
  team or a person with the identifier `data_engineering`: the line `the_data_engineer = "team"`
  sets which, and you can change it to `"person"` and press **Run below**. It lists the 7 assets
  with their `responsible` values and the three columns.
- With the data engineer a team: `one_owner` 5 of 7, `one_person` 3, `one_team` 5. With a person:
  5, 5 and 3 (the person `data_engineering` has no team).
- `orders.jsonl` and `customers.jsonl` have no `responsible` line in the records, so they fail
  every reading. (Do not say why, or link it to the export.)
- No reading holds for all 7 assets. The head did not say which was meant. A list you send should
  say which reading it meets, and for which assets.

The close (section "## Before Chapter 5"):

- Showed: with a type on each line and identifiers for people, the count of `responsible` values
  went from 4 to 3, one for each person or role; a check can find a value that names nothing the
  records describe; the model refused a fact it had no attribute for until the model was changed;
  no reading of the requirement holds for every asset, and the two files hold none.
- Could not show: whether a line is true. The check tests a value's form and whether it names an
  entity the records describe, not whether Jo Marsh is really responsible.
- Next: the lines now point from one entity to another: a dataset to a person, a person to a team.
  Chapter 5 follows them from one entity to the next.

## Slots: what to rewrite

A. **objectives** (DA A): four items that say what the reader does: count the owners the lines
name, and find why the count is not a count of people; give two spellings of one person one
identifier, and check the records against a model; decide what to do with a fact the model has no
place for; question the requirement "Each asset has one owner." No new terms.

B1. **opening** (DA B, first part, the heading, the day and the quoted requirement): keep.

B2. **first_cell_lead** (DA B, last paragraph): what the first cell holds and where each set comes
from (facts above), and the word "owner" against `responsible` and the warehouse's account.

C. **list_lead** (DA C): one sentence: the next cell lists every line whose field is
`responsible`.

D. **count_lead** (DA D): what to write in the next cell (facts above), before you read on. The
cell does not ask: you write.

E. **count_cell** (DA E): the text inside the cell, between triple quotes: the question with the
four answers named (the number of people, more, fewer, can't tell yet), then `........`, then "How I
decided:" and `........`. At most about 60 characters a line.

F. **count_after** (DA F): the count and the four values; a count of values is a count of
spellings; the evidence on Jo Marsh and `j.marsh`, and its limit, said once; as written,
`daily_sales` has two owners; then the head's answer about the two logins, and that you have no
line yet.

G. **things** (DA G): entity (with the dashboard and the assets), attribute, identifier (facts
above; drop "and never sometimes Jo Marsh").

H. **dataset** (DA H): dataset, columns as entities, the dashboard's type (facts above).

I. **notation_lead** (DA I): "Chapter 4 writes each line" becomes "In this chapter's notation";
keep the examples and the column identifier; name the records cell by its first line; what it
holds.

J. **model_lead** (DA J): keep.

K. **check_lead** (DA K): keep.

L. **check_after** (DA L): begin "Before your change, the check lists 5 problems"; keep the list.

M. **merge** (DA M): the cell named by its first line; the edit; the 3 problems; the two identical
lines; the spelling kept as a name.

COUNT_LEAD. **count_again**: one or two sentences before the new count cell: it counts the different
`responsible` values in these records; before your change 4, after it 3, one for each person or
role.

N. **role** (DA N): two sentences (facts above): a role, not on the head's list; the requirement's
section makes it a person or a team, by your choice.

DA. **no_type** (DB A): from the facts; "refuses this line" may stay; drop the sentence on Chapter
6; replace "A model decides" with whoever writes the model deciding; replace "Anyone who keeps the
records to the model loses it" with plain words; give the instruction to try adding the attribute
and the result, 2 problems.

DB. **requirement_lead** (DB B): the requirement, then what to write in the next cell first (what
you would send and what you take "one owner" to mean). The readings move after the cell.

DC. **requirement_cell** (DB C): the text inside the cell: what list would you send the head, then
`........`; what does "one owner" mean to you, then `........`. At most about 60 characters a line.

DD. **readings**: after the cell: the three readings as a Markdown list, each with its column name
in backticks and what it needs; then that each needs identifiers, so two spellings count once.

DE. **owners_lead** (DB D): what the next cell does (facts above), including the line
`the_data_engineer = "team"` and how to change it.

DF. **owners_after** (DB E): the numbers for a team and for a person; the two files, named, with no
`responsible` line; no reading holds for all 7; the head did not say which; what the list should
say.

DG. **close** (DB F): from the facts; keep the three reflective questions, but in the second, say
"line" for one line.

DH. **reality** (DB G): keep.

Write the slots under `## A`, `## B1`, `## B2`, `## C` and so on, using exactly the slot names
above, each the exact text to place.
