# Chapter 1 fact sheet: The invisible data system

Every brief for Chapter 1 attaches this sheet. Each fact was read off the lab (`packages/lab`) on
6 October 2026, and read again for the revision after the review, by running it (two statements
the first version carried were not the lab's, and are gone), and again on 7 October 2026 for the
author's second round (the predictions, the map, the definitions); the chapter's facts test pins
every number below. Do not add a number that is not here. Do not change a number.

## The situation

- An online shop sells bicycle parts. It opened its online store on Monday 7 September 2026.
- You (the learner) start work on Monday 14 September 2026, at 09:00. You are a data engineer who
  has just joined.
- You can read everything in the shop's storage. You cannot see anything else yet: not the code,
  not when each program is due to run, not anybody's notes.
- Every figure on the page runs the Metadata Lab: a small data platform, holding the shop, that
  runs in your browser. The lab works out everything a figure shows; it is the one thing on the
  page that knows the shop's insides (for example, that `etl_service` is the account the programs
  log in as). Call it "the lab".
- All times are UTC. Write a time like this: Monday 14 September, 02:30.

## The seven assets

An asset is something in the platform that can be stored, described, changed, related to other
assets, or depended on. The shop's assets are files, tables and a dashboard.

| Asset | Where it lives | Rows |
| --- | --- | --- |
| customers.parquet | object storage, bucket shop-raw | 10 |
| orders.parquet | object storage, bucket shop-raw | 48 |
| products.parquet | object storage, bucket shop-raw | 8 |
| clean_customers | the warehouse, shop.analytics | 9 |
| clean_orders | the warehouse, shop.analytics | 44 |
| daily_sales | the warehouse, shop.analytics | 7 |
| sales_dashboard | the reporting tool | shows 7 values |

## The map of the platform

The chapter shows a small map of the platform near its start, and keeps it to hand.

- The map shows the shop's data platform: its three systems, in the order data moves through them
  each night (object storage, then the warehouse, then the reporting tool), and the assets each
  holds: three files, three tables, one dashboard.
- Between object storage and the warehouse, and between the warehouse and the reporting tool, an
  arrow stands for programs that move data from one system to the next each night. You cannot
  see the programs.
- The map shows no asset made from another. Which file or table feeds which is what this chapter
  finds storage cannot tell. Never draw, describe or hint at a link between two assets.
- The map stays to hand: once its place on the page scrolls out of view, a button at the foot of
  the window opens the same map over the page. The button goes when the map's place comes back
  into view.
- The map shows the week as it first ran. It does not show the analyst's copy or any change.

## What each storage system records about an asset (and nothing else)

- Object storage: the file's location, its size, and when it was last modified. A Parquet file
  also carries, inside it, its column names, their types and its row count.
- The warehouse: each table's column names and types, its row count, its size, when it was
  created, when it was last altered, and the name of the account that owns it.
- The reporting tool: the dashboard's title ("Sales, last 7 days"), who created it (j.marsh) and
  when (2 September 2026), when it last refreshed, and the values it shows. It keeps no query: a
  program fills the dashboard each night, as programs fill the tables.
- These are the lab's choice of what a system of each kind keeps. The lab does not model why a
  system keeps a field. Do not say a system "must" or "needs to" keep anything.
