# Copyright © 2026 Christopher Snow

"""The shop's week, run night by night.

Each night, in the early hours of Tuesday 8 to Monday 14 September, the export writes the three raw
files, then four programs run in order, each logged in as `etl_service`: they clean the customers,
clean the orders, add up the day before into `daily_sales`, and refresh the dashboard. The result is
the platform as the learner finds it on Monday morning.

A change is applied before the week runs, so a changed week is as deterministic as the plain one:

- `copy`: an analyst copies `clean_orders` to a scratch bucket every night;
- `refunds`: the program that writes `daily_sales` is edited, from Saturday's row on, to keep every
  order that has not been refunded, where it kept completed orders (the shop has no refunds);
- `failed`: the program that writes `daily_sales` fails on the last night and writes nothing;
- `column` (Chapter 3): from Saturday's row on, the program that writes `daily_sales` also writes
  the number of completed orders, into a new column `order_count`; the rows before have none;
- `source` (Chapter 6): from Saturday's row on, the program that writes `daily_sales` reads the
  analyst's copy instead of `clean_orders`. It brings `copy` with it. The rows it writes are the
  same; only the code, which the shop's repository holds, says which it reads.
- `net` (Chapter 10): from Saturday's row on, the program that writes `daily_sales` takes away
  what was returned, through a function the shop's developer added to the warehouse,
  `returned_quantity(order_id, product_id)`, which reads the table `returns`. It brings `returns`
  with it. No order of Saturday or Sunday was returned, so the rows it writes are the same.
- `added`, `renamed` and `retyped` (Chapter 11): from the export that comes before Saturday's row,
  the checkout's supplier changes `orders.jsonl`: it adds a field `coupon_code`; or it renames
  `quantity` to `qty`; or it writes each customer id as text, `C101` where it wrote `101`.
- `dev` (Chapter 12): a development database, `shop_dev`, beside the production one, where a
  developer runs the program that writes `daily_sales` on Monday morning over a sample of Sunday's
  orders; and the supplier's test of a new export, which wrote `Orders.jsonl` into `shop-raw`.
- `view` (Chapter 12): a view, `sales_by_day`, that Jo Marsh made over `daily_sales`.
- `clock` (Chapter 13): the reporting tool's clock runs 40 minutes slow, so the time it records for
  each refresh is 40 minutes early.
- `returns` (Chapter 7 on): the returns desk keeps each return as an object in `shop-returns`, at
  any hour of the day. Each create, overwrite or delete starts a function at once: `record_return`
  writes the return's row into the table `returns`, `remove_return` removes it. Object storage
  keeps every version of each object.
- `twice` (Chapter 19): object storage delivers its notice of the desk's correction of `r-202` twice,
  so `record_return` starts twice for it.

The programs' SQL lives here, and the platform does not record it: storage holds what the programs
wrote, not what they did.
"""

from __future__ import annotations

import csv
import io
import json
from dataclasses import dataclass, field

from .data import (
    RETURN_FIELDS,
    RETURNS_DESK,
    CUSTOMER_FIELDS,
    CUSTOMERS,
    DAYS,
    DUPLICATED,
    ORDER_FIELDS,
    ORDERS,
    PRODUCT_FIELDS,
    PRODUCTS,
    day_of,
)
from .platform import ObjectStorage, Reporting, Rows, Warehouse, epoch, file_schema, iso, stage

CHANGES = (
    "copy", "refunds", "failed", "column", "source", "returns", "net", "added", "renamed", "retyped", "dev", "view", "clock",
    "corrected", "withdrawn", "customer", "twice",
)

# The nights of the week: the date each night's work starts on, Tuesday 8 to Monday 14.
NIGHTS = DAYS[1:] + ("2026-09-14",)

RAW = "s3://shop-raw"
SCRATCH = "s3://shop-scratch"
FILES = {
    "orders": f"{RAW}/orders.jsonl",
    "customers": f"{RAW}/customers.jsonl",
    "products": f"{RAW}/products.csv",
}
COPY = f"{SCRATCH}/clean_orders_copy.csv"
# The analyst's script's query (the `copy` change): every column of `clean_orders`.
ANALYST_SQL = "SELECT * FROM clean_orders"
RETURNS_BUCKET = "s3://shop-returns"
RETURNS_TABLE = (
    ("return_id", "TEXT"),
    ("order_id", "INTEGER"),
    ("product_id", "INTEGER"),
    ("quantity", "INTEGER"),
    ("returned_at", "TIMESTAMP"),
)
RETURNS_CREATED = "2026-09-07T09:00:00Z"

