# Brief G: drafts returned, and three new labels

Attach: `common.md`, `../facts.md`, `docs/style.md`. Write to `docs/notes/chapter-01/drafts/G.md`.

Three passages came back with a fact wrong. Each note says what was wrong; redraft only that
passage, from the facts listed, in the same format as before.

## explanationQuestions
The third paragraph of the explanation section. The first draft listed questions the fact sheet
does not have ("Who wrote the program that computed it?", "What does a cancelled order mean?").
Use only this list. Two to four sentences. Facts:
1. Your questions are about the platform around the data: what a number means, who answers for
   an asset, what made it, what reads it, and what changed.
2. None of the three systems needed those answers to store or serve the data, so none recorded
   them.
3. Some of the systems do keep records for their own work that you were not shown: the reporting
   tool keeps the query behind its chart, and something keeps the programs and their timetable.
   You will see them in later chapters.

## reflection
The chapter's last section. The first draft said storage showed who owns `daily_sales`; it did
not (it showed an account, `etl_service`, which is the chapter's point). It also added a claim
about a "strong hint" and used a long dash. Two short paragraphs and two questions. Facts, and
nothing else:
1. Storage gave you names, types, row counts, sizes, times and one account.
2. The data suggested where `daily_sales` comes from, until a copy, an edit or a failed night.
3. The program the shop really runs for `clean_orders` also drops orders with a quantity of 0 or
   less. No order this week had one, so both answers to that rule passed your tests, and no
   rebuilding from this week's data could find the rule.
4. Close with two questions for the learner to keep: what would you write down about
   `daily_sales` so that the next person need not rebuild it? Who should write it down, and when?

## c1Fields
The first draft gave the fields' internal keys, not labels a learner reads. Write four labels, one
per line, one to three words each, as `key: label`:
- source: which asset to read
- keep: which rows to keep
- measure: what to add up
- per: what to add up per (for example "per", or "for each")

## labels
Three labels the figures gained after the first brief, as `key: text`, one per line:
- recorded: the column heading over what storage recorded, beside the field's name (one word)
- yours: a column heading for the learner's own query's value, in a table that also has the
  target's value (two or three words)
- problem: template with slot {message}: a note shown in place of a figure that could not be
  shown, giving the reason {message}
