# Copyright © 2026 Christopher Snow

"""The metadata interface, built (Chapter 28): a page for one asset, drawn from the store, the
collector's file and the lineage graph that Chapters 24 to 27 built (the shop's reference pieces),
for the same week as Chapter 27.

The page is made of sections. The learner chooses which, as a list of names from `SECTIONS`, and
writes one section's rows, `run_history(asset)`, from `runs()` and `writers(asset)`. `page` draws
the page; `check` tests the run history and the sections.
"""

from __future__ import annotations

import html

from . import query, store
from .ingest import normalise, objects
from .lineage_graph import stored
from .platform import Rows
from .week import Week, run_week

SECTIONS = ("description", "owner", "runs", "upstream", "downstream", "columns", "freshness")

MESSAGES = {
    "summary": "{passed} of {total} tests pass.",
    "runs": "The run history of `daily_sales` holds {n} runs, Monday's `FAIL` among them.",
    "runs_no": "The run history of `daily_sales` holds {n} runs: {missing}.",
    "missing_fail": "Monday's run, which failed, is not among them",
    "others": "it holds runs of programs that do not write `daily_sales`",
    "sections": "Every section named is one the page can draw.",
    "sections_no": "The page cannot draw {unknown}: choose from {known}.",
    "left_out": "Not on this page: {names}.",
    "none_left_out": "Every section is on this page.",
    "nothing": "Nothing recorded.",
}


def _week() -> Week:
    return run_week(list(query.WEEK))


def runs() -> Rows:
    """Every run in the collector's file: its job, state, start and end, and what it wrote."""
    objs = objects(normalise([e for _, e in stored(_week())]))
    return Rows(
        {"job": r["job"], "state": r["state"], "started": r["started"], "ended": r["ended"], "writes": [w.rsplit("/", 1)[-1].removeprefix("shop.analytics.") for w in r["writes"]]}
        for r in objs.runs.values()
    )


def writers(asset: str) -> list[str]:
    """The jobs the lineage graph records writing `asset`."""
    g = query.graph(_week())
    return sorted({j for (j, e, d) in g if e == "writes" and query._short(d) == asset})


def _section(name: str, asset: str, run_history) -> Rows:
    week = _week()
    g = query.graph(week)
    if name == "description":
        found = [{"field": f, "value": v} for a, fields in store.DESCRIBED.items() if query._short(a) == asset for f, v in fields.items()]
        return Rows(found, empty=MESSAGES["nothing"])
    if name == "owner":
        return Rows([{"meaning": m, "owner": v} for m, v in query.owners(asset).items() if v], empty=MESSAGES["nothing"])
    if name == "runs":
        return Rows(({k: v for k, v in r.items() if k != "writes"} for r in run_history(asset)), empty=MESSAGES["nothing"])
    if name == "upstream":
        return Rows([{"asset": a} for a in query.upstream(g, asset)], empty=MESSAGES["nothing"])
    if name == "downstream":
        ns: dict = {"shop": __import__("shop")}
        exec(query.REFERENCE["downstream"], ns)
        return Rows([{"asset": a} for a in sorted(ns["downstream"](g, asset))], empty=MESSAGES["nothing"])
    if name == "columns":
        try:
            return Rows({"column": c, "type": t} for c, t in week.warehouse.table_schema(asset))
        except KeyError:
            return Rows([], empty=MESSAGES["nothing"])
    if name == "freshness":
        from . import observe
        return Rows([r for r in observe.freshness(week) if r["asset"] == asset], empty=MESSAGES["nothing"])
    raise KeyError(name)


class Page:
    def __init__(self, asset: str, sections: list[str], run_history) -> None:
        self.asset, self.sections = asset, [s for s in sections if s in SECTIONS]
        self.parts = [(s, _section(s, asset, run_history)) for s in self.sections]

    def _repr_html_(self) -> str:
        out = [f"<h3>{html.escape(self.asset)}</h3>"]
        for name, rows in self.parts:
            out.append(f"<h4>{html.escape(name)}</h4>" + rows._repr_html_())
        left = [s for s in SECTIONS if s not in self.sections]
        out.append("<p>" + html.escape(MESSAGES["left_out"].format(names=", ".join(left)) if left else MESSAGES["none_left_out"]) + "</p>")
        return "".join(out)

    def _mime_(self):
        return ("text/html", self._repr_html_())


def page(asset: str, sections: list[str], run_history) -> Page:
    return Page(asset, sections, run_history)


class Checked(Rows):
    def __init__(self, rows) -> None:
        super().__init__(rows)
        self.passed = sum(r["passes"] == "yes" for r in rows)

    def _repr_html_(self) -> str:
        return f"<p>{MESSAGES['summary'].format(passed=self.passed, total=len(self))}</p>" + super()._repr_html_()


def check(run_history, sections: list[str] | None = None) -> Checked:
    """The run history of `daily_sales`; and, given `sections`, whether the page can draw each."""
    rows = []
    got = list(run_history("daily_sales"))
    jobs = set(writers("daily_sales"))
    states = [r["state"] for r in got]
    problems = []
    if "FAIL" not in states:
        problems.append(MESSAGES["missing_fail"])
    if any(r["job"] not in jobs for r in got):
        problems.append(MESSAGES["others"])
    rows.append({"test": (MESSAGES["runs"] if not problems else MESSAGES["runs_no"]).format(n=len(got), missing="; ".join(problems)), "passes": "no" if problems else "yes"})
    if sections is None:
        return Checked(rows)
    unknown = [s for s in sections if s not in SECTIONS]
    rows.append({
        "test": MESSAGES["sections"] if not unknown else MESSAGES["sections_no"].format(unknown=", ".join(f"`{u}`" for u in unknown), known=", ".join(f"`{k}`" for k in SECTIONS)),
        "passes": "no" if unknown else "yes",
    })
    return Checked(rows)


STUBS = {
    "run_history": '''def run_history(asset):
    return [r for r in shop.interface.runs() if asset in r["writes"]]''',
}

REFERENCE = {
    "run_history": '''def run_history(asset):
    jobs = shop.interface.writers(asset)
    return [r for r in shop.interface.runs() if r["job"] in jobs]''',
}

__all__ = ["SECTIONS", "runs", "writers", "page", "check", "STUBS", "REFERENCE"]