- What storage keeps (names, types, row counts, sizes, times, an owner's name, a creator) is
  itself a kind of record about the assets: each system keeps it for its own work.

## Monday morning, as storage shows it

- orders.parquet last modified Monday 14 September, 01:00. customers.parquet 01:02.
  products.parquet 01:04.
- clean_customers last altered 02:00. clean_orders 02:05. daily_sales 02:30.
- sales_dashboard last refreshed 03:00.
- In that order the seven times run: the three files, then clean_customers, clean_orders,
  daily_sales, and the dashboard last. The order fits programs that each read what an earlier one
  wrote. It does not prove that any one reads another: two writes can follow each other without
  either reading the other.
- The warehouse records the name `etl_service` as the owner of all three tables. The lab knows,
  and storage does not show, that `etl_service` is the account all four of the shop's programs
  log in as. Storage records no creator for a table.

## daily_sales and the dashboard

daily_sales has one row per day, with two columns: `day` and `revenue`. The column `revenue` is a
decimal with two places. No currency is recorded anywhere.

| Day | revenue |
| --- | --- |
| Monday 7 | 147.00 |
| Tuesday 8 | 162.25 |
| Wednesday 9 | 153.75 |
| Thursday 10 | 51.50 |
| Friday 11 | 204.24 |
| Saturday 12 | 191.49 |
| Sunday 13 | 97.75 |

The dashboard shows the same seven values as a chart. Thursday is the lowest. Sunday is the second
lowest.

## What the data shows, if you look

- orders.parquet has 48 rows. clean_orders has 44.
- Order 7015 (Wednesday) appears twice in orders.parquet, and once in clean_orders.
- Three orders on Thursday (7021, 7023, 7025) have no customer id (the cell is NULL) in
  orders.parquet. None of them is in clean_orders. Together they are worth 154.00.
- Thursday had 7 orders in orders.parquet and 4 in clean_orders. Sunday had 5 orders, all 5 in
  clean_orders: Sunday's figure is low because Sunday had fewer orders.
- Two orders are cancelled: 7009 on Tuesday (29.99) and 7037 on Saturday (24.00). Both are in
  orders.parquet and in clean_orders. Neither counts in daily_sales.
- Thursday, the low day: the total of every Thursday row of orders.parquet is 205.50; daily_sales
  has 51.50. The difference, 154.00, is the three orders with no customer id. Nothing in storage
  says whether leaving them out is a fault in the checkout or a rule somebody chose. The course
  leaves that question open in Chapter 1 and comes back to it in later chapters.
- In the reflection, after the rules challenge: the three orders the check found left out are the
  three with no customer id, and every setting of the rules that passes drops orders with no
  customer id.
- products.parquet has a column `updated_by`, holding staff names (k.adeyemi, r.novak, s.lund).
  It says who last edited each product's row. It is a fact about a product, not a record of who
  is responsible for the file. No program in the lab reads products.parquet; storage cannot show
  that.

## The two predictions before storage

Each option of a prediction is a result the learner could expect and the belief it reflects,
never the explanation the result is about to give. The learner has seen the map, the dashboard
and the words before them, nothing else.

1. **The owner, as a requirement.** The shop has set one requirement for its warehouse, in these
   words: "Every table must have an owner." Suppose you write the program that writes daily_sales
   every night: what would you store as the owner of daily_sales? Five options: a person, for
   example whoever built it; a team, for example finance; the program that writes it; an account
   that programs log in as; or nothing yet, because you would first ask what the owner is for.
   No option is right or wrong, and the figure calls none of them either.
   - Each of the first four meets the requirement as written: each puts an owner on the table.
     Each answers a different question about daily_sales:
     - a person: who is responsible for daily_sales?
     - a team: which team is responsible for daily_sales?
     - the program that writes it: which program writes daily_sales?
     - an account: which account controls daily_sales in the warehouse?
   - The requirement does not say which question the owner must answer, so it does not say which
     to store. Somebody has to ask whoever set it what the owner is for.
   - The lab then shows what the shop's warehouse holds: `etl_service` as the owner of
     daily_sales, and an owner for 3 of its 3 tables, `etl_service` for each. `etl_service` is the
     account all four of the shop's programs log in as; the lab knows this, storage does not show
     it. The shop's tables have no person or team as owner.
   - So the warehouse meets the requirement as written: every table has an owner. The warehouse
     has its own meaning of owner: the account that controls the table. Of the four questions,
     `etl_service` answers only the last.
   - "Who should I ask about daily_sales?", one of the four questions at the start of the chapter,
     needs a person or a team. The warehouse's owner names neither.
   - The name of a field does not say which question the field answers.
2. **Thursday.** The dashboard shows 51.50 for Thursday, and daily_sales holds the same figure for
   Thursday. Add up price times quantity over Thursday's rows of orders.parquet: what do you
   expect the total to be? Three options, each a total and the belief behind it:
   - 51.50: daily_sales holds the total of Thursday's orders;
   - a different total: daily_sales is not simply the total of Thursday's orders;
   - I can't tell yet: nothing so far says what daily_sales measures.
   Nothing before the result says or hints whether the totals differ, or why they might.
   The lab finds a different total: 205.50 against 51.50. Only now is there a difference to
   explain. Thursday's raw total is close to Wednesday's (198.75) and Friday's (204.24), so
   Thursday was not a slow day in orders.parquet. The totals are equal on three days (Monday,
   Friday and Sunday) and differ on four, Thursday among them. What explains the difference is
   for the next section, where the learner reads the rows; the prediction does not say.

## Where to look first (the investigation's opening decision)

Once the Thursday prediction has shown the difference, the investigation opens with a decision:
which asset would you inspect first, to find where Thursday's 205.50 became 51.50, and what would
you look for there? Four options, each an asset and the evidence sought:

- orders.parquet, for the orders that make up Thursday's 205.50;
- clean_orders, to set its Thursday orders beside the raw ones;
- daily_sales, for how its 51.50 was worked out;
- the dashboard, for where its 51.50 comes from.

No option is right: it is a decision about where to look. After the choice, one line says what
that asset can show, a fact about the asset's shape, never what it shows for Thursday:

- each row of orders.parquet is an order, with its price, quantity and status: it shows what
  Thursday's 205.50 is made of, and does not say which orders daily_sales counts. It is not one
  row per order: order 7015 appears twice, which the learner finds in the chapter's last
  challenge, so this line says nothing about how many rows an order has;
- each row of clean_orders is an order too, with the same columns as orders.parquet: set beside
  it, it shows which orders the two hold differently;
- daily_sales keeps one row per day, the day and its revenue: it shows 51.50, and not which orders
  make it up;
- the dashboard keeps the values it shows, one per day: it shows 51.50, and nothing about orders.

Then the inspector, below, opens on the chosen asset, and the learner may open any other. The
choice of an explanation to test comes after the inspector.

The decision states what the Thursday prediction found, and it sits just below that prediction,
in view while the learner is still choosing. So it waits until the learner has committed their
answer there, and the choice of an explanation waits for the decision; until then, one line
stands in place of each, naming the figure it waits for by its caption. Nothing that shows before
the answer (a caption, the words above the inspector) may say that Thursday's totals differ.

## Testing an explanation for Thursday

Once the Thursday prediction has shown the difference (205.50 against 51.50), and the learner has
decided where to look first and used the inspector, the investigation ends with a choice: which
explanation will you test? Three explanations, each one a reasonable engineer could hold:

- some of Thursday's orders are not counted in daily_sales;
- Thursday's orders are counted, but at lower values;
- some of Thursday's orders are counted on another day.

The figure keeps the choice and reveals nothing. The learner tests it with the query builder in the
construction section, which adds up an asset's rows and compares each day with daily_sales; the
inspector, above the choice, has already shown them Thursday's rows. There is no "I can't tell yet": the figure asks which
explanation to test, not which is true.

Once the learner's query rebuilds daily_sales, a check after the challenge reads the rows, at a
press: of Thursday's 7 orders in orders.parquet, 4 are among the rows the learner's query keeps,
each at the same price and quantity and on Thursday; the other 3 are not, and together they are
worth 154.00, the whole difference. So the rows support the first explanation, and rule out the
other two: no order is counted at a lower value, and none on another day. The check does not say
why the three were left out, and must not say they have no customer id: the challenge at the end
of the chapter asks the learner to find which rows the cleaning keeps. (Before the rebuild passes,
nothing may name clean_orders as what daily_sales is made from.)

## Adding up orders.parquet per day

If you add up price times quantity over every row of orders.parquet, per day, and compare with
daily_sales: the totals are the same on 3 of the 7 days (Monday, Friday, Sunday) and different on
4 (Tuesday 192.24, Wednesday 198.75, Thursday 205.50, Saturday 215.49). Each difference is one of
the things above: the cancelled order, the order written twice, the orders with no customer id,
the cancelled order. A learner who expects only Thursday to differ expects 6 equal days; the lab
finds 3.

## Rebuilding daily_sales

A query **rebuilds** an asset when it gives every row the asset has, with the same values. The
query builder offers: an asset to read (customers.parquet, orders.parquet, products.parquet,
clean_customers or clean_orders); which rows to keep (every row, completed orders only, cancelled
orders only); what to add up (price times quantity, quantity, the number of rows); and per what
(the day the order was placed, the customer, the product). Exactly one choice rebuilds
daily_sales. (Do not state it in any text a learner reads before passing the challenge.) A query
that rebuilds an asset suggests how the asset was made. It does not show it: the failure
experiment finds a second asset that fits as well, an edit that leaves no choice that fits, and a
failed night the query does not notice. The construction asks the question; the failure
experiment answers it. Do not answer it in the construction.

## Three changes to the shop (the failure experiment)

The experiment re-runs the learner's own query, so it starts once their query passes. Each change
gives a different week: the lab runs the whole week again from Monday with that change. The
builder's choices cover every asset in storage that week, so the analyst's copy is among them in
the copy's week. Before each change runs, the learner predicts what the data will then say about
where daily_sales comes from, as the number of queries in the builder's choices that rebuild it:
none (the data no longer points to any query), one (it still points to one), or two or more (it
fits more than one). The lab answers: 2 after the copy, 0 after the edit, 1 after the failed
night. The learner can reason to each before it runs: a copy has the same rows; the edit keeps
cancelled orders from Saturday's row on but not before, and every builder choice keeps the same
rows on every day; the failed night leaves a table with one row fewer, and "rebuild" asks only for
the rows the asset has. Storage in a changed week holds only that week's values; any
comparison with the week as it first ran is the lab's, because the lab ran both weeks.

1. An analyst's copy. A script copies clean_orders every night to
   `clean_orders_copy.parquet`, in a second bucket, shop-scratch, last modified at 02:15, before
   daily_sales is written. The copy has the same 44 rows. Now 2 queries rebuild daily_sales: the
   same query from clean_orders and from the copy. The data cannot say which one daily_sales was
   built from. Storage shows the new file; nothing says who made it or why.
2. A program edited for refunds. From Saturday's row on, the program that writes daily_sales
   keeps every order whose status is not "refunded", where it kept completed orders only. The
   change's label says what the edit does, so the learner can reason about it before it runs; it
   must say "from Saturday's row on", not a day or time of the edit, which the lab does not
   record. The shop
   has no refunds: every order is completed or cancelled. Saturday's row now reads 215.49 (it read
   191.49 in the week as it first ran), because Saturday's cancelled order now counts; the
   dashboard shows the same. Sunday's row is unchanged, 97.75, because Sunday had no cancelled
   order. Storage shows nothing else different: the same 7 rows, the same last-written time. No
   query in the builder's choices rebuilds daily_sales any more. A query with a condition on the
   date would, and the builder offers none: so say "none of the builder's choices", never that
   rebuilding is impossible. Nothing says whether Saturday is a mistake or a decision.
