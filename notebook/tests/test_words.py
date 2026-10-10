# Copyright © 2026 Christopher Snow

"""Every sentence of the notebooks that states a fact, pinned against the engine, and the prose rules.

Chapter 1 is two notebooks, one per part. Their words are their markdown cells and the labels in
their code cells. A number in them is a number the engine produced; if the shop changes, this fails
until the words change with it.
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
PARTS = {
    1: ROOT / "notebook" / "chapter_01_part_1.py",
    2: ROOT / "notebook" / "chapter_01_part_2.py",
}
SOURCE = {part: path.read_text(encoding="utf-8") for part, path in PARTS.items()}


def markdown_cells(part: int) -> list[str]:
    """The text of every `mo.md(...)` cell of a part, in the notebook's order."""
    out = []
    for node in ast.parse(SOURCE[part]).body:
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


def strings(part: int) -> list[str]:
    """Every string constant in a part: its words, its labels, and its code's strings."""
    tree = ast.parse(SOURCE[part])
    return [n.value for n in ast.walk(tree) if isinstance(n, ast.Constant) and isinstance(n.value, str)]


CELLS = {part: markdown_cells(part) for part in PARTS}
TEXT = {part: "\n\n".join(cells) for part, cells in CELLS.items()}


def flat(s: str) -> str:
    return re.sub(r"\s+", " ", s)


