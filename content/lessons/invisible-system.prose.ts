// Copyright © 2026 Christopher Snow

// The words of Chapter 1, "The invisible data system".
//
// Drafted by the course's prose process from the briefs in docs/notes/chapter-01/briefs, checked
// against the lab for facts only, and placed here by the chapter's structure in
// invisible-system.ts. Every number is pinned by invisible-system.facts.test.ts. Edit a fact here
// only after checking it against the lab.

export const PROSE = {
  question:
    "You start work on Monday 14 September 2026 at 09:00. You are a data engineer at an online shop selling bicycle parts. The shop opened its online store on Monday 7 September.\n\nThe views on this page let you investigate the shop. They use the Metadata Lab, a small data platform written for and built into this course. It runs in your browser: there is nothing to install, open or sign in to.\n\nThe first three views, the pipeline, the shop's week and the dashboard, introduce you to the shop. When you first investigate an issue at a data platform you did not build, you often cannot see the programs that produced the data. You can see the data they wrote, and have to work out what happened from what the systems hold. This chapter is that situation: you cannot see the shop's programs, only the data they write, so you work out what happened from the views.",
  /** How the lab is built, behind the control the reader opens (brief AF). */
  labDetails:
    "The lab holds the shop's first week: real rows in files and tables, dashboard values and SQL programs. The shop is invented. The lab's query engine runs the programs and your queries. Nothing about the shop is kept between page loads: each load builds its data and runs its first week night by night, in memory. Every reader sees the same rows, results and times on any day. Dates and times come from the shop's first week, not from today or your computer's clock. Your browser keeps your work by chapter: predictions, choices and challenge answers. Nothing you do leaves your browser.",
  platformLead:
    "The shop's data platform has three systems. The pipeline shows them in the order data moves through them each night. Once you scroll past the pipeline, a button at the foot of the window opens it again.",
  platformAfter:
    "An asset is one thing the platform holds: here, a file, a table or a dashboard. Wider things count too, wherever this course goes: anything that can be stored, described, changed, related to other assets, or depended on.",
  weekLead:
    "The shop's first week ran from Monday 7 to Sunday 13 September 2026. After each day, in the early hours of the next day, the three files are written again, then the programs write the tables and refresh the dashboard.",
  weekAfter: "The last night ends early on Monday 14 September, before you start work.",
  dashboardLead:
    "The dashboard shows revenue per day for the shop's first week. Thursday is far lower than the other days. The head of the shop asks you why.",
  exploreLead:
    "The platform holds three kinds of thing, and you have met each: a file in object storage, tables in the warehouse, a dashboard in the reporting tool. Open a card to see a little of what it holds. Nothing is asked here; the questions start below.",
  dashboardAfter:
    "You can inspect the files, tables and dashboard, but not the code that produces them or the notes people have written about them. How much can you find out from the systems alone?",
  motivation:
    "A data engineer who joins a platform they did not build is asked questions like these:\n\n- Can we delete `products.parquet`?\n- What stops working if the checkout renames a column in `orders.parquet`?\n- Is Thursday's total wrong, and since when?\n- Who should I ask about `daily_sales`?\n\nA wrong answer to the first breaks a program that still reads the file. A wrong answer to the third can leave a total wrong for weeks before anybody notices. None of the four can be answered by reading rows alone.",
  prediction:
    "Before you inspect anything, commit to a belief about Thursday: choose an option, then press the button below it. The lab then shows you the evidence, and you can compare what you expected with what it shows.",
  p1Known:
    '"Who should I ask about `daily_sales`?" was one of the questions at the start of this chapter. You have just read what the warehouse records about `daily_sales`.',
  p1Question: "From that record, what can you conclude about who to ask?",
  p1Explain:
    'The record establishes this much: the warehouse\'s owner field for `daily_sales` names the account `etl_service`. You read that in the inspector.\n\nWhat it does not establish: `etl_service` is the account all four of the shop\'s programs log in as. The lab tells you this; the systems do not.\n\nThe field is called "owner", but the name of a field does not say which question the field answers. This one records which account is named as the owner of the table, not who is responsible for it. An account that several programs share tells you who to ask about the account, not who is responsible for the table.\n\n### What we established\n\n- The warehouse records `etl_service` in the owner field for `daily_sales`.\n- That record names an account, not a person or a team.\n- The record therefore does not establish who is responsible for `daily_sales`.\n- \"Who should I ask?\" remains unanswered by this metadata: answering it needs a record the warehouse does not keep.',
  p1UndecidedLine:
    "You said you could not tell yet, and you cannot: who is responsible for `daily_sales` is not in the record. But you can tell what the record holds: {answer}.",

  p2Known: "The dashboard shows 51.50 for Thursday. `daily_sales` holds the same total.",
  p2Question:
    "What total do you expect for Thursday's orders, if you add up price times quantity over Thursday's rows in `orders.parquet`?",
  p2UndecidedLine:
    "You said you could not tell yet. The page so far does not show how `daily_sales` was made, so you cannot tell from it; adding up Thursday\'s rows can. The lab found {answer}.",

  p2Explain:
    "Thursday's rows of `orders.parquet` add up to 205.50, but the reported total for Thursday is 51.50. The two numbers describe the same day, so the change happened somewhere between the raw orders and the reported total.\n\nThursday's raw total is not unusually low: it is close to Wednesday's (198.75) and Friday's (204.24). That is evidence against a slow day of orders. It does not show what changed the total on the way to the dashboard.\n\nThe table compares every day: the totals are equal on three days (Monday, Friday and Sunday) and differ on four (Tuesday, Wednesday, Thursday and Saturday). Three days match and four differ, so this is not one day's oddity to explain away: the pattern across the week is the next thing to inspect.\n\n### What we established\n\n- Thursday's raw total is 205.50; the reported total is 51.50.\n- The reported total is not simply each day's raw total.\n- The change happened somewhere between `orders.parquet` and `daily_sales`.",
  wQuestion:
    "Thursday's orders in `orders.parquet` add up to 205.50. `daily_sales` and the dashboard both show 51.50. Somewhere between them, the total changed. Which asset would you inspect first to find where, and what would you look for there?",
  wMine: "You will start with: {choice}.",
  /** What the chosen asset can show: a fact of its shape, never what it shows for Thursday. */
  wAfter: {
    orders:
      "Each row of `orders.parquet` is an order, with its price, quantity and status. It shows what Thursday's 205.50 is made of. It does not say which orders `daily_sales` counts.",
    clean:
      "Each row of `clean_orders` is an order too, with the same columns as `orders.parquet`. Compared with the raw file, it shows which orders the two hold differently.",
    daily:
      "`daily_sales` keeps one row per day: the day and its revenue. It shows 51.50, and not which orders make it up.",
    dashboard:
      "The dashboard keeps the values it shows, one per day. It shows 51.50, and nothing about orders.",
  },
  wNext:
    "The inspector below opens on the asset you chose. Inspect it first, then inspect any other asset you need.",
  hQuestion:
    "Thursday's `orders.parquet` rows add up to 205.50, but `daily_sales` holds 51.50. Which explanation will you test?",
  hMine: "You will test: {choice}.",
  hTest:
    "In the next section, the query builder adds up an asset's rows and compares each day with `daily_sales`. Once your query rebuilds `daily_sales`, a check at the end of that section reads the rows and says which explanations they support.",
  cMine: "You chose to test: {choice}.",
  cNone: "You did not choose an explanation to test.",
  cLab: "Of Thursday's {orders} orders in `orders.parquet`, {kept} are among the rows your query keeps, each at the same price and quantity and on the same day. The other {left} are not, and together they are worth {leftTotal}, the whole difference.",
  cExplain:
    "The rows support one explanation. Some of Thursday's orders are not counted.\n\nThey rule out the other two. No order is counted at a lower value, and none on another day.\n\nThe rows do not say why those orders were left out. Ask: what do they have in common?\n\nThe challenge at the end of this chapter asks which rows the cleaning keeps.\n\nYou now have a fact, evidence for an explanation, and the explanation itself in front of you. Keep these apart:\n\n**Fact.** `daily_sales` contains 51.50 for Thursday. You read that in the table.\n\n**Evidence.** A query over the cleaned orders reproduces that result. You ran it yourself.\n\n**Explanation.** The shop's program creates `daily_sales` from completed orders. The first two you observed; the third the query does not establish, and the next section tests it.\n\n### What we established\n\n- A query over the cleaned orders that keeps completed orders and adds up price times quantity per day gives `daily_sales` exactly: the data is evidence for how the reported total was made.\n- The evidence does not show why the left-out rows are left out, nor that this is the query the shop runs.",
  inspectorLead:
    "Choose an asset from the list. The inspector asks every asset the same eight questions.\n\nThen, if you like, try one of these:\n\n- open `orders.parquet` and `clean_orders` in turn, and set their rows beside each other to find which rows are missing or duplicated;\n- open each of the seven assets in turn, note the last time each was written, and say what that order suggests and what it cannot prove;\n- open `daily_sales` in the inspector and check what the systems record for each question.",
  construction:
    "The systems do not say where `daily_sales` comes from. The data may still show it: a query over another asset might give `daily_sales` exactly.\n\nA query **rebuilds** an asset when it gives every row the asset has, with the same values.\n\nBuild one with the query builder below. It writes your choices as SQL and runs the query on Monday morning's data.\n\nIf your query rebuilds `daily_sales`, have you found out how `daily_sales` was made?",
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
    "This experiment tests whether rebuilding `daily_sales` with a query shows how it was made.\n\nIt runs your query from the construction section again, so it starts once your query passes its tests.\n\nEach change gives a different week: the lab runs the whole week again from Monday with that change. The builder's choices cover every asset in the systems that week.\n\nAfter a change runs, the experiment shows the queries in the builder's choices, what the systems hold on Monday morning, and your query's rows against the new `daily_sales`.",
  changeQuestion:
    "After this change, how many queries in the builder's choices will rebuild `daily_sales`?",
  outcomeCopy:
    "A new file appears in object storage: `clean_orders_copy.parquet`, in the bucket `shop-scratch`, last modified at 02:15, with the same 44 rows as `clean_orders`.\n\nNow 2 queries rebuild `daily_sales`: the same query over `clean_orders` and over the copy.\n\nThe data cannot say which of the two `daily_sales` was built from. Both fit equally well.\n\nThe systems show the new file, but no metadata identifies who created it or why.",
  outcomeRefunds:
    "Before the edit, the program kept completed orders only.\n\nThe shop has no refunds: every order is completed or cancelled.\n\nSaturday's row now reads 215.49, because Saturday's cancelled order counts. The dashboard shows the same. In the week as it first ran it read 191.49.\n\nSunday's row is unchanged, 97.75, because Sunday had no cancelled order.\n\nThe systems show no other difference: `daily_sales` still has 7 rows and the same last-written time.\n\nNone of the builder's choices rebuilds `daily_sales` any more. A query with a condition on the date would, and the builder offers none.\n\nNo metadata says whether Saturday's total is a mistake or a deliberate change.",
  outcomeFailed:
    "On the last night, the program that writes `daily_sales` fails and writes nothing.\n\n`daily_sales` has 6 rows, with no row for Sunday. It was last altered on Sunday 13 September at 02:30, a day before `clean_orders` (Monday at 02:05) and the dashboard (Monday at 03:00).\n\nThe dashboard refreshed on Monday at 03:00 as on every morning, and shows 6 values. Its own record shows that Monday-morning refresh, so it looks up to date.\n\nThe systems show that `daily_sales` is a day behind. They do not show that a write was due on Monday, or that one failed.\n\nYour query still rebuilds `daily_sales`: it gives the 6 rows `daily_sales` has, and a seventh, for Sunday, that `daily_sales` lacks.",
  afterAll:
    "Rebuilding `daily_sales` suggested how it was made, but did not show it. Each of the three changes altered that evidence.\n\nThe copy made it ambiguous: two assets fit equally well.\n\nThe edit left none of the builder's choices that fits.\n\nThe failed night left the dashboard looking up to date over a table a day behind.\n\nThe systems kept some traces: the copy left a new file, and the failed night a stale time.\n\nNone of the changes left a record of the change itself: what changed, who changed it, or why.\n\n### What we established\n\n- A rebuild is evidence for how an asset was made, never proof: a copy fits as well as the original, an edit can leave no fitting query, and a failed night can leave the dashboard looking up to date.\n- In every changed week, the rows and the last-written times were still there to read. In none of them did any system record the change itself: what changed, who changed it, or why. Without that record, the data cannot establish what happened.",
  explanation:
    "Each system that holds data keeps some information about its own assets.\n\nObject storage keeps each file's location, its size and when it was last modified. A Parquet file carries its own column names, their types and its row count, written inside the file after its rows. That is where the inspector found a file's columns. The warehouse keeps each table's column names and types, its row count, its size, when it was created and when it was last altered, and the name of the account that owns it. The reporting tool keeps the dashboard's title, who created it and when, when it last refreshed and its values.\n\nThese are the lab's choices of what each kind of system keeps. Each field is one the system uses for its own work. The warehouse uses column names and types to run a query. Object storage uses a file's location to serve it. The reporting tool uses the values to draw its chart.\n\nNone of the three keeps what your questions asked about who is responsible for an asset, what made it, what reads it or what changed in it. The programs exist, and each is due to run at its time, but no system records them: you cannot read them anywhere.",
  mapLead:
    "The eight questions about `daily_sales` differ in what can answer them. They fall into three groups:\n\n- The systems record it.\n- The data suggests it.\n- Only a record kept at the time answers it.\n\nThese are three kinds of knowledge, and they are not the same. A system's record says what it holds now. The data can suggest how something came to be. A record kept at the time says what actually happened.\n\nA question goes with the data when the data itself can answer it. A query might reproduce the asset's rows. Another asset might hold the same values. A last-written time, beside rows that fit it, might show that a write worked. These are evidence, not proof.\n\nFor each question, choose the group that can answer it, then check your sorting. After you check, the lab places each question itself, by reading the systems and trying every query the builder offers. You can then choose any change from the failure experiment, and the lab places the questions again for that week.",
  mapAfter:
    "The data's group holds evidence, not a certainty. A change to the shop can move a question out of the data's group.",
  generalisation:
    "Once you have checked your sorting, look at the questions in the group \"Only a record kept at the time answers it\". The lab tags each with the kind of record that would answer it.\n\nThere are three kinds of record:\n\n- a record of what the asset is: who is responsible for it, the unit of its numbers;\n- a record of what happened: what changed in it, when it was written, whether a write worked;\n- a record of what was made from what: what it is made from, how its numbers are worked out, what reads it.\n\nThe groups say what can answer a question now. The kinds say what record would answer it for certain. The two sortings need not line up.\n\nOne column in the data names people: `updated_by` in `products.parquet` says who last edited each product's row. That is a fact about a product, not a record of who is responsible for the file.\n\nAfter the edit to the program, two questions about what made `daily_sales` left the data's group.\n\nInformation about an asset or about the platform is called **metadata**: what an asset is, where it came from, who is responsible for it, what its numbers mean, how it is made, and how it relates to other assets. Metadata can live inside the system that holds the data, as the warehouse's column names and types do. It can live next to the data, inside the same file, as a Parquet file's own column names and types do. It can live in a system of its own. What the systems keep (names, types, row counts, sizes, times, an owner's name) is metadata too: the part each system keeps for its own work. The questions only a record answers need the rest.\n\nThe rest of this course builds a system that keeps all three kinds.",
  c2Task:
    "Choose four rules that turn `orders.parquet` into `clean_orders`. The tests check that your rules keep every row `clean_orders` has, and no row it lacks.",
  c2Hints: [
    "Open `orders.parquet` and `clean_orders` in the inspector, in turn, and set their rows beside each other. Which rows are missing, and which appear fewer times?",
    "A common mistake: dropping cancelled orders. `clean_orders` keeps them; `daily_sales` leaves them out later.",
    "On Wednesday, order 7015 appears twice in `orders.parquet` and once in `clean_orders`.",
    "Keep one row of an order that appears twice. Drop orders with no customer id.",
    "Keep one row of an order that appears twice. Drop orders with no customer id. Keep cancelled orders. Either choice passes for the quantity rule.",
  ],
  c2Lead:
    "`clean_orders` is made from `orders.parquet` by rules you cannot read. Recover them from the two files by choosing, for each kind of row that differs between them, whether the rules keep it. The tests compare the rows your rules keep with `clean_orders`. Your rules appear as SQL below the choices.",
  p3Question:
    "Your rules pass. Is your setting of the four rules the only one that gives `clean_orders` exactly?",
  p3Explain:
    "Two settings pass. They differ only in the rule for orders with a quantity of 0 or less. No order this week had a quantity of 0 or less, so either choice keeps the same rows. The shop's program drops such orders. This week's data cannot show that rule, however you rebuild it.",
  reflection:
    "The systems tell you what exists now: which assets there are, their columns and rows, and when each was last written. The data can sometimes suggest what made an asset: your query rebuilt `daily_sales`, and your four rules rebuilt `clean_orders`. The data cannot prove it: a copy fitted as well, an edit left no matching query in the builder, and two settings of the rules rebuild `clean_orders`. Neither the systems nor the data tell you for certain what happened, why it happened, who is responsible, or what depends on an asset. Those are things somebody has to record on purpose, when they happen.\n\nThe three orders your check found left out are the three with no customer id. Every setting of the rules that passes drops orders with no customer id.\n\nNothing you could read says whether leaving them out is a fault in the checkout or a rule somebody chose.\n\nThe four questions from the start each needed a record nobody kept:\n\n- Can we delete `products.parquet`? It needs a record of what reads it. No program in the lab reads it, but the systems could not show you that.\n- What stops working if the checkout renames a column in `orders.parquet`? It needs a record of what reads that file and what is made from it.\n- Is Thursday's total wrong, and since when? It needs a record of what happened, and of the rule somebody chose.\n- Who should I ask about `daily_sales`? It needs a record of what the asset is, including who is responsible for it.\n\nWhat would you write down about `daily_sales` so that the next person need not rebuild it? Who should write it down, and when?\n\nThe systems hold what exists now: the assets, their rows, and the times they were written. The data can give you evidence about how something came to be, but without records of changes, ownership, dependencies and transformations, neither can tell you what happened, why it happened, or who was responsible. Those things have to be recorded deliberately, when they happen.",
  modelVsReality:
    "Some real systems keep history that the lab's warehouse does not. An Apache Iceberg table keeps snapshots, each the state of the table at some time. A Delta Lake table keeps, for each write, the operation, the user and the time, for 30 days by default. The lab's systems keep only the current rows.\n\nIn some real databases, a table's owner is an account too. In PostgreSQL, for example, a new table's owner is normally the account that created it. At first, only the owner (or a superuser) can do anything with the table. Other accounts can use it once they are given the right to. The right to alter or drop the table comes with being its owner. The lab's warehouse records the owning account and models no such rights.\n\nThe lab's sizes are estimates from the rows.\n\nThe lab works in UTC and has no time zones.\n\nA real platform has hundreds or thousands of assets. Searching for queries that rebuild one would cost far more.\n\nThe lab's search covers only the query builder's choices. \"None of the builder's choices rebuilds it\" means none of those choices; a query outside them might.",
} as const;
