## titles.question
A week of questions

## question
You start work on Monday 14 September, 09:00. You are a data engineer at an online shop selling bicycle parts. The shop opened on Monday 7 September.

The platform holds seven assets. An asset is anything the platform stores or shows: a file, a table, or a dashboard. Three files sit in object storage. Three tables sit in the warehouse. One dashboard sits in the reporting tool. Every night, something writes the files. Programs you cannot see yet write the tables. The dashboard refreshes.

The dashboard below shows revenue per day for the shop's first week. Thursday is far lower than other days. The head of the shop asks you why. You can read everything the shop's storage holds. You cannot see anything else: not the code, not the timetable, not anybody's notes. How much can you find out from what storage holds?

## dashboardCaption
The dashboard shows daily revenue for 7 to 13 September.

## titles.motivation
Why these questions matter

## motivation
A data engineer joining a platform they did not build faces questions like these. Wrong answers cost real things: a deleted file that a program still reads, or a dashboard that stays wrong for weeks before anybody notices. Each question is about the assets, not the rows inside them.

- Can we delete `products.parquet`?
- What stops working if the checkout renames a column in `orders.parquet`?
- Is Thursday's figure wrong, and since when?
- Who should I ask about `daily_sales`?

## titles.prediction
What you expect storage to tell you

## prediction
Make two predictions about what storage holds. Choose your answer for each, then check it against the facts.

## p1Caption
The owner the warehouse records for `daily_sales`.

## p1Question
The warehouse records an owner for every table. What will it name as the owner of `daily_sales`?

## p1Options
- account: an account that programs log in as
- person: a person
- team: a team, such as finance
- none: no owner at all

## p1Explain
The warehouse names `etl_service` as the owner of all three tables. `etl_service` is the account the shop's programs log in as. The course tells you this; storage does not. So the owner field says which login created the table, not which person or team answers for it.

## p2Caption
How many days do `orders.parquet` totals match `daily_sales`?

## p2Question
`daily_sales` has one row per day with the day and revenue. Add up price times quantity from `orders.parquet`, for each day. On how many of the seven days will your total equal `daily_sales`?

## p2Options
- all: on all seven days
- some: on some days but not all
- none: on no day

## p2Explain
The totals match on three days: Monday, Friday, and Sunday. They differ on the other four days. On each of those days, `orders.parquet` holds a row that `daily_sales` does not count. You will find those rows in the next section.
