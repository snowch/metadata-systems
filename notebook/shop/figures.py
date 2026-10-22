# Copyright © 2026 Christopher Snow

"""The chapters' figures, drawn from the engine's data when the site is built.

The build writes each figure into a notebook's Markdown cell, so a reader sees it before running
anything. A Markdown cell keeps HTML's boxes and lists and drops `<style>` and inline `<svg>`, so:

- the platform and the dashboard are HTML with class names only: the course's stylesheet
  (notebook/buttons/style/index.css) draws them in the theme's own colours, and on a phone the
  platform's systems stack into one column;
- the week is an SVG image, base64 in a data URI, drawn at a phone's width so its words stay
  readable there, with its own colours for the light and the dark theme (an image cannot take the
  page's), and one sentence saying the same as its alternative text.

Each figure shows only what the learner has been told: the pipeline names the systems and the
assets each holds, and never draws an asset made from another, because which asset is made from
which is what Chapter 2 shows the platform cannot tell.
"""

from __future__ import annotations

import base64
from datetime import datetime, timezone
from html import escape

from .data import ARRIVAL, DAYS
from .week import Week, timeline


_KIND_LABEL = {"file": "file", "table": "table", "dashboard": "dashboard"}


def _day_label(day: str) -> str:
    d = datetime.strptime(day, "%Y-%m-%d")
    return f"{d.strftime('%a')} {d.day}"


def show_time(iso: str) -> str:
    """A time as a person reads it: 2026-09-14 02:30:21 UTC."""
    return iso.replace("T", " ").replace("Z", " UTC")


def platform_assets(week: Week) -> list[tuple[str, list[tuple[str, str]]]]:
    """The systems, in the order data moves through them, and the assets each holds by kind."""
    files = [(r["key"].rsplit("/", 1)[1], "file") for r in week.storage.ls("s3://shop-raw/")]
    # From Chapter 7, the returns desk's bucket: one small file per return.
    files += [(r["key"].rsplit("/", 1)[1], "file") for r in week.storage.ls("s3://shop-returns/")]
    tables = [
        (r["table_name"], "table")
        for r in week.warehouse.sql("SELECT table_name FROM information_schema.tables ORDER BY rowid")
    ]
    dashboards = [(week.reporting.dashboard()["name"], "dashboard")]
    return [("Object storage", files), ("Warehouse", tables), ("Reporting tool", dashboards)]


def tally(systems) -> str:
    counts: dict[str, int] = {}
    for _, assets in systems:
        for _, kind in assets:
            counts[kind] = counts.get(kind, 0) + 1
    parts = [f"{n} {kind}{'' if n == 1 else 's'}" for kind, n in counts.items()]
    total = sum(counts.values())
    return f"{' + '.join(parts)} = {total} asset{'' if total == 1 else 's'}"


def pipeline(week: Week, flow_label: str = "Nightly jobs") -> str:
    """The three systems, in the order data moves through them, with what each holds and a count."""
    systems = platform_assets(week)
    cells = []
    for i, (name, assets) in enumerate(systems):
        items = "".join(
            f'<li><span class="ms-asset-icon ms-icon-{k}" aria-hidden="true"></span>'
            f'<span class="ms-visually-hidden">{_KIND_LABEL[k]}: </span><code>{escape(a)}</code></li>' for a, k in assets
        )
        cells.append(f'<div class="ms-system"><h4>{escape(name)}</h4><ul>{items}</ul></div>')
        if i < len(systems) - 1:
            cells.append('<div class="ms-flow" aria-hidden="true"><span class="ms-asset-icon ms-icon-job"></span><span class="ms-right">&rarr;</span></div>')
    legend = "".join(
        f'<span><span class="ms-asset-icon ms-icon-{kind}" aria-hidden="true"></span>{escape(label)}</span>'
        for kind, label in [*_KIND_LABEL.items(), ("job", flow_label)]
    )
    return f'<div class="ms-fig ms-pipeline"><div class="ms-systems">{"".join(cells)}</div><div class="ms-pipeline-key">{legend}</div><div class="ms-tally">{escape(tally(systems))}</div></div>'


