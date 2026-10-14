# Brief BW: the head asks in the shop's terms; you write the rule

Read `docs/style.md` for the voice: British English, short plain sentences, present tense, no em
dashes, no filler. The reader is "you", the shop's new data engineer. Write each string under its
own `## BWn` heading, exactly as it will appear, and nothing else. Do not use the word "metadata".

## The problem

Chapter 2 now has the head of the shop write: "Every table must have an owner. Who owns
`daily_sales`? When a number looks wrong, as Thursday's did, I need to know whom to ask." The head
runs a shop that sells bicycle parts. The head knows the dashboard and its numbers, not the
warehouse's tables or their names. The fix: the head asks in the shop's terms, and you, the data
engineer, turn that into a rule for the platform about tables.

## Facts

- Earlier the same morning the head wrote "Thursday's revenue looks wrong." The dashboard shows
  each day's revenue.
- The head's new message: when a number on the dashboard looks wrong, as Thursday's did, the head
  needs to know whom to ask about it.
- You turn that into a rule for the shop's platform: "Every table must have an owner."
- Later on the page: the warehouse records `etl_service` as every table's owner, an account the
  nightly programs log in as. The readings of "owner": `as_written`, `a_person`, `a_team`,
  `the_job`. Someone to ask is a person or a team.

## BW1: one or two sentences, plain text, under the section's heading

The head's second message, quoted in the head's own voice. No table names, no backticks, nothing
about tables or the warehouse: the head speaks of the dashboard's numbers and whom to ask.

## BW2: one line, in a box

Say that you turn the head's request into a rule for the shop's platform, then quote the rule. The
line must end exactly with: "Every table must have an owner."

## BW3: two or three sentences, in a box that closes the section

What the head asked for (someone to ask when a number looks wrong) needs `a_person` or `a_team`.
The warehouse's owner, `etl_service`, is an account, and does not meet that reading. The last
sentence must be exactly:
`Your rule becomes "Every table must name whom to ask about it."`