# The first night whose export the supplier's changes (`added`, `renamed`, `retyped`) reach: the
# export before Saturday's row.
EXPORT_CHANGED = "2026-09-13"
# The value the `added` change gives `coupon_code`, for the two orders that used one.
COUPONS = {7040: "WHEELS10", 7046: "WHEELS10"}
# The `clock` change: how slow the reporting tool's clock runs.
SLOW_CLOCK = 40 * 60
# The `dev` change: the development database, when the developer's run starts and how long it takes,
# the day of the sample it reads, and the supplier's test export.
DEV_DATABASE = "shop_dev"
DEV_RUN = "2026-09-14T10:20:00Z"
DEV_DURATION = 4
DEV_SAMPLE_DAY = "2026-09-13"
TEST_EXPORT = f"{RAW}/Orders.jsonl"
TEST_EXPORT_AT = "2026-09-11T15:12:00Z"
TEST_ORDERS = (
    (9001, 101, 1, 1, 650, "completed", "2026-09-11T15:00:00Z"),
    (9002, 102, 2, 1, 1200, "completed", "2026-09-11T15:01:00Z"),
)
# The `view` change: Jo Marsh's view over `daily_sales`, and when Jo made it.
VIEW = "sales_by_day"
VIEW_SQL = "SELECT day, revenue_pence FROM daily_sales"
VIEW_CREATED = "2026-09-04T11:02:00Z"
# Part IV's returns of Sunday's orders, in the form of RETURNS_DESK: made on Sunday evening, after
# Saturday's row and before Sunday's, and changed on Monday morning, after the night's work.
# `corrected`: the desk records two rolls of bar tape back from order 7044, and corrects it to one.
CORRECTED = (
    ("2026-09-13T18:10:00Z", "created", "r-205", (7044, 8, 2)),
    ("2026-09-14T08:40:00Z", "overwritten", "r-205", (7044, 8, 1)),
)
# `withdrawn`: the desk records the brake pads of order 7047 back, and withdraws the return.
WITHDRAWN = (
    ("2026-09-13T21:15:00Z", "created", "r-206", (7047, 2, 1)),
    ("2026-09-14T08:50:00Z", "deleted", "r-206", None),
)
# The `twice` change (Chapter 19): object storage delivers its notice of one change twice, so the
# function starts twice for it: the desk's correction of r-202, the second start this long after.
TWICE = ("2026-09-10T09:30:00Z", "r-202")
TWICE_GAP = 25
# The `customer` change: from Sunday's night on, `build_clean_orders` names the column `customer`.
RENAMED_ON = "2026-09-13"
# The error the warehouse gave the failed night's program (`failed`).
FAILED_ERROR = "database is locked"

# Each program's name in the shop's repository. The export and the analyst's copy are not there.
JOBS = {
    "clean_customers": "build_clean_customers",
    "clean_orders": "build_clean_orders",
    "daily_sales": "build_daily_sales",
    "dashboard_refresh": "refresh_dashboard",
    "record_return": "record_return",
    "remove_return": "remove_return",
}

# Each writer's start time, UTC, and how long it takes in seconds: fixed, so every time is the same.
STARTS = {
    "export": "01:00",
    "clean_customers": "02:00",
    "clean_orders": "02:05",
    "analyst_copy": "02:15",
    "daily_sales": "02:30",
    "dashboard_refresh": "03:00",
}
# A function starts this many seconds after the object change that starts it.
FUNCTION_DELAY = 2
DURATION = {
    "export": 41,
    "clean_customers": 38,
    "clean_orders": 52,
    "analyst_copy": 17,
    "daily_sales": 21,
    "dashboard_refresh": 9,
    "record_return": 3,
    "remove_return": 2,
}

