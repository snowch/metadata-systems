# Copyright © 2026 Christopher Snow

"""Records a person writes about the shop's assets, and the checks a notebook runs on them.

Chapter 3's records are lines of text, one fact to a line: the asset, a column if the fact is about
one, a field, a colon and the value, as `daily_sales revenue_pence unit: pence`. A value of dots
(`........`) is one not yet written. `records.check(warehouse)` holds them to what the warehouse
and object storage record: every column the warehouse has needs a description (a `means` line), and
every line must name an asset, and a column, that exists. It cannot tell whether a description is
true: nothing on the platform records what an asset means.

Chapter 4's records name the type of thing each line describes: `dataset daily_sales responsible:
j.marsh`, `person j.marsh name: Jo Marsh`. A model, also lines of text, says which attributes each
type has and what each attribute's value is: text, or the identifier of a thing of another type
(`dataset responsible: person or team`). `model.check(records)` reports every line the model has
no type or attribute for, and every value that names a thing no record describes.

The notations are the course's own. Nothing here reads or writes the shop's platform.
"""

from __future__ import annotations

import re
import sqlite3

from .platform import Rows

# What a check prints, in the reader's words: Haiku's drafts of brief CC (docs/notes/chapter-03/).
MESSAGES = {
    "none": "No problems found.",
    "unread": "This line is not in the form `asset field: value` or `asset column field: value`.",
    "no_asset": "This line names an asset that is neither a table in the warehouse nor a file in object storage.",
    "no_column": "This line names a column that the warehouse table does not have.",
    "no_description": "The records do not describe this column, because there is no `means` line for it or its value is still only dots.",
    "typed_unread": "This record line is not in the form `type identifier attribute: value`.",
    "model_unread": "This model line is not in the form `type attribute: text`, `type attribute: type`, or `type attribute: type or type`.",
    "no_type": "The model does not define this line's type.",
    "no_attribute": "The model does not give this type this attribute.",
    "no_value_type": "This model line names a value type that the model does not define.",
    "no_thing": "This value should be the identifier of something of type {types}, and no record describes such a thing with that identifier.",
}

# A value not yet written: dots, as the chapters' records leave them for the reader.
_UNWRITTEN = re.compile(r"^\.{3,}$")
# Everything before the first colon that ends its word: `s3://` is part of a name, not a field.
_LINE = re.compile(r"^(.*?):(?:\s+(.*))?$")


def written(value: str | None) -> bool:
    """Whether a value has been written: not empty, and not dots."""
    return bool(value) and not _UNWRITTEN.match(value.strip())


def _lines(text: str):
    """Each line that holds a fact: its number and its text, without blank lines and `#` notes."""
    for number, raw in enumerate(text.splitlines(), start=1):
        line = raw.strip()
        if line and not line.startswith("#"):
            yield number, line


def _split(line: str) -> tuple[list[str], str] | None:
    """The words before the colon, and the value after it; None if the line has no such colon."""
    match = _LINE.match(line)
    if not match:
        return None
    return match.group(1).split(), (match.group(2) or "").strip()


def _query(table: list[dict], columns: tuple[str, ...], query: str, params: dict) -> Rows:
    db = sqlite3.connect(":memory:")
    try:
        db.execute(f"CREATE TABLE records ({', '.join(columns)})")
        db.executemany(
            f"INSERT INTO records VALUES ({', '.join('?' for _ in columns)})",
            [tuple(r[c] for c in columns) for r in table],
        )
        cursor = db.execute(query, params)
        names = [d[0] for d in cursor.description or ()]
        return Rows((dict(zip(names, row)) for row in cursor.fetchall()), null="")
    finally:
        db.close()