# The week's image: drawn 340 units wide with 14-unit text. A 360-pixel phone gives a notebook's
# Markdown about 295 pixels, where the text shows at about 12 pixels; the stylesheet lets the image
# grow to 560 pixels on a wider screen. Each day's label takes two lines, so eight fit side by side.
_WEEK_WIDTH = 340
_WEEK_TEXT = 14
_WEEK_STYLE = (
    f"text{{font-family:system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;font-size:{_WEEK_TEXT}px;fill:#1f2328}}"
    ".grid{fill:none;stroke:#1f2328;stroke-opacity:.3}.band{fill:#1f2328;fill-opacity:.12}"
    ".night{fill:#2a9d8f}.start{stroke:#e76f51;stroke-width:2.5}.start-key{fill:#e76f51}"
    "@media (prefers-color-scheme:dark){text{fill:#e6e6e6}.grid{stroke:#e6e6e6}.band{fill:#e6e6e6;fill-opacity:.16}}"
)


def week_strip(
    week: Week,
    start_label: str = "You start work at 09:00",
    keys: tuple[str, str, str] = ("the days the shop took orders", "the export and jobs", "the morning you start work"),
) -> str:
    """The shop's first week on one line: the order days, the export and jobs each night, and the morning you start."""
    days = list(DAYS) + ["2026-09-14"]
    width, left, top, row = _WEEK_WIDTH, 4, 42, 26
    col = (width - 2 * left) / len(days)
    hour = col / 24

    def x(iso: str) -> float:
        t = datetime.strptime(iso, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        i = days.index(t.strftime("%Y-%m-%d"))
        return left + i * col + (t.hour + t.minute / 60 + t.second / 3600) * hour

    parts = []
    for i, d in enumerate(days):
        cx = left + i * col
        parts.append(f'<rect class="grid" x="{cx:.1f}" y="{top}" width="{col:.1f}" height="{row}"/>')
        weekday, date = _day_label(d).split(" ")
        parts.append(f'<text x="{cx + col / 2:.1f}" y="{top - 24}" text-anchor="middle">{weekday}</text>')
        parts.append(f'<text x="{cx + col / 2:.1f}" y="{top - 7}" text-anchor="middle">{date}</text>')
    parts.append(f'<rect class="band" x="{left}" y="{top + 4}" width="{col * len(DAYS):.1f}" height="{row - 8}"/>')
    for n in timeline(week):
        x0, x1 = x(n["started"]), x(n["finished"])
        parts.append(f'<rect class="night" x="{x0:.1f}" y="{top + 2}" width="{max(x1 - x0, 3):.1f}" height="{row - 4}"/>')
    ax = x(ARRIVAL)
    parts.append(f'<line class="start" x1="{ax:.1f}" x2="{ax:.1f}" y1="{top - 2}" y2="{top + row + 6}"/>')
    parts.append(f'<text x="{width - left}" y="{top + row + 22}" text-anchor="end">{escape(start_label)}</text>')
    # The key, one line each, under the strip.
    legend = [("band", keys[0]), ("night", keys[1]), ("start-key", keys[2])]
    y = top + row + 48
    for cls, label in legend:
        parts.append(f'<rect class="{cls}" x="{left}" y="{y - 10}" width="14" height="10"/>')
        parts.append(f'<text x="{left + 22}" y="{y}">{escape(label)}</text>')
        y += 20
    height = y - 6
    heard = (
        f"The shop's first week: the shop took orders from {_day_label(DAYS[0])} to {_day_label(DAYS[-1])} September; "
        f"each night's export and jobs ran in the early hours of the next day; you start work at 09:00 on Mon 14."
    )
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">'
        f"<style>{_WEEK_STYLE}</style>{''.join(parts)}</svg>"
    )
    data = base64.b64encode(svg.encode("utf-8")).decode("ascii")
    return f'<img class="ms-svg" alt="{escape(heard)}" src="data:image/svg+xml;base64,{data}">'


