# Copyright © 2026 Christopher Snow

"""Four metadata platforms compared, and the shop's owners put to each one's rules (Chapter 31).

No platform runs here. `architectures` sets out what each project's own documentation and code
say, read at the commits `docs/sources.md` names ("Read for Part VII"); `owners_in` applies each
platform's rule for an owner, as its code states it, to the three owners of `daily_sales`
(Chapter 27: the warehouse's account, the person responsible, the team):

- DataHub (`Owner.pdl`, `OwnershipType.pdl`): a list of owners; each is a user (`corpuser`) or a
  group (`corpGroup`), and has a type: `TECHNICAL_OWNER`, `BUSINESS_OWNER`, `DATA_STEWARD`, `NONE`,
  or a type the organisation defines, named by an `ownershipType` URN.
- OpenMetadata (`EntityRepository.validateOwners`): a list of owners; each is a user, or a team
  whose type is `Group`; any other kind is refused. An owner carries no type.
- Apache Atlas (`0010-base_model.json`): one optional text attribute, `owner`, on every asset.
- Marquez (its service models and API): no owner on a dataset; a namespace has one, and a namespace
  made from an OpenLineage event gets the owner `anonymous`.

`check` holds the learner's DataHub types to that rule and asks whether a reader could tell the
three owners' meanings apart.
"""

from __future__ import annotations

from .platform import Rows

OWNERS = (
    ("account", "etl_service", "user"),
    ("responsible", "j.marsh", "user"),
    ("team", "data team", "group"),
)
DATAHUB_TYPES = ("TECHNICAL_OWNER", "BUSINESS_OWNER", "DATA_STEWARD", "NONE")
CUSTOM = "urn:li:ownershipType:"

MESSAGES = {
    "summary": "{passed} of {total} tests pass.",
    "valid": "Each type is one DataHub accepts.",
    "valid_no": "DataHub does not accept {bad}: use one of {types}, or a type of your own as `urn:li:ownershipType:` and a name.",
    "apart": "Each of the three owners has its own type, so a reader can tell the three apart.",
    "apart_no": "{same} share the type `{type}`, so a reader cannot tell them apart.",
}


def architectures() -> Rows:
    """How metadata arrives, is modelled, stored and searched, platform by platform."""
    return Rows([
        {"platform": "DataHub", "metadata arrives": "pulled by connectors on a schedule, or pushed", "modelled as": "entities and aspects, in a schema language", "stored in": "a relational database", "searched through": "a search index"},
        {"platform": "OpenMetadata", "metadata arrives": "pulled by connectors on a schedule, or pushed, through one API", "modelled as": "JSON Schemas", "stored in": "a relational database", "searched through": "a search index"},
        {"platform": "Apache Atlas", "metadata arrives": "pushed, by hooks' messages or the API", "modelled as": "a type system of entities", "stored in": "a graph store", "searched through": "a search index"},
        {"platform": "Marquez", "metadata arrives": "pushed, as OpenLineage events or API calls", "modelled as": "namespaces, sources, datasets, jobs and runs", "stored in": "PostgreSQL", "searched through": "an optional search index"},
    ])


def _stored(platform: str, types: dict) -> list[dict]:
    """What the platform keeps of the three owners: each kept owner, and the type it carries."""
    if platform == "DataHub":
        return [
            {"owner": who, "as": f"urn:li:{'corpuser' if kind == 'user' else 'corpGroup'}:{who.replace(' ', '_')}", "type": types.get(meaning)}
            for meaning, who, kind in OWNERS
        ]
    if platform == "OpenMetadata":
        return [{"owner": who, "as": "a user" if kind == "user" else "a team of type Group", "type": None} for meaning, who, kind in OWNERS]
    if platform == "Apache Atlas":
        meaning, who, _ = OWNERS[0]
        return [{"owner": who, "as": "the text of `owner`", "type": None}]
    return []


PLATFORMS = ("DataHub", "OpenMetadata", "Apache Atlas", "Marquez")
EXAMPLE_TYPES = {"account": "TECHNICAL_OWNER", "responsible": "BUSINESS_OWNER", "team": "TECHNICAL_OWNER"}


def owners_in(types: dict | None = None) -> Rows:
    """Each platform's record of `daily_sales`'s owners, under its rule. Atlas has room for one: here,
    the first of the three."""
    types = types or EXAMPLE_TYPES
    out = []
    for platform in PLATFORMS:
        stored = _stored(platform, types)
        for st in stored:
            out.append({"platform": platform, "owner": st["owner"], "stored as": st["as"], "ownership type": st["type"]})
        if not stored:
            out.append({"platform": platform, "owner": None, "stored as": "no owner on a dataset", "ownership type": None})
    return Rows(out, null="")


def kept(types: dict | None = None) -> Rows:
    """For each platform: how many of the three owners it keeps, and how many meanings a reader can
    tell apart from what it keeps."""
    types = types or EXAMPLE_TYPES
    out = []
    for platform in PLATFORMS:
        stored = _stored(platform, types)
        typed = [st["type"] for st in stored if st["type"]]
        out.append({"platform": platform, "owners kept": len(stored), "meanings told apart": len(set(typed)) if len(typed) > 1 else 0})
    return Rows(out)


class Checked(Rows):
    def __init__(self, rows) -> None:
        super().__init__(rows)
        self.passed = sum(r["passes"] == "yes" for r in rows)

    def _repr_html_(self) -> str:
        return f"<p>{MESSAGES['summary'].format(passed=self.passed, total=len(self))}</p>" + super()._repr_html_()


def _valid(t) -> bool:
    return t in DATAHUB_TYPES or (isinstance(t, str) and t.startswith(CUSTOM) and len(t) > len(CUSTOM))


def _and(names: list[str]) -> str:
    return names[0] if len(names) == 1 else ", ".join(names[:-1]) + " and " + names[-1]


def check(types: dict) -> Checked:
    """The learner's DataHub types for the three owners: each accepted, and each its own."""
    given = [types.get(m) for m, _, _ in OWNERS]
    bad = [t for t in given if not _valid(t)]
    rows = [{
        "test": MESSAGES["valid"] if not bad else MESSAGES["valid_no"].format(bad=", ".join(f"`{b}`" for b in bad), types=", ".join(f"`{t}`" for t in DATAHUB_TYPES)),
        "passes": "no" if bad else "yes",
    }]
    shared = {}
    for (meaning, who, _), t in zip(OWNERS, given):
        shared.setdefault(t, []).append(f"`{who}`")
    same = [(t, ws) for t, ws in shared.items() if len(ws) > 1]
    rows.append({
        "test": MESSAGES["apart"] if not same else MESSAGES["apart_no"].format(same=_and(same[0][1]), type=same[0][0]),
        "passes": "no" if same else "yes",
    })
    return Checked(rows)


STUBS = {"types": 'types = {\n    "account": "TECHNICAL_OWNER",\n    "responsible": "TECHNICAL_OWNER",\n    "team": "TECHNICAL_OWNER",\n}'}
REFERENCE = {"types": 'types = {\n    "account": "urn:li:ownershipType:warehouse_account",\n    "responsible": "BUSINESS_OWNER",\n    "team": "TECHNICAL_OWNER",\n}'}

__all__ = ["architectures", "owners_in", "kept", "PLATFORMS", "check", "STUBS", "REFERENCE", "OWNERS", "DATAHUB_TYPES"]
