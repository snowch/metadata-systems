# Copyright © 2026 Christopher Snow

"""From events to a graph: the shop's ingestion, stage by stage (Chapter 9).

The collector keeps every event it receives as one line of JSON, in the order it received them
(`event_lines`). Ingestion turns those lines into stored records and graph edges, in four stages,
each a function the reader runs and inspects:

1. `parse`: each line to an event, or a row in a list of lines it could not use, and why;
2. `normalise`: the same thing written the same way: every time in UTC with `Z`, and a warehouse
   table named without its database given the shop's (`shop`), so that two producers' names for one
   table become one;
3. `objects`: jobs, runs and datasets, each run's state taken from its latest event, and the fields
   of the facets the stage knows (`KNOWN`); a facet it does not know is listed, not read;
4. `edges`: what each run read and wrote, and, job by job, every dataset any of its runs read or
   wrote, with the first and last time a run did.

Every rule here is the shop's own choice. The OpenLineage specification says what an event must
hold, not how a consumer stores it (docs/sources.md).
"""

from __future__ import annotations

import copy
import json
from datetime import datetime, timezone

from .graph import Graph
from .openlineage import WAREHOUSE, analyst_events, dev_events, problems, run_events
from .platform import Rows
from .week import Week

# The facets the objects stage reads, and the fields it takes from each.
KNOWN = {
    "nominalTime": ["nominalStartTime"],
    "jobType": ["processingType", "jobType"],
    "sourceCodeLocation": ["version"],
    "inputStatistics": ["rowCount"],
    "outputStatistics": ["rowCount"],
    "version": ["datasetVersion"],
}

MESSAGES = {
    'json': 'The line is not JSON.',
    'rules': "The line is JSON but breaks the specification's rules for a run event.",
    'no_refused': 'No line was refused.',
    'no_changes': 'Normalising changed nothing.',
    'no_unknown': 'The stage knows every facet in the events.',
    'no_runs': 'No run matches.',
}


def event_lines(week: Week) -> list[str]:
    """Every event the collector received in the week, one line of JSON each, in the order received:
    the jobs' and the functions', and the analyst's script's when the week has the analyst's copy."""
    events = run_events(week) + analyst_events(week) + dev_events(week)
    events.sort(key=lambda ev: _utc(ev["eventTime"]))
    return [json.dumps(ev, separators=(",", ":")) for ev in events]


def _utc(text: str) -> str:
    return datetime.fromisoformat(text.replace("Z", "+00:00")).astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


class Parsed(list):
    """The events a stage passes on, and the lines it could not use."""

    def __init__(self, events, refused) -> None:
        super().__init__(events)
        self.refused = Rows(refused, empty=MESSAGES["no_refused"])

    def _repr_html_(self) -> str:
        return Rows([{"events": len(self), "refused": len(self.refused)}])._repr_html_()

    def _mime_(self):
        return ("text/html", self._repr_html_())


def parse(lines: list[str]) -> Parsed:
    """Each line to an event. A line that is not JSON, or that breaks the specification's rules, is
    refused, with its number and why."""
    events, refused = [], []
    for number, line in enumerate(lines, start=1):
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            refused.append({"line": number, "problem": MESSAGES["json"], "starts": line[:40]})
            continue
        if problems(event):
            refused.append({"line": number, "problem": MESSAGES["rules"], "starts": line[:40]})
            continue
        event["_line"] = number
        events.append(event)
    return Parsed(events, refused)


class Normalised(list):
    """The events with every change the stage made, one row per change."""

    def __init__(self, events, changes) -> None:
        super().__init__(events)
        self.changes = Rows(changes, empty=MESSAGES["no_changes"])

    def _repr_html_(self) -> str:
        return Rows([{"events": len(self), "changes": len(self.changes)}])._repr_html_()

    def _mime_(self):
        return ("text/html", self._repr_html_())


def normalise(events: list[dict], databases: dict[str, str] | None = None) -> Normalised:
    """The same thing written the same way: times in UTC with `Z`; a warehouse table's name with its
    database where the producer left it out.

    `databases` says which database a producer's names without one mean, producer by producer; a
    producer it does not list gets `shop`, the production database, as in Chapter 9.
    """
    databases = databases or {}
    out, changes = [], []
    for event in events:
        e = copy.deepcopy(event)
        line = e.get("_line")
        t = _utc(e["eventTime"])
        if t != e["eventTime"]:
            changes.append({"line": line, "where": "eventTime", "before": e["eventTime"], "after": t})
            e["eventTime"] = t
        for side in ("inputs", "outputs"):
            for k, d in enumerate(e.get(side) or []):
                if d["namespace"] == WAREHOUSE and d["name"].count(".") == 1:
                    after = f"{databases.get(e.get('producer'), 'shop')}.{d['name']}"
                    changes.append({"line": line, "where": f"{side}[{k}].name", "before": d["name"], "after": after})
                    d["name"] = after
        out.append(e)
    return Normalised(out, changes)


def _key(d: dict) -> str:
    return f"{d['namespace']}/{d['name']}"


