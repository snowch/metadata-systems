# Copyright © 2026 Christopher Snow

"""A second platform: an island ferry's ticket gates, functions, scheduled jobs and tables (Chapter 33).

The ferry crosses between the mainland and the island, three times a day from each side, Tuesday 22
to Thursday 24 September 2026. Its platform is built another way from the shop's:

- **Object storage** (the shop's `ObjectStorage`, which keeps every version and a delete marker).
  Each harbour has two ticket gates; a minute after each departure, each gate uploads the sailing's
  scans as one object, `s3://ferry-gates/{harbour}/{date}/{HHMM}/gate-{n}.jsonl`, one scan per line
  (`ticket`, `fare`, `scanned_at`).
- **Functions.** Two seconds after each change to an object in `ferry-gates`, the function platform
  starts `load_scans` (a create or an overwrite: it replaces the batch's rows in `boardings`, keeping
  only scans with a `scanned_at`, since the gates' firmware writes an aborted scan with no time) or
  `drop_scans` (a delete: it removes the batch's rows and reads nothing). The platform records its
  triggers and a log of its invocations: when, which function, which object and version, finished.
- **The warehouse** (SQLite): `sailings`, the timetable, typed in by hand before the week, which no
  job writes; `boardings`; `sailing_loads`.
- **The scheduler.** `build_loads` at 01:00 rebuilds the day before's rows of `sailing_loads` from
  `boardings` and `sailings`; `send_report` at 06:00 writes the day before's loads to
  `s3://ferry-reports/loads-{date}.csv`, which the harbour masters get by email. The scheduler
  records each run's start, end and status.

Three things go wrong (`docs/notes/part-8/design.md`): Tuesday's 17:30 from the mainland, gate 2,
uploads 3 scans short and again in full at 07:05 on Wednesday, after the build; an engineer's test
batch of 5 scans lands under Wednesday's 19:30 from the island at 23:40 and is deleted at 08:30 on
Thursday, after the build and the report; and from noon on Thursday the island's gate 2 writes
`scan_time` for `scanned_at`, so `load_scans` keeps none of its scans and finishes as usual. One batch,
Wednesday's 12:30 from the mainland, gate 1, holds an aborted scan with no time.

The functions' and jobs' OpenLineage run events (`events`) are built with the learner's
`inputs(change)` for the functions' inputs; the rest of each event is the ferry's. The events go
through the shop's collector and lineage graph, with Part VI's reference pieces.

Every rule, name, time and number here is the course's own. No real object store, function platform
or scheduler is described.
"""

from __future__ import annotations

import copy
import json

from . import collector, lineage_graph
from .openlineage import SCHEMA_URL, problems, uuid7
from .platform import ObjectStorage, Rows, epoch, iso

DAYS = ("2026-09-22", "2026-09-23", "2026-09-24")
DAY_NAMES = {"2026-09-22": "Tuesday 22", "2026-09-23": "Wednesday 23", "2026-09-24": "Thursday 24", "2026-09-25": "Friday 25"}
DEPARTURES = {"mainland": ("07:30", "12:30", "17:30"), "island": ("09:30", "14:30", "19:30")}
GATES = ("gate-1", "gate-2")
CAPACITY = 60
ASKED = "2026-09-25T09:00:00Z"

GATES_BUCKET = "s3://ferry-gates"
REPORTS_BUCKET = "s3://ferry-reports"
WAREHOUSE = "warehouse://ferry-warehouse"
JOBS = "ferry"
FUNCTIONS_PRODUCER = "https://example.org/ferry/functions/runtime/v1"
JOBS_PRODUCER = "https://example.org/ferry/scheduler/v1"
CHANGE_FACET = "ferry_batchChange"
CHANGE_SCHEMA = "https://example.org/ferry/facets/1-0-0/FerryBatchChangeRunFacet.json#/$defs/FerryBatchChangeRunFacet"

# Scans per gate at each departure, before the day's own difference (`_scans`).
BASE = {
    ("mainland", "07:30"): (18, 14), ("mainland", "12:30"): (11, 9), ("mainland", "17:30"): (21, 17),
    ("island", "09:30"): (16, 13), ("island", "14:30"): (12, 10), ("island", "19:30"): (8, 7),
}
SHORT = ("2026-09-22", "mainland", "17:30", "gate-2")
SHORT_BY = 3
RESENT_AT = "2026-09-23T07:05:00Z"
TEST_KEY = "island/2026-09-23/1930/gate-1-test.jsonl"
TEST_SCANS = 5
TEST_AT = "2026-09-23T23:40:00Z"
TEST_DELETED_AT = "2026-09-24T08:30:00Z"
FIRMWARE = ("2026-09-24", "island", "gate-2", "12:00")
ABORTED = ("2026-09-23", "mainland", "12:30", "gate-1")