CLEAN_CUSTOMERS = """SELECT customer_id, name, LOWER(email), country, signed_up
FROM raw_customers
WHERE email IS NOT NULL"""

CLEAN_ORDERS = """SELECT DISTINCT order_id, customer_id, product_id, quantity, price_pence, status, ordered_at
FROM raw_orders
WHERE customer_id IS NOT NULL AND quantity > 0"""

DAILY_SALES = """SELECT date(ordered_at), SUM(price_pence * quantity)
FROM clean_orders
WHERE status = 'completed' AND date(ordered_at) = :day
GROUP BY date(ordered_at)"""

# The edited program of the `refunds` change: every order that is not refunded.
DAILY_SALES_FOR_REFUNDS = """SELECT date(ordered_at), SUM(price_pence * quantity)
FROM clean_orders
WHERE status <> 'refunded' AND date(ordered_at) = :day
GROUP BY date(ordered_at)"""

# The edited program of the `column` change: the same revenue, and the number of orders it counts.
DAILY_SALES_WITH_COUNT = """SELECT date(ordered_at), SUM(price_pence * quantity), COUNT(*)
FROM clean_orders
WHERE status = 'completed' AND date(ordered_at) = :day
GROUP BY date(ordered_at)"""

# The edited program of the `net` change: each order's quantity less what was returned of it.
DAILY_SALES_NET = """WITH lines AS (
    SELECT date(ordered_at) AS day, price_pence * (quantity - returned_quantity(order_id, product_id)) AS line_pence, status
    FROM clean_orders
)
SELECT day, SUM(line_pence)
FROM lines
WHERE status = 'completed' AND day = :day
GROUP BY day"""

DASHBOARD = "SELECT day, revenue_pence FROM daily_sales ORDER BY day"


def returned_quantity(db) -> callable:
    """The warehouse function of the `net` change: how many of one product of an order came back."""

    def returned(order_id, product_id) -> int:
        [(n,)] = db.execute(
            "SELECT COALESCE(SUM(quantity), 0) FROM main.returns WHERE order_id = ? AND product_id = ?",
            (order_id, product_id),
        ).fetchall()
        return n

    return returned


def timestamp(day: str, time: str, plus_seconds: int = 0) -> str:
    """The ISO time of `time` (HH:MM, UTC) on `day`, plus some seconds."""
    return iso(epoch(f"{day}T{time}:00Z") + plus_seconds)


def jsonl(fields: tuple[str, ...], rows) -> str:
    return "".join(json.dumps(dict(zip(fields, row))) + "\n" for row in rows)


def to_csv(fields: tuple[str, ...], rows) -> str:
    out = io.StringIO()
    writer = csv.writer(out, lineterminator="\n")
    writer.writerow(fields)
    writer.writerows(rows)
    return out.getvalue()


def exported_orders(night: str) -> list[tuple]:
    """The raw orders as the export writes them on a night: every order placed before it."""
    rows = []
    for row in ORDERS:
        if day_of(row[6]) >= night:
            continue
        rows.append(row)
        if row[0] == DUPLICATED:
            rows.append(row)
    return rows


@dataclass
class Execution:
    """One time a writer did its work. Storage keeps none of these; Chapter 7 on records them.

    `night` is the night's date for the nightly work, and None for a function, which runs when an
    object changes. `job` is the program's name in the shop's repository, None for the export and
    the analyst's copy. `code` is the program's code as it was when it ran. A function's `object`,
    `version` and `change` say which object change started it.
    """

    writer: str
    night: str | None
    started: str
    finished: str
    status: str
    wrote: str | None = None
    rows: int | None = None
    job: str | None = None
    reads: tuple[str, ...] = ()
    rows_read: int | None = None
    code: str | None = None
    object: str | None = None
    version: str | None = None
    change: str | None = None
    schema: tuple[tuple[str, str], ...] | None = None
    bytes: int | None = None
    error: str | None = None
    environment: str = "production"
    quality: tuple[tuple[str, str, int], ...] = ()


@dataclass
class Week:
    """The platform as the learner finds it on Monday morning, after a week with these changes."""

    changes: tuple[str, ...]
    storage: ObjectStorage
    warehouse: Warehouse
    reporting: Reporting
    executions: list[Execution] = field(default_factory=list)