class Records(Rows):
    """Chapter 3's records: one row per line, as `line`, `asset`, `column`, `field` and `value`."""

    COLUMNS = ("line", "asset", "column", "field", "value")

    def __init__(self, text: str) -> None:
        super().__init__(null="")
        self.text = text
        self.unread: list[dict] = []
        for number, line in _lines(text):
            parts = _split(line)
            words = parts[0] if parts else []
            if parts and len(words) in (2, 3):
                asset, *column, field = words
                self.append(
                    {"line": number, "asset": asset, "column": column[0] if column else None, "field": field, "value": parts[1]}
                )
            else:
                self.unread.append({"line": number, "text": line})

    def sql(self, query: str, **params) -> Rows:
        """Runs a query over the records, as a table called `records`."""
        return _query(self, self.COLUMNS, query, params)

    def about(self, asset: str) -> Rows:
        """Every line about one asset."""
        return Rows((r for r in self if r["asset"] == asset), null="")

    def check(self, warehouse, asset: str | None = None) -> Rows:
        """The records against what the warehouse and object storage record.

        Each line must name a table or a file that exists, and a column the table has; every column
        of every table needs a description. With `asset`, only that asset is checked.
        """
        storage = warehouse.storage
        columns: dict[str, list[str]] = {}
        for r in warehouse.sql("SELECT table_name, column_name FROM information_schema.columns ORDER BY rowid"):
            columns.setdefault(r["table_name"], []).append(r["column_name"])
        mine = [r for r in self if asset is None or r["asset"] == asset]
        out = [{"line": u["line"], "asset": None, "column": None, "problem": MESSAGES["unread"]} for u in self.unread if asset is None]
        for r in mine:
            if r["asset"] not in columns and not (r["asset"].startswith("s3://") and storage.exists(r["asset"])):
                out.append({"line": r["line"], "asset": r["asset"], "column": r["column"], "problem": MESSAGES["no_asset"]})
            elif r["column"] is not None and r["column"] not in columns.get(r["asset"], ()):
                out.append({"line": r["line"], "asset": r["asset"], "column": r["column"], "problem": MESSAGES["no_column"]})
        described = {(r["asset"], r["column"]) for r in self if r["field"] == "means" and written(r["value"])}
        for table, names in columns.items():
            if asset is not None and table != asset:
                continue
            for column in names:
                if (table, column) not in described:
                    out.append({"line": None, "asset": table, "column": column, "problem": MESSAGES["no_description"]})
        return Rows(out, null="", empty=MESSAGES["none"])


class TypedRecords(Rows):
    """Chapter 4's records: one row per line, as `line`, `type`, `identifier`, `attribute` and `value`."""

    COLUMNS = ("line", "type", "identifier", "attribute", "value")

    def __init__(self, text: str) -> None:
        super().__init__(null="")
        self.text = text
        self.unread: list[dict] = []
        for number, line in _lines(text):
            parts = _split(line)
            if parts and len(parts[0]) == 3:
                kind, identifier, attribute = parts[0]
                self.append({"line": number, "type": kind, "identifier": identifier, "attribute": attribute, "value": parts[1]})
            else:
                self.unread.append({"line": number, "text": line})

    def sql(self, query: str, **params) -> Rows:
        """Runs a query over the records, as a table called `records`."""
        return _query(self, self.COLUMNS, query, params)

    def things(self) -> set[tuple[str, str]]:
        """Every thing the records describe, as its type and its identifier."""
        return {(r["type"], r["identifier"]) for r in self}


