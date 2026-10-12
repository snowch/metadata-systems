# Copyright © 2026 Christopher Snow

"""Where one figure on the dashboard came from (Chapter 15).

`trace` follows one day's figure back, step by step: the dashboard's value and the run that drew
it; the row of `daily_sales` and the run that wrote it; the rows of `clean_orders` that row was
computed from (and, under the `net` change, the rows of `returns` its function read); and the lines
of `orders.jsonl`, in the version the run of `build_clean_orders` read, that became those rows. At
each step it sums what it found, so a step that does not add up to the step above shows.

It reads each file in the version the run read, since object storage keeps every version. It reads
each table as it is now, since the warehouse keeps none, unless `as_read` is set: then `returns` is
rebuilt as it was when the run started, from the versions of the objects that the returns desk's
functions recorded reading (`returns_as_of`). With `dropped`, it also lists the lines and rows each
run read and did not use, and the condition that left each out.

Every rule here is the shop's own choice.
"""

from __future__ import annotations

import json

from .data import DAYS
from .platform import Rows, epoch
from .runs import executions
from .week import FILES, NIGHTS, RETURNS_BUCKET, Week

DASHBOARD = "sales_dashboard"


def _run(week: Week, job: str, night: str):
    [(run, e)] = [(r, e) for r, e in executions(week) if e.job == job and e.night == night]
    return run, e


def _version(week: Week, uri: str, at: str) -> dict:
    """The version of an object that was current at `at`."""
    return [v for v in week.storage.versions(uri) if v["key"] == uri and v["at"] <= at][-1]


def returns_as_of(week: Week, at: str) -> Rows:
    """The table `returns` as it was at `at`, rebuilt from the functions' runs: each run of
    `record_return` that had finished put in the row of the object version it read, and each run of
    `remove_return` took the return's row out."""
    table: dict[str, dict] = {}
    for run, e in executions(week):
        if e.job not in ("record_return", "remove_return") or e.finished > at:
            continue
        return_id = e.object.rsplit("/", 1)[1].removesuffix(".json")
        if e.job == "remove_return":
            table.pop(return_id, None)
        else:
            row = json.loads(week.storage.version_text(e.object, e.version))
            table[return_id] = {**row, "run": run, "version": e.version}
    return Rows(sorted(table.values(), key=lambda r: r["return_id"]))


def _returns_now(week: Week) -> Rows:
    return week.warehouse.sql("SELECT * FROM returns ORDER BY return_id")


