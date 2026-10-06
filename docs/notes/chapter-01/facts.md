# Chapter 1 fact sheet: The invisible data system

Every brief for Chapter 1 attaches this sheet. Each fact was read off the lab (`packages/lab`) on
6 October 2026; the chapter's facts test pins every number below. Do not add a number that is not
here. Do not change a number.

## The situation

- An online shop sells bicycle parts. It opened its online store on Monday 7 September 2026.
- You (the learner) start work on Monday 14 September 2026, at 09:00. You are a data engineer who
  has just joined.
- You can read everything in the shop's storage. You cannot see anything else yet: not the code,
  not the timetable, not anybody's notes.
- All times are UTC. Write a time like this: Monday 14 September, 02:30.

## The seven assets

An asset is anything the platform stores or shows: a file, a table, a dashboard.

| Asset | Where it lives | Rows |
| --- | --- | --- |
| customers.parquet | object storage, bucket shop-raw | 10 |
| orders.parquet | object storage, bucket shop-raw | 48 |
| products.parquet | object storage, bucket shop-raw | 8 |
| clean_customers | the warehouse, shop.analytics | 9 |
| clean_orders | the warehouse, shop.analytics | 44 |
| daily_sales | the warehouse, shop.analytics | 7 |
| sales_dashboard | the reporting tool | shows 7 values |

## What each storage system records about an asset (and nothing else)

- Object storage: the file's location, its size, and when it was last modified. A Parquet file
  also carries, inside it, its column names, their types and its row count.
- The warehouse: each table's column names and types, its row count, its size, when it was
  created, when it was last altered, and the account that owns it.
- The reporting tool: the dashboard's title ("Sales, last 7 days"), who created it (j.marsh) and
  when (2 September 2026), when it last refreshed, and the values it shows.

## Monday morning, as storage shows it

- orders.parquet last modified Monday 14 September, 01:00. customers.parquet 01:02.
  products.parquet 01:04.
- clean_customers last altered 02:00. clean_orders 02:05. daily_sales 02:30.
- sales_dashboard last refreshed 03:00.
- The warehouse names `etl_service` as the owner of all three tables. (The lab knows, and storage
  does not show, that etl_service is the account the shop's programs log in as.)

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

## Adding up orders.parquet per day

If you add up price times quantity over every row of orders.parquet, per day, and compare with
daily_sales: the totals are the same on 3 of the 7 days (Monday, Friday, Sunday) and different on
4 (Tuesday 192.24, Wednesday 198.75, Thursday 205.50, Saturday 215.49). Each difference is one of
the things above: the cancelled order, the order written twice, the orders with no customer id,
the cancelled order.

## Rebuilding daily_sales

The query builder offers: an asset to read; which rows to keep (every row, completed orders only,
cancelled orders only); what to add up (price times quantity, quantity, the number of rows); and
per what (the day the order was placed, the customer, the product). Exactly one choice rebuilds
daily_sales: read clean_orders, keep completed orders only, add up price times quantity, per day.

## Three changes storage does not record (the failure experiment)

1. An analyst's copy. A script copies clean_orders every night to
   `clean_orders_copy.parquet`, in a second bucket, shop-scratch, at 02:15, before daily_sales is
   written. The copy has the same 44 rows. Now two queries rebuild daily_sales: the same query
   from clean_orders and from the copy. The data cannot say which one daily_sales was built from.
2. A program edited for refunds. From Saturday's row on, the program that writes daily_sales
   keeps every order whose status is not "refunded", where it kept completed orders. The shop has
   no refunds. Saturday's row now reads 215.49, not 191.49, because Saturday's cancelled order now
   counts; the dashboard shows the same change. Sunday's row is unchanged, 97.75, because Sunday
   had no cancelled order. Storage shows
   nothing else different: the same 7 rows, the same last-written time. No query in the builder's
   choices rebuilds daily_sales any more.
3. A failed night. On the last night, the program that writes daily_sales fails and writes
   nothing. daily_sales has 6 rows, with no row for Sunday, and was last altered on Sunday 13
   September at 02:30. The dashboard refreshed on Monday at 03:00 as usual and shows 6 values.
   From storage, a failed night looks like a night with nothing to write. The query still
   rebuilds every row daily_sales has, and gives one row more, for Sunday.

## Rebuilding clean_orders (the challenge)

The rule builder offers four rules over orders.parquet: copies of the same order (keep every copy,
keep one), orders with no customer id (keep, drop), cancelled orders (keep, drop), orders with a
quantity of 0 or less (keep, drop). The rules that give clean_orders exactly: keep one copy, drop
orders with no customer id, keep cancelled orders, and either choice for the quantity rule,
because no order this week has a quantity of 0 or less. The program the shop really runs drops
them. No reconstruction from this week's data can find that rule.

## The three columns of questions about daily_sales

| Question | What answers it |
| --- | --- |
| When was it last written? | storage records it |
| What is it made from? | the data suggests it (one query rebuilds it) |
| How are its numbers worked out? | the data suggests it (the same query) |
| What reads it? | the data suggests it (the dashboard shows the same numbers) |
| Did last night's write work? | the data suggests it (last written Monday 02:30, with a row for Sunday) |
| Who is responsible for it? | only a record kept at the time (storage names etl_service, an account) |
| In what units are its numbers? | only a record kept at the time (revenue is a decimal; no currency) |
| What changed in it this week? | only a record kept at the time (storage keeps only the current rows) |

With the analyst's copy, "What is it made from?" stays in the middle column but now has two
candidate sources. With the edit for refunds, it moves to the right-hand column: no query rebuilds
it.

## Words on this page, each with one meaning

- **asset**: a file, a table or a dashboard. Introduced in this chapter.
- **metadata**: introduced at the end of this chapter, in the generalisation: records about assets
  and about the platform that the data does not contain. Do not use the word before that section.
- **row**: a line of data in a file or a table. Never call a row a "record".
- **record**: something written down about an asset or the platform, other than its rows.
- **program**: code that reads assets and writes one. The shop has four. Never "job".
- **storage**: the three systems that hold assets, and what they keep about each.
- **query**: what the learner builds in the query builder, shown as SQL.
- **rebuild**: give exactly the same rows.
- **night**: the hours when the export and the programs run.
- **account**: a login that programs use, such as etl_service.
- **revenue**: the number daily_sales holds for each day. Do not say "sales" for it.

## Words this chapter must not use

Each belongs to a later chapter: lineage, upstream, downstream, job, run (as a noun: say "the
night's work" or "the program"), event, dataset, schema, entity, attribute, identifier, graph (say
"chart" for the dashboard), node, edge, traversal, OpenLineage, facet, namespace, producer,
ingestion, observation, freshness, data quality, assertion, provenance, impact analysis, root
cause, identity, environment, alias, index, partition, retention, descriptive, operational,
catalog, catalogue.
