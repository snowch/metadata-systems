# Copyright © 2026 Christopher Snow

"""A dataset's schema over the week, and what a change to it does downstream (Chapter 11).

Neither system keeps a dataset's past schemas. Object storage records nothing about a file's
fields, and the warehouse's catalogue holds each table's columns as they are now. The shop records
the schema each time a program writes a dataset: for a file, the fields a reader finds and the type
of their values; for a table, the columns and declared types the catalogue records just after the
write (`Execution.schema`). Consecutive writes with the same schema make one version.

`diff` compares two versions by name, as the shop's records allow: a column whose name is gone is
`removed`, and a new name is `added`. A rename is both: nothing in the records says the two are one
column. `readers` uses the column lineage of Chapter 10 to list the programs that read a column, and
`compare` runs the week with and without a change and sets what a reader gets side by side.
"""

from __future__ import annotations

from .columns import deps, programs
from .platform import Rows
from .week import FILES, Week, run_week

# Jo Marsh's own query, in a spreadsheet that reads the warehouse: orders by the customer's country.
# It is not in the shop's repository and sends no events.
JO_QUERY = """SELECT c.country, COUNT(*) AS orders
FROM clean_orders o JOIN clean_customers c ON o.customer_id = c.customer_id
GROUP BY c.country"""

MESSAGES = {
    "no_difference": "The two versions have the same columns, with the same types.",
    "no_readers": "No program whose code the shop has reads this column.",
}


def _dataset(name: str) -> str:
    """A dataset as a program's execution records it: a file by its address, a table by its name."""
    return FILES.get(name.split(".")[0], name) if name.endswith((".jsonl", ".csv")) else name


def versions(week: Week, dataset: str) -> Rows:
    """Each version of a dataset's schema in the week: when it was first and last written with it."""
    uri = _dataset(dataset)
    out: list[dict] = []
    for e in week.executions:
        if e.wrote != uri or e.schema is None or e.environment != "production":
            continue
        if out and out[-1]["_schema"] == e.schema:
            out[-1]["last written"] = e.finished
            out[-1]["writes"] += 1
            continue
        out.append({"version": len(out) + 1, "first written": e.finished, "last written": e.finished, "writes": 1, "_schema": e.schema})
    return Rows(
        {
            "version": v["version"],
            "columns": ", ".join(f"{c} {t}" for c, t in v["_schema"]),
            "first written": v["first written"],
            "last written": v["last written"],
            "writes": v["writes"],
        }
        for v in out
    )


def schema(week: Week, dataset: str, version: int) -> tuple[tuple[str, str], ...]:
    """The columns and types of one version of a dataset's schema."""
    uri = _dataset(dataset)
    found: list[tuple[tuple[str, str], ...]] = []
    for e in week.executions:
        if e.wrote == uri and e.schema is not None and e.environment == "production" and (not found or found[-1] != e.schema):
            found.append(e.schema)
    return found[version - 1]


def diff(week: Week, dataset: str, before: int = 1, after: int = 2) -> Rows:
    """What changed between two versions, column by column, matched by name."""
    old, new = dict(schema(week, dataset, before)), dict(schema(week, dataset, after))
    out = []
    for c, t in old.items():
        if c not in new:
            out.append({"column": c, "change": "removed", "before": t, "after": None})
        elif new[c] != t:
            out.append({"column": c, "change": "retyped", "before": t, "after": new[c]})
    for c, t in new.items():
        if c not in old:
            out.append({"column": c, "change": "added", "before": None, "after": t})
    return Rows(out, null="", empty=MESSAGES["no_difference"])


def readers(week: Week, dataset: str, column: str) -> Rows:
    """Every program whose code the shop has that reads a column, and how (Chapter 10's kinds)."""
    uri = _dataset(dataset)
    out = []
    for p in programs(week):
        target, found = deps(p["code"], week.warehouse)
        hows = sorted({f"{d.kind}: {d.how}" for d in found if d.dataset in (uri, dataset) and d.column == column})
        if hows:
            out.append({"column": column, "program": p["job"], "writes": target.rsplit("/", 1)[-1], "reads it for": "; ".join(hows)})
    return Rows(out, empty=MESSAGES["no_readers"])


def compare(change: str) -> Rows:
    """What three readers get on Monday, in the plain week and with one change to the export: the rows
    of `daily_sales`, the days the dashboard shows, and the rows of Jo Marsh's query."""
    plain, changed = run_week(), run_week([change])

    def reading(week: Week) -> tuple[int, int, int]:
        return (
            len(week.warehouse.sql("SELECT * FROM daily_sales")),
            len(week.reporting.dashboard()["values"]),
            len(week.warehouse.sql(JO_QUERY)),
        )

    a, b = reading(plain), reading(changed)
    names = ("rows of daily_sales", "days on the dashboard", "rows of Jo Marsh's query")
    return Rows({"reader": n, "plain week": x, f"with {change}": y} for n, x, y in zip(names, a, b))


SUPPLIER = ("added", "renamed", "retyped")


def diffs(changes=SUPPLIER) -> Rows:
    """The diff of `orders.jsonl` under each of the supplier's changes, and how many versions of the
    schema of `clean_orders` the catalogue's records give under it."""
    out = []
    for change in changes:
        week = run_week([change])
        tables = len(versions(week, "clean_orders"))
        for r in diff(week, "orders.jsonl"):
            out.append({"supplier's change": change, **r, "schema versions of clean_orders": tables})
    return Rows(out, null="")


def compare_all(changes=SUPPLIER) -> Rows:
    """What three readers get on Monday, in the plain week and with each of the supplier's changes."""
    tables = [compare(c) for c in changes]
    return Rows(
        {"reader": row["reader"], "plain week": row["plain week"], **{c: t[k][f"with {c}"] for c, t in zip(changes, tables)}}
        for k, row in enumerate(tables[0])
    )


__all__ = ["JO_QUERY", "SUPPLIER", "compare", "compare_all", "diff", "diffs", "readers", "schema", "versions"]
