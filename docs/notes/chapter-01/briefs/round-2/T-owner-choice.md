# Brief T: the owner question, asked of the learner as the program's author

Read `common.md` in this directory first. Write your draft to
`docs/notes/chapter-01/drafts/round-2/T.md`.

The author found the owner prediction still a guess: "will the owner name someone you could ask?"
depends on how this shop set up its warehouse, which nothing on the page shows. So the question
now asks what the learner would do in the shop's place. There is no right answer: the learner
chooses, and the lab then shows what the shop's warehouse holds. Nothing may call the learner's
choice correct or incorrect.

## prediction

Section 3's prose, above the two questions. It replaces: "Before you open storage, make two
predictions. Each option is an explanation of how the platform works. Choose the one you think
more likely, then press its button to check it." Facts:

- Before you open storage, answer two questions.
- The first asks what you would do if you wrote one of the shop's programs. The lab then shows
  what the shop's warehouse holds.
- The second asks what you expect the data to show. Each of its options is an explanation of how
  the platform works, and the lab checks it.
- For each, choose an option, then press its button.

## p1Question

Shown before the learner chooses. Facts:

- Suppose you write the program that writes `daily_sales` every night.
- The warehouse keeps an owner for every table.
- Ask: what would you store as the owner of `daily_sales`?

Do not say what the shop stores, or which account the programs use.

## p1Mine

The first half of the line shown after the learner chooses, plain text, one sentence, ending with
a full stop. It must contain the slot `{choice}` exactly once, where the label of the learner's
option goes; the labels read "a person, for example whoever built it", "a team, for example
finance", "the program that writes it" and "an account that programs log in as". Fact: you would
store {choice}.

## p1Lab

The second half of that line, plain text, one sentence, ending with a full stop. It must contain
the slot `{answer}` exactly once, where one of the same labels goes. Fact: the shop's warehouse
holds {answer}. It must not say whether the two match, or that either is right.

## p1Explain

Shown after the learner chooses, under that line. It replaces the old text, which said: "The
warehouse records the name `etl_service` as the owner of all three tables. `etl_service` is the
account all four of the shop's programs log in as. The lab tells you this; storage does not. So
the owner field names an account. It does not say which person or team is responsible for the
table. A field with the right name answered a different question." Keep all of it, and add one
fact at the start of its second paragraph:

- If you would store a person or a team, the shop's tables have neither.

## p1Caption

The figure's caption, plain text, one sentence, ending with a full stop. Facts: choose what you
would store as the owner of daily_sales; then see what the shop's warehouse holds.
