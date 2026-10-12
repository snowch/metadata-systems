# Copyright © 2026 Christopher Snow

"""The shop's runs as OpenLineage run events, a check of an event against the specification's rules,
and a small consumer that accumulates events (Chapter 8).

What the OpenLineage specification requires, and where the course read it, is in `docs/sources.md`.
The specification's schema is not copied here: `check` holds an event to the rules the sources
record, in the course's own code, and `notebook/tests` checks that every event the shop produces
passes them. Everything else here is the shop's own choice and is labelled so: the namespaces of
its warehouse and its reporting tool, which the specification's naming page does not list; its
producer's address; the custom facet in which a function records the object change that started it;
and what the consumer does with an event.
"""

from __future__ import annotations

import copy
import hashlib
import json
import re
from datetime import datetime

from .graph import Graph
from .platform import Rows, epoch
from .runs import code_version, executions
from .week import FILES, RETURNS_BUCKET, STARTS, Week

SPEC = "https://openlineage.io/spec/2-0-2/OpenLineage.json"
SCHEMA_URL = f"{SPEC}#/$defs/RunEvent"
EVENT_TYPES = ("START", "RUNNING", "COMPLETE", "ABORT", "FAIL", "OTHER")

# The shop's own choices: who produced its events, and where its jobs and its warehouse live.
PRODUCER = "https://example.org/shop/jobs/tree/v1"
# The functions send their events through the function platform's own library, a second producer,
# which writes times with an offset (`+00:00`) where the jobs' producer writes `Z`.
FUNCTIONS_PRODUCER = "https://example.org/shop/functions/runtime/v2"
# The analyst's copy script, once it sends events (Chapter 9): a third producer, with its own names.
ANALYST_PRODUCER = "https://example.org/analyst/copy-script/v1"
ANALYST_NAMESPACE = "analyst"
JOB_NAMESPACE = "shop"
WAREHOUSE = "warehouse://shop-warehouse"
REPORTING = "reporting://shop-reporting"
REPOSITORY = "https://example.org/shop/repository"

# Each standard facet the shop uses, and the version of its schema (docs/sources.md).
FACETS = {
    "inputStatistics": ("1-0-0", "InputStatisticsInputDatasetFacet"),
    "outputStatistics": ("1-0-2", "OutputStatisticsOutputDatasetFacet"),
    "version": ("1-0-1", "DatasetVersionDatasetFacet"),
    "jobType": ("2-0-4", "JobTypeJobFacet"),
    "sourceCodeLocation": ("1-1-0", "SourceCodeLocationJobFacet"),
    "nominalTime": ("1-0-1", "NominalTimeRunFacet"),
}
# The shop's custom facet, named as the specification asks: a prefix, then the name.
OBJECT_CHANGE = "shop_objectChange"
OBJECT_CHANGE_SCHEMA = "https://example.org/shop/facets/1-0-0/ShopObjectChangeRunFacet.json#/$defs/ShopObjectChangeRunFacet"


def facet(name: str, producer: str = PRODUCER, **fields) -> dict:
    """A facet: the producer and the address of its schema, then its own fields."""
    if name == OBJECT_CHANGE:
        url = OBJECT_CHANGE_SCHEMA
    else:
        version, title = FACETS[name]
        url = f"https://openlineage.io/spec/facets/{version}/{title}.json#/$defs/{title}"
    return {"_producer": producer, "_schemaURL": url, **fields}


def dataset(uri: str) -> dict:
    """An asset as the shop's producer names it: a namespace, and a name inside it."""
    if uri.startswith("s3://"):
        bucket, _, key = uri[len("s3://") :].partition("/")
        return {"namespace": f"s3://{bucket}", "name": key}
    if uri == "sales_dashboard":
        return {"namespace": REPORTING, "name": uri}
    return {"namespace": WAREHOUSE, "name": f"shop.analytics.{uri}"}


def uuid7(at: str, seed: str) -> str:
    """A UUID of version 7: the run's start in milliseconds, then bits from a hash of `seed`.

    The specification recommends version 7 (docs/sources.md); the hash in place of random bits
    keeps the shop's identifiers the same on every machine.
    """
    ms = int(epoch(at) * 1000)
    h = int.from_bytes(hashlib.sha1(seed.encode()).digest()[:10], "big")
    rand_a = h >> 68 & 0xFFF
    rand_b = h & ((1 << 62) - 1)
    value = (ms << 80) | (0x7 << 76) | (rand_a << 64) | (0b10 << 62) | rand_b
    text = f"{value:032x}"
    return f"{text[:8]}-{text[8:12]}-{text[12:16]}-{text[16:20]}-{text[20:]}"


