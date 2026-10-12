# Copyright © 2026 Christopher Snow

"""The shop's data platform, which every figure and query in the notebook runs.

`run_week()` runs the shop's first week, night by night, and returns the platform as the learner
finds it on Monday morning: `storage`, `warehouse` and `reporting`. `run_week(["copy"])`,
`["refunds"]` and `["failed"]` run the week with one of Chapter 2's three changes, and
`["column"]` with Chapter 3's and `["source"]` with Chapter 6's. `records`, `typed_records` and `model` read the records a person
writes about the shop (Chapters 3 and 4); `graph` makes them a graph (Chapters 5 and 6), and
`repository` gives the jobs' code (Chapter 6). `["returns"]` adds the returns desk (Chapter 7 on).
`events`, `runs`, `readings` and `lineage` are Chapter 7's runs and their events; `openlineage`
holds Chapter 8's run events, check and consumer; `ingest` is Chapter 9's pipeline. `columns`,
`schemas`, `identity` and `observe` are Part III's: column lineage, schema versions, references,
and what runs recorded with how recent each asset is. `quality`, `provenance`, `impact` and `cause`
are Part IV's. `delivery`, `claims`, `aliases` and `scale` are Part V's: the path events travel and
what goes wrong on it, claims from several sources, references across systems, and cost as the
platform grows.
"""

from .data import ARRIVAL, DAYS
from .infer import cleaning_rules_that_fit, day_gap, queries_that_rebuild
from .platform import pounds
from .graph import compare_with_code, graph
from . import aliases, cause, claims, columns, delivery, identity, impact, ingest, observe, openlineage, provenance, quality, scale, schemas
from .records import model, owners, records, typed_records
from .runs import event_fields, events, lineage, readings, runs
from .week import CHANGES, COPY, FILES, NIGHTS, Week, reads_and_writes, repository, run_week, timeline

__all__ = [
    "ARRIVAL",
    "CHANGES",
    "COPY",
    "DAYS",
    "FILES",
    "NIGHTS",
    "Week",
    "aliases",
    "cause",
    "claims",
    "cleaning_rules_that_fit",
    "columns",
    "compare_with_code",
    "day_gap",
    "delivery",
    "event_fields",
    "events",
    "identity",
    "impact",
    "ingest",
    "lineage",
    "observe",
    "openlineage",
    "provenance",
    "quality",
    "readings",
    "runs",
    "scale",
    "schemas",
    "graph",
    "model",
    "owners",
    "pounds",
    "queries_that_rebuild",
    "reads_and_writes",
    "records",
    "repository",
    "run_week",
    "timeline",
    "typed_records",
]
