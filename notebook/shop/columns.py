# Copyright © 2026 Christopher Snow

"""Which columns each column is made from, read from the programs' SQL (Chapter 10).

The shop's parser reads the course's small SQL: `SELECT [DISTINCT] ... FROM one source [WHERE ...]
[GROUP BY ...] [ORDER BY ...]`, with `WITH name AS (...)` before it, inside a program's code in
the repository's notation (`read`, `write`, `refresh`, `change`). For every column a program writes
it records the columns it reads, of two kinds, which are the shop's own names:

- `value`: the column's value is computed from the input column: `copied`, `computed` (by an
  expression or a function) or `aggregated` (by SUM, COUNT and the like, over many rows);
- `rows`: the input column decides which rows there are: a `filter` (WHERE), a `grouping`
  (GROUP BY), or `distinct` (SELECT DISTINCT, which keeps one row of each set of equal values).

ORDER BY changes no value and no row, and the parser records nothing for it. A function's value is
taken to depend on its arguments and on nothing else: the parser cannot see into a function, so a
function that reads a table hides that table. `SELECT *` names no column: without the columns of its
source, the parser records the source's columns as `*` and does not guess them.

A table's columns are matched to the SELECT by position, as the warehouse's INSERT matches them:
without the warehouse's catalogue the parser cannot name them, and calls them `column 1` and so on.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field

from .platform import Rows, Warehouse
from .week import ANALYST_SQL, COPY, Week, repository

KEYWORDS = {
    "SELECT", "DISTINCT", "FROM", "WHERE", "GROUP", "BY", "ORDER", "AS", "AND", "OR", "NOT", "IS",
    "NULL", "WITH", "IN", "LIKE", "ASC", "DESC", "INSERT", "INTO", "DELETE", "VALUES", "BETWEEN",
}
AGGREGATES = {"SUM", "COUNT", "MIN", "MAX", "AVG", "TOTAL"}
# How a value is made, from the least to the most changed: a value copied, then computed, then
# aggregated is, in the end, aggregated.
_RANK = ["copied", "computed", "aggregated"]

# The analyst's script, as the analyst sends it (Chapter 10): it is not in the shop's repository.
ANALYST_COPY = f'write("{COPY}", """\n{ANALYST_SQL}\n""")\n'

_TOKEN = re.compile(r"\s+|'(?:[^']|'')*'|\d+(?:\.\d+)?|:\w+|[A-Za-z_][\w]*(?:\.[A-Za-z_*][\w]*)*|<>|>=|<=|[=<>*+\-/(),;]")


def _tokens(sql: str) -> list[str]:
    out, at = [], 0
    while at < len(sql):
        m = _TOKEN.match(sql, at)
        if not m:
            raise ValueError(f"the shop's parser cannot read {sql[at:at + 20]!r}")
        if not m.group().isspace():
            out.append(m.group())
        at = m.end()
    return out


def _is_name(t: str) -> bool:
    return bool(re.match(r"[A-Za-z_]", t)) and t.upper() not in KEYWORDS


@dataclass
class Item:
    """One expression of a SELECT list: the columns it uses, and how."""

    name: str | None
    columns: list[str]
    how: str  # copied, computed, aggregated, or star


@dataclass
class Select:
    distinct: bool
    items: list[Item]
    source: str
    rows: list[tuple[str, str]] = field(default_factory=list)  # (column, filter|grouping)


def _split(tokens: list[str], at_words: tuple[str, ...]) -> tuple[list[str], list[str]]:
    """Tokens up to the first of `at_words` outside brackets, and the rest."""
    depth = 0
    for i, t in enumerate(tokens):
        depth += t == "("
        depth -= t == ")"
        if depth == 0 and t.upper() in at_words:
            return tokens[:i], tokens[i:]
    return tokens, []


def _commas(tokens: list[str]) -> list[list[str]]:
    parts, depth, cur = [], 0, []
    for t in tokens:
        if t == "," and depth == 0:
            parts.append(cur)
            cur = []
            continue
        depth += t == "("
        depth -= t == ")"
        cur.append(t)
    if cur:
        parts.append(cur)
    return parts


def _used(tokens: list[str]) -> tuple[list[str], set[str]]:
    """The columns an expression names, in order, and the functions it calls."""
    cols, funcs = [], set()
    for i, t in enumerate(tokens):
        if not _is_name(t):
            continue
        if i + 1 < len(tokens) and tokens[i + 1] == "(":
            funcs.add(t.upper())
            continue
        name = t.split(".")[-1]
        if name not in cols:
            cols.append(name)
    return cols, funcs


def _item(tokens: list[str]) -> Item:
    name = None
    if len(tokens) >= 3 and tokens[-2].upper() == "AS":
        name, tokens = tokens[-1], tokens[:-2]
    if tokens == ["*"]:
        return Item(name, ["*"], "star")
    cols, funcs = _used(tokens)
    if len(tokens) == 1 and cols:
        return Item(name or cols[0], cols, "copied")
    how = "aggregated" if funcs & AGGREGATES else "computed"
    return Item(name, cols, how)


def _select(tokens: list[str]) -> Select:
    if not tokens or tokens[0].upper() != "SELECT":
        raise ValueError("the shop's parser reads a SELECT")
    tokens = tokens[1:]
    distinct = bool(tokens) and tokens[0].upper() == "DISTINCT"
    if distinct:
        tokens = tokens[1:]
    items, rest = _split(tokens, ("FROM",))
    if not rest or len(rest) < 2:
        raise ValueError("the shop's parser reads a SELECT with a FROM")
    source, rest = rest[1], rest[2:]
    if rest and rest[0].upper() in ("JOIN", ","):
        raise ValueError("the shop's parser reads one source per SELECT")
    select = Select(distinct, [_item(i) for i in _commas(items)], source.split(".")[-1])
    while rest:
        word = rest[0].upper()
        if word == "WHERE":
            part, rest = _split(rest[1:], ("GROUP", "ORDER"))
            select.rows += [(c, "filter") for c in _used(part)[0]]
        elif word == "GROUP":
            part, rest = _split(rest[2:], ("ORDER",))
            select.rows += [(c, "grouping") for c in _used(part)[0]]
        elif word == "ORDER":
            rest = []
        else:
            raise ValueError(f"the shop's parser does not read {rest[0]!r} here")
    return select


def _query(tokens: list[str]) -> tuple[dict[str, Select], Select]:
    """A query's named SELECTs (from WITH) and its last SELECT."""
    named: dict[str, Select] = {}
    if tokens and tokens[0].upper() == "WITH":
        tokens = tokens[1:]
        while True:
            name = tokens[0]
            if tokens[1].upper() != "AS" or tokens[2] != "(":
                raise ValueError("the shop's parser reads WITH name AS (SELECT ...)")
            depth, end = 0, 2
            for end in range(2, len(tokens)):
                depth += tokens[end] == "("
                depth -= tokens[end] == ")"
                if depth == 0:
                    break
            named[name] = _select(tokens[3:end])
            tokens = tokens[end + 1 :]
            if tokens and tokens[0] == ",":
                tokens = tokens[1:]
                continue
            break
    return named, _select(tokens)