def dashboard_chart(week: Week) -> str:
    """The dashboard as Monday morning shows it: one bar per day, in pounds."""
    d = week.reporting.dashboard()
    values = d["values"]
    pence = [int(v["revenue"].replace("£", "").replace(".", "")) for v in values]
    top = max(pence) if pence else 1
    rows = "".join(
        f'<span>{_day_label(v["day"])}</span><div><div class="ms-bar" style="width:{100 * p / top:.1f}%"></div></div>'
        f'<span class="ms-mono">{escape(v["revenue"])}</span>'
        for v, p in zip(values, pence)
    )
    return (
        f'<div class="ms-fig"><strong>{escape(d["title"])}</strong>'
        f'<div class="ms-muted">Last refreshed {escape(show_time(d["last_refreshed"]))}.</div>'
        f'<div class="ms-bars">{rows}</div></div>'
    )


def figure(body: str, caption: str) -> str:
    """A figure with its caption above it, as the chapter captions its figures."""
    parts = escape(caption).split("`")
    shown = "".join(f"<code>{p}</code>" if i % 2 else p for i, p in enumerate(parts))
    return f'<figure class="ms-figure"><figcaption>{shown}</figcaption>{body}</figure>'


# Chapter 2's figures for its investigation. Their words are drafted by the prose process
# (docs/notes/chapter-02/briefs/round-22/); every number in them is the engine's.

def _thursday(week: Week, day: str) -> tuple[int, int]:
    """A day's total of the raw orders, and that day's row in `daily_sales`, in pence."""
    from .week import FILES

    raw = sum(o["price_pence"] * o["quantity"] for o in week.storage.records(FILES["orders"]) if o["ordered_at"].startswith(day))
    [row] = week.warehouse.sql("SELECT revenue_pence FROM daily_sales WHERE day = :d", d=day)
    return raw, row["revenue_pence"]


def totals(week: Week, labels: tuple[str, str, str], day: str = "2026-09-10") -> str:
    """Three totals side by side: a day's raw orders, its row in `daily_sales`, and the difference."""
    from .platform import pounds

    raw, table = _thursday(week, day)
    tiles = []
    for label, pence, cls in zip(labels, (raw, table, raw - table), ("", "", " ms-stat-gap")):
        tiles.append(
            f'<div class="ms-stat{cls}"><div class="ms-stat-label">{_named(label)}</div>'
            f'<div class="ms-stat-value">{pounds(pence)}</div><div class="ms-muted">{pence} pence</div></div>'
        )
    return f'<div class="ms-fig ms-stats">{"".join(tiles)}</div>'


def _named(text: str) -> str:
    """Escapes a label, and sets a name written in backticks in the code font."""
    parts = escape(text).split("`")
    return "".join(f"<code>{p}</code>" if i % 2 else p for i, p in enumerate(parts))


def inferred(week: Week, labels: dict[str, str]) -> str:
    """The reconstruction as a link from one table to another, drawn dashed: inferred, not recorded.

    It draws the only query that rebuilds `daily_sales` exactly, and the two tables' row counts."""
    from .infer import queries_that_rebuild

    [query] = queries_that_rebuild(week)
    counts = {
        t: week.warehouse.sql(f"SELECT COUNT(*) AS n FROM {t}")[0]["n"] for t in (query["source"], "daily_sales")
    }
    node = lambda name, under: (
        f'<div class="ms-system ms-node"><code>{escape(name)}</code><div class="ms-muted">{_named(under)}</div></div>'
    )
    return (
        f'<div class="ms-fig"><div class="ms-link">'
        f'{node(query["source"], labels["from"].format(rows=counts[query["source"]]))}'
        f'<div class="ms-inferred"><span>{_named(labels["step"])}</span><span class="ms-arrow"></span>'
        f'<span class="ms-tag">{_named(labels["fit"].format(rows=counts["daily_sales"]))}</span></div>'
        f'{node("daily_sales", labels["to"].format(rows=counts["daily_sales"]))}'
        f'</div><div class="ms-muted ms-recorded">{_named(labels["recorded"])}</div></div>'
    )


def _columns(week: Week, table: str) -> list[str]:
    return [
        r["column_name"]
        for r in week.warehouse.sql(
            "SELECT column_name FROM information_schema.columns WHERE table_name = :t ORDER BY rowid", t=table
        )
    ]


