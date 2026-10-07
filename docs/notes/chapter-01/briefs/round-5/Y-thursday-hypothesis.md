# Brief Y: an explanation for Thursday, chosen, tested and checked

Read `docs/notes/chapter-01/briefs/round-4/common.md` first, and the files it names: every rule
there holds for this brief. Write your draft to `docs/notes/chapter-01/drafts/round-5/Y.md`.

The Thursday prediction now shows the learner a difference (205.50 against 51.50) and asks what
might explain it. The author wants the learner to answer that by investigating, not by guessing
and being told. So the investigation section opens with a choice of which explanation to test; the
learner tests it with the inspector and, in the next section, the query builder; and after their
query rebuilds `daily_sales`, a check reads the rows and says which explanations they support. The
facts are in `docs/notes/chapter-01/facts.md`, under "Testing an explanation for Thursday". The
check must not say why the orders were left out, or that they have no customer id: the chapter's
last challenge asks the learner to find that.

## hCaption

The choice's caption, plain text, one sentence with a full stop, like the chapter's other captions
("Predict what Thursday's rows of orders.parquet add up to."). Fact: choose the explanation you
will test for the difference on Thursday.

## hQuestion

Shown above the options, in Markdown, names in backticks. Facts:

- Thursday's orders in `orders.parquet` add up to 205.50, and `daily_sales` holds 51.50.
- Ask: which explanation will you test?

## hOptions

The three options, plain text, lower case, no full stop, each a short explanation, in the same
form and about the same length. Facts, in this order:

- left: some of Thursday's orders are not counted in daily_sales
- lower: Thursday's orders are counted, but at lower values
- moved: some of Thursday's orders are counted on another day

Write the names without backticks: this is plain text.

## hCommit

The button the learner presses once they have chosen, plain text, two to four words, no full
stop. Fact: it keeps the explanation they will test. It must not say "check", "correct" or
"prediction": nothing is checked yet.

## hMine

Shown after the choice, plain text, one sentence with a full stop. It must contain the slot
`{choice}` exactly once, where the option's label goes. Fact: you will test {choice}.

## hTest

Shown under that line, in Markdown, names in backticks, two or three short sentences. Facts:

- Read Thursday's rows in the inspector below.
- In the next section, the query builder adds up an asset's rows and compares each day with
  `daily_sales`.
- Once your query rebuilds `daily_sales`, a check at the end of that section reads the rows and
  says which explanations they support.

Do not say which explanation the rows will support, or name `clean_orders`.

## inspectorFirstTask

The investigation's figure has a list of tasks. Its first reads: "find the rows of
`orders.parquet` that make Thursday's total differ from `daily_sales`;". Rewrite only this item,
in Markdown, names in backticks, one line ending with a semicolon. Facts: test the explanation you
chose; find the rows of `orders.parquet` that make Thursday's total differ from `daily_sales`.

## cCaption

The check's caption, plain text, one sentence with a full stop. Fact: check the explanation you
chose against Thursday's rows.

## cMine

The line at the top of the check, plain text, one sentence with a full stop. It must contain the
slot `{choice}` exactly once. Fact: you chose to test {choice}.

## cNone

The same line for a learner who chose no explanation, plain text, one sentence with a full stop.
Fact: you did not choose an explanation to test.

## cButton

The check's button, plain text, two to five words, no full stop. Fact: it reads Thursday's rows
and shows which explanations they support.

## cHeadings

The check's table, two column headings, plain text, sentence case, no full stop, a few words each:

- explanation: the explanation
- supported: whether Thursday's rows support it

## cLab

Shown after the press, under the table, plain text with names in backticks, one or two sentences,
each with a full stop. It must contain the slots `{orders}`, `{kept}`, `{left}` and `{leftTotal}`
exactly once each. Facts: of Thursday's {orders} orders in `orders.parquet`, {kept} are among the
rows your query keeps, at the same price and quantity and on the same day; the other {left} are
not, and together they are worth {leftTotal}, the whole difference.

## cExplain

Shown under that line, in Markdown, names in backticks, short paragraphs. Facts:

- The rows support one explanation: some of Thursday's orders are not counted.
- They rule out the other two: no order is counted at a lower value, and none on another day.
- If you chose another explanation, the rows have ruled it out; the first explanation you test
  need not be the right one.
- The rows do not say why those orders were left out. Ask: what do they have in common?
- The challenge at the end of this chapter asks which rows the cleaning keeps.

Do not say what the left-out orders have in common, and do not mention a customer id.

## reflectionThursday

A paragraph of the chapter's reflection, after the challenge, in Markdown, names in backticks. It
replaces: "Back to Thursday. Three orders on Thursday have no customer id. They are in
orders.parquet and not in clean_orders. Together they are worth 154.00, which makes up the
difference between Thursday's raw total (205.50) and daily_sales (51.50)." The check has already
given the numbers, so do not give them again. Facts:

- Back to Thursday.
- The three orders your check found left out are the three with no customer id.
- Every setting of the rules that passes drops orders with no customer id.
