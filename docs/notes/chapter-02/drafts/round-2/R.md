## p3Question

Is your setting of the four rules the only one that gives `clean_orders` exactly?

## p3Options

- one: every rule you chose decides some row this week
- more: some rule decides no row this week

## p3Caption

Predict whether your setting of the four rules is the only one that passes.

## reflection

Storage tells you what exists now: which assets there are, their columns and rows, and when each was last written.

The data can sometimes suggest what made an asset: your query rebuilt `daily_sales`, and your four rules rebuilt `clean_orders`.

The data cannot prove it: a copy fitted as well, an edit left no matching query, and two settings of the rules rebuild `clean_orders`.

Neither storage nor the data tells you what happened, why it happened, who is responsible, or what depends on an asset.

Those are things somebody has to record on purpose, when they happen.

Back to Thursday. Three orders on Thursday have no customer id. They are in `orders.parquet` and not in `clean_orders`. Together they are worth 154.00, which makes up the difference between Thursday's raw total (205.50) and `daily_sales` (51.50).

Nothing you could read says whether leaving them out is a fault in the checkout or a rule somebody chose. The course comes back to Thursday later.

The four questions from the start each needed a record nobody kept:

- Can we delete `products.parquet`? It needs a record of what reads it. No program in the lab reads it, but storage could not show you that.
- What stops working if the checkout renames a column in `orders.parquet`? It needs a record of what reads that file and what is made from it.
- Is Thursday's figure wrong, and since when? It needs a record of what happened, and of the rule somebody chose.
- Who should I ask about `daily_sales`? It needs a record of what the asset is, including who is responsible for it.

What would you write down about `daily_sales` so that the next person need not rebuild it? Who should write it down, and when?
