# Brief DB: Chapter 4's fact with no type, the requirement "Each asset has one owner.", and the close

Chapter 4, "Metadata as a model", is a Jupyter notebook for a data engineer. The reader is "you".
Above these sections, the chapter has introduced four terms: an **entity** is a thing the records
describe (a table, a file, a column, a person, a team), with a type; an **attribute** is a named
property every entity of a type can have, such as `means` or `name`; an **identifier** is a value
that names exactly one entity of its type, and that every record uses for it (`j.marsh`); a
**dataset** is a file or a table of rows. You wrote a model (which types there are, which attributes
each has, and what each attribute's value is: text, or the identifier of an entity of another type),
checked the records against it, and merged two spellings of Jo Marsh into the identifier `j.marsh`.
You may use those four terms. Write each slot below, following `docs/style.md` and `AGENTS.md`
(attached): British English, short plain sentences, no em dashes, no filler, no reassurance, nothing
that personifies a system, a record or a model. Keep every name in backticks exactly as written. A
block of code is a "cell". The buttons are **Run all**, **Run below** and **Save**, in bold, and no
other control is named.

Words you must not use anywhere: graph, node, edge, traversal, lineage, upstream, downstream, event,
observation, freshness, identity, environment, assertion, namespace, alias, data quality,
provenance, the noun "run" ("run the cell" is fine), "lab", "engine", "simulator", "Jupyter",
"Pyodide". Never refer to Jo Marsh or Sam Lund with "he" or "she": repeat the name.

Write the file once. Do not change it after you reply.

## Facts (each checked against the shop's data)

The fact the model has no type for:

- After the merge, the check still reports the line `dataset clean_orders drops: orders with no
  customer id, and orders with a quantity of 0 or less`: the model gives a dataset no attribute
  `drops`.
- That line is the rule that explains Thursday's low revenue (Chapter 2), and the model has no place
  for it.
- There are two choices. Leave the model as it is: the check refuses the fact, and anyone who keeps
  the records to the model loses it. Or add the line `dataset drops: text` to the model: the check
  accepts it, as text. Then any dataset can have any text about what it drops, and no check can say
  whether the text is true, or whether the job that writes the table applies that rule.
- A model decides which facts the records can hold, and which of those a check can test.
- A fact about how an asset is made, as this one is, gets a place of its own in Chapter 6. (Do not
  name what Chapter 6 calls it.)

The requirement:

- The head of the shop's requirement: "Each asset has one owner."
- It could mean three things, each needing something different in the records:
  - one person to ask about each asset: `responsible` names a person, one value per asset;
  - one team that answers for each asset: a team for each asset, named directly or as the team of
    the person named;
  - one owner however the records spell the owner's name: identifiers, so that two spellings of one
    person count once.
- Before the next cell, you write in a cell which reading you would require in the shop's place,
  and why. Nothing marks a reading right or wrong.
- The next cell takes the records after your two changes, makes the data engineer a team with the
  identifier `data_engineering`, and lists every asset on the platform: the values of its
  `responsible` lines and, for each of three readings, `yes` or `no`: `one_owner` (exactly one
  value), `one_person` (exactly one value, a person), `one_team` (exactly one team, directly or
  through the person).
- Its result: 7 assets. 5 have one owner: every asset except `orders.jsonl` and `customers.jsonl`,
  the two files the export writes, for which nobody has told you who is responsible. 3 have one
  person: `products.csv` (`s.lund`), `daily_sales` and `sales_dashboard` (both `j.marsh`); the two
  cleaned tables name a team. 5 have one team: each asset with an owner.
- No reading is wrong. The head did not say which was meant. Whatever list you send, it meets some
  readings and not others, and it should say which it meets.

The close (section "## Before Chapter 5"):

- What the chapter's checks showed: with a type for each line and identifiers for people, the
  records can count people instead of spellings, and a check can find a value that names nothing
  the records describe. The model refused a fact it had no attribute for. The requirement is met
  under some readings and not others, and the two files the export writes have no owner under any.
- What they could not show: whether a record is true. The model checks a value's form and whether
  it names a known entity, not whether Jo Marsh is really responsible.
- Next: the records now point from one entity to another: a dataset to a person, a person to a
  team. Chapter 5 follows those references from one entity to the next.

The note "### How this differs from a real platform":

- The shop, its people, its staff list and its data are invented for the course.
- The record notation and the model notation are the course's own. Real metadata systems each define
  their own types and attributes, and Chapter 31 compares some.
- The shop uses staff logins as identifiers for people. A login can change, or be given to someone
  else after a person leaves; the shop's staff list does not record when.

## Slots

A. **no_type**: the section "## A fact the model has no type for": the line, why it matters, the two
choices and what each costs, what a model decides, and Chapter 6.

B. **requirement_lead**: the section `## "Each asset has one owner."`: the requirement, the three
readings as a Markdown list with what each needs, and what to write in the next cell.

C. **requirement_cell**: the text inside that cell, between triple quotes: a question asking which
reading you would require in the shop's place, then `........`, then a line asking why, then
`........`. At most about 60 characters a line. Plain text.

D. **owners_lead**: one or two sentences before the cell that lists the owners: what it does to the
records and what it lists.

E. **owners_after**: its result, by reading; why the two files have no owner; and that no reading is
wrong and the list should say which it meets.

F. **close**: the section "## Before Chapter 5": one short paragraph of what the checks showed and
could not show; one paragraph on Chapter 5; then two or three reflective questions as a Markdown
list, the first about a platform the reader works on, none with its answer.

G. **reality**: the note "### How this differs from a real platform", from its facts.

Write the slots under `## A` to `## G`, each the exact text to place.