class Model(Rows):
    """A model of the records: one row per attribute, as `type`, `attribute` and `value`.

    The value is `text`, or the names of the types whose identifiers the attribute's value may be,
    joined by `or`.
    """

    COLUMNS = ("type", "attribute", "value")

    def __init__(self, text: str) -> None:
        super().__init__(null="")
        self.text = text
        self.unread: list[dict] = []
        for number, line in _lines(text):
            parts = _split(line)
            if parts and len(parts[0]) == 2 and parts[1]:
                kind, attribute = parts[0]
                self.append({"line": number, "type": kind, "attribute": attribute, "value": parts[1]})
            else:
                self.unread.append({"line": number, "text": line})

    def types(self) -> set[str]:
        """The types the model defines: each type that has an attribute."""
        return {r["type"] for r in self}

    def attribute(self, kind: str, attribute: str) -> list[str] | None:
        """What an attribute's value is, as a list of type names or `["text"]`; None if undefined."""
        for r in self:
            if r["type"] == kind and r["attribute"] == attribute:
                return [v.strip() for v in re.split(r"\s+or\s+", r["value"])]
        return None

    def check(self, records: TypedRecords) -> Rows:
        """The records against the model: every line the model has no type or attribute for, and
        every value that should name a thing and names none the records describe."""
        out = [{"line": u["line"], "record": u["text"], "problem": MESSAGES["model_unread"]} for u in self.unread]
        for r in self:
            if any(v != "text" and v not in self.types() for v in self.attribute(r["type"], r["attribute"]) or ()):
                out.append({"line": r["line"], "record": f"{r['type']} {r['attribute']}: {r['value']}", "problem": MESSAGES["no_value_type"]})
        out += [{"line": u["line"], "record": u["text"], "problem": MESSAGES["typed_unread"]} for u in records.unread]
        things = records.things()
        for r in records:
            text = f"{r['type']} {r['identifier']} {r['attribute']}: {r['value']}"
            if r["type"] not in self.types():
                out.append({"line": r["line"], "record": text, "problem": MESSAGES["no_type"]})
                continue
            kinds = self.attribute(r["type"], r["attribute"])
            if kinds is None:
                out.append({"line": r["line"], "record": text, "problem": MESSAGES["no_attribute"]})
            elif kinds != ["text"] and not any((k, r["value"]) in things for k in kinds):
                out.append({"line": r["line"], "record": text, "problem": MESSAGES["no_thing"].format(types=" or ".join(kinds))})
        return Rows(out, null="", empty=MESSAGES["none"])


def assets(week) -> list[tuple[str, str]]:
    """Every asset on the platform, as its type in Chapter 4's model and its identifier."""
    files = [("dataset", r["key"]) for r in week.storage.ls()]
    tables = [("dataset", r["table_name"]) for r in week.warehouse.sql("SELECT table_name FROM information_schema.tables ORDER BY rowid")]
    return files + tables + [("dashboard", week.reporting.dashboard()["name"])]


def owners(week, records: TypedRecords) -> Rows:
    """Each asset on the platform, its `responsible` values, and three readings of "one owner".

    `one_owner`: exactly one value. `one_person`: exactly one value, the identifier of a person.
    `one_team`: exactly one team, named directly or as the `team` of the person named.
    """
    kinds = {}
    for kind, identifier in records.things():
        if kind in ("person", "team"):
            kinds.setdefault(identifier, kind)
    team_of = {}
    for r in records:
        if r["type"] == "person" and r["attribute"] == "team":
            team_of.setdefault(r["identifier"], []).append(r["value"])
    out = []
    for kind, identifier in assets(week):
        values = list(
            dict.fromkeys(
                r["value"]
                for r in records
                if (r["type"], r["identifier"]) == (kind, identifier) and r["attribute"] == "responsible"
            )
        )
        teams = set()
        for v in values:
            if kinds.get(v) == "team":
                teams.add(v)
            elif kinds.get(v) == "person":
                teams.update(team_of.get(v, []))
        yes = lambda b: "yes" if b else "no"
        out.append(
            {
                "asset": identifier,
                "responsible": values,
                "one_owner": yes(len(values) == 1),
                "one_person": yes(len(values) == 1 and kinds.get(values[0]) == "person"),
                "one_team": yes(len(teams) == 1 and len(values) == 1),
            }
        )
    return Rows(out, null="")


def records(text: str) -> Records:
    """Chapter 3's records, from lines of text."""
    return Records(text)


def typed_records(text: str) -> TypedRecords:
    """Chapter 4's records, from lines of text that each start with a type."""
    return TypedRecords(text)


def model(text: str) -> Model:
    """A model of Chapter 4's records, from lines of text."""
    return Model(text)
