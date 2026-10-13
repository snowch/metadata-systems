# Copyright © 2026 Christopher Snow

"""The query layer, built (Chapter 27): questions over the lineage graph Chapter 26 built and the
records the shop holds.

The week has the returns desk, the analyst's copy as `build_daily_sales`'s source from Sunday 13
(`source`), and Monday's run of `build_daily_sales` failing (`failed`). The graph is Chapter 26's,
built by the shop's reference pieces from the collector's file.

The learner writes two queries:

- `downstream(graph, asset)`: every asset made, at any number of steps, from `asset`, using
  `next_assets`, which gives the assets one step on;
- `owner(asset)`: an owner, and which meaning of "owner" it is: `account` (the warehouse's owner,
  Chapter 2), `responsible` (the person your records name, Chapter 4) or `team` (the team sheet's,
  Chapter 21). Each meaning's value comes from its own source, through `owners(asset)`.

`answers` gives the shop's own answers to the other questions: where an asset came from, which
assets are stale, which runs failed, and which columns a change to one column reaches.
"""

from __future__ import annotations

from . import claims, impact, lineage_graph, observe
from .ingest import normalise, objects
from .platform import Rows
from .delivery import week_events
from .week import Week

WEEK = ("returns", "source", "failed")
MEANINGS = ("account", "responsible", "team")

# Each meaning's source, for the assets that have a value in it.
ACCOUNT = "etl_service"  # the warehouse records it as every table's owner (Chapter 2)
# the `responsible` lines of your records and Jo's notes (Chapter 4)
RESPONSIBLE = {
    "daily_sales": "j.marsh",
    "sales_dashboard": "j.marsh",
    "products.csv": "s.lund",
    "clean_orders": "the data engineer",
    "clean_customers": "the data engineer",
}
TEAM = {"daily_sales": claims.SOURCES["team sheet"]["owner"]}

MESSAGES = {
    "summary": "{passed} of {total} tests pass.",
    "down": "Downstream of `{asset}`: {got}.",
    "down_no": "Downstream of `{asset}`: {got}. Expected {want}.",
    "meaning": "The owner of `daily_sales` is `{value}`, as `{meaning}`.",
    "meaning_no": "The answer does not say which meaning it holds: return one of {meanings} as `meaning`.",
    "value_no": "`{value}` is not the `{meaning}` of `daily_sales`: that is `{want}`.",
    "none": "none",
}


def _short(name: str) -> str:
    return name.rsplit("/", 1)[-1].removeprefix("shop.analytics.")


def graph(week: Week) -> dict:
    """Chapter 26's graph, built from the collector's file with the shop's reference pieces."""
    ns: dict = {"shop": __import__("shop")}
    exec(lineage_graph.REFERENCE["add"], ns)
    return lineage_graph.build(week, ns["add"])


def _find(graph: dict, asset: str) -> list[str]:
    return sorted({d for (_, _, d) in graph if d == asset or _short(d) == asset})


def next_assets(graph: dict, asset: str) -> list[str]:
    """The assets one step downstream: what each job that reads `asset` writes."""
    names = set(_find(graph, asset)) or {asset}
    jobs = {j for (j, e, d) in graph if e == "reads" and d in names}
    return sorted({_short(d) for (j, e, d) in graph if e == "writes" and j in jobs})


def previous_assets(graph: dict, asset: str) -> list[str]:
    """The assets one step upstream: what each job that writes `asset` reads."""
    names = set(_find(graph, asset)) or {asset}
    jobs = {j for (j, e, d) in graph if e == "writes" and d in names}
    return sorted({_short(d) for (j, e, d) in graph if e == "reads" and j in jobs})


def upstream(graph: dict, asset: str) -> list[str]:
    found, todo = set(), [asset]
    while todo:
        for nxt in previous_assets(graph, todo.pop()):
            if nxt not in found:
                found.add(nxt)
                todo.append(nxt)
    return sorted(found)


