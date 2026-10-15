# Copyright © 2026 Christopher Snow

"""The shop's data platform: three systems, each recording what its own work needs.

- Object storage holds files in buckets and records each file's key, size and last-modified
  time. The files are real: JSON Lines and CSV, readable with Python's standard library. It also
  keeps every version of each object, and a marker where one was deleted, which it lists only
  when asked (`versions`).
- The warehouse holds tables in SQLite and keeps a catalogue the learner can query as
  `information_schema`: each table's columns and types, row count, size, created and
  last-altered times, and the account that owns it.
- The reporting tool holds a dashboard and records its title, who created it and when, when it
  last refreshed, and the values it shows.

Nothing here records which program wrote an asset, what it read, or why: that is what Chapter 2
shows a platform's state cannot tell.
"""

from __future__ import annotations

import csv
import hashlib
import html
import io
import json
import os
import re
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
    ".ms-table th{font-weight:600}.ms-scroll{overflow-x:auto;max-width:100%}"
    ".ms-table .ms-wd{margin-left:0.35em;opacity:0.65}</style>"
)

# A date or a time standing as a word of its own: 2026-09-10, 2026-09-10T02:30:21Z, "2026-09-22
# mainland 17:30", "... on 2026-09-24.". Not one inside a path or a name (s3://.../2026-09-22/1730).
_DATE = re.compile(
    r"(?<![\w/:.-])(\d{4}-\d{2}-\d{2}(?:[T ]\d{2}:\d{2}(?::\d{2}(?:\.\d+)?)?(?:Z|[+-]\d{2}:?\d{2})?)?)(?![\w/-]|\.\d)"
)


def _code(text: str) -> str:
    """Escapes text for HTML, and sets a name written in backticks in the code font."""
    return re.sub(r"`([^`]+)`", r"<code>\1</code>", html.escape(text))


def _value(value) -> str:
    """A value as a table shows it. Each date or time in it carries its day of the week after it,
    muted, since the chapters name the shop's days (Thursday's revenue, the failed night on Monday)
    and a table shows dates: 2026-09-10 (Thu). The day is the date's as written, in UTC like every
    time."""
    shown = _code(str(value))
    if not isinstance(value, str):
        return shown

    def mark(m: re.Match) -> str:
        try:
            day = datetime.strptime(m.group(1)[:10], "%Y-%m-%d").strftime("%a")
        except ValueError:
            return m.group(0)
        return f'{m.group(1)}<span class="ms-wd">({day})</span>'

    return _DATE.sub(mark, shown)


def _cell(value, null: str) -> str:
    if value is None:
        return f"<em>{null}</em>"
    if isinstance(value, list):
        return "<br>".join(
            ", ".join(f"{_code(str(k))}: {_value(v)}" for k, v in x.items()) if isinstance(x, dict) else _value(x)
            for x in value
        )
    return _value(value)


class Rows(list):
    """Rows as a list of dictionaries, which a notebook shows as a table."""

    def __init__(self, rows=(), null: str = "NULL", empty: str = "No rows.") -> None:
        super().__init__(rows)
        self.null = null
        self.empty = empty

    def _repr_html_(self) -> str:
        if not self:
            return f"<em>{html.escape(self.empty)}</em>"
        names = list(self[0])
        head = "".join(f"<th>{_value(n)}</th>" for n in names)
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


_BESIDE_STYLE = (
    "<style>table.ms-table.ms-beside th,table.ms-table.ms-beside td{text-align:left;vertical-align:top}"
    "table.ms-table.ms-beside td:first-child{font-family:var(--jp-content-font-family,sans-serif);font-weight:600}"
    "table.ms-table.ms-beside tr.ms-changed td{background:color-mix(in srgb,var(--jp-warn-color1,#f59e0b) 14%,transparent)}"
    "table.ms-table.ms-beside .ms-badge{display:none}"
    "@media (max-width:640px){table.ms-table.ms-beside thead{display:none}"
    "table.ms-table.ms-beside tr{display:block;padding:0.4rem 0.5rem;border-bottom:1px solid "
    "color-mix(in srgb,currentColor 18%,transparent)}"
    "table.ms-table.ms-beside tr.ms-changed{background:color-mix(in srgb,var(--jp-warn-color1,#f59e0b) 14%,transparent)}"
    "table.ms-table.ms-beside tr.ms-changed td{background:none}"
    "table.ms-table.ms-beside td{display:block;border:0;padding:0.1rem 0;white-space:normal;overflow-wrap:anywhere}"
    "table.ms-table.ms-beside td.ms-flag{display:none}"
    "table.ms-table.ms-beside tr.ms-same td:nth-child(3){display:none}"
    "table.ms-table.ms-beside .ms-badge{display:inline-block;margin-left:0.4rem;padding:0 0.4rem;border-radius:999px;"
    "font-size:0.75em;font-weight:600;background:color-mix(in srgb,var(--jp-warn-color1,#f59e0b) 35%,transparent)}"
    "table.ms-table.ms-beside td[data-label]::before{content:attr(data-label);display:block;"
    "font-family:var(--jp-content-font-family,sans-serif);font-style:italic;opacity:0.8}"
    "table.ms-table.ms-beside tr.ms-same td[data-same]::before{content:attr(data-same)}}</style>"
)