LOAD_SCANS = """DELETE FROM boardings WHERE batch = :batch;
INSERT INTO boardings (sailing, ticket, fare, scanned_at, batch)
SELECT :sailing, ticket, fare, scanned_at, :batch FROM scans WHERE scanned_at IS NOT NULL"""
DROP_SCANS = "DELETE FROM boardings WHERE batch = :batch"
BUILD_LOADS = """DELETE FROM sailing_loads WHERE date = :day;
INSERT INTO sailing_loads (sailing, date, harbour, departs, passengers, capacity)
SELECT s.sailing, s.date, s.harbour, s.departs, COUNT(b.ticket), s.capacity
FROM sailings AS s LEFT JOIN boardings AS b ON b.sailing = s.sailing
WHERE s.date = :day GROUP BY s.sailing ORDER BY s.departs"""

MESSAGES = {
    "summary": "{passed} of {total} tests pass.",
    "valid": "Every event passes Chapter 8's check.",
    "valid_no": "{n} events break the rules Chapter 8's check tests, the first at `{where}`.",
    "versions": "Each run started by a create or an overwrite names the version of the batch it read.",
    "versions_no": "{n} of {total} runs started by a create or an overwrite do not name the version of the batch they read.",
    "deleted": "The run started by the delete of the test batch names the batch and the version it removed.",
    "deleted_no": "The run started by the delete of the test batch names {got}; the version it removed is `{want}`.",
    "nothing": "nothing",
    "thursday": "Both of Thursday's runs on the island's gate 2 after noon are flagged.",
    "thursday_no": "{n} of Thursday's 2 runs on the island's gate 2 after noon are flagged.",
    "others": "No other run is flagged.",
    "others_no": "Also flagged: {runs}.",
    "error": "`{name}` raised {error}.",
    "not_recorded": "not recorded",
    "still": "yes",
    "gone": "no",
}


def sailing_id(day: str, harbour: str, departs: str) -> str:
    return f"{day} {harbour} {departs}"


def _at(day: str, hhmm: str, plus: int = 0) -> str:
    return iso(epoch(f"{day}T{hhmm}:00Z") + plus)


def _scans(day: str, harbour: str, departs: str, gate: str) -> list[dict]:
    """A gate's scans for one departure, as its firmware writes them."""
    d = DAYS.index(day)
    g1, g2 = BASE[(harbour, departs)]
    n = (g1 + d) if gate == "gate-1" else (g2 + d % 2)
    renamed = (day, harbour, gate) == FIRMWARE[:3] and departs >= FIRMWARE[3]
    out = []
    for i in range(n):
        fare = "child" if i % 6 == 5 else ("vehicle" if i % 9 == 8 else "adult")
        scan = {"ticket": f"{harbour[0].upper()}{day[8:10]}{departs.replace(':', '')}-{gate[-1]}-{i + 1:02d}", "fare": fare}
        scan["scan_time" if renamed else "scanned_at"] = _at(day, departs, -1800 + 60 * i)
        out.append(scan)
    if (day, harbour, departs, gate) == ABORTED:
        out.insert(4, {"ticket": f"{harbour[0].upper()}{day[8:10]}{departs.replace(':', '')}-{gate[-1]}-xx", "fare": "adult", "scanned_at": None})
    return out


def _jsonl(scans: list[dict]) -> str:
    return "".join(json.dumps(s, separators=(",", ":")) + "\n" for s in scans)


def _key(harbour: str, day: str, departs: str, gate: str) -> str:
    return f"{harbour}/{day}/{departs.replace(':', '')}/{gate}.jsonl"


def _sailing_of(key: str) -> str:
    harbour, day, hhmm, _ = key.split("/")
    return sailing_id(day, harbour, f"{hhmm[:2]}:{hhmm[2:]}")


class Functions:
    """The function platform: its triggers, and a log of every invocation."""

    def __init__(self) -> None:
        self._log: list[dict] = []

    def triggers(self) -> Rows:
        return Rows([
            {"function": "load_scans", "starts when": f"an object in `{GATES_BUCKET}` is created or overwritten"},
            {"function": "drop_scans", "starts when": f"an object in `{GATES_BUCKET}` is deleted"},
        ])

    def log(self, prefix: str = "") -> Rows:
        """Each invocation the platform logged: when, which function, which object and version, how it ended."""
        return Rows([{k: r[k] for k in ("started", "function", "object", "version", "status")} for r in self._log if r["object"].startswith(prefix)])


