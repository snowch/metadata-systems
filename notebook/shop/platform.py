# Copyright © 2026 Christopher Snow

"""The shop's data platform: three systems, each recording what its own work needs.

- Object storage holds files in buckets and records each file's key, size and last-modified
  time. The files are real: JSON Lines and CSV, readable with Python's standard library.
- The warehouse holds tables in SQLite and keeps a catalogue the learner can query as
  `information_schema`: each table's columns and types, row count, size, created and
  last-altered times, and the account that owns it.
- The reporting tool holds a dashboard and records its title, who created it and when, when it
  last refreshed, and the values it shows.

Nothing here records which program wrote an asset, what it read, or why: that is what Chapter 1
shows a platform's state cannot tell.
"""

from __future__ import annotations

import csv
import html
import io
import json
import os
import shutil
import sqlite3
import tempfile
import weakref
from datetime import datetime, timezone
from pathlib import Path


def epoch(iso: str) -> float:
    """Seconds since 1970 for an ISO timestamp in UTC, as `2026-09-14T02:30:21Z`."""
    return datetime.strptime(iso, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc).timestamp()


def iso(seconds: float) -> str:
    """The ISO timestamp, in UTC, of a time in seconds since 1970."""
    return datetime.fromtimestamp(seconds, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


_TABLE_STYLE = (
    "<style>.ms-table{border-collapse:collapse;font-size:0.85rem}"
    ".ms-table th,.ms-table td{padding:0.2rem 0.6rem;border-bottom:1px solid "
    "color-mix(in srgb,currentColor 18%,transparent);text-align:left;white-space:nowrap}"
    ".ms-table td{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}"
    ".ms-table th{font-weight:600}.ms-scroll{overflow-x:auto;max-width:100%}</style>"
)


def _cell(value, null: str) -> str:
    if value is None:
        return f"<em>{null}</em>"
    if isinstance(value, list):
        return "<br>".join(html.escape(", ".join(f"{k}: {v}" for k, v in x.items()) if isinstance(x, dict) else str(x)) for x in value)
    return html.escape(str(value))


class Rows(list):
    """Rows as a list of dictionaries, which a notebook shows as a table."""

    def __init__(self, rows=(), null: str = "NULL") -> None:
        super().__init__(rows)
        self.null = null

    def _repr_html_(self) -> str:
        if not self:
            return "<em>No rows.</em>"
        names = list(self[0])
        head = "".join(f"<th>{html.escape(n)}</th>" for n in names)
        body = "".join("<tr>" + "".join(f"<td>{_cell(r.get(n), self.null)}</td>" for n in names) + "</tr>" for r in self)
        return f'{_TABLE_STYLE}<div class="ms-scroll"><table class="ms-table"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'

    def _mime_(self) -> tuple[str, str]:
        return ("text/html", self._repr_html_())


class Record(dict):
    """One record's fields, which a notebook shows as a two-column table."""

    def _repr_html_(self) -> str:
        body = "".join(f"<tr><th>{html.escape(k)}</th><td>{_cell(v, 'null')}</td></tr>" for k, v in self.items())
        return f'{_TABLE_STYLE}<div class="ms-scroll"><table class="ms-table"><tbody>{body}</tbody></table></div>'

    def _mime_(self) -> tuple[str, str]:
        return ("text/html", self._repr_html_())


def rows_of(cursor: sqlite3.Cursor) -> Rows:
    """A query's rows as dictionaries, keyed by column name."""
    names = [d[0] for d in cursor.description or ()]
    return Rows(dict(zip(names, row)) for row in cursor.fetchall())


def parse(uri: str, text: str) -> "Rows":
    """A file's records: one object per line of JSON Lines, or one row per line of CSV.

    A CSV file has no types, so every value is text, and an empty field is an empty string.
    """
    if uri.endswith(".jsonl"):
        return Rows((json.loads(line) for line in text.splitlines() if line.strip()), null="null")
    if uri.endswith(".csv"):
        return Rows(csv.DictReader(io.StringIO(text)), null="")
    raise ValueError(f"no reader for {uri}")


def stage(db: sqlite3.Connection, name: str, records: list[dict], fields: tuple[str, ...]) -> None:
    """Loads records into a temporary table, with no declared types, as a reader of a file would."""
    db.execute(f'DROP TABLE IF EXISTS temp."{name}"')
    db.execute(f'CREATE TEMP TABLE "{name}" ({", ".join(f'"{f}"' for f in fields)})')
    db.executemany(
        f'INSERT INTO temp."{name}" VALUES ({", ".join("?" for _ in fields)})',
        [tuple(r.get(f) for f in fields) for r in records],
    )


class ObjectStorage:
    """Buckets of files. What it records about a file: its key, its size and its last-modified time."""

    def __init__(self) -> None:
        self._root = Path(tempfile.mkdtemp(prefix="shop-storage-"))
        weakref.finalize(self, shutil.rmtree, self._root, ignore_errors=True)

    def _path(self, uri: str) -> Path:
        if not uri.startswith("s3://"):
            raise ValueError(f"not an object storage address: {uri}")
        return self._root / uri[len("s3://") :]

    def put(self, uri: str, text: str, at: str) -> None:
        """Writes a file and records `at` as its last-modified time."""
        path = self._path(uri)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        os.utime(path, (epoch(at), epoch(at)))

    def ls(self, prefix: str = "s3://") -> Rows:
        """Every file under a prefix, as object storage lists it."""
        out = []
        for path in sorted(self._root.rglob("*")):
            if not path.is_file():
                continue
            uri = "s3://" + path.relative_to(self._root).as_posix()
            if uri.startswith(prefix):
                stat = path.stat()
                out.append(
                    {"key": uri, "size_bytes": stat.st_size, "last_modified": iso(stat.st_mtime)}
                )
        return Rows(out)

    def exists(self, uri: str) -> bool:
        return self._path(uri).is_file()

    def read_text(self, uri: str) -> str:
        """A file's contents, exactly as written."""
        return self._path(uri).read_text(encoding="utf-8")

    def records(self, uri: str) -> Rows:
        """A file's records, parsed by its format."""
        return parse(uri, self.read_text(uri))

    def sql(self, uri: str, query: str, **params) -> Rows:
        """Runs a query over one file, which it calls `file`, as a query engine reading files would."""
        records = self.records(uri)
        fields = tuple(records[0]) if records else ()
        db = sqlite3.connect(":memory:")
        try:
            stage(db, "file", records, fields)
            return rows_of(db.execute(query, params))
        finally:
            db.close()


# The warehouse's tables, their declared column types, and when each was created.
TABLES = {
    "clean_customers": (
        (
            ("customer_id", "INTEGER"),
            ("name", "TEXT"),
            ("email", "TEXT"),
            ("country", "TEXT"),
            ("signed_up", "DATE"),
        ),
        "2026-09-01T10:12:00Z",
    ),
    "clean_orders": (
        (
            ("order_id", "INTEGER"),
            ("customer_id", "INTEGER"),
            ("product_id", "INTEGER"),
            ("quantity", "INTEGER"),
            ("price_pence", "INTEGER"),
            ("status", "TEXT"),
            ("ordered_at", "TIMESTAMP"),
        ),
        "2026-09-01T10:14:00Z",
    ),
    "daily_sales": (
        (("day", "DATE"), ("revenue_pence", "INTEGER")),
        "2026-09-01T10:20:00Z",
    ),
}

# The account every program logs in as, which the warehouse records as each table's owner.
PROGRAM_ACCOUNT = "etl_service"

_WIDTH = {"INTEGER": 8, "DATE": 4, "TIMESTAMP": 8}


def estimated_bytes(rows: list[tuple], types: tuple[str, ...]) -> int:
    """A deterministic estimate of a table's size: the warehouse's own figure is not modelled."""
    total = 512 + 64 * len(types)
    for row in rows:
        for value, kind in zip(row, types):
            if value is None:
                continue
            total += _WIDTH.get(kind, 4) + (len(value) if isinstance(value, str) else 0)
    return total


class Warehouse:
    """Tables in SQLite, with a catalogue queryable as `information_schema.tables` and `.columns`."""

    def __init__(self, storage: ObjectStorage) -> None:
        self.storage = storage
        self.db = sqlite3.connect(":memory:")
        weakref.finalize(self, self.db.close)
        self.db.execute("ATTACH DATABASE ':memory:' AS information_schema")
        self.db.execute(
            """CREATE TABLE information_schema.tables (
                table_catalog TEXT, table_schema TEXT, table_name TEXT, table_type TEXT,
                table_owner TEXT, row_count INTEGER, bytes INTEGER, created TEXT,
                last_altered TEXT)"""
        )
        self.db.execute(
            """CREATE TABLE information_schema.columns (
                table_name TEXT, column_name TEXT, ordinal_position INTEGER, data_type TEXT)"""
        )
        for name, (columns, created) in TABLES.items():
            spec = ", ".join(f"{c} {t}" for c, t in columns)
            self.db.execute(f"CREATE TABLE main.{name} ({spec})")
            self.db.executemany(
                "INSERT INTO information_schema.columns VALUES (?, ?, ?, ?)",
                [(name, c, i + 1, t) for i, (c, t) in enumerate(columns)],
            )
            self.db.execute(
                "INSERT INTO information_schema.tables VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                ("shop", "analytics", name, "BASE TABLE", PROGRAM_ACCOUNT, 0, 0, created, created),
            )
        self.db.commit()

    def sql(self, query: str, files: dict[str, str] | None = None, **params) -> Rows:
        """Runs a query over the warehouse and returns its rows.

        `files` names files in object storage to read as tables for this query only, as a query
        engine that reads files would: `files={"raw_orders": "s3://shop-raw/orders.jsonl"}`.
        """
        staged = []
        try:
            for name, uri in (files or {}).items():
                records = self.storage.records(uri)
                stage(self.db, name, records, tuple(records[0]) if records else ())
                staged.append(name)
            return rows_of(self.db.execute(query, params))
        finally:
            for name in staged:
                self.db.execute(f'DROP TABLE IF EXISTS temp."{name}"')

    def write(self, table: str, select: str, at: str, *, append: bool = False, **params) -> int:
        """A program's write: replaces the table's rows, or appends to them, and updates the catalogue."""
        if not append:
            self.db.execute(f"DELETE FROM main.{table}")
        cursor = self.db.execute(f"INSERT INTO main.{table} {select}", params)
        added = cursor.rowcount
        rows = self.db.execute(f"SELECT * FROM main.{table}").fetchall()
        types = tuple(t for _, t in TABLES[table][0])
        self.db.execute(
            """UPDATE information_schema.tables
               SET row_count = ?, bytes = ?, last_altered = ? WHERE table_name = ?""",
            (len(rows), estimated_bytes(rows, types), at, table),
        )
        self.db.commit()
        return added


# The member of staff who built the dashboard, and its title, which the reporting tool records.
DASHBOARD_CREATOR = "j.marsh"
DASHBOARD_TITLE = "Sales, last 7 days"
DASHBOARD_CREATED = "2026-09-02T15:41:00Z"


def pounds(pence: int) -> str:
    """An amount of pence as a person reads it: £51.50."""
    sign = "-" if pence < 0 else ""
    return f"{sign}£{abs(pence) // 100}.{abs(pence) % 100:02d}"


class Reporting:
    """The reporting tool: a dashboard and what it records about it."""

    def __init__(self) -> None:
        self._dashboard = {
            "name": "sales_dashboard",
            "title": DASHBOARD_TITLE,
            "created_by": DASHBOARD_CREATOR,
            "created": DASHBOARD_CREATED,
            "last_refreshed": DASHBOARD_CREATED,
            "values": [],
        }

    def refresh(self, rows: list[tuple[str, int]], at: str) -> None:
        """Redraws the chart from rows of day and pence, and records the time."""
        self._dashboard["values"] = [{"day": day, "revenue": pounds(p)} for day, p in rows]
        self._dashboard["last_refreshed"] = at

    def dashboard(self, name: str = "sales_dashboard") -> Record:
        """What the reporting tool records about a dashboard, and the values it shows."""
        if name != "sales_dashboard":
            raise KeyError(name)
        return Record({**self._dashboard, "values": list(self._dashboard["values"])})
