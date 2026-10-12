# Copyright © 2026 Christopher Snow

"""What a change affects, asked of the lineage the shop has (Chapter 16).

`downstream` walks the graph Chapter 9's ingestion builds from the week's events: from an asset to
each program the events say read it, and on to what that program wrote. `downstream_columns` walks
Chapter 10's column lineage forward, through every program whose code the shop has, from one column
to every column computed from it or decided by it. Neither knows a reader that sends no events and
whose code the shop does not have.

`readers` runs Monday morning's readers in two weeks and sets what each got side by side: the rows of
`daily_sales`, the dashboard's values, the first line of the analyst's copy and the result of Jo
Marsh's query, or the error it raised. `made_from` lists what the shop made from one return, by the
runs that read it, and whether each is still there.

Every rule here is the shop's own choice.
"""

from __future__ import annotations

import sqlite3

from .columns import deps, programs
from .data import DAYS
from .ingest import edges, event_lines, normalise, objects, parse
from .platform import Rows
from .provenance import returns_as_of
from .runs import executions
from .schemas import JO_QUERY
from .week import COPY, NIGHTS, RETURNS_BUCKET, Week


def _short(name: str) -> str:
    """A dataset's name as the page writes it: a file by its address, a table by its own name."""
    if name.startswith("warehouse://"):
        return name.rsplit(".", 1)[1]
    if name.startswith("reporting://"):
        return name.rsplit("/", 1)[1]
    return name


def downstream(week: Week, start: str) -> Rows:
    """Every program and dataset downstream of `start` in the graph the week's events make, with how
    many steps away each is."""
    found = edges(objects(normalise(parse(event_lines(week)))))
    reads: dict[str, list[str]] = {}
    writes: dict[str, list[str]] = {}
    for r in found.by_job:
        (reads if r["edge"] == "reads" else writes).setdefault(r["dataset"] if r["edge"] == "reads" else r["job"], []).append(
            r["job"] if r["edge"] == "reads" else r["dataset"]
        )
    starts = [d for d in {r["dataset"] for r in found.by_job} if _short(d) == start or d == start]
    out, seen, frontier, step = [], set(starts), list(starts), 0
    while frontier:
        step += 1
        nxt = []
        for d in frontier:
            for job in reads.get(d, []):
                for made in writes.get(job, []):
                    if (job, made) in seen:
                        continue
                    seen.add((job, made))
                    out.append({"step": step, "program": job.split("/", 1)[1], "writes": _short(made)})
                    if made not in seen:
                        seen.add(made)
                        nxt.append(made)
        frontier = nxt
    return Rows(out, empty="No program read it, by the events.")


def downstream_columns(week: Week, dataset: str, column: str) -> Rows:
    """Every column downstream of one column, through every program whose code the shop has, read
    with the warehouse's catalogue: what each is, and whether its value is computed from the column
    or the column decides its rows."""
    readers = []
    for p in programs(week):
        target, found = deps(p["code"], week.warehouse)
        readers.append((p["job"], target, found))
    out, seen = [], set()
    frontier = [(dataset, column)]
    while frontier:
        nxt = []
        for ds, col in frontier:
            for job, target, found in readers:
                for d in found:
                    if d.dataset != ds or d.column != col:
                        continue
                    key = (target, d.output, d.kind)
                    if key in seen:
                        continue
                    seen.add(key)
                    out.append({"column": f"{_short(target)}.{d.output}", "from": f"{_short(ds)}.{col}", "kind": d.kind, "how": f"{d.how} in {job}"})
                    nxt.append((target, d.output))
        frontier = nxt
    return Rows(out, empty="No program whose code the shop has reads this column.")


def _jo(week: Week) -> str:
    try:
        rows = week.warehouse.sql(JO_QUERY)
    except sqlite3.Error as e:
        return f"error: {e}"
    return f"{len(rows)} rows, {sum(r['orders'] for r in rows)} orders"


def _got(week: Week) -> dict[str, str]:
    w = week.warehouse
    daily = w.sql("SELECT * FROM daily_sales ORDER BY day")
    got = {
        "daily_sales": f"{len(daily)} rows, {sum(r['revenue_pence'] for r in daily)} pence",
        "sales_dashboard": ", ".join(v["revenue"] for v in week.reporting.dashboard()["values"]),
    }
    if "copy" in week.changes:
        got["clean_orders_copy.csv"] = week.storage.read_text(COPY).splitlines()[0]
    got["Jo Marsh's query"] = _jo(week)
    return got


def readers(before: Week, after: Week) -> Rows:
    """What each reader got on Monday morning in two weeks, and whether it changed."""
    a, b = _got(before), _got(after)
    return Rows({"reader": k, "before": a[k], "after": b[k], "changed": "yes" if a[k] != b[k] else "no"} for k in a)


def made_from(week: Week, return_id: str) -> Rows:
    """What the shop made from one return: its row in `returns`, and each row of `daily_sales` whose
    run counted it, by what `returns` held when the run started; and whether each is still so."""
    uri = f"{RETURNS_BUCKET}/{return_id}.json"
    w = week.warehouse
    out = []
    for run, e in executions(week):
        if e.job == "record_return" and e.object == uri:
            [here] = w.sql("SELECT COUNT(*) AS n FROM returns WHERE return_id = :r", r=return_id)
            out.append({"made": f"returns, the row for {return_id}", "by": f"{run}, {e.job}", "still there": "yes" if here["n"] else "no"})
    for run, e in executions(week):
        if e.job != "build_daily_sales" or "returned_quantity" not in (e.code or ""):
            continue
        day = DAYS[NIGHTS.index(e.night)]
        held = {r["return_id"]: r for r in returns_as_of(week, e.started)}
        if return_id not in held:
            continue
        r = held[return_id]
        [hit] = w.sql("SELECT COUNT(*) AS n FROM clean_orders WHERE order_id = :o AND date(ordered_at) = :d", o=r["order_id"], d=day)
        if hit["n"]:
            out.append({"made": f"daily_sales, the row for {day}", "by": f"{run}, {e.job}", "still there": "yes"})
            shown = any(v["day"] == day for v in week.reporting.dashboard()["values"])
            out.append({"made": f"sales_dashboard, the value for {day}", "by": "refresh_dashboard", "still there": "yes" if shown else "no"})
    return Rows(out, empty="Nothing the shop made counted it.")


__all__ = ["downstream", "downstream_columns", "made_from", "readers"]
