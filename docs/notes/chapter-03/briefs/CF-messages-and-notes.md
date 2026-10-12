# Brief CF: three check messages, and the notes in Chapter 4's first cell

British English, no em dashes, no "error", "invalid" or exclamation marks; nothing that makes a
check sound like a person. Keep every name in backticks exactly as written. Do not use the words
lab, engine, graph, node, edge, lineage, identity, event.

Write the file once. Do not change it after you reply.

## Facts

Chapter 3's check prints one row per problem. A reader's record is a set of lines; one line is a
fact about an asset or a column (`daily_sales revenue_pence means: the value of the day's completed
orders`). A column's description is a line with the field `means`. A value of dots (`........`) is
one the reader has not written yet. On this page "record" means the reader's whole set of lines,
never one line. The check now tells two cases apart:

- the record has no `means` line for the column at all;
- the record has a `means` line for the column, but its value is still dots.

Chapter 4's check: a value should be the identifier of something of a type (for example "person or
team", which a placeholder `{types}` stands for), and no line of the records describes such a thing
with that identifier. In Chapter 4, "records" is the whole set and one of them is a "line".

Chapter 4's first cell holds lines in four groups, each headed by a note (a line starting with `#`,
which the check ignores):

1. the reader's own record of `daily_sales`, written in Chapter 3;
2. three lines taken from the head of the shop's message in Chapter 3;
3. one line from the orders Chapter 2 found missing on Thursday;
4. Jo Marsh's notes (Jo Marsh works in finance).

## Write

1. **no_description**: the message for a column with no `means` line in the record. One short
   sentence.
2. **unwritten**: the message for a column whose `means` line still has dots as its value. One
   short sentence.
3. **no_thing**: Chapter 4's message; it must contain `{types}` exactly. Say "line", not "record",
   for one line.
4. **notes**: the four `#` notes, each a short phrase after `# `, under 60 characters.

Write them under `## 1` to `## 4` (the four notes as a list under `## 4`).
