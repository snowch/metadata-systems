# Copyright © 2026 Christopher Snow

"""The collector, built (Chapter 25): it receives the week's events with Part V's faults, refuses
what breaks the specification, keeps each event once in a file, keeps each run's latest state, and
starts again from its file after a restart.

The faults, all in one week (`arrivals`): a COMPLETE whose acknowledgement is lost, so it arrives
twice (`remove_return`, Saturday 12); a COMPLETE whose acknowledgement is lost and which the
program builds again with the time of the new sending (`build_daily_sales`, Thursday 10); a
COMPLETE held up 26 hours (Wednesday 9's); a START held up a minute, past its own COMPLETE (Friday
11's); an event from the developer's laptop with no `eventTime`; and a restart of the collector
between the two arrivals of Saturday's COMPLETE.

The learner writes three pieces, and the rest is the shop's:

- `key(event)`: what makes two events the same, for dropping repeats;
- `newer(event, current)`: whether an event that arrives replaces the state the collector holds for
  its run;
- `start(stored)`: what the collector remembers when it starts, from the events in its file.

`check` runs the collector over the week with the three pieces and reports each test. Validation
is Chapter 8's check; the file is a list of normalised events (Chapter 9's first stage), which
survives the restart; everything else is in memory and does not.
"""

from __future__ import annotations

import copy

from . import openlineage
from .delivery import Delivery, send, week_events
from .ingest import _utc, edges, normalise, objects
from .platform import Rows
from .week import Week

FILE = "s3://shop-metadata/events.jsonl"
RESTART = "2026-09-12T16:50:20Z"
BROKEN_AT = "2026-09-11T10:00:00Z"
FAULTS = {
    "delay": {"build_daily_sales COMPLETE 2026-09-09": 26 * 3600, "build_daily_sales START 2026-09-11": 60},
    "lose_ack": ["remove_return COMPLETE", "build_daily_sales COMPLETE 2026-09-10"],
    "restamp": ["build_daily_sales COMPLETE 2026-09-10"],
}

MESSAGES = {
    "refused": "The broken event is refused: {why}.",
    "refused_no": "The broken event is not refused.",
    "once": "Each of the week's {n} events is kept once.",
    "once_no": "The file holds {stored} events, not {n}: {extra}.",
    "thursday": "The run early on Thursday 10 ends at {got}.",
    "thursday_no": "The run early on Thursday 10 ends at {got}, not {want}.",
    "friday": "The run early on Friday 11 is {got}.",
    "friday_no": "The run early on Friday 11 is {got}, not {want}.",
    "restart": "The COMPLETE that arrived again after the restart is dropped.",
    "restart_no": "The COMPLETE that arrived again after the restart is kept a second time.",
    "graph": "The graph from the file is the graph of the week with no faults.",
    "graph_no": "The graph from the file differs from the graph of the week with no faults.",
    "summary": "{passed} of {total} tests pass.",
}


def _broken(week: Week) -> dict:
    """The developer's test event: a copy of a START, in a namespace of its own, with no time."""
    ev = copy.deepcopy(next(e for e in week_events(week) if e["eventType"] == "START"))
    ev["job"] = {"namespace": openlineage.DEV_NAMESPACE, "name": "try_daily_sales"}
    ev["producer"] = openlineage.DEV_PRODUCER
    ev["run"] = {"runId": "019a0000-0000-7000-8000-000000000001"}
    del ev["eventTime"]
    return ev


def arrivals(week: Week) -> list[tuple[str, dict]]:
    """Every event the collector receives in the week, with when it arrived, in that order."""
    d: Delivery = send(week, at_least_once=True, **FAULTS)
    got = [(a.arrived, a.event) for a in d.arrivals]
    got.append((BROKEN_AT, _broken(week)))
    return sorted(got, key=lambda p: p[0])


def faults(week: Week) -> Rows:
    """The arrivals the faults touch: the broken event, each repeat, and each event held up."""
    whole = week_events(week)
    plain = {(e["job"]["name"], e["eventType"], e["eventTime"]) for e in whole}
    seen: dict = {}
    out = []
    for arrived, ev in arrivals(week):
        job, kind, when = ev.get("job", {}).get("name"), ev.get("eventType"), ev.get("eventTime")
        k = (ev.get("run", {}).get("runId"), kind)
        if when is None:
            fault = "no eventTime"
        elif k in seen:
            fault = "a repeat" if when == seen[k] else "a repeat, with a new time"
        elif (job, kind, when) in plain and _secs(arrived) - _secs(when) > 3:
            fault = "held up"
        else:
            seen[k] = when
            continue
        seen.setdefault(k, when)
        out.append({"arrived": arrived, "job": job, "type": kind, "event time": _utc(when) if when else None, "fault": fault})
    return Rows(out, null="")


def _secs(t: str) -> int:
    from .platform import epoch

    return epoch(_utc(t))


