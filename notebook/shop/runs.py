# Copyright © 2026 Christopher Snow

"""Runs and the events that describe them (Chapter 7).

From Chapter 7 on, each program in the shop's repository sends a message as it works: one when it
starts and one when it finishes. Which fields the messages carry is the reader's design: `events`
fills in the fields the reader chose, from what really happened in the week (`Week.executions`),
and leaves out the rest. The export and the analyst's copy send nothing: their code is not the
shop's.

A field is filled where its value is known. When a program starts, it knows which program it is,
the time, the version of its code, what it is about to read and, for a function, which object
change started it. When it finishes, it knows the time, whether it succeeded, what it wrote, and
how many rows it read and wrote.

`runs` groups events into runs by the fields it is given; `run` is an identifier the program makes
when it starts and repeats in every message it sends. `day` is the UTC date of an event's `time`.
`readings` sets a design against four readings of "Record every run.", and `lineage` makes a graph
of what each run read and wrote.
"""

from __future__ import annotations

import hashlib

from .graph import Graph
from .platform import Rows
from .week import Execution, Week

FIELDS = (
    "run",
    "job",
    "type",
    "time",
    "status",
    "code_version",
    "reads",
    "writes",
    "rows_read",
    "rows_written",
    "object",
    "object_version",
    "object_change",
)

# What each field holds, as the reader's table of fields says it (Haiku's drafts of brief IA).
FIELD_NOTES = {
    'run': 'an identifier the program makes when it starts and repeats in each event of the run',
    'job': "the program's name in the shop's repository",
    'type': '`start` or `finish`',
    'time': 'when the program sent the event, in UTC',
    'status': '`succeeded` or `failed`',
    'code_version': "the first seven characters of a hash of the program's code",
    'reads': 'what the program is about to read',
    'writes': 'what the program wrote',
    'rows_read': 'how many rows the program read',
    'rows_written': 'how many rows the program wrote or removed',
    'object': 'for a program started by a change to a file, that file',
    'object_version': 'the identifier object storage gave that version of the file',
    'object_change': '`created`, `overwritten` or `deleted`',
}

# Which event carries each field: the start, the finish, or both.
AT_START = ("run", "job", "type", "time", "code_version", "reads", "object", "object_version", "object_change")
AT_FINISH = ("run", "job", "type", "time", "status", "writes", "rows_read", "rows_written")

# Four readings of "Record every run.", and the fields each needs.
READINGS = (
    ("find the runs that failed", ("run", "status")),
    ("know when each asset was last written", ("time", "writes")),
    ("know which version of the code each run used", ("run", "code_version")),
    ("know which object change started a run", ("run", "object", "object_version", "object_change")),
)


def event_fields() -> Rows:
    """The fields a design can choose from: which event carries each, and what it holds."""
    def sent(f: str) -> str:
        return "both" if f in AT_START and f in AT_FINISH else ("start" if f in AT_START else "finish")
    return Rows({"field": f, "sent at": sent(f), "holds": FIELD_NOTES[f]} for f in FIELDS)


def code_version(code: str | None) -> str | None:
    """A short version of a program's code: the first seven characters of a hash of its text."""
    return hashlib.sha1(code.encode()).hexdigest()[:7] if code is not None else None


def executions(week: Week) -> list[tuple[str, Execution]]:
    """Every time one of the repository's programs did its work, in order, each with its run identifier."""
    done = [e for e in week.executions if e.job and e.environment == "production"]
    return [(f"run-{k + 1:03d}", e) for k, e in enumerate(done)]


def _name(uri: str) -> str:
    """How an event names an asset: a file by its address, a table or the dashboard by its name."""
    return uri


def _check(fields) -> tuple[str, ...]:
    fields = tuple(fields)
    unknown = [f for f in fields if f not in FIELDS]
    if unknown:
        raise ValueError(f"no field called {unknown[0]!r}; the fields are {', '.join(FIELDS)}")
    return fields


def events(week: Week, fields=FIELDS) -> Rows:
    """Every event the repository's programs sent in the week, carrying only `fields`, in time order."""
    fields = _check(fields)
    out = []
    for run, e in executions(week):
        start = {
            "run": run,
            "job": e.job,
            "type": "start",
            "time": e.started,
            "code_version": code_version(e.code),
            "reads": ", ".join(_name(r) for r in e.reads),
            "object": e.object,
            "object_version": e.version,
            "object_change": e.change,
        }
        finish = {
            "run": run,
            "job": e.job,
            "type": "finish",
            "time": e.finished,
            "status": e.status,
            "writes": _name(e.wrote) if e.wrote and e.status == "succeeded" else "",
            "rows_read": e.rows_read,
            "rows_written": e.rows if e.status == "succeeded" else None,
        }
        for event, carried in ((start, AT_START), (finish, AT_FINISH)):
            out.append({f: event.get(f) if f in carried else None for f in fields})
    order = {f: k for k, f in enumerate(FIELDS)}
    out.sort(key=lambda ev: ev.get("time") or "")
    return Events(out, fields, sorted(fields, key=order.get))