class Scheduler:
    def __init__(self) -> None:
        self._runs: list[dict] = []

    def schedule(self) -> Rows:
        return Rows([{"job": "build_loads", "runs": "every day at 01:00"}, {"job": "send_report", "runs": "every day at 06:00"}])

    def runs(self, job: str | None = None) -> Rows:
        return Rows([{k: r[k] for k in ("job", "started", "finished", "status")} for r in self._runs if job in (None, r["job"])])


class Warehouse:
    """The ferry's tables, in SQLite."""

    def __init__(self) -> None:
        import sqlite3

        self.db = sqlite3.connect(":memory:")
        self.db.executescript(
            """CREATE TABLE sailings (sailing TEXT, date TEXT, harbour TEXT, departs TEXT, capacity INTEGER);
               CREATE TABLE boardings (sailing TEXT, ticket TEXT, fare TEXT, scanned_at TEXT, batch TEXT);
               CREATE TABLE sailing_loads (sailing TEXT, date TEXT, harbour TEXT, departs TEXT, passengers INTEGER, capacity INTEGER);"""
        )
        self.altered: dict[str, str] = {}

    def sql(self, query: str, **params) -> Rows:
        cur = self.db.execute(query, params)
        cols = [c[0] for c in cur.description]
        return Rows([dict(zip(cols, r)) for r in cur.fetchall()])

    def tables(self) -> Rows:
        return Rows(
            {"table": t, "rows": self.db.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0], "last altered": self.altered.get(t)}
            for t in ("sailings", "boardings", "sailing_loads")
        )


class Ferry:
    """The ferry's platform after the three days, as the data team finds it on Friday 25 at 09:00."""

    def __init__(self) -> None:
        self.storage = ObjectStorage()
        self.functions = Functions()
        self.warehouse = Warehouse()
        self.scheduler = Scheduler()
        self.changes: list[dict] = []
        self.loads_built: dict[str, dict[str, int]] = {}

    def _change(self, key: str, text: str | None, at: str) -> None:
        uri = f"{GATES_BUCKET}/{key}"
        previous = [v["version"] for v in self.storage._versions.get(uri, []) if not v["deleted"]]
        existed = self.storage.exists(uri)
        version = self.storage.put(uri, text, at) if text is not None else self.storage.delete(uri, at)
        kind = "deleted" if text is None else ("overwritten" if existed else "created")
        started = iso(epoch(at) + 2)
        change = {"key": key, "change": kind, "version": version, "previous": previous[-1] if previous else None, "at": at, "started": started}
        db = self.warehouse.db
        if kind == "deleted":
            removed = db.execute(DROP_SCANS, {"batch": key}).rowcount
            change.update(function="drop_scans", scans_read=0, rows_written=removed, fields=[])
        else:
            lines = [json.loads(l) for l in text.splitlines() if l]
            fields = sorted({k for s in lines for k in s})
            db.execute("CREATE TEMP TABLE scans (ticket TEXT, fare TEXT, scanned_at TEXT)")
            db.executemany("INSERT INTO scans VALUES (?, ?, ?)", [(s.get("ticket"), s.get("fare"), s.get("scanned_at")) for s in lines])
            first, second = LOAD_SCANS.split(";\n")
            db.execute(first, {"batch": key})
            written = db.execute(second, {"batch": key, "sailing": _sailing_of(key)}).rowcount
            db.execute("DROP TABLE temp.scans")
            change.update(function="load_scans", scans_read=len(lines), rows_written=written, fields=fields)
        db.commit()
        change["finished"] = iso(epoch(started) + 1)
        self.warehouse.altered["boardings"] = change["finished"]
        self.changes.append(change)
        self.functions._log.append({"started": started, "function": change["function"], "object": f"{GATES_BUCKET}/{key}", "version": version, "status": "finished"})

    def _job(self, job: str, day: str, at: str) -> None:
        db = self.warehouse.db
        finished = iso(epoch(at) + (4 if job == "build_loads" else 2))
        if job == "build_loads":
            first, second = BUILD_LOADS.split(";\n")
            db.execute(first, {"day": day})
            written = db.execute(second, {"day": day}).rowcount
            self.warehouse.altered["sailing_loads"] = finished
            self.loads_built[day] = {r["sailing"]: r["passengers"] for r in self.warehouse.sql("SELECT sailing, passengers FROM sailing_loads WHERE date = :d", d=day)}
            reads, writes = ["boardings", "sailings"], f"{WAREHOUSE}|ferry.sailing_loads"
        else:
            rows = self.warehouse.sql("SELECT sailing, passengers, capacity FROM sailing_loads WHERE date = :d ORDER BY departs, harbour", d=day)
            text = "sailing,passengers,capacity\n" + "".join(f"{r['sailing']},{r['passengers']},{r['capacity']}\n" for r in rows)
            self.storage.put(f"{REPORTS_BUCKET}/loads-{day}.csv", text, finished)
            written = len(rows)
            reads, writes = ["sailing_loads"], f"{REPORTS_BUCKET}|loads-{day}.csv"
        db.commit()
        self.scheduler._runs.append({"job": job, "day": day, "started": at, "finished": finished, "status": "succeeded", "rows": written, "reads": reads, "writes": writes})

    def report(self, day: str) -> Rows:
        """The morning report for one day's sailings, as the harbour masters got it."""
        from .platform import parse

        return parse(f"{REPORTS_BUCKET}/loads-{day}.csv", self.storage.read_text(f"{REPORTS_BUCKET}/loads-{day}.csv"))


