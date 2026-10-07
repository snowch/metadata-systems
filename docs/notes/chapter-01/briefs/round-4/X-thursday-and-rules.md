# Brief X: the Thursday prediction and the rules prediction, as results to predict

Read `common.md` in this directory first. Write your draft to
`docs/notes/chapter-01/drafts/round-4/X.md`.

The author found that the Thursday prediction gave its explanation away: its "no" option said
that something on the way to `daily_sales` left some orders out, before the learner had any
evidence that the totals differ. It now asks only what Thursday's raw orders add up to; the lab
shows the total, and only then does the text ask what might explain the difference. The rules
prediction in Section 9 had the same fault: its options named a rule that decides no row, which is
the explanation its result gives.

## prediction

Section 3's prose, above the two questions, in Markdown. Keep its first two paragraphs exactly as
they are ("Before you open storage, answer two questions." and "The first gives you a requirement
the shop has set. It asks what you would store to meet it. Then it shows what the requirement
could mean and what the shop's warehouse holds."), and its last ("For each, choose an option,
then press the button below it."). Replace only its third paragraph, which said: "The second asks
what you expect the data to show. Each of its options is an explanation of how the platform
works, and the lab checks it." Facts for the new third paragraph:

- The second asks what you expect Thursday's orders in `orders.parquet` to add up to.
- Each of its options is a total you could expect and the belief behind it; one says you cannot
  tell yet.
- The lab adds up the orders and checks.

## p2Caption

The figure's caption, plain text, one sentence with a full stop. It replaces "Predict whether
Thursday's rows of orders.parquet add up to the dashboard's figure." Fact: predict what Thursday's
rows of orders.parquet add up to.

## p2Question

Shown above the options, before the learner commits, in Markdown, names in backticks. Facts:

- The dashboard shows 51.50 for Thursday.
- `daily_sales` holds the same figure for Thursday.
- Add up price times quantity over Thursday's rows of `orders.parquet`.
- Ask: what do you expect the total to be?

Do not say or hint whether the total differs from 51.50, or why it might.

## p2Options

The options, plain text, lower case, no full stop. Each is a total, then a colon, then the belief
behind it, in a few words. They share a form and run to about the same length. None says why a
total might differ. Facts, in this order:

- same: 51.50; the belief: `daily_sales` holds the total of Thursday's orders.
- different: a different total; the belief: `daily_sales` is not simply the total of Thursday's
  orders.

Write the names without backticks: this is plain text.

## p2Undecided

The third option, plain text, lower case, no full stop, in the same form and about the same length
as the other two. Facts: I can't tell yet; the belief: nothing so far says what daily_sales
measures.

## p2UndecidedLine

Shown after the learner chose the third option, plain text, one or two sentences, each with a
full stop. It must contain the slot `{answer}` exactly once, where the label of the option the
lab's total stands for goes. Facts: you said you could not tell yet; the lab found {answer}. It
must not call the choice right or wrong.

## p2Explain

Shown under the result, after the learner has committed, in Markdown, names in backticks, short
paragraphs. It replaces the old text, which said: "Thursday's rows of orders.parquet add up to
205.50. daily_sales has 51.50. Thursday's raw total of 205.50 is close to Wednesday's raw total
(198.75) and Friday's (204.24). In orders.parquet, Thursday was not a slow day. The table shows
the other days too. The totals are equal on three days: Monday, Friday and Sunday. They differ on
four, Thursday among them. The reason is in the rows of orders.parquet. The next section lets you
read them." Facts:

- Thursday's rows of `orders.parquet` add up to 205.50. `daily_sales` holds 51.50 for Thursday.
- So `daily_sales` is not simply the total of Thursday's orders in `orders.parquet`.
- Thursday's raw total of 205.50 is close to Wednesday's (198.75) and Friday's (204.24). In
  `orders.parquet`, Thursday was not a slow day.
- The table shows every day: the totals are equal on three days, Monday, Friday and Sunday, and
  differ on four, Thursday among them.
- Now there is a difference to explain. Ask: what might explain it?
- The next section lets you read the rows of `orders.parquet`.

Do not say what explains the difference, or where the reason is.

## p3Options

Section 9's prediction, after the learner's rules pass. The question above them reads: "Your rules
pass. Is your setting of the four rules the only one that gives `clean_orders` exactly?" The
options, plain text, lower case, no full stop, each a word for the answer, then a comma, then the
belief behind it, in a few words; they share a form and run to about the same length. They replace
"yes, because every rule you chose decides some row this week" and "no, because some rule decides
no row this week", which named the explanation the result gives. Facts, in this order:

- one: yes; the belief: a setting that gives clean_orders exactly is the only one that does.
- more: no; the belief: another setting can give exactly the same rows.

Neither may name a rule, or say that a rule decides no row, or mention quantities.
