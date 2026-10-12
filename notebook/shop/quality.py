# Copyright © 2026 Christopher Snow

"""What a run measures of the rows it reads and writes, and assertions over it (Chapter 14).

Each run of `build_clean_orders` counts, as it runs, four things in the file it read and in the
table it wrote: the rows; the rows with no customer id; the rows beyond the first with the same
order id; and the rows with a quantity of 0 or less (`week.METRICS`). Nothing else in the shop
measures what a run reads.

An assertion is a rule a measurement must meet on every run: here, that one count in one dataset is
at most a number. `check` tests it against each run's measurement and records whether it held.
`reconcile` sets each run's rows read against its rows written. `readings` tests three readings of
"No order without a customer.", and `facets` gives one run's measurements and assertion in
OpenLineage's form. Every rule here is the shop's own choice.
"""

from __future__ import annotations

from .data import DAYS
from .openlineage import dataset as named, facet
from .platform import Rows
from .runs import executions
from .week import FILES, METRICS, Week

DATASETS = ("orders.jsonl", "clean_orders")


def _measured(week: Week):
    for run, e in executions(week):
        if e.quality:
            yield run, e, {(d, m): v for d, m, v in e.quality}


def _data_up_to(night: str) -> str:
    """The last day of orders a night's export holds: the day before the night."""
    return DAYS[DAYS.index(night) - 1] if night in DAYS else DAYS[-1]


def measurements(week: Week, dataset: str | None = None) -> Rows:
    """Each run of `build_clean_orders`, and what it counted in the file it read and the table it
    wrote; with `dataset`, in that one only."""
    out = []
    for run, e, q in _measured(week):
        for d in DATASETS:
            if dataset in (None, d):
                out.append({"run": run, "night": e.night, "orders up to": _data_up_to(e.night), "dataset": d, **{m: q[(d, m)] for m in METRICS}})
    return Rows(out)


def check(week: Week, dataset: str, metric: str, at_most: int = 0) -> Rows:
    """An assertion, `metric` in `dataset` is at most `at_most`, tested against each run."""
    if dataset not in DATASETS:
        raise ValueError(f"no dataset called {dataset!r}; the datasets are {', '.join(DATASETS)}")
    if metric not in METRICS:
        raise ValueError(f"no measurement called {metric!r}; the measurements are {', '.join(METRICS)}")
    return Rows(
        {"run": run, "night": e.night, "dataset": dataset, metric: q[(dataset, metric)], "at most": at_most, "passed": "yes" if q[(dataset, metric)] <= at_most else "no"}
        for run, e, q in _measured(week)
    )


def reconcile(week: Week) -> Rows:
    """Each run's rows read and written, and how many of the rows it read it left out beyond those
    that repeat an order: a count no measurement of one dataset gives."""
    out = []
    for run, e, q in _measured(week):
        left = q[("orders.jsonl", "rows")] - q[("clean_orders", "rows")] - q[("orders.jsonl", "order_id twice")]
        out.append(
            {
                "run": run,
                "night": e.night,
                "rows read": q[("orders.jsonl", "rows")],
                "rows written": q[("clean_orders", "rows")],
                "repeats": q[("orders.jsonl", "order_id twice")],
                "left out": left,
                "passed": "yes" if left == 0 else "no",
            }
        )
    return Rows(out)


def left_out(week: Week) -> Rows:
    """The completed orders in the file that have no customer id, by day, and their value: what the
    dashboard's revenue does not count for that reason."""
    return week.storage.sql(
        FILES["orders"],
        """SELECT date(ordered_at) AS day, COUNT(DISTINCT order_id) AS orders, SUM(price_pence * quantity) AS pence
           FROM (SELECT DISTINCT * FROM file) WHERE customer_id IS NULL AND status = 'completed' GROUP BY 1 ORDER BY 1""",
    )


def readings(week: Week) -> Rows:
    """"No order without a customer." under three readings, each tested by an assertion or a count."""
    in_file = check(week, "orders.jsonl", "no customer_id")
    in_table = check(week, "clean_orders", "no customer_id")
    missed = left_out(week)
    fails = lambda rows: sum(r["passed"] == "no" for r in rows)
    return Rows(
        [
            {"reading": "in the file the checkout sends", "test": "no customer_id in orders.jsonl is 0", "runs failed": fails(in_file), "met": "yes" if not fails(in_file) else "no"},
            {"reading": "in clean_orders", "test": "no customer_id in clean_orders is 0", "runs failed": fails(in_table), "met": "yes" if not fails(in_table) else "no"},
            {
                "reading": "on the dashboard",
                "test": "every completed order is counted in a day's revenue",
                "runs failed": None,
                "met": "yes" if not missed else "no",
            },
        ],
        null="",
    )


def facets(week: Week, run: str) -> dict:
    """The input `orders.jsonl` of one run of `build_clean_orders` as the shop's producer would send
    it: its measurements as `dataQualityMetrics` and the assertion as `dataQualityAssertions`."""
    [(e, q)] = [(e, q) for r, e, q in _measured(week) if r == run]
    metrics = facet(
        "dataQualityMetrics",
        rowCount=q[("orders.jsonl", "rows")],
        captureDate=e.started,
        columnMetrics={
            "customer_id": {"nullCount": q[("orders.jsonl", "no customer_id")]},
            "order_id": {"distinctCount": q[("orders.jsonl", "rows")] - q[("orders.jsonl", "order_id twice")]},
        },
    )
    missing = q[("orders.jsonl", "no customer_id")]
    assertions = facet(
        "dataQualityAssertions",
        assertions=[{"assertion": "not_null", "column": "customer_id", "success": missing == 0, "expected": "0", "actual": str(missing)}],
    )
    return {**named(FILES["orders"]), "facets": {"dataQualityMetrics": metrics}, "inputFacets": {"dataQualityAssertions": assertions}}


__all__ = ["DATASETS", "check", "facets", "left_out", "measurements", "readings", "reconcile"]
