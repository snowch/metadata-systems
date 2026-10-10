# Copyright © 2026 Christopher Snow

"""The shop's data platform, which every figure and query in the notebook runs.

`run_week()` runs the shop's first week, night by night, and returns the platform as the learner
finds it on Monday morning: `storage`, `warehouse` and `reporting`. `run_week(["copy"])`,
`["refunds"]` and `["failed"]` run the week with one of Chapter 1's three changes.
"""

from .data import ARRIVAL, DAYS
from .infer import cleaning_rules_that_fit, day_gap, queries_that_rebuild
from .platform import pounds
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
    "pounds",
    "queries_that_rebuild",
    "run_week",
    "timeline",
]
