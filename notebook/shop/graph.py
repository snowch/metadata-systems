# Copyright © 2026 Christopher Snow

"""Records as a graph, and walks over it (Chapters 5 and 6).

Each entity the records describe is a node, named by its identifier and its type. Each line whose
attribute the model says names another entity is an edge, from the line's entity to the entity it
names, labelled with the attribute: `dataset daily_sales responsible: j.marsh` is an edge
`daily_sales -responsible-> j.marsh`. A value that names no entity the records describe makes no
edge (the model's check reports it).

`traverse` starts at one node and follows the edges it is told to follow, each forwards (`out`),
backwards (`in`) or both ways (`both`), and lists every node it reaches with the shortest path it
took. Chapter 6's `downstream` and `upstream` are two such walks over `reads` and `writes`.

`drawing` draws a graph as layers, top to bottom, in the course's phone-width image.
"""

from __future__ import annotations

import base64
from collections import deque
from html import escape

from .platform import Rows
from .records import Model, TypedRecords

DIRECTIONS = ("out", "in", "both")


class Graph:
    """The nodes and edges of a set of records under a model."""

    def __init__(self, records: TypedRecords, model: Model) -> None:
        things = records.things()
        self._nodes: list[tuple[str, str]] = sorted(things, key=lambda t: (t[0], t[1]))
        self._edges: list[tuple[tuple[str, str], str, tuple[str, str]]] = []
        for r in records:
            kinds = model.attribute(r["type"], r["attribute"])
            if not kinds or kinds == ["text"]:
                continue
            for kind in kinds:
                if (kind, r["value"]) in things:
                    edge = ((r["type"], r["identifier"]), r["attribute"], (kind, r["value"]))
                    if edge not in self._edges:
                        self._edges.append(edge)
                    break

    def nodes(self) -> Rows:
        """Every node: its identifier and its type."""
        return Rows({"node": i, "type": t} for t, i in self._nodes)

    def edges(self) -> Rows:
        """Every edge: the node it leaves, its attribute, and the node it reaches."""
        return Rows({"from": a[1], "edge": e, "to": b[1]} for a, e, b in self._edges)

    def _find(self, identifier: str) -> tuple[str, str]:
        found = [n for n in self._nodes if n[1] == identifier]
        if not found:
            raise KeyError(f"no node {identifier!r}")
        if len(found) > 1:
            raise KeyError(f"{identifier!r} names more than one node: {', '.join(t for t, _ in found)}")
        return found[0]

    def traverse(self, start: str, follow: dict[str, str] | None = None) -> Rows:
        """Every node reached from `start`, following the edges `follow` names, each in its direction.

        `follow` maps an attribute to `out`, `in` or `both`; without it, every edge is followed
        both ways. Each row gives a node, its type, the number of edges walked to reach it, and
        the path.
        """
        follow = follow if follow is not None else {e: "both" for _, e, _ in self._edges}
        for attribute, direction in follow.items():
            if direction not in DIRECTIONS:
                raise ValueError(f"{attribute}: the direction is one of {', '.join(DIRECTIONS)}")
        origin = self._find(start)
        seen = {origin: (0, origin[1])}
        queue = deque([origin])
        order = []
        while queue:
            node = queue.popleft()
            steps, path = seen[node]
            for a, e, b in self._edges:
                way = follow.get(e)
                nexts = []
                if way in ("out", "both") and a == node:
                    nexts.append((b, f"{path} -{e}-> {b[1]}"))
                if way in ("in", "both") and b == node:
                    nexts.append((a, f"{path} <-{e}- {a[1]}"))
                for n, p in nexts:
                    if n not in seen:
                        seen[n] = (steps + 1, p)
                        order.append(n)
                        queue.append(n)
        return Rows({"node": n[1], "type": n[0], "steps": seen[n][0], "path": seen[n][1]} for n in order)

    def downstream(self, start: str) -> Rows:
        """What is made, through jobs, from `start`: what reads it, what that writes, and so on."""
        return self.traverse(start, {"reads": "in", "writes": "out"})

    def upstream(self, start: str) -> Rows:
        """What `start` is made from, through jobs: what wrote it, what that read, and so on."""
        return self.traverse(start, {"writes": "in", "reads": "out"})

    def only(self, attributes: list[str], types: list[str]) -> "Graph":
        """The same graph with only these edges, and only nodes of these types."""
        g = object.__new__(Graph)
        g._nodes = [n for n in self._nodes if n[0] in types]
        g._edges = [(a, e, b) for a, e, b in self._edges if e in attributes and a in g._nodes and b in g._nodes]
        return g

    def drawing(self, layers: list[list[str]] | None = None, label: str = "") -> "Drawing":
        """The graph drawn as layers: by type, in the order given, or by the longest walk along the
        edges from a node with none coming in."""
        return Drawing(self, layers, label)