def run_events(week: Week) -> list[dict]:
    """Every run of the shop's programs in the week as OpenLineage run events: a START and a COMPLETE
    for each run that succeeded, a START and a FAIL for one that failed, in time order."""
    out = []
    for run, e in executions(week):
        producer = FUNCTIONS_PRODUCER if e.object else PRODUCER
        facet_ = lambda name, **fields: facet(name, producer, **fields)
        when = (lambda t: t.replace("Z", "+00:00")) if e.object else (lambda t: t)
        run_id = uuid7(e.started, f"{e.job}|{e.started}")
        version = code_version(e.code)
        folder = "functions" if e.object else "jobs"
        job = {
            "namespace": JOB_NAMESPACE,
            "name": e.job,
            "facets": {
                "jobType": facet_("jobType", processingType="BATCH", integration="SHOP", jobType="FUNCTION" if e.object else "JOB"),
                "sourceCodeLocation": facet_(
                    "sourceCodeLocation", type="git", url=f"{REPOSITORY}/blob/{version}/{folder}/{e.job}.py", version=version
                ),
            },
        }
        run_facets: dict = {}
        if e.night:
            run_facets["nominalTime"] = facet_("nominalTime", nominalStartTime=f"{e.night}T{STARTS[e.writer]}:00Z")
        if e.object:
            run_facets[OBJECT_CHANGE] = facet_(OBJECT_CHANGE, object=e.object, version=e.version, change=e.change)
        inputs = []
        for r in e.reads:
            d = dataset(r)
            if e.object and r == e.object:
                d["facets"] = {"version": facet_("version", datasetVersion=e.version)}
            inputs.append(d)
        start = {
            "eventType": "START",
            "eventTime": when(e.started),
            "run": {"runId": run_id, "facets": run_facets},
            "job": job,
            "inputs": inputs,
            "outputs": [],
            "producer": producer,
            "schemaURL": SCHEMA_URL,
        }
        finished = copy.deepcopy(start)
        finished["eventTime"] = when(e.finished)
        if e.status == "succeeded":
            finished["eventType"] = "COMPLETE"
            for d in finished["inputs"]:
                if e.rows_read is not None:
                    d["inputFacets"] = {"inputStatistics": facet_("inputStatistics", rowCount=e.rows_read)}
            out_ = dataset(e.wrote)
            if e.rows is not None:
                out_["outputFacets"] = {"outputStatistics": facet_("outputStatistics", rowCount=e.rows)}
            finished["outputs"] = [out_]
        else:
            finished["eventType"] = "FAIL"
        out += [start, finished]
    out.sort(key=lambda ev: epoch(ev["eventTime"].replace("+00:00", "Z")))
    return out


def analyst_events(week: Week) -> list[dict]:
    """The analyst's copy as its own script reports it, once it does (Chapter 9): a START and a
    COMPLETE each night, naming `clean_orders` its own way, with no database (`analytics.clean_orders`)."""
    out = []
    for e in week.executions:
        if e.writer != "analyst_copy":
            continue
        run_id = uuid7(e.started, f"copy|{e.started}")
        base = {
            "run": {"runId": run_id},
            "job": {"namespace": ANALYST_NAMESPACE, "name": "copy_clean_orders"},
            "inputs": [{"namespace": WAREHOUSE, "name": "analytics.clean_orders"}],
            "producer": ANALYST_PRODUCER,
            "schemaURL": SCHEMA_URL,
        }
        out.append({"eventType": "START", "eventTime": e.started, **copy.deepcopy(base), "outputs": []})
        done = {"eventType": "COMPLETE", "eventTime": e.finished, **copy.deepcopy(base)}
        done["outputs"] = [{**dataset(e.wrote), "outputFacets": {"outputStatistics": facet("outputStatistics", ANALYST_PRODUCER, rowCount=e.rows)}}]
        out.append(done)
    return out