class Events(Rows):
    """The events, as a table of the fields the design chose."""

    def __init__(self, rows, fields, shown) -> None:
        super().__init__(({f: r.get(f) for f in shown} for r in rows), null="")
        self.fields = tuple(fields)

    def where(self, **match) -> "Events":
        """The events whose fields have these values: `events.where(job="build_clean_orders")`."""
        for f in match:
            if f not in self.fields:
                raise KeyError(f"the events carry no field {f!r}")
        return Events([r for r in self if all(r.get(f) == v for f, v in match.items())], self.fields, list(self[0]) if self else self.fields)


class Runs(Rows):
    """Runs, one per row, with a way to pick some."""

    def where(self, **match) -> "Runs":
        """The runs whose fields have these values; a list or a tuple means any of them."""
        def ok(r: dict, f: str, v) -> bool:
            return r.get(f) in v if isinstance(v, (list, tuple)) else r.get(f) == v
        return Runs([r for r in self if all(ok(r, f, v) for f, v in match.items())], null="")


def runs(events: Events, by=("run",)) -> Runs:
    """The events grouped into runs: one row for each value of the fields in `by`.

    `day` in `by` is the UTC date of an event's `time`. Where the events of one group disagree on
    a field, the row lists every value they hold; the row counts are added up.
    """
    by = tuple(by)
    for f in by:
        if f == "day":
            if "time" not in events.fields:
                raise KeyError("`day` is the date of an event's `time`, and the events carry no `time`")
        elif f not in events.fields:
            raise KeyError(f"the events carry no field {f!r}, so it cannot tell runs apart")
    groups: dict[tuple, list[dict]] = {}
    for ev in events:
        key = tuple((ev["time"] or "")[:10] if f == "day" else ev.get(f) for f in by)
        groups.setdefault(key, []).append(ev)
    out = []
    for key, group in groups.items():
        row: dict = dict(zip(by, key))
        row["events"] = len(group)
        for f in events.fields:
            if f in by or f == "type":
                continue
            if f == "time":
                starts = [e["time"] for e in group if e.get("type") in (None, "start")]
                finishes = [e["time"] for e in group if e.get("type") in (None, "finish")]
                if "type" in events.fields:
                    row["started"] = min(starts) if starts else None
                    row["finished"] = max(finishes) if finishes else None
                else:
                    row["first"], row["last"] = min(e["time"] for e in group), max(e["time"] for e in group)
                continue
            if f in ("rows_read", "rows_written"):
                # Counts add up: a row that holds two runs holds both runs' rows.
                counts = [e[f] for e in group if e.get(f) is not None]
                row[f] = sum(counts) if counts else None
                continue
            values = []
            for e in group:
                v = e.get(f)
                if v not in (None, "") and v not in values:
                    values.append(v)
            row[f] = values[0] if len(values) == 1 else (", ".join(str(v) for v in values) if values else None)
        out.append(row)
    return Runs(out, null="")


def readings(fields) -> Rows:
    """Four readings of "Record every run.", the fields each needs, and whether the design has them."""
    fields = _check(fields)
    return Rows(
        {
            "reading": reading,
            "needs": ", ".join(needs),
            "missing": ", ".join(f for f in needs if f not in fields),
            "met": "yes" if all(f in fields for f in needs) else "no",
        }
        for reading, needs in READINGS
    )


def lineage(runs_: Rows) -> Graph:
    """What each run read and wrote, as a graph of jobs and assets: `reads` and `writes` edges.

    A run whose events carry no `reads` adds no edge into its job, which the graph cannot tell from
    a job that reads nothing.
    """
    nodes: list[tuple[str, str]] = []
    edges: list[tuple[tuple[str, str], str, tuple[str, str]]] = []

    def node(kind: str, name: str) -> tuple[str, str]:
        n = (kind, name)
        if n not in nodes:
            nodes.append(n)
        return n

    def kind_of(name: str) -> str:
        return "dashboard" if name == "sales_dashboard" else "dataset"

    for r in runs_:
        job = r.get("job")
        if not job:
            continue
        j = node("job", job)
        for attribute in ("reads", "writes"):
            for name in str(r.get(attribute) or "").split(", "):
                if not name:
                    continue
                edge = (j, attribute, node(kind_of(name), name))
                if edge not in edges:
                    edges.append(edge)
    g = object.__new__(Graph)
    g._nodes = sorted(nodes, key=lambda t: (t[0], t[1]))
    g._edges = edges
    return g


__all__ = ["FIELDS", "READINGS", "event_fields", "events", "runs", "readings", "lineage", "code_version"]