def graph(records: TypedRecords, model: Model) -> Graph:
    """The records as a graph under a model."""
    return Graph(records, model)


def compare_with_code(records: TypedRecords, repository: Rows) -> Rows:
    """The `reads` and `writes` lines of each job against what the job's code reads and writes.

    A line the code does not bear out, a read or write in the code that no line records, and a job
    with lines but no code in the repository: one row each.
    """
    from .week import reads_and_writes

    code = {r["job"]: reads_and_writes(r["code"]) for r in repository}
    lines: dict[tuple[str, str], list[dict]] = {}
    for r in records:
        if r["type"] == "job" and r["attribute"] in ("reads", "writes"):
            lines.setdefault((r["identifier"], r["attribute"]), []).append(r)
    out = []
    for job in dict.fromkeys(j for j, _ in lines):
        if job not in code:
            out.append({"line": None, "job": job, "says": "", "code": "", "problem": COMPARE["no_code"]})
            continue
    for (job, attribute), rows in lines.items():
        if job not in code:
            continue
        for r in rows:
            if r["value"] not in code[job][attribute]:
                out.append({"line": r["line"], "job": job, "says": f"{attribute}: {r['value']}", "code": "", "problem": COMPARE[f"not_in_code_{attribute}"]})
    for job, found in code.items():
        for attribute in ("reads", "writes"):
            said = {r["value"] for r in lines.get((job, attribute), [])}
            for value in found[attribute]:
                if value not in said:
                    out.append({"line": None, "job": job, "says": "", "code": f"{attribute}: {value}", "problem": COMPARE[f"not_said_{attribute}"]})
    return Rows(out, null="", empty=COMPARE["none"])


# What the comparison prints, in the reader's words: Haiku's drafts of brief FC (docs/notes/chapter-06/).
COMPARE = {
    "none": "Every line matches the job's code, and the code reads and writes nothing that the lines do not record.",
    "no_code": "The lines name a job that has no code in the repository.",
    "not_in_code_reads": "The line says the job reads this, but the job's code does not read it.",
    "not_in_code_writes": "The line says the job writes this, but the job's code does not write it.",
    "not_said_reads": "The job's code reads this, but no line says so.",
    "not_said_writes": "The job's code writes this, but no line says so.",
}


# Drawn as the week is: 340 units wide, 14-unit text, its own colours for each theme.
_WIDTH = 340
_TEXT = 14
_STYLE = (
    f"text{{font-family:system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;font-size:{_TEXT}px;fill:#1f2328}}"
    ".box{fill:#ffffff;stroke:#1f2328;stroke-opacity:.55}.job{fill:#1f2328;fill-opacity:.08;stroke:#1f2328;stroke-opacity:.55;stroke-dasharray:4 3}"
    ".edge{fill:none;stroke-width:1.6}.head{stroke:none}"
    ".e0{stroke:#2a9d8f}.f0{fill:#2a9d8f}.e1{stroke:#e76f51}.f1{fill:#e76f51}.e2{stroke:#6c7a89}.f2{fill:#6c7a89}.e3{stroke:#8e6bbf}.f3{fill:#8e6bbf}"
    "@media (prefers-color-scheme:dark){text{fill:#e6e6e6}.box{fill:#1f2328;stroke:#e6e6e6}"
    ".job{fill:#e6e6e6;fill-opacity:.12;stroke:#e6e6e6}.e2{stroke:#a7b3bf}.f2{fill:#a7b3bf}}"
)


