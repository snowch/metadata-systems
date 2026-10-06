## objectives

- Read what each of the shop's three systems keeps about a file, a table and a dashboard.
- Rebuild one asset from another with a query, and test what that shows.
- Change the shop in three ways and see what the data can still tell you.
- Sort questions about an asset by what can answer them, then check your sort against the lab.

## question

You start work on Monday 14 September 2026 at 09:00. You are a data engineer at an online shop that sells bicycle parts. The shop opened its online store on Monday 7 September.

The platform holds seven assets: files, tables and a dashboard. Three files sit in object storage, three tables in the warehouse, one dashboard in the reporting tool. Every night the three files are written again. Then programs write the tables and refresh the dashboard.

The dashboard below shows revenue per day for the shop's first week. Thursday is far lower than the other days. The head of the shop asks you why.

You can read everything storage holds. You cannot see the code, when each program is due to run, or anybody's notes. Every figure on this page runs the Metadata Lab, a small data platform that holds the shop and runs in your browser. The lab works out everything a figure shows.

How much can you find out from what storage holds?

## dashboard caption

On Monday morning the dashboard shows daily revenue for 7 to 13 September.

## motivation

A data engineer who joins a platform they did not build is asked questions like these:

- Can we delete `products.parquet`?
- What stops working if the checkout renames a column in `orders.parquet`?
- Is Thursday's figure wrong, and since when?
- Who should I ask about `daily_sales`?

A wrong answer to the first breaks a program that still reads the file. A wrong answer to the third can leave a figure wrong for weeks before anybody notices. None of the four can be answered by reading rows alone.

## prediction

Before you open storage, make two predictions. Choose an answer for each, then press its button to check it.

## p1Question

The warehouse records an owner for every table. What will it name as the owner of `daily_sales`?

## p1Options

- person: a person, for example whoever built it
- team: a team, for example finance
- program: the program that writes it
- account: an account that programs log in as

## p1Explain

The warehouse records the name `etl_service` as the owner of all three tables. `etl_service` is the account all four of the shop's programs log in as. The lab tells you this; storage does not.

So the owner field names an account. It does not say which person or team is responsible for the table. A field with the right name answered a different question.

## p2Question

`daily_sales` has one row per day, with the day and the revenue. Add up price times quantity over every row of `orders.parquet`, for each day, and compare the totals with `daily_sales`. On how many of the seven days will the two be equal?

## p2Options

- all: all seven
- six: six, every day but Thursday
- fourOrFive: four or five
- threeOrFewer: three or fewer

## p2Explain

The totals are equal on three days: Monday, Friday and Sunday. They differ on the other four, Thursday among them. The reason is in the rows of `orders.parquet`, and the next section lets you read them.

## p1Caption

Predict the owner the warehouse records for daily_sales.

## p2Caption

Predict on how many days the totals of orders.parquet equal daily_sales.
