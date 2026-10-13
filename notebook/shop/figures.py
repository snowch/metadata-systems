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


def pipeline(week: Week, flow_label: str = "unseen jobs move data each night") -> str:
    """The three systems, in the order data moves through them, with what each holds and a count."""
    systems = platform_assets(week)
    cells = []
    for i, (name, assets) in enumerate(systems):
        items = "".join(
            f'<li><code>{escape(a)}</code><span class="ms-kind">{_KIND_LABEL[k]}</span></li>' for a, k in assets
        )
        cells.append(f'<div class="ms-system"><h4>{escape(name)}</h4><ul>{items}</ul></div>')
        if i < len(systems) - 1:
            cells.append(f'<div class="ms-flow">{escape(flow_label)}<span class="ms-right">&nbsp;&rarr;</span></div>')
    return f'<div class="ms-fig"><div class="ms-systems">{"".join(cells)}</div><div class="ms-tally">{escape(tally(systems))}</div></div>'


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
