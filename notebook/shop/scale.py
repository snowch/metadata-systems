# Copyright © 2026 Christopher Snow

"""What the shop's metadata system costs as the platform grows (Chapter 23).

`measure` counts the week's own metadata: assets, runs, events, edges and the bytes of an event.
`project` scales those rates from the shop's size to ten million assets, each asset with the week's
events per asset per day, and counts the stored records each of four questions reads, with and
without the structure that serves it:

- the latest run of one job: every stored event, or with an index on job and time, a walk down the
  index (about log2 of the events) and one record;
- one day's events: every stored event, or with the events partitioned by day, one day's;
- what is downstream of one asset, followed to the end: every edge it reaches. The share of the
  graph the widest traversal reaches is measured in the week (`reach`) and kept as the graph grows;
  with a limit of `DEPTH` steps, at most `FANOUT` to the power `DEPTH` edges.

`first_over` gives, for each question, the first size at which the records read pass `BUDGET`.

`retain` deletes the events older than a number of days, and `compact` first folds each run's edges
into one edge per job with its first and last time, which retention keeps.

Every rate, limit and budget beyond the week's own counts is the shop's assumption, stated here.
"""

from __future__ import annotations

import json
import math

from .ingest import _utc, edges, normalise, objects, parse
from .platform import Rows, epoch
from .delivery import week_events
from .week import Week

SIZES = (10, 100, 1_000, 10_000, 100_000, 1_000_000, 10_000_000)
RETENTION_DAYS = 90
BUDGET = 1_000_000
FANOUT = 3
DEPTH = 4

QUESTIONS = (
    "latest run of one job",
    "one day's events",
    "downstream of one asset, to the end",
    "downstream of one asset, 4 steps",
)


def measure(week: Week) -> Rows:
    """The week's own metadata: how many of each thing, over how many days."""
    events = week_events(week)
    objs = objects(normalise(parse([json.dumps(e) for e in events])))
    found = edges(objs)
    days = len({_utc(e["eventTime"])[:10] for e in events})
    size = sum(len(json.dumps(e, separators=(",", ":"))) for e in events)
    return Rows([
        {
            "assets": len(objs.datasets),
            "jobs": len(objs.jobs),
            "runs": len(objs.runs),
            "events": len(events),
            "run edges": len(found.by_run),
            "job edges": len(found.by_job),
            "days": days,
            "bytes per event": round(size / len(events)),
        }
    ])


def reach(week: Week) -> Rows:
    """For each dataset, how many of the week's job edges a traversal downstream from it follows, to
    the end, and what share of all the job edges that is."""
    events = week_events(week)
    by_job = edges(objects(normalise(parse([json.dumps(e) for e in events])))).by_job
    readers: dict[str, list[dict]] = {}
    writes: dict[str, list[dict]] = {}
    for r in by_job:
        (readers if r["edge"] == "reads" else writes).setdefault(r["dataset"] if r["edge"] == "reads" else r["job"], []).append(r)
    out = []
    for start in sorted({r["dataset"] for r in by_job}):
        seen, frontier = set(), [start]
        while frontier:
            nxt = []
            for d in frontier:
                for e in readers.get(d, []):
                    for w in [e] + writes.get(e["job"], []):
                        k = (w["job"], w["edge"], w["dataset"])
                        if k not in seen:
                            seen.add(k)
                            if w["edge"] == "writes":
                                nxt.append(w["dataset"])
            frontier = nxt
        out.append({"dataset": start, "edges followed": len(seen), "share": round(len(seen) / len(by_job), 2)})
    return Rows(sorted(out, key=lambda r: -r["edges followed"]))


def project(week: Week, sizes=SIZES, retention_days: int = RETENTION_DAYS) -> Rows:
    """At each number of assets: the events a day and the events stored for `retention_days`, the
    edges, and the stored records each question reads without and with its structure."""
    m = measure(week)[0]
    widest = reach(week)[0]["share"]
    per_asset_day = m["events"] / m["days"] / m["assets"]
    edges_per_asset = m["job edges"] / m["assets"]
    out = []
    for n in sizes:
        per_day = round(n * per_asset_day)
        stored = per_day * retention_days
        graph = round(n * edges_per_asset)
        out.append({
            "assets": n,
            "events a day": per_day,
            "events stored": stored,
            "edges": graph,
            "latest run, scan": stored,
            "latest run, index": math.ceil(math.log2(max(stored, 2))) + 1,
            "one day, scan": stored,
            "one day, partitions": per_day,
            "downstream, to the end": max(1, round(graph * widest)),
            "downstream, 4 steps": min(max(1, round(graph * widest)), FANOUT ** DEPTH),
        })
    return Rows(out)


def first_over(week: Week, budget: int = BUDGET) -> Rows:
    """For each way of answering each question, the first number of assets at which it reads more
    than `budget` stored records; none, within ten million assets."""
    rows = project(week)
    ways = [k for k in rows[0] if k not in ("assets", "events a day", "events stored", "edges")]
    return Rows(
        {"question": w, "first over budget at": next((r["assets"] for r in rows if r[w] > budget), None)}
        for w in ways
    )


def retain(events: list[dict], days: int, now: str) -> list[dict]:
    """The events no older than `days` days at `now`."""
    return [e for e in events if epoch(now) - epoch(_utc(e["eventTime"])) <= days * 86400]


def compact(events: list[dict]) -> Rows:
    """Each job's edges, folded from its runs' events: one row per job, edge and dataset, with how
    many runs had it and the first and last time one did."""
    return edges(objects(normalise(parse([json.dumps(e) for e in events])))).by_job


def lineage_of(found: list[dict], dataset: str) -> Rows:
    """The edges, run or job, that name a dataset whose name ends with `dataset`."""
    return Rows((r for r in found if r["dataset"].endswith(dataset)), empty="No edge names it.")


__all__ = ["measure", "reach", "project", "first_over", "retain", "compact", "lineage_of", "SIZES", "BUDGET"]
