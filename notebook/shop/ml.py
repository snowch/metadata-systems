# Copyright © 2026 Christopher Snow

"""A forecast trained on the shop's data, recorded as an experiment tracker records it (Chapter 32).

On Saturday 12 at 09:00 the shop trains a forecast of the next day's revenue: the mean of the last
3 days in `daily_sales`. The run is recorded with the fields MLflow gives a run's input and a
registered version (read at commit 9d651c2, `docs/sources.md`): the dataset's `name`, `digest`,
`source`, `schema` and `profile`, the context `training`, and a version that names its run.

`digest` is the shop's, computed in MLflow's manner for a table (`compute_pandas_digest`): an MD5
over the first 10,000 rows, the number of rows and the column names, cut to 8 characters. MLflow
hashes the rows with pandas, which the shop does not use, so the shop's value is not MLflow's; the
rule it follows is. `daily_sales` gains one row each night and keeps the rows it has, so its rows
on Saturday morning are the ones for Monday 7 to Friday 11.
"""

from __future__ import annotations

import hashlib
import json

from . import openlineage
from .platform import Rows
from .week import Week

TRAINED_AT = "2026-09-12T09:00:00Z"
ASKED_AT = "2026-09-14T09:00:00Z"
MAX_ROWS = 10000
TABLE = "shop.analytics.daily_sales"
SOURCE = f"warehouse://shop-warehouse/{TABLE}"
COLUMNS = ("day", "revenue_pence")

MESSAGES = {
    "summary": "{passed} of {total} tests pass.",
    "match": "Your rows ({n}) give the digest `{got}`, the one the run recorded.",
    "match_no": "Your rows ({n}) give the digest `{got}`, not the run's `{want}`; the run read {want_n} rows.",
    "where_no": "The condition could not be run: {error}.",
}


def digest(rows: list[dict], columns=COLUMNS) -> str:
    """The shop's digest of a table, in MLflow's manner: the first 10,000 rows, the row count and the
    column names, through MD5, cut to 8 characters."""
    md5 = hashlib.md5()
    for row in rows[:MAX_ROWS]:
        md5.update(json.dumps([row[c] for c in columns]).encode())
    md5.update(str(len(rows)).encode())
    for c in columns:
        md5.update(c.encode())
    return md5.hexdigest()[:8]


def rows_at(week: Week, at: str) -> list[dict]:
    """The rows `daily_sales` held at `at`: each night's run that had finished by then added the row
    for the day before it."""
    days = {_day_before(e.night) for e in week.executions if e.wrote == "daily_sales" and e.status == "succeeded" and e.finished <= at}
    return [dict(r) for r in week.warehouse.sql("SELECT day, revenue_pence FROM daily_sales ORDER BY day") if r["day"] in days]


def _day_before(night: str) -> str:
    from datetime import date, timedelta

    return (date.fromisoformat(night) - timedelta(days=1)).isoformat()


def train(week: Week) -> dict:
    """The forecast trained at `TRAINED_AT`, and the record of its run and its registered version."""
    rows = rows_at(week, TRAINED_AT)
    last = [r["revenue_pence"] for r in rows[-3:]]
    run_id = openlineage.uuid7(TRAINED_AT, "train next_day_revenue")
    return {
        "forecast_pence": round(sum(last) / len(last)),
        "run": {"run_id": run_id, "start": TRAINED_AT},
        "input": {
            "name": TABLE,
            "digest": digest(rows),
            "source": SOURCE,
            "schema": list(COLUMNS),
            "profile": {"num_rows": len(rows)},
            "context": "training",
        },
        "version": {"name": "next_day_revenue", "version": 1, "run_id": run_id, "source": f"runs:/{run_id}/forecast"},
    }


def record(week: Week) -> Rows:
    """The run's input as the tracker records it, one field a row."""
    rec = train(week)["input"]
    return Rows({"field": k, "value": json.dumps(v) if isinstance(v, (dict, list)) else v} for k, v in rec.items())


def version(week: Week) -> Rows:
    """The registered version of the forecast, one field a row: it names the run, and the run names
    its input."""
    rec = train(week)
    return Rows(
        [{"field": k, "value": v} for k, v in rec["version"].items()]
        + [{"field": "the forecast, in pence", "value": rec["forecast_pence"]}]
    )


def today(week: Week) -> Rows:
    """The table as it is when the question is asked, beside the run's record."""
    now = rows_at(week, ASKED_AT)
    rec = train(week)["input"]
    return Rows([
        {"": "the run's record", "rows": rec["profile"]["num_rows"], "digest": rec["digest"]},
        {"": "daily_sales on Monday 14 at 09:00", "rows": len(now), "digest": digest(now)},
    ])


def cap(n: int = MAX_ROWS + 1) -> Rows:
    """A table of `n` rows made for this cell: its digest, and the digest after one row changes."""
    rows = [{"day": f"row {i}", "revenue_pence": i} for i in range(n)]
    out = [{"change": "none", "digest": digest(rows)}]
    for where, i in (("the first row", 0), (f"row {n}, the last", n - 1)):
        changed = [dict(r) for r in rows]
        changed[i]["revenue_pence"] += 1
        out.append({"change": f"{where}, plus 1 penny", "digest": digest(changed)})
    return Rows(out)


class Checked(Rows):
    def __init__(self, rows) -> None:
        super().__init__(rows)
        self.passed = sum(r["passes"] == "yes" for r in rows)

    def _repr_html_(self) -> str:
        return f"<p>{MESSAGES['summary'].format(passed=self.passed, total=len(self))}</p>" + super()._repr_html_()


def check(week: Week, where: str) -> Checked:
    """Whether the rows of today's `daily_sales` that meet `where` give the digest the run recorded."""
    record = train(week)["input"]
    want, want_n = record["digest"], record["profile"]["num_rows"]
    try:
        rows = [dict(r) for r in week.warehouse.sql(f"SELECT day, revenue_pence FROM daily_sales WHERE {where} ORDER BY day")]
    except Exception as e:  # the learner's condition is SQL; say what SQLite said
        return Checked([{"test": MESSAGES["where_no"].format(error=str(e).rstrip(".")), "passes": "no"}])
    got = digest(rows)
    return Checked([{
        "test": MESSAGES["match" if got == want else "match_no"].format(n=len(rows), got=got, want=want, want_n=want_n),
        "passes": "yes" if got == want else "no",
    }])


STUBS = {"where": "where = \"day <= '2026-09-13'\""}
REFERENCE = {"where": "where = \"day <= '2026-09-11'\""}

__all__ = ["digest", "rows_at", "train", "record", "version", "today", "cap", "check", "STUBS", "REFERENCE", "TRAINED_AT", "ASKED_AT"]
