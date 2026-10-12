// Copyright © 2026 Christopher Snow

// The course plan as data: every chapter the plan has, its part, its title and the terms it
// introduces (docs/plan.md, "The parts"). The front page lists every chapter from here; the
// notebooks' tests hold each written chapter to the terms of the chapters after it, and
// plan.test.ts checks this list against docs/plan.md, so the two cannot drift.

export interface PlannedChapter {
  readonly number: number;
  readonly part: number;
  readonly title: string;
  readonly introduces: readonly string[];
}

export const PARTS = [
  "Why metadata exists",
  "Lineage",
  "Deeper lineage",
  "Metadata becomes operational",
  "When the simple model breaks",
  "Building a metadata platform",
  "Real systems",
  "The complete system",
] as const;

const C = (number: number, part: number, title: string, introduces: readonly string[] = []) => ({
  number,
  part,
  title,
  introduces,
});

export const PLAN: readonly PlannedChapter[] = [
  C(1, 1, "The shop and its platform", ["asset"]),
  C(2, 1, "The invisible data system", ["metadata"]),
  C(3, 1, "What is metadata?", ["descriptive", "operational", "schema"]),
  C(4, 1, "Metadata as a model", ["entity", "attribute", "identifier", "dataset"]),
  C(5, 1, "Metadata as a graph", ["graph", "node", "edge", "traversal"]),
  C(6, 2, "What is lineage?", ["lineage", "upstream", "downstream"]),
  C(7, 2, "Jobs, runs and events", ["run", "event"]),
  C(8, 2, "OpenLineage", ["OpenLineage", "facet", "namespace", "producer"]),
  C(9, 2, "From events to graphs", ["ingestion", "normalise"]),
  C(10, 3, "Column-level lineage", ["column lineage"]),
  C(11, 3, "Schema evolution", ["schema evolution", "breaking change"]),
  C(12, 3, "Identity", ["identity", "qualified name", "environment"]),
  C(13, 3, "Runtime metadata", ["observation", "freshness"]),
  C(14, 4, "Data quality as metadata", ["data quality", "assertion"]),
  C(15, 4, "Provenance", ["provenance"]),
  C(16, 4, "Impact analysis", ["impact analysis"]),
  C(17, 4, "Root-cause analysis", ["root cause"]),
  C(18, 5, "Missing events", ["collector", "delivery", "at least once"]),
  C(19, 5, "Duplicate events", ["idempotent", "deduplication"]),
  C(20, 5, "Out-of-order events", ["event time", "arrival time"]),
  C(21, 5, "Conflicting metadata", ["precedence"]),
  C(22, 5, "Identity across systems", ["alias", "entity resolution"]),
  C(23, 5, "Metadata at scale", ["index", "partition", "retention", "compaction"]),
  C(24, 6, "Build the metadata store"),
  C(25, 6, "Build the event collector"),
  C(26, 6, "Build the lineage graph"),
  C(27, 6, "Build the query layer"),
  C(28, 6, "Build the metadata interface"),
  C(29, 7, "OpenLineage in practice"),
  C(30, 7, "Airflow, Spark, dbt and Trino"),
  C(31, 7, "Metadata platforms"),
  C(32, 7, "Metadata for ML and AI"),
  C(33, 8, "Build the whole thing"),
];

/** Every rationed term, with the chapter that introduces it. */
export const TERMS: ReadonlyMap<string, number> = new Map(
  PLAN.flatMap((c) => c.introduces.map((t) => [t, c.number] as const)),
);
