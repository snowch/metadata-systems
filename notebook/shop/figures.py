# Copyright © 2026 Christopher Snow

"""The chapter's figures, drawn as HTML and SVG from the engine's data.

Each figure shows only what the learner has been told: the pipeline names the systems and the
assets each holds, and never draws an asset made from another, because which asset is made from
which is what Chapter 1 shows the platform cannot tell. Colours follow the page's theme: text and
lines use the current colour, and fills are translucent mixes of it.
"""

from __future__ import annotations

from datetime import datetime, timezone
from html import escape

from .data import ARRIVAL, DAYS
from .week import Week, timeline

_STYLE = """
<style>
.ms-fig { font-size: 0.95rem; line-height: 1.4; }
.ms-fig code, .ms-mono { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: 0.88em; }
.ms-systems { display: grid; grid-template-columns: 1fr auto 1fr auto 1fr; gap: 0.5rem; align-items: stretch; }
.ms-system { border: 1px solid color-mix(in srgb, currentColor 30%, transparent); border-radius: 8px; padding: 0.6rem 0.75rem; }
.ms-system h4 { margin: 0 0 0.4rem; font-size: 0.72rem; letter-spacing: 0.08em; text-transform: uppercase; opacity: 0.75; }
.ms-system ul { list-style: none; margin: 0; padding: 0; }
.ms-system li { margin: 0.15rem 0; }
.ms-kind { font-size: 0.68rem; letter-spacing: 0.06em; text-transform: uppercase; opacity: 0.6; margin-left: 0.35rem; }
.ms-flow { display: flex; align-items: center; justify-content: center; text-align: center; font-size: 0.75rem; opacity: 0.7; max-width: 7.5rem; }
.ms-tally { margin-top: 0.6rem; opacity: 0.85; }
@media (max-width: 640px) {
  .ms-systems { grid-template-columns: 1fr; }
  .ms-flow { max-width: none; }
  .ms-flow::before { content: "\\2193\\00a0"; }
  .ms-flow .ms-right { display: none; }
}
.ms-bars { display: grid; grid-template-columns: auto 1fr auto; gap: 0.25rem 0.6rem; align-items: center; }
.ms-bar { height: 0.9rem; border-radius: 3px; background: color-mix(in srgb, #2a9d8f 75%, transparent); }
.ms-muted { opacity: 0.7; font-size: 0.85rem; }
.ms-figure { margin: 0.5rem 0 1rem; }
.ms-figure figcaption { font-size: 0.85rem; opacity: 0.75; margin-bottom: 0.4rem; }
.ms-raw { max-height: 16rem; overflow: auto; padding: 0.5rem 0.6rem; border-radius: 6px; background: color-mix(in srgb, currentColor 6%, transparent); white-space: pre; }
</style>
"""

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


def pipeline(week: Week, flow_label: str = "unseen programs move data each night") -> str:
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
    return f'{_STYLE}<div class="ms-fig"><div class="ms-systems">{"".join(cells)}</div><div class="ms-tally">{escape(tally(systems))}</div></div>'


def week_strip(
    week: Week,
    start_label: str = "You start work at 09:00",
    keys: tuple[str, str, str] = ("the days the shop took orders", "a night's work", "the morning you start work"),
) -> str:
    """The shop's first week on one line: the order days, each night's work, and the morning you start."""
    days = list(DAYS) + ["2026-09-14"]
    width, left, top, row = 800, 10, 22, 26
    col = (width - 2 * left) / len(days)
    hour = col / 24

    def x(iso: str) -> float:
        t = datetime.strptime(iso, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
        i = days.index(t.strftime("%Y-%m-%d"))
        return left + i * col + (t.hour + t.minute / 60 + t.second / 3600) * hour

    parts = []
    for i, d in enumerate(days):
        cx = left + i * col
        parts.append(f'<rect x="{cx:.1f}" y="{top}" width="{col:.1f}" height="{row}" fill="none" stroke="currentColor" stroke-opacity="0.25"/>')
        parts.append(f'<text x="{cx + col / 2:.1f}" y="{top - 7}" text-anchor="middle" font-size="12" fill="currentColor">{_day_label(d)}</text>')
    band_w = col * len(DAYS)
    parts.append(f'<rect x="{left}" y="{top + 4}" width="{band_w:.1f}" height="{row - 8}" fill="currentColor" fill-opacity="0.12"/>')
    for n in timeline(week):
        x0, x1 = x(n["started"]), x(n["finished"])
        parts.append(f'<rect x="{x0:.1f}" y="{top + 2}" width="{max(x1 - x0, 3):.1f}" height="{row - 4}" fill="#2a9d8f"/>')
    ax = x(ARRIVAL)
    parts.append(f'<line x1="{ax:.1f}" x2="{ax:.1f}" y1="{top - 2}" y2="{top + row + 6}" stroke="#e76f51" stroke-width="2.5"/>')
    parts.append(f'<text x="{min(ax + 4, width - 4):.1f}" y="{top + row + 18}" text-anchor="end" font-size="12" fill="currentColor">{escape(start_label)}</text>')
    legend_y = top + row + 40
    legend = [("currentColor", 0.12, keys[0]), ("#2a9d8f", 1, keys[1]), ("#e76f51", 1, keys[2])]
    lx = left
    for colour, opacity, label in legend:
        parts.append(f'<rect x="{lx}" y="{legend_y - 10}" width="14" height="10" fill="{colour}" fill-opacity="{opacity}"/>')
        parts.append(f'<text x="{lx + 20}" y="{legend_y}" font-size="12" fill="currentColor">{escape(label)}</text>')
        lx += 30 + 7.2 * len(label)
    heard = (
        f"The shop's first week: the shop took orders from {_day_label(DAYS[0])} to {_day_label(DAYS[-1])} September; "
        f"each night's work ran in the early hours of the next day; you start work at 09:00 on Mon 14."
    )
    svg = (
        f'<svg viewBox="0 0 {width} {legend_y + 8}" width="100%" role="img" aria-label="{escape(heard)}" '
        f'style="max-width:{width}px; height:auto; display:block">{"".join(parts)}</svg>'
    )
    return f'{_STYLE}<div class="ms-fig">{svg}</div>'


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
        f'{_STYLE}<div class="ms-fig"><strong>{escape(d["title"])}</strong>'
        f'<div class="ms-muted">Last refreshed {escape(show_time(d["last_refreshed"]))}.</div>'
        f'<div class="ms-bars" style="margin-top:0.5rem">{rows}</div></div>'
    )


def raw_text(week: Week, uri: str, caption: str = "The first {shown} of {total} lines.", lines: int = 7) -> str:
    """The first lines of a file, exactly as stored."""
    text = week.storage.read_text(uri).splitlines()
    shown = "\n".join(text[:lines])
    more = len(text) - lines
    note = f'<div class="ms-muted">{escape(caption.format(shown=lines, total=len(text)))}</div>' if more > 0 else ""
    return f'{_STYLE}<div class="ms-fig"><div class="ms-raw ms-mono">{escape(shown)}</div>{note}</div>'


def figure(body: str, caption: str) -> str:
    """A figure with its caption above it, as the chapter captions its figures."""
    return f'{_STYLE}<figure class="ms-figure"><figcaption>{escape(caption)}</figcaption>{body}</figure>'
