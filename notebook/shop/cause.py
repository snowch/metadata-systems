# Copyright © 2026 Christopher Snow

"""A backwards search from a wrong figure to where it went wrong (Chapter 17).

`search` starts at one day's value on the dashboard and steps back along the lineage that feeds it:
the row of `daily_sales`, the rows of `clean_orders`, and the version of `orders.jsonl` the run of
`build_clean_orders` read. At each step it measures the day's revenue the way the dashboard's own
program defines it (price times quantity, over the day's completed orders, each order once), and
records whether the measure differs from the step after it, and whether the code of the program that
made the step had changed since its run the night before. The search stops at the export, whose
inputs no record names.

It reads each file in the version the run read and each table as it is now (Chapter 15). Every rule
here is the shop's own choice.
"""

from __future__ import annotations

import difflib
import json

from .data import DAYS
from .platform import Rows
from .runs import executions
from .week import FILES, NIGHTS, Week


def _runs(week: Week, job: str) -> list[tuple[str, object]]:
    return [(r, e) for r, e in executions(week) if e.job == job]


def _changed(week: Week, job: str, night: str) -> str:
    """Whether a program's code on a night differs from its code on the night before."""
    runs = {e.night: e for _, e in _runs(week, job)}
    k = NIGHTS.index(night)
    if k == 0 or NIGHTS[k - 1] not in runs:
        return ""
    return "yes" if runs[night].code != runs[NIGHTS[k - 1]].code else "no"


def search(week: Week, day: str) -> Rows:
    """One day's figure, followed back step by step, measured the same way at every step."""
    w = week.warehouse
    night = NIGHTS[DAYS.index(day)]
    out = []

    shown = {v["day"]: v["revenue"] for v in week.reporting.dashboard()["values"]}.get(day)
    [(refresh, re)] = [(r, e) for r, e in _runs(week, "refresh_dashboard") if e.status == "succeeded"][-1:]
    out.append({"step": 1, "asset": "sales_dashboard", "made by": f"{refresh}, {re.job}", "pence": int(shown.lstrip("£").replace(".", "")) if shown else None, "code changed": _changed(week, re.job, re.night)})

    [(run, sales)] = [(r, e) for r, e in _runs(week, "build_daily_sales") if e.night == night]
    [row] = w.sql("SELECT revenue_pence FROM daily_sales WHERE day = :d", d=day) or [{"revenue_pence": None}]
    out.append({"step": 2, "asset": "daily_sales", "made by": f"{run}, {sales.job}", "pence": row["revenue_pence"], "code changed": _changed(week, sales.job, night)})

    [(run, cleaned)] = [(r, e) for r, e in _runs(week, "build_clean_orders") if e.night == night]
    [total] = w.sql(
        "SELECT SUM(price_pence * quantity) AS p FROM clean_orders WHERE status = 'completed' AND date(ordered_at) = :d", d=day
    )
    out.append({"step": 3, "asset": "clean_orders", "made by": f"{run}, {cleaned.job}", "pence": total["p"], "code changed": _changed(week, cleaned.job, night)})

    versions = [v for v in week.storage.versions(FILES["orders"]) if v["key"] == FILES["orders"] and v["at"] <= cleaned.started]
    text = week.storage.version_text(FILES["orders"], versions[-1]["version"])
    seen, pence = set(), 0
    for line in text.splitlines():
        o = json.loads(line)
        if o["ordered_at"][:10] == day and o.get("status") == "completed" and o["order_id"] not in seen:
            seen.add(o["order_id"])
            pence += o["price_pence"] * (o.get("quantity") or 0)
    out.append({"step": 4, "asset": f"orders.jsonl, version of {versions[-1]['at'][5:16].replace('T', ' ')}", "made by": "the export", "pence": pence, "code changed": ""})

    for k, r in enumerate(out):
        r["differs from its input"] = "" if k == len(out) - 1 else ("yes" if r["pence"] != out[k + 1]["pence"] else "no")
    out.append({"step": 5, "asset": "the checkout", "made by": "", "pence": None, "code changed": "", "differs from its input": ""})
    return Rows(
        ({"step": r["step"], "asset": r["asset"], "made by": r["made by"], "pence": r["pence"], "differs from its input": r["differs from its input"], "code changed since the night before": r["code changed"]} for r in out),
        null="",
    )


def code_change(week: Week, job: str, night: str) -> str:
    """The lines of a program's code that changed between the night before and `night`."""
    runs = {e.night: e for _, e in _runs(week, job)}
    before = runs[NIGHTS[NIGHTS.index(night) - 1]].code.splitlines()
    after = runs[night].code.splitlines()
    return "\n".join(l for l in difflib.unified_diff(before, after, lineterm="", n=0) if l[:1] in "+-" and l[:3] not in ("+++", "---"))


__all__ = ["code_change", "search"]