3. The last night's write fails. On the last night, the program that writes daily_sales fails
   and writes nothing. daily_sales has 6 rows, with no row for Sunday, and was last altered on
   Sunday 13 September at 02:30: a day before clean_orders (Monday 02:05) and the dashboard
   (Monday 03:00). The dashboard refreshed on Monday at 03:00 as it does every morning and shows 6
   values; its own record says it is up to date. Storage shows that daily_sales is a day behind,
   but not that a write was due on Monday, or that one failed. The query still rebuilds
   daily_sales: it gives the 6 rows daily_sales has, and a seventh, for Sunday, that daily_sales
   lacks. (Do not compare a failed night with a quiet one: the lab has no week without orders.)

After all three: the copy left a new file and the failed night a stale time, but none of the
changes left a record of the change itself: what changed, who changed it, or why.

## Rebuilding clean_orders (the challenge)

The rule builder offers four rules over orders.parquet: an order that appears twice (keep both
rows, keep one), orders with no customer id (keep, drop), cancelled orders (keep, drop), orders
with a quantity of 0 or less (keep, drop). That makes 16 settings. Exactly 2 of them give
clean_orders exactly, and they differ only in the quantity rule, because no order this week has a
quantity of 0 or less. The shop's program drops such orders. No rebuilding from this week's data
can find that rule. (Do not state the passing settings in any text a learner reads before
passing.) After a pass, the learner predicts whether their own setting is the only one that
passes, or whether another setting can match every row too. The options must not name a rule, or
say that a rule decides no row: that is the explanation the result gives. The lab answers more
than one: 2.

