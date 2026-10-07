# Brief V: the owner question, as a requirement to question

Read `common.md` in this directory first. Write your draft to
`docs/notes/chapter-01/drafts/round-3/V.md`.

The author wants the owner question to teach the learner to question a requirement. The figure
now runs in three steps. First it shows a requirement the shop has set, "Every table must have an
owner.", and asks what the learner would store as the owner of `daily_sales` if they wrote its
program; one of the options is to choose nothing yet and ask what the owner is for. Second, once
the learner has chosen, it shows the four questions the requirement could be asking, each beside
what it would need stored, and the learner's choice marked. Third, at a second button, it shows
what the shop's warehouse holds, and marks which of the four questions that answers. Nothing calls
the learner's choice right or wrong.

## prediction

Section 3's prose, above the two questions, in Markdown. It replaces: "Before you open storage,
answer two questions. The first asks what you would do if you wrote one of the shop's programs.
The lab then shows what the shop's warehouse holds. The second asks what you expect the data to
show. Each of its options is an explanation of how the platform works, and the lab checks it. For
each, choose an option, then press its button." Facts:

- Before you open storage, answer two questions.
- The first gives you a requirement the shop has set, and asks what you would store to meet it.
  Then it shows what the requirement could mean, and what the shop's warehouse holds.
- The second asks what you expect the data to show. Each of its options is an explanation of how
  the platform works, and the lab checks it.
- For each, choose an option, then press the button below it.

## p1Caption

The figure's caption, plain text, one sentence with a full stop, like the chapter's other
captions ("Predict whether Thursday's rows of orders.parquet add up to the dashboard's
figure."). Facts: a requirement; choose what you would store to meet it; see what it could mean;
then see what the shop's warehouse holds.

## requirementLabel

A label set small above the requirement's words, plain text, one or two words, no full stop.
Fact: what follows is a requirement, as it was written.

## p1Question

Shown under the requirement, before the learner chooses, in Markdown, names in backticks. Facts:

- Suppose you write the program that writes `daily_sales` every night.
- Ask: what would you store as the owner of `daily_sales`?

Do not restate the requirement: it is shown just above. Do not say what the shop stores, which
account the programs use, or that the requirement could mean more than one thing.

## p1Undecided

The fifth option, plain text, no full stop. The other four read "a person, for example whoever
built it", "a team, for example finance", "the program that writes it" and "an account that
programs log in as": match their form (a short phrase, lower case) and their length, so that it
does not look right because of its wording. Fact: nothing yet; first you would ask what the owner
is for.

## p1Commit

The button the learner presses once they have chosen, plain text, two to four words, no full
stop. Facts: it keeps their choice and shows what the requirement could mean. It must not say
"check", "correct", "submit" or "prediction": nothing is checked.

## p1MineUndecided

Shown after the learner chose the fifth option, plain text, one sentence, with a full stop. (For
the other four the line is "You would store {choice}.") Fact: you would not store anything yet;
you would first ask what the owner is for.

## p1Meanings

Shown under that line, above a table of the four questions, in Markdown, names in backticks,
two or three short sentences. Facts:

- Each of the four stores meets the requirement as written: each puts an owner on the table.
- Each answers a different question about `daily_sales`; the table below lists them.
- The requirement does not say which question the owner must answer, so it does not say which to
  store.

Do not say what the shop's warehouse holds: the learner has not asked yet.

## p1Asks

The table's first column, one question per row, each a full question with a question mark, names
in backticks. Facts, in this order:

- person: who is responsible for `daily_sales`?
- team: which team is responsible for `daily_sales`?
- program: which program writes `daily_sales`?
- account: which account controls `daily_sales` in the warehouse?

## p1Short

The table's second column: what each question needs stored, plain text, two to four words, lower
case, no full stop, in the same order:

- person: a person
- team: a team
- program: the program that writes it
- account: an account that programs log in as

## p1Headings

The table's three column headings, plain text, no full stop, a few words each, in this order:

- asks: the question the owner would answer
- store: what you would store for it
- answers: whether the warehouse's owner answers it (this column appears only after the second
  button)

## p1Lab

The line shown after the second button, plain text with names in backticks, one sentence with a
full stop. It must contain the slots `{value}`, `{owned}` and `{tables}` exactly once each. Facts:
the warehouse records `{value}` as the owner of `daily_sales`; it records an owner for {owned} of
its {tables} tables.

## p1Explain

Shown under that line, in Markdown, names in backticks, short paragraphs. It replaces the old
text, which said: "The warehouse records the name `etl_service` as the owner of all three tables.
`etl_service` is the account all four of the shop's programs log in as. The lab tells you this;
storage does not. If you would store a person or a team, the shop's tables have neither. So the
owner field names an account. It does not say which person or team is responsible for the table.
A field with the right name answered a different question." Facts:

- `etl_service` is the owner of all three tables. It is the account all four of the shop's
  programs log in as. The lab tells you this; storage does not.
- Every table has an owner, so the warehouse meets the requirement as written.
- The warehouse has its own meaning of "owner": the account that controls the table. Of the four
  questions in the table, `etl_service` answers only the last.
- The requirement did not say which meaning it wanted. The name of a field does not say which
  question the field answers.
- "Who should I ask about `daily_sales`?", one of the questions at the start of the chapter,
  needs a person or a team. The warehouse's owner names neither.
- Before you decide what to store, ask whoever set the requirement what the owner is for.

## modelVsRealityOwner

A new paragraph for the chapter's closing note on how the lab differs from a real platform, in
Markdown. Facts:

- In a real database a table's owner is an account too.
- In PostgreSQL, for example, a new table's owner is normally the account that created it, and
  only the owner (or a superuser) may change or drop the table or let other accounts use it.
- The lab's warehouse records the owning account and models no such rights.
