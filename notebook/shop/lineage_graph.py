# Copyright © 2026 Christopher Snow

"""The lineage graph, built (Chapter 26): persistent edges with the time each was first and last
seen, updated one stored event at a time.

The events are the collector's file, as Chapter 25 built it (the shop's reference pieces), for the
week in which the analyst's copy replaced `clean_orders` as `build_daily_sales`'s source on Sunday
13 (`source`), with Part V's faults. `edges_of(event)` gives the edges an event names, as (job,
edge, dataset); the learner writes `add(edges, event)`, which keeps for each edge the runs that had
it and its first and last time; `check` builds the graph as the events arrive and tests it.

`now` answers "which edges does the platform have now?" three ways: the edges of each job's latest
run, every edge ever seen, and the edges seen since a time.
"""

from __future__ import annotations

import copy

from . import collector
from .ingest import _key, edges, normalise, objects
from .platform import Rows, epoch
from .week import Week

THURSDAY = "2026-09-10T09:00:00Z"
MONDAY = "2026-09-14T09:00:00Z"

MESSAGES = {
    "summary": "{passed} of {total} tests pass.",
    "whole": "Built from the whole file, the graph has the edges and run counts Chapter 9's way of building edges by job gives for it.",
    "whole_no": "Built from the whole file, the graph differs in {n} edges or run counts from what Chapter 9's way of building edges by job gives for it.",
    "thursday": "At 09:00 on Thursday 10, `build_daily_sales` last wrote `daily_sales` at {got}.",
    "thursday_no": "At 09:00 on Thursday 10, `build_daily_sales` last wrote `daily_sales` at {got}, not {want}.",
    "reload": "Saved and loaded again after the restart, the graph holds the same edges, runs and times as one never saved.",
    "reload_no": "Saved and loaded again after the restart, the graph differs from one never saved.",
}


def edges_of(event: dict) -> list[tuple[str, str, str]]:
    """The edges one event names: (job, "reads" or "writes", dataset)."""
    job = f"{event['job']['namespace']}/{event['job']['name']}"
    return [(job, edge, _key(d)) for side, edge in (("inputs", "reads"), ("outputs", "writes")) for d in event.get(side) or []]


def stored(week: Week) -> list[tuple[str, dict]]:
    """The collector's file, as Chapter 25 built it, with when each event arrived."""
    ns: dict = {}
    for piece in ("key", "newer", "start"):
        exec(collector.REFERENCE[piece], ns)
    kept = []
    c = collector.Collector(ns["key"], ns["newer"], ns["start"])
    for arrived, ev in collector.arrivals(week):
        if c.receive(copy.deepcopy(ev), arrived) == "kept":
            kept.append((arrived, c.file[-1]))
    return kept


def build(week: Week, add, until: str | None = None, reload_at: str | None = None) -> dict:
    """The graph built by `add` from the stored events, in the order they arrived, up to `until`;
    saved and loaded again at `reload_at`, as the edges' own file would be."""
    graph: dict = {}
    for arrived, ev in stored(week):
        if until and epoch(arrived) > epoch(until):
            break
        if reload_at and epoch(arrived) > epoch(reload_at):
            graph = load(save(graph))
            reload_at = None
        add(graph, copy.deepcopy(ev))
    return graph


def save(graph: dict) -> list[dict]:
    """The graph as lines for a file: one per edge, its runs as a sorted list."""
    return [{"job": j, "edge": e, "dataset": d, "runs": sorted(v["runs"]), "first": v["first"], "last": v["last"]} for (j, e, d), v in sorted(graph.items())]


def load(lines: list[dict]) -> dict:
    return {(r["job"], r["edge"], r["dataset"]): {"runs": set(r["runs"]), "first": r["first"], "last": r["last"]} for r in lines}


def table(graph: dict, job: str | None = None) -> Rows:
    """The graph as rows: each edge, how many runs had it, and its first and last time."""
    return Rows(
        {"job": j, "edge": e, "dataset": d, "runs": len(v["runs"]), "first": v["first"], "last": v["last"]}
        for (j, e, d), v in sorted(graph.items())
        if job is None or j.endswith(job)
    )


class Checked(Rows):
    def __init__(self, rows) -> None:
        super().__init__(rows)
        self.passed = sum(r["passes"] == "yes" for r in rows)

    def _repr_html_(self) -> str:
        return f"<p>{MESSAGES['summary'].format(passed=self.passed, total=len(self))}</p>" + super()._repr_html_()


def check(week: Week, add) -> Checked:
    rows = []

    def test(ok, yes, no, **kw):
        rows.append({"test": (yes if ok else no).format(**kw), "passes": "yes" if ok else "no"})

    whole = table(build(week, add))
    mine = {(r["job"], r["edge"], r["dataset"], r["runs"]) for r in whole}
    want = {(r["job"], r["edge"], r["dataset"], r["runs"]) for r in edges(objects(normalise([e for _, e in stored(week)]))).by_job}
    differ = len(mine ^ want)
    test(differ == 0, MESSAGES["whole"], MESSAGES["whole_no"], n=differ)
    thursday = build(week, add, until=THURSDAY)
    key = ("shop/build_daily_sales", "writes", "warehouse://shop-warehouse/shop.analytics.daily_sales")
    got = thursday.get(key, {}).get("last", "nothing")
    want_t = "2026-09-10T02:30:21Z"
    test(got == want_t, MESSAGES["thursday"], MESSAGES["thursday_no"], got=got, want=want_t)
    test(table(build(week, add, reload_at=collector.RESTART)) == whole, MESSAGES["reload"], MESSAGES["reload_no"])
    return Checked(rows)


def now(graph: dict, at: str, days: int = 2, jobs: tuple[str, ...] = ("build_daily_sales", "record_return")) -> Rows:
    """Which of the chosen programs' edges the platform has now, three ways: in the program's latest
    run, ever, and seen in the last `days` days before `at`."""
    latest: dict[str, str] = {}
    for (j, e, d), v in graph.items():
        latest[j] = max(latest.get(j, ""), v["last"])
    since = epoch(at) - days * 86400
    out = []
    for name in jobs:
        for (j, e, d), v in sorted(graph.items()):
            if j.rsplit("/", 1)[-1] != name:
                continue
            out.append({
                "job": name, "edge": e, "dataset": d.rsplit("/", 1)[-1],
                "in the latest run": "yes" if v["last"] == latest[j] else "no",
                "ever": "yes",
                f"in the last {days} days": "yes" if epoch(v["last"]) >= since else "no",
            })
    return Rows(out)


STUBS = {
    "add": '''def add(edges, event):
    for key in shop.lineage_graph.edges_of(event):
        edge = edges.setdefault(key, {"runs": set(), "first": event["eventTime"], "last": event["eventTime"]})
        edge["runs"].add(event["run"]["runId"])
        edge["last"] = event["eventTime"]''',
}

REFERENCE = {
    "add": '''def add(edges, event):
    for key in shop.lineage_graph.edges_of(event):
        edge = edges.setdefault(key, {"runs": set(), "first": event["eventTime"], "last": event["eventTime"]})
        edge["runs"].add(event["run"]["runId"])
        edge["first"] = min(edge["first"], event["eventTime"])
        edge["last"] = max(edge["last"], event["eventTime"])''',
}

__all__ = ["edges_of", "stored", "build", "save", "load", "table", "check", "now", "STUBS", "REFERENCE"]
