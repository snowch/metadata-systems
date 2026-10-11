## lead_tabs

These are the four assets this chapter uses, one per tab. Choose a tab to see what each one holds: for `orders.jsonl`, its first lines exactly as stored; for `clean_orders` and `daily_sales`, their rows; for `sales_dashboard`, its chart.

## lead_thursday_raw

The cell below reads every order in `orders.jsonl` and adds up `price_pence` times `quantity` for one day. The day is set to Thursday, `2026-09-10`, and you can change it and run the cell again.

## lead_thursday_row

The cell below reads Thursday's row, `2026-09-10`, from `daily_sales`.

## lead_every_day

The cell below puts, for every day, the total of the raw orders in `orders.jsonl` beside that day's row in `daily_sales`. It shows whether the two are the same.

## lead_storage

The cell below lists the files in the bucket `shop-raw`. For each file, object storage records its key, its size in bytes and when it was last modified.

## lead_catalogue

The cell below reads the warehouse's record of `daily_sales` from its catalogue, which you query with SQL. `information_schema.tables` has one row per table, and `information_schema.columns` has one row per column, with the column's type.

## lead_dashboard_record

The cell below shows what the reporting tool records about `sales_dashboard`.

## lead_owners

The cell below lists the owner of every table in the catalogue.

## lead_rebuild

The cell below runs a query over `clean_orders` that adds up price times quantity, in pence, for each day, counting only completed orders. It compares the query's rows with the rows of `daily_sales`; `True` means every row is the same.

## lead_changes

The cells below show the platform on Monday morning, after the week ran with the option you choose. The cells above the menu keep showing the week as it ran.

## change_menu_label

Choose a change to the shop

## change_options

- The shop stays as it is
- An analyst copies `clean_orders` every night
- Edited program keeps every unrefunded order
- Program fails on the last night

## lead_changed_storage

What object storage holds

## lead_changed_record

The warehouse's record of `daily_sales`

## lead_changed_dashboard

The dashboard

## lead_changed_queries

Queries that give every row of `daily_sales`

## lead_quantity

The cell below counts the orders in `orders.jsonl` with a quantity of 0 or less.

## lead_rules

The cell below lists the settings of the four cleaning rules that turn the raw orders into `clean_orders` exactly, with one setting on each row. The rules cover orders written twice, orders with no customer id, cancelled orders, and orders with a quantity of 0 or less.

## handover_label

Your handover note for `daily_sales`

## handover_placeholder

Write what `daily_sales` means and who to ask about it. Include what runs each night, what it reads and what it writes, and what to do when a night fails.

## lead_handover_record

The cell below shows your note beside everything the warehouse records about `daily_sales`.

## first_lines

The first `{shown}` of the file's `{total}` lines.

## prediction_p1

Start with the arithmetic. `orders.jsonl` holds every order the shop took, as the checkout sent it. Thursday's orders add up to 20550 pence. `daily_sales` holds one row per day, with amounts in pence, and its Thursday row says 5150; the dashboard shows £51.50. Somewhere between the file and the table, 15400 pence, £154.00, went missing.

## investigation_formats

`orders.jsonl` and `customers.jsonl` are JSON Lines, with one record per line, and every record names its fields. A JSON value has one of a few types, such as a string, a number, true or false, or null, and a date or an amount is just a string or a number. `products.csv` names its columns once, in its first line, and has no types: every value is text.

## failure_thursday_worth

and they are worth 15400 pence, £154.00.

## failure_copy

An analyst copies `clean_orders` to a CSV file, `clean_orders_copy.csv`, in the bucket `shop-scratch`, every night.

## failure_saturday

Saturday's row in `daily_sales` becomes 21549 instead of 19149, in pence. The dashboard shows £215.49 instead of £191.49.

## note_sizes

A file's size is its real size in bytes. A table's size is an estimate from its rows.

# Round 2

## lead_thursday_row

The cell below reads the row for the same day from `daily_sales`. That is the day set in the cell above, which you may have changed.

## change_menu_label

Choose a change to the shop

## change_options

- The shop stays as it is
- An analyst copies clean_orders every night
- From Saturday, daily_sales program keeps every unrefunded order
- The daily_sales program fails on the last night

## handover_placeholder

Write what daily_sales means and who to ask about it. Include what runs each night, what it reads and what it writes, and what to do when a night fails.

## lead_handover_record

You write your handover note in the box above. The cell below shows only what the warehouse records about `daily_sales`, so you can compare it with your note.

## first_lines

The first {shown} of the file's {total} lines.

## first_rows

The first {shown} of the table's {total} rows.
