# Copyright © 2026 Christopher Snow

"""The week's metadata as one store, in four shapes, each asked the same question (Chapter 24).

The store holds the week with the returns desk: each job's runs and its edges by job (Chapter 9),
and the descriptive lines Chapter 4 ended with for the assets that have them. Four shapes:

- `documents`: one JSON document per job (its runs, what it reads, what it writes) and one per
  dataset (its descriptive fields). Going through the documents counts each one read.
- `tables`: SQLite tables `edges(job, edge, dataset, runs)` and `descriptions(asset, field,
  value)`. What a query reads is taken from SQLite's own query plan: a scan reads every row of the
  table; a search through an index reads the index's entries for the value it looks up.
- the same tables with an index the learner adds;
- `graph`: Chapter 5's shape, a node for each job and dataset and an edge for each edge by job;
  `edges_at(name)` gives one node's edges and counts each one read.

The question each shape answers is what reads a dataset. The learner writes it for each shape, and
`check` runs it for every dataset in the week against the answer from Chapter 9's edges. Each
shape's stub (`STUBS`) gives a wrong answer and the reference (`REFERENCE`) the right one; the
course's tests hold both to `check`.

The shapes, the counting and the rule for reading a query plan are the shop's own.
"""

from __future__ import annotations

import json
import sqlite3

from .delivery import week_events
from .ingest import edges, normalise, objects
from .platform import Rows
from .week import Week

# Chapter 4's descriptive lines, with identifiers, for the assets the edges name.
DESCRIBED = {
    "warehouse://shop-warehouse/shop.analytics.daily_sales": {
        "means": "the value of every completed order placed that day, by its UTC date",
        "responsible": "j.marsh",
    },
    "reporting://shop-reporting/sales_dashboard": {"responsible": "j.marsh"},
}

MESSAGES = {
    "right": "right",
    "wrong": "expected {expected}",
    "summary": "{right} of {total} datasets right; {read} {unit} read in all.",
    "scan": "reads every row of `{table}`",
    "search": "uses the index `{index}`",
    "no_query": "The query must take the dataset as :dataset.",
}


def _week_edges(week: Week) -> Rows:
    return edges(objects(normalise(week_events(week)))).by_job


def _runs(week: Week) -> dict[str, int]:
    return {j["job"]: j["runs"] for j in objects(normalise(week_events(week))).jobs.values()}


class Documents(list):
    """The documents, one per job and one per dataset. Going through them counts each one read."""

    def __init__(self, docs) -> None:
        super().__init__(docs)
        self.read = 0

    def __iter__(self):
        for d in super().__iter__():
            self.read += 1
            yield d

    def get(self, name: str) -> dict | None:
        """The document for one job or dataset, found by its name: one document read."""
        self.read += 1
        return next((d for d in list.__iter__(self) if d.get("job") == name or d.get("dataset") == name), None)

    def __str__(self) -> str:
        return "\n".join(json.dumps(d) for d in list.__iter__(self))


def documents(week: Week) -> Documents:
    by_job = _week_edges(week)
    runs = _runs(week)
    docs = []
    for job in sorted({r["job"] for r in by_job}):
        docs.append({
            "job": job,
            "runs": runs.get(job, 0),
            "reads": [r["dataset"] for r in by_job if r["job"] == job and r["edge"] == "reads"],
            "writes": [r["dataset"] for r in by_job if r["job"] == job and r["edge"] == "writes"],
        })
    for dataset in sorted({r["dataset"] for r in by_job}):
        docs.append({"dataset": dataset, **DESCRIBED.get(dataset, {})})
    return Documents(docs)