def mapping() -> Rows:
    """Where each of Chapter 7's fields goes in the shop's OpenLineage run events."""
    return Rows(
        {"field": f, "in OpenLineage": place}
        for f, place in (
            ("run", "run.runId"),
            ("job", "job.namespace and job.name"),
            ("type", "eventType: START, or COMPLETE or FAIL"),
            ("time", "eventTime"),
            ("status", "eventType: COMPLETE or FAIL"),
            ("code_version", "job.facets.sourceCodeLocation.version"),
            ("reads", "inputs"),
            ("writes", "outputs"),
            ("rows_read", "inputs[].inputFacets.inputStatistics.rowCount"),
            ("rows_written", "outputs[].outputFacets.outputStatistics.rowCount"),
            ("object", f"run.facets.{OBJECT_CHANGE}.object"),
            ("object_version", f"run.facets.{OBJECT_CHANGE}.version, and inputs[].facets.version.datasetVersion"),
            ("object_change", f"run.facets.{OBJECT_CHANGE}.change"),
        )
    )


def summary(events: list[dict]) -> Rows:
    """Job by job: how many runs sent events, how many events of each type, and how many break the
    specification's rules."""
    out: dict[str, dict] = {}
    for e in events:
        key = f"{e['job']['namespace']}/{e['job']['name']}"
        row = out.setdefault(key, {"job": key, "runs": set(), "START": 0, "COMPLETE": 0, "FAIL": 0, "breaking a rule": 0})
        row["runs"].add(e["run"]["runId"])
        if e.get("eventType") in row:
            row[e["eventType"]] += 1
        if problems(e):
            row["breaking a rule"] += 1
    return Rows({**r, "runs": len(r["runs"])} for r in out.values())


def show(event: dict) -> str:
    """An event as indented JSON, for reading."""
    return json.dumps(event, indent=2)


# --- The specification's rules, as docs/sources.md records them -------------------------------

