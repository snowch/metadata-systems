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
- `failed`: the program that writes `daily_sales` fails on the last night and writes nothing.

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
from .platform import ObjectStorage, Reporting, Warehouse, epoch, iso, stage

CHANGES = ("copy", "refunds", "failed")

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
            n = warehouse.write("daily_sales", sql, timestamp(night, "02:30", 21), append=True, day=day)
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


__all__ = ["CHANGES", "NIGHTS", "FILES", "COPY", "Week", "run_week", "timeline"]
