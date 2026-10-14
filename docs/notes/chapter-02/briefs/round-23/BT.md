# Brief BT: the owner readings' table, as alternatives

Read `docs/style.md` for the voice: British English, plain, short, no em dashes, no filler. Write
each string under its own `## BTn` heading, exactly as it will appear, and nothing else. Do not use
the word "metadata".

## The problem

Chapter 2 shows this table after the learner finds that the warehouse records `etl_service` as the
owner of every table:

| What the rule could mean | What it needs | Does `etl_service` answer it? |
| --- | --- | --- |
| who is responsible for the table | a person | no |
| which team is responsible for it | a team | no |
| which job writes it | a program | no: it names an account, not a program |
| which account controls it in the warehouse | an account | yes |

The author found that the table reads as if all four rows are requirements, things the rule asks
for together. They are not: each row is one alternative reading of the single word "owner" in the
rule "Every table must have an owner.", and each reading asks for a different thing. Right after
the table the learner rewrites the rule to choose what it is for (someone to ask).

## BT1: one sentence, just above the table

It says that the word "owner" in the rule can be read in four ways, each a different question that
needs a different thing recorded, and that the table gives one reading per row. At most 30 words.

## BT2: the table's three column headings

Write them so that a reader takes each row as one alternative reading, not as one of several
things required. Keep them short (at most six words each). The third heading must keep
`etl_service` in backticks and ask whether it answers that reading. Give them as one Markdown table
header line, e.g. `| ... | ... | ... |`. Do not change the rows.
