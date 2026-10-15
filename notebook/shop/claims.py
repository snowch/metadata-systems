# Copyright © 2026 Christopher Snow

"""What three of the shop's sources say about one table, and rules for choosing between them
(Chapter 21).

A claim is one source's statement of one attribute of one asset: who its owner is, or which columns
it has. Each claim keeps two times: when the source sent it (`sent`), and when the source's content
was last changed (`as of`). The shop's metadata system takes claims about `daily_sales` from three
sources:

- the warehouse: its catalogue, read every night at `CATALOGUE_SYNC`; its owner is the account that
  created the table, and its columns are the table's;
- the records: the descriptive records you keep (Chapters 3 and 4), sent when they change;
- the team sheet: a spreadsheet of owners and columns that the engineer who built the platform wrote
  before the shop opened, naming a "data team" that left with them; nobody has edited it since. It
  is imported every night at `SHEET_IMPORT`, and each import sends every row again.

`resolve` chooses a value for each attribute by one rule: the claim sent most recently (`newest`),
the claim whose source changed most recently (`as of`), the claim of the source ranked first for that
attribute (`ranked`), or every claim with its source (`all`).

Every source, time and rule here is the shop's own, invented for the course.
"""

from __future__ import annotations

from .platform import Rows, epoch, iso
from .week import NIGHTS

TABLE = "daily_sales"
CATALOGUE_SYNC = "03:30"
SHEET_IMPORT = "04:00"
# When each night's work changes `daily_sales` (the time of day; Chapter 2's last-altered time).
TABLE_ALTERED = "2026-09-14T02:30:21Z"
# When you last changed the records (Chapter 4's, with identifiers).
RECORDS_CHANGED = "2026-09-14T16:40:00Z"
# The team sheet: last edited in August, before the shop opened.
SHEET_EDITED = "2026-08-28T17:05:00Z"

SOURCES = {
    "warehouse": {"owner": "etlsvc/batch01.corp.internal@CORP.INTERNAL", "columns": "day, revenue_pence"},
    "records": {"owner": "j.marsh"},
    "team sheet": {"owner": "data team", "columns": "day, revenue"},
}
# The `ranked` rule's order, attribute by attribute: the shop's choice.
RANKS = {"owner": ("records", "team sheet", "warehouse"), "columns": ("warehouse", "records", "team sheet")}

MESSAGES = {"no_claims": "No source had sent a claim by then."}


def _sends(daily: str, at: str) -> list[str]:
    """The times of a nightly sending at `daily` (HH:MM), on each night up to `at`."""
    days = sorted({n for n in NIGHTS} | {at[:10]})
    return [t for t in (f"{d}T{daily}:00Z" for d in days) if epoch(t) <= epoch(at)]


def claims(at: str) -> Rows:
    """Every claim about `daily_sales` the shop's metadata system holds at `at`: the latest sending of
    each source's claim of each attribute."""
    out = []
    for source, attrs in SOURCES.items():
        if source == "warehouse":
            sends = _sends(CATALOGUE_SYNC, at)
            # The night's work changes the table before each read of the catalogue.
            as_of = f"{sends[-1][:10]}T{TABLE_ALTERED[11:]}" if sends else None
        elif source == "team sheet":
            sends, as_of = _sends(SHEET_IMPORT, at), SHEET_EDITED
        else:
            sends, as_of = ([RECORDS_CHANGED] if epoch(RECORDS_CHANGED) <= epoch(at) else []), RECORDS_CHANGED
        if not sends:
            continue
        for attribute, value in attrs.items():
            out.append({"attribute": attribute, "value": value, "source": source, "sent": sends[-1], "as of": as_of})
    return Rows(sorted(out, key=lambda r: (r["attribute"], r["source"])), empty=MESSAGES["no_claims"])


def resolve(held: Rows, rule: str = "newest", ranks: dict | None = None) -> Rows:
    """One value for each attribute, chosen from the claims by `rule`: `newest`, `as of`, `ranked` or
    `all`; with the source it came from."""
    ranks = RANKS if ranks is None else ranks
    out = []
    for attribute in sorted({c["attribute"] for c in held}):
        mine = [c for c in held if c["attribute"] == attribute]
        if rule == "all":
            out += [{"attribute": attribute, "value": c["value"], "source": c["source"], "sent": c["sent"], "as of": c["as of"]} for c in mine]
            continue
        if rule == "newest":
            best = max(mine, key=lambda c: (epoch(c["sent"]), c["source"]))
        elif rule == "as of":
            best = max(mine, key=lambda c: (epoch(c["as of"]), c["source"]))
        elif rule == "ranked":
            order = ranks[attribute]
            best = min(mine, key=lambda c: order.index(c["source"]) if c["source"] in order else len(order))
        else:
            raise ValueError(f"no rule {rule!r}: newest, as of, ranked or all")
        out.append({"attribute": attribute, "value": best["value"], "source": best["source"]})
    return Rows(out)


__all__ = ["claims", "resolve", "SOURCES", "RANKS"]
