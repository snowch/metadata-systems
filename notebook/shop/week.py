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
- `returns` (Chapter 7 on): the returns desk keeps each return as an object in `shop-returns`, at
  any hour of the day. Each create, overwrite or delete starts a function at once: `record_return`
  writes the return's row into the table `returns`, `remove_return` removes it. Object storage
  keeps every version of each object.

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
from .platform import ObjectStorage, Reporting, Rows, Warehouse, epoch, iso, stage

CHANGES = ("copy", "refunds", "failed", "column", "source", "returns")

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
RETURNS_BUCKET = "s3://shop-returns"
RETURNS_TABLE = (
    ("return_id", "TEXT"),
    ("order_id", "INTEGER"),
    ("product_id", "INTEGER"),
    ("quantity", "INTEGER"),
    ("returned_at", "TIMESTAMP"),
)
RETURNS_CREATED = "2026-09-07T09:00:00Z"

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

    if "returns" in changes:
        warehouse.create_table("returns", RETURNS_TABLE, RETURNS_CREATED)

    def returns_desk(on: str) -> None:
        """What the returns desk did on one day, and the function each change started."""
        for at, change, return_id, what in RETURNS_DESK:
            if at[:10] != on:
                continue
            uri = f"{RETURNS_BUCKET}/{return_id}.json"
            if change == "deleted":
                version = storage.delete(uri, at)
            else:
                order_id, product_id, quantity = what
                first = next(a for a, c, r, _ in RETURNS_DESK if r == return_id)
                text = json.dumps(dict(zip(RETURN_FIELDS, (return_id, order_id, product_id, quantity, first)))) + "\n"
                version = storage.put(uri, text, at)
            started = iso(epoch(at) + FUNCTION_DELAY)
            writer = "remove_return" if change == "deleted" else "record_return"
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

        def done(writer: str, status: str = "succeeded", wrote=None, rows=None, after=0, reads=(), rows_read=None) -> str:
            started = timestamp(night, STARTS[writer], after)
            finished = timestamp(night, STARTS[writer], after + DURATION[writer])
            job = JOBS.get(writer)
            code = job_code(writer, changes, day) if job else None
            week.executions.append(
                Execution(writer, night, started, finished, status, wrote, rows, job, tuple(reads), rows_read, code)
            )
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
        customers = storage.records(FILES["customers"])
        stage(db, "raw_customers", customers, CUSTOMER_FIELDS)
        n = warehouse.write("clean_customers", CLEAN_CUSTOMERS, timestamp(night, "02:00", 38))
        done("clean_customers", wrote="clean_customers", rows=n, reads=[FILES["customers"]], rows_read=len(customers))

        raw = storage.records(FILES["orders"])
        stage(db, "raw_orders", raw, ORDER_FIELDS)
        n = warehouse.write("clean_orders", CLEAN_ORDERS, timestamp(night, "02:05", 52))
        done("clean_orders", wrote="clean_orders", rows=n, reads=[FILES["orders"]], rows_read=len(raw))

        if "copy" in changes:
            rows = db.execute(f"SELECT {', '.join(ORDER_FIELDS)} FROM clean_orders").fetchall()
            storage.put(COPY, to_csv(ORDER_FIELDS, rows), timestamp(night, "02:15", 17))
            done("analyst_copy", wrote=COPY, rows=len(rows))

        if "failed" in changes and night == NIGHTS[-1]:
            done("daily_sales", status="failed", reads=["clean_orders"])
        else:
            sql = DAILY_SALES_FOR_REFUNDS if "refunds" in changes and day >= "2026-09-12" else DAILY_SALES
            if "column" in changes and day >= "2026-09-12":
                if day == "2026-09-12":
                    warehouse.add_column("daily_sales", "order_count", "INTEGER")
                sql = DAILY_SALES_WITH_COUNT
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
        if "returns" in changes:
            returns_desk(day)
    week.executions.sort(key=lambda e: e.started)
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
        return _job({"raw_orders": FILES["orders"]}, "clean_orders", CLEAN_ORDERS)
    if writer == "dashboard_refresh":
        return _job({}, "sales_dashboard", DASHBOARD, verb="refresh")
    if writer != "daily_sales":
        raise KeyError(writer)
    edited = day >= "2026-09-12"
    daily = DAILY_SALES_FOR_REFUNDS if "refunds" in changes and edited else DAILY_SALES
    if "column" in changes and edited:
        daily = DAILY_SALES_WITH_COUNT
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
