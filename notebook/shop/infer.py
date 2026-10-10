# Copyright © 2026 Christopher Snow

"""What the data suggests: inference from contents alone.

Chapter 1's reconstructions are searches the engine can run exhaustively. One is a sum over one
asset: which rows to keep, what to add up, and per what. The other is a set of cleaning rules over
the raw orders. Each choice is written as SQL and run over Monday's platform, so the engine can
list every choice that reproduces an asset, and show that two sources fit equally well, or none.
"""

from __future__ import annotations

import itertools
import sqlite3
from collections import Counter

from .data import ORDER_FIELDS
from .platform import Rows, stage
from .week import Week

KEEP = ("all", "completed", "cancelled")
MEASURE = {
    "revenue": "SUM(price_pence * quantity)",
    "quantity": "SUM(quantity)",
    "rows": "COUNT(*)",
}
PER = {"day": "date(ordered_at)", "customer": "customer_id", "product": "product_id"}


def sum_sql(source: str, keep: str, measure: str, per: str) -> str:
    """The query a sum choice means, over a table called `source`."""
    where = "" if keep == "all" else f"\nWHERE status = '{keep}'"
    key = PER[per]
    return f"SELECT {key} AS key, {MEASURE[measure]} AS value\nFROM {source}{where}\nGROUP BY {key}\nORDER BY key"


def _sources(week: Week, target: str) -> list[str]:
    """The assets a sum could be over: every warehouse table and every file, except the target."""
    tables = [r["table_name"] for r in week.warehouse.sql("SELECT table_name FROM information_schema.tables")]
    files = [r["key"] for r in week.storage.ls()]
    return [s for s in tables + files if s != target]


def _scratch(week: Week) -> sqlite3.Connection:
    """A connection that sees the warehouse's tables, for queries that also stage files."""
    return week.warehouse.db


def _rows(week: Week, source: str, sql: str) -> list[tuple] | None:
    """Runs a sum over a table, or over a file staged as a temporary table; None if it cannot run."""
    db = _scratch(week)
    try:
        if source.startswith("s3://"):
            records = week.storage.records(source)
            fields = tuple(records[0]) if records else ()
            stage(db, "staged", records, fields)
            sql = sql.replace(f"FROM {source}", "FROM temp.staged")
        return [tuple(r) for r in db.execute(sql).fetchall()]
    except sqlite3.Error:
        return None
    finally:
        db.execute("DROP TABLE IF EXISTS temp.staged")


def _target(week: Week, target: str) -> list[tuple]:
    return [tuple(r) for r in week.warehouse.db.execute(f"SELECT * FROM main.{target}").fetchall()]


def fits(result: list[tuple] | None, target: list[tuple], fit: str = "exact") -> bool:
    """Whether a result has the target's rows: `exact`, the same rows; `covers`, at least them."""
    if not result or not target:
        return False
    got = {k: v for k, v in result}
    want = {k: v for k, v in target}
    if any(got.get(k) != v for k, v in want.items()):
        return False
    return fit == "covers" or set(got) == set(want)


def queries_that_rebuild(week: Week, target: str = "daily_sales", fit: str = "exact") -> list[dict]:
    """Every sum over another asset that reproduces the target table, with the SQL it runs."""
    goal = _target(week, target)
    out = Rows()
    for source in _sources(week, target):
        for keep, measure, per in itertools.product(KEEP, MEASURE, PER):
            sql = sum_sql(source, keep, measure, per)
            if fits(_rows(week, source, sql), goal, fit):
                out.append({"source": source, "keep": keep, "measure": measure, "per": per, "sql": sql})
    return out


CLEAN_SPACE = [
    {"duplicates": d, "missing_customer": m, "cancelled": c, "quantity": q}
    for d in ("keep", "one")
    for m in ("keep", "drop")
    for c in ("keep", "drop")
    for q in ("keep", "drop")
]


def clean_sql(rules: dict) -> str:
    """The query a setting of the cleaning rules means, over the raw orders."""
    conditions = []
    if rules["missing_customer"] == "drop":
        conditions.append("customer_id IS NOT NULL")
    if rules["cancelled"] == "drop":
        conditions.append("status <> 'cancelled'")
    if rules["quantity"] == "drop":
        conditions.append("quantity > 0")
    where = f"\nWHERE {' AND '.join(conditions)}" if conditions else ""
    distinct = "DISTINCT " if rules["duplicates"] == "one" else ""
    return f"SELECT {distinct}{', '.join(ORDER_FIELDS)}\nFROM raw_orders{where}"


def cleaning_rules_that_fit(week: Week) -> list[dict]:
    """Every setting of the cleaning rules that turns the raw orders into `clean_orders` exactly."""
    from .week import FILES

    db = _scratch(week)
    stage(db, "raw_orders", week.storage.records(FILES["orders"]), ORDER_FIELDS)
    try:
        goal = Counter(_target(week, "clean_orders"))
        return Rows(r for r in CLEAN_SPACE if Counter(db.execute(clean_sql(r)).fetchall()) == goal)
    finally:
        db.execute("DROP TABLE IF EXISTS temp.raw_orders")


def day_gap(week: Week, day: str) -> dict:
    """A day's raw orders against the rows `clean_orders` keeps: how many, and what the rest are worth."""
    from .week import FILES

    raw = [o for o in week.storage.records(FILES["orders"]) if o["ordered_at"].startswith(day)]
    kept_ids = {
        r["order_id"] for r in week.warehouse.sql("SELECT order_id FROM clean_orders WHERE date(ordered_at) = :d", d=day)
    }
    left = [o for o in raw if o["order_id"] not in kept_ids]
    return {
        "orders": len(raw),
        "kept": len(raw) - len(left),
        "left": len(left),
        "left_ids": [o["order_id"] for o in left],
        "left_pence": sum(o["price_pence"] * o["quantity"] for o in left),
    }