def run() -> Ferry:
    """The ferry's three days, from the timetable to Friday morning's report."""
    f = Ferry()
    db = f.warehouse.db
    for day in DAYS:
        for harbour, times in DEPARTURES.items():
            for t in times:
                db.execute("INSERT INTO sailings VALUES (?, ?, ?, ?, ?)", (sailing_id(day, harbour, t), day, harbour, t, CAPACITY))
    db.commit()
    f.warehouse.altered["sailings"] = "2026-09-18T16:20:00Z"
    happenings: list[tuple[str, str, object]] = []
    for day in DAYS:
        for harbour, times in DEPARTURES.items():
            for t in times:
                for gate in GATES:
                    scans = _scans(day, harbour, t, gate)
                    key = _key(harbour, day, t, gate)
                    at = _at(day, t, 60)
                    if (day, harbour, t, gate) == SHORT:
                        happenings.append((at, "object", (key, _jsonl(scans[:-SHORT_BY]))))
                        happenings.append((RESENT_AT, "object", (key, _jsonl(scans))))
                    else:
                        happenings.append((at, "object", (key, _jsonl(scans))))
    test = [{"ticket": f"TEST-{i + 1}", "fare": "adult", "scanned_at": iso(epoch(TEST_AT) - 60 * (TEST_SCANS - i))} for i in range(TEST_SCANS)]
    happenings.append((TEST_AT, "object", (TEST_KEY, _jsonl(test))))
    happenings.append((TEST_DELETED_AT, "object", (TEST_KEY, None)))
    for i, day in enumerate(DAYS):
        nxt = iso(epoch(f"{day}T00:00:00Z") + 86400)[:10]
        happenings.append((f"{nxt}T01:00:00Z", "job", ("build_loads", day)))
        happenings.append((f"{nxt}T06:00:00Z", "job", ("send_report", day)))
    for at, kind, what in sorted(happenings, key=lambda h: (epoch(h[0]), h[1])):
        if kind == "object":
            f._change(what[0], what[1], at)
        else:
            f._job(what[0], what[1], at)
    return f


# What the harbour masters counted on board, sailing by sailing: independent of the gates and the
# warehouse. Every scan a gate made, the test batch's excepted.
def harbour_counts(day: str, harbour: str) -> Rows:
    out = []
    for t in DEPARTURES[harbour]:
        n = sum(1 for g in GATES for s in _scans(day, harbour, t, g) if s.get("scanned_at") or s.get("scan_time"))
        out.append({"sailing": sailing_id(day, harbour, t), "counted on board": n})
    return Rows(out)


def compare_counts(f: Ferry, day: str, harbour: str) -> Rows:
    """`sailing_loads` beside the harbour master's own count, for one day's departures from one side."""
    loads = {r["sailing"]: r["passengers"] for r in f.warehouse.sql("SELECT sailing, passengers FROM sailing_loads")}
    return Rows({"sailing": r["sailing"], "sailing_loads": loads.get(r["sailing"]), "counted on board": r["counted on board"]} for r in harbour_counts(day, harbour))


def platform() -> Rows:
    """The ferry's platform part by part, and what each system records about its own work."""
    return Rows([
        {"system": "object storage", "part": f"`{GATES_BUCKET}`, `{REPORTS_BUCKET}`", "records": "each object's key, size, time, and every version, with a marker where one was deleted"},
        {"system": "functions", "part": "`load_scans`, `drop_scans`", "records": "each trigger, and each invocation: when, which object and version, and that it finished"},
        {"system": "warehouse", "part": "`sailings`, `boardings`, `sailing_loads`", "records": "each table's columns, rows and last change"},
        {"system": "scheduler", "part": "`build_loads` at 01:00, `send_report` at 06:00", "records": "each run's start, end and status"},
    ])


# --- events -------------------------------------------------------------------------------------


def _facet(producer: str, schema: str, **fields) -> dict:
    return {"_producer": producer, "_schemaURL": schema, **fields}


