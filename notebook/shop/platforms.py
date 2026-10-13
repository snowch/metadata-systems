# Copyright © 2026 Christopher Snow

"""Four metadata platforms compared, and the shop's owners put to each one's rules (Chapter 31).

No platform runs here. `architectures` sets out what each project's own documentation and code
say, read at the commits `docs/sources.md` names ("Read for Part VII"); `owners_in` applies each
platform's rule for an owner, as its code states it, to the three owners of `daily_sales`
(Chapter 27: the warehouse's account, the person responsible, the team):

- DataHub (`Owner.pdl`; `ownership-types.yaml`): a list of owners; each names a user
  (`urn:li:corpuser:...`) or a group (`urn:li:corpGroup:...`) and carries an ownership type as a
  `typeUrn`, the name of an ownership type record (`urn:li:ownershipType:...`). DataHub defines four
  of these records, each with a name and a description; an organisation can define more. The older
  field `type`, an enum, is marked deprecated, and the shop does not use it.
- OpenMetadata (`EntityRepository.validateOwners`): a list of owners; each is a user, or a team
  whose team type is `Group`; any other kind is refused. An owner carries no ownership type.
- Apache Atlas (`0010-base_model.json`): one optional text attribute, `owner`, on every asset.
- Marquez (its service models and API): no owner on a dataset; a namespace has one, and a namespace
  made from an OpenLineage event gets the owner `anonymous`.

`check` holds the learner's DataHub ownership types to the form of a `typeUrn` and asks whether a
reader could tell the three owners apart by them. It does not check that a type the learner names
has a record, as DataHub would need one: that is the shop's simplification.
"""

from __future__ import annotations

from .platform import Rows

OWNERS = (
    ("account", "etl_service", "user"),
    ("responsible", "j.marsh", "user"),
    ("team", "data team", "group"),
)
PREFIX = "urn:li:ownershipType:"
# DataHub's own ownership type records (`bootstrap_mcps/ownership-types.yaml`): name and description.
BUILT_IN = {
    f"{PREFIX}__system__technical_owner": ("Technical Owner", "Involved in the production, maintenance, or distribution of the asset(s)."),
    f"{PREFIX}__system__business_owner": ("Business Owner", "Principal stakeholders or domain experts associated with the asset(s)."),
    f"{PREFIX}__system__data_steward": ("Data Steward", "Involved in governance of the asset(s)."),
    f"{PREFIX}__system__none": ("None", "No ownership type specified."),
}
PLATFORMS = ("DataHub", "OpenMetadata", "Apache Atlas", "Marquez")

MESSAGES = {
    "summary": "{passed} of {total} tests pass.",
    "valid": "Each ownership type is written as DataHub names one: `urn:li:ownershipType:` and a name.",
    "valid_no": "Not written as DataHub names an ownership type ({bad}): use `urn:li:ownershipType:` and a name.",
    "apart": "Each of the three owners has its own ownership type, so a reader can tell the three apart.",
    "apart_no": "{same} share the ownership type `{type}`, so a reader cannot tell them apart.",
}


def architectures() -> Rows:
    """How metadata arrives, is modelled, kept and searched, platform by platform."""
    return Rows([
        {"platform": "DataHub", "metadata arrives": "pulled by connectors on a schedule, or pushed", "modelled as": "entities and aspects, in a schema language", "kept in": "a database: MySQL, PostgreSQL or Cassandra", "searched through": "a search index"},
        {"platform": "OpenMetadata", "metadata arrives": "pulled by connectors on a schedule, or pushed, through one API", "modelled as": "JSON Schemas", "kept in": "a database: MySQL or PostgreSQL", "searched through": "a search index"},
        {"platform": "Apache Atlas", "metadata arrives": "pushed: messages from hooks in other systems, or calls to its API", "modelled as": "a type system of entities", "kept in": "a graph store", "searched through": "a search index"},
        {"platform": "Marquez", "metadata arrives": "pushed: OpenLineage events, or calls to its API", "modelled as": "namespaces, sources, datasets, jobs and runs", "kept in": "PostgreSQL", "searched through": "a search index, off unless set"},
    ])


STARTING_TYPES = {"account": f"{PREFIX}__system__technical_owner", "responsible": f"{PREFIX}__system__technical_owner", "team": f"{PREFIX}__system__technical_owner"}