def _short(identifier: str) -> str:
    return identifier.rsplit("/", 1)[1] if "/" in identifier else identifier


# Rough widths of characters in a sans-serif face at 14 units, a little generous, so a label's box
# fits its text on any phone: narrow letters, wide letters and the rest.
_NARROW = set("fijlrt.,:;'!|()[]-")
_WIDE = set("mwMW@%")


def _text_width(text: str) -> float:
    return sum(4.6 if c in _NARROW else 11.5 if c in _WIDE else 8.0 if c.isupper() or c.isdigit() else 7.3 for c in text)


def _box_width(node, pad: float = 18) -> float:
    return 12.0 if node[0] == "bend" else _text_width(_short(node[1])) + pad


class Drawing:
    """A graph drawn as an image the notebook shows: each connected part on its own, its nodes in
    layers, edges as arrows, and a key."""

    # Without jobs, a graph is drawn by type, each edge pointing down: a column to its dataset, an
    # asset to the person or team responsible, a person to a team.
    BY_TYPE = [["column"], ["dataset", "dashboard"], ["person"], ["team"]]

    def __init__(self, g: Graph, layers: list[list[str]] | None, label: str) -> None:
        if layers is None and not any(n[0] == "job" for n in g._nodes):
            layers = self.BY_TYPE
        self.graph, self.label, self.layers = g, label, layers

    def _parts(self) -> list[list[list[tuple[str, str]]]]:
        """Each connected part of the graph, as its layers of nodes, top to bottom."""
        g = self.graph
        near = {n: set() for n in g._nodes}
        for a, _e, b in g._edges:
            near[a].add(b)
            near[b].add(a)
        parts, seen = [], set()
        for n in g._nodes:
            if n in seen:
                continue
            group, stack = [], [n]
            seen.add(n)
            while stack:
                m = stack.pop()
                group.append(m)
                for o in sorted(near[m]):
                    if o not in seen:
                        seen.add(o)
                        stack.append(o)
            parts.append(group)
        self.chains: dict[int, list[tuple[str, str]]] = {}
        if self.layers is not None:
            layered = [[[n for n in g._nodes if n in part and n[0] in types] for types in self.layers] for part in parts]
        else:
            # The order data flows: a `reads` edge from the asset to the job, a `writes` edge from
            # the job to the asset. Each node one layer below the deepest node flowing into it; a
            # node nothing flows into, one layer above the first node it flows into.
            flows = [((b, a) if e == "reads" else (a, b)) for a, e, b in g._edges]
            depth = {n: 0 for n in g._nodes}
            for _ in g._nodes:
                for src, dst in flows:
                    depth[dst] = max(depth[dst], depth[src] + 1)
            for n in g._nodes:
                if not any(dst == n for _, dst in flows):
                    after = [depth[dst] for src, dst in flows if src == n]
                    if after:
                        depth[n] = min(after) - 1
            # An edge that skips a layer bends through a point in each layer it crosses.
            for k, (src, dst) in enumerate(flows):
                points = [("bend", f"{k}:{d}") for d in range(depth[src] + 1, depth[dst])]
                for d, pnt in zip(range(depth[src] + 1, depth[dst]), points):
                    depth[pnt] = d
                if points:
                    self.chains[k] = points
            layered = []
            for part in parts:
                members = list(part) + [p for k, pts in self.chains.items() for p in pts if flows[k][0] in part]
                top = max(depth[n] for n in members)
                layered.append([[n for n in members if depth[n] == d] for d in range(top + 1)])
        # The biggest part first; within it, layers without nodes dropped.
        layered = [[row for row in part if row] for part in layered]
        return sorted(layered, key=lambda part: -sum(len(r) for r in part if r[0][0] != "bend"))

    def _place(self):
        g = self.graph
        parts_ = self._parts()
        near: dict = {n: set() for n in g._nodes}
        for k, (a, e, b) in enumerate(g._edges):
            src, dst = (b, a) if e == "reads" else (a, b)
            chain = [src] + self.chains.get(k, []) + [dst]
            for u, v in zip(chain, chain[1:]):
                near.setdefault(u, set()).add(v)
                near.setdefault(v, set()).add(u)
        pos, y, h = {}, 8.0, 28
        for part in parts_:
            for row in part:
                # Order a layer by where its neighbours already stand, so edges cross less.
                placed = [n for n in row if any(o in pos for o in near[n])]
                key = lambda n: sum(pos[o][0] + pos[o][2] / 2 for o in near[n] if o in pos) / max(1, sum(1 for o in near[n] if o in pos))
                row = sorted(placed, key=key) + sorted((n for n in row if n not in placed), key=lambda n: n[1])
                # A wide layer is drawn tighter before it is split over two lines.
                pad, gap = 18, 8
                if sum(_box_width(n) for n in row) + gap * (len(row) - 1) > _WIDTH - 8:
                    pad, gap = 8, 4
                lines, line, width = [], [], 0.0
                for n in row:
                    w = _box_width(n, pad)
                    if line and width + gap + w > _WIDTH - 4:
                        lines.append((line, width))
                        line, width = [], 0.0
                    width += (gap if line else 0) + w
                    line.append((n, w))
                lines.append((line, width))
                for line, width in lines:
                    x = (_WIDTH - width) / 2
                    for n, w in line:
                        pos[n] = (x, y, w, h)
                        x += w + gap
                    y += h + 10
                y += 22
            y += 18
        return pos, y - 40

    def svg(self) -> str:
        pos, height = self._place()
        kinds = list(dict.fromkeys(e for _, e, _ in self.graph._edges))
        parts = []
        for i, (a, e, b) in enumerate(self.graph._edges):
            k = kinds.index(e) % 4
            src, dst = (b, a) if e == "reads" else (a, b)
            (x0, y0, w0, h0), (x1, y1, w1, h1) = pos[src], pos[dst]
            down = y1 > y0
            sx, sy = x0 + w0 / 2, (y0 + h0 if down else y0)
            ex, ey = x1 + w1 / 2, (y1 if down else y1 + h1)
            points = [(sx, sy)]
            for bend in self.chains.get(i, []):
                bx, by, bw, bh = pos[bend]
                points += [(bx + bw / 2, by), (bx + bw / 2, by + bh)]
            points.append((ex, ey))
            line = " ".join(f"{px:.1f},{py:.1f}" for px, py in points)
            parts.append(f'<polyline class="edge e{k}" points="{line}"/>')
            d = 1 if down else -1
            parts.append(f'<path class="head f{k}" d="M{ex:.1f},{ey:.1f} l-4.5,{-8 * d} l9,0 z"/>')
        for n, (x, y, w, h) in pos.items():
            if n[0] == "bend":
                continue
            cls = "job" if n[0] == "job" else "box"
            parts.append(f'<rect class="{cls}" x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h}" rx="6"/>')
            parts.append(f'<text x="{x + w / 2:.1f}" y="{y + 19:.1f}" text-anchor="middle">{escape(_short(n[1]))}</text>')
        y = height + 30
        for k, e in enumerate(kinds):
            words = "read by" if e == "reads" else e
            parts.append(f'<line class="edge e{k % 4}" x1="6" y1="{y - 5}" x2="30" y2="{y - 5}"/>')
            parts.append(f'<text x="38" y="{y}">{escape(words)}</text>')
            y += 22
        height = y - 8
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {_WIDTH} {height:.0f}" width="{_WIDTH}" height="{height:.0f}">'
            f"<style>{_STYLE}</style>{''.join(parts)}</svg>"
        )

    def _repr_html_(self) -> str:
        data = base64.b64encode(self.svg().encode("utf-8")).decode("ascii")
        return f'<img class="ms-svg" alt="{escape(self.label)}" src="data:image/svg+xml;base64,{data}">'

    def _mime_(self) -> tuple[str, str]:
        return ("text/html", self._repr_html_())