def version_facet(version: str) -> dict:
    """OpenLineage's `version` dataset facet, as the ferry's function platform writes it."""
    return _facet(FUNCTIONS_PRODUCER, "https://openlineage.io/spec/facets/1-0-1/DatasetVersionDatasetFacet.json#/$defs/DatasetVersionDatasetFacet", datasetVersion=version)


def _schema_facet(fields: list[str]) -> dict:
    return _facet(
        FUNCTIONS_PRODUCER,
        "https://openlineage.io/spec/facets/1-2-0/SchemaDatasetFacet.json#/$defs/SchemaDatasetFacet",
        fields=[{"name": n, "type": "string"} for n in fields],
    )


def _table(name: str) -> dict:
    return {"namespace": WAREHOUSE, "name": f"ferry.{name}"}


def _run_event(kind: str, job: str, run_id: str, at: str, producer: str, inputs: list, outputs: list, facets: dict | None = None) -> dict:
    return {
        "eventType": kind,
        "eventTime": at,
        "run": {"runId": run_id, "facets": facets or {}},
        "job": {"namespace": JOBS, "name": job},
        "inputs": inputs,
        "outputs": outputs,
        "producer": producer,
        "schemaURL": SCHEMA_URL,
    }


def change_record(c: dict) -> dict:
    """What the learner's `inputs` is given: the object change that started a function."""
    return {"bucket": GATES_BUCKET, "key": c["key"], "change": c["change"], "version": c["version"], "previous": c["previous"], "at": c["at"]}


def events(f: Ferry, inputs) -> list[dict]:
    """Every run of the ferry's functions and jobs as OpenLineage run events, a START and a COMPLETE
    each, in time order. A function's inputs are `inputs(change)`, with the ferry's statistics and
    the batch's fields added to its own batch where it names it; the rest is the ferry's."""
    out = []
    for c in f.changes:
        run_id = uuid7(c["started"], f"{c['function']}|{c['key']}|{c['started']}")
        got = inputs(change_record(c))
        facets = {CHANGE_FACET: _facet(FUNCTIONS_PRODUCER, CHANGE_SCHEMA, change=c["change"])}
        start = _run_event("START", c["function"], run_id, c["started"], FUNCTIONS_PRODUCER, copy.deepcopy(got), [], facets)
        done_inputs = copy.deepcopy(got)
        for d in done_inputs if isinstance(done_inputs, list) else []:
            if isinstance(d, dict) and d.get("namespace") == GATES_BUCKET and d.get("name") == c["key"] and c["function"] == "load_scans":
                d.setdefault("facets", {})["schema"] = _schema_facet(c["fields"])
                d["inputFacets"] = {"inputStatistics": _facet(FUNCTIONS_PRODUCER, "https://openlineage.io/spec/facets/1-0-0/InputStatisticsInputDatasetFacet.json#/$defs/InputStatisticsInputDatasetFacet", rowCount=c["scans_read"])}
        out_ = _table("boardings")
        if c["function"] == "load_scans":
            out_["outputFacets"] = {"outputStatistics": _facet(FUNCTIONS_PRODUCER, "https://openlineage.io/spec/facets/1-0-2/OutputStatisticsOutputDatasetFacet.json#/$defs/OutputStatisticsOutputDatasetFacet", rowCount=c["rows_written"])}
        done = _run_event("COMPLETE", c["function"], run_id, c["finished"], FUNCTIONS_PRODUCER, done_inputs, [out_], facets)
        out += [start, done]
    for r in f.scheduler._runs:
        run_id = uuid7(r["started"], f"{r['job']}|{r['day']}")
        ins = [_table(t) for t in r["reads"]]
        ns, name = r["writes"].split("|")
        o = {"namespace": ns, "name": name}
        o["outputFacets"] = {"outputStatistics": _facet(JOBS_PRODUCER, "https://openlineage.io/spec/facets/1-0-2/OutputStatisticsOutputDatasetFacet.json#/$defs/OutputStatisticsOutputDatasetFacet", rowCount=r["rows"])}
        facets = {"nominalTime": _facet(JOBS_PRODUCER, "https://openlineage.io/spec/facets/1-0-1/NominalTimeRunFacet.json#/$defs/NominalTimeRunFacet", nominalStartTime=r["started"])}
        out.append(_run_event("START", r["job"], run_id, r["started"], JOBS_PRODUCER, ins, [], facets))
        out.append(_run_event("COMPLETE", r["job"], run_id, r["finished"], JOBS_PRODUCER, copy.deepcopy(ins), [o], facets))
    out.sort(key=lambda e: (epoch(e["eventTime"]), e["eventType"] != "START"))
    return out