@dataclass(frozen=True)
class Dep:
    """One input column of one output column."""

    output: str
    dataset: str
    column: str
    kind: str  # value or rows
    how: str


def _outputs(select: Select, named: dict[str, Select], catalogue) -> list[tuple[str | None, set[tuple[str, str, str, str]]]]:
    """Each output of a SELECT, with its dependencies on (dataset, column, kind, how), through WITH."""

    def deps_of(sel: Select, column: str) -> set[tuple[str, str, str, str]]:
        """What a column named in `sel` depends on, followed back through the names WITH defines."""
        if sel.source not in named:
            return {(sel.source, column, "value", "copied")}
        inner = named[sel.source]
        out: set[tuple[str, str, str, str]] = set()
        for name, deps in _outputs(inner, named, catalogue):
            if name == column:
                out |= deps
        if not out:
            raise ValueError(f"{sel.source} has no column {column}")
        return out

    def through(sel: Select, column: str, kind: str, how: str) -> set[tuple[str, str, str, str]]:
        out = set()
        for d, c, k, h in deps_of(sel, column):
            if kind == "rows":
                out.add((d, c, "rows", how if k == "value" else h))
            elif k == "rows":
                out.add((d, c, "rows", h))
            else:
                out.add((d, c, "value", max(h, how, key=_RANK.index)))
        return out

    rows: set[tuple[str, str, str, str]] = set()
    for column, how in select.rows:
        rows |= through(select, column, "rows", how)
    if select.distinct:
        for item in select.items:
            for column in item.columns:
                if column != "*":
                    rows |= through(select, column, "rows", "distinct")
    # Rows decided inside a named SELECT decide the rows of everything made from it.
    if select.source in named:
        for name, deps in _outputs(named[select.source], named, catalogue):
            rows |= {d for d in deps if d[2] == "rows"}

    out = []
    for item in select.items:
        if item.how == "star":
            if select.source in named:
                names = [n for n, _ in _outputs(named[select.source], named, catalogue)]
            else:
                names = catalogue(select.source) if catalogue else None
            if names is None:
                out.append(("*", {(select.source, "*", "value", "copied")} | rows))
                continue
            for name in names:
                out.append((name, through(select, name, "value", "copied") | rows))
            continue
        deps = set()
        for column in item.columns:
            deps |= through(select, column, "value", item.how)
        out.append((item.name, deps | rows))
    return out