def run_week(changes=()) -> Week:
    """Runs the shop's week, night by night, with the given changes."""
    changes = tuple(changes)
    if "source" in changes and "copy" not in changes:
        changes = ("copy",) + changes
    if any(c in changes for c in ("corrected", "withdrawn")) and "net" not in changes:
        changes = changes + ("net",)
    if "net" in changes and "returns" not in changes:
        changes = changes + ("returns",)
    for c in changes:
        if c not in CHANGES:
            raise ValueError(f"no change called {c!r}; the changes are {', '.join(CHANGES)}")
    storage = ObjectStorage()
    week = Week(changes, storage, Warehouse(storage), Reporting(SLOW_CLOCK if "clock" in changes else 0))
    storage, warehouse, reporting = week.storage, week.warehouse, week.reporting
    db = warehouse.db

    if "returns" in changes:
        warehouse.create_table("returns", RETURNS_TABLE, RETURNS_CREATED)
    if "net" in changes:
        db.create_function("returned_quantity", 2, returned_quantity(db))
    if "view" in changes:
        warehouse.create_view(VIEW, VIEW_SQL, VIEW_CREATED)
    if "dev" in changes:
        warehouse.create_database(DEV_DATABASE, ("clean_orders", "daily_sales"))

    desk = sorted(
        RETURNS_DESK + (CORRECTED if "corrected" in changes else ()) + (WITHDRAWN if "withdrawn" in changes else ()),
        key=lambda d: d[0],
    )

    def returns_desk(on: str) -> None:
        """What the returns desk did on one day, and the function each change started."""
        for at, change, return_id, what in desk:
            if at[:10] != on:
                continue
            uri = f"{RETURNS_BUCKET}/{return_id}.json"
            if change == "deleted":
                version = storage.delete(uri, at)
            else:
                order_id, product_id, quantity = what
                first = next(a for a, c, r, _ in desk if r == return_id)
                text = json.dumps(dict(zip(RETURN_FIELDS, (return_id, order_id, product_id, quantity, first)))) + "\n"
                version = storage.put(uri, text, at)
            writer = "remove_return" if change == "deleted" else "record_return"
            notices = [FUNCTION_DELAY]
            if "twice" in changes and (at, return_id) == TWICE:
                notices.append(FUNCTION_DELAY + TWICE_GAP)
            for delay in notices:
                started = iso(epoch(at) + delay)
                finished = iso(epoch(started) + DURATION[writer])
                if writer == "remove_return":
                    statements = [("DELETE FROM main.returns WHERE return_id = :r", {"r": return_id})]
                    reads: tuple[str, ...] = ()
                else:
                    row = storage.records(uri)[0]
                    statements = [
                        ("DELETE FROM main.returns WHERE return_id = :return_id", row),
                        ("INSERT INTO main.returns VALUES (:return_id, :order_id, :product_id, :quantity, :returned_at)", row),
                    ]
                    reads = (uri,)
                changed = warehouse.change("returns", statements, finished)
                n = 1 if writer == "record_return" else changed
                week.executions.append(
                    Execution(
                        writer, None, started, finished, "succeeded", "returns", n, JOBS[writer], reads,
                        len(reads), job_code(writer, changes, on), uri, version, change,
                    )
                )

    for night in NIGHTS:
        day = DAYS[NIGHTS.index(night)]
        # The returns desk works during the day, before the night's work.
        if "returns" in changes:
            returns_desk(day)

        def done(writer: str, status: str = "succeeded", wrote=None, rows=None, after=0, reads=(), rows_read=None, error=None, quality=()) -> str:
            started = timestamp(night, STARTS[writer], after)
            finished = timestamp(night, STARTS[writer], after + DURATION[writer])
            job = JOBS.get(writer)
            code = job_code(writer, changes, day) if job else None
            schema, size = None, None
            if status == "succeeded" and wrote and wrote.startswith("s3://"):
                schema, size = file_schema(storage.records(wrote)), len(storage.read_text(wrote).encode())
            elif status == "succeeded" and wrote in warehouse.tables():
                schema, size = warehouse.table_schema(wrote), warehouse.bytes(wrote)
            week.executions.append(
                Execution(
                    writer, night, started, finished, status, wrote, rows, job, tuple(reads), rows_read, code,
                    schema=schema, bytes=size, error=error, quality=tuple(quality),
                )
            )
            return finished

        # The export: three files, two minutes apart.
        orders = exported_orders(night)
        fields = ORDER_FIELDS
        if night >= EXPORT_CHANGED:
            fields, orders = supplier_changes(changes, fields, orders)
        for k, (uri, text, n) in enumerate(
            (
                (FILES["orders"], jsonl(fields, orders), len(orders)),
                (FILES["customers"], jsonl(CUSTOMER_FIELDS, CUSTOMERS), len(CUSTOMERS)),
                (FILES["products"], to_csv(PRODUCT_FIELDS, PRODUCTS), len(PRODUCTS)),
            )
        ):
            at = timestamp(night, STARTS["export"], k * 120 + DURATION["export"])
            storage.put(uri, text, at)
            done("export", wrote=uri, rows=n, after=k * 120)

        # Each program reads the files it needs, as a reader of the file would.
        customers = storage.records(FILES["customers"])
        stage(db, "raw_customers", customers, CUSTOMER_FIELDS)
        n = warehouse.write("clean_customers", CLEAN_CUSTOMERS, timestamp(night, "02:00", 38))
        done("clean_customers", wrote="clean_customers", rows=n, reads=[FILES["customers"]], rows_read=len(customers))

        raw = storage.records(FILES["orders"])
        stage(db, "raw_orders", raw, ORDER_FIELDS)
        if "customer" in changes and night == RENAMED_ON:
            warehouse.rename_column("clean_orders", "customer_id", "customer")
        n = warehouse.write("clean_orders", clean_orders_sql(changes, night), timestamp(night, "02:05", 52))
        measured = measure(db, "orders.jsonl", "temp.raw_orders", "customer_id") + measure(
            db, "clean_orders", "main.clean_orders", "customer" if "customer" in changes and night >= RENAMED_ON else "customer_id"
        )
        done("clean_orders", wrote="clean_orders", rows=n, reads=[FILES["orders"]], rows_read=len(raw), quality=measured)

        if "copy" in changes:
            cursor = db.execute(ANALYST_SQL)
            rows = cursor.fetchall()
            storage.put(COPY, to_csv(tuple(d[0] for d in cursor.description), rows), timestamp(night, "02:15", 17))
            done("analyst_copy", wrote=COPY, rows=len(rows))

        if "failed" in changes and night == NIGHTS[-1]:
            # The night's program reads what it reads on any other night of the week.
            failed_read = COPY if "source" in changes and day >= "2026-09-12" else "clean_orders"
            done("daily_sales", status="failed", reads=[failed_read], error=FAILED_ERROR)
        else:
            sql = DAILY_SALES_FOR_REFUNDS if "refunds" in changes and day >= "2026-09-12" else DAILY_SALES
            if "column" in changes and day >= "2026-09-12":
                if day == "2026-09-12":
                    warehouse.add_column("daily_sales", "order_count", "INTEGER")
                sql = DAILY_SALES_WITH_COUNT
            if "net" in changes and day >= "2026-09-12":
                sql = DAILY_SALES_NET
            source, [(read,)] = "clean_orders", db.execute("SELECT COUNT(*) FROM clean_orders")
            if "source" in changes and day >= "2026-09-12":
                copied = storage.records(COPY)
                stage(db, "clean_orders_copy", copied, ORDER_FIELDS)
                sql = sql.replace("FROM clean_orders", "FROM temp.clean_orders_copy")
                source, read = COPY, len(copied)
            n = warehouse.write("daily_sales", sql, timestamp(night, "02:30", 21), append=True, day=day)
            db.execute("DROP TABLE IF EXISTS temp.clean_orders_copy")
            done("daily_sales", wrote="daily_sales", rows=n, reads=[source], rows_read=read)

        shown = db.execute(DASHBOARD).fetchall()
        reporting.refresh(shown, timestamp(night, "03:00", 9))
        done("dashboard_refresh", wrote="sales_dashboard", rows=len(shown), reads=["daily_sales"], rows_read=len(shown))

        db.execute("DROP TABLE temp.raw_customers")
        db.execute("DROP TABLE temp.raw_orders")
        if "dev" in changes and day == "2026-09-11":
            storage.put(TEST_EXPORT, jsonl(ORDER_FIELDS, TEST_ORDERS), TEST_EXPORT_AT)
    # Monday morning, after the last night's work and before you start.
    if "returns" in changes:
        returns_desk(NIGHTS[-1])
    if "dev" in changes:
        development_run(week)
    week.executions.sort(key=lambda e: e.started)
    return week