class Checked(Rows):
    def __init__(self, rows) -> None:
        super().__init__(rows)
        self.passed = sum(r["passes"] == "yes" for r in rows)

    def _repr_html_(self) -> str:
        return f"<p>{MESSAGES['summary'].format(passed=self.passed, total=len(self))}</p>" + super()._repr_html_()


def _version_of(inputs_got, key: str):
    for d in inputs_got if isinstance(inputs_got, list) else []:
        if isinstance(d, dict) and d.get("namespace") == GATES_BUCKET and d.get("name") == key:
            return ((d.get("facets") or {}).get("version") or {}).get("datasetVersion", MESSAGES["not_recorded"])
    return None


def check_inputs(f: Ferry, inputs) -> Checked:
    """The learner's `inputs` for every object change of the three days."""
    try:
        evs = events(f, inputs)
    except Exception as e:  # the learner's code
        return Checked([{"test": MESSAGES["error"].format(name="inputs", error=f"{type(e).__name__}: {e}"), "passes": "no"}])
    broken = [(ev, problems(ev)) for ev in evs if problems(ev)]
    rows = [{
        "test": MESSAGES["valid"] if not broken else MESSAGES["valid_no"].format(n=len(broken), where=broken[0][1][0][0]),
        "passes": "no" if broken else "yes",
    }]
    loads = [c for c in f.changes if c["change"] != "deleted"]
    missing = [c for c in loads if _version_of(inputs(change_record(c)), c["key"]) != c["version"]]
    rows.append({
        "test": MESSAGES["versions"] if not missing else MESSAGES["versions_no"].format(n=len(missing), total=len(loads)),
        "passes": "no" if missing else "yes",
    })
    [delete] = [c for c in f.changes if c["change"] == "deleted"]
    got = _version_of(inputs(change_record(delete)), delete["key"])
    ok = got == delete["previous"]
    rows.append({
        "test": MESSAGES["deleted"] if ok else MESSAGES["deleted_no"].format(
            got=MESSAGES["nothing"] if got is None else (f"the batch, with its version {got}" if got == MESSAGES["not_recorded"] else f"the batch, with the version `{got}`"),
            want=delete["previous"],
        ),
        "passes": "yes" if ok else "no",
    })
    return Checked(rows)


def one_event(f: Ferry, inputs, change: str) -> dict:
    """The COMPLETE event of the first function run started by a change of this kind."""
    evs = events(f, inputs)
    return next(e for e in evs if e["eventType"] == "COMPLETE" and (e["run"]["facets"].get(CHANGE_FACET) or {}).get("change") == change)


# --- collecting, the graph and the questions -------------------------------------------------------


def collect(evs: list[dict]) -> collector.Collector:
    """The events through the shop's collector, with Part VI's reference pieces, each arriving 3
    seconds after its event time."""
    ns: dict = {}
    for piece in ("key", "newer", "start"):
        exec(collector.REFERENCE[piece], ns)
    c = collector.Collector(ns["key"], ns["newer"], ns["start"])
    for ev in evs:
        c.receive(copy.deepcopy(ev), iso(epoch(ev["eventTime"]) + 3))
    return c


def graph(c: collector.Collector) -> dict:
    """The lineage graph from the collector's file, built by Part VI's reference `add`."""
    ns: dict = {"shop": __import__("shop")}
    exec(lineage_graph.REFERENCE["add"], ns)
    g: dict = {}
    for ev in c.file:
        ns["add"](g, copy.deepcopy(ev))
    return g


def short(name: str) -> str:
    for prefix in (f"{WAREHOUSE}/ferry.", f"{GATES_BUCKET}/", f"{REPORTS_BUCKET}/", f"{JOBS}/"):
        if name.startswith(prefix):
            return name[len(prefix):]
    return name


def edges(g: dict, batches: bool = False) -> Rows:
    """The graph's edges by job, the batches folded into one row per job and edge unless `batches`."""
    rows: dict = {}
    for (j, e, d), v in sorted(g.items()):
        name = short(d)
        if not batches and d.startswith(GATES_BUCKET + "/"):
            name = f"{GATES_BUCKET}/... ({{n}})"
        r = rows.setdefault((short(j), e, name), {"job": short(j), "edge": e, "dataset": name, "runs": set(), "n": set()})
        r["runs"] |= v["runs"]
        r["n"].add(d)
    def named(r):
        n = len(r["n"])
        return r["dataset"].format(n=f"{n} batch" if n == 1 else f"{n} batches")

    return Rows({"job": r["job"], "edge": r["edge"], "dataset": named(r), "runs": len(r["runs"])} for r in rows.values())