_UUID = re.compile(r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$")
_URI = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:\S+$")

MESSAGES = {
    'missing': 'Every run event needs this field, and the event does not have it.',
    'event_type': 'The event type is not one of `START`, `RUNNING`, `COMPLETE`, `ABORT`, `FAIL` or `OTHER`.',
    'run_id': "The run's identifier is not a UUID.",
    'time': 'The time is not a date and time in the form `2026-09-11T02:15:00Z`.',
    'uri': 'The value is not an address with a scheme, such as `https:`.',
    'facet': 'Every facet needs `_producer` and `_schemaURL`, and this facet lacks this one.',
    'not_object': 'This should be an object, with fields inside braces.',
    'none': "The event breaks none of the specification's rules that the check tests.",
}


def _date_time(value) -> bool:
    if not isinstance(value, str) or not re.match(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?(Z|[+-]\d{2}:\d{2})$", value):
        return False
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return False
    return True


def problems(event) -> list[tuple[str, str]]:
    """Each place where a run event breaks the specification's rules, as (where, kind)."""
    found: list[tuple[str, str]] = []
    if not isinstance(event, dict):
        return [("event", "not_object")]
    for key in ("eventTime", "producer", "schemaURL", "run", "job"):
        if key not in event:
            found.append((key, "missing"))
    if "eventType" in event and event["eventType"] not in EVENT_TYPES:
        found.append(("eventType", "event_type"))
    if "eventTime" in event and not _date_time(event["eventTime"]):
        found.append(("eventTime", "time"))
    for key in ("producer", "schemaURL"):
        if key in event and not (isinstance(event[key], str) and _URI.match(event[key])):
            found.append((key, "uri"))
    run = event.get("run")
    if "run" in event:
        if not isinstance(run, dict):
            found.append(("run", "not_object"))
        elif "runId" not in run:
            found.append(("run.runId", "missing"))
        elif not (isinstance(run["runId"], str) and _UUID.match(run["runId"])):
            found.append(("run.runId", "run_id"))
    things = [("job", event.get("job"))] if "job" in event else []
    for side in ("inputs", "outputs"):
        for k, d in enumerate(event.get(side) or []):
            things.append((f"{side}[{k}]", d))
    for where, thing in things:
        if not isinstance(thing, dict):
            found.append((where, "not_object"))
            continue
        for key in ("namespace", "name"):
            if key not in thing:
                found.append((f"{where}.{key}", "missing"))
    facet_groups = []
    if isinstance(run, dict):
        facet_groups.append(("run.facets", run.get("facets")))
    if isinstance(event.get("job"), dict):
        facet_groups.append(("job.facets", event["job"].get("facets")))
    for where, thing in things[1:] if "job" in event else things:
        if isinstance(thing, dict):
            for group in ("facets", "inputFacets", "outputFacets"):
                facet_groups.append((f"{where}.{group}", thing.get(group)))
    for where, group in facet_groups:
        for name, f in (group or {}).items():
            if not isinstance(f, dict):
                found.append((f"{where}.{name}", "not_object"))
                continue
            for key in ("_producer", "_schemaURL"):
                if key not in f:
                    found.append((f"{where}.{name}.{key}", "facet"))
                elif not (isinstance(f[key], str) and _URI.match(f[key])):
                    found.append((f"{where}.{name}.{key}", "uri"))
    return found


def check(event) -> Rows:
    """What breaks the specification's rules in an event, one row per problem."""
    return Rows(({"where": w, "problem": MESSAGES[k]} for w, k in problems(event)), empty=MESSAGES["none"])


# --- A small consumer: the shop's own -----------------------------------------------------------

TERMINAL = ("COMPLETE", "ABORT", "FAIL")


def _key(d: dict) -> str:
    """A dataset as the consumer keys it: its namespace and its name, exactly as the event wrote them."""
    return f"{d['namespace']}/{d['name']}"


class Consumer:
    """Accumulates run events, run by run, as the shop's consumer does.

    It keys a run by its `runId` and a dataset by its namespace and name exactly as written. Each
    event adds to what the consumer knows of its run: inputs and outputs are added to the run's,
    and a facet replaces the facet of the same name (docs/sources.md). It takes the run's state
    from the latest event it received. It refuses an event that breaks the specification's rules.
    """

    def __init__(self) -> None:
        self._runs: dict[str, dict] = {}
        self.refused: list[dict] = []

    def send(self, *events: dict) -> "Consumer":
        for event in events:
            if problems(event):
                self.refused.append(event)
                continue
            run_id = event["run"]["runId"]
            r = self._runs.setdefault(
                run_id,
                {"run": run_id, "job": f"{event['job']['namespace']}/{event['job']['name']}", "events": 0,
                 "state": None, "started": None, "ended": None, "inputs": [], "outputs": [], "facets": {}},
            )
            r["events"] += 1
            r["state"] = event.get("eventType", r["state"])
            if event.get("eventType") == "START":
                r["started"] = event["eventTime"]
            if event.get("eventType") in TERMINAL:
                r["ended"] = event["eventTime"]
            for side in ("inputs", "outputs"):
                for d in event.get(side) or []:
                    if _key(d) not in r[side]:
                        r[side].append(_key(d))
            r["facets"].update(event["run"].get("facets") or {})
        return self

    def runs(self, state: str | None = None) -> Rows:
        """What the consumer knows of each run; with `state`, only the runs in that state."""
        return Rows(
            (
                {
                    "job": r["job"],
                    "state": r["state"],
                    "started": r["started"],
                    "ended": r["ended"],
                    "inputs": ", ".join(r["inputs"]),
                    "outputs": ", ".join(r["outputs"]),
                    "events": r["events"],
                }
                for r in self._runs.values()
                if state is None or r["state"] == state
            ),
            null="",
        )

    def lineage(self) -> Graph:
        """Every job and dataset the runs name, with `reads` and `writes` edges: datasets joined
        only where two events name them with the same namespace and name."""
        nodes: list[tuple[str, str]] = []
        edges: list = []
        for r in self._runs.values():
            j = ("job", r["job"])
            if j not in nodes:
                nodes.append(j)
            for side, attribute in (("inputs", "reads"), ("outputs", "writes")):
                for key in r[side]:
                    n = ("dataset", key)
                    if n not in nodes:
                        nodes.append(n)
                    if (j, attribute, n) not in edges:
                        edges.append((j, attribute, n))
        g = object.__new__(Graph)
        g._nodes = sorted(nodes)
        g._edges = edges
        return g


__all__ = ["run_events", "analyst_events", "mapping", "summary", "check", "problems", "Consumer", "dataset", "uuid7", "show", "PRODUCER", "SCHEMA_URL"]