class Beside(Rows):
    """Records side by side, one per row, in columns. A column `changed` marks each row that
    differs, which is tinted. On a narrow screen each row stacks, with each value under its
    column's name; a row that did not change shows its value once, and one that did carries a
    badge in place of the column."""

    def _repr_html_(self) -> str:
        names = list(self[0])
        flagged = "changed" in names
        head = "".join(f"<th>{_value(n)}</th>" for n in names)
        body = []
        for r in self:
            changed = flagged and r["changed"] == "yes"
            cls = (" class=\"ms-changed\"" if changed else " class=\"ms-same\"") if flagged else ""
            cells = []
            for i, n in enumerate(names):
                value = _cell(r.get(n), self.null)
                if i == 0:
                    badge = '<span class="ms-badge">changed</span>' if changed else ""
                    cells.append(f"<td>{value}{badge}</td>")
                elif n == "changed":
                    cells.append(f'<td class="ms-flag">{value}</td>')
                elif i == 1 and flagged:
                    cells.append(f'<td data-label="{html.escape(n)}" data-same="in both weeks">{value}</td>')
                else:
                    cells.append(f'<td data-label="{html.escape(n)}">{value}</td>')
            body.append(f"<tr{cls}>{''.join(cells)}</tr>")
        return f'{_TABLE_STYLE}{_BESIDE_STYLE}<div class="ms-scroll"><table class="ms-table ms-beside"><thead><tr>{head}</tr></thead><tbody>{"".join(body)}</tbody></table></div>'


def rows_of(cursor: sqlite3.Cursor) -> Rows:
    """A query's rows as dictionaries, keyed by column name."""
    names = [d[0] for d in cursor.description or ()]
    return Rows(dict(zip(names, row)) for row in cursor.fetchall())


def parse(uri: str, text: str) -> "Rows":
    """A file's records: one object per line of JSON Lines, one row per line of CSV, or one JSON object.

    A CSV file has no types, so every value is text, and an empty field is an empty string.
    """
    if uri.endswith(".jsonl"):
        return Rows((json.loads(line) for line in text.splitlines() if line.strip()), null="null")
    if uri.endswith(".csv"):
        return Rows(csv.DictReader(io.StringIO(text)), null="")
    if uri.endswith(".json"):
        return Rows([json.loads(text)], null="null")
    raise ValueError(f"no reader for {uri}")