class Tables:
    """The week's edges and descriptions as SQLite tables, in memory."""

    def __init__(self, week: Week) -> None:
        self.db = sqlite3.connect(":memory:")
        self.db.execute("CREATE TABLE edges (job TEXT, edge TEXT, dataset TEXT, runs INTEGER)")
        self.db.execute("CREATE TABLE descriptions (asset TEXT, field TEXT, value TEXT)")
        self.db.executemany(
            "INSERT INTO edges VALUES (?, ?, ?, ?)",
            [(r["job"], r["edge"], r["dataset"], r["runs"]) for r in _week_edges(week)],
        )
        self.db.executemany(
            "INSERT INTO descriptions VALUES (?, ?, ?)",
            [(a, f, v) for a, fields in DESCRIBED.items() for f, v in fields.items()],
        )

    def sql(self, query: str, **params) -> Rows | None:
        """A query's rows; nothing for a statement that returns no rows, such as `CREATE INDEX`."""
        cur = self.db.execute(query, params)
        if cur.description is None:
            return None
        names = [d[0] for d in cur.description]
        return Rows(dict(zip(names, row)) for row in cur.fetchall())

    def plan(self, query: str, **params) -> list[str]:
        """SQLite's plan for the query: one line per step."""
        return [row[-1] for row in self.db.execute("EXPLAIN QUERY PLAN " + query, params).fetchall()]

    def rows_read(self, query: str, **params) -> tuple[int, str]:
        """How many rows the query reads, from its plan, and the plan in words."""
        steps = self.plan(query, **params)
        total = self.db.execute("SELECT COUNT(*) FROM edges").fetchone()[0]
        for step in steps:
            if step.startswith("SEARCH") and "INDEX" in step:
                index = step.split("INDEX", 1)[1].split()[0]
                column = self.db.execute(f"PRAGMA index_info({index})").fetchone()[2]
                value = params.get(column)
                n = self.db.execute(f"SELECT COUNT(*) FROM edges WHERE {column} = ?", (value,)).fetchone()[0]
                return n, MESSAGES["search"].format(index=index)
        return total, MESSAGES["scan"].format(table="edges")

    def _repr_html_(self) -> str:
        return self.sql("SELECT * FROM edges")._repr_html_()


def tables(week: Week) -> Tables:
    return Tables(week)


class Graph:
    """A node for each job and dataset, and an edge for each edge by job. Reading a node's edges
    counts each edge read."""

    def __init__(self, week: Week) -> None:
        self.edges = [{"job": r["job"], "edge": r["edge"], "dataset": r["dataset"]} for r in _week_edges(week)]
        self.read = 0

    def edges_at(self, name: str) -> list[dict]:
        """Every edge with the job or dataset `name` at one end."""
        found = [e for e in self.edges if name in (e["job"], e["dataset"])]
        self.read += len(found)
        return found

    def _repr_html_(self) -> str:
        return Rows(self.edges)._repr_html_()


def graph(week: Week) -> Graph:
    return Graph(week)


STUBS = {
    "documents": '''def readers_of(documents, dataset):
    found = []
    for doc in documents:
        pass  # add doc["job"] when the document's "reads" lists the dataset
    return found''',
    "tables": '''query = "SELECT job FROM edges"''',
    "index": '''tables.sql("CREATE INDEX IF NOT EXISTS edges_by_job ON edges(job)")''',
    "graph": '''def readers_of(graph, dataset):
    return [e["job"] for e in graph.edges_at(dataset)]''',
}

REFERENCE = {
    "documents": '''def readers_of(documents, dataset):
    found = []
    for doc in documents:
        if dataset in doc.get("reads", []):
            found.append(doc["job"])
    return found''',
    "tables": '''query = "SELECT job FROM edges WHERE edge = 'reads' AND dataset = :dataset"''',
    "index": '''tables.sql("CREATE INDEX IF NOT EXISTS edges_by_dataset ON edges(dataset)")''',
    "graph": '''def readers_of(graph, dataset):
    return [e["job"] for e in graph.edges_at(dataset) if e["edge"] == "reads"]''',
}


def expected(week: Week) -> dict[str, list[str]]:
    """What reads each dataset, from Chapter 9's edges by job."""
    by_job = _week_edges(week)
    return {d: sorted(r["job"] for r in by_job if r["dataset"] == d and r["edge"] == "reads") for d in sorted({r["dataset"] for r in by_job})}


