# Copyright © 2026 Christopher Snow

"""What each run recorded as it ran, and how recent each asset's data is (Chapter 13).

`observations` lists, for every run of a program in the repository, what was recorded while it ran:
when it started, how long it took, its status, the rows it read and wrote, the size of what it
wrote, and the error a failed run reported. `freshness` sets each asset's own record of its last
write (the time its store keeps, by the store's own clock) beside the latest day its data holds.
`readings` tests the dashboard against three readings of "fresh":

- refreshed lately: the reporting tool's record of the last refresh is within a day;
- built from the latest data: along the lineage that feeds the dashboard, each asset was last
  written after the asset it is made from, by the times each store records;
- showing the latest day: the latest day the dashboard shows is the day before.

Every rule here is the shop's own choice.
"""

from __future__ import annotations

from .data import ARRIVAL
from .platform import Rows, epoch, iso
from .runs import executions
from .week import FILES, RETURNS_BUCKET, Week

# The lineage that feeds the dashboard, as the jobs' code says (Chapter 6): each asset and the one it
# is made from.
CHAIN = (
    ("orders.jsonl", "clean_orders"),
    ("clean_orders", "daily_sales"),
    ("daily_sales", "sales_dashboard"),
)


def observations(week: Week) -> Rows:
    """Every run of a program in the repository, with what was recorded as it ran."""
    return Rows(
        (
            {
                "run": run,
                "program": e.job,
                "started": e.started,
                "seconds": int(epoch(e.finished) - epoch(e.started)),
                "status": e.status,
                "rows read": e.rows_read,
                "rows written": e.rows if e.status == "succeeded" else None,
                "bytes": e.bytes,
                "error": e.error,
            }
            for run, e in executions(week)
        ),
        null="",
    )


def last_written(week: Week, asset: str) -> str:
    """The time an asset's own store records for its last write, by that store's clock."""
    if asset == "sales_dashboard":
        return week.reporting.dashboard()["last_refreshed"]
    if asset.endswith(".jsonl"):
        [row] = [r for r in week.storage.ls() if r["key"] == FILES[asset.split(".")[0]]]
        return row["last_modified"]
    [row] = week.warehouse.sql("SELECT last_altered FROM information_schema.tables WHERE table_name = :t", t=asset)
    return row["last_altered"]


def latest_day(week: Week, asset: str) -> str | None:
    """The latest day an asset's data holds."""
    w = week.warehouse
    if asset == "sales_dashboard":
        shown = week.reporting.dashboard()["values"]
        return shown[-1]["day"] if shown else None
    if asset == "orders.jsonl":
        return max((r["ordered_at"][:10] for r in week.storage.records(FILES["orders"])), default=None)
    if asset == "clean_orders":
        [row] = w.sql("SELECT MAX(date(ordered_at)) AS d FROM clean_orders")
    elif asset == "daily_sales":
        [row] = w.sql("SELECT MAX(day) AS d FROM daily_sales")
    elif asset == "returns":
        [row] = w.sql("SELECT MAX(date(returned_at)) AS d FROM returns")
    else:
        raise KeyError(asset)
    return row["d"]


def freshness(week: Week, at: str = ARRIVAL) -> Rows:
    """Each asset: when its store says it was last written, how many hours before `at`, and the
    latest day its data holds."""
    assets = ["orders.jsonl", "clean_orders", "daily_sales", "sales_dashboard"]
    if "returns" in week.changes:
        assets.append("returns")
    out = []
    for a in assets:
        t = last_written(week, a)
        out.append({"asset": a, "last written": t, "hours before": round((epoch(at) - epoch(t)) / 3600, 1), "latest day": latest_day(week, a)})
    return Rows(out, null="")


def last_run(week: Week, asset: str) -> str:
    """When the last run that wrote an asset finished, by the clock the runs' events carry."""
    uri = FILES.get(asset.split(".")[0], asset) if asset.endswith(".jsonl") else asset
    return max(e.finished for e in week.executions if e.wrote == uri and e.status == "succeeded" and e.environment == "production")


def chain(week: Week, by: str = "stores") -> Rows:
    """Each step of the lineage that feeds the dashboard: was the asset written after its input?

    `by="stores"` takes each time from the asset's own store, each by its own clock; `by="runs"` takes
    every time from the runs' events, which carry one clock.
    """
    when = {"stores": last_written, "runs": last_run}[by]
    out = []
    for source, made in CHAIN:
        a, b = when(week, source), when(week, made)
        out.append({"made": made, "last written": b, "from": source, "which was last written": a, "written after it": "yes" if b >= a else "no"})
    return Rows(out)


def readings(week: Week, at: str = ARRIVAL, by: str = "stores") -> Rows:
    """The dashboard against three readings of "fresh"."""
    refreshed = last_written(week, "sales_dashboard")
    day_before = iso(epoch(at) - 86400)[:10]
    shown = latest_day(week, "sales_dashboard")
    in_order = all(r["written after it"] == "yes" for r in chain(week, by))
    return Rows(
        [
            {"reading": "refreshed lately", "test": f"last refreshed {refreshed}, within a day", "met": "yes" if epoch(at) - epoch(refreshed) <= 86400 else "no"},
            {"reading": "built from the latest data", "test": "each asset feeding it written after its input", "met": "yes" if in_order else "no"},
            {"reading": "showing the latest day", "test": f"latest day shown {shown}, the day before is {day_before}", "met": "yes" if shown == day_before else "no"},
        ]
    )


def source_changed(week: Week) -> str | None:
    """The last change to the returns bucket, by object storage's record of every version."""
    found = [v["at"] for v in week.storage.versions(RETURNS_BUCKET)]
    return max(found) if found else None


__all__ = ["CHAIN", "chain", "freshness", "last_run", "last_written", "latest_day", "observations", "readings", "source_changed"]