# The hypothesis's image: two tables drawn at a phone's width, as the week is, with 14-unit names
# that show at about 12 pixels on a 360-pixel phone. The stylesheet keeps it to 420 pixels on a
# wider screen, so the names stay near the text's size.
_HYP_STYLE = (
    "text{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:14px;fill:#1f2328}"
    ".head{font-weight:700}.unused{fill-opacity:.45}"
    ".box{fill:none;stroke:#1f2328;stroke-opacity:.45}.band{fill:#1f2328;fill-opacity:.07}"
    ".rule{stroke:#1f2328;stroke-opacity:.15}"
    ".link{fill:none;stroke:#1f2328;stroke-opacity:.6;stroke-width:1.5;stroke-dasharray:4 3}"
    ".tip{fill:#1f2328;fill-opacity:.6}.dot{fill:#2a9d8f}.num{fill:#fff;font-family:system-ui,sans-serif;"
    "font-size:11px;font-weight:700}"
    "@media (prefers-color-scheme:dark){text{fill:#e6e6e6}.box,.rule{stroke:#e6e6e6}.band{fill:#e6e6e6}"
    ".link{stroke:#e6e6e6}.tip{fill:#e6e6e6}.num{fill:#1f2328}}"
)


def hypothesis(week: Week, labels: dict[str, str]) -> str:
    """The hypothesis column by column: `clean_orders` and `daily_sales` drawn as two tables, a
    dashed, numbered link from each column the hypothesis uses to the column it makes, and from
    `status` to the table, whose rows it decides; a numbered key under it says each step. The
    columns the hypothesis leaves unused are greyed, at the foot of their table. Every link is
    dashed: a guess the query then tests.

    The links are the parts of the one query that rebuilds `daily_sales` (shop/infer.py): the column
    it groups by, the sum it adds up, and the status it keeps. The columns are the warehouse's own."""
    import re

    from .infer import MEASURE, PER, queries_that_rebuild

    [query] = queries_that_rebuild(week)
    assert (query["keep"], query["measure"], query["per"]) == ("completed", "revenue", "day"), query
    source, target = query["source"], "daily_sales"
    have, made = _columns(week, source), _columns(week, target)

    def used(expr: str) -> list[str]:
        named = [c for c in have if re.search(rf"\b{c}\b", expr)]
        return sorted(named, key=expr.index)

    key, value, kept = used(PER[query["per"]]), used(MEASURE[query["measure"]]), used("status")
    unused = [c for c in have if c not in key + value + kept]
    left = key + value + kept + unused  # the used columns first, in the order of the links

    width, head, row, w = 340, 30, 26, 128
    lx, rx = 2, width - 2 - w
    y = lambda i: head + i * row + row / 2  # the middle of a column's row
    parts = []

    def table(x: float, name: str, cols: list[str], dim: set[str]) -> None:
        h = head + row * len(cols)
        parts.append(f'<rect class="band" x="{x}" y="1" width="{w}" height="{head - 1}" rx="5"/>')
        parts.append(f'<rect class="box" x="{x}" y="1" width="{w}" height="{h - 1}" rx="5"/>')
        parts.append(f'<text class="head" x="{x + 10}" y="{head / 2 + 6}">{escape(name)}</text>')
        for i, c in enumerate(cols):
            parts.append(f'<line class="rule" x1="{x}" x2="{x + w}" y1="{head + i * row}" y2="{head + i * row}"/>')
            cls = ' class="unused"' if c in dim else ""
            parts.append(f'<text{cls} x="{x + 10}" y="{y(i) + 5}">{escape(c)}</text>')

    table(lx, source, left, set(unused))
    table(rx, target, made, set())
    a, b = lx + w, rx  # the gap the links cross
    mid = (a + b) / 2

    def link(path: str, end: tuple[float, float], n: int, at: tuple[float, float]) -> None:
        parts.append(f'<path class="link" d="{path}"/>')
        ex, ey = end
        parts.append(f'<path class="tip" d="M{ex} {ey} l-7 -4 v8 z"/>')
        cx, cy = at
        parts.append(f'<circle class="dot" cx="{cx}" cy="{cy}" r="9"/>')
        parts.append(f'<text class="num" x="{cx}" y="{cy + 4}" text-anchor="middle">{n}</text>')

    # 1: the column it groups by, to the first column of daily_sales.
    yk, yd = y(left.index(key[0])), y(0)
    link(f"M{a} {yk} C{mid} {yk} {mid} {yd} {b - 7} {yd}", (b, yd), 1, (mid, (yk + yd) / 2))
    # 2: the columns it multiplies, joined, to the second.
    yv = y(1)
    jx, jy = mid, sum(y(left.index(c)) for c in value) / len(value)
    for c in value:
        yc = y(left.index(c))
        parts.append(f'<path class="link" d="M{a} {yc} C{a + 18} {yc} {jx - 18} {jy} {jx} {jy}"/>')
    link(f"M{jx} {jy} C{jx + 18} {jy} {b - 25} {yv} {b - 7} {yv}", (b, yv), 2, (jx, jy))
    # 3: the status, to the foot of daily_sales: it decides which rows reach the table.
    ys, foot = y(left.index(kept[0])), head + row * len(made)
    fx = rx + w / 2
    parts.append(f'<path class="link" d="M{a} {ys} C{fx - 30} {ys} {fx} {ys} {fx} {foot + 7}"/>')
    parts.append(f'<path class="tip" d="M{fx} {foot} l-4 7 h8 z"/>')
    parts.append(f'<circle class="dot" cx="{(a + fx) / 2}" cy="{ys - 2}" r="9"/>')
    parts.append(f'<text class="num" x="{(a + fx) / 2}" y="{ys + 2}" text-anchor="middle">3</text>')

    height = head + row * len(left) + 2
    heard = (
        f"{source} has the columns {', '.join(left)}; {target} has {', '.join(made)}. "
        f"1: {key[0]} links to {made[0]}. 2: {' and '.join(value)} link to {made[1]}. "
        f"3: {kept[0]} links to the table {target}. {', '.join(unused)} link to nothing."
    )
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">'
        f"<style>{_HYP_STYLE}</style>{''.join(parts)}</svg>"
    )
    data = base64.b64encode(svg.encode("utf-8")).decode("ascii")
    steps = "".join(f"<li>{_named(labels[k])}</li>" for k in ("per", "measure", "keep"))
    shown = ", ".join(f"`{c}`" for c in unused)
    return (
        '<div class="ms-fig ms-hyp">'
        f'<img class="ms-svg ms-svg-small" alt="{escape(heard)}" src="data:image/svg+xml;base64,{data}">'
        f'<ol class="ms-hyp-key">{steps}</ol>'
        f'<div class="ms-muted">{_named(labels["unused"].format(columns=shown))}</div>'
        "</div>"
    )


