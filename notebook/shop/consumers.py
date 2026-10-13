# Copyright © 2026 Christopher Snow

"""A real producer's names and a real consumer's rules, applied to the shop's week (Chapter 29).

Neither system runs here. Each function applies a rule that the system's code states, read at a
named commit (`docs/sources.md`, "Read for Part VII"), to the shop's own events:

- `provider`: how Airflow's OpenLineage provider (`providers/openlineage`, 2.20.3) would name the
  shop's four nightly jobs if they ran as tasks of one Dag, `shop_nightly`: the job is
  `{dag_id}.{task_id}`; its namespace is the configured one, or `default`; each task's events carry
  a `parent` facet naming the Dag's run. The run id here is the shop's own, made from the same
  values the provider uses (namespace, Dag, task, try and map index, with the logical date); it is
  not the provider's value.
- `MarquezRules`: how Marquez (`MarquezProject/marquez`, commit 180f37b) takes run events: it
  refuses an event with no `eventTime`; it keeps every event it takes as a row, with nothing that
  makes a row unique; for an event with a type, it writes a state row, sets the run's current state
  from that event whatever the order (`RunDao.upsert`), and moves the run's start time on a
  `START` and its end time on `COMPLETE`, `ABORT` or `FAIL`, each to the event's own time. `START`,
  `RUNNING`, `OTHER` and any type it does not know all map to its state `RUNNING`.
- `compare`: Chapter 25's arrivals, faults and all, through the learner's collector (the shop's
  versions of its three pieces) and through Marquez's rules, in the order the events arrived or in
  event-time order; `check` asks one thing of the order the learner chooses.

The Dag's name, the order a buffer could impose, and every name the tables show are the shop's.
"""

from __future__ import annotations

import copy

from . import collector, openlineage
from .delivery import week_events
from .ingest import normalise
from .platform import Rows
from .week import Week

DAG = "shop_nightly"
PROVIDER = "https://github.com/apache/airflow/tree/providers-openlineage/2.20.3"
NIGHTLY = ("build_clean_customers", "build_clean_orders", "build_daily_sales", "refresh_dashboard")
ORDERS = ("arrival", "event time")

MESSAGES = {
    "summary": "{passed} of {total} tests pass.",
    "friday": "The run early on Friday 11 is `{marquez}` by Marquez's rules, and `{yours}` in your collector.",
    "friday_no": "The run early on Friday 11 is `{marquez}` by Marquez's rules, but `{yours}` in your collector.",
    "order_no": "`order` must be one of {orders}.",
}

# Marquez's states for each event type (`OpenLineageDao.getRunState`); any other type is RUNNING.
STATES = {"COMPLETE": "COMPLETED", "ABORT": "ABORTED", "FAIL": "FAILED", "START": "RUNNING"}
DONE = ("COMPLETED", "ABORTED", "FAILED")


def provider(week: Week, namespace: str = "default") -> Rows:
    """The shop's nightly jobs, as the shop names them and as the provider would."""
    return Rows(
        {
            "the shop's job": f"{openlineage.JOB_NAMESPACE}/{job}",
            "the provider's job": f"{namespace}/{DAG}.{job}",
            "its parent": f"{namespace}/{DAG}",
        }
        for job in NIGHTLY
    )


def provider_event(week: Week, job: str = "build_daily_sales", day: str = "2026-09-11", namespace: str = "default") -> dict:
    """The `START` of one of the shop's runs, with the names and facets the provider would give it."""
    ev = copy.deepcopy(next(e for e in week_events(week) if e["job"]["name"] == job and e["eventType"] == "START" and e["eventTime"].startswith(day)))
    logical = ev["run"]["facets"]["nominalTime"]["nominalStartTime"]
    ev["producer"] = PROVIDER
    ev["run"]["runId"] = openlineage.uuid7(ev["eventTime"], f"{namespace}.{DAG}.{job}.1.-1")
    ev["run"]["facets"]["parent"] = {
        "_producer": PROVIDER,
        "_schemaURL": "https://openlineage.io/spec/facets/1-2-0/ParentRunFacet.json#/$defs/ParentRunFacet",
        "run": {"runId": openlineage.uuid7(logical, f"{namespace}.{DAG}.{logical}")},
        "job": {"namespace": namespace, "name": DAG},
    }
    for facet in ev["run"]["facets"].values():
        facet["_producer"] = PROVIDER
    ev["job"] = {
        "namespace": namespace,
        "name": f"{DAG}.{job}",
        "facets": {"jobType": {**ev["job"]["facets"]["jobType"], "_producer": PROVIDER, "integration": "AIRFLOW", "jobType": "TASK"}},
    }
    return ev


