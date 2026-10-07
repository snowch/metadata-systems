# Brief Z: figures that say what they ask, and an instrument with a question in front of it

Read `docs/notes/chapter-01/briefs/round-4/common.md` first, and the files it names: every rule
there holds for this brief. Write your draft to `docs/notes/chapter-01/drafts/round-6/Z.md`.

The author found that every figure on the page carried the same badge, "Lab", so a map, a browser
of the assets and an experiment looked alike. Each figure now says in its badge what it asks of
the learner: an experiment, an instrument to inspect with, or a reference. And the browser of the
assets is now an instrument for a question: the investigation opens with a decision about which
asset to inspect first, and the browser opens on it. The facts are in
`docs/notes/chapter-01/facts.md`, under "Where to look first".

## roleLabels

The badge on each figure, plain text, one word each, capitalised, no full stop. The page sets
badges in small capitals. Facts, in this order:

- experiment: the learner decides or predicts, then acts, and the evidence answers
- inspect: the learner examines what the platform holds, to find evidence
- reference: something the learner has been told, kept to hand

## roleBadgeLabel

The badge's name for a screen reader, plain text, a few words, no full stop. It must contain the
slot `{role}` exactly once, where the badge's word goes. Fact: what this figure asks of you is
{role}.

## roleNotes

What the badge opens, one short paragraph per role, in Markdown. Under each, the page goes on with
a note on the Metadata Lab itself, so do not describe the lab. Facts:

- experiment: you commit first, to a prediction, a choice or a query you build; then you act, and
  the lab's evidence answers; what you take away is what the evidence shows beside what you
  expected.
- inspect: an instrument: it shows what the platform holds, and answers no question by itself;
  use it on the question the page has just asked, and look for the evidence that question needs.
- reference: what you have been told about the platform, kept to hand; it asks nothing of you.

## wCaption

The decision's caption, plain text, one sentence with a full stop, like the chapter's other
captions ("Choose the explanation you will test for the difference on Thursday."). Fact: decide
which asset you will inspect first, and what you will look for there.

## wQuestion

Shown above the options, in Markdown, names in backticks. Facts:

- Thursday's orders in `orders.parquet` add up to 205.50; `daily_sales` and the dashboard hold
  51.50.
- Somewhere between them, the total became 51.50.
- Ask: which asset would you inspect first to find where, and what would you look for there?

Do not say which asset is made from which, or where the total changed.

## wOptions

The four options, plain text, lower case except where a name needs otherwise, no full stop. Each
is an asset, then a comma, then the evidence you would look for there, in a few words; they share
a form and run to about the same length. Facts, in this order:

- orders: orders.parquet; for the orders that make up Thursday's 205.50
- clean: clean_orders; to set its Thursday orders beside the raw ones
- daily: daily_sales; for how its 51.50 was worked out
- dashboard: the dashboard; for where its 51.50 comes from

## wCommit

The button the learner presses once they have chosen, plain text, two to four words, no full
stop. Facts: it keeps their choice and opens the inspector below on that asset. It must not say
"check", "correct" or "prediction".

## wMine

Shown after the choice, plain text, one sentence with a full stop. It must contain the slot
`{choice}` exactly once, after a colon. Fact: you will start with {choice}.

## wAfter

One line for each option, shown after the choice, in Markdown, names in backticks. Each says what
that asset can show: a fact about the asset's shape, never what it shows for Thursday. Facts, in
this order:

- orders: `orders.parquet` keeps one row per order, with its price, quantity and status. It shows
  what Thursday's 205.50 is made of. It does not say which orders `daily_sales` counts.
- clean: `clean_orders` keeps one row per order too, with the same columns as `orders.parquet`.
  Set beside it, it shows which orders the two hold differently.
- daily: `daily_sales` keeps one row per day: the day and its revenue. It shows 51.50, and not
  which orders make it up.
- dashboard: the dashboard keeps the values it shows, one per day. It shows 51.50, and nothing
  about orders.

## wNext

Shown after that line for every option, plain text, one sentence with a full stop. Fact: the
inspector below opens on it; look there, then at any other asset.

## inspectorCaption

The inspector's caption, plain text, one sentence with a full stop. It replaces "Browse the seven
assets and what storage records about each.", which presented the inspector as the activity
itself. Facts: inspect what storage records about each asset; start with the one you chose.

## inspectorLead

Shown above the inspector, in Markdown, names in backticks. It replaces: "Choose an asset from the
list. The figure shows what storage records about it: its record, what storage says about eight
questions, its columns and their types, and its rows. The figure asks every asset the same eight
questions. Then try one of these: [a list]". Keep the list exactly as it is, except its first
item, which now reads "find the rows of `orders.parquet` that make Thursday's total differ from
`daily_sales`;". Facts for the sentences above the list:

- The inspector is your instrument for the question above: where could Thursday's difference
  have entered?
- Choose an asset from the list. It shows what storage records about it: its record, what storage
  says about eight questions, its columns and their types, and its rows.
- It asks every asset the same eight questions.
- Then try one of these:

## p2ExplainEnd

The last two paragraphs of the Thursday prediction's explanation, in Markdown, names in
backticks. They replace: "Now there is a difference to explain. What might explain it?" and "The
next section lets you read the rows of `orders.parquet`." Facts:

- Now there is a difference to explain.
- First, where to look: the next section starts there.