def two_sources(week: Week, labels: dict[str, str]) -> str:
    """With the analyst's copy: the two assets the same query fits, each linked to `daily_sales` by a
    dashed arrow, inferred, not recorded. The sources and the row counts are the engine's."""
    import re

    from .infer import queries_that_rebuild

    sources = [q["source"] for q in queries_that_rebuild(week)]
    assert len(sources) == 2 and sources[1].endswith("clean_orders_copy.csv"), sources
    table = week.warehouse.sql(f"SELECT COUNT(*) AS n FROM {sources[0]}")[0]["n"]
    copy = len(week.storage.records(sources[1]))
    target = week.warehouse.sql("SELECT COUNT(*) AS n FROM daily_sales")[0]["n"]
    # The copy's long name breaks after a slash or an underscore, where a reader would split it, not at
    # any letter; a table's name stays whole.
    breakable = lambda name: (
        re.sub(r"(?<!/)/(?!/)", "/<wbr>", escape(name)).replace("_", "_<wbr>") if "/" in name else escape(name)
    )
    node = lambda cls, name, under: (
        f'<div class="ms-system ms-node {cls}"><code>{breakable(name)}</code><div class="ms-muted">{_named(under)}</div></div>'
    )
    arrow = lambda cls: (
        f'<div class="ms-two-link {cls}"><span class="ms-tag">{_named(labels["fit"].format(rows=target))}</span>'
        '<span class="ms-hyp-arrow"></span></div>'
    )
    return (
        '<div class="ms-fig ms-two">'
        + node("ms-two-a", sources[0], labels["table"].format(rows=table))
        + arrow("ms-two-la")
        + node("ms-two-b", sources[1], labels["file"].format(rows=copy))
        + arrow("ms-two-lb")
        + node("ms-two-t", "daily_sales", labels["to"].format(rows=target))
        + "</div>"
    )