class Collector:
    """The shop's collector, with the learner's three pieces."""

    def __init__(self, key, newer, start) -> None:
        self.key, self.newer, self.start = key, newer, start
        self.file: list[dict] = []
        self.refused: list[dict] = []
        self.dropped: list[dict] = []
        self.restarted = False
        self.boot()

    def boot(self) -> None:
        """Start: memory is empty except what `start` makes from the file."""
        self.seen = set(self.start(list(self.file)) or ())
        self.state: dict[str, dict] = {}
        for ev in self.file:
            self._keep_state(ev)

    def _keep_state(self, ev: dict) -> None:
        run = ev["run"]["runId"]
        current = self.state.get(run)
        if current is None or self.newer(ev, current):
            self.state[run] = ev

    def receive(self, ev: dict, arrived: str) -> str:
        found = openlineage.problems(ev)
        if found:
            self.refused.append({"arrived": arrived, "job": ev.get("job", {}).get("name"), "problems": ", ".join(f"{w} {k}" for w, k in found)})
            return "refused"
        [ev] = normalise([ev])
        k = self.key(ev)
        if k in self.seen:
            self.dropped.append({"arrived": arrived, "job": ev["job"]["name"], "type": ev["eventType"], "event time": ev["eventTime"], "after restart": self.restarted})
            return "dropped"
        self.seen.add(k)
        self.file.append(ev)
        self._keep_state(ev)
        return "kept"

    def stored(self) -> Rows:
        return Rows({"job": e["job"]["name"], "type": e["eventType"], "event time": e["eventTime"]} for e in self.file)


def run(week: Week, key, newer, start=None) -> Collector:
    """The collector over the week's arrivals; with `start`, restarted once at `RESTART`."""
    c = Collector(key, newer, start or (lambda stored: set()))
    for arrived, ev in arrivals(week):
        if start is not None and not c.restarted and arrived > RESTART:
            c.restarted = True
            c.boot()
        c.receive(copy.deepcopy(ev), arrived)
    return c


def _run_of(c: Collector, job: str, day: str) -> dict | None:
    starts = [e for e in c.file if e["job"]["name"] == job and e["eventType"] == "START" and e["eventTime"].startswith(day)]
    return c.state.get(starts[0]["run"]["runId"]) if starts else None


class Checked(Rows):
    def __init__(self, rows) -> None:
        super().__init__(rows)
        self.passed = sum(r["passes"] == "yes" for r in rows)

    def _repr_html_(self) -> str:
        return f"<p>{MESSAGES['summary'].format(passed=self.passed, total=len(self))}</p>" + super()._repr_html_()


def check(week: Week, key, newer, start=None) -> Checked:
    """The tests, over the week's arrivals; with `start`, the collector restarts once and one more
    test asks whether the repeat after the restart was dropped."""
    c = run(week, key, newer, start)
    whole = week_events(week)
    rows = []

    def test(ok: bool, yes: str, no: str, **kw) -> None:
        rows.append({"test": (yes if ok else no).format(**kw), "passes": "yes" if ok else "no"})

    test(len(c.refused) == 1, MESSAGES["refused"], MESSAGES["refused_no"], why=c.refused[0]["problems"] if c.refused else "")
    keys = [(e["run"]["runId"], e["eventType"]) for e in c.file]
    extra = len(c.file) - len(whole)
    test(len(c.file) == len(whole) and len(set(keys)) == len(keys), MESSAGES["once"], MESSAGES["once_no"], n=len(whole), stored=len(c.file), extra=f"{extra} more" if extra > 0 else f"{-extra} fewer")
    thu = _run_of(c, "build_daily_sales", "2026-09-10")
    got = thu["eventTime"][11:19] if thu and thu["eventType"] == "COMPLETE" else (thu or {}).get("eventType", "missing")
    test(got == "02:30:21", MESSAGES["thursday"], MESSAGES["thursday_no"], got=got, want="02:30:21")
    fri = _run_of(c, "build_daily_sales", "2026-09-11")
    got = (fri or {}).get("eventType", "missing")
    test(got == "COMPLETE", MESSAGES["friday"], MESSAGES["friday_no"], got=f"`{got}`", want="`COMPLETE`")
    if start is not None:
        after = [d for d in c.dropped if d["after restart"] and d["job"] == "remove_return"]
        test(bool(after), MESSAGES["restart"], MESSAGES["restart_no"])
    same = edges(objects(c.file)).by_job == edges(objects(normalise(whole))).by_job
    test(same, MESSAGES["graph"], MESSAGES["graph_no"])
    return Checked(rows)


STUBS = {
    "key": '''import json

def key(event):
    return json.dumps(event, sort_keys=True)''',
    "newer": '''def newer(event, current):
    return True''',
    "start": '''def start(stored):
    return set()''',
}

REFERENCE = {
    "key": '''def key(event):
    return (event["run"]["runId"], event["eventType"])''',
    "newer": '''def newer(event, current):
    return event["eventTime"] >= current["eventTime"]''',
    "start": '''def start(stored):
    return {key(event) for event in stored}''',
}

__all__ = ["arrivals", "faults", "run", "check", "Collector", "STUBS", "REFERENCE", "RESTART", "FILE"]
