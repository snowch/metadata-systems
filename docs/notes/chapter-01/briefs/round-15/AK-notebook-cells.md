# Brief AK: the notebook prototype's new words

Chapter 1 is being prototyped as a notebook: the same essay, with code cells the reader runs. These
are the only new or changed words. Every fact below was read off the shop's engine on 10 October
2026 and is pinned by its tests. Write each slot as plain sentences, following `docs/style.md` and
the writing standard in `AGENTS.md`. Write only the slots below, each under its key. Do not add
facts. Do not mention a lab, an engine, a simulator or marimo. The reader is "you", a data
engineer. British English. No em dashes.

## Who reads this

A data engineer on their first Monday at an online shop that sells bicycle parts. The page is a
notebook: prose, figures, and cells of Python they can run, change and run again. In the code,
`storage`, `warehouse` and `reporting` are the shop's three systems.

## Slots for the cells (each one or two sentences, said before the cell)

- **lead_tabs**: before four tabs, one per asset: `orders.jsonl`, `clean_orders`, `daily_sales`,
  `sales_dashboard`. Facts: these are the four assets the chapter uses; choose a tab to see what
  the asset holds; for the file, its first lines exactly as stored; for a table, its rows; for the
  dashboard, its chart.
- **lead_thursday_raw**: before a cell that reads every order in `orders.jsonl` and adds up
  `price_pence` times `quantity` for one day. Facts: the day is set to Thursday, `2026-09-10`; you
  can change the day and run the cell again.
- **lead_thursday_row**: before a cell that reads the same day's row from `daily_sales`.
- **lead_every_day**: before a cell that puts, for every day, the total of the raw orders in the
  file beside the row in `daily_sales`, and says whether they are the same.
- **lead_storage**: before a cell that lists the files in the bucket `shop-raw`. Facts: object
  storage records each file's key, its size in bytes and when it was last modified.
- **lead_catalogue**: before a cell that reads the warehouse's record of `daily_sales` from its
  catalogue. Facts: the warehouse keeps a catalogue you query with SQL;
  `information_schema.tables` has one row per table; `information_schema.columns` has one row per
  column, with its type.
- **lead_dashboard_record**: before a cell that shows what the reporting tool records about the
  dashboard.
- **lead_owners**: before a cell that lists every table's owner from the catalogue.
- **lead_rebuild**: before a cell that runs the query over `clean_orders` (completed orders, price
  times quantity in pence, per day) and compares its rows with the rows of `daily_sales`. Facts:
  `True` means every row is the same.
- **lead_changes**: before a menu of three changes to the shop. Facts: choose a change, and the
  cells below it show the platform on Monday morning after a week run with that change: what
  object storage holds, the warehouse's record of `daily_sales`, the dashboard, and which queries
  over the other assets give every row `daily_sales` has; the cells above the menu keep showing the
  week as it ran.
- **change_menu_label**: the menu's label, a few words.
- **change_options**: four short labels, one per option: no change; the analyst's copy
  (`clean_orders` copied every night to a CSV file in the bucket `shop-scratch`); the edited
  program (the program that writes `daily_sales`, from Saturday's row on, keeps every order not
  refunded); the failed night (the program that writes `daily_sales` fails on the last night).
  Each label at most six words.
- **lead_changed_storage**, **lead_changed_record**, **lead_changed_dashboard**,
  **lead_changed_queries**: four short headings, one before each cell below the menu. Facts: the
  last shows the queries over the other assets that give every row of `daily_sales`, with the SQL
  each runs.
- **lead_quantity**: before a cell that counts the orders in the week's file with a quantity of 0
  or less.
- **lead_rules**: before a cell that lists the settings of the four cleaning rules that turn the
  raw orders into `clean_orders` exactly. Facts: each row is one setting; the four rules are about
  orders written twice, orders with no customer id, cancelled orders, and orders with a quantity of
  0 or less.
- **handover_label**: the label of a box where you write your handover note for `daily_sales`,
  a few words.
- **handover_placeholder**: the greyed hint inside the box. Facts: what the table means and who to
  ask; what runs each night, reading what and writing what; what to do when a night fails.
- **lead_handover_record**: before a cell that shows, beside your note, everything the warehouse
  records about `daily_sales`.
- **first_lines**: a caption under a file's first lines, with slots `{shown}` and `{total}`:
  it shows the first `{shown}` of the file's `{total}` lines.

## Sentences of the essay to redraft (keep every other word as it is)

The essay is unchanged except where the files and money changed. Money is now whole pence in the
files and tables, and pounds on the dashboard. The raw files are now JSON Lines and CSV.

- **prediction_p1**, from: "Start with the arithmetic. `orders.parquet` holds every order the shop
  took, as the checkout sent it. Thursday's orders add up to 205.50. `daily_sales` holds one row
  per day, and its Thursday row says 51.50; the dashboard shows the same. Somewhere between the
  file and the table, 154.00 went missing." Facts now: the file is `orders.jsonl`; Thursday's
  orders add up to 20550 pence; `daily_sales` holds one row per day, in pence, and its Thursday
  row says 5150; the dashboard shows £51.50; 15400 pence, £154.00, went missing between the file
  and the table.
- **investigation_formats**, replacing: "A Parquet file also carries its own column names and
  types, written inside the file." Facts now: `orders.jsonl` and `customers.jsonl` are JSON Lines,
  one record per line, and every record names its fields; JSON gives a value one of a few types: a
  string, a number, true or false, or null; a date or an amount is just a string or a number.
  `products.csv` names its columns once, in its first line, and has no types: every value is text.
  Two or three sentences.
- **failure_thursday_worth**, from: "and they are worth 154.00." Facts: worth 15400 pence, £154.00.
- **failure_copy**, from: "An analyst copies `clean_orders` to a scratch bucket every night."
  Facts: to a CSV file, `clean_orders_copy.csv`, in the bucket `shop-scratch`, every night.
- **failure_saturday**, from: "Saturday's row becomes 215.49 instead of 191.49." Facts: Saturday's
  row in `daily_sales` becomes 21549 instead of 19149, in pence; the dashboard shows £215.49
  instead of £191.49.
- **note_sizes**, replacing: "The lab's sizes are estimates from the rows." Facts: a file's size
  is its real size in bytes; a table's size is an estimate from its rows.