def three_records(week: Week, copied: Week, heads: tuple[str, str, str], rows: list[tuple[str, str, str]]) -> str:
    """For `daily_sales`: each question, what the platform holds, and the record that would answer it.

    The middle column's numbers are the warehouse's own: its columns, rows, last-altered time and
    owner. The sources a query fits come from the week with the analyst's copy."""
    from .infer import queries_that_rebuild

    [t] = week.warehouse.sql("SELECT * FROM information_schema.tables WHERE table_name = 'daily_sales'")
    columns = len(week.warehouse.sql("SELECT column_name FROM information_schema.columns WHERE table_name = 'daily_sales'"))
    altered = datetime.strptime(t["last_altered"], "%Y-%m-%dT%H:%M:%SZ")
    sources = [q["source"] for q in queries_that_rebuild(copied)]
    assert sources[0] == "clean_orders" and sources[1].endswith("clean_orders_copy.csv"), sources
    fill = {
        "columns": columns,
        "rows": t["row_count"],
        "time": f"{altered:%H:%M} {_day_label(t['last_altered'][:10])}",
        "owner": t["table_owner"],
    }
    head = "".join(f"<th>{escape(h)}</th>" for h in heads)
    body = "".join(
        "<tr>"
        + "".join(
            f'<td>{"" if i == 0 else f"<span class=\"ms-cell-label\">{escape(h)}</span>"}{_named(c.format(**fill))}</td>'
            for i, (h, c) in enumerate(zip(heads, row))
        )
        + "</tr>"
        for row in rows
    )
    return f'<div class="ms-fig"><table class="ms-records"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>'


# Chapter 33's second platform: four systems where the shop had three. The labels are drafted by the
# prose process (docs/notes/part-8/briefs/) and say only what the page has told the reader; the figure
# draws no arrow from one asset to another, and leaves what the platform records to the chapter's cells.
FERRY_FLOWS = ("a change starts a function", "the functions write to tables", "the jobs run at set times")


def ferry_platform(f) -> str:
    """The ferry's four systems, with what each holds now, and a count of each kind of part."""
    batches = len(f.storage.ls("s3://ferry-gates/"))
    reports = len(f.storage.ls("s3://ferry-reports/"))
    systems = [
        ("Object storage", "bucket", [("ferry-gates", f"{batches} batches"), ("ferry-reports", f"{reports} reports")]),
        ("Functions", "function", [("load_scans", "function"), ("drop_scans", "function")]),
        ("Warehouse", "table", [(t, "table") for t in ("sailings", "boardings", "sailing_loads")]),
        ("Scheduler", "job", [("build_loads", "job"), ("send_report", "job")]),
    ]
    cells = []
    for i, (name, _, parts) in enumerate(systems):
        items = "".join(f'<li><code>{escape(a)}</code><span class="ms-kind">{escape(k)}</span></li>' for a, k in parts)
        cells.append(f'<div class="ms-system"><h4>{escape(name)}</h4><ul>{items}</ul></div>')
        if i < len(systems) - 1:
            cells.append(f'<div class="ms-flow">{escape(FERRY_FLOWS[i])}<span class="ms-right">&nbsp;&rarr;</span></div>')
    tally = " + ".join(f"{len(parts)} {kind}s" for _, kind, parts in systems)
    return f'<div class="ms-fig"><div class="ms-systems ms-four">{"".join(cells)}</div><div class="ms-tally">{escape(tally)}</div></div>'