_READ = re.compile(r'^(\w+) = read\(("[^"]+"|\w+)\)', re.M)
_WRITE = re.compile(r'^(write|refresh|change)\("([^"]+)", """(.*?)"""', re.M | re.S)


def _catalogue(warehouse: Warehouse | None):
    if warehouse is None:
        return None

    def columns(table: str) -> list[str] | None:
        found = [
            r["column_name"]
            for r in warehouse.sql(
                "SELECT column_name FROM information_schema.columns WHERE table_name = :t ORDER BY ordinal_position", t=table
            )
        ]
        return found or None

    return columns


def _name(dataset: str) -> str:
    """A dataset as the page shows it: a table by its name, a file by its file name."""
    return dataset.rsplit("/", 1)[-1]


def deps(code: str, catalogue: Warehouse | None = None) -> tuple[str, list[Dep]]:
    """What one program writes, and every column dependency in its code."""
    files = {name: uri.strip('"') for name, uri in _READ.findall(code)}
    columns_of = _catalogue(catalogue)
    m = _WRITE.search(code)
    if not m:
        return "", []
    verb, target, sql = m.groups()
    out: list[Dep] = []
    for statement in (s.strip() for s in sql.split(";")):
        tokens = _tokens(statement)
        if not tokens or tokens[0].upper() == "DELETE":
            continue
        writes = target
        if tokens[0].upper() == "INSERT":
            writes, tokens = tokens[2], tokens[3:]
        named, select = _query(tokens)
        outputs = _outputs(select, named, columns_of)
        is_table = verb != "refresh" and not writes.startswith("s3://")
        if is_table:
            names = columns_of(writes) if columns_of else None
            if names is None or len(names) < len(outputs):
                names = [f"column {i + 1}" for i in range(len(outputs))]
            outputs = [(names[i], d) for i, (_, d) in enumerate(outputs)]
        for name, ds in outputs:
            for dataset, column, kind, how in sorted(ds):
                out.append(Dep(name or "?", files.get(dataset, dataset), column, kind, how))
    return target, out


def lineage(code: str, catalogue: Warehouse | None = None) -> Rows:
    """The column lineage of one program's code: each column it writes, and each column it reads."""
    target, found = deps(code, catalogue)
    return Rows(
        {"column": f"{_name(target)}.{d.output}", "from": f"{_name(d.dataset)}.{d.column}", "kind": d.kind, "how": d.how}
        for d in found
    )