# What a run of `build_clean_orders` measures, as it runs, of the file it read and the table it wrote
# (Chapter 14). Each is a count of rows.
METRICS = ("rows", "no customer_id", "order_id twice", "quantity 0 or less")


def measure(db, name: str, table: str, customer: str) -> list[tuple[str, str, int]]:
    """The four counts for one dataset, by SQL over the rows as the program saw them. A column the
    file does not have reads as empty, as the program reads it."""
    have = {c for (_, c, *_ ) in db.execute(f"PRAGMA {table.split('.')[0]}.table_info({table.split('.')[1]})")}
    nulls = f"SUM({customer} IS NULL)" if customer in have else "COUNT(*)"
    quantity = "SUM(quantity <= 0)" if "quantity" in have else "0"
    [(rows, missing, twice, low)] = db.execute(
        f"SELECT COUNT(*), COALESCE({nulls}, 0), COUNT(*) - COUNT(DISTINCT order_id), COALESCE({quantity}, 0) FROM {table}"
    )
    return [(name, m, v) for m, v in zip(METRICS, (rows, missing, twice, low))]


def clean_orders_sql(changes, night: str) -> str:
    """The SQL of `build_clean_orders` on a night: with the `customer` change, from Sunday's night on,
    it names the customer's column `customer`."""
    if "customer" in changes and night >= RENAMED_ON:
        return CLEAN_ORDERS.replace("customer_id, product_id", "customer_id AS customer, product_id", 1)
    return CLEAN_ORDERS


