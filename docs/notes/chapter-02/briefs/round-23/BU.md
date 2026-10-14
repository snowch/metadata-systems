# Brief BU: the owner requirement, questioned as Chapters 3 and 4 question theirs

Read `docs/style.md` for the voice: British English, active voice, present tense, short
declarative sentences, no em dashes, no filler, no reassurance, no slogans, no meta-commentary
("notice", "this section", "this chapter"). The reader is "you", a software or data engineer. Do
not use the word "metadata". Write each string under its own `## BUn` heading, exactly as it will
appear, and nothing else.

## Context (do not repeat it)

Chapter 2: the head of the shop wrote "Thursday's revenue looks wrong." The learner compares each
day's raw orders in `orders.jsonl` with `daily_sales`, reads what each system records about its
assets, then tests an explanation. Partway through, the head sends a second message, shown in a
box: "Every table must have an owner. Who owns `daily_sales`?" Then: "The warehouse has a column
that looks like the answer. The cell below reads it." The cell lists `table_name` and
`table_owner` from the warehouse's `information_schema.tables`.

## BU1: the chapter's objectives, a bulleted list under "**Objectives**"

Four bullets, imperative, one line each, in the style of Chapter 3's:
"- Write a record of `daily_sales` from what the shop's people tell you."
"- Find which of Chapter 2's four questions the record answers."

Facts, one bullet each, in this order:
1. Compare each day's raw orders with `daily_sales`, and find which orders Thursday's total leaves
   out.
2. Read what each of the shop's systems records about its assets, and find what those records do
   not say: which job wrote an asset, and what it read.
3. Write this bullet exactly: `- Question the requirement "Every table must have an owner."`
4. Test an explanation of how `daily_sales` is made, and find what a query that rebuilds it
   cannot show.

## BU2: one paragraph after the cell's result

Facts:
- The warehouse records `etl_service` in `table_owner` for all three tables.
- `etl_service` is the account the shop's nightly jobs log in as: four programs run each night,
  each logged in as `etl_service`.
- So the requirement is met as written: every table has an owner.
Do not say whether this answers the head's question. At most three sentences.

## BU3: one sentence, in a box above a cell the reader edits

The cell holds two questions with dots to replace: "What would you send the head?" and "What do
you take "owner" to mean?". Tell the reader to write their answers in the cell below, and that the
readings follow the cell. Model it on Chapter 4's: "In the cell below, write what you would send
the head, and what you take "one owner" to mean. The readings follow the cell."

## BU4: one short paragraph after the list of readings

This is the first time the course questions a requirement this way; later chapters do it without
explaining. Facts, in this order:
- A requirement as written is met by whatever the platform already holds.
- Each reading of it asks for a different thing to be recorded.
- Your work is to say which reading was meant, and to record what that reading needs.
At most three sentences.