class Objects:
    """Jobs, runs and datasets, and the facets the stage did not know."""

    def __init__(self, jobs, runs, datasets, unknown) -> None:
        self.jobs, self.runs, self.datasets = jobs, runs, datasets
        self.unknown = Rows(unknown, empty=MESSAGES["no_unknown"])

    def runs_of(self, job: str | None = None, state: str | None = None, columns: list[str] | None = None) -> Rows:
        """The runs, with every field read from their facets; only those of `job`, or in `state`,
        and only the `columns` named, where a run has them."""
        rows = [
            {k: (", ".join(v) if isinstance(v, list) else v) for k, v in r.items() if k != "run" and (columns is None or k in columns)}
            for r in self.runs.values()
            if (job is None or r["job"] == job) and (state is None or r["state"] == state)
        ]
        return Rows(rows, null="", empty=MESSAGES["no_runs"])

    def _repr_html_(self) -> str:
        return Rows(
            [{"jobs": len(self.jobs), "runs": len(self.runs), "datasets": len(self.datasets), "unknown facets": len(self.unknown)}]
        )._repr_html_()

    def _mime_(self):
        return ("text/html", self._repr_html_())


def objects(events: list[dict], known: dict | None = None) -> Objects:
    """Jobs, runs and datasets from the events. A run's state is its latest event's type, by event
    time. Of each facet, only the fields `known` names are read; any other facet is listed."""
    known = KNOWN if known is None else known
    runs: dict[str, dict] = {}
    unknown: list[dict] = []
    for e in sorted(events, key=lambda ev: ev["eventTime"]):
        job = f"{e['job']['namespace']}/{e['job']['name']}"
        r = runs.setdefault(
            e["run"]["runId"],
            {"run": e["run"]["runId"], "job": job, "state": None, "started": None, "ended": None, "reads": [], "writes": []},
        )
        r["state"] = e.get("eventType", r["state"])
        if e.get("eventType") == "START":
            r["started"] = e["eventTime"]
        if e.get("eventType") in ("COMPLETE", "ABORT", "FAIL"):
            r["ended"] = e["eventTime"]
        groups = [("run", e["run"].get("facets")), ("job", e["job"].get("facets"))]
        for side, edge in (("inputs", "reads"), ("outputs", "writes")):
            for d in e.get(side) or []:
                if _key(d) not in r[edge]:
                    r[edge].append(_key(d))
                for g in ("facets", "inputFacets", "outputFacets"):
                    groups.append((f"{d['name']}", d.get(g)))
        for where, group in groups:
            for name, f in (group or {}).items():
                if name in known:
                    for field in known[name]:
                        if field in f:
                            r[f"{name}.{field}" if where in ("run", "job") else f"{where} {name}.{field}"] = f[field]
                elif not any(u["run"] == r["run"] and u["facet"] == name for u in unknown):
                    unknown.append({"run": r["run"], "job": job, "facet": name})
    jobs: dict[str, dict] = {}
    datasets: dict[str, dict] = {}
    for r in runs.values():
        j = jobs.setdefault(r["job"], {"job": r["job"], "runs": 0})
        j["runs"] += 1
        for key in r["reads"] + r["writes"]:
            datasets.setdefault(key, {"dataset": key})
    return Objects(jobs, runs, datasets, unknown)


class Edges:
    """What each run read and wrote, and the same job by job, with the first and last time seen."""

    def __init__(self, by_run, by_job) -> None:
        self.by_run = Rows(by_run)
        self.by_job = Rows(by_job)

    def _repr_html_(self) -> str:
        return Rows([{"run edges": len(self.by_run), "job edges": len(self.by_job)}])._repr_html_()

    def _mime_(self):
        return ("text/html", self._repr_html_())

    def of(self, job: str) -> Rows:
        """The job's edges, one per dataset it read or wrote."""
        return Rows(r for r in self.by_job if r["job"] == job)

    def latest(self) -> Rows:
        """Each job's edges that its latest run had."""
        last: dict[str, str] = {}
        for r in self.by_run:
            last[r["job"]] = max(last.get(r["job"], ""), r["time"])
        return Rows(r for r in self.by_job if r["last"] == last[r["job"]])

    def graph(self, level: str = "job") -> Graph:
        """The edges as a graph: jobs and datasets (`job`), or runs and datasets (`run`)."""
        rows = self.by_job if level == "job" else self.by_run
        nodes, edges = [], []
        for r in rows:
            a = ("job", r["job"]) if level == "job" else ("run", r["run"])
            b = ("dataset", r["dataset"])
            for n in (a, b):
                if n not in nodes:
                    nodes.append(n)
            edges.append((a, r["edge"], b))
        g = object.__new__(Graph)
        g._nodes = sorted(nodes)
        g._edges = edges
        return g


def edges(objs: Objects) -> Edges:
    """Run by run, an edge to each dataset the run read or wrote; job by job, the same edges once,
    with how many runs had each and the first and last time one did."""
    by_run, by_job = [], {}
    for r in objs.runs.values():
        when = r["ended"] or r["started"]
        for edge in ("reads", "writes"):
            for d in r[edge]:
                by_run.append({"run": r["run"], "job": r["job"], "edge": edge, "dataset": d, "time": when})
                k = (r["job"], edge, d)
                j = by_job.setdefault(k, {"job": r["job"], "edge": edge, "dataset": d, "runs": 0, "first": when, "last": when})
                j["runs"] += 1
                j["first"], j["last"] = min(j["first"], when), max(j["last"], when)
    return Edges(by_run, list(by_job.values()))


__all__ = ["event_lines", "parse", "normalise", "objects", "edges", "KNOWN"]
