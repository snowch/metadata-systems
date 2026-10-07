// Copyright © 2026 Christopher Snow

// The words of Chapter 1, "The invisible data system".
//
// Drafted by the course's prose process from the briefs in docs/notes/chapter-01/briefs, checked
// against the lab for facts only, and placed here by the chapter's structure in
// invisible-system.ts. Every number is pinned by invisible-system.facts.test.ts. Edit a fact here
// only after checking it against the lab.

export const PROSE = {
  question:
    "You start work on Monday 14 September 2026 at 09:00. You are a data engineer at an online shop that sells bicycle parts. The shop opened its online store on Monday 7 September.\n\nEvery figure on this page runs the Metadata Lab: a small data platform that holds the shop and runs in your browser. The lab works out everything a figure shows.\n\nThe shop's data platform has three systems. Object storage holds files. The warehouse holds tables. The reporting tool holds a dashboard. An asset is something in the platform that can be stored, described, changed, related to other assets, or depended on.\n\nThe shop has seven assets: three files in object storage, three tables in the warehouse, one dashboard in the reporting tool. In this chapter, storage means all three systems.\n\nEvery night the three files are written again. Then programs write the tables and refresh the dashboard. You cannot see the programs.\n\nThe map below shows the systems and their assets, in the order data moves through them each night. Once you scroll past it, a button at the foot of the window opens it again.",
  dashboardLead:
    "The dashboard shows revenue per day for the shop's first week. Thursday is far lower than the other days. The head of the shop asks you why.",
  dashboardAfter:
    "You can read everything storage holds. You cannot see the code, when each program is due to run, or anybody's notes. How much can you find out from what storage holds?",
  motivation:
    "A data engineer who joins a platform they did not build is asked questions like these:\n\n- Can we delete `products.parquet`?\n- What stops working if the checkout renames a column in `orders.parquet`?\n- Is Thursday's figure wrong, and since when?\n- Who should I ask about `daily_sales`?\n\nA wrong answer to the first breaks a program that still reads the file. A wrong answer to the third can leave a figure wrong for weeks before anybody notices. None of the four can be answered by reading rows alone.",
  prediction:
    "Before you open storage, make two predictions. Each option is an explanation of how the platform works. Choose the one you think more likely, then press its button to check it.",
  p1Question:
    "The warehouse records an owner for every table. Will the owner it records for `daily_sales` name someone you could ask about the table?",
  p1Explain:
    "The warehouse records the name `etl_service` as the owner of all three tables. `etl_service` is the account all four of the shop's programs log in as. The lab tells you this; storage does not.\n\nSo the owner field names an account. It does not say which person or team is responsible for the table. A field with the right name answered a different question.",
  p2Question:
    "The dashboard shows 51.50 for Thursday. `daily_sales` holds the same figure for Thursday. Add up price times quantity over Thursday's rows of `orders.parquet`. Will the total be 51.50 too?",
  p2Explain:
    "Thursday's rows of `orders.parquet` add up to 205.50. `daily_sales` has 51.50. Thursday's raw total of 205.50 is close to Wednesday's raw total (198.75) and Friday's (204.24). In `orders.parquet`, Thursday was not a slow day.\n\nThe table shows the other days too. The totals are equal on three days: Monday, Friday and Sunday. They differ on four, Thursday among them. The reason is in the rows of `orders.parquet`. The next section lets you read them.",
  inspectorLead:
    "Choose an asset from the list. The figure shows what storage records about it: its record, what storage says about eight questions, its columns and their types, and its rows.\n\nThe figure asks every asset the same eight questions.\n\nThen try one of these:\n\n- find the rows of `orders.parquet` that make Thursday's total differ from `daily_sales`;\n- compare `orders.parquet` with `clean_orders`;\n- put the seven assets in the order they were last written, and say what that order suggests and what it cannot prove;\n- open `daily_sales` and read what storage says about each question.",
  inspectorAfter:
    "Storage cannot answer some of the questions about `daily_sales`. The next section tries the data on them.",
  construction:
    "Storage does not say where `daily_sales` comes from. The data might.\n\nA query **rebuilds** an asset when it gives every row the asset has, with the same values.\n\nBuild one with the query builder below. It writes your choices as SQL and runs the query on Monday morning's data.\n\nIf your query rebuilds `daily_sales`, have you found out how `daily_sales` was made?",
  c1Task:
    "Build a query over another asset that rebuilds `daily_sales`. Choose an asset to read, which rows to keep, what to add up, and per what. The tests compare your result with `daily_sales` one day at a time, and each day's row must match its row.",
  c1Hints: [
    "A query that rebuilds `daily_sales` must count exactly the orders it counts and add up the same total per day.",
    "Reading `orders.parquet` does not work. The raw file holds rows that `daily_sales` does not: an order written twice, orders with no customer id, and cancelled orders.",
    "From `orders.parquet`, Monday already matches. Monday had none of those rows. Pick a day that does not match and compare.",
    "Read from `clean_orders`.",
    "Read from `clean_orders`, keep completed orders only, add up price times quantity, per day.",
  ],
  c1Lead: "Your query appears below as SQL, with its result, before you run the tests.",
  changeLead:
    "This experiment tests whether rebuilding `daily_sales` with a query shows how it was made.\n\nIt runs your query from the construction section again, so it starts once your query passes its tests.\n\nEach change gives a different week: the lab runs the whole week again from Monday with that change.\n\nBefore a change runs, you predict what the data will then say about where `daily_sales` comes from: how many queries in the builder's choices will rebuild it. The builder's choices cover every asset in storage that week.\n\nAfter it runs, the figure shows those queries, what storage holds on Monday morning, and your query's rows against the new `daily_sales`.",
  changeQuestion:
    "After this change, how many queries in the builder's choices will rebuild `daily_sales`?",
  outcomeCopy:
    "A new file appears in storage: `clean_orders_copy.parquet`, in the bucket `shop-scratch`, last modified at 02:15, with the same 44 rows as `clean_orders`.\n\nNow 2 queries rebuild `daily_sales`: the same query over `clean_orders` and over the copy.\n\nThe data cannot say which of the two `daily_sales` was built from. Both fit equally well.\n\nStorage shows the new file. Nothing says who made it or why.",
  outcomeRefunds:
    "Before the edit, the program kept completed orders only.\n\nThe shop has no refunds: every order is completed or cancelled.\n\nSaturday's row now reads 215.49, because Saturday's cancelled order counts. The dashboard shows the same. In the week as it first ran it read 191.49.\n\nSunday's row is unchanged, 97.75, because Sunday had no cancelled order.\n\nStorage shows nothing else different: the same 7 rows and the same last-written time.\n\nNone of the builder's choices rebuilds `daily_sales` any more. A query with a condition on the date would, and the builder offers none.\n\nNothing says whether Saturday's figure is a mistake or a decision.",
  outcomeFailed:
    "On the last night, the program that writes `daily_sales` fails and writes nothing.\n\n`daily_sales` has 6 rows, with no row for Sunday. It was last altered on Sunday 13 September at 02:30, a day before `clean_orders` (Monday at 02:05) and the dashboard (Monday at 03:00).\n\nThe dashboard refreshed on Monday at 03:00 as on every morning, and shows 6 values. Its own record shows that Monday-morning refresh, so it looks up to date.\n\nStorage shows that `daily_sales` is a day behind. It does not show that a write was due on Monday, or that one failed.\n\nYour query still rebuilds `daily_sales`: it gives the 6 rows `daily_sales` has, and a seventh, for Sunday, that `daily_sales` lacks.",
  afterAll:
    "Rebuilding `daily_sales` suggested how it was made, but did not show it. Each of the three changes altered that evidence.\n\nThe copy made it ambiguous: two assets fit equally well.\n\nThe edit left none of the builder's choices that fits.\n\nThe failed night left the dashboard looking up to date over a table a day behind.\n\nStorage kept some traces: the copy left a new file, and the failed night a stale time.\n\nNone of the changes left a record of the change itself: what changed, who changed it, or why.",
  explanation:
    "Each system that holds data keeps some information about its own assets.\n\nObject storage keeps each file's location, its size and when it was last modified. A Parquet file carries its own column names, their types and its row count, written inside the file after its rows. That is where the inspector found a file's columns. The warehouse keeps each table's column names and types, its row count, its size, when it was created and when it was last altered, and the name of the account that owns it. The reporting tool keeps the dashboard's title, who created it and when, when it last refreshed and its values.\n\nThese are the lab's choices of what each kind of system keeps. Each field is one the system uses for its own work. The warehouse uses column names and types to run a query. Object storage uses a file's location to serve it. The reporting tool uses the values to draw its chart.\n\nNone of the three keeps what your questions asked about who is responsible for an asset, what made it, what reads it or what changed in it. The programs, and when each is due to run, exist. This page has not shown them yet. Later chapters do.",
  mapLead:
    "The figure lists the eight questions about `daily_sales`. For each question, choose the group that can answer it, then check your sorting.\n\nThe three groups are:\n\n- Storage records it.\n- The data suggests it.\n- Only a record kept at the time answers it.\n\nA question goes with the data when a query rebuilds the asset, when another asset shows the same numbers, or when the last-written time and the latest row fit a write that worked. After you check, the lab places each question itself, by reading storage and trying every query the builder offers. You can then choose any change from the failure experiment, and the lab places the questions again for that week.",
  mapAfter:
    "The data's group holds evidence, not a certainty. A change to the shop can move a question out of the data's group.",
  generalisation:
    "Once you have checked your sorting, look at the questions in the group \"Only a record kept at the time answers it\". The lab tags each with the kind of record that would answer it.\n\nThere are three kinds of record:\n\n- a record of what the asset is: who is responsible for it, the unit of its numbers;\n- a record of what happened: what changed in it, when it was written, whether a write worked;\n- a record of what was made from what: what it is made from, how its numbers are worked out, what reads it.\n\nThe groups say what can answer a question now. The kinds say what record would answer it for certain. The two sortings need not line up.\n\nOne column in the data names people: `updated_by` in `products.parquet` says who last edited each product's row. That is a fact about a product, not a record of who is responsible for the file.\n\nAfter the edit to the program, two questions about what made `daily_sales` left the data's group.\n\nInformation about an asset or about the platform is called **metadata**: what an asset is, where it came from, who is responsible for it, what its numbers mean, how it is made, and how it relates to other assets. Metadata can live inside the system that holds the data, as the warehouse's column names and types do. It can live next to the data, inside the same file, as a Parquet file's own column names and types do. It can live in a system of its own. What storage keeps (names, types, row counts, sizes, times, an owner's name) is metadata too: the part each system keeps for its own work. The questions only a record answers need the rest.\n\nThe rest of this course builds a system that keeps all three kinds.",
  c2Task:
    "Choose four rules that turn `orders.parquet` into `clean_orders`. The tests check that your rules keep every row `clean_orders` has, and no row it lacks.",
  c2Hints: [
    "Compare `orders.parquet` with `clean_orders` row by row. Which rows are missing, and which appear fewer times?",
    "A common mistake: dropping cancelled orders. `clean_orders` keeps them; `daily_sales` leaves them out later.",
    "On Wednesday, order 7015 appears twice in `orders.parquet` and once in `clean_orders`.",
    "Keep one row of an order that appears twice. Drop orders with no customer id.",
    "Keep one row of an order that appears twice. Drop orders with no customer id. Keep cancelled orders. Either choice passes for the quantity rule.",
  ],
  c2Lead:
    "`clean_orders` is made from `orders.parquet` by rules you cannot read. Recover them from the two files by choosing, for each kind of row that differs between them, whether the rules keep it. The tests compare the rows your rules keep with `clean_orders`. Your rules appear as SQL below the choices, with the number of rows they keep.",
  p3Question:
    "Your rules pass. Is your setting of the four rules the only one that gives `clean_orders` exactly?",
  p3Explain:
    "Two settings pass. They differ only in the rule for orders with a quantity of 0 or less. No order this week had a quantity of 0 or less, so either choice keeps the same rows. The shop's program drops such orders. This week's data cannot show that rule, however you rebuild it.",
  reflection:
    "Storage tells you what exists now: which assets there are, their columns and rows, and when each was last written. The data can sometimes suggest what made an asset: your query rebuilt `daily_sales`, and your four rules rebuilt `clean_orders`. The data cannot prove it: a copy fitted as well, an edit left no matching query in the builder, and two settings of the rules rebuild `clean_orders`. Neither storage nor the data tells you for certain what happened, why it happened, who is responsible, or what depends on an asset. Those are things somebody has to record on purpose, when they happen.\n\nBack to Thursday. Three orders on Thursday have no customer id. They are in `orders.parquet` and not in `clean_orders`. Together they are worth 154.00, which makes up the difference between Thursday's raw total (205.50) and `daily_sales` (51.50).\n\nNothing you could read says whether leaving them out is a fault in the checkout or a rule somebody chose. The course comes back to Thursday later.\n\nThe four questions from the start each needed a record nobody kept:\n\n- Can we delete `products.parquet`? It needs a record of what reads it. No program in the lab reads it, but storage could not show you that.\n- What stops working if the checkout renames a column in `orders.parquet`? It needs a record of what reads that file and what is made from it.\n- Is Thursday's figure wrong, and since when? It needs a record of what happened, and of the rule somebody chose.\n- Who should I ask about `daily_sales`? It needs a record of what the asset is, including who is responsible for it.\n\nWhat would you write down about `daily_sales` so that the next person need not rebuild it? Who should write it down, and when?",
  modelVsReality:
    "Real systems keep different things. Some keep history that the lab's warehouse does not. An Apache Iceberg table keeps snapshots, each the state of the table at some time. A Delta Lake table keeps, for each write, the operation, the user and the time, for 30 days by default. The lab's storage keeps only the current rows.\n\nThe lab's sizes are estimates from the rows.\n\nThe lab works in UTC and has no time zones.\n\nA real platform has hundreds or thousands of assets. Searching for queries that rebuild one would cost far more.\n\nThe lab's search covers only the query builder's choices. \"None of the builder's choices rebuilds it\" means none of those choices; a query outside them might.",
} as const;
