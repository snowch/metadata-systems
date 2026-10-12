# Copyright © 2026 Christopher Snow

"""The shop's data platform, which every figure and query in the notebook runs.

`run_week()` runs the shop's first week, night by night, and returns the platform as the learner
finds it on Monday morning: `storage`, `warehouse` and `reporting`. `run_week(["copy"])`,
`["refunds"]` and `["failed"]` run the week with one of Chapter 2's three changes, and
`["column"]` with Chapter 3's. `records`, `typed_records` and `model` read the records a person
writes about the shop (Chapters 3 and 4).
"""

from .data import ARRIVAL, DAYS
from .infer import cleaning_rules_that_fit, day_gap, queries_that_rebuild
from .platform import pounds
from .records import model, owners, records, typed_records
from .week import CHANGES, COPY, FILES, NIGHTS, Week, run_week, timeline

__all__ = [
    "ARRIVAL",
    "CHANGES",
    "COPY",
    "DAYS",
    "FILES",
    "NIGHTS",
    "Week",
    "cleaning_rules_that_fit",
    "day_gap",
    "model",
    "owners",
    "pounds",
    "queries_that_rebuild",
    "records",
    "run_week",
    "timeline",
    "typed_records",
]