class Checked(Rows):
    """One row per dataset, and the totals."""

    def __init__(self, rows, right: int, total: int, read: int, unit: str, plan: str | None = None) -> None:
        super().__init__(rows, null="")
        self.right, self.total, self.read, self.unit, self.plan = right, total, read, unit, plan

    @property
    def passed(self) -> bool:
        return self.right == self.total

    def _repr_html_(self) -> str:
        head = MESSAGES["summary"].format(right=self.right, total=self.total, read=self.read, unit=self.unit)
        if self.plan:
            head += f" The query {self.plan}" + ("" if self.plan.endswith(".") else ".")
        return f"<p>{head}</p>" + super()._repr_html_()


def _short(name: str) -> str:
    return name.rsplit("/", 1)[-1].removeprefix("shop.analytics.")


def check(week: Week, store, answer) -> Checked:
    """Runs the learner's answer for every dataset in the week: `answer` is a function
    `readers_of(store, dataset)` for documents or a graph, or a query string for tables."""
    want = expected(week)
    rows, right, plan = [], 0, None
    if isinstance(store, Tables):
        read = 0
        for d, jobs in want.items():
            if ":dataset" not in answer:
                got: list[str] = []
            else:
                got = sorted(r["job"] for r in store.sql(answer, dataset=d))
            n, plan = store.rows_read(answer, dataset=d) if ":dataset" in answer else store.rows_read(answer)
            read += n
            ok = got == jobs
            right += ok
            rows.append({"dataset": _short(d), "yours": ", ".join(map(_short, got)), "rows read": n, "": MESSAGES["right"] if ok else MESSAGES["wrong"].format(expected=", ".join(map(_short, jobs)) or "none")})
        if ":dataset" not in answer:
            plan = f"{plan}. {MESSAGES['no_query']}"
        return Checked(rows, right, len(want), read, "rows", plan)
    store.read = 0
    for d, jobs in want.items():
        before = store.read
        got = sorted(answer(store, d))
        ok = got == jobs
        right += ok
        rows.append({"dataset": _short(d), "yours": ", ".join(map(_short, got)), "read": store.read - before, "": MESSAGES["right"] if ok else MESSAGES["wrong"].format(expected=", ".join(map(_short, jobs)) or "none")})
    unit = "documents" if isinstance(store, Documents) else "edges"
    return Checked(rows, right, len(want), store.read, unit)


def compare(week: Week, dataset: str, job: str) -> Rows:
    """Records read by each shape for two questions: what reads `dataset`, and what `job` reads;
    each answered by the shop's own code, with the index on `dataset` in place."""
    docs, tab, g = documents(week), tables(week), graph(week)
    tab.sql("CREATE INDEX IF NOT EXISTS edges_by_dataset ON edges(dataset)")
    out = []
    docs.read = 0
    [d for d in docs if dataset in d.get("reads", [])]
    by_dataset_docs = docs.read
    docs.read = 0
    docs.get(job)
    by_job_docs = docs.read
    q1 = "SELECT job FROM edges WHERE edge = 'reads' AND dataset = :dataset"
    q2 = "SELECT dataset FROM edges WHERE edge = 'reads' AND job = :job"
    g.read = 0
    g.edges_at(dataset)
    by_dataset_graph = g.read
    g.read = 0
    g.edges_at(job)
    by_job_graph = g.read
    out.append({"question": f"what reads {_short(dataset)}", "documents": by_dataset_docs, "table with the index": tab.rows_read(q1, dataset=dataset)[0], "graph": by_dataset_graph})
    out.append({"question": f"what {_short(job)} reads", "documents": by_job_docs, "table with the index": tab.rows_read(q2, job=job)[0], "graph": by_job_graph})
    return Rows(out)


__all__ = ["documents", "tables", "graph", "check", "compare", "expected", "STUBS", "REFERENCE"]