def trace(week: Week, day: str, dropped: bool = False, as_read: bool = False) -> Rows:
    """One day's figure on the dashboard, followed back to the lines of the file it came from."""
    w = week.warehouse
    night = NIGHTS[DAYS.index(day)]
    out = []

    shown = {v["day"]: v["revenue"] for v in week.reporting.dashboard()["values"]}
    refreshes = [(r, e) for r, e in executions(week) if e.job == "refresh_dashboard" and e.status == "succeeded"]
    run, e = refreshes[-1]
    value = shown.get(day)
    pence = int(value.lstrip("£").replace(".", "")) if value else None
    out.append({"step": 1, "asset": DASHBOARD, "made by": f"{run}, {e.job}", "rows": f"the value for {day}, shown as {value}", "pence": pence})

    run, sales = _run(week, "build_daily_sales", night)
    [row] = w.sql("SELECT revenue_pence FROM daily_sales WHERE day = :d", d=day) or [{"revenue_pence": None}]
    out.append({"step": 2, "asset": "daily_sales", "made by": f"{run}, {sales.job}", "rows": f"the row for {day}", "pence": row["revenue_pence"]})

    code = sales.code or ""
    keep = "status <> 'refunded'" if "status <> 'refunded'" in code else "status = 'completed'"
    orders = w.sql(f"SELECT order_id, product_id, quantity, price_pence, status FROM clean_orders WHERE date(ordered_at) = :d ORDER BY order_id", d=day)
    used = [o for o in orders if (o["status"] != "refunded" if "<>" in keep else o["status"] == "completed")]
    returned: dict[tuple[int, int], int] = {}
    if "returned_quantity" in code:
        table = returns_as_of(week, sales.started) if as_read else _returns_now(week)
        for r in table:
            key = (r["order_id"], r["product_id"])
            returned[key] = returned.get(key, 0) + r["quantity"]
    run_c, cleaned = _run(week, "build_clean_orders", night)
    total = sum(o["price_pence"] * o["quantity"] for o in used)
    out.append({"step": 3, "asset": "clean_orders", "made by": f"{run_c}, {cleaned.job}", "rows": ", ".join(str(o["order_id"]) for o in used), "pence": total})
    if returned:
        counted = {(o["order_id"], o["product_id"]) for o in used}
        hits = [r for r in table if (r["order_id"], r["product_id"]) in counted]
        where = "returns, as it was at " + sales.started[11:19] if as_read else "returns, as it is now"
        made = ", ".join(sorted({r["run"] for r in hits})) if as_read else "record_return"
        less = sum(o["price_pence"] * returned.get((o["order_id"], o["product_id"]), 0) for o in used)
        detail = "; ".join(f"{r['return_id']}: {r['quantity']} of order {r['order_id']}" for r in hits)
        out.append({"step": 3, "asset": where, "made by": made, "rows": detail or "none for these orders", "pence": -less})
    if dropped:
        left = [o for o in orders if o not in used]
        if left:
            out.append({"step": 3, "asset": "clean_orders, not counted", "made by": f"{run}, {sales.job}", "rows": ", ".join(f"{o['order_id']}: {keep} is false" for o in left), "pence": sum(o["price_pence"] * o["quantity"] for o in left)})

    version = _version(week, FILES["orders"], cleaned.started)
    lines = [json.loads(t) for t in week.storage.version_text(FILES["orders"], version["version"]).splitlines()]
    ids = {o["order_id"] for o in used}
    found = [(n, l) for n, l in enumerate(lines, start=1) if l.get("order_id") in ids]
    first: dict[int, int] = {}
    for n, l in found:
        first.setdefault(l["order_id"], n)
    asset = f"orders.jsonl, version of {version['at'][5:16].replace('T', ' ')}"
    out.append(
        {
            "step": 4,
            "asset": asset,
            "made by": "the export",
            "rows": "lines " + ", ".join(str(n) for n in sorted(first.values())),
            "pence": sum(l["price_pence"] * l["quantity"] for n, l in found if first[l["order_id"]] == n),
        }
    )
    if dropped:
        why = []
        seen: set = set()
        for n, l in enumerate(lines, start=1):
            if l["ordered_at"][:10] != day:
                continue
            if l["order_id"] in seen:
                why.append((n, l, "repeats an earlier line"))
            elif l.get("customer_id") is None:
                why.append((n, l, "customer_id IS NOT NULL is false"))
            elif l.get("quantity") is not None and l["quantity"] <= 0:
                why.append((n, l, "quantity > 0 is false"))
            seen.add(l["order_id"])
        if why:
            out.append(
                {
                    "step": 4,
                    "asset": asset + ", read and left out",
                    "made by": f"{run_c}, {cleaned.job}",
                    "rows": "; ".join(f"line {n}, order {l['order_id']}: {reason}" for n, l, reason in why),
                    "pence": sum(l["price_pence"] * l["quantity"] for n, l, reason in why),
                }
            )
    return Rows(out, null="")


def figure_adds_up(week: Week, day: str, as_read: bool = False) -> bool:
    """Whether the rows `trace` finds add up to the row of `daily_sales`."""
    steps = trace(week, day, as_read=as_read)
    written = steps[1]["pence"]
    return written == sum(r["pence"] for r in steps if r["step"] == 3)


def object_versions(week: Week, return_id: str) -> Rows:
    """Every version of one return's object, and what each says."""
    uri = f"{RETURNS_BUCKET}/{return_id}.json"
    out = []
    for v in week.storage.versions(uri):
        text = week.storage.version_text(uri, v["version"])
        body = json.loads(text) if text else None
        out.append({"version": v["version"], "at": v["at"], "order": body["order_id"] if body else None, "quantity": body["quantity"] if body else None, "deleted": "yes" if v["deleted"] else ""})
    return Rows(out, null="")


__all__ = ["figure_adds_up", "object_versions", "returns_as_of", "trace"]
