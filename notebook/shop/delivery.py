# Copyright © 2026 Christopher Snow

"""The path an event takes from a program to the collector, and what goes wrong on it (Part V).

Each program sends each event a second after its event time (`SEND_LAG`), and the collector
receives it two seconds later (`LATENCY`), unless the path loses it or holds it up. `send` takes the
week's events and the faults to apply, picked by `job TYPE` or `job TYPE YYYY-MM-DD` (the date of the
event's time, in UTC):

- `lose`: the path loses that many of the event's sendings (one, unless given as `(pick, n)`);
- `delay`: the path holds the event up for that many seconds;
- `lose_ack`: the event arrives, and the collector's acknowledgement of it is lost;
- `restamp`: a program that sends an event again builds it again, with the time of the new sending
  as its event time.

With `at_least_once`, a program keeps each event until the collector acknowledges it, and sends it
again after `ACK_WAIT` seconds without one. Without it, a program sends each event once and keeps
nothing, and an event the path loses is gone.

`open_runs` lists the runs the collector has a START for and no COMPLETE, ABORT or FAIL.
`repeated_work` finds function runs started twice for one change of one object.

Every rule and every time here is the shop's own choice. The OpenLineage specification says what an
event holds, not how it travels (docs/sources.md).
"""

from __future__ import annotations

import copy
import json
from dataclasses import dataclass, field
from statistics import median

from .ingest import _utc
from .openlineage import OBJECT_CHANGE, analyst_events, dev_events, run_events
from .platform import Rows, epoch, iso
from .week import Week

SEND_LAG = 1
LATENCY = 2
ACK_WAIT = 30
TERMINAL = ("COMPLETE", "ABORT", "FAIL")

MESSAGES = {
    "no_open": "Every run the collector has a START for also has its end.",
    "no_repeats": "No change of an object started its function more than once.",
    "no_retries": "Every event was sent once and received once.",
}


def _job(ev: dict) -> str:
    return ev["job"]["name"]


def _time(ev: dict) -> str:
    return _utc(ev["eventTime"])


def describe(ev: dict) -> str:
    """An event as the pages name it: its job, its type and its time."""
    return f"{_job(ev)} {ev['eventType']} {_time(ev)}"


def pick(events: list[dict], spec: str) -> int:
    """The position of the one event `spec` names: `job TYPE`, or `job TYPE YYYY-MM-DD`."""
    parts = spec.split()
    job, kind = parts[0], parts[1]
    day = parts[2] if len(parts) > 2 else None
    found = [i for i, ev in enumerate(events) if _job(ev) == job and ev["eventType"] == kind and (day is None or _time(ev)[:10] == day)]
    if len(found) != 1:
        names = ", ".join(describe(events[i]) for i in found) or "none"
        raise ValueError(f"{spec!r} names {len(found)} events, not one: {names}")
    return found[0]


def week_events(week: Week) -> list[dict]:
    """Every event the week's programs send, in the order of their event times."""
    events = run_events(week) + analyst_events(week) + dev_events(week)
    return sorted(events, key=_time)


@dataclass
class Arrival:
    event: dict
    sent: str
    arrived: str
    attempt: int


@dataclass
class Delivery:
    """What the collector received, in the order it received it, and what happened to each event."""

    arrivals: list[Arrival]
    log: Rows
    at_least_once: bool
    lost: list[dict] = field(default_factory=list)

    @property
    def events(self) -> list[dict]:
        """The events as received, in the order received."""
        return [a.event for a in self.arrivals]

    @property
    def lines(self) -> list[str]:
        """The collector's lines: one line of JSON per event received, in the order received."""
        return [json.dumps(e, separators=(",", ":")) for e in self.events]

    def retried(self) -> Rows:
        """The events sent more than once or received more than once."""
        return Rows((r for r in self.log if r["sendings"] > 1 or r["received"] > 1), null="", empty=MESSAGES["no_retries"])

    def until(self, at: str) -> list[dict]:
        """The events the collector had received by `at`, in the order received."""
        return [a.event for a in self.arrivals if epoch(a.arrived) <= epoch(at)]

    def received(self, job: str | None = None, type: str | None = None) -> Rows:
        """Each event as the collector received it, in the order it arrived: its job, type and event
        time, and when it arrived; only `job`'s events, or only those of `type`, if given."""
        return Rows(
            {"arrived": a.arrived, "job": _job(a.event), "type": a.event["eventType"], "event time": _time(a.event)}
            for a in self.arrivals
            if (job is None or _job(a.event) == job) and (type is None or a.event["eventType"] == type)
        )

    def _repr_html_(self) -> str:
        sent = len(self.log)
        return Rows(
            [{"events sent": sent, "received": len(self.arrivals), "lost": len(self.lost),
              "received more than once": sum(1 for r in self.log if r["received"] > 1)}]
        )._repr_html_()

    def _mime_(self):
        return ("text/html", self._repr_html_())


