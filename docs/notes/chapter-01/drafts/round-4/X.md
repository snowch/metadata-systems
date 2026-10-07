## prediction

Before you open storage, answer two questions.

The first gives you a requirement the shop has set. It asks what you would store to meet it. Then it shows what the requirement could mean and what the shop's warehouse holds.

The second asks what you expect Thursday's orders in `orders.parquet` to add up to. Each of its options is a total you could expect and the belief behind it; one says you cannot tell yet. The lab adds up the orders and checks.

For each, choose an option, then press the button below it.

## p2Caption

Predict what Thursday's rows of orders.parquet add up to.

## p2Question

The dashboard shows 51.50 for Thursday. `daily_sales` holds the same figure for Thursday. Add up price times quantity over Thursday's rows of `orders.parquet`. What do you expect the total to be?

## p2Options

- same: 51.50: daily_sales holds the total of Thursday's orders
- different: a different total: daily_sales is not simply the total of Thursday's orders

## p2Undecided

- i can't tell yet: nothing so far says what daily_sales measures

## p2UndecidedLine

You said you could not tell yet. The lab found {answer}.

## p2Explain

Thursday's rows of `orders.parquet` add up to 205.50. `daily_sales` holds 51.50 for Thursday. So `daily_sales` is not simply the total of Thursday's orders in `orders.parquet`.

Thursday's raw total of 205.50 is close to Wednesday's (198.75) and Friday's (204.24). In `orders.parquet`, Thursday was not a slow day.

The table shows every day: the totals are equal on three days (Monday, Friday and Sunday) and differ on four.

Now there is a difference to explain. What might explain it?

The next section lets you read the rows of `orders.parquet`.

## p3Options

- one: yes, a setting that gives clean_orders exactly is the only one that does
- more: no, another setting can give exactly the same rows

