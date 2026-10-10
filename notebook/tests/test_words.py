# Copyright © 2026 Christopher Snow

"""Every sentence of the notebook that states a fact, pinned against the engine, and the prose rules.

The notebook's words are its markdown cells and the labels in its code cells. A number in them is a
number the engine produced; if the shop changes, this fails until the words change with it.
"""

import ast
import re
import textwrap
import unittest
from pathlib import Path

import shop
from shop import figures
from shop.infer import KEEP

ROOT = Path(__file__).resolve().parents[2]
NOTEBOOK = ROOT / "notebook" / "chapter_01.py"


def markdown_cells() -> list[str]:
    """The text of every `mo.md(...)` cell, in the notebook's order."""
    out = []
    for node in ast.parse(NOTEBOOK.read_text(encoding="utf-8")).body:
        if not isinstance(node, ast.FunctionDef):
            continue
        for stmt in node.body:
            call = stmt.value if isinstance(stmt, ast.Expr) else None
            if (
                isinstance(call, ast.Call)
                and isinstance(call.func, ast.Attribute)
                and call.func.attr == "md"
                and call.args
                and isinstance(call.args[0], ast.Constant)
            ):
                out.append(textwrap.dedent(call.args[0].value).strip())
    return out


def strings() -> list[str]:
    """Every string constant in the notebook: its words, its labels, and its code's strings."""
    tree = ast.parse(NOTEBOOK.read_text(encoding="utf-8"))
    return [n.value for n in ast.walk(tree) if isinstance(n, ast.Constant) and isinstance(n.value, str)]


CELLS = markdown_cells()
TEXT = "\n\n".join(CELLS)


def flat(s: str) -> str:
    return re.sub(r"\s+", " ", s)


