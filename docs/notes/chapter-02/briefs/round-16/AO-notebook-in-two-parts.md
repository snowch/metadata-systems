# Brief AO: the notebook chapter in two parts

The author asked for Chapter 1's notebook to be split in two: part 1 gets the reader used to the
shop and what happens on its platform; part 2 starts from the problem, Thursday's revenue, and is
the chapter's essay as it stands. These are the only new words. Every fact below was read off the
shop's engine (`notebook/shop`) on 10 October 2026 and is pinned by its tests. Write each slot as
plain sentences, following `docs/style.md` and the writing standard in `AGENTS.md`. Write only the
slots below, each under its key. Do not add facts. Do not mention a lab, an engine, a simulator,
marimo, Pyodide or WebAssembly. The reader is "you", a data engineer. British English. No em
dashes.

## Who reads this

A data engineer on their first Monday at an online shop that sells bicycle parts. The page is a
notebook: prose, figures, and cells of Python they can run, change and run again. Part 1 is one
page and part 2 another; part 2 links back to part 1 and part 1 links on to part 2.

Words the chapter has not introduced yet, and which no slot may use: metadata (part 2 introduces
it), schema, dataset, lineage, job, event, identifier, attribute, entity, environment,
observation, freshness, index, partition, producer, delivery, alias, upstream, downstream. "Run"
is fine as a verb (run a cell); not as a noun.

## What part 1 already says, kept word for word (do not redraft; your slots sit around these)

1. Under the heading "The shop and its platform": "You start work on Monday 14 September 2026 at
   09:00, as the data engineer of an online shop that sells bicycle parts. The shop opened its
   online store a week ago, on Monday 7 September. Nobody who built its data platform is there to
   ask, and nothing about it is written down." Then slot **task**.
2. "The platform has three systems: object storage, which holds files; a warehouse, which holds
   tables; and a reporting tool, which holds a dashboard. Every night, programs read the files,
   write the tables and refresh the dashboard. You can read everything the three systems hold. You
   cannot see the programs, when they are due to run, or any note anybody kept."
3. A paragraph on how to run a cell (a triangle at the top right of the cell; Ctrl+Enter). Then
   slot **names**.
4. A figure of the three systems and the files, tables and dashboard each holds, with the count
   "3 files + 3 tables + 1 dashboard = 7 assets", and under it: "An asset is one thing the platform
   holds: here, a file, a table or a dashboard."
5. "The shop's first week ran from Monday 7 to Sunday 13 September. Each night, in the early hours
   of the next day, the three files are written again, then programs write the tables and refresh
   the dashboard. The last night ends early on Monday 14 September, before you start work." Then
   a figure of the week.
6. Kept, but moved into the slots named: "`products.csv` names its columns once, in its first line,
   and has no types: every value is text." (goes in **products**); "`orders.jsonl` and
   `customers.jsonl` are JSON Lines, with one record per line, and every record names its fields. A
   JSON value has one of a few types, such as a string, a number, true or false, or null, and a date
   or an amount is just a string or a number." (goes in **customers**). Reproduce these sentences
   exactly where your slot places them.

## Slots for part 1

- **title_1**: the page's main heading. Facts: the chapter is Chapter 1, "The invisible data
  system"; this page is its part 1, about the shop and its platform. The heading names the
  chapter, the part and the part's subject. At most twelve words.
- **app_title_1**: the browser tab's title for this page, at most six words.
- **objectives_1**: three or four bullets, each one sentence that starts with a verb: what you can
  do after this page. Facts to choose from: name the shop's three systems and which of its seven
  assets each holds; read the shop's products, customers and orders as its files store them; read
  the rows of the warehouse's three tables and the values the dashboard shows; say what happens on
  the platform each night, and what of it you cannot see (the programs, when they are due to run,
  any notes); run a cell, change it and run it again.
- **task**: one sentence after the situation, before the paragraph on the three systems. Facts:
  before anybody asks you about the shop's numbers, you find out what the platform holds and what
  happens on it each night.
- **names**: one sentence after the paragraph on how to run a cell. Facts: in the cells, `storage`,
  `warehouse` and `reporting` are the shop's three systems: object storage, the warehouse and the
  reporting tool.