class TheWordsMatchTheEngine(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.week = shop.run_week()
        cls.w = cls.week.warehouse
        cls.text = {part: flat(text) for part, text in TEXT.items()}

    def says(self, phrase: str, part: int = 2) -> None:
        self.assertIn(flat(phrase), self.text[part])

    def test_the_situation_and_the_week(self):
        self.assertEqual(shop.ARRIVAL, "2026-09-14T09:00:00Z")
        self.says("You start work on Monday 14 September 2026 at 09:00", 1)
        self.assertEqual(shop.DAYS[0], "2026-09-07")
        self.says("a week ago, on Monday 7 September", 1)
        self.assertEqual((shop.DAYS[0], shop.DAYS[-1]), ("2026-09-07", "2026-09-13"))
        self.says("The shop's first week ran from Monday 7 to Sunday 13 September", 1)
        self.assertEqual(shop.NIGHTS[-1], "2026-09-14")
        self.says("The last night ends early on Monday 14 September", 1)

    def test_part_1_opens_with_the_message_and_part_2_starts_on_it(self):
        # The story is introduced first, so the tour of the platform serves the question; part 2
        # holds the investigation (brief AQ).
        first = CELLS[1][1]
        self.assertTrue(first.startswith("You start work on Monday 14 September 2026 at 09:00"))
        self.assertIn("the head of the shop sends you one line: Thursday's revenue looks wrong.", first)
        self.assertIn("you first need to know what the platform holds and what happens on it each night", first)
        self.assertEqual(CELLS[1][-2], "[Part 2](part-2.html) goes back to the head of the shop's line and starts with Thursday's revenue.")
        self.says("The head of the shop has sent you one line", 2)

    def test_the_three_systems(self):
        systems = figures.platform_assets(self.week)
        self.assertEqual([s for s, _ in systems], ["Object storage", "Warehouse", "Reporting tool"])
        self.assertEqual([{k for _, k in a} for _, a in systems], [{"file"}, {"table"}, {"dashboard"}])
        self.says(
            "three systems: object storage, which holds files; a warehouse, which holds tables; "
            "and a reporting tool, which holds a dashboard",
            1,
        )
        self.says("In the cells, `storage`, `warehouse` and `reporting` name the shop's three systems", 1)

    def test_the_shops_files(self):
        products = self.week.storage.records(shop.FILES["products"])
        self.assertEqual((len(products), len({p["category"] for p in products})), (8, 6))
        self.says("holds the shop's catalogue: 8 products in 6 categories", 1)
        self.assertEqual(list(products[0]), ["product_id", "name", "category", "list_price_pence", "updated_by"])
        for name in ("`product_id`", "`list_price_pence`", "`updated_by`"):
            self.says(name, 1)
        customers = self.week.storage.records(shop.FILES["customers"])
        self.assertEqual((len(customers), len({c["country"] for c in customers})), (10, 7))
        self.says("holds the shop's 10 customers, in 7 countries", 1)
        self.assertEqual(list(customers[0]), ["customer_id", "name", "email", "country", "signed_up"])
        self.assertTrue(all(len(c) == 5 for c in customers))
        self.says("A customer's record has five fields", 1)
        self.assertTrue(all(len(c["country"]) == 2 for c in customers))
        for name in ("`customer_id`", "`signed_up`"):
            self.says(name, 1)
        orders = self.week.storage.records(shop.FILES["orders"])
        self.assertEqual(list(orders[0]), ["order_id", "customer_id", "product_id", "quantity", "price_pence", "status", "ordered_at"])
        self.assertTrue(all(len(o) == 7 for o in orders))
        self.says("An order's record has seven fields", 1)
        for name in ("`order_id`", "`customer_id`", "`product_id`", "`quantity`", "`price_pence`", "`status`", "`ordered_at`"):
            self.says(name, 1)
        self.assertEqual({o["status"] for o in orders}, {"completed", "cancelled"})
        self.says("In this week's file, `status` is `completed` or `cancelled`.", 1)
        self.assertTrue(all(o["ordered_at"].endswith("Z") for o in orders))
        self.assertTrue(all(o["price_pence"] == {p[0]: p[3] for p in shop.data.PRODUCTS}[o["product_id"]] for o in orders))
        # The file on Monday holds every order of the week: each night's export writes them all again.
        self.assertEqual({o["order_id"] for o in orders}, {row[0] for row in shop.data.ORDERS})
        self.says("Each night, the file is written again, with every order taken since the online store opened.", 1)
        self.assertEqual(sorted({o["ordered_at"][:10] for o in orders}), list(shop.DAYS))
        self.assertIn('day = "2026-09-07"', SOURCE[1])
        self.says("the day is set to Monday, `2026-09-07`", 1)
        self.says("any day from `2026-09-07` to `2026-09-13`", 1)

    def test_the_warehouse_and_the_dashboard(self):
        tables = [r["table_name"] for r in self.w.sql("SELECT table_name FROM information_schema.tables ORDER BY rowid")]
        self.assertEqual(tables, ["clean_customers", "clean_orders", "daily_sales"])
        self.says("The warehouse holds three tables: `clean_customers`, `clean_orders` and `daily_sales`.", 1)
        days = [r["day"] for r in self.w.sql("SELECT day FROM daily_sales ORDER BY day")]
        self.assertEqual(days, list(shop.DAYS))
        self.says("`daily_sales` has one row per day: the day and that day's revenue in pence (`revenue_pence`).", 1)
        self.assertIn('warehouse.sql("SELECT * FROM clean_orders LIMIT 7")', SOURCE[1])
        self.says("the first 7 rows of `clean_orders`", 1)
        d = self.week.reporting.dashboard()
        self.assertEqual((d["name"], d["title"], [v["day"] for v in d["values"]]), ("sales_dashboard", "Sales, last 7 days", list(shop.DAYS)))
        self.says('one dashboard, `sales_dashboard`, titled "Sales, last 7 days"', 1)
        self.says("each day's revenue in pounds for 7 to 13 September", 1)

    def test_the_parts_link_to_each_other_where_the_export_puts_them(self):
        export = (ROOT / "notebook" / "export.sh").read_text(encoding="utf-8")
        self.assertIn('chapter_01_part_1.py -o "$out/index.html"', export)
        self.assertIn('chapter_01_part_2.py -o "$out/part-2.html"', export)
        self.assertIn("](part-2.html)", TEXT[1])
        self.assertIn("](./)", TEXT[2])

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
        self.assertIn('day = "2026-09-10"', SOURCE[2])

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
        self.says("`orders.jsonl` and `customers.jsonl` are JSON Lines", 1)
        first = self.week.storage.read_text(shop.FILES["products"]).splitlines()[0]
        self.assertEqual(first, "product_id,name,category,list_price_pence,updated_by")
        self.says("`products.csv` names its columns once, in its first line", 1)
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
        note = flat((ROOT / "docs" / "notes" / "notebook-prototype.md").read_text(encoding="utf-8"))
        gzip = "| Size if the host compresses text and WebAssembly (gzip, level 6) | 17.0 MB | 17.0 MB | |"
        ready = "| Python ready | 8.9 to 10.3 s | 8.9 to 9.3 s | 7.7 to 8.7 s |"
        live = "Python is ready after 15 to 16.5 s"  # the published single notebook, the same runtime
        memory = "| Peak memory of the page's renderer process | 0.79 to 0.82 GB | 1.01 to 1.09 GB |"
        stored = "| Size, as stored | 31.8 MB | 31.9 MB | 0.15 MB |"
        expected = {
            1: [
                ("downloads about 17 MB", gzip),
                ("downloads about 17 MB", "transfers 17.1 MB"),
                ("Python took 9 to 17 seconds to start", ready),
                ("Python took 9 to 17 seconds to start", live),
                ("the page used about 0.8 GB of memory", memory),
            ],
            2: [
                ("downloads about 17 MB", gzip),
                ("the page downloaded less than 1 MB when opened from part 1's link", stored),
                ("Python took 8 to 17 seconds to start", ready),
                ("Python took 8 to 17 seconds to start", live),
                ("the page used about 1 GB of memory", memory),
            ],
        }
        for part, pairs in expected.items():
            [warning] = [s for s in strings(part) if s.startswith("This page runs Python in your browser")]
            for said, measured in pairs:
                self.assertIn(said, warning, part)
                self.assertIn(flat(measured), note, part)
            self.assertIn("the browser may reload the page, and a reload loses what you changed", warning)

    def test_the_menu_offers_the_engines_changes(self):
        [menu] = [
            n
            for n in ast.walk(ast.parse(SOURCE[2]))
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
        return [
            t
            for part in PARTS
            for t in CELLS[part]
            + [s for s in strings(part) if " " in s and not s.lstrip().upper().startswith(("SELECT", "\n"))]
        ]

    def test_no_prohibited_phrase(self):
        source = (ROOT / "scripts" / "prose.mjs").read_text(encoding="utf-8")
        phrases = re.findall(r'phrase: "([^"]+)"', source) + ["the lab ", "the lab's", "Metadata Lab"]
        self.assertGreater(len(phrases), 10)
        found = [(p, t[:60]) for t in self.learner_text() for p in phrases if p.lower() in t.lower()]
        self.assertEqual(found, [])

    def test_no_em_dash_and_no_placeholder(self):
        self.assertEqual([t[:60] for t in self.learner_text() if "—" in t], [])
        for source in SOURCE.values():
            self.assertNotIn("[[", source)

    def test_terms_arrive_where_the_chapter_introduces_them(self):
        # Part 1 introduces "asset", part 2 "metadata", at its "Records made at the time".
        chapter = CELLS[1] + CELLS[2]
        first = lambda word: next(i for i, c in enumerate(chapter) if re.search(rf"\b{word}", c, re.I))
        records = next(i for i, c in enumerate(chapter) if c.startswith("## Records made at the time"))
        self.assertGreaterEqual(records, len(CELLS[1]))
        self.assertEqual(first("metadata"), records)
        self.assertTrue(chapter[first("asset")].startswith("An asset is one thing the platform holds"))
        self.assertLess(first("asset"), len(CELLS[1]))

    def test_no_term_of_a_later_chapter(self):
        # The course's term gate (content/lessons/plan.ts), with the course's one exemption for
        # Chapter 1: "run" as the verb (run a cell); the noun arrives in Chapter 6.
        plan = (ROOT / "content" / "lessons" / "plan.ts").read_text(encoding="utf-8")
        terms = {
            term: int(number)
            for number, introduces in re.findall(r'C\((\d+), \d+, "[^"]+"(?:, \[([^\]]*)\])?\)', plan)
            for term in re.findall(r'"([^"]+)"', introduces or "")
        }
        self.assertGreater(len(terms), 40)
        found = [
            (term, t[:60])
            for term, home in terms.items()
            if home > 1 and term != "run"
            for t in self.learner_text()
            if re.search(rf"\b{re.escape(term)}", t, re.I)
        ]
        self.assertEqual(found, [])


if __name__ == "__main__":
    unittest.main()
