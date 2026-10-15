# Copyright © 2026 Christopher Snow

"""Where four systems' metadata comes from, applied to the shop's nightly work (Chapter 30).

The shop's four nightly jobs are imagined running in each of four systems. None of them runs
here: each function applies the rules the system's code or documentation states, read at the
commits `docs/sources.md` names ("Read for Part VII"), to the shop's own week with the returns
desk, the analyst's copy and Monday's failed night.

- Airflow (3.3.0; the OpenLineage provider 2.20.3): a task instance is one task in one Dag run; the
  scheduler raises its `try_number` on each try, and one row holds the latest try. The provider
  names the job `{dag_id}.{task_id}` and makes each try's run id from the try number among other
  values, so a retried task instance is two OpenLineage runs. The shop's Dag retries a task once.
- Spark (4.0.0; OpenLineage's Spark integration): the job is named from the application's name,
  the executed plan's top node put through the integration's normaliser, and, for an insert into a
  table kept as files, the last two parts of the path its files are written to. The top node of
  such an insert is Spark's `Execute InsertIntoHadoopFsRelationCommand`. Where the shop's table's
  files are kept (`SPARK_PATH`) is the shop's assumption.
- dbt (artifacts of 1.11; `openlineage-dbt`): the wrapper runs dbt, then reads its artifacts and
  sends every event; a model's job is `{database}.{schema}.{package}.{model}`, and each reading of
  the artifacts makes new run ids. The shop's warehouse jobs run as one dbt invocation.
- Trino (`trino-openlineage`): the listener sends `START` when a query is created and `COMPLETE` or
  `FAIL` when it ends, the inputs and output on the second only; the job's name follows
  `openlineage-event-listener.job.name-format`, `$QUERY_ID` unless set, with `$SOURCE`, `$USER` and
  `$CLIENT_IP` the other values it takes; a `SELECT` sends nothing unless configured.

Names such as the Dag `shop_nightly`, the dbt project `shop_models`, the Spark application
`shop_nightly`, the query ids and the client sources are the shop's.
"""

from __future__ import annotations

from .delivery import week_events
from .platform import Rows
from .week import Week

WEEK = ("returns", "source", "failed")
DAG = "shop_nightly"
APP = "shop_nightly"
PROJECT = "shop_models"
NIGHTLY = ("build_clean_customers", "build_clean_orders", "build_daily_sales", "refresh_dashboard")
WAREHOUSE_JOBS = {"build_clean_customers": "clean_customers", "build_clean_orders": "clean_orders", "build_daily_sales": "daily_sales"}
FORMATS = ("$QUERY_ID", "$SOURCE", "$USER", "$CLIENT_IP")
SPARK_TOP_NODE = "Execute InsertIntoHadoopFsRelationCommand"

MESSAGES = {
    "summary": "{passed} of {total} tests pass.",
    "jobs": "The 7 runs of `build_daily_sales` are {n} {noun} in Trino's events.",
    "merged": "That job holds the runs of `build_daily_sales` only.",
    "merged_no": "That job also holds the runs of {others}.",
    "format_no": "`name_format` must be one of {formats}.",
}


def rules() -> Rows:
    """What each system's integration makes an OpenLineage job and run, where it takes the inputs
    from, and when it sends."""
    return Rows([
        {"system": "Airflow", "OpenLineage job": "a task in a Dag", "OpenLineage run": "a try of a task instance", "inputs from": "the operator's extractor, hooks' lineage, or the task's declared inlets and outlets", "sent": "as each try starts and ends"},
        {"system": "Spark", "OpenLineage job": "a Spark action, named from its plan's top node and its output", "OpenLineage run": "one execution", "inputs from": "the query plan", "sent": "as the execution starts and ends"},
        {"system": "dbt", "OpenLineage job": "a model", "OpenLineage run": "one reading of the files dbt wrote", "inputs from": "the manifest's parents of the model", "sent": "after dbt has finished"},
        {"system": "Trino", "OpenLineage job": "a query, named by its id unless set", "OpenLineage run": "one query", "inputs from": "the tables the query names", "sent": "as the query is created and ends"},
    ])


def _nights(week: Week) -> list[dict]:
    """Each nightly run of the shop's four jobs: job, day, start, end, state, reads, writes."""
    runs: dict = {}
    for e in week_events(week):
        name = e["job"]["name"]
        if e["job"]["namespace"] != "shop" or name not in NIGHTLY:
            continue
        r = runs.setdefault(e["run"]["runId"], {"job": name, "reads": [], "writes": []})
        if e["eventType"] == "START":
            r["start"] = e["eventTime"]
            r["day"] = e["eventTime"][:10]
        else:
            r["end"], r["state"] = e["eventTime"], e["eventType"]
            r["reads"] = [i["name"].rsplit(".", 1)[-1] if "analytics" in i["name"] else i["name"] for i in e.get("inputs", [])]
            r["writes"] = [o["name"] for o in e.get("outputs", [])]
    return sorted(runs.values(), key=lambda r: r["start"])


def airflow(week: Week, retries: int = 1) -> Rows:
    """The task instances of `build_daily_sales` in the Dag's 7 runs, and the OpenLineage runs of each."""
    out = []
    for r in _nights(week):
        if r["job"] != "build_daily_sales":
            continue
        tries = 1 + (retries if r["state"] == "FAIL" else 0)
        out.append({
            "Dag run": r["day"],
            "task instance": f"{DAG}.{r['job']}",
            "try_number": tries,
            "state": "failed" if r["state"] == "FAIL" else "success",
            "OpenLineage job": f"default/{DAG}.{r['job']}",
            "OpenLineage runs": tries,
        })
    return Rows(out)


