// Copyright © 2026 Christopher Snow

// The words of Chapter 1, "The invisible data system".
//
// Drafted by the course's prose process from the briefs in docs/notes/chapter-01/briefs, checked
// against the lab for facts only, and placed here by the chapter's structure in
// invisible-system.ts. Every number is pinned by invisible-system.facts.test.ts. Edit a fact here
// only after checking it against the lab.

export const PROSE = {
  question:
    "You start work on Monday 14 September 2026, 09:00. You are a data engineer at an online shop selling bicycle parts. The shop opened its online store on Monday 7 September.\n\nThe platform holds seven assets. An asset is anything the platform stores or shows: a file, a table, or a dashboard. Three files sit in object storage. Three tables sit in the warehouse. One dashboard sits in the reporting tool. Every night, something writes the files. Programs you cannot see yet write the tables. The dashboard refreshes.\n\nThe dashboard below shows revenue per day for the shop's first week. Thursday is far lower than other days. The head of the shop asks you why. You can read everything the shop's storage holds. You cannot see anything else yet: not the code, not the timetable, not anybody's notes. How much can you find out from what storage holds?",
  motivation:
    "A data engineer joining a platform they did not build faces questions like these. Wrong answers cost real things: a deleted file that a program still reads, or a dashboard that stays wrong for weeks before anybody notices. Each question is about the assets, not the rows inside them.\n\n- Can we delete `products.parquet`?\n- What stops working if the checkout renames a column in `orders.parquet`?\n- Is Thursday's figure wrong, and since when?\n- Who should I ask about `daily_sales`?",
  prediction:
    "Before you open storage, make two predictions. Choose your answer for each, then press its button to check it.",
  p1Question:
    "The warehouse records an owner for every table. What will it name as the owner of `daily_sales`?",
  p1Explain:
    "The warehouse names `etl_service` as the owner of all three tables. `etl_service` is the account the shop's programs log in as. The course tells you this; storage does not. So the owner field says which login created the table, not which person or team answers for it. A field with the right name answered a different question.",
  p2Question:
    "`daily_sales` has one row per day with the day and revenue. Add up price times quantity over every row of `orders.parquet`, for each day. On how many of the seven days will your total equal `daily_sales`?",
  p2Explain:
    "The totals match on three days: Monday, Friday, and Sunday. They differ on the other four days. On each of those days, `orders.parquet` holds a row that `daily_sales` does not count. You will find those rows in the next section.",
  inspectorLead:
    "Choose an asset from the list. The figure shows what its storage system records about it: the rows, column names and types, and what storage says about eight questions.\n\nThings to try:\n\n- In `orders.parquet`, find the rows whose `customer_id` is NULL, and their day.\n- Find an `order_id` that appears twice.\n- Find the orders whose `status` is cancelled.\n- Compare the number of rows in `orders.parquet` with the number in `clean_orders`.\n- Open `daily_sales` and read what storage says about each question.",
  inspectorAfter:
    "Storage recorded names, types, row counts, sizes, times and an owning account. It does not say which program wrote an asset, from what, or why some orders in `orders.parquet` are missing from `clean_orders`.",
  construction:
    "Storage does not say where `daily_sales` comes from. The data might. If a query over another asset gives exactly the same rows as `daily_sales`, that query is a candidate for how it was made.\n\nBuild one with the query builder. Choose an asset to read, which rows to keep, what to add up, and per what. The builder writes your choices as SQL and runs the query on Monday morning's data.",
  c1Task:
    "Build a query that makes `daily_sales` from another asset. Choose an asset to read, which rows to keep, what to add up, and per what. The tests compare your result with `daily_sales` for each day: your row for that day must be exactly equal to its row.",
  c1Hints: [
    "A query that rebuilds `daily_sales` must count exactly the orders it counts and add up the same total per day.",
    "Reading `orders.parquet` does not work. The raw file holds rows that `daily_sales` does not: an order written twice, orders with no customer id, and cancelled orders.",
    "From `orders.parquet`, Monday already matches. Monday had none of those rows. Pick a day that does not match and compare.",
    "Read from `clean_orders`.",
    "Read from `clean_orders`, keep completed orders only, add up price times quantity, per day.",
  ],
  c1Lead: "Your query appears below as SQL, with its result, before you run the tests.",
  changeLead:
    "Each change alters the shop before the week begins. The figure will run the whole week again from Monday, with that change in place. It then shows what storage shows differently, your query's rows against the new `daily_sales`, and every query in the builder's choices that rebuilds it. It uses your query from the construction section if it passes its tests, and the course's query if it does not.\n\nBefore you run each change, make a prediction. Will storage show the change? Will your query still rebuild `daily_sales`?",
  changeQuestion:
    "Before the week runs: how many queries in the builder's choices will rebuild `daily_sales` after this change?",
  outcomeCopy:
    "A new file appears in storage: `clean_orders_copy.parquet` in bucket `shop-scratch`, last modified at 02:15, with the same 44 rows as `clean_orders`. Now two queries rebuild `daily_sales`: from `clean_orders` and from the copy. The data cannot say which one was used. Both fit equally well.",
  outcomeRefunds:
    "From Saturday's row on, the program keeps every order whose status is not \"refunded\", where it used to keep completed orders. The shop has no refunds. Saturday's row now reads 215.49, not 191.49, here and on the dashboard, because its cancelled order counts. Sunday's row is unchanged at 97.75, because Sunday had no cancelled order. Storage shows nothing else different: the same 7 rows and the same last-written time. No query in the builder's choices rebuilds `daily_sales` any more. Nothing says whether Saturday is a mistake or a decision.",
  outcomeFailed:
    "The program fails on the last night and writes nothing. `daily_sales` has 6 rows, with no row for Sunday, and was last altered on Sunday 13 September at 02:30. The dashboard refreshed on Monday at 03:00 as usual and shows 6 values. From storage, a failed night looks like a night with nothing to write. Your query still rebuilds every row `daily_sales` has, and gives one more: Sunday.",
  afterAll:
    "The data suggested where `daily_sales` comes from. A copy made the answer ambiguous, an edit made it impossible, and a failure made a missing row look like a quiet night. None of the three changes left anything in storage that says what happened.",
  explanation:
    "Object storage keeps the location, size and last-modified time of every file. The warehouse keeps each table's column names, their types, its row count and the account that owns it. The reporting tool keeps the dashboard title, its values and its last refresh time.\n\nEach system records only what it needs for its own work. The warehouse must know the columns and types to run a query, and the owning account to control who may read. Object storage must know the file size to serve it. The reporting tool must know the values to draw its chart. None of them ask: what does this number mean, or who is answerable for it?\n\nYour questions were about the platform around the data: what a number means, who answers for an asset, what made it, what reads it, what changed. None of the three systems recorded these because they were not needed to store or serve the data. Some of the systems do keep records for their own work that you were not shown: the reporting tool keeps the query behind its chart, and something keeps the programs and their timetable. You will see them in later chapters.",
  mapLead:
    "The lab places each question in one of three columns: storage records it; the data suggests it because a query rebuilds the asset or another asset shows the same numbers; or only a record kept at the time answers it.\n\nThe lab finds each place by running storage and trying queries in the query builder, not from a list.",
  mapAfter:
    "The middle column is evidence, not an answer. The failure experiment showed it: the evidence can change when an analyst adds a copy, when a program is edited, or when a night's work fails.",
  generalisation:
    "The right-hand column holds questions no amount of data answers: who is answerable for each asset, what unit a number uses, what changed.\n\nThe middle column holds answers the data suggests. They can be ambiguous, impossible or misleading.\n\nRecords about assets and about the platform, written down and kept separate from the data itself, are called **metadata**. A platform needs three kinds: what each asset is (its meaning, the units it uses, who is answerable for it); what happened (what programs ran, when they ran, whether they worked); and what was made from what. The rest of this course builds a system that keeps all three, starting with the first records in the next chapter.",
  c2Task:
    "You need to choose four rules that turn `orders.parquet` into `clean_orders`. The tests check that your rules keep every row `clean_orders` has, and no row it lacks.",
  c2Hints: [
    "Compare `orders.parquet` with `clean_orders` row by row. Which rows are missing, and which appear fewer times?",
    "A common mistake: dropping cancelled orders. `clean_orders` keeps them; `daily_sales` leaves them out later.",
    "On Wednesday, order 7015 appears twice in `orders.parquet` and once in `clean_orders`.",
    "Keep one copy of each order, and drop orders with no customer id.",
    "Keep one copy, drop orders with no customer id, keep cancelled orders. Either choice passes for the quantity rule.",
  ],
  c2Lead: "The rules appear as SQL below the choices, with the number of rows they keep.",
  p3Question:
    "Your rules pass. How many settings of the four rules give `clean_orders` exactly, yours included?",
  p3Explain:
    "Two settings pass. They differ only in the rule for orders with a quantity of 0 or less: no order this week had one, so either choice keeps the same rows.",
  reflection:
    "Storage gave you names, types, row counts, sizes, times and one account. The data suggested where `daily_sales` comes from, until a copy, an edit or a failed night.\n\nThe program the shop really runs for `clean_orders` also drops orders with a quantity of 0 or less. No order this week had one, so both answers to that rule passed your tests, and no rebuilding from this week's data could find the rule.\n\nWhat would you write down about `daily_sales` so that the next person need not rebuild it? Who should write it down, and when?",
  modelVsReality:
    "Real storage systems record different things. Some warehouses record no owner and no last-altered time. Some object stores keep every version of a file, and logs of who read it. The lab models none of these.\n\nThe lab's sizes are estimates from the rows.\n\nThe lab works in UTC and has no time zones.\n\nA real platform has hundreds or thousands of assets. Searching for queries that rebuild one would cost far more.\n\nThe lab's search covers only the query builder's choices. \"No query rebuilds it\" means none of those choices.",
} as const;