def file_schema(records: list[dict]) -> tuple[tuple[str, str], ...]:
    """A file's fields as a reader finds them: each name, in the order first seen, and the type of its
    values (JSON's: integer, number, string, boolean), with an empty value left out. A field with
    values of two types gets both, as `integer or string`; one with no value at all, `null`."""
    seen: dict[str, set[str]] = {}
    for r in records:
        for k, v in r.items():
            kinds = seen.setdefault(k, set())
            if v is None or v == "":
                continue
            kinds.add("boolean" if isinstance(v, bool) else "integer" if isinstance(v, int) else "number" if isinstance(v, float) else "string")
    return tuple((k, " or ".join(sorted(v)) or "null") for k, v in seen.items())


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
        self._versions: dict[str, list[dict]] = {}
        self._texts: dict[tuple[str, str], str | None] = {}

    def _path(self, uri: str) -> Path:
        if not uri.startswith("s3://"):
            raise ValueError(f"not an object storage address: {uri}")
        return self._root / uri[len("s3://") :]

    def _version(self, uri: str, at: str, text: str | None) -> str:
        """A new version of an object: an opaque identifier, the same on every machine."""
        made = hashlib.sha1(f"{uri}|{at}|{text}".encode()).hexdigest()[:12]
        self._texts[(uri, made)] = text
        self._versions.setdefault(uri, []).append(
            {"key": uri, "version": made, "at": at, "deleted": text is None, "size_bytes": len(text.encode()) if text is not None else None}
        )
        return made

    def put(self, uri: str, text: str, at: str) -> str:
        """Writes a file, records `at` as its last-modified time, and returns the new version's id."""
        path = self._path(uri)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        os.utime(path, (epoch(at), epoch(at)))
        return self._version(uri, at, text)

    def delete(self, uri: str, at: str) -> str:
        """Deletes a file. Its earlier versions stay, under a delete marker, whose id it returns."""
        self._path(uri).unlink()
        return self._version(uri, at, None)

    def versions(self, prefix: str = "s3://") -> Rows:
        """Every version of every object under a prefix, oldest first, delete markers included."""
        return Rows(
            ({k: v for k, v in version.items()} for uri in sorted(self._versions) if uri.startswith(prefix) for version in self._versions[uri]),
            null="",
        )

    def version_text(self, uri: str, version: str) -> str | None:
        """One version's contents, exactly as written; None for a delete marker."""
        return self._texts[(uri, version)]

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
PROGRAM_ACCOUNT = "etlsvc/batch01.corp.internal@CORP.INTERNAL"

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

    def tables(self) -> list[str]:
        """The names of the production tables the catalogue records."""
        return [t for (t,) in self.db.execute("SELECT table_name FROM information_schema.tables WHERE table_type = 'BASE TABLE'")]

    def bytes(self, table: str) -> int:
        """The catalogue's size of a table, in bytes."""
        [(n,)] = self.db.execute("SELECT bytes FROM information_schema.tables WHERE table_name = ?", (table,))
        return n

    def create_view(self, view: str, select: str, created: str) -> None:
        """A view: a name for a query, which the catalogue records as a VIEW and which holds no rows."""
        self.db.execute(f"CREATE VIEW main.{view} AS {select}")
        self.db.execute(
            "INSERT INTO information_schema.tables VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            ("shop", "analytics", view, "VIEW", "j.marsh", None, None, created, created),
        )
        self.db.commit()

    def create_database(self, name: str, tables: tuple[str, ...]) -> None:
        """A second database in the warehouse, with empty tables of the same columns as production's."""
        self.db.execute(f"ATTACH DATABASE ':memory:' AS {name}")
        for t in tables:
            columns, _ = TABLES[t]
            self.db.execute(f"CREATE TABLE {name}.{t} ({', '.join(f'{c} {k}' for c, k in columns)})")
        self.db.commit()

    def table_schema(self, table: str) -> tuple[tuple[str, str], ...]:
        """A table's columns and declared types, as the catalogue records them."""
        return tuple(
            (c, t)
            for c, t in self.db.execute(
                "SELECT column_name, data_type FROM information_schema.columns WHERE table_name = ? ORDER BY ordinal_position", (table,)
            )
        )

    def add_column(self, table: str, column: str, kind: str) -> None:
        """A change to a table's columns, which the warehouse's catalogue records at once."""
        self.db.execute(f"ALTER TABLE main.{table} ADD COLUMN {column} {kind}")
        [(n,)] = self.db.execute("SELECT COUNT(*) FROM information_schema.columns WHERE table_name = ?", (table,))
        self.db.execute("INSERT INTO information_schema.columns VALUES (?, ?, ?, ?)", (table, column, n + 1, kind))
        self.db.commit()

    def rename_column(self, table: str, old: str, new: str) -> None:
        """A column renamed, which the warehouse's catalogue records at once (the `customer` change)."""
        self.db.execute(f"ALTER TABLE main.{table} RENAME COLUMN {old} TO {new}")
        self.db.execute("UPDATE information_schema.columns SET column_name = ? WHERE table_name = ? AND column_name = ?", (new, table, old))
        self.db.commit()

    def create_table(self, table: str, columns: tuple[tuple[str, str], ...], created: str) -> None:
        """A new table, which the catalogue records at once."""
        spec = ", ".join(f"{c} {t}" for c, t in columns)
        self.db.execute(f"CREATE TABLE main.{table} ({spec})")
        self.db.executemany(
            "INSERT INTO information_schema.columns VALUES (?, ?, ?, ?)",
            [(table, c, i + 1, t) for i, (c, t) in enumerate(columns)],
        )
        self.db.execute(
            "INSERT INTO information_schema.tables VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            ("shop", "analytics", table, "BASE TABLE", PROGRAM_ACCOUNT, 0, 0, created, created),
        )
        self.db.commit()

    def change(self, table: str, statements: list[tuple[str, dict]], at: str) -> int:
        """A program's change to some rows of a table: the statements in order, then the catalogue."""
        changed = 0
        for sql, params in statements:
            changed += self.db.execute(sql, params).rowcount
        self._catalogue(table, at)
        return changed

    def write(self, table: str, select: str, at: str, *, append: bool = False, **params) -> int:
        """A program's write: replaces the table's rows, or appends to them, and updates the catalogue."""
        if not append:
            self.db.execute(f"DELETE FROM main.{table}")
        cursor = self.db.execute(f"INSERT INTO main.{table} {select}", params)
        added = cursor.rowcount
        self._catalogue(table, at)
        return added

    def _catalogue(self, table: str, at: str) -> None:
        rows = self.db.execute(f"SELECT * FROM main.{table}").fetchall()
        types = tuple(
            t
            for (t,) in self.db.execute(
                "SELECT data_type FROM information_schema.columns WHERE table_name = ? ORDER BY ordinal_position",
                (table,),
            )
        )
        self.db.execute(
            """UPDATE information_schema.tables
               SET row_count = ?, bytes = ?, last_altered = ? WHERE table_name = ?""",
            (len(rows), estimated_bytes(rows, types), at, table),
        )
        self.db.commit()


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

    def __init__(self, slow_seconds: int = 0) -> None:
        # The reporting tool keeps its own clock. With the `clock` change it runs slow, and every
        # time the tool records is early by this much (Chapter 13).
        self.slow_seconds = slow_seconds
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
        self._dashboard["last_refreshed"] = iso(epoch(at) - self.slow_seconds)

    def dashboard(self, name: str = "sales_dashboard") -> Record:
        """What the reporting tool records about a dashboard, and the values it shows."""
        if name != "sales_dashboard":
            raise KeyError(name)
        return Record({**self._dashboard, "values": list(self._dashboard["values"])})