def programs(week: Week) -> list[dict]:
    """The code of every program whose SQL the shop has: the repository's, and the analyst's script."""
    rows = list(repository(week))
    if "copy" in week.changes:
        rows.append({"job": "copy_clean_orders", "file": "the analyst's script", "code": ANALYST_COPY})
    return rows


def upstream(week: Week, dataset: str, column: str, catalogue: Warehouse | None = None) -> Rows:
    """Every column upstream of one column, through every program whose code the shop has.

    `value` says whether the column's value is computed from it, through every step; `rows` says
    where it decides which rows count, as `how in program`.
    """
    writers = {}
    for p in programs(week):
        target, found = deps(p["code"], catalogue)
        writers.setdefault(target, []).append((p["job"], found))

    found: dict[tuple[str, str], dict] = {}
    order: list[tuple[str, str]] = []

    def visit(ds: str, col: str, kind: str, reasons: frozenset[str], seen: frozenset) -> None:
        for job, deps_ in writers.get(ds, []):
            for d in deps_:
                if d.output != col and not (col == "*" or d.output == "*"):
                    continue
                k = "rows" if (kind == "rows" or d.kind == "rows") else "value"
                # A column that decides rows here is reported where it does so; a column whose value
                # feeds one that decides rows downstream is reported where that one does.
                why = frozenset({f"{d.how} in {job}"}) if d.kind == "rows" else (reasons if kind == "rows" else frozenset())
                key = (d.dataset, d.column)
                if key not in found:
                    found[key] = {"value": False, "rows": set()}
                    order.append(key)
                if k == "value":
                    found[key]["value"] = True
                else:
                    found[key]["rows"] |= why
                if d.column != "*" and (key, k, why) not in seen:
                    visit(d.dataset, d.column, k, why, seen | {(key, k, why)})

    visit(dataset, column, "value", frozenset(), frozenset())
    depth = {}
    for ds, _ in order:
        depth.setdefault(ds, len(depth))
    order.sort(key=lambda k: depth[k[0]])
    return Rows(
        {
            "dataset": _name(ds),
            "column": col,
            "value": "yes" if found[(ds, col)]["value"] else "no",
            "rows": "; ".join(sorted(found[(ds, col)]["rows"])),
        }
        for ds, col in order
    )


# How the shop's kinds are written in OpenLineage's column lineage facet (docs/sources.md). The
# facet's documentation lists no subtype for DISTINCT, so the shop writes that one without a subtype.
SUBTYPES = {
    "copied": ("DIRECT", "IDENTITY"),
    "computed": ("DIRECT", "TRANSFORMATION"),
    "aggregated": ("DIRECT", "AGGREGATION"),
    "filter": ("INDIRECT", "FILTER"),
    "grouping": ("INDIRECT", "GROUP_BY"),
    "distinct": ("INDIRECT", None),
}


def facet(week: Week, table: str, catalogue: Warehouse | None = None) -> dict:
    """The column lineage facet the shop's producer would add to an output: OpenLineage's form.

    The columns whose values are computed go under `fields`, each output column with its inputs;
    the columns that decide which rows there are go once under `dataset`, as they decide the rows
    of every column.
    """
    from .openlineage import dataset, facet as make

    catalogue = catalogue or week.warehouse
    [code] = [p["code"] for p in programs(week) if deps(p["code"], catalogue)[0] == table]
    _, found = deps(code, catalogue)

    def field(d: Dep) -> dict:
        kind, subtype = SUBTYPES[d.how]
        how = {"type": kind}
        if subtype:
            how["subtype"] = subtype
        else:
            how["description"] = "SELECT DISTINCT"
        return {**dataset(d.dataset), "field": d.column, "transformations": [how]}

    fields: dict[str, dict] = {}
    for d in found:
        if d.kind == "value":
            fields.setdefault(d.output, {"inputFields": []})["inputFields"].append(field(d))
    rows = []
    for d in found:
        if d.kind == "rows":
            f = field(d)
            if f not in rows:
                rows.append(f)
    return make("columnLineage", fields=fields, dataset=rows)


__all__ = ["ANALYST_COPY", "SUBTYPES", "deps", "facet", "lineage", "programs", "upstream"]