def supplier_changes(changes, fields: tuple[str, ...], orders: list[tuple]) -> tuple[tuple[str, ...], list[tuple]]:
    """The orders file as the supplier's changed export writes it (`added`, `renamed`, `retyped`)."""
    if "added" in changes:
        fields = fields + ("coupon_code",)
        orders = [row + (COUPONS.get(row[0]),) for row in orders]
    if "renamed" in changes:
        fields = tuple("qty" if f == "quantity" else f for f in fields)
    if "retyped" in changes:
        k = fields.index("customer_id")
        orders = [row[:k] + ((None if row[k] is None else f"C{row[k]}"),) + row[k + 1 :] for row in orders]
    return fields, orders


def development_run(week: Week) -> None:
    """The `dev` change's run: on Monday morning a developer loads Sunday's orders into the development
    database and runs the program that writes `daily_sales` there, for Sunday."""
    db, warehouse = week.warehouse.db, week.warehouse
    sample = [r for r in ORDERS if r[6][:10] == DEV_SAMPLE_DAY]
    db.executemany(f"INSERT INTO {DEV_DATABASE}.clean_orders VALUES (?, ?, ?, ?, ?, ?, ?)", sample)
    finished = iso(epoch(DEV_RUN) + DEV_DURATION)
    sql = DAILY_SALES.replace("FROM clean_orders", f"FROM {DEV_DATABASE}.clean_orders")
    n = db.execute(f"INSERT INTO {DEV_DATABASE}.daily_sales {sql}", {"day": DEV_SAMPLE_DAY}).rowcount
    db.commit()
    week.executions.append(
        Execution(
            "daily_sales", None, DEV_RUN, finished, "succeeded", "daily_sales", n, JOBS["daily_sales"],
            ("clean_orders",), len(sample), job_code("daily_sales", (), DEV_SAMPLE_DAY), environment="development",
        )
    )


def timeline(week: Week) -> list[dict]:
    """When each night's work began and ended. It says nothing about what a night wrote."""
    out = []
    for night in NIGHTS:
        work = [e for e in week.executions if e.night == night]
        out.append(
            {
                "night": night,
                "after": DAYS[NIGHTS.index(night)],
                "started": min(e.started for e in work),
                "finished": max(e.finished for e in work),
            }
        )
    return out


