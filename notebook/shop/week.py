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

The programs' SQL lives here, and the platform does not record it: storage holds what the programs
wrote, not what they did.
"""

from __future__ import annotations

import csv
import io
import json
from dataclasses import dataclass, field

from .data import (
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
from .platform import ObjectStorage, Reporting, Rows, Warehouse, epoch, iso, stage

CHANGES = ("copy", "refunds", "failed", "column", "source")

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

# Each writer's start time, UTC, and how long it takes in seconds: fixed, so every time is the same.
STARTS = {
    "export": "01:00",
    "clean_customers": "02:00",
    "clean_orders": "02:05",
    "analyst_copy": "02:15",
    "daily_sales": "02:30",
    "dashboard_refresh": "03:00",
}
DURATION = {
    "export": 41,
    "clean_customers": 38,
    "clean_orders": 52,
    "analyst_copy": 17,
    "daily_sales": 21,
    "dashboard_refresh": 9,
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

DASHBOARD = "SELECT day, revenue_pence FROM daily_sales ORDER BY day"


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
    """One thing that happened in a night. Storage keeps none of these; later chapters record them."""

    writer: str
    night: str
    started: str
    finished: str
    status: str
    wrote: str | None = None
    rows: int | None = None


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
    for c in changes:
        if c not in CHANGES:
            raise ValueError(f"no change called {c!r}; the changes are {', '.join(CHANGES)}")
    storage = ObjectStorage()
    week = Week(changes, storage, Warehouse(storage), Reporting())
    storage, warehouse, reporting = week.storage, week.warehouse, week.reporting
    db = warehouse.db

    for night in NIGHTS:
        day = DAYS[NIGHTS.index(night)]

        def done(writer: str, status: str = "succeeded", wrote=None, rows=None, after=0) -> str:
            started = timestamp(night, STARTS[writer], after)
            finished = timestamp(night, STARTS[writer], after + DURATION[writer])
            week.executions.append(Execution(writer, night, started, finished, status, wrote, rows))
            return finished

        # The export: three files, two minutes apart.
        orders = exported_orders(night)
        for k, (uri, text, n) in enumerate(
            (
                (FILES["orders"], jsonl(ORDER_FIELDS, orders), len(orders)),
                (FILES["customers"], jsonl(CUSTOMER_FIELDS, CUSTOMERS), len(CUSTOMERS)),
                (FILES["products"], to_csv(PRODUCT_FIELDS, PRODUCTS), len(PRODUCTS)),
            )
        ):
            at = timestamp(night, STARTS["export"], k * 120 + DURATION["export"])
            storage.put(uri, text, at)
            done("export", wrote=uri, rows=n, after=k * 120)

        # Each program reads the files it needs, as a reader of the file would.
        stage(db, "raw_customers", storage.records(FILES["customers"]), CUSTOMER_FIELDS)
        n = warehouse.write("clean_customers", CLEAN_CUSTOMERS, timestamp(night, "02:00", 38))
        done("clean_customers", wrote="clean_customers", rows=n)

        stage(db, "raw_orders", storage.records(FILES["orders"]), ORDER_FIELDS)
        n = warehouse.write("clean_orders", CLEAN_ORDERS, timestamp(night, "02:05", 52))
        done("clean_orders", wrote="clean_orders", rows=n)

        if "copy" in changes:
            rows = db.execute(f"SELECT {', '.join(ORDER_FIELDS)} FROM clean_orders").fetchall()
            storage.put(COPY, to_csv(ORDER_FIELDS, rows), timestamp(night, "02:15", 17))
            done("analyst_copy", wrote=COPY, rows=len(rows))

        if "failed" in changes and night == NIGHTS[-1]:
            done("daily_sales", status="failed")
        else:
            sql = DAILY_SALES_FOR_REFUNDS if "refunds" in changes and day >= "2026-09-12" else DAILY_SALES
            if "column" in changes and day >= "2026-09-12":
                if day == "2026-09-12":
                    warehouse.add_column("daily_sales", "order_count", "INTEGER")
                sql = DAILY_SALES_WITH_COUNT
            if "source" in changes and day >= "2026-09-12":
                stage(db, "clean_orders_copy", storage.records(COPY), ORDER_FIELDS)
                sql = sql.replace("FROM clean_orders", "FROM temp.clean_orders_copy")
            n = warehouse.write("daily_sales", sql, timestamp(night, "02:30", 21), append=True, day=day)
            db.execute("DROP TABLE IF EXISTS temp.clean_orders_copy")
            done("daily_sales", wrote="daily_sales", rows=n)

        reporting.refresh(db.execute(DASHBOARD).fetchall(), timestamp(night, "03:00", 9))
        done("dashboard_refresh", wrote="sales_dashboard")

        db.execute("DROP TABLE temp.raw_customers")
        db.execute("DROP TABLE temp.raw_orders")
    return week


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


def repository(week: "Week") -> Rows:
    """The jobs' code, as the shop's repository holds it on Monday morning: one row per job.

    The export is not here: its code belongs to the checkout's supplier. The analyst's copy is not
    here either: it is a script on the analyst's laptop. The code is the code as it is now, not as
    it was on each night.
    """
    daily = DAILY_SALES_FOR_REFUNDS if "refunds" in week.changes else DAILY_SALES
    if "column" in week.changes:
        daily = DAILY_SALES_WITH_COUNT
    daily_reads: dict[str, str] = {}
    if "source" in week.changes:
        daily = daily.replace("FROM clean_orders", "FROM clean_orders_copy")
        daily_reads = {"clean_orders_copy": COPY}
    jobs = {
        "build_clean_customers": _job({"raw_customers": FILES["customers"]}, "clean_customers", CLEAN_CUSTOMERS),
        "build_clean_orders": _job({"raw_orders": FILES["orders"]}, "clean_orders", CLEAN_ORDERS),
        "build_daily_sales": _job(daily_reads, "daily_sales", daily, extra=", append=True, day=yesterday"),
        "refresh_dashboard": _job({}, "sales_dashboard", DASHBOARD, verb="refresh"),
    }
    return Rows({"job": name, "file": f"jobs/{name}.py", "code": code} for name, code in jobs.items())


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


__all__ = ["CHANGES", "NIGHTS", "FILES", "COPY", "Week", "run_week", "timeline", "repository", "reads_and_writes"]