class TheWordsMatchTheEngine(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.week = shop.run_week()
        cls.w = cls.week.warehouse
        cls.text = flat(TEXT)

    def says(self, phrase: str) -> None:
        self.assertIn(flat(phrase), self.text)

    def test_the_situation_and_the_week(self):
        self.assertEqual(shop.ARRIVAL, "2026-09-14T09:00:00Z")
        self.says("You start work on Monday 14 September 2026 at 09:00")
        self.assertEqual(shop.DAYS[0], "2026-09-07")
        self.says("a week ago, on Monday 7 September")
        self.assertEqual((shop.DAYS[0], shop.DAYS[-1]), ("2026-09-07", "2026-09-13"))
        self.says("The shop's first week ran from Monday 7 to Sunday 13 September")
        self.assertEqual(shop.NIGHTS[-1], "2026-09-14")
        self.says("The last night ends early on Monday 14 September")

    def test_the_three_systems(self):
        systems = figures.platform_assets(self.week)
        self.assertEqual([s for s, _ in systems], ["Object storage", "Warehouse", "Reporting tool"])
        self.assertEqual([{k for _, k in a} for _, a in systems], [{"file"}, {"table"}, {"dashboard"}])
        self.says(
            "three systems: object storage, which holds files; a warehouse, which holds tables; "
            "and a reporting tool, which holds a dashboard"
        )

    def test_thursday_against_the_days_either_side(self):
        shown = {v["day"]: v["revenue"] for v in self.week.reporting.dashboard()["values"]}
        self.assertEqual((shown["2026-09-09"], shown["2026-09-10"], shown["2026-09-11"]), ("£153.75", "£51.50", "£204.24"))
        self.says("Thursday shows £51.50, against £153.75 on Wednesday and £204.24 on Friday.")

    def test_thursdays_arithmetic(self):
        raw = {}
        for o in self.week.storage.records(shop.FILES["orders"]):
            raw[o["ordered_at"][:10]] = raw.get(o["ordered_at"][:10], 0) + o["price_pence"] * o["quantity"]
        daily = {r["day"]: r["revenue_pence"] for r in self.w.sql("SELECT * FROM daily_sales")}
        self.assertEqual((raw["2026-09-10"], daily["2026-09-10"]), (20550, 5150))
        self.says("Thursday's orders add up to 20550 pence")
        self.says("its Thursday row says 5150; the dashboard shows £51.50")
        self.assertEqual(raw["2026-09-10"] - daily["2026-09-10"], 15400)
        self.says("15400 pence, £154.00, went missing")
        same = [d for d in shop.DAYS if raw[d] == daily[d]]
        self.assertEqual(same, ["2026-09-07", "2026-09-11", "2026-09-13"])
        self.says(
            "On Monday, Friday and Sunday the raw orders add up to the day's row in `daily_sales`. "
            "On Tuesday, Wednesday, Thursday and Saturday they do not."
        )
        self.assertIn('day = "2026-09-10"', NOTEBOOK.read_text(encoding="utf-8"))

    def test_the_record_of_daily_sales(self):
        [t] = self.w.sql("SELECT * FROM information_schema.tables WHERE table_name = 'daily_sales'")
        cols = [c["column_name"] for c in self.w.sql("SELECT column_name FROM information_schema.columns WHERE table_name = 'daily_sales'")]
        self.assertEqual(cols, ["day", "revenue_pence"])
        self.assertEqual((t["row_count"], t["created"][:10], t["last_altered"][:16], t["table_owner"]), (7, "2026-09-01", "2026-09-14T02:30", "etl_service"))
        self.says(
            "two columns, `day` and `revenue_pence`, with their types; 7 rows and a size in bytes; "
            "a created time, 1 September, and a last-altered time, 02:30 on Monday 14 September; "
            "and an owner, `etl_service`"
        )
        self.says("two column names, a row count, a size, two times and an account")

    def test_the_file_formats(self):
        self.assertTrue(shop.FILES["orders"].endswith("orders.jsonl") and shop.FILES["customers"].endswith("customers.jsonl"))
        self.says("`orders.jsonl` and `customers.jsonl` are JSON Lines")
        first = self.week.storage.read_text(shop.FILES["products"]).splitlines()[0]
        self.assertEqual(first, "product_id,name,category,list_price_pence,updated_by")
        self.says("`products.csv` names its columns once, in its first line")
        self.says("its location, its size and when it was last modified")
        self.says("the dashboard's title, who created it and when, when it last refreshed, and the values it shows")

    def test_the_owner_and_the_programs(self):
        owners = {r["table_owner"] for r in self.w.sql("SELECT table_owner FROM information_schema.tables")}
        programs = {e.writer for e in self.week.executions} - {"export"}
        self.assertEqual((owners, len(programs)), ({"etl_service"}, 4))
        self.says("The warehouse answers `etl_service`, the account that all four of the shop's programs log in as.")

    def test_the_reconstruction_and_thursday(self):
        self.assertEqual(len(shop.queries_that_rebuild(self.week)), 1)
        self.assertEqual(len(self.w.sql("SELECT * FROM daily_sales")), 7)
        self.says("It reproduces `daily_sales` exactly, all seven rows.")
        gap = shop.day_gap(self.week, "2026-09-10")
        self.assertEqual((gap["left"], gap["left_pence"]), (3, 15400))
        self.says("three of Thursday's orders arrived with no customer id")
        self.says("worth 15400 pence, £154.00")

    def test_the_three_changes(self):
        self.assertEqual(len(shop.CHANGES), 3)
        self.says("three small changes to the shop")
        self.says("three ordinary changes")
        self.assertEqual(shop.COPY, "s3://shop-scratch/clean_orders_copy.csv")
        self.says("to a CSV file, `clean_orders_copy.csv`, in the bucket `shop-scratch`, every night")
        refunds = shop.run_week(["refunds"])
        sat = {r["day"]: r["revenue_pence"] for r in refunds.warehouse.sql("SELECT * FROM daily_sales")}["2026-09-12"]
        shown = {v["day"]: v["revenue"] for v in refunds.reporting.dashboard()["values"]}["2026-09-12"]
        self.assertEqual((sat, shown), (21549, "£215.49"))
        self.says("becomes 21549 instead of 19149, in pence")
        self.says("£215.49 instead of £191.49")
        [t] = refunds.warehouse.sql("SELECT row_count, last_altered FROM information_schema.tables WHERE table_name = 'daily_sales'")
        self.assertEqual((t["row_count"], t["last_altered"]), (7, "2026-09-14T02:30:21Z"))
        self.says("The table still has 7 rows and the same last-altered time")
        failed = shop.run_week(["failed"])
        tables = {r["table_name"]: r for r in failed.warehouse.sql("SELECT * FROM information_schema.tables")}
        d = failed.reporting.dashboard()
        self.assertEqual(
            (tables["daily_sales"]["row_count"], tables["daily_sales"]["last_altered"][:16], tables["clean_orders"]["last_altered"][:10], d["last_refreshed"][:16], len(d["values"])),
            (6, "2026-09-13T02:30", "2026-09-14", "2026-09-14T03:00", 6),
        )
        self.says(
            "The table has 6 rows, none for Sunday, and was last altered on Sunday at 02:30, a day earlier "
            "than `clean_orders` and the dashboard. The dashboard refreshed at 03:00 on Monday as usual and "
            "shows the 6 values it found."
        )
        self.assertEqual(KEEP, ("all", "completed", "cancelled"))
        self.says("none that keeps every row, completed orders or cancelled orders of one asset")

    def test_the_rule_the_week_never_tests(self):
        orders = self.week.storage.records(shop.FILES["orders"])
        self.assertEqual(sum(1 for o in orders if o["quantity"] <= 0), 0)
        self.says("No order in the week has a quantity of 0 or less")
        self.assertEqual(len(shop.cleaning_rules_that_fit(self.week)), 2)


class TheWordsAboutThePage(unittest.TestCase):
    """The warning at the top states what was measured on the exported page, and the menu offers
    the engine's changes.

    The warning's numbers are measurements, not the engine's: docs/notes/notebook-prototype.md
    records them, and this keeps the page and that record saying the same thing.
    """

    def test_the_warning_states_the_measurements(self):
        [warning] = [s for s in strings() if s.startswith("This page runs Python in your browser")]
        note = flat((ROOT / "docs" / "notes" / "notebook-prototype.md").read_text(encoding="utf-8"))
        for said, measured in [
            ("downloads about 17 MB", "transfers 17.1 MB"),
            ("Python took 10 to 17 seconds to start", "| Python ready | 9.5 to 15 s |"),
            ("Python took 10 to 17 seconds to start", "Python is ready after 15 to 16.5 s"),
            ("used about 1 GB of memory", "| Peak memory of the page's renderer process | 0.97 to 1.16 GB |"),
        ]:
            self.assertIn(said, warning)
            self.assertIn(measured, note)
        self.assertIn("the browser may reload the page, and a reload loses what you changed", warning)

    def test_the_menu_offers_the_engines_changes(self):
        [menu] = [
            n
            for n in ast.walk(ast.parse(NOTEBOOK.read_text(encoding="utf-8")))
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == "dropdown"
        ]
        options = ast.literal_eval(next(k.value for k in menu.keywords if k.arg == "options"))
        self.assertEqual(list(options.values()), [[], ["copy"], ["refunds"], ["failed"]])
        self.assertEqual([c for v in options.values() for c in v], list(shop.CHANGES))
        self.assertEqual(
            list(options),
            [
                "The shop stays as it is",
                "An analyst copies clean_orders every night",
                "From Saturday, the daily_sales program keeps unrefunded orders",
                "The daily_sales program fails on the last night",
            ],
        )


class TheWordsKeepTheRules(unittest.TestCase):
    """The writing standard's checkable parts (AGENTS.md, scripts/prose.mjs, CLAUDE.md)."""

    def learner_text(self) -> list[str]:
        # The markdown, and every string with a space in it: labels, options, placeholders. Code
        # identifiers and SQL keywords are not prose, and SQL has no prohibited phrase.
        return CELLS + [s for s in strings() if " " in s and not s.lstrip().upper().startswith(("SELECT", "\n"))]

    def test_no_prohibited_phrase(self):
        source = (ROOT / "scripts" / "prose.mjs").read_text(encoding="utf-8")
        phrases = re.findall(r'phrase: "([^"]+)"', source) + ["the lab ", "the lab's", "Metadata Lab"]
        self.assertGreater(len(phrases), 10)
        found = [(p, t[:60]) for t in self.learner_text() for p in phrases if p.lower() in t.lower()]
        self.assertEqual(found, [])

    def test_no_em_dash_and_no_placeholder(self):
        self.assertEqual([t[:60] for t in self.learner_text() if "—" in t], [])
        self.assertNotIn("[[", NOTEBOOK.read_text(encoding="utf-8"))

    def test_terms_arrive_where_the_chapter_introduces_them(self):
        first = lambda word: next(i for i, c in enumerate(CELLS) if re.search(rf"\b{word}", c, re.I))
        records = next(i for i, c in enumerate(CELLS) if c.startswith("## Records made at the time"))
        self.assertEqual(first("metadata"), records)
        self.assertTrue(CELLS[first("asset")].startswith("An asset is one thing the platform holds"))


if __name__ == "__main__":
    unittest.main()
