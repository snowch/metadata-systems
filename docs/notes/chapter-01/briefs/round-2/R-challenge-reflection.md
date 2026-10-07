# Brief R: Section 9's prediction and Section 10, the chapter's end

Read `common.md` in this directory first. Write your draft to
`docs/notes/chapter-01/drafts/round-2/R.md`.

## p3Question

Shown once the learner's four rules pass, before they commit. It replaces "Your rules pass. How
many settings of the four rules give `clean_orders` exactly, yours included?", which asked for a
number. Facts:

- Your rules pass.
- Ask: is your setting of the four rules the only one that gives `clean_orders` exactly?

## p3Options

Two option labels, each an explanation, parallel in form and length:

- one: yes, only mine, because every rule I chose decides some row this week;
- more: no, more than one, because some rule decides no row this week.

## p3Caption

The figure's caption, plain text, one sentence ending with a full stop: predict whether your
setting of the four rules is the only one that passes.

## reflection

Section 10's prose, the chapter's end. It begins with a new short summary, then keeps the old
text. Facts for the summary, said once, in four or five short sentences, before anything else:

- Storage tells you what exists now: which assets there are, their columns and rows, and when
  each was last written.
- The data can sometimes suggest what produced an asset: your query rebuilt `daily_sales`, and
  your four rules rebuilt `clean_orders`.
- The data cannot prove it: a copy fitted as well, an edit left no query in the builder that
  fits, and two settings of the rules fitted `clean_orders`.
- Neither storage nor the data tells you for certain what happened, why it happened, who was
  responsible, or what depends on an asset.
- Those are things somebody has to record on purpose, when they happen.

Then keep the old text exactly as it was:

"Back to Thursday. Three orders on Thursday have no customer id. They are in `orders.parquet` and
not in `clean_orders`. Together they are worth 154.00, which makes up the difference between
Thursday's raw total (205.50) and `daily_sales` (51.50).

Nothing you could read says whether leaving them out is a fault in the checkout or a rule
somebody chose. The course comes back to Thursday later.

The four questions from the start each needed a record nobody kept:

- Can we delete `products.parquet`? It needs a record of what reads it. No program in the lab
  reads it, but storage could not show you that.
- What stops working if the checkout renames a column in `orders.parquet`? It needs a record of
  what reads that file and what is made from it.
- Is Thursday's figure wrong, and since when? It needs a record of what happened, and of the rule
  somebody chose.
- Who should I ask about `daily_sales`? It needs a record of what the asset is, including who is
  responsible for it.

What would you write down about `daily_sales` so that the next person need not rebuild it? Who
should write it down, and when?"
