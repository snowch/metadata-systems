# Brief: Chapter 2, "What the fields are for", after the author's question

Read `docs/style.md` first; its rules hold. The author read the section headed "What the fields are
for" and asked: "What fields?" Its first sentence, "These fields exist because the systems need
them", points back across a heading to nothing the page has named. In Chapter 1, "field" means a
named value in a file's record (`customer_id`, `quantity`); here it meant what a system keeps about
an asset, a second meaning on one page. These slots replace four passages, and use "field" only for
a file's record.

## Facts (each checked against the chapter's cells)

### Slot E: replaces the paragraph after the reporting tool's cell

- Everything the three systems showed describes each asset as it is this morning.
- None of it describes how the asset got that way: which job wrote it, what it read, what its rows
  were yesterday, or who decided its rules.
- The platform records the current state of each asset and none of its history.

### Slot H: a heading, starting `## `

- Names the section's subject: why each system records what it does about an asset.

### Slot P: the section's first paragraph

- Each system records what it does about an asset because its own work needs it.
- The warehouse keeps column names and types so that it can run a query; object storage keeps a
  file's key so that it can serve the file; the reporting tool keeps the values so that it can draw
  the chart.
- In the shop's platform, a system records what its own work needs and nothing more. The questions
  you want answered are not its work.

### Slot O: the section's second paragraph

- The warehouse's owner shows how far that goes.
- "Who should I ask about `daily_sales`?" wants a person or a team.
- The requirement is: "Every table must have an owner."
- The warehouse records `etl_service` as the owner of all three tables, in the column `table_owner`
  of `information_schema.tables`.
- The name looks like an account a program logs in as, and the warehouse records nothing more about
  it.
- The column is called `table_owner`, but the question it answers is which account controls the
  table.
- The requirement is met as written, and your question is not.

## Slots

Write the file `docs/notes/chapter-02/drafts/round-10/fields.md` with the slots under `## E`, `## H`,
`## P` and `## O`, each the exact text to place, and nothing else in the file.
