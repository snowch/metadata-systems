# Brief BV: the head's reason for the owner requirement

Read `docs/style.md` for the voice: British English, short plain sentences, no em dashes, no
filler. Write each string under its own `## BVn` heading, exactly as it will appear, and nothing
else. Do not use the word "metadata".

## The problem

Chapter 2's head of the shop sends: "Every table must have an owner. Who owns `daily_sales`?"
Later a box says "The reading the head wanted: `a_person` or `a_team`." But the head never says
what they want, or why they would ask about tables at all. The page asserts the head's intent with
no evidence. The fix: the head's message gives the reason, and the box derives the reading from
that reason.

## Facts

- Earlier the same morning the head wrote "Thursday's revenue looks wrong." The dashboard shows
  each day's revenue; `daily_sales` is the table behind it.
- The head's reason: when a number on the dashboard looks wrong, as Thursday's did, the head needs
  to know whom to ask.
- The four readings of "owner" on the page: `as_written` (a value in `table_owner`), `a_person`
  (a named member of staff), `a_team` (a named team), `the_job` (a program).
- Someone to ask is a person or a team: `a_person` or `a_team`.
- The warehouse's owner, `etl_service`, is an account; it does not meet that reading.

## BV1: the head's message, in a box

One line, in exactly this shape: `The head of the shop sends a second message: "...".` Inside the
quotation marks, in the head's voice, short: the requirement "Every table must have an owner.",
the question "Who owns `daily_sales`?", and the reason (when a number looks wrong, as Thursday's
did, the head needs to know whom to ask). The line must end with the closing quotation mark, and
the quotation must contain no other double quotation marks.

## BV2: the box that closes the section

Two or three sentences. The head's reason needs `a_person` or `a_team`: someone to ask. The account
that controls a table in the warehouse does not meet it. The last sentence must be exactly:
`The requirement becomes "Every table must name whom to ask about it."`
Do not claim to know what the head wanted beyond what the message says.