def owners(asset: str) -> dict[str, str | None]:
    """Each meaning's owner of `asset`, from its own source; None where the source has none."""
    asset = _short(asset)
    warehouse = asset in ("daily_sales", "clean_orders", "clean_customers", "returns")
    return {"account": ACCOUNT if warehouse else None, "responsible": RESPONSIBLE.get(asset), "team": TEAM.get(asset)}


def coverage(week: Week) -> Rows:
    """Every asset on the platform, and the owner each meaning's source has for it."""
    from .records import assets

    return Rows(({"asset": _short(identifier), **owners(identifier)} for _, identifier in assets(week)), null="")


class Checked(Rows):
    def __init__(self, rows) -> None:
        super().__init__(rows)
        self.passed = sum(r["passes"] == "yes" for r in rows)

    def _repr_html_(self) -> str:
        return f"<p>{MESSAGES['summary'].format(passed=self.passed, total=len(self))}</p>" + super()._repr_html_()


def check_downstream(week: Week, downstream) -> Checked:
    g = graph(week)
    rows = []
    for asset in ("orders.jsonl", "clean_orders", "returns"):
        ns: dict = {"shop": __import__("shop")}
        exec(REFERENCE["downstream"], ns)
        want = sorted(ns["downstream"](g, asset))
        got = sorted(downstream(g, asset))
        ok = got == want
        msg = MESSAGES["down" if ok else "down_no"].format(asset=asset, got=", ".join(got) or MESSAGES["none"], want=", ".join(want) or MESSAGES["none"])
        rows.append({"test": msg, "passes": "yes" if ok else "no"})
    return Checked(rows)


def check_owner(owner) -> Checked:
    answer = owner("daily_sales") or {}
    meaning, value = answer.get("meaning"), answer.get("owner")
    if meaning not in MEANINGS:
        rows = [{"test": MESSAGES["meaning_no"].format(meanings=", ".join(f"`{m}`" for m in MEANINGS)), "passes": "no"}]
    elif owners("daily_sales")[meaning] != value:
        rows = [{"test": MESSAGES["value_no"].format(value=value, meaning=meaning, want=owners("daily_sales")[meaning]), "passes": "no"}]
    else:
        rows = [{"test": MESSAGES["meaning"].format(value=value, meaning=meaning), "passes": "yes"}]
    return Checked(rows)


def answers(week: Week, asset: str = "daily_sales") -> Rows:
    """The shop's own answers to the other questions, over the same week."""
    g = graph(week)
    runs = objects(normalise(week_events(week)))
    failed = [f"{r['job']} at {r['ended']}" for r in runs.runs_of(state="FAIL", columns=["job", "ended"])]
    stale = [r["asset"] for r in observe.freshness(week) if r["hours before"] > 24]
    reached = impact.downstream_columns(week, "clean_orders", "customer_id")
    return Rows([
        {"question": f"where did `{asset}` come from?", "answer": ", ".join(upstream(g, asset))},
        {"question": "which assets were last written more than 24 hours before Monday 09:00?", "answer": ", ".join(stale) or MESSAGES["none"]},
        {"question": "which runs failed?", "answer": ", ".join(failed) or MESSAGES["none"]},
        {"question": "which columns does a change to `clean_orders.customer_id` reach?", "answer": ", ".join(_short(r["column"]) for r in reached) or MESSAGES["none"]},
    ])


STUBS = {
    "downstream": '''def downstream(graph, asset):
    return shop.query.next_assets(graph, asset)''',
    "owner": '''def owner(asset):
    return {"owner": shop.query.owners(asset)["account"]}''',
}

REFERENCE = {
    "downstream": '''def downstream(graph, asset):
    found, todo = set(), [asset]
    while todo:
        for nxt in shop.query.next_assets(graph, todo.pop()):
            if nxt not in found:
                found.add(nxt)
                todo.append(nxt)
    return found''',
    "owner": '''def owner(asset):
    return {"owner": shop.query.owners(asset)["responsible"], "meaning": "responsible"}''',
}

__all__ = ["coverage", "graph", "next_assets", "previous_assets", "upstream", "owners", "check_downstream", "check_owner", "answers", "MEANINGS", "WEEK", "STUBS", "REFERENCE"]
