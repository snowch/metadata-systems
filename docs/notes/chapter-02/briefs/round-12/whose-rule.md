# Brief: Chapter 2, whose rule "Every table must have an owner" is

Read `docs/style.md` first; its rules hold. The author asked why the head of the shop would care
whether every table has an owner: it is a data engineer's rule, not a shop owner's. The rule
becomes the learner's own. The learner is the shop's data engineer (Chapter 1), on their first
morning, and "Who should I ask about `daily_sales`?" is one of the four questions listed earlier in
this chapter. Do not say the rule is common, standard or good practice: nothing on the page
supports that. Do not name `etl_service` or say what the cell shows. Never write "field". Do not
call the Markdown table below the cell a "table" in the prose.

## Facts (each checked against the chapter)

### Slot O1: the paragraph before the cell that lists the owners (replaces the current one)

Current text: The owner the warehouse records shows how far that goes. "Who should I ask about
`daily_sales`?" wants a person or a team. The head of the shop's requirement is: "Every table must
have an owner." The cell below lists the owner of every table in the warehouse.

- Keep the first sentence as it is: "The owner the warehouse records shows how far that goes."
- "Who should I ask about `daily_sales`?" wants a person or a team.
- As the shop's data engineer, you want that question to have an answer for every table.
- So you might write a requirement for the platform: "Every table must have an owner."
- The cell below lists the owner the warehouse records for every table.

### Slot O3: the last two sentences after the readings (replaces them)

Current text: "Who should I ask about `daily_sales`?" needs the first or the second reading. The
requirement as written is met only by the fourth: every table has an owner, and the owner is an
account.

- "Who should I ask about `daily_sales`?" needs the first or the second reading.
- The warehouse meets your requirement as written by the fourth reading only: every table has an
  owner, and the owner is an account.
- So the requirement is met before you do anything, and the question you wrote it for still has no
  answer.

## Slots

Write the file `docs/notes/chapter-02/drafts/round-12/whose-rule.md` with the slots under `## O1`
and `## O3`, each the exact text to place, and nothing else in the file.