## The three groups of questions about daily_sales

The inspector asks every asset the same eight questions. A figure places the eight questions about
daily_sales in three groups, by what can answer them, and the lab works out each place. Do not
call this figure a map: "map" is the platform's map. Call it the figure, or speak of your sorting. Name a
group by its heading, never by its position (on a phone they stack):

- **Storage records it.**
- **The data suggests it**: a query rebuilds the asset, another asset shows the same numbers, or
  the last-written time and the latest row fit a write that worked.
- **Only a record kept at the time answers it.**

| Question | Group, in the week as it first ran |
| --- | --- |
| When was it last written? | storage records it |
| What is it made from? | the data suggests it (one asset rebuilds it) |
| How are its numbers worked out? | the data suggests it (one query rebuilds it) |
| What reads it? | the data suggests it (the dashboard shows the same numbers) |
| Did last night's write work? | the data suggests it (last written Monday 02:30, with a row for Sunday) |
| Who is responsible for it? | only a record kept at the time (storage records the name etl_service) |
| In what units are its numbers? | only a record kept at the time (revenue is a decimal; no currency) |
| What changed in it this week? | only a record kept at the time (storage keeps only the current rows) |

Before the lab places them, the learner places all eight and commits; the lab then shows its
places and marks where the learner's differ. A week selector places them again on each change: with the
copy, "What is it made from?" stays with the data, with two assets; with the edit, "What is it made
from?" and "How are its numbers worked out?" leave the data's group for the record's; with the
failed night, "Did last night's write work?" stays with the data, and its evidence becomes "last
written Sunday 02:30; the latest row is for Saturday, not Sunday".

