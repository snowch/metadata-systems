# Copyright © 2026 Christopher Snow

"""Which references across the shop's systems name one asset (Chapter 22).

Six references come into the shop's metadata system, each from a system that names things its own
way (`REFERENCES`): the warehouse's catalogue, the events (a namespace and a name), the development
database's catalogue (the `dev` change), the transformation tool the shop's developer has started to
use, which names each program's output by a model, the reporting tool's dataset behind the
dashboard, and a CSV file Jo Marsh exported from `daily_sales` into `shop-scratch`.

`merge` groups them into entities by one rule:

- `exact`: the same text;
- `qualified`: a warehouse name read by the warehouse's rules (Chapter 12): case ignored, the
  connection's defaults filled in, and an event's namespace and name taken as the warehouse and the
  name; a reference the rule cannot read stays alone;
- `last part`: the last part of the name, lower case, with spaces and hyphens read as underscores;
- `aliases`: `qualified`, then the aliases each system's own configuration states: the transformation
  tool's model says which table it builds, and the reporting tool's dataset which table it reads.

Every system, name and rule here is the shop's own, invented for the course.
"""

from __future__ import annotations

import re

from .platform import Rows

WAREHOUSE_NAMESPACE = "warehouse://shop-warehouse"
REFERENCES = (
    ("warehouse", "shop.analytics.daily_sales"),
    ("events", f"{WAREHOUSE_NAMESPACE}/shop.analytics.daily_sales"),
    ("development warehouse", "shop_dev.analytics.daily_sales"),
    ("transformation tool", "shop_models:daily_sales"),
    ("reporting tool", "dataset:Daily sales"),
    ("object storage", "s3://shop-scratch/daily_sales.csv"),
)
# What each system's own configuration says a reference stands for.
CONFIGURED = {
    "shop_models:daily_sales": "shop.analytics.daily_sales",
    "dataset:Daily sales": "shop.analytics.daily_sales",
}
RULES = ("exact", "qualified", "last part", "aliases")


def _qualified(ref: str) -> str | None:
    """A warehouse name by the warehouse's rules, or None where the reference is not one."""
    if ref.startswith(WAREHOUSE_NAMESPACE + "/"):
        ref = ref[len(WAREHOUSE_NAMESPACE) + 1 :]
    if ":" in ref or "/" in ref or " " in ref:
        return None
    parts = ref.lower().split(".")
    return ".".join((["shop", "analytics"] + parts)[-3:])


def _last(ref: str) -> str:
    name = re.split(r"[/:.]", ref)[-1] if not ref.endswith(".csv") else ref.rsplit("/", 1)[-1][: -len(".csv")]
    return re.sub(r"[ -]", "_", name.lower())


def key(ref: str, rule: str) -> str:
    """The key `rule` gives a reference; references with one key are merged into one entity."""
    if rule == "exact":
        return ref
    if rule == "qualified":
        return _qualified(ref) or ref
    if rule == "last part":
        return _last(ref)
    if rule == "aliases":
        return _qualified(CONFIGURED.get(ref, ref)) or ref
    raise ValueError(f"no rule {rule!r}: {', '.join(RULES)}")


def references() -> Rows:
    """The six references, and the system each came from."""
    return Rows({"system": s, "reference": r} for s, r in REFERENCES)


def merge(rule: str, refs=REFERENCES) -> Rows:
    """The entities `rule` makes of the references: each entity, numbered in order of its first
    reference, with the references merged into it and the systems they came from."""
    entities: dict[str, list[tuple[str, str]]] = {}
    for system, ref in refs:
        entities.setdefault(key(ref, rule), []).append((system, ref))
    return Rows(
        {"entity": i + 1, "references": len(members), "systems": ", ".join(s for s, _ in members)}
        for i, members in enumerate(entities.values())
    )


__all__ = ["references", "merge", "key", "RULES", "REFERENCES"]
