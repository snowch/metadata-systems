## outcomeRefunds

Before the edit, the program kept completed orders only.

The shop has no refunds: every order is completed or cancelled.

Saturday's row now reads 215.49, because Saturday's cancelled order counts. The dashboard shows the same. In the week as it first ran it read 191.49.

Sunday's row is unchanged, 97.75, because Sunday had no cancelled order.

Storage shows nothing else different: the same 7 rows and the same last-written time.

None of the builder's choices rebuilds `daily_sales` any more. A query with a condition on the date would, and the builder offers none.

Nothing says whether Saturday's figure is a mistake or a decision.
