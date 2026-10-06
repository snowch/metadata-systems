// Copyright © 2026 Christopher Snow

// The course plan as data: every chapter the plan has, its part, its title and the terms it
// introduces (docs/plan.md, "The parts"). The front page lists every chapter from here, and the
// content tests hold every written chapter to the terms of the chapters after it, written or
// not, and check this list against docs/plan.md, so the two cannot drift.

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
  C(1, 1, "The invisible data system", ["asset", "metadata"]),
  C(2, 1, "What is metadata?", ["descriptive", "operational", "schema"]),
  C(3, 1, "Metadata as a model", ["entity", "attribute", "identifier", "dataset"]),
  C(4, 1, "Metadata as a graph", ["graph", "node", "edge", "traversal"]),
  C(5, 2, "What is lineage?", ["lineage", "job", "upstream", "downstream"]),
  C(6, 2, "Jobs, runs and events", ["run", "event"]),
  C(7, 2, "OpenLineage", ["OpenLineage", "facet", "namespace", "producer"]),
  C(8, 2, "From events to graphs", ["ingestion", "normalise"]),
  C(9, 3, "Column-level lineage", ["column lineage"]),
  C(10, 3, "Schema evolution", ["schema evolution", "breaking change"]),
  C(11, 3, "Identity", ["identity", "qualified name", "environment"]),
  C(12, 3, "Runtime metadata", ["observation", "freshness"]),
  C(13, 4, "Data quality as metadata", ["data quality", "assertion"]),
  C(14, 4, "Provenance", ["provenance"]),
  C(15, 4, "Impact analysis", ["impact analysis"]),
  C(16, 4, "Root-cause analysis", ["root cause"]),
  C(17, 5, "Missing events", ["delivery", "at least once"]),
  C(18, 5, "Duplicate events", ["idempotent", "deduplication"]),
  C(19, 5, "Out-of-order events", ["event time", "arrival time"]),
  C(20, 5, "Conflicting metadata", ["precedence"]),
  C(21, 5, "Identity across systems", ["alias", "entity resolution"]),
  C(22, 5, "Metadata at scale", ["index", "partition", "retention", "compaction"]),
  C(23, 6, "Build the metadata store"),
  C(24, 6, "Build the event collector", ["collector"]),
  C(25, 6, "Build the lineage graph"),
  C(26, 6, "Build the query layer"),
  C(27, 6, "Build the metadata interface"),
  C(28, 7, "OpenLineage in practice"),
  C(29, 7, "Airflow, Spark, dbt and Trino"),
  C(30, 7, "Metadata platforms"),
  C(31, 7, "Metadata for ML and AI"),
  C(32, 8, "Build the whole thing"),
];

/** Every rationed term, with the chapter that introduces it. */
export const TERMS: ReadonlyMap<string, number> = new Map(
  PLAN.flatMap((c) => c.introduces.map((t) => [t, c.number] as const)),
);

/** A lesson's chapter number: lessons are ordered by chapter within their part. */
export const chapterOf = (lesson: { readonly order: number }) => lesson.order;
