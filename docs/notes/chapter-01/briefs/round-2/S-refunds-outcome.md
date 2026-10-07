# Brief S: the edit's outcome, now that its label says what the edit does

Read `common.md` in this directory first. Write your draft to
`docs/notes/chapter-01/drafts/round-2/S.md`.

## outcomeRefunds

Shown after the edit for refunds has run, below the figure's own line "The lab ran the whole week
again with this change: the program that writes daily_sales is edited to keep orders that are not
refunded, from Saturday's row on." The old text's first sentence repeated that label: "From
Saturday's row on, the program that writes daily_sales keeps every order whose status is not
"refunded", where before it kept completed orders only." Replace that first sentence only, with
the one fact the label does not carry:

- Before the edit, the program kept completed orders only.

Keep the rest exactly as it was:

"The shop has no refunds: every order is completed or cancelled.

Saturday's row now reads 215.49, because Saturday's cancelled order counts. The dashboard shows the
same. In the week as it first ran it read 191.49.

Sunday's row is unchanged, 97.75, because Sunday had no cancelled order.

Storage shows nothing else different: the same 7 rows and the same last-written time.

None of the builder's choices rebuilds `daily_sales` any more. A query with a condition on the date
would, and the builder offers none.

Nothing says whether Saturday's figure is a mistake or a decision."