def runs(c: collector.Collector) -> Rows:
    """Each run of `load_scans` in the collector's file, with what it measured: its batch, the
    version it read, its state, the scans it read, the rows it wrote and the batch's fields."""
    out: dict = {}
    for ev in c.file:
        if ev["job"]["name"] != "load_scans":
            continue
        r = out.setdefault(ev["run"]["runId"], {"batch": None, "version": None, "state": None, "scans_read": None, "rows_written": None, "fields": []})
        r["state"] = ev["eventType"]
        for d in ev.get("inputs") or []:
            if d.get("namespace") == GATES_BUCKET:
                r["batch"] = d["name"]
                r["version"] = ((d.get("facets") or {}).get("version") or {}).get("datasetVersion", r["version"])
                stats = (d.get("inputFacets") or {}).get("inputStatistics")
                if stats:
                    r["scans_read"] = stats["rowCount"]
                schema = (d.get("facets") or {}).get("schema")
                if schema:
                    r["fields"] = [x["name"] for x in schema["fields"]]
        for d in ev.get("outputs") or []:
            stats = (d.get("outputFacets") or {}).get("outputStatistics")
            if stats:
                r["rows_written"] = stats["rowCount"]
        r["started"] = r.get("started") or ev["eventTime"]
    return Rows(sorted(({"started": r.pop("started"), **r} for r in out.values()), key=lambda r: r["started"]), null="")


def run_states(c: collector.Collector) -> Rows:
    """Each job's runs in the collector's file, by the state each run ended in."""
    last: dict = {}
    for ev in c.file:
        last[ev["run"]["runId"]] = (ev["job"]["name"], ev["eventType"])
    out: dict = {}
    for job, state in last.values():
        r = out.setdefault(job, {"job": job, "runs": 0, "COMPLETE": 0, "FAIL": 0})
        r["runs"] += 1
        if state in ("COMPLETE", "FAIL"):
            r[state] += 1
    return Rows(sorted(out.values(), key=lambda r: r["job"]))


def _flagged_label(r: dict) -> str:
    harbour, day, hhmm, gate = r["batch"].split("/")
    return f"{DAY_NAMES[day].split()[0]}'s {hhmm[:2]}:{hhmm[2:]} from the {harbour}, {gate.removesuffix('.jsonl').replace('-', ' ')}"


def check_suspect(c: collector.Collector, suspect) -> Checked:
    """The learner's `suspect(run)` over every run of `load_scans`."""
    try:
        flagged = [r for r in runs(c) if suspect(dict(r))]
    except Exception as e:  # the learner's code
        return Checked([{"test": MESSAGES["error"].format(name="suspect", error=f"{type(e).__name__}: {e}"), "passes": "no"}])
    target = lambda r: r["batch"].startswith(f"island/{FIRMWARE[0]}/") and r["batch"].endswith(f"{FIRMWARE[2]}.jsonl") and r["batch"].split("/")[2] >= FIRMWARE[3].replace(":", "")
    hit = [r for r in flagged if target(r)]
    other = [r for r in flagged if not target(r)]
    return Checked([
        {"test": MESSAGES["thursday"] if len(hit) == 2 else MESSAGES["thursday_no"].format(n=len(hit)), "passes": "yes" if len(hit) == 2 else "no"},
        {"test": MESSAGES["others"] if not other else MESSAGES["others_no"].format(runs="; ".join(_flagged_label(r) for r in other[:3]) + ("; and more" if len(other) > 3 else "")), "passes": "no" if other else "yes"},
    ])


def fields(c: collector.Collector, harbour: str, gate: str) -> Rows:
    """The fields of each batch from one gate, by the version its run read, as the runs recorded them."""
    return Rows(
        {"started": r["started"], "batch": r["batch"], "fields": ", ".join(r["fields"]), "scans read": r["scans_read"], "rows written": r["rows_written"]}
        for r in runs(c)
        if r["batch"].startswith(f"{harbour}/") and r["batch"].endswith(f"{gate}.jsonl")
    )


