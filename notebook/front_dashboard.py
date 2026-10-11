# Copyright © 2026 Christopher Snow

"""Writes the dashboard the course's front page shows, from the shop's engine.

The front page shows Monday morning's dashboard, as Chapters 1 and 2 do. The page is the course's
own React shell, which has no engine of its own, so the dashboard's title, refresh time and values
come from here, as JSON, and notebook/tests/test_front.py fails if the file the page ships differs
from what the engine gives.

Usage: python3 notebook/front_dashboard.py   (writes apps/course/src/dashboard.json)
"""

import json
from pathlib import Path

import shop

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "apps" / "course" / "src" / "dashboard.json"


def dashboard() -> dict:
    """The dashboard as Monday morning shows it: its title, when it was refreshed, and each day's
    revenue, as the reporting tool shows it and in pence, for the bars' lengths."""
    week = shop.run_week()
    d = week.reporting.dashboard()
    pence = {r["day"]: r["revenue_pence"] for r in week.warehouse.sql("SELECT * FROM daily_sales")}
    return {
        "title": d["title"],
        "lastRefreshed": d["last_refreshed"],
        "values": [{"day": v["day"], "shown": v["revenue"], "pence": pence[v["day"]]} for v in d["values"]],
    }


def text() -> str:
    return json.dumps(dashboard(), indent=2, ensure_ascii=False) + "\n"


if __name__ == "__main__":
    OUT.write_text(text(), encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}")