- **products**: a section heading (names the subject, at most five words), then one paragraph,
  then a one-sentence lead for the cell below it. Facts for the paragraph: `products.csv`, in
  object storage, holds the shop's catalogue: 8 products in 6 categories; for each product, an id
  (`product_id`), a name, a category, a list price in pence (`list_price_pence`) and the member of
  staff who last edited it (`updated_by`). Then the kept CSV sentence (item 6). Lead: the cell
  below prints `products.csv` exactly as it is stored.
- **customers**: a section heading, one paragraph, a one-sentence lead. Facts: `customers.jsonl`
  holds the shop's 10 customers, in 7 countries; each customer's record has five fields: an id
  (`customer_id`), a name, an email address (`email`), a country as a two-letter code, and the date
  the customer signed up (`signed_up`). Not every record has a value in every field: one
  customer's `email` is null. Say which fields a record has; do not say that every customer has
  each value, and do not mention the null. Then
  the kept JSON Lines sentences (item 6). Lead: the cell below prints `customers.jsonl` exactly as
  it is stored.
- **orders**: a section heading, one paragraph, a lead of one or two sentences. Facts:
  `orders.jsonl` holds every order the shop took, as the checkout sent it; each night the file is
  written again, with every order taken since the store opened. Each order's record has seven
  fields: its id (`order_id`), the customer (`customer_id`), the product (`product_id`), how many
  items (`quantity`), the price of one item in pence (`price_pence`), a status (`status`: in this
  week's file, `completed` or `cancelled`) and when it was placed (`ordered_at`, in UTC). Not every
  record has a value in every field: some orders' `customer_id` is null. Say which fields a record
  has; do not say that every order has each value, and do not mention the nulls. Lead: the cell
  below shows one day's orders as a table; the day is set to Monday, `2026-09-07`; you can change
  it to any day from `2026-09-07` to `2026-09-13` and run the cell again.
- **warehouse**: a section heading, one short paragraph, and three one-sentence leads, one before
  each of three cells. Facts: the warehouse holds three tables: `clean_customers`, `clean_orders`
  and `daily_sales`; you read a table by writing SQL in `warehouse.sql`; `daily_sales` has one row
  per day: the day and that day's revenue in pence (`revenue_pence`). Leads: (a) the cell below
  reads every row of `clean_customers`; (b) the cell below reads the first 7 rows of
  `clean_orders`, and you can change `LIMIT 7` to read more; (c) the cell below reads every row of
  `daily_sales`. Do not compare the tables with the files.
- **dashboard**: a section heading and a one-sentence lead before the dashboard's figure. Facts:
  the reporting tool holds one dashboard, `sales_dashboard`, titled "Sales, last 7 days"; it shows
  each day's revenue, in pounds, for 7 to 13 September. (The figure's caption, kept: "Monday
  morning's dashboard: revenue per day, 7 to 13 September.")
- **message**: one short paragraph after the dashboard, the last of part 1. Facts: before you have
  finished looking round the platform, the head of the shop sends you one line: Thursday's revenue
  looks wrong. Part 2 starts from that line. Include a Markdown link to part 2, written as
  `[link text](part-2.html)`.

## Slots for part 2

Part 2 is the chapter's essay as it stands, from its list of questions the platform cannot answer
to the handover. Its later sections are headed "Questions the platform cannot answer", "Thursday",
"What the platform holds", "What the fields are for", "Reconstruction", "A rule the week never
tests", "Records made at the time", "The handover" and "Before Chapter 2".

- **title_2**: the page's main heading. Facts: Chapter 1, "The invisible data system", part 2,
  about Thursday's revenue and what the platform cannot say about how its tables came to hold
  their rows. The heading names the chapter, the part and the part's subject. At most twelve
  words.
- **app_title_2**: the browser tab's title, at most six words.
- **opening_2**: a section heading (not "Thursday", which a later section uses), then one paragraph.
  After it come a figure of the three systems and their seven assets, and the dashboard. Facts: it
  is Monday 14 September 2026, your first morning as the shop's data engineer; you have looked
  round the shop's platform in part 1 (include a Markdown link to it, written as
  `[link text](./)`); the head of the shop has sent you one line: Thursday's revenue looks wrong.
  At most three sentences.

## Corrections after the first draft

The first version of this brief said that every customer has an email address and every order
names its customer. Both are false of the shop's files (one customer's `email` is null; Thursday's
three orders have no `customer_id`), and the draft copied them. The slots above now give the
fields a record has. It also asked for titles of at most eight words, and the draft's titles named
the chapter and the part but not the part's subject; the titles now ask for all three.