class MarquezRules:
    """Marquez's rules for run events, as its code states them (see the module's note)."""

    def __init__(self) -> None:
        self.events: list[dict] = []
        self.states: list[dict] = []
        self.runs: dict[str, dict] = {}
        self.refused: list[dict] = []

    def take(self, ev: dict) -> str:
        if not ev.get("eventTime") or not ev.get("run", {}).get("runId"):
            self.refused.append(ev)
            return "refused"
        self.events.append(ev)
        run = self.runs.setdefault(ev["run"]["runId"], {"job": ev["job"]["name"], "state": None, "started": None, "ended": None})
        kind = ev.get("eventType")
        if kind is None:
            return "kept"
        state = STATES.get(kind, "RUNNING")
        self.states.append({"run": ev["run"]["runId"], "state": state, "time": ev["eventTime"]})
        run["state"] = state
        if state in DONE:
            run["ended"] = ev["eventTime"]
        elif kind == "START":
            run["started"] = ev["eventTime"]
        return "kept"


def _sent(week: Week, order: str) -> list[dict]:
    got = [ev for _, ev in collector.arrivals(week)]
    if order == "event time":
        got = sorted(got, key=lambda e: (e.get("eventTime") is None, e.get("eventTime") or ""))
    return [copy.deepcopy(e) for e in got]


def _collector(week: Week, order: str) -> collector.Collector:
    ns: dict = {}
    for name in ("key", "newer", "start"):
        exec(collector.REFERENCE[name], ns)
    c = collector.Collector(ns["key"], ns["newer"], ns["start"])
    for ev in _sent(week, order):
        c.receive(ev, ev.get("eventTime") or "")
    return c


def _marquez(week: Week, order: str) -> MarquezRules:
    m = MarquezRules()
    for ev in _sent(week, order):
        [ev] = normalise([ev]) if ev.get("eventTime") else [ev]
        m.take(ev)
    return m


def _run(runs: dict, job: str, day: str) -> tuple[str, dict]:
    for run_id, r in runs.items():
        if r["job"] == job and (r["started"] or r["ended"] or "").startswith(day):
            return run_id, r
    raise KeyError((job, day))


FAULTED = (
    ("build_daily_sales", "2026-09-10", "build_daily_sales, Thursday 10: its COMPLETE again, with a new time"),
    ("build_daily_sales", "2026-09-11", "build_daily_sales, Friday 11: its START after its COMPLETE"),
    ("remove_return", "2026-09-12", "remove_return, Saturday 12: its COMPLETE twice"),
)


def compare(week: Week, order: str = "arrival") -> Rows:
    """The runs the faults touch, in the learner's collector and by Marquez's rules."""
    c, m = _collector(week, order), _marquez(week, order)
    out = []
    for job, day, what in FAULTED:
        run_id, r = _run(m.runs, job, day)
        mine = c.state.get(run_id, {})
        out.append({
            "run": what,
            "collector's state": mine.get("eventType"),
            "collector's end": (mine.get("eventTime") or "")[11:19] if mine.get("eventType") == "COMPLETE" else None,
            "collector's events": sum(e["run"]["runId"] == run_id for e in c.file),
            "Marquez's state": r["state"],
            "Marquez's end": (r["ended"] or "")[11:19] or None,
            "Marquez's event rows": sum(e["run"]["runId"] == run_id for e in m.events),
            "Marquez's state rows": sum(s["run"] == run_id for s in m.states),
        })
    return Rows(out, null="")


def totals(week: Week, order: str = "arrival") -> Rows:
    """What each consumer stored from the week's arrivals."""
    c, m = _collector(week, order), _marquez(week, order)
    return Rows([
        {"consumer": "your collector", "events refused": len(c.refused), "events stored": len(c.file)},
        {"consumer": "Marquez's rules", "events refused": len(m.refused), "events stored": len(m.events)},
    ])


class Checked(Rows):
    def __init__(self, rows) -> None:
        super().__init__(rows)
        self.passed = sum(r["passes"] == "yes" for r in rows)

    def _repr_html_(self) -> str:
        return f"<p>{MESSAGES['summary'].format(passed=self.passed, total=len(self))}</p>" + super()._repr_html_()


def check(week: Week, order: str) -> Checked:
    """Whether Marquez's rules and the learner's collector agree on Friday 11's run, in `order`."""
    if order not in ORDERS:
        return Checked([{"test": MESSAGES["order_no"].format(orders=", ".join(f'"{o}"' for o in ORDERS)), "passes": "no"}])
    friday = compare(week, order)[1]
    same = (friday["Marquez's state"], friday["collector's state"]) == ("COMPLETED", "COMPLETE")
    return Checked([{
        "test": MESSAGES["friday" if same else "friday_no"].format(marquez=friday["Marquez's state"], yours=friday["collector's state"]),
        "passes": "yes" if same else "no",
    }])


STUBS = {"order": 'order = "arrival"'}
REFERENCE = {"order": 'order = "event time"'}

__all__ = ["provider", "provider_event", "MarquezRules", "compare", "totals", "check", "STUBS", "REFERENCE", "DAG", "ORDERS"]
