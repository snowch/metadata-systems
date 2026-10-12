# Brief: Chapter 2, the paragraph after the readings of "Every table must have an owner."

Read `docs/style.md` first; its rules hold. The author found the current paragraph very unclear:

> "Who should I ask about `daily_sales`?" needs the first or the second reading. The warehouse
> meets your requirement as written. It does so on the fourth reading only: every table has an
> owner, and the owner is an account. So the requirement is met before you do anything, and the
> question the requirement was written for still has no answer.

Its faults: it points at rows of the list above by number ("the first or the second reading",
"the fourth reading"), so the reader has to look back to decode it; and "meets your requirement as
written" beside "on the fourth reading only" reads as a contradiction.

## What comes just before it

The learner has adopted the rule "Every table must have an owner." so that "Who should I ask about
`daily_sales`?" has an answer for every table. A cell listed each table's owner. Then: "The
warehouse records `etl_service` as the owner of all three tables ... The name looks like an
account a program logs in as", and a list of four things the rule could mean, each with what it
needs and whether `etl_service` answers it: who is responsible for the table (a person: no); which
team is responsible for it (a team: no); which job writes it (a program: no, it names an account,
not a program); which account controls it in the warehouse (an account: yes).

## Facts, in this order

- To answer "Who should I ask about `daily_sales`?" you need a person or a team responsible for
  the table.
- The rule's words are already met: the warehouse records an owner for every table, so every table
  has an owner, and you did nothing to make it so.
- But that owner is an account, `etl_service`. It says only which account controls the table in the
  warehouse.
- So the rule is met, and you still do not know whom to ask about `daily_sales`.

## Rules

- Name each reading by what it is (a person, a team, an account), never by its position ("the
  first", "the fourth").
- Do not say "as written" or "as meant"; say what is met and what is not.
- No closing slogan or moral. Three or four short sentences.

## Output

Write the file `docs/notes/chapter-02/drafts/round-14/after-readings.md` holding only the paragraph.
