## question

You start work on Monday 14 September 2026 at 09:00. You are a data engineer at an online shop that sells bicycle parts. The shop opened its online store on Monday 7 September.

Every figure on this page runs the Metadata Lab: a small data platform that holds the shop and runs in your browser. The lab works out everything a figure shows.

The shop's data platform has three systems. Object storage holds files. The warehouse holds tables. The reporting tool holds a dashboard. An asset is something in the platform that can be stored, described, changed, related to other assets, or depended on.

The shop has seven assets: three files in object storage, three tables in the warehouse, one dashboard in the reporting tool. In this chapter, storage means all three systems.

Every night the three files are written again. Then programs write the tables and refresh the dashboard. You cannot see the programs.

The map below shows the systems and their assets, in the order data moves through them each night. Once you scroll past it, a button at the foot of the window opens it again.

## dashboardLead

The dashboard shows revenue per day for the shop's first week. Thursday is far lower than the other days. The head of the shop asks you why.

## dashboardAfter

You can read everything storage holds. You cannot see the code, when each program is due to run, or anybody's notes. How much can you find out from what storage holds?

## prediction

Before you open storage, make two predictions. Each option is an explanation of how the platform works. Choose the one you think more likely, then press its button to check it.

## p1Question

The warehouse records an owner for every table. Will the owner it records for `daily_sales` name someone you could ask about the table?

## p1Options

- yes: yes, because an owner field names whoever is responsible for the table;
- no: no, because an owner field names the account that writes the table, and programs write the tables.

## p2Question

The dashboard shows 51.50 for Thursday. `daily_sales` holds the same figure for Thursday. Add up price times quantity over Thursday's rows of `orders.parquet`. Will the total be 51.50 too?

## p2Options

- same: yes, because Thursday was a slow day, and the raw orders show it too;
- more: no, the total is more, because the orders came in and something on the way to daily_sales left some out.

## p2Explain

Thursday's rows of `orders.parquet` add up to 205.50. `daily_sales` has 51.50. Thursday's raw total of 205.50 is close to Wednesday's raw total (198.75) and Friday's (204.24). In `orders.parquet`, Thursday was not a slow day.

The table shows the other days too. The totals are equal on three days: Monday, Friday and Sunday. They differ on four, Thursday among them. The reason is in the rows of `orders.parquet`. The next section lets you read them.

## captions

- platform: the map: the shop's three systems and the assets each holds.
- p1: predict whether the owner the warehouse records for daily_sales is someone you could ask.
- p2: predict whether Thursday's rows of orders.parquet add up to the dashboard's figure.

## mapStrings

- label: the shop's data platform
- objectStorage: object storage
- warehouse: warehouse
- reporting: reporting tool
- flow: unseen programs move data here each night
- open: The map
- close: close

