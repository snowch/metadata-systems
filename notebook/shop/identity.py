# Copyright © 2026 Christopher Snow

"""When two references name the same asset (Chapter 12).

A reference is how a program, a person or an event names an asset: `shop.analytics.daily_sales`,
`daily_sales`, `s3://shop-raw/orders.jsonl`, or an object with one of its versions,
`s3://shop-returns/r-202.json@<version>`. `resolve` finds what a reference names, by the rules of
the store that holds it, which are the shop's:

- the warehouse reads a name without regard to case, and fills in what a name leaves out from the
  defaults of the connection that uses it: production's are the database `shop` and the schema
  `analytics`. The database `shop_dev` is the development copy (the `dev` change).
- object storage reads a key exactly, case and all. A version is one of the object's versions.

`compare` sets two references side by side under five tests, each the evidence for one reading of
"the same": the same text; the same object in its store; the same rows; the same environment; the
same version. The warehouse keeps no versions of a table, so that test is left empty for a table.
"""

from __future__ import annotations

import hashlib

from .platform import Rows
from .week import DEV_DATABASE, Week

ENVIRONMENTS = {"shop": "production", DEV_DATABASE: "development"}
# What the warehouse's databases are called inside it.
DATABASES = {"shop": "main", DEV_DATABASE: DEV_DATABASE}
DEFAULTS = ("shop", "analytics")

MESSAGES = {
    "nothing": "names nothing",
}


def _rows(week: Week, database: str, table: str) -> str:
    rows = week.warehouse.db.execute(f"SELECT * FROM {DATABASES[database]}.{table} ORDER BY 1, 2").fetchall()
    return hashlib.sha1(repr(rows).encode()).hexdigest()[:12]


def resolve(week: Week, reference: str, defaults: tuple[str, str] = DEFAULTS) -> dict:
    """What a reference names: its store, the object, a fingerprint of its rows, its environment, and
    its version where the store keeps one. `object` is None where it names nothing."""
    if reference.startswith("s3://"):
        key, _, version = reference.partition("@")
        found = [v for v in week.storage.versions(key) if v["key"] == key]
        if not found:
            return {"store": "object storage", "object": None, "rows": None, "environment": None, "version": None}
        if not version:
            version = found[-1]["version"]
        text = week.storage.version_text(key, version)
        return {
            "store": "object storage",
            "object": key,
            "rows": hashlib.sha1(text.encode()).hexdigest()[:12] if text is not None else None,
            "environment": "production",
            "version": version,
        }
    parts = reference.lower().split(".")
    database, schema, table = (list(defaults) + parts)[-3:] if len(parts) < 3 else parts
    if database not in DATABASES or schema != "analytics":
        return {"store": "warehouse", "object": None, "rows": None, "environment": None, "version": None}
    kinds = dict(week.warehouse.db.execute(f"SELECT name, type FROM {DATABASES[database]}.sqlite_master"))
    if table not in kinds:
        return {"store": "warehouse", "object": None, "rows": None, "environment": None, "version": None}
    return {
        "store": "warehouse",
        "object": f"{database}.{schema}.{table}",
        "rows": _rows(week, database, table),
        "environment": ENVIRONMENTS[database],
        "version": None,
    }


def _same(a, b) -> str:
    if a is None and b is None:
        return ""
    return "yes" if a == b else "no"


def compare(week: Week, pairs: list[tuple[str, str]]) -> Rows:
    """Each pair of references under the five tests."""
    out = []
    for k, (a, b) in enumerate(pairs, start=1):
        x, y = resolve(week, a), resolve(week, b)
        named = x["object"] is not None and y["object"] is not None
        out.append(
            {
                "pair": k,
                "same text": "yes" if a == b else "no",
                "same object": "yes" if named and x["object"] == y["object"] else "no",
                "same rows": _same(x["rows"], y["rows"]) if named else "no",
                "same environment": _same(x["environment"], y["environment"]) if named else "",
                "same version": _same(x["version"], y["version"]) if named else "",
            }
        )
    return Rows(out)


def references(week: Week, pairs: list[tuple[str, str]]) -> Rows:
    """Each pair, and what each of its references names."""
    out = []
    for k, (a, b) in enumerate(pairs, start=1):
        for ref in (a, b):
            r = resolve(week, ref)
            out.append({"pair": k, "reference": ref, "names": r["object"] or MESSAGES["nothing"]})
    return Rows(out)


__all__ = ["DEFAULTS", "compare", "references", "resolve"]