def _normalise(name: str) -> str:
    """OpenLineage's Spark normaliser, as its code states it: words split at case changes, lower case,
    every run of other characters made `_`."""
    import re

    s = re.sub(r"^[^\w]+|[^\w]+$", "", name)
    s = re.sub(r"([a-z])([A-Z])", r"\1 \2", s)
    s = re.sub(r"(?<!^)([A-Z])([a-z])", r" \1\2", s)
    s = re.sub(r"(\d)([A-Z])", r"\1 \2", s)
    return re.sub(r"[^a-zA-Z0-9]+", "_", s.lower())


SPARK_PATH = "s3://shop-warehouse/analytics/daily_sales"


def spark(path: str = SPARK_PATH) -> str:
    """The job name Spark's integration gives an insert into a table whose files are under `path`:
    the application, the plan's top node through the normaliser, and the last two parts of the
    output's path joined with `_` (`JobNameSuffixProvider.trimPath`), its dots then made `_`."""
    name = path.split("://", 1)[-1].split("/", 1)[-1]
    parts = name.split("/")
    suffix = "_".join(parts[-2:]) if len(parts) >= 2 else parts[-1]
    return f"{APP}.{_normalise(SPARK_TOP_NODE)}.{suffix.replace('.', '_')}"


def dbt(week: Week, day: str = "2026-09-13") -> Rows:
    """One night's dbt invocation: each model's job, its run's times, and when its events are sent."""
    night = [r for r in _nights(week) if r["day"] == day and r["job"] in WAREHOUSE_JOBS]
    sent = max(r["end"] for r in night)
    return Rows(
        {
            "model": f"model.{PROJECT}.{WAREHOUSE_JOBS[r['job']]}",
            "OpenLineage job": f"dbt/shop.analytics.{PROJECT}.{WAREHOUSE_JOBS[r['job']]}",
            "START time": r["start"][11:19],
            "end time": r["end"][11:19],
            "events sent at": sent[11:19],
        }
        for r in night
    )


def trino(week: Week, name_format: str = "$QUERY_ID", source_of: dict | None = None) -> Rows:
    """Each nightly query's job name in Trino's events, under `name_format`."""
    source_of = source_of or {job: "shop-nightly" for job in NIGHTLY}
    out = []
    for n, r in enumerate(_nights(week), start=1):
        query_id = f"q{r['day'][8:10]}{NIGHTLY.index(r['job']) + 1:02d}"
        values = {"$QUERY_ID": query_id, "$SOURCE": source_of.get(r["job"], ""), "$USER": "etlsvc/batch01.corp.internal@CORP.INTERNAL", "$CLIENT_IP": "10.0.0.5"}
        out.append({"program": r["job"], "night": r["day"], "query": query_id, "job in Trino's events": values.get(name_format, name_format)})
    return Rows(out)


class Checked(Rows):
    def __init__(self, rows) -> None:
        super().__init__(rows)
        self.passed = sum(r["passes"] == "yes" for r in rows)

    def _repr_html_(self) -> str:
        return f"<p>{MESSAGES['summary'].format(passed=self.passed, total=len(self))}</p>" + super()._repr_html_()


def check_trino(week: Week, name_format: str, source_of: dict) -> Checked:
    """One job for the 7 runs of `build_daily_sales`, holding no other program's runs."""
    if name_format not in FORMATS:
        return Checked([{"test": MESSAGES["format_no"].format(formats=", ".join(f"`{f}`" for f in FORMATS)), "passes": "no"}])
    rows = trino(week, name_format, source_of)
    mine = {r["job in Trino's events"] for r in rows if r["program"] == "build_daily_sales"}
    n = len(mine)
    out = [{"test": MESSAGES["jobs"].format(n=n, noun="job" if n == 1 else "jobs"), "passes": "yes" if n == 1 else "no"}]
    if n == 1:
        others = sorted({r["program"] for r in rows if r["job in Trino's events"] in mine and r["program"] != "build_daily_sales"})
        out.append({
            "test": MESSAGES["merged"] if not others else MESSAGES["merged_no"].format(others=", ".join(f"`{o}`" for o in others)),
            "passes": "no" if others else "yes",
        })
    return Checked(out)


def jobs_by_format(week: Week, source_of: dict | None = None) -> Rows:
    """For each name format, how many jobs the week's 28 nightly queries make."""
    return Rows(
        {"name format": f, "jobs": len({r["job in Trino's events"] for r in trino(week, f, source_of)})}
        for f in FORMATS
    )


STUBS = {"trino": 'name_format = "$QUERY_ID"\nsource_of = {\n    "build_clean_customers": "shop-nightly",\n    "build_clean_orders": "shop-nightly",\n    "build_daily_sales": "shop-nightly",\n    "refresh_dashboard": "shop-nightly",\n}'}
REFERENCE = {"trino": 'name_format = "$SOURCE"\nsource_of = {\n    "build_clean_customers": "clean-customers",\n    "build_clean_orders": "clean-orders",\n    "build_daily_sales": "daily-sales",\n    "refresh_dashboard": "dashboard",\n}'}

__all__ = ["rules", "airflow", "spark", "dbt", "trino", "check_trino", "jobs_by_format", "STUBS", "REFERENCE", "WEEK", "FORMATS"]