def _valid(t) -> bool:
    return isinstance(t, str) and t.startswith(PREFIX) and len(t) > len(PREFIX)


def _stored(platform: str, types: dict) -> list[dict]:
    """What the platform keeps of the three owners: each kept owner, and its ownership type."""
    if platform == "DataHub":
        return [
            {"owner": who, "as": f"urn:li:{'corpuser' if kind == 'user' else 'corpGroup'}:{who.replace(' ', '_')}", "type": types.get(meaning)}
            for meaning, who, kind in OWNERS
        ]
    if platform == "OpenMetadata":
        return [{"owner": who, "as": "a user" if kind == "user" else "a team of team type Group", "type": None} for meaning, who, kind in OWNERS]
    if platform == "Apache Atlas":
        meaning, who, _ = OWNERS[0]
        return [{"owner": who, "as": "the text of `owner`", "type": None}]
    return []


def owners_in(types: dict | None = None) -> Rows:
    """Each platform's record of `daily_sales`'s owners, under its rule. Atlas has room for one: here,
    the first of the three. A DataHub ownership type of its own shows its name and description."""
    types = types or STARTING_TYPES
    out = []
    for platform in PLATFORMS:
        stored = _stored(platform, types)
        for st in stored:
            name, description = BUILT_IN.get(st["type"], (None, None))
            out.append({"platform": platform, "owner": st["owner"], "stored as": st["as"], "ownership type": st["type"], "its description": description})
        if not stored:
            out.append({"platform": platform, "owner": None, "stored as": "no owner on a dataset", "ownership type": None, "its description": None})
    return Rows(out, null="")


def kept(types: dict | None = None) -> Rows:
    """For each platform: how many of the three owners it keeps, and how many of those a reader can
    tell from the others by an ownership type that is written as a `typeUrn` and that no other owner
    has."""
    types = types or STARTING_TYPES
    out = []
    for platform in PLATFORMS:
        stored = _stored(platform, types)
        typed = [st["type"] for st in stored if _valid(st["type"])]
        apart = sum(1 for t in typed if typed.count(t) == 1) if len(stored) > 1 else 0
        out.append({"platform": platform, "owners kept": len(stored), "owners told apart by ownership type": apart})
    return Rows(out)


class Checked(Rows):
    def __init__(self, rows) -> None:
        super().__init__(rows)
        self.passed = sum(r["passes"] == "yes" for r in rows)

    def _repr_html_(self) -> str:
        return f"<p>{MESSAGES['summary'].format(passed=self.passed, total=len(self))}</p>" + super()._repr_html_()


def _and(names: list[str]) -> str:
    return names[0] if len(names) == 1 else ", ".join(names[:-1]) + " and " + names[-1]


def check(types: dict) -> Checked:
    """The learner's DataHub ownership types for the three owners: each written as a `typeUrn`, and
    each its own."""
    bad = [f"`{who}`: `{types.get(meaning)}`" for meaning, who, _ in OWNERS if not _valid(types.get(meaning))]
    rows = [{
        "test": MESSAGES["valid"] if not bad else MESSAGES["valid_no"].format(bad=", ".join(bad)),
        "passes": "no" if bad else "yes",
    }]
    shared: dict = {}
    for meaning, who, _ in OWNERS:
        shared.setdefault(types.get(meaning), []).append(f"`{who}`")
    same = [(t, ws) for t, ws in shared.items() if len(ws) > 1]
    rows.append({
        "test": MESSAGES["apart"] if not same else MESSAGES["apart_no"].format(same=_and(same[0][1]), type=same[0][0]),
        "passes": "no" if same else "yes",
    })
    return Checked(rows)


STUBS = {"types": 'types = {\n    "account": "urn:li:ownershipType:__system__technical_owner",\n    "responsible": "urn:li:ownershipType:__system__technical_owner",\n    "team": "urn:li:ownershipType:__system__technical_owner",\n}'}
REFERENCE = {"types": 'types = {\n    "account": "urn:li:ownershipType:warehouse_account",\n    "responsible": "urn:li:ownershipType:__system__business_owner",\n    "team": "urn:li:ownershipType:__system__technical_owner",\n}'}

__all__ = ["architectures", "owners_in", "kept", "check", "STUBS", "REFERENCE", "OWNERS", "BUILT_IN", "PLATFORMS"]