def trace(f: Ferry, c: collector.Collector, sailing: str) -> Rows:
    """Where one sailing's row of `sailing_loads` came from, from the collector's file: the run of
    `build_loads` that wrote it, and for each batch of the sailing the run of `load_scans` that last
    loaded it before that run started, with the version it read and the rows it wrote; then what
    `boardings` holds for the sailing now."""
    day, harbour, departs = sailing.split()
    builds = [e for e in c.file if e["job"]["name"] == "build_loads" and e["eventType"] == "COMPLETE"
              and (e["run"]["facets"].get("nominalTime") or {}).get("nominalStartTime", "")[:10] == iso(epoch(f"{day}T00:00:00Z") + 86400)[:10]]
    [build] = builds
    built_at = build["run"]["facets"]["nominalTime"]["nominalStartTime"]
    prefix = f"{harbour}/{day}/{departs.replace(':', '')}/"
    loads = [r for r in runs(c) if r["batch"] and r["batch"].startswith(prefix)]
    rows = [{"step": "the row of `sailing_loads`", "made by": f"`build_loads`, {built_at}", "batch": "", "version": "", "passengers": f.loads_built[day][sailing]}]
    total = 0
    for batch in sorted({r["batch"] for r in loads}):
        before = [r for r in loads if r["batch"] == batch and epoch(r["started"]) < epoch(built_at)]
        if not before:
            continue
        r = before[-1]
        total += r["rows_written"] or 0
        rows.append({"step": "a batch, as that run read it", "made by": f"`load_scans`, {r['started']}", "batch": batch.rsplit("/", 1)[-1], "version": r["version"] or MESSAGES["not_recorded"], "passengers": r["rows_written"]})
    later = [r for r in loads if epoch(r["started"]) >= epoch(built_at)]
    for r in later:
        rows.append({"step": "a later version of a batch", "made by": f"`load_scans`, {r['started']}", "batch": r["batch"].rsplit("/", 1)[-1], "version": r["version"] or MESSAGES["not_recorded"], "passengers": r["rows_written"]})
    now = f.warehouse.sql("SELECT COUNT(*) AS n FROM boardings WHERE sailing = :s", s=sailing)[0]["n"]
    rows.append({"step": "`boardings` now", "made by": "", "batch": "", "version": "", "passengers": now})
    return Rows(rows, null="")


def downstream(g: dict, start: str) -> list[str]:
    """Every dataset made, at any number of steps, from `start`, following the graph's edges by job."""
    found, todo = set(), [start]
    while todo:
        d = todo.pop()
        jobs = {j for (j, e, x) in g if e == "reads" and x == d}
        for (j, e, x) in g:
            if e == "writes" and j in jobs and x not in found:
                found.add(x)
                todo.append(x)
    return sorted(found)


def made_from_test(f: Ferry, g: dict) -> Rows:
    """Everything downstream of the test batch in the graph, and whether each still counts its scans."""
    start = f"{GATES_BUCKET}/{TEST_KEY}"
    sailing = _sailing_of(TEST_KEY)
    day = sailing.split()[0]
    out = []
    order = lambda d: (0 if short(d) == "boardings" else 1 if short(d) == "sailing_loads" else 2, d)
    for d in sorted(downstream(g, start), key=order):
        name = short(d)
        if name == "boardings":
            still = f.warehouse.sql("SELECT COUNT(*) AS n FROM boardings WHERE batch = :b", b=TEST_KEY)[0]["n"] > 0
        elif name == "sailing_loads":
            row = f.warehouse.sql("SELECT passengers FROM sailing_loads WHERE sailing = :s", s=sailing)[0]["passengers"]
            still = row != sum(r["counted on board"] for r in harbour_counts(day, sailing.split()[1]) if r["sailing"] == sailing)
        elif name.startswith("loads-"):
            text = f.storage.read_text(f"{REPORTS_BUCKET}/{name}")
            line = next((l for l in text.splitlines() if l.startswith(sailing + ",")), None)
            if line is None:
                continue
            counted = sum(r["counted on board"] for r in harbour_counts(day, sailing.split()[1]) if r["sailing"] == sailing)
            still = int(line.split(",")[1]) != counted
        else:
            continue
        out.append({"dataset": name, "still counts the test scans": MESSAGES["still"] if still else MESSAGES["gone"]})
    return Rows(out)


STUBS = {
    "inputs": '''def inputs(change):
    batch = {"namespace": change["bucket"], "name": change["key"]}
    if change["change"] == "deleted":
        return []
    return [batch]''',
    "suspect": '''def suspect(run):
    return run["state"] == "FAIL"''',
}

REFERENCE = {
    "inputs": '''def inputs(change):
    batch = {"namespace": change["bucket"], "name": change["key"]}
    if change["change"] == "deleted":
        batch["facets"] = {"version": shop.ferry.version_facet(change["previous"])}
    else:
        batch["facets"] = {"version": shop.ferry.version_facet(change["version"])}
    return [batch]''',
    "suspect": '''def suspect(run):
    return run["scans_read"] > 0 and run["rows_written"] == 0''',
}

__all__ = [
    "run", "Ferry", "platform", "harbour_counts", "compare_counts", "version_facet", "change_record", "events",
    "check_inputs", "one_event", "collect", "graph", "edges", "runs", "run_states", "check_suspect", "fields", "trace",
    "downstream", "made_from_test", "STUBS", "REFERENCE", "ASKED", "TEST_KEY",
]