def _job(reads: dict[str, str], writes: str, sql: str, verb: str = "write", extra: str = "") -> str:
    """A job's code as the shop's repository holds it: what it reads, and what it writes with which SQL."""
    lines = [f'{name} = read("{uri}")' for name, uri in reads.items()]
    lines.append(f'{verb}("{writes}", """\n{sql}\n"""{extra})')
    return "\n".join(lines) + "\n"


RECORD_RETURN = """returned = read(changed_object)
change("returns", \"\"\"
DELETE FROM returns WHERE return_id = :return_id;
INSERT INTO returns SELECT return_id, order_id, product_id, quantity, returned_at FROM returned
\"\"\")
"""

REMOVE_RETURN = """change("returns", \"\"\"
DELETE FROM returns WHERE return_id = :return_id
\"\"\", return_id=name_of(changed_object))
"""


def job_code(writer: str, changes, day: str) -> str:
    """A program's code as the repository held it on `day`: the changes take effect from Saturday."""
    if writer == "record_return":
        return RECORD_RETURN
    if writer == "remove_return":
        return REMOVE_RETURN
    if writer == "clean_customers":
        return _job({"raw_customers": FILES["customers"]}, "clean_customers", CLEAN_CUSTOMERS)
    if writer == "clean_orders":
        night = NIGHTS[DAYS.index(day)]
        return _job({"raw_orders": FILES["orders"]}, "clean_orders", clean_orders_sql(changes, night))
    if writer == "dashboard_refresh":
        return _job({}, "sales_dashboard", DASHBOARD, verb="refresh")
    if writer != "daily_sales":
        raise KeyError(writer)
    edited = day >= "2026-09-12"
    daily = DAILY_SALES_FOR_REFUNDS if "refunds" in changes and edited else DAILY_SALES
    if "column" in changes and edited:
        daily = DAILY_SALES_WITH_COUNT
    if "net" in changes and edited:
        daily = DAILY_SALES_NET
    reads: dict[str, str] = {}
    if "source" in changes and edited:
        daily = daily.replace("FROM clean_orders", "FROM clean_orders_copy")
        reads = {"clean_orders_copy": COPY}
    return _job(reads, "daily_sales", daily, extra=", append=True, day=yesterday")


def repository(week: "Week") -> Rows:
    """The jobs' code, as the shop's repository holds it on Monday morning: one row per job.

    The export is not here: its code belongs to the checkout's supplier. The analyst's copy is not
    here either: it is a script on the analyst's laptop. The code is the code as it is now, not as
    it was on each night. With the `returns` change, the two functions are here too.
    """
    last = DAYS[-1]
    rows = [
        {"job": JOBS[w], "file": f"jobs/{JOBS[w]}.py", "code": job_code(w, week.changes, last)}
        for w in ("clean_customers", "clean_orders", "daily_sales", "dashboard_refresh")
    ]
    if "returns" in week.changes:
        rows += [
            {"job": w, "file": f"functions/{w}.py", "code": job_code(w, week.changes, last)}
            for w in ("record_return", "remove_return")
        ]
    return Rows(rows)


def reads_and_writes(code: str) -> dict[str, list[str]]:
    """What a job's code reads and writes, from the code alone.

    A `read("...")` names a file; a name after FROM or JOIN that no `read` defines is a table in
    the warehouse; `write("...")` or `refresh("...")` names what the job writes.
    """
    import re

    files = dict(re.findall(r'^(\w+) = read\("([^"]+)"\)', code, re.M))
    tables = []
    for name in re.findall(r"\b(?:FROM|JOIN)\s+(\w+)", code):
        target = files.get(name, name)
        if target not in tables:
            tables.append(target)
    writes = re.findall(r'^(?:write|refresh)\("([^"]+)"', code, re.M)
    return {"reads": tables, "writes": writes}


__all__ = ["CHANGES", "NIGHTS", "FILES", "COPY", "JOBS", "RETURNS_BUCKET", "Week", "run_week", "timeline", "repository", "reads_and_writes", "job_code"]