def _specs(given) -> dict[str, int]:
    out = {}
    for g in given or ():
        spec, n = (g, 1) if isinstance(g, str) else g
        out[spec] = n
    return out


def send(week_or_events, lose=(), delay=None, lose_ack=(), restamp=False, at_least_once=False) -> Delivery:
    """The week's events sent down the path, with the faults given, and what the collector received."""
    events = week_events(week_or_events) if isinstance(week_or_events, Week) else list(week_or_events)
    losses = {pick(events, s): n for s, n in _specs(lose).items()}
    holds = {pick(events, s): secs for s, secs in (delay or {}).items()}
    acks = {pick(events, s) for s in lose_ack}
    # `restamp` is True for every event sent again, or the specs of the events it applies to.
    restamped = set(range(len(events))) if restamp is True else {pick(events, s) for s in (restamp or ())}
    arrivals: list[Arrival] = []
    log: list[dict] = []
    lost: list[dict] = []
    for i, ev in enumerate(events):
        sent_at = epoch(_time(ev)) + SEND_LAG
        attempt, received, first, last = 0, 0, None, None
        while True:
            attempt += 1
            body = copy.deepcopy(ev)
            if attempt > 1 and i in restamped:
                body["eventTime"] = iso(sent_at)
            if losses.get(i, 0) >= attempt:
                outcome = "lost"
            else:
                arrived = sent_at + LATENCY + holds.get(i, 0)
                arrivals.append(Arrival(body, iso(sent_at), iso(arrived), attempt))
                received += 1
                first = first or iso(arrived)
                last = iso(arrived)
                outcome = "acknowledgement lost" if (i in acks and received == 1) else "acknowledged"
            if not at_least_once or outcome == "acknowledged":
                break
            sent_at += ACK_WAIT
        if not received:
            lost.append(ev)
        log.append({"event": describe(ev), "sendings": attempt, "received": received, "first arrival": first, "last arrival": last})
    arrivals.sort(key=lambda a: (epoch(a.arrived), a.sent))
    return Delivery(arrivals, Rows(log, null=""), at_least_once, lost)


def open_runs(events: list[dict], now: str) -> Rows:
    """The runs the collector has a START for and no end, at `now`: how long since each started, and
    how long the job's runs that did end usually took, in seconds."""
    runs: dict[str, dict] = {}
    for ev in events:
        r = runs.setdefault(ev["run"]["runId"], {"job": _job(ev), "started": None, "ended": None})
        if ev["eventType"] == "START":
            r["started"] = _time(ev)
        if ev["eventType"] in TERMINAL:
            r["ended"] = _time(ev)
    took: dict[str, list[float]] = {}
    for r in runs.values():
        if r["started"] and r["ended"]:
            took.setdefault(r["job"], []).append(epoch(r["ended"]) - epoch(r["started"]))
    out = []
    for r in runs.values():
        if r["started"] and not r["ended"]:
            usual = took.get(r["job"])
            out.append({
                "job": r["job"],
                "started": r["started"],
                "seconds since": int(epoch(now) - epoch(r["started"])),
                "usual seconds": int(median(usual)) if usual else None,
            })
    return Rows(out, null="", empty=MESSAGES["no_open"])


def repeated_work(events: list[dict]) -> Rows:
    """Function runs started more than once for the same change to the same version of an object, by
    the object facet each run's events carry."""
    seen: dict[tuple, list[str]] = {}
    for ev in events:
        if ev["eventType"] != "START":
            continue
        f = (ev["run"].get("facets") or {}).get(OBJECT_CHANGE)
        if not f:
            continue
        key = (f["object"], f["version"], f["change"])
        runs = seen.setdefault(key, [])
        if ev["run"]["runId"] not in runs:
            runs.append(ev["run"]["runId"])
    return Rows(
        ({"object": k[0], "version": k[1], "change": k[2], "runs": len(v)} for k, v in seen.items() if len(v) > 1),
        empty=MESSAGES["no_repeats"],
    )


def object_states(events: list[dict], order: str = "event") -> Rows:
    """Each object as the function runs' events leave it: its last change, taken by event time, or with
    `order="arrival"`, from the last event to arrive; and whether that leaves it existing."""
    starts = [e for e in events if e["eventType"] == "START" and OBJECT_CHANGE in (e["run"].get("facets") or {})]
    if order == "event":
        starts = sorted(starts, key=_time)
    last: dict[str, dict] = {}
    for e in starts:
        f = e["run"]["facets"][OBJECT_CHANGE]
        last[f["object"]] = {"object": f["object"], "last change": f["change"], "at": _time(e), "exists": "no" if f["change"] == "deleted" else "yes"}
    return Rows(sorted(last.values(), key=lambda r: r["object"]))


__all__ = ["object_states", "send", "pick", "describe", "week_events", "open_runs", "repeated_work", "SEND_LAG", "LATENCY", "ACK_WAIT"]
