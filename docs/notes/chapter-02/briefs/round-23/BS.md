# Brief BS: the owner rule, rewritten to say what it is for

Read `docs/style.md` for the voice: British English, active voice, short plain sentences, no em
dashes, no filler, no reassurance, no meta-commentary ("notice", "this shows"), no slogans. The
reader is "you", a software or data engineer. Do not use the word "metadata". Write each string
under its own `## BSn` heading, exactly as it will appear, and nothing else.

## Where this goes (context, do not repeat it)

Earlier in Chapter 2 a box reads: Data teams often adopt a rule so that every table has someone to
ask about it: "Every table must have an owner." The learner adopted the rule for the shop. The
warehouse records `etl_service` as the owner of all three tables. A table then gives four things
"owner" could mean: who is responsible for the table (a person), which team is responsible for it
(a team), which job writes it (a program), which account controls it in the warehouse (an
account); `etl_service` answers only the last. The paragraph just above the new text ends: "The
rule is met as written: the warehouse fills in an owner for every table by itself. The owner it
found answers only the last reading, which account controls the table, so you still do not know
whom to ask about `daily_sales`."

## BS1: one or two sentences before the new box

Facts:
- The rule said "an owner", a word with four meanings in the table, and did not say which one it
  wanted.
- So you rewrite your rule to say what it is for: someone to ask about the table.

## BS2: the text of a box that states the rewritten rule

One sentence, starting "Your rule, rewritten:" and then the rule in double quotes. The rule says:
every table must name whom to ask about it, and the account that controls the table in the
warehouse does not count as that. Do not say "person" or "team": the rule leaves open which, on
purpose. At most about 30 words in all.

## BS3: one sentence after the box

Fact: nothing on the shop's platform meets the rewritten rule yet, because no system records whom
to ask about a table. Do not mention later chapters.