Each question that only a record answers is tagged with the kind of record that would answer it:

- a record of **what the asset is**: who is responsible for it; in what units its numbers are;
- a record of **what happened**: what changed in it; also when it was last written and whether
  last night's write worked;
- a record of **what was made from what**: what it is made from; how its numbers are worked out;
  what reads it.

The groups say what can answer a question now; the kinds say what record would answer it for
certain. They are different sortings and need not line up.

## Words on this page, each with one meaning

- **asset**: something in the platform that can be stored, described, changed, related to other
  assets, or depended on; the shop's are files, tables and a dashboard. Introduced at the start of
  this chapter, with the map.
- **metadata**: introduced at the end of this chapter, in the generalisation: information about an
  asset or about the platform: what an asset is, where it came from, who is responsible for it,
  what its numbers mean, how it is made, and how it relates to other assets. It can live inside the
  system that holds the data (the warehouse keeps each table's column names and types), next to
  the data (a Parquet file carries its own column names, types and row count after its rows), or
  in a system of its own. Never say metadata is kept apart from the data: some of it is not. Do not
  use the word before the generalisation.
- **map**: the map of the platform, and nothing else. Never call the figure that sorts the
  questions a map.
- **row**: a line of data in a file or a table. Never call a row a "record".
- **record**: something written down about an asset or the platform, other than its rows.
- **program**: code that reads assets and writes one. The shop has four. Never "job".
- **storage**: the three systems that hold assets, and what they keep about each. Say once, early,
  that "storage" means all three.
- **platform**: the whole of it: the assets, the three systems and the programs.
- **query**: what the learner builds in the query builder, shown as SQL.
- **rebuild**: a query rebuilds an asset when it gives every row the asset has, with the same
  values.
- **night**: the hours when the export and the programs run. The failure is always "the last
  night's write".
- **responsible**: the one word for who answers for an asset. Not "answerable", not "answers for".
  "Answer" is for questions only.
- **an order that appears twice**: the repeated order 7015. Not "a copy": "copy" is the analyst's
  file.
- **account**: a login that programs use, such as etl_service.
- **owner**: on this page the word has several meanings, and that is the point of the requirement
  figure. Never use it alone where it could mean more than one: say "the warehouse's owner" for
  the account the warehouse records, and quote the requirement's word as "owner".
- **requirement**: something the shop has written down that its platform must do. This chapter
  has one: "Every table must have an owner."
- **revenue**: the number daily_sales holds for each day. Do not say "sales" for it.

## Words this chapter must not use

Each belongs to a later chapter: lineage, upstream, downstream, job, run (as a noun: say "the
night's work" or "the program"), event, dataset, schema, entity, attribute, identifier, graph (say
"chart" for the dashboard), node, edge, traversal, OpenLineage, facet, namespace, producer,
ingestion, observation, freshness, data quality, assertion, provenance, impact analysis, root
cause, identity, environment, alias, index, partition, retention, descriptive, operational,
catalog, catalogue.

## What the chapter found, at its end

Said once, at the start of the reflection, as a short summary:

- Storage tells you what exists now: which assets there are, their columns and rows, and when each
  was last written.
- The data can sometimes suggest what produced an asset: a query rebuilt daily_sales, and four
  rules rebuilt clean_orders. It cannot prove it: a copy fitted as well, an edit left no choice
  that fits, and two settings of the rules fitted clean_orders.
- Neither storage nor the data tells you for certain what happened, why it happened, who was
  responsible, or what depends on an asset.
- Those are things somebody has to record on purpose, when they happen.

## How the lab differs from a real platform (the closing note)

- Real systems keep different things. Some keep history that the lab's warehouse does not: an
  Apache Iceberg table keeps snapshots, each the state of the table at some time (the Iceberg
  table specification); a Delta Lake table keeps, for each write, the operation, the user and the
  time, for 30 days by default (Delta Lake's documentation of its history command). The lab's
  storage keeps only the current rows.
- The lab's sizes are estimates from the rows.
- The lab works in UTC and has no time zones.
- A real platform has hundreds or thousands of assets. Searching for queries that rebuild one
  would cost far more.
- The lab's search covers only the query builder's choices. "None of the builder's choices
  rebuilds it" means none of those choices; a query outside them might.
- In some real databases a table's owner is an account too. In PostgreSQL, for example, a new
  table's owner is normally the account that created it. At first only the owner (or a superuser)
  can do anything with the table; other accounts can use it once they are given the right to. The
  right to alter or drop the table comes with being its owner (PostgreSQL's documentation,
  "Privileges"). Not every database gives a table an owner. The lab's warehouse records the owning
  account and models no such rights.
