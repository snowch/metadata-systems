# Brief: Chapter 2, the owner paragraph as evidence, then a table

Read `docs/style.md` first; its rules hold. The author asked how to make the owner paragraph's key
points stand out, and approved this: the cell that lists each table's owner comes first, then a
table of what "Every table must have an owner" could mean against whether `etl_service` answers each,
then two sentences. Do not call the Markdown table a "table" in the prose (the page's tables are the
warehouse's); call it nothing, or "the readings below". Never write "field".

## Facts (each checked against the shop's data)

### Slot O1: the paragraph before the cell that lists the owners (replaces the old owner paragraph)

- The owner the warehouse records shows how far that goes.
- "Who should I ask about `daily_sales`?" wants a person or a team.
- The head of the shop's requirement is: "Every table must have an owner."
- The cell below lists the owner of every table in the warehouse.

### Slot O2: after that cell

- The warehouse records `etl_service` as the owner of all three tables, in the column `table_owner` of
  `information_schema.tables`.
- The name looks like an account a program logs in as, and the warehouse records nothing more about
  it.
- Then a Markdown table with three columns. Write the header row with these meanings, in few words:
  what "Every table must have an owner" could mean; what it needs; whether `etl_service` answers it.
  Four rows, in this order:
  1. who is responsible for the table | a person | no
  2. which team is responsible for it | a team | no
  3. which job writes it | a program | no: it names an account, not a program
  4. which account controls it in the warehouse | an account | yes
- After it, two sentences: "Who should I ask about `daily_sales`?" needs the first or the second
  reading. The requirement as written is met only by the fourth: every table has an owner, and the
  owner is an account.

## Slots

Write the file `docs/notes/chapter-02/drafts/round-11/owner-table.md` with the slots under `## O1`
and `## O2`, each the exact text to place, and nothing else in the file.
