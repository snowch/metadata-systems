# Copyright © 2026 Christopher Snow

"""Every sentence of the notebooks that states a fact, pinned against the engine, and the prose rules.

Chapters 1 to 28 are a notebook each. Their words are their markdown cells and the labels in their
code cells. A number in them is a number the engine produced; if the shop changes, this fails
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
CHAPTERS = {
    1: ROOT / "notebook" / "chapter_01.py",
    2: ROOT / "notebook" / "chapter_02.py",
    3: ROOT / "notebook" / "chapter_03.py",
    4: ROOT / "notebook" / "chapter_04.py",
    5: ROOT / "notebook" / "chapter_05.py",
    6: ROOT / "notebook" / "chapter_06.py",
    7: ROOT / "notebook" / "chapter_07.py",
    8: ROOT / "notebook" / "chapter_08.py",
    9: ROOT / "notebook" / "chapter_09.py",
    10: ROOT / "notebook" / "chapter_10.py",
    11: ROOT / "notebook" / "chapter_11.py",
    12: ROOT / "notebook" / "chapter_12.py",
    13: ROOT / "notebook" / "chapter_13.py",
    14: ROOT / "notebook" / "chapter_14.py",
    15: ROOT / "notebook" / "chapter_15.py",
    16: ROOT / "notebook" / "chapter_16.py",
    17: ROOT / "notebook" / "chapter_17.py",
    18: ROOT / "notebook" / "chapter_18.py",
    19: ROOT / "notebook" / "chapter_19.py",
    20: ROOT / "notebook" / "chapter_20.py",
    21: ROOT / "notebook" / "chapter_21.py",
    22: ROOT / "notebook" / "chapter_22.py",
    23: ROOT / "notebook" / "chapter_23.py",
    24: ROOT / "notebook" / "chapter_24.py",
    25: ROOT / "notebook" / "chapter_25.py",
    26: ROOT / "notebook" / "chapter_26.py",
    27: ROOT / "notebook" / "chapter_27.py",
    28: ROOT / "notebook" / "chapter_28.py",
}
SOURCE = {chapter: path.read_text(encoding="utf-8") for chapter, path in CHAPTERS.items()}


def markdown_cells(chapter: int) -> list[str]:
    """The text of every `mo.md(...)` cell of a chapter, in the notebook's order, with the text of
    each requirement's box (a callout of the kind "neutral"), which reads as part of the chapter."""
    out = []
    for node in ast.parse(SOURCE[chapter]).body:
        if not isinstance(node, ast.FunctionDef):
            continue
        for stmt in node.body:
            call = stmt.value if isinstance(stmt, ast.Expr) else None
            if (
                isinstance(call, ast.Call)
                and isinstance(call.func, ast.Attribute)
                and call.func.attr == "callout"
                and any(k.arg == "kind" and getattr(k.value, "value", None) == "neutral" for k in call.keywords)
            ):
                call = call.args[0]
            if (
                isinstance(call, ast.Call)
                and isinstance(call.func, ast.Attribute)
                and call.func.attr == "md"
                and call.args
                and isinstance(call.args[0], ast.Constant)
            ):
                out.append(textwrap.dedent(call.args[0].value).strip())
    return out


def strings(chapter: int) -> list[str]:
    """Every string constant in a chapter: its words, its labels, and its code's strings."""
    tree = ast.parse(SOURCE[chapter])
    return [n.value for n in ast.walk(tree) if isinstance(n, ast.Constant) and isinstance(n.value, str)]


CELLS = {chapter: markdown_cells(chapter) for chapter in CHAPTERS}
TEXT = {chapter: "\n\n".join(cells) for chapter, cells in CELLS.items()}


def flat(s: str) -> str:
    return re.sub(r"\s+", " ", s)


class TheWordsMatchTheEngine(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.week = shop.run_week()
        cls.w = cls.week.warehouse
        cls.text = {chapter: flat(text) for chapter, text in TEXT.items()}

    def says(self, phrase: str, chapter: int = 2) -> None:
        self.assertIn(flat(phrase), self.text[chapter])

    def test_the_situation_and_the_week(self):
        self.assertEqual(shop.ARRIVAL, "2026-09-14T09:00:00Z")
        self.says("You start work on Monday 14 September 2026 at 09:00", 1)
        self.assertEqual(shop.DAYS[0], "2026-09-07")
        self.says("a week ago, on Monday 7 September", 1)
        self.assertEqual((shop.DAYS[0], shop.DAYS[-1]), ("2026-09-07", "2026-09-13"))
        self.says("The shop's first week ran from Monday 7 to Sunday 13 September", 1)
        self.assertEqual(shop.NIGHTS[-1], "2026-09-14")
        self.says("The last night ends early on Monday 14 September", 1)

    def test_chapter_1_opens_with_the_message_and_chapter_2_starts_on_it(self):
        # The story is introduced first, so the tour of the platform serves the question; Chapter 2
        # holds the investigation (brief AQ).
        first = CELLS[1][1]
        self.assertTrue(first.startswith("You start work on Monday 14 September 2026 at 09:00"))
        self.assertIn("the head of the shop sends you a message: \"Thursday's revenue looks wrong.\"", first)
        self.assertIn("you first need to know what the platform holds and what happens on it each night", first)
        self.assertEqual(CELLS[1][-2], "[Chapter 2](chapter_02.ipynb) goes back to the head of the shop's message and starts with Thursday's revenue.")
        self.says("The head of the shop has sent you a message", 2)
        self.says("You cannot see the export, the jobs, when they are due to run, or any note anybody kept.", 1)

    def test_the_three_systems(self):
        systems = figures.platform_assets(self.week)
        self.assertEqual([s for s, _ in systems], ["Object storage", "Warehouse", "Reporting tool"])
        self.assertEqual([{k for _, k in a} for _, a in systems], [{"file"}, {"table"}, {"dashboard"}])
        self.says(
            "three systems: object storage, which holds files; a warehouse, which holds tables; "
            "and a reporting tool, which holds a dashboard",
            1,
        )
        self.says(
            "three Python variables stand for the shop's three systems: `storage` is object storage, "
            "`warehouse` is the warehouse, and `reporting` is the reporting tool",
            1,
        )
        # And the setup makes them so.
        self.assertIn("storage, warehouse, reporting = week.storage, week.warehouse, week.reporting", SOURCE[1])

    def test_the_shops_files(self):
        products = self.week.storage.records(shop.FILES["products"])
        self.assertEqual((len(products), len({p["category"] for p in products})), (8, 6))
        self.says("holds the shop's product catalogue: 8 products in 6 categories", 1)
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

    def test_the_chapters_link_to_each_other_by_their_notebooks_names(self):
        build = (ROOT / "notebook" / "jupyterlite" / "build_ipynb.py").read_text(encoding="utf-8")
        names = re.findall(r'"(chapter_\d\d\.ipynb)"', build)
        self.assertEqual(names, [f"chapter_{n:02d}.ipynb" for n in CHAPTERS])
        for chapter in CHAPTERS:
            if chapter > 1:
                self.assertIn(f"](chapter_{chapter - 1:02d}.ipynb)", TEXT[chapter])
            if chapter < len(CHAPTERS):
                self.assertIn(f"](chapter_{chapter + 1:02d}.ipynb)", TEXT[chapter])

    def test_the_closing_names_the_next_chapter(self):
        # Chapter 2 ends by naming the chapter after it, which the plan numbers 3; and so on.
        self.says("## Before Chapter 3", 2)
        self.says("Chapter 3 starts making them", 2)
        self.says("## Before Chapter 4", 3)
        self.says("Neither your record nor the reporting tool says that the two names refer to one person.", 3)
        self.says("## Before Chapter 5", 4)
        self.says("Chapter 5 follows them from one entity to the next.", 4)
        self.says("## Before Chapter 6", 5)
        self.says("In Chapter 6 you read the jobs' code", 5)
        self.says("## Before Chapter 7", 6)
        self.says("Chapter 7 records each time a job does its work", 6)
        self.says("## Before Chapter 8", 7)
        self.says("Chapter 8 writes the same runs in the form an open standard sets", 7)
        self.says("## Before Chapter 9", 8)
        self.says("Chapter 9 builds that consumer, one stage at a time", 8)
        self.says("## Before Chapter 10", 9)
        self.says("## Before Chapter 11", 10)
        self.says("## Before Chapter 12", 11)
        self.says("## Before Chapter 13", 12)
        self.says("## Before Chapter 14", 13)
        self.says("## Before Chapter 15", 14)
        self.says("## Before Chapter 16", 15)
        self.says("## Before Chapter 17", 16)
        self.says("## Before Chapter 18", 17)
        self.says("## Before Chapter 19", 18)
        self.says("## Before Chapter 20", 19)
        self.says("## Before Chapter 21", 20)
        self.says("## Before Chapter 22", 21)
        self.says("## Before Chapter 23", 22)
        self.says("## Before Chapter 24", 23)
        self.says("## Before Chapter 25", 24)
        self.says("## Before Chapter 26", 25)
        self.says("## Before Chapter 27", 26)
        self.says("## Before Chapter 28", 27)
        self.says("## Before Chapter 29", 28)
        self.says("Chapter 10 reads the jobs' SQL", 9)

    def test_each_chapter_has_its_own_title_in_its_tab(self):
        for chapter, source in SOURCE.items():
            title = re.search(r"^# Chapter \d+: (.*)$", TEXT[chapter], re.M).group(1)
            self.assertIn(f'app_title="{title}"', source, chapter)

    def test_each_chapter_opens_and_ends_with_the_way_back_to_the_course(self):
        # Relative links in a notebook open as files of the site, so the course's address is whole.
        nav = {
            1: "[Back to contents](https://snowch.github.io/metadata-systems/) · [Next: Chapter 2](chapter_02.ipynb)",
            2: "[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 1](chapter_01.ipynb) · [Next: Chapter 3](chapter_03.ipynb)",
            3: "[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 2](chapter_02.ipynb) · [Next: Chapter 4](chapter_04.ipynb)",
            4: "[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 3](chapter_03.ipynb) · [Next: Chapter 5](chapter_05.ipynb)",
            5: "[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 4](chapter_04.ipynb) · [Next: Chapter 6](chapter_06.ipynb)",
            6: "[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 5](chapter_05.ipynb) · [Next: Chapter 7](chapter_07.ipynb)",
            7: "[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 6](chapter_06.ipynb) · [Next: Chapter 8](chapter_08.ipynb)",
            8: "[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 7](chapter_07.ipynb) · [Next: Chapter 9](chapter_09.ipynb)",
            9: "[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 8](chapter_08.ipynb) · [Next: Chapter 10](chapter_10.ipynb)",
            10: "[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 9](chapter_09.ipynb) · [Next: Chapter 11](chapter_11.ipynb)",
            11: "[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 10](chapter_10.ipynb) · [Next: Chapter 12](chapter_12.ipynb)",
            12: "[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 11](chapter_11.ipynb) · [Next: Chapter 13](chapter_13.ipynb)",
            13: "[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 12](chapter_12.ipynb) · [Next: Chapter 14](chapter_14.ipynb)",
            14: "[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 13](chapter_13.ipynb) · [Next: Chapter 15](chapter_15.ipynb)",
            15: "[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 14](chapter_14.ipynb) · [Next: Chapter 16](chapter_16.ipynb)",
            16: "[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 15](chapter_15.ipynb) · [Next: Chapter 17](chapter_17.ipynb)",
            17: "[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 16](chapter_16.ipynb) · [Next: Chapter 18](chapter_18.ipynb)",
            18: "[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 17](chapter_17.ipynb) · [Next: Chapter 19](chapter_19.ipynb)",
            19: "[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 18](chapter_18.ipynb) · [Next: Chapter 20](chapter_20.ipynb)",
            20: "[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 19](chapter_19.ipynb) · [Next: Chapter 21](chapter_21.ipynb)",
            21: "[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 20](chapter_20.ipynb) · [Next: Chapter 22](chapter_22.ipynb)",
            22: "[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 21](chapter_21.ipynb) · [Next: Chapter 23](chapter_23.ipynb)",
            23: "[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 22](chapter_22.ipynb) · [Next: Chapter 24](chapter_24.ipynb)",
            24: "[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 23](chapter_23.ipynb) · [Next: Chapter 25](chapter_25.ipynb)",
            25: "[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 24](chapter_24.ipynb) · [Next: Chapter 26](chapter_26.ipynb)",
            26: "[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 25](chapter_25.ipynb) · [Next: Chapter 27](chapter_27.ipynb)",
            27: "[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 26](chapter_26.ipynb) · [Next: Chapter 28](chapter_28.ipynb)",
            28: "[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 27](chapter_27.ipynb)",
        }
        for chapter, line in nav.items():
            self.assertTrue(CELLS[chapter][0].startswith(line + "\n"), chapter)
            self.assertEqual(SOURCE[chapter].count(line), 2, chapter)

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
        self.says("Thursday's orders in `orders.jsonl` add up to 20550 pence")
        self.says("`daily_sales` says 5150 for Thursday, and the dashboard shows £51.50")
        self.assertEqual(raw["2026-09-10"] - daily["2026-09-10"], 15400)
        self.says("The two totals differ by 15400 pence, £154.00.")
        # The orders clean_orders lacks on Thursday, which the new cell lists: all of them have no
        # customer id, and together they are the whole gap.
        kept = {r["order_id"] for r in self.w.sql("SELECT order_id FROM clean_orders")}
        thursday = [o for o in self.week.storage.records(shop.FILES["orders"]) if o["ordered_at"].startswith("2026-09-10")]
        lacking = [o for o in thursday if o["order_id"] not in kept]
        self.assertEqual([o["order_id"] for o in lacking], [7021, 7023, 7025])
        self.assertTrue(all(o["customer_id"] is None for o in lacking))
        self.assertEqual(sum(o["price_pence"] * o["quantity"] for o in lacking), 15400)
        self.says("Orders 7021, 7023 and 7025 have no customer id. Together they are worth 15400 pence, the whole of Thursday's gap.")
        self.assertIn("AND order_id NOT IN (SELECT order_id FROM clean_orders)", SOURCE[2])
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
            "The cells showed the two columns of `daily_sales`, `day` and `revenue_pence`, with their types. "
            "They also showed 7 rows, a size in bytes, a created time of 1 September, and a last-altered time "
            "of 02:30 on Monday 14 September. The warehouse lists `etl_service` as the owner."
        )
        # The record is shown before it is described: the cells come first.
        holds = SOURCE[2][SOURCE[2].index("## What the platform holds"):]
        self.assertLess(holds.index("FROM information_schema.columns"), holds.index("The cells showed"))
        self.says("two column names, a row count, a size, two times and an account")

    def test_the_file_formats(self):
        self.assertTrue(shop.FILES["orders"].endswith("orders.jsonl") and shop.FILES["customers"].endswith("customers.jsonl"))
        self.says("Each record names its fields. A date such as `signed_up` is just a string: the file has no date type.", 1)
        self.assertIsInstance(self.week.storage.records(shop.FILES["customers"])[0]["signed_up"], str)
        first = self.week.storage.read_text(shop.FILES["products"]).splitlines()[0]
        self.assertEqual(first, "product_id,name,category,list_price_pence,updated_by")
        self.says("`products.csv` stores every value as text, and it has no types.", 1)
        keys = [r["key"] for r in self.week.storage.ls("s3://shop-raw/")]
        self.assertIn("s3://shop-raw/orders.jsonl", keys)
        self.assertEqual(set(self.week.storage.ls("s3://shop-raw/")[0]), {"key", "size_bytes", "last_modified"})
        self.says("Object storage records three things about a file: its key, its size in bytes and when it was last modified.")
        self.says("A key is the file's full name, such as `s3://shop-raw/orders.jsonl`, where `shop-raw` is the bucket")
        self.says("the dashboard's title, who created it and when, when it last refreshed, and the values it shows")

    def test_the_owner_and_the_programs(self):
        owners = {r["table_owner"] for r in self.w.sql("SELECT table_owner FROM information_schema.tables")}
        programs = {e.writer for e in self.week.executions} - {"export"}
        self.assertEqual((owners, len(programs)), ({"etl_service"}, 4))
        tables = self.w.sql("SELECT table_name FROM information_schema.tables")
        self.assertEqual(len(tables), 3)
        # The rule is one data teams often adopt (docs/sources.md), which the data engineer adopts so
        # that "Who should I ask?" has an answer; the warehouse meets it as written before anyone acts.
        self.says('Data teams often adopt a rule so that every table has someone to ask about it: "Every table must have an owner."')
        self.says("You adopt the rule for the shop's platform.")
        self.says("The warehouse already records an owner for every table, so the rule is met, and you did nothing to make it so.")
        self.says("so you still do not know whom to ask.")
        self.assertNotIn("head of the shop's requirement is: \"Every table", self.text[2])
        self.says("The warehouse records `etl_service` as the owner of all three tables, in the column `table_owner` of `information_schema.tables`.")
        # The readings of the requirement, each against what the warehouse records: the account it
        # names answers only which account controls the table. Its owner is one account for every
        # table, which four programs share, so it names no person, team or job.
        self.says("| which account controls it in the warehouse | an account | yes |")
        self.says("| which job writes it | a program | no: it names an account, not a program |")
        self.assertEqual(flat(TEXT[2]).count("| yes |"), 1)
        # "field" is kept for a file's record (Chapter 1); what a system keeps is not called one here.
        self.says("## What each system records about assets, and why")
        self.assertNotIn("These fields", self.text[2])

    def test_the_reconstruction_and_thursday(self):
        self.assertEqual(len(shop.queries_that_rebuild(self.week)), 1)
        self.assertEqual(len(self.w.sql("SELECT * FROM daily_sales")), 7)
        self.says("It prints `True`: the query gives all 7 rows of `daily_sales`, Thursday's 5150 pence included.")
        gap = shop.day_gap(self.week, "2026-09-10")
        self.assertEqual((gap["left"], gap["left_pence"]), (3, 15400))
        # The reader writes a guess before the query runs; the page says why Thursday matches.
        self.says("Thursday matches because `clean_orders` does not hold Thursday's three orders with no customer id")
        self.says("`clean_orders` also holds 2 cancelled orders.")

    def test_the_three_changes(self):
        # Chapter 2's three; Chapter 3 adds a fourth, `column`.
        self.assertEqual(shop.CHANGES[:3], ("copy", "refunds", "failed"))
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
        self.says(
            "\"No simple query over the week's assets reproduces it\" means none of the simple queries "
            "the menu's last cell tries."
        )
        # What the menu's last cell lists for each change, and the columns the text names.
        counts = [len(shop.queries_that_rebuild(shop.run_week(c), "daily_sales", fit="covers")) for c in ([], ["copy"], ["refunds"], ["failed"])]
        self.assertEqual(counts, [1, 2, 0, 1])
        self.assertEqual(set(shop.queries_that_rebuild(self.week)[0]), {"source", "keep", "measure", "per", "sql"})
        self.says("`source` names the asset it reads; `keep` says which orders it keeps (all, completed or cancelled)")
        self.says("Each record is normal on its own. The gap shows only when you compare the last-altered times.")

    def test_what_the_rows_can_answer(self):
        # Under the four questions: the rows answer only whether Thursday's total differs.
        self.says("The rows show whether Thursday's total differs from Thursday's orders.")
        self.says("The rows a table holds today record none of these.")

    def test_the_rule_the_week_never_tests(self):
        orders = self.week.storage.records(shop.FILES["orders"])
        self.assertEqual(sum(1 for o in orders if o["quantity"] <= 0), 0)
        self.says("No order in the week has a quantity of 0 or less")
        self.assertEqual(len(shop.cleaning_rules_that_fit(self.week)), 2)


def literal(chapter: int, call: str) -> str:
    """The text a chapter's code passes to `shop.<call>(...)`, or assigns to the name `call`."""
    for node in ast.walk(ast.parse(SOURCE[chapter])):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == call and node.args and isinstance(node.args[0], ast.Constant):
            return node.args[0].value
        if isinstance(node, ast.Assign) and [getattr(t, "id", None) for t in node.targets] == [call] and isinstance(node.value, ast.Constant):
            return node.value.value
    raise KeyError(call)


# The record of `daily_sales` as the reader fills it in from the head of the shop's and Jo Marsh's
# messages: the chapter states what the cells show once it is written.
FILLED = {
    "daily_sales means": "the value of every completed order placed that day, by its UTC date",
    "daily_sales responsible": "Jo Marsh",
    "daily_sales day means": "the UTC date the orders were placed",
    "daily_sales revenue_pence means": "the value of the day's completed orders",
    "daily_sales revenue_pence unit": "pence",
}


class TheWordsOfChapter3(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.week = shop.run_week()
        cls.w = cls.week.warehouse
        cls.text = flat(TEXT[3])
        blank = literal(3, "records")
        lines = [line for line in blank.splitlines() if line.strip()]
        assert [line.split(":")[0] for line in lines] == list(FILLED), lines
        assert all(line.endswith(": ........") for line in lines), lines
        cls.blank = shop.records(blank)
        cls.mine = shop.records("\n".join(f"{k}: {v}" for k, v in FILLED.items()))
        cls.jos = re.search(r'by_jos_meaning = """(.*?)"""', SOURCE[3], re.S).group(1)

    def says(self, phrase: str) -> None:
        self.assertIn(flat(phrase), self.text)

    def test_the_opening(self):
        gap = shop.day_gap(self.week, "2026-09-10")
        self.assertEqual((gap["left_ids"], gap["left_pence"]), ([7021, 7023, 7025], 15400))
        self.says("Thursday's three orders with no customer id (7021, 7023 and 7025, worth 15400 pence together)")
        self.assertEqual(self.week.reporting.dashboard()["created_by"], "j.marsh")
        self.says("For `daily_sales` and the dashboard, ask Jo Marsh in finance, who built the dashboard and decides what counts as revenue.")
        self.says("The value of every completed order placed that day, taking the day from the order's time in UTC, in pence.")

    def test_the_record_and_its_check(self):
        self.assertEqual(len(self.blank.check(self.w, "daily_sales")), 2)
        self.assertEqual(self.mine.check(self.w, "daily_sales"), [])
        self.says("With every line written, it finds no problems.")
        self.assertEqual(self.mine.sql("SELECT value FROM records WHERE asset = 'daily_sales' AND field = 'responsible'"), [{"value": "Jo Marsh"}])
        self.says("The record answers the fourth question with Jo Marsh")
        # The example line is not one of the five the reader fills in.
        self.says("`clean_orders price_pence unit: pence`")
        self.assertNotIn("clean_orders price_pence", literal(3, "records"))
        self.assertEqual([r["line"] for r in self.blank], [1, 2, 3, 4, 5])

    def test_jos_meaning_against_the_table(self):
        files = {"raw_orders": shop.FILES["orders"]}
        rows = self.w.sql(self.jos, files=files)
        differ = [(r["day"], r["revenue_pence"], r["meant_pence"]) for r in rows if r["compared"] == "different"]
        self.assertEqual(differ, [("2026-09-10", 5150, 20550)])
        self.says("Thursday is the only day that differs: `daily_sales` shows 5150 pence, and Jo Marsh's meaning gives 20550.")
        every_line = self.jos.replace("(SELECT DISTINCT * FROM raw_orders)", "raw_orders")
        self.assertEqual([r["day"] for r in self.w.sql(every_line, files=files) if r["compared"] == "different"], ["2026-09-09", "2026-09-10"])
        self.assertEqual(shop.data.DUPLICATED, 7015)
        self.says("The file holds order 7015 on two lines.")
        self.says("A query that counted every line would find Wednesday different too.")
        cancelled = {o["ordered_at"][:10] for o in self.week.storage.records(shop.FILES["orders"]) if o["status"] == "cancelled"}
        self.assertEqual(cancelled, {"2026-09-08", "2026-09-12"})
        self.says("Tuesday, Wednesday and Saturday agree because the query leaves out cancelled orders and counts the order the export wrote twice once")
        rebuilt = self.jos.replace("(SELECT DISTINCT * FROM raw_orders)", "clean_orders")
        self.assertEqual({r["compared"] for r in self.w.sql(rebuilt)}, {"same"})
        self.assertIn("FROM clean_orders", SOURCE[3])
        self.says("Every day is the same, Thursday included.")
        found = self.mine.sql("SELECT * FROM records WHERE asset LIKE '%products.csv%' OR asset LIKE '%orders.jsonl%' OR value LIKE '%products.csv%' OR value LIKE '%orders.jsonl%'")
        self.assertEqual(found, [])
        self.says("It finds none.")

    def test_the_schema_and_the_person(self):
        counts = {}
        for r in self.w.sql("SELECT table_name FROM information_schema.columns"):
            counts[r["table_name"]] = counts.get(r["table_name"], 0) + 1
        self.assertEqual(counts, {"clean_customers": 5, "clean_orders": 7, "daily_sales": 2})
        self.says("14 columns in all, 5 in `clean_customers`, 7 in `clean_orders` and 2 in `daily_sales`")
        edits = self.week.storage.sql(shop.FILES["products"], "SELECT updated_by, COUNT(*) AS products FROM file GROUP BY updated_by")
        self.assertEqual([(r["updated_by"], r["products"]) for r in edits], [("k.adeyemi", 3), ("r.novak", 2), ("s.lund", 3)])
        self.says("Three people last edited the 8 products.")
        self.says("whose values include `s.lund`")
        first = self.week.storage.read_text(shop.FILES["products"]).splitlines()[0]
        self.says(f"The file's first line, `{first}`, names the file's columns.")

    def test_the_requirement(self):
        problems = self.mine.check(self.w)
        self.assertEqual(len(problems), 12)
        self.assertEqual({p["asset"] for p in problems}, {"clean_customers", "clean_orders"})
        self.says("so the check lists the 12 columns of `clean_customers` and `clean_orders`")
        by_name = shop.records("\n".join(
            f"{c['table_name']} {c['column_name']} means: {c['column_name'].replace('_', ' ')}"
            for c in self.w.sql("SELECT table_name, column_name FROM information_schema.columns")
        ))
        self.assertIn("by_name = shop.records(", SOURCE[3])
        self.assertEqual(by_name.check(self.w), [])
        self.says("With a description for each of the 14 columns, the check finds no problems")
        self.assertEqual([r["value"] for r in by_name.about("daily_sales")], ["day", "revenue pence"])

    def test_the_record_nobody_updates(self):
        [p] = self.mine.check(shop.run_week(["column"]).warehouse, "daily_sales")
        self.assertEqual(p["column"], "order_count")
        self.says("For change 1, the check reports `order_count`, which has no description in your record.")
        refunds = shop.run_week(["refunds"])
        self.assertEqual(self.mine.check(refunds.warehouse, "daily_sales"), [])
        self.says("For change 2, the check reports nothing: the edit changed no column.")
        rows = refunds.warehouse.sql(self.jos, files={"raw_orders": shop.FILES["orders"]})
        differ = [(r["day"], r["revenue_pence"], r["meant_pence"]) for r in rows if r["compared"] == "different"]
        self.assertEqual(differ, [("2026-09-10", 5150, 20550), ("2026-09-12", 21549, 19149)])
        self.says("Saturday now differs too: 21549 pence in `daily_sales`, against 19149 by Jo's meaning. Thursday still differs.")

    def test_postgresql_comment(self):
        # docs/sources.md, "A description inside the database (Chapter 3's closing note)".
        self.says("In PostgreSQL, the command `COMMENT ON` stores one comment for a table or a column, and a new one replaces the old.")


class TheWordsOfChapter4(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.week = shop.run_week()
        cls.text = flat(TEXT[4])
        cls.together = shop.records(literal(4, "yours") + literal(4, "jos"))
        cls.records = shop.typed_records(literal(4, "typed_records"))
        cls.model = shop.model(literal(4, "model"))

    def says(self, phrase: str) -> None:
        self.assertIn(flat(phrase), self.text)

    def merged(self) -> "shop.records.TypedRecords":
        return shop.typed_records(
            self.records.text.replace("responsible: Jo Marsh", "responsible: j.marsh").replace("responsible: Sam Lund", "responsible: s.lund")
        )

    def test_the_list_of_owners(self):
        owners = self.together.sql("SELECT asset, value AS responsible FROM records WHERE field = 'responsible' ORDER BY asset")
        self.assertEqual(len(owners), 6)
        self.assertEqual([o["responsible"] for o in owners if o["asset"] == "daily_sales"], ["Jo Marsh", "j.marsh"])
        [count] = self.together.sql("SELECT COUNT(DISTINCT value) AS owners FROM records WHERE field = 'responsible'")
        self.assertEqual(count["owners"], 4)
        self.assertEqual({o["responsible"] for o in owners}, {"the data engineer", "Jo Marsh", "j.marsh", "Sam Lund"})
        self.says("The cell counts 4 different values of `responsible`: the data engineer, Jo Marsh, `j.marsh` and Sam Lund.")
        self.assertEqual(self.week.reporting.dashboard()["created_by"], "j.marsh")
        self.says("the reporting tool records `j.marsh` as the dashboard's creator")

    def test_the_two_notations_hold_the_same_records(self):
        # Chapter 4's records are Chapter 3's notation's, with a type on each line and the staff list.
        typed = {(r["identifier"].replace("daily_sales.", "daily_sales "), r["attribute"], r["value"]) for r in self.records if r["type"] in ("dataset", "column", "dashboard")}
        plain = {(r["asset"] + (" " + r["column"] if r["column"] else ""), r["field"], r["value"]) for r in self.together}
        self.assertEqual(typed, plain)
        people = {(r["identifier"], r["attribute"], r["value"]) for r in self.records if r["type"] == "person"}
        self.assertEqual(people, {("j.marsh", "name", "Jo Marsh"), ("j.marsh", "team", "finance"), ("s.lund", "name", "Sam Lund"), ("s.lund", "team", "catalogue")})
        self.says("The head answers that `j.marsh` is Jo Marsh, in finance, and `s.lund` is Sam Lund, in catalogue.")
        self.assertEqual({r["type"] for r in self.model}, {"dataset", "column", "dashboard", "person", "team"})
        self.says("The model cell defines the types `dataset`, `column`, `dashboard`, `person` and `team`.")

    def test_the_check_and_the_merge(self):
        problems = self.model.check(self.records)
        self.assertEqual(len(problems), 5)
        self.assertEqual(
            sorted(p["text"].split(":")[0] for p in problems),
            sorted([
                "dataset daily_sales responsible", "dataset s3", "dataset clean_customers responsible",
                "dataset clean_orders responsible", "dataset clean_orders drops",
            ]),
        )
        self.says("Before your change, the check lists 5 problems.")
        after = self.model.check(self.merged())
        self.assertEqual(len(after), 3)
        self.says("The check then lists 3 problems.")
        count = "SELECT COUNT(DISTINCT value) AS owners\n        FROM records\n        WHERE attribute = 'responsible'"
        self.assertIn(count, SOURCE[4])
        self.assertEqual((self.records.sql(count)[0]["owners"], self.merged().sql(count)[0]["owners"]), (4, 3))
        self.says("Before your change it counts 4. After your change it counts 3: `j.marsh`, `s.lund` and the data engineer")
        drops = shop.model(self.model.text + "\ndataset drops: text\n")
        self.assertEqual(len(drops.check(self.merged())), 2)
        self.says("Add the line `dataset drops: text` to the model cell, and press **Run below**. The check then lists 2 problems")
        self.assertEqual(sorted({r["value"] for r in self.merged() if r["identifier"] == "daily_sales" and r["attribute"] == "responsible"}), ["j.marsh"])

    def test_the_owners_by_reading(self):
        self.assertIn('.replace("responsible: Jo Marsh", "responsible: j.marsh")', SOURCE[4])
        self.assertIn('the_data_engineer = "team"', SOURCE[4])
        got = {}
        for kind in ("team", "person"):
            after = shop.typed_records(
                self.merged().text.replace("responsible: the data engineer", "responsible: data_engineering")
                + f"\n{kind} data_engineering name: the data engineer\n"
            )
            rows = shop.owners(self.week, after)
            self.assertEqual(len(rows), 7)
            got[kind] = tuple(sum(1 for r in rows if r[k] == "yes") for k in ("one_owner", "one_person", "one_team"))
            self.assertEqual({r["asset"] for r in rows if r["one_owner"] == "no"}, {"s3://shop-raw/orders.jsonl", "s3://shop-raw/customers.jsonl"})
        self.assertEqual(got, {"team": (5, 3, 5), "person": (5, 5, 3)})
        self.says("With the data engineer as a team, 5 of the 7 assets have one owner under `one_owner`, 3 have one person under `one_person`, and 5 have one team under `one_team`. With the data engineer as a person, the counts are 5, 5 and 3")
        self.says("`orders.jsonl` and `customers.jsonl` have no `responsible` line in the records, so they fail every reading.")
        self.says("No reading holds for all 7 assets.")


class TheWordsOfChapter5(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = flat(TEXT[5])
        cls.records = shop.typed_records(literal(5, "typed_records"))
        cls.model = shop.model(literal(5, "model"))
        cls.graph = shop.graph(cls.records, cls.model)

    def says(self, phrase: str) -> None:
        self.assertIn(flat(phrase), self.text)

    def test_the_records_are_chapter_4s(self):
        self.assertEqual(self.model.check(self.records), [])
        self.assertIn("column of: dataset", self.model.text)
        self.assertIn("dataset drops: text", self.model.text)
        self.assertIn("dataset clean_orders drops: orders with no customer id", self.records.text)
        # Chapter 4's records after both changes: the merge, and the data engineer a team.
        four = literal(4, "typed_records")
        after = (four.replace("responsible: Jo Marsh", "responsible: j.marsh").replace("responsible: Sam Lund", "responsible: s.lund")
                 .replace("responsible: the data engineer", "responsible: data_engineering"))
        lines = lambda t: {l for l in t.splitlines() if l.strip() and not l.startswith("#")}
        extra = {"team data_engineering name: the data engineer", "column daily_sales.day of: daily_sales", "column daily_sales.revenue_pence of: daily_sales"}
        self.assertEqual(lines(self.records.text), lines(after) | extra)
        self.assertEqual(len(lines(self.records.text)), 20)
        self.says("The shop's records are 20 lines.")

    def test_the_graph(self):
        nodes = self.graph.nodes()
        self.assertEqual(len(nodes), 12)
        kinds = {}
        for n in nodes:
            kinds[n["type"]] = kinds.get(n["type"], 0) + 1
        self.assertEqual(kinds, {"dataset": 4, "column": 2, "dashboard": 1, "person": 2, "team": 3})
        self.says("There are 12: 4 datasets (`daily_sales`, `clean_customers`, `clean_orders`, `products.csv`), 2 columns, the dashboard, 2 people and 3 teams.")
        self.assertFalse({"s3://shop-raw/orders.jsonl", "s3://shop-raw/customers.jsonl"} & {n["node"] for n in nodes})
        edges = {}
        for e in self.graph.edges():
            edges[e["edge"]] = edges.get(e["edge"], 0) + 1
        self.assertEqual(edges, {"responsible": 5, "team": 2, "of": 2})
        self.says("There are 9, of three kinds: 5 `responsible`, 2 `of` and 2 `team`.")
        self.assertEqual(len(self.graph.drawing()._parts()), 3)
        self.says("There are 3 parts.")

    def test_the_traversals(self):
        self.assertIn('graph.traverse("j.marsh", {"responsible": "in"})', SOURCE[5])
        first = self.graph.traverse("j.marsh", {"responsible": "in"})
        self.assertEqual([(r["node"], r["steps"]) for r in first], [("daily_sales", 1), ("sales_dashboard", 1)])
        self.says("The traversal reaches `daily_sales` and `sales_dashboard`, each by 1 edge")
        self.assertEqual(len(self.graph.traverse("j.marsh", {"responsible": "out"})), 0)
        self.says('With `"out"`, the traversal reaches no node, and the cell shows "No rows."')
        self.says("took the traversal from `j.marsh` from 2 nodes to none")
        every = self.graph.traverse("daily_sales")
        self.assertEqual({r["node"] for r in every}, {"j.marsh", "daily_sales.day", "daily_sales.revenue_pence", "sales_dashboard", "finance"})
        [dash] = [r for r in every if r["node"] == "sales_dashboard"]
        self.says(f"Read the `path` of `sales_dashboard` in the table above: `{dash['path']}`.")
        self.says("The traversal does not reach `clean_orders`.")
        shared = self.graph.traverse("clean_customers")
        self.assertEqual([(r["node"], r["steps"]) for r in shared], [("data_engineering", 1), ("clean_orders", 2)])
        self.says("It reaches `data_engineering` by 1 edge, then `clean_orders` by 2")
        self.assertEqual({e["edge"] for e in self.graph.edges()}, {"responsible", "team", "of"})


class TheWordsOfChapter6(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.week = shop.run_week()
        cls.text = flat(TEXT[6])
        cls.records = shop.typed_records(literal(6, "typed_records"))
        cls.model = shop.model(literal(6, "model"))
        cls.lineage = shop.graph(cls.records, cls.model).only(["reads", "writes"], ["dataset", "dashboard", "job"])
        cls.repo = shop.repository(cls.week)

    def says(self, phrase: str) -> None:
        self.assertIn(flat(phrase), self.text)

    def test_the_code_and_the_lines(self):
        self.assertEqual([r["file"] for r in self.repo], [
            "jobs/build_clean_customers.py", "jobs/build_clean_orders.py", "jobs/build_daily_sales.py", "jobs/refresh_dashboard.py",
        ])
        self.assertEqual(shop.compare_with_code(self.records, self.repo), [])
        self.assertEqual(self.model.check(self.records), [])
        # Chapter 5's records and model in full, then the files' and the jobs' lines.
        lines = lambda t: {l for l in t.splitlines() if l.strip() and not l.startswith("#")}
        self.assertLessEqual(lines(literal(5, "typed_records")), lines(self.records.text))
        self.assertLessEqual(lines(literal(5, "model")), lines(self.model.text))
        self.says("The records cell holds Chapter 5's records in full.")
        self.says("The model cell holds Chapter 5's model")
        # Only build_clean_orders' code names the column the developer renames.
        self.assertEqual([r["file"] for r in self.repo if "customer_id" in r["code"]], ["jobs/build_clean_customers.py", "jobs/build_clean_orders.py"])
        [orders] = [r for r in self.repo if r["file"] == "jobs/build_clean_orders.py"]
        self.assertIn("customer_id IS NOT NULL", orders["code"])
        self.assertIn("SELECT DISTINCT order_id, customer_id", orders["code"])
        self.says("Only the code of `build_clean_orders` names `customer_id`: in its `SELECT` and in its `WHERE`.")
        self.says("The code of `build_clean_orders` has `WHERE customer_id IS NOT NULL`.")

    def test_the_map(self):
        self.assertEqual((len(self.lineage.nodes()), len(self.lineage.edges())), (11, 8))
        self.assertEqual(len(self.lineage.drawing()._parts()), 3)

    def test_downstream_and_upstream(self):
        down = [r["node"] for r in self.lineage.downstream("s3://shop-raw/orders.jsonl")]
        self.assertEqual(down, ["build_clean_orders", "clean_orders", "build_daily_sales", "daily_sales", "refresh_dashboard", "sales_dashboard"])
        self.says("Downstream of `orders.jsonl` there are 6 nodes: the jobs `build_clean_orders`, `build_daily_sales` and `refresh_dashboard`, and the assets `clean_orders`, `daily_sales` and `sales_dashboard`.")
        up = [r["node"] for r in self.lineage.upstream("sales_dashboard")]
        self.assertEqual((len(up), up[-1]), (6, "s3://shop-raw/orders.jsonl"))
        self.assertFalse({"s3://shop-raw/customers.jsonl", "clean_customers"} & set(up))
        self.assertEqual(self.lineage.upstream("sales_dashboard")[-1]["steps"], 6)
        self.says("Upstream of `sales_dashboard` there are 6 nodes. The farthest back is `orders.jsonl`, 6 steps away.")
        self.assertEqual(self.lineage.downstream("s3://shop-raw/products.csv"), [])
        self.says("Downstream of `products.csv` there is nothing: the cell shows \"No rows.\"")

    def test_the_belief_and_the_stale_line(self):
        self.assertIn('jos_line = "job build_daily_sales reads: clean_customers"', SOURCE[6])
        with_jo = shop.typed_records(self.records.text + "\njob build_daily_sales reads: clean_customers\n")
        reached = [r["node"] for r in shop.graph(with_jo, self.model).downstream("s3://shop-raw/customers.jsonl")]
        self.assertEqual(len(reached), 6)
        self.assertTrue({"daily_sales", "sales_dashboard"} <= set(reached))
        self.says("With Jo's line, downstream of `customers.jsonl` there are 6 nodes, `daily_sales` and `sales_dashboard` among them.")
        [row] = shop.compare_with_code(with_jo, self.repo)
        self.assertEqual(row["says"], "reads: clean_customers")
        self.says("The comparison lists one row: Jo's line.")
        changed = shop.run_week(["source"])
        stale = shop.compare_with_code(self.records, shop.repository(changed))
        self.assertEqual([(r["says"], r["code"]) for r in stale], [("reads: clean_orders", ""), ("", "reads: s3://shop-scratch/clean_orders_copy.csv")])
        self.says("It lists 2 rows.")
        self.assertEqual(changed.warehouse.sql("SELECT * FROM daily_sales"), self.week.warehouse.sql("SELECT * FROM daily_sales"))
        self.says("`True`: the rows of `daily_sales` are the same in the changed week as today.")
        from shop import week as w

        self.assertIn("SUM(price_pence * quantity)", w.DAILY_SALES)
        self.says("`revenue_pence` is made from `price_pence` and `quantity` of `clean_orders`")


class TheWordsOfChapter7(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.week = shop.run_week()
        cls.returns = shop.run_week(["returns"])
        cls.text = flat(TEXT[7])

    def says(self, phrase: str) -> None:
        self.assertIn(flat(phrase), self.text)

    def test_what_the_shop_held(self):
        [row] = self.week.warehouse.sql("SELECT row_count, last_altered FROM information_schema.tables WHERE table_name = 'clean_orders'")
        self.assertEqual((row["row_count"], row["last_altered"]), (44, "2026-09-14T02:05:52Z"))
        self.says("The warehouse records that `clean_orders` has 44 rows and was last written at `2026-09-14T02:05:52Z`")

    def test_the_rows_left_out(self):
        events = shop.events(self.week, ["job", "type", "time", "rows_read", "rows_written"]).where(job="build_clean_orders")
        self.assertEqual(len(events), 14)
        self.says("`build_clean_orders` sent 14 events: a start and a finish on each of the 7 nights.")
        runs = shop.runs(events, by=["job", "day"])
        left = [r["rows_read"] - r["rows_written"] for r in runs]
        self.assertEqual(left, [0, 0, 1, 4, 4, 4, 4])
        self.says("Rows read minus rows written gives the rows left out: 0, 0, 1, 4, 4, 4 and 4.")
        self.assertEqual(shop.data.DUPLICATED, 7015)
        self.says("The 1 is the export's second copy of order 7015, which Chapter 2's rules keep once.")
        thursday = [o for o in shop.data.ORDERS if o[6].startswith("2026-09-10") and o[1] is None]
        self.assertEqual(len(thursday), 3)
        self.says("For Jo, the answer is 3 orders, all placed on Thursday, left out from the run on Friday 11 onwards.")
        self.says("They do not say which orders, or why.")

    def test_two_runs_on_one_day(self):
        design = ["job", "type", "time", "rows_read", "rows_written", "object", "object_change"]
        by_day = shop.runs(shop.events(self.returns, design).where(job="record_return"), by=["job", "day"])
        [wednesday] = [r for r in by_day if r["day"] == "2026-09-09"]
        self.assertEqual((wednesday["events"], wednesday["rows_read"], wednesday["rows_written"], wednesday["started"], wednesday["finished"]), (4, 2, 2, "2026-09-09T10:05:02Z", "2026-09-09T15:40:05Z"))
        self.says("Wednesday 9 shows 1 row with 4 events, 2 objects (`r-202.json` and `r-203.json`), 2 rows read and 2 written, starting at `10:05:02` and finishing at `15:40:05`.")
        runs = shop.runs(shop.events(self.returns, design + ["run", "object_version"])).where(job=["record_return", "remove_return"])
        self.assertEqual(len(runs), 6)
        self.says("There are 6 runs of the two functions, one for each change to a return's file.")
        [removed] = [r for r in runs if r["job"] == "remove_return"]
        self.assertEqual((removed["rows_read"], removed["object_change"]), (0, "deleted"))
        self.says("It read 0 rows: the file was gone when it started.")
        self.assertEqual(len(self.returns.storage.ls("s3://shop-returns/")), 3)
        self.says("three return files in object storage")

    def test_what_each_run_read(self):
        changed = shop.run_week(["returns", "source"])
        runs = shop.runs(shop.events(changed, ["run", "job", "type", "reads", "code_version"])).where(job="build_daily_sales")
        self.assertEqual([(r["reads"], r["code_version"]) for r in runs], [("clean_orders", "256e271")] * 5 + [(shop.COPY, "c715bde")] * 2)
        self.says("The runs on Tuesday 8 to Saturday 12 read `clean_orders`, with code version `256e271`.")
        self.says("The runs on Sunday 13 and Monday 14 read `s3://shop-scratch/clean_orders_copy.csv`, with code version `c715bde`.")

    def test_without_reads(self):
        with_reads = shop.lineage(shop.runs(shop.events(self.week, ["run", "job", "type", "reads", "writes"])))
        self.assertEqual(len(with_reads.upstream("sales_dashboard")), 6)
        without = shop.lineage(shop.runs(shop.events(self.week, ["run", "job", "type", "writes"])))
        self.assertEqual([r["node"] for r in without.upstream("sales_dashboard")], ["refresh_dashboard"])
        self.says("With `reads`, the traversal reaches 6 nodes, back to `orders.jsonl`.")
        self.says("Without `reads`, the traversal reaches only `refresh_dashboard`.")
        changed = shop.run_week(["returns", "source"])
        [removed] = shop.runs(shop.events(changed, ["run", "job", "type", "time", "reads", "code_version"])).where(job="remove_return")
        self.assertIn(removed["reads"], (None, ""))
        self.says("The run of `remove_return` on Saturday 12 has an empty `reads`")

    def test_the_readings(self):
        rows = shop.readings(["run", "job", "type", "time", "status"])
        self.assertIn('yours = ["run", "job", "type", "time", "status"]', SOURCE[7])
        self.assertEqual([r["met"] for r in rows], ["yes", "no", "no", "no"])
        self.says("and meets the first reading only")


class TheWordsOfChapter8(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.week = shop.run_week(["returns", "failed"])
        cls.events = shop.openlineage.run_events(cls.week)
        cls.text = flat(TEXT[8])

    def says(self, phrase: str) -> None:
        self.assertIn(flat(phrase), self.text)

    def test_one_run(self):
        friday = [e for e in self.events if e["job"]["name"] == "build_clean_orders" and e["eventTime"].startswith("2026-09-11")]
        start, complete = friday
        self.assertEqual((start["eventType"], complete["eventType"]), ("START", "COMPLETE"))
        self.assertEqual(complete["inputs"][0]["inputFacets"]["inputStatistics"]["rowCount"], 27)
        self.assertEqual(complete["outputs"][0]["outputFacets"]["outputStatistics"]["rowCount"], 23)
        self.assertEqual(complete["job"]["facets"]["sourceCodeLocation"]["version"], "b178023")
        self.says("`sourceCodeLocation` holds the code version, `b178023`.")
        self.says("`inputStatistics` holds the rows read, 27. `outputStatistics` holds the rows written, 23.")
        self.assertEqual(start["run"]["runId"][14], "7")
        self.assertEqual(start["producer"], shop.openlineage.PRODUCER)
        self.says("Here it is `https://example.org/shop/jobs/tree/v1`, which makes the events of all four jobs.")
        self.assertEqual((complete["outputs"][0]["namespace"], complete["outputs"][0]["name"]), ("warehouse://shop-warehouse", "shop.analytics.clean_orders"))

    def test_the_consumer(self):
        friday = [e for e in self.events if e["job"]["name"] == "build_clean_orders" and e["eventTime"].startswith("2026-09-11")]
        c = shop.openlineage.Consumer().send(friday[0])
        [row] = c.runs()
        self.assertEqual((row["state"], row["outputs"], row["ended"]), ("START", "", None))
        c.send(friday[1])
        [row] = c.runs()
        self.assertEqual((row["state"], row["ended"], row["events"]), ("COMPLETE", "2026-09-11T02:05:52Z", 2))
        self.says("The row now holds the state `COMPLETE`, the end time `2026-09-11T02:05:52Z`")
        everything = shop.openlineage.Consumer().send(*self.events)
        self.assertEqual((len(everything.runs()), len(everything.runs(state="FAIL"))), (34, 1))
        self.says("The consumer holds 34 runs. One of them has the state `FAIL`: `build_daily_sales` on Monday 14.")

    def test_two_names(self):
        OL = shop.openlineage
        start = {
            "eventType": "START", "eventTime": "2026-09-11T02:15:00Z",
            "run": {"runId": OL.uuid7("2026-09-11T02:15:00Z", "copy")},
            "job": {"namespace": "analyst", "name": "copy_clean_orders"},
            "inputs": [{"namespace": "warehouse://shop-warehouse", "name": "analytics.clean_orders"}],
            "outputs": [], "producer": "https://example.org/analyst/copy-script/v1", "schemaURL": OL.SCHEMA_URL,
        }
        self.assertIn('"name": "analytics.clean_orders"', SOURCE[8])
        complete = {**start, "eventType": "COMPLETE", "eventTime": "2026-09-11T02:15:17Z", "outputs": [{"namespace": "s3://shop-scratch", "name": "clean_orders_copy.csv"}]}
        self.assertEqual(OL.problems(start), [])
        up = OL.Consumer().send(*self.events, start, complete).lineage().upstream("s3://shop-scratch/clean_orders_copy.csv")
        self.assertEqual(len(up), 2)
        self.assertEqual([r["node"] for r in up], ["analyst/copy_clean_orders", "warehouse://shop-warehouse/analytics.clean_orders"])
        self.says("The traversal reaches 2 nodes, `analyst/copy_clean_orders` and `warehouse://shop-warehouse/analytics.clean_orders`, and stops.")
        start["inputs"] = [{"namespace": "warehouse://shop-warehouse", "name": "shop.analytics.clean_orders"}]
        complete["inputs"] = start["inputs"]
        up = OL.Consumer().send(*self.events, start, complete).lineage().upstream("s3://shop-scratch/clean_orders_copy.csv")
        self.assertEqual([r["node"] for r in up][-1], "s3://shop-raw/orders.jsonl")
        self.assertEqual(len(up), 4)
        self.says("The traversal then reaches 4 nodes, through `shop/build_clean_orders`, to `orders.jsonl`.")

        broken = {**start, "run": {"runId": "copy-friday"}}
        del broken["producer"]
        self.assertEqual(OL.problems(broken), [("producer", "missing"), ("run.runId", "run_id")])
        self.says("The check lists 2 problems: `producer` is missing, and `run.runId` is not a UUID.")
        refusing = OL.Consumer().send(broken)
        self.assertEqual((len(refusing.refused), len(refusing.runs())), (1, 0))

    def test_the_summary(self):
        rows = shop.openlineage.summary(self.events)
        self.assertEqual(len(rows), 6)
        self.assertEqual(sum(r["FAIL"] for r in rows), 1)
        self.assertEqual(sum(r["breaking a rule"] for r in rows), 0)
        self.says("In all, 6 programs sent events: the four jobs and the two functions.")
        self.says("No event breaks the specification's rules.")


class TheWordsOfChapter9(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        I = shop.ingest
        cls.text = flat(TEXT[9])
        lines = I.event_lines(shop.run_week(["returns", "source"]))
        cls.lines = lines
        damaged = list(lines)
        k = next(i for i, line in enumerate(damaged) if '"build_daily_sales"' in line and '"COMPLETE"' in line and "2026-09-09" in line)
        damaged[k] = damaged[k][:150]
        cls.parsed = I.parse(damaged)
        cls.normal = I.normalise(cls.parsed)
        cls.objs = I.objects(cls.normal)
        cls.edges = I.edges(cls.objs)

    def says(self, phrase: str) -> None:
        self.assertIn(flat(phrase), self.text)

    def test_parse_and_normalise(self):
        self.assertEqual((len(self.lines), len(self.parsed), [r["line"] for r in self.parsed.refused]), (82, 81, [20]))
        self.says("The week has 82 lines. One is refused: line 20, which is not JSON. 81 events pass.")
        kinds = [c["where"].split("[")[0] for c in self.normal.changes]
        self.assertEqual((len(kinds), kinds.count("eventTime"), kinds.count("inputs")), (26, 12, 14))
        self.says("The stage made 26 changes: 12 times, in the functions' events (6 runs, 2 events each), and 14 names, in the analyst's events (7 nights, 2 events each).")

    def test_objects(self):
        o = self.objs
        self.assertEqual((len(o.jobs), len(o.runs), len(o.datasets), len(o.unknown)), (7, 41, 12, 6))
        self.says("The stage made 7 job records, one for each program that sent events: the four jobs, the two functions and the analyst's script. It made 41 run records and 12 dataset records, and it listed 6 facets it does not read.")
        [still] = o.runs_of(state="START")
        self.assertEqual((still["job"], still["started"]), ("shop/build_daily_sales", "2026-09-09T02:30:00Z"))
        self.assertEqual({u["facet"] for u in o.unknown}, {"shop_objectChange"})
        self.assertEqual(list(shop.ingest.KNOWN), ["nominalTime", "jobType", "sourceCodeLocation", "inputStatistics", "outputStatistics", "version"])
        self.says("It reads fields only from the facets it knows: `nominalTime`, `jobType`, `sourceCodeLocation`, `inputStatistics`, `outputStatistics` and `version`.")
        known = {**shop.ingest.KNOWN, "shop_objectChange": ["object", "version", "change"]}
        self.assertIn('# known["shop_objectChange"] = ["object", "version", "change"]', SOURCE[9])
        taught = shop.ingest.objects(self.normal, known)
        self.assertEqual(len(taught.unknown), 0)

    def test_edges_and_current(self):
        e = self.edges
        self.assertEqual((len(e.by_run), len(e.by_job)), (80, 17))
        self.says("There are 80 edges by run and 17 edges by job.")
        self.says("The week has 41 runs: 35 by night (7 nights, each with the four jobs and the analyst's script) and 6 by the functions, during the day.")
        daily = {(r["edge"], r["dataset"].rsplit("/", 1)[-1]): r for r in e.of("shop/build_daily_sales")}
        self.assertEqual(daily[("reads", "shop.analytics.clean_orders")]["runs"], 5)
        self.assertEqual((daily[("reads", "shop.analytics.clean_orders")]["first"], daily[("reads", "shop.analytics.clean_orders")]["last"]), ("2026-09-08T02:30:21Z", "2026-09-12T02:30:21Z"))
        self.assertEqual(daily[("reads", "clean_orders_copy.csv")]["runs"], 2)
        self.assertEqual(daily[("writes", "shop.analytics.daily_sales")]["runs"], 6)
        self.says("It reads `clean_orders` in 5 runs, the first at `2026-09-08T02:30:21Z` and the last at `2026-09-12T02:30:21Z`. It reads the analyst's copy in 2 runs, on Sunday 13 and Monday 14. It writes `daily_sales` in 6 runs, not 7.")
        latest = e.latest()
        self.assertEqual(len(latest), 13)
        self.says("That cell lists 13 of the 17 edges by job.")
        dropped = {(r["job"], r["dataset"].rsplit("/", 1)[-1]) for r in e.by_job} - {(r["job"], r["dataset"].rsplit("/", 1)[-1]) for r in latest}
        self.assertEqual(dropped, {("shop/build_daily_sales", "shop.analytics.clean_orders"), ("shop/record_return", "r-201.json"), ("shop/record_return", "r-202.json"), ("shop/record_return", "r-203.json")})
        held = {r["return_id"] for r in shop.run_week(["returns"]).warehouse.sql("SELECT return_id FROM returns")}
        self.assertEqual(held, {"r-201", "r-202", "r-204"})
        self.says("The rows of `r-201` and `r-202` are still in the table `returns`. The row of `r-203` was removed when its file was deleted.")
        g = e.graph()
        self.assertEqual((len(g.nodes()), len(g.edges())), (19, 17))


class TheWordsOfChapter10(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from shop import columns

        cls.C = columns
        cls.text = flat(TEXT[10])
        cls.week = shop.run_week()
        [cls.code] = [p["code"] for p in columns.programs(cls.week) if p["job"] == "build_daily_sales"]

    def says(self, phrase: str) -> None:
        self.assertIn(flat(phrase), self.text)

    def test_what_the_sql_names(self):
        self.assertEqual(sorted({r["column"] for r in self.C.lineage(self.code)}), ["daily_sales.column 1", "daily_sales.column 2"])
        self.says("The parser lists `column 1` and `column 2`. The SELECT names no column of `daily_sales`.")
        self.assertIn("catalogue = None\n# catalogue = warehouse\n", SOURCE[10].replace("    ", ""))
        named = self.C.lineage(self.code, self.week.warehouse)
        revenue = {(r["from"].split(".")[1], r["kind"], r["how"]) for r in named if r["column"] == "daily_sales.revenue_pence"}
        self.assertEqual(revenue, {("price_pence", "value", "aggregated"), ("quantity", "value", "aggregated"), ("status", "rows", "filter"), ("ordered_at", "rows", "filter"), ("ordered_at", "rows", "grouping")})
        self.assertNotIn("Then the parser names them", TEXT[10])

    def test_back_to_the_raw_orders(self):
        up = self.C.upstream(self.week, "daily_sales", "revenue_pence", self.week.warehouse)
        by = lambda d: [r for r in up if r["dataset"] == d]
        self.assertEqual((len(up), len(by("clean_orders")), len(by("orders.jsonl"))), (11, 4, 7))
        self.says("11 columns: 4 of `clean_orders` and 7 of `orders.jsonl`.")
        self.assertEqual({r["column"] for r in by("orders.jsonl") if r["value"] == "yes"}, {"price_pence", "quantity"})
        self.says("The value of `revenue_pence` is made from 2 columns of `orders.jsonl`: `price_pence` and `quantity`.")
        self.assertTrue(all(r["rows"] for r in by("orders.jsonl")))
        self.says("All 7 decide which rows count: `build_clean_orders` keeps one row of each set of equal rows (`distinct`)")
        # The week's three oddities, each through a column that decides which rows count.
        from shop.data import DUPLICATED, ORDERS

        self.assertEqual(DUPLICATED, 7015)
        self.assertEqual(len([o for o in ORDERS if o[6][:10] == "2026-09-10" and o[1] is None]), 3)
        self.assertEqual({o[6][:10] for o in ORDERS if o[5] == "cancelled"}, {"2026-09-08", "2026-09-12"})
        self.says("`distinct` removed Wednesday's second copy of order 7015; the filter of `build_clean_orders` removed Thursday's 3 orders with no `customer_id`")

    def test_select_star(self):
        week = shop.run_week(["source"])
        self.assertEqual([r["from"] for r in self.C.lineage(self.C.ANALYST_COPY)], ["clean_orders.*"])
        self.assertEqual(len(self.C.lineage(self.C.ANALYST_COPY, week.warehouse)), 7)
        self.says("With the catalogue, it gives 7 rows, one for each column of `clean_orders`, each `copied`.")
        up = self.C.upstream(week, "daily_sales", "revenue_pence", week.warehouse)
        count = lambda d: len([r for r in up if r["dataset"] == d])
        self.assertEqual((len(up), count("clean_orders_copy.csv"), count("clean_orders"), count("orders.jsonl")), (15, 4, 4, 7))
        self.says("15 columns in all, through the copy (4), then `clean_orders` (4), to `orders.jsonl` (7).")

    def test_a_function(self):
        week = shop.run_week(["net"])
        self.assertEqual(week.warehouse.sql("SELECT * FROM daily_sales"), self.week.warehouse.sql("SELECT * FROM daily_sales"))
        self.says("No order of Saturday or Sunday was returned, so the rows of `daily_sales` are the same.")
        self.assertEqual(week.warehouse.sql("SELECT returned_quantity(7004, 2) AS a, returned_quantity(7008, 1) AS b, returned_quantity(7001, 1) AS c"), [{"a": 1, "b": 1, "c": 0}])
        self.says("`returned_quantity(7004, 2)` and `returned_quantity(7008, 1)` give 1: one of each came back (`r-201` and `r-202`). `returned_quantity(7001, 1)` gives 0.")
        up = self.C.upstream(week, "daily_sales", "revenue_pence", week.warehouse)
        self.assertEqual(len(up), 13)
        self.assertNotIn("returns", {r["dataset"] for r in up})
        self.says("13 columns. None is in `returns`.")
        inputs = {d["name"] for e in shop.openlineage.run_events(week) if e["job"]["name"] == "build_daily_sales" for d in e["inputs"]}
        self.assertEqual(inputs, {"shop.analytics.clean_orders"})
        self.says("The run's events also name `clean_orders` as the only input.")

    def test_the_facet(self):
        f = self.C.facet(self.week, "daily_sales")
        got = {name: {(i["field"], i["transformations"][0]["subtype"]) for i in v["inputFields"]} for name, v in f["fields"].items()}
        self.assertEqual(got, {"day": {("ordered_at", "TRANSFORMATION")}, "revenue_pence": {("price_pence", "AGGREGATION"), ("quantity", "AGGREGATION")}})
        self.assertEqual({(i["field"], i["transformations"][0]["subtype"]) for i in f["dataset"]}, {("ordered_at", "FILTER"), ("ordered_at", "GROUP_BY"), ("status", "FILTER")})
        self.says("Under `dataset`: `ordered_at` (`FILTER` and `GROUP_BY`) and `status` (`FILTER`).")


class TheWordsOfChapter11(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from shop import schemas

        cls.S = schemas
        cls.text = flat(TEXT[11])

    def says(self, phrase: str) -> None:
        self.assertIn(flat(phrase), self.text)

    def test_versions_and_comparisons(self):
        week = shop.run_week(["renamed"])
        v = self.S.versions(week, "orders.jsonl")
        self.assertEqual([(r["writes"], r["first written"][:10], r["last written"][:10]) for r in v], [(5, "2026-09-08", "2026-09-12"), (2, "2026-09-13", "2026-09-14")])
        self.says("The changed export first appears on Sunday 13, and its schema version is the second.")
        self.assertEqual([(r["column"], r["change"]) for r in self.S.diff(week, "orders.jsonl")], [("quantity", "removed"), ("qty", "added")])
        self.says("The shop's records match columns by name: `quantity` is removed and `qty` added.")
        rows = self.S.diffs()
        self.assertEqual({r["schema versions of clean_orders"] for r in rows}, {1})
        self.says("Under every change, `clean_orders` has 1 schema version")
        types = shop.run_week(["retyped"]).warehouse.sql("SELECT typeof(customer_id) AS type, COUNT(*) AS n FROM clean_orders GROUP BY 1")
        self.assertEqual(types, [{"type": "text", "n": 44}])
        self.says("All 44 values are `text`, in a column the catalogue declares `INTEGER`.")

    def test_what_each_reader_gets(self):
        got = {r["reader"]: (r["added"], r["renamed"], r["retyped"]) for r in self.S.compare_all()}
        self.assertEqual(list(got.values()), [(7, 5, 7), (7, 5, 7), (7, 0, 0)])
        self.says("The new name broke all three readers. The new ids broke Jo Marsh's query only. The new field broke none.")
        week = shop.run_week(["renamed"])
        self.assertEqual([e.rows for e in week.executions if e.writer == "clean_orders"][-2:], [0, 0])
        self.assertEqual({e.status for e in week.executions if e.writer == "clean_orders"}, {"succeeded"})

    def test_who_reads_the_column(self):
        week = shop.run_week(["renamed"])
        for column in ("quantity", "customer_id"):
            [r] = self.S.readers(week, "orders.jsonl", column)
            self.assertEqual((r["program"], r["reads it for"]), ("build_clean_orders", "rows: distinct; rows: filter; value: copied"))
        self.assertIn('column = "quantity"', SOURCE[11])


class TheWordsOfChapter12(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = flat(TEXT[12])
        I = shop.ingest
        cls.week = shop.run_week(["returns", "dev", "view"])
        cls.parsed = I.parse(I.event_lines(cls.week))

    def says(self, phrase: str) -> None:
        self.assertIn(flat(phrase), self.text)

    def writers(self, databases=None):
        I = shop.ingest
        edges = I.edges(I.objects(I.normalise(self.parsed, databases)))
        return {(r["job"], r["dataset"].rsplit("/", 1)[-1], r["runs"], r["last"]) for r in edges.by_job if r["edge"] == "writes" and r["dataset"].endswith(".daily_sales")}

    def test_the_development_run(self):
        self.assertEqual(
            self.writers(),
            {("shop/build_daily_sales", "shop.analytics.daily_sales", 7, "2026-09-14T02:30:21Z"), ("dev/build_daily_sales", "shop.analytics.daily_sales", 1, "2026-09-14T10:20:04Z")},
        )
        self.says("`shop/build_daily_sales`, in 7 runs, the last at `2026-09-14T02:30:21Z`;")
        self.says("`dev/build_daily_sales`, in 1 run, at `2026-09-14T10:20:04Z`.")
        after = self.writers({shop.openlineage.DEV_PRODUCER: "shop_dev"})
        self.assertIn(("dev/build_daily_sales", "shop_dev.analytics.daily_sales", 1, "2026-09-14T10:20:04Z"), after)
        self.says("After the change, `dev/build_daily_sales` writes `shop_dev.analytics.daily_sales`, and `shop/build_daily_sales` is the only program that writes `shop.analytics.daily_sales`.")

    def test_the_six_pairs(self):
        from shop import identity

        v1, v2 = [v["version"] for v in self.week.storage.versions("s3://shop-returns/r-202.json")]
        self.assertEqual([v["at"][:10] for v in self.week.storage.versions("s3://shop-returns/r-202.json")], ["2026-09-09", "2026-09-10"])
        self.assertEqual(self.week.storage.versions("s3://shop-raw/Orders.jsonl")[0]["at"][:10], "2026-09-11")
        pairs = [
            ("shop.analytics.daily_sales", "SHOP.ANALYTICS.DAILY_SALES"),
            ("daily_sales", "shop.analytics.daily_sales"),
            ("shop.analytics.daily_sales", "shop_dev.analytics.daily_sales"),
            ("shop.analytics.daily_sales", "shop.analytics.sales_by_day"),
            ("s3://shop-raw/orders.jsonl", "s3://shop-raw/Orders.jsonl"),
            (f"s3://shop-returns/r-202.json@{v1}", f"s3://shop-returns/r-202.json@{v2}"),
        ]
        for a, b in pairs:
            self.assertIn(a.split("@")[0], SOURCE[12])
        got = [(r["same object"], r["same rows"], r["same environment"], r["same version"]) for r in identity.compare(self.week, pairs)]
        self.assertEqual(
            got,
            [("yes", "yes", "yes", ""), ("yes", "yes", "yes", ""), ("no", "no", "no", ""), ("no", "yes", "yes", ""), ("no", "no", "yes", ""), ("yes", "no", "yes", "no")],
        )
        self.says("No pair has the same text, yet pairs 1 and 2 are the same object, with the same rows and environment.")
        self.says("Pair 4 has the same rows and environment, but is another object.")
        self.says("Pair 6 is one object, but not the same rows or version.")


class TheWordsOfPartV(unittest.TestCase):
    """Chapters 18 to 23: every number and time the prose states, computed again."""

    @classmethod
    def setUpClass(cls):
        from shop import aliases, claims, delivery, ingest, scale

        cls.D, cls.I, cls.C, cls.A, cls.S = delivery, ingest, claims, aliases, scale
        cls.week = shop.run_week(["returns"])

    def says(self, phrase: str, chapter: int) -> None:
        self.assertIn(flat(phrase), flat(TEXT[chapter]))

    def graph(self, events):
        return self.I.edges(self.I.objects(self.I.normalise(events)))

    def test_chapter_18(self):
        D = self.D
        whole = D.send(self.week)
        self.assertEqual((len(whole.log), len(whole.events)), (68, 68))
        self.says("The cell sent 68 events, and the collector received 68. None was lost.", 18)
        runs = lambda d: [(r["edge"], r["runs"]) for r in self.graph(d.events).of("shop/build_daily_sales")]
        self.assertEqual(runs(whole), [("reads", 7), ("writes", 7)])
        lost = D.send(self.week, lose=["build_daily_sales COMPLETE 2026-09-10"])
        self.assertEqual(runs(lost), [("reads", 7), ("writes", 6)])
        self.says("Both edges are still there. `writes` now has 6 runs, not 7. `reads` still has 7.", 18)
        [open_] = D.open_runs(lost.events, "2026-09-14T09:00:00Z")
        self.assertEqual((open_["seconds since"], open_["usual seconds"]), (369000, 21))
        self.says("That is 369000 seconds before Monday 09:00, more than four days. The job's runs that ended took 21 seconds.", 18)
        self.assertEqual(self.week.warehouse.sql("SELECT revenue_pence FROM daily_sales WHERE day = '2026-09-09'"), [{"revenue_pence": 15375}])
        self.says("The row is there: 15375 pence for Wednesday 9.", 18)
        self.assertEqual((D.SEND_LAG, D.LATENCY, D.ACK_WAIT), (1, 2, 30))
        self.says("a program sends an event 1 second after the time the event records, and the collector receives it 2 seconds later", 18)
        self.says("It sends the event again if no acknowledgement comes within 30 seconds.", 18)
        [r] = D.send(self.week, lose=["remove_return COMPLETE"], at_least_once=True).retried()
        self.assertEqual((r["sendings"], r["received"], r["first arrival"]), (2, 1, "2026-09-12T16:50:37Z"))
        sendings = sorted(a.sent for a in D.send(self.week, lose_ack=["remove_return COMPLETE"], at_least_once=True).arrivals if a.event["job"]["name"] == "remove_return" and a.event["eventType"] == "COMPLETE")
        self.assertEqual(sendings, ["2026-09-12T16:50:05Z", "2026-09-12T16:50:35Z"])
        self.says("The program sent it at 16:50:05. No acknowledgement came, so it sent it again at 16:50:35, 30 seconds later.", 18)
        self.says("The collector received it once, at 16:50:37.", 18)
        [r] = D.send(self.week, lose_ack=["remove_return COMPLETE"], at_least_once=True).retried()
        self.assertEqual((r["first arrival"], r["last arrival"]), ("2026-09-12T16:50:07Z", "2026-09-12T16:50:37Z"))
        self.says("the `COMPLETE` is sent twice and received twice: at 16:50:07 and at 16:50:37", 18)
        self.says("The export sends no events (Chapter 13).", 18)
        lost_once = D.send(self.week, lose=["remove_return COMPLETE"])
        self.assertEqual(list(self.graph(lost_once.events).of("shop/remove_return")), [])
        self.assertEqual([r["job"] for r in self.graph(lost_once.events).of("returns") if r["edge"] == "writes"], ["shop/record_return"])
        self.says("The graph now shows `record_return` as the only program that writes `returns`.", 18)
        [o] = D.open_runs(lost_once.events, "2026-09-14T09:00:00Z")
        self.assertEqual((o["started"], o["usual seconds"]), ("2026-09-12T16:50:02Z", None))

    def test_chapter_19(self):
        D, I = self.D, self.I
        twice = D.send(self.week, lose_ack=["build_daily_sales COMPLETE 2026-09-10"], at_least_once=True)
        self.assertEqual(len(twice.events), 69)
        once = D.send(self.week)
        self.assertEqual(self.graph(twice.events).by_job, self.graph(once.events).by_job)
        self.assertEqual([(r["edge"], r["runs"]) for r in self.graph(twice.events).of("shop/build_daily_sales")], [("reads", 7), ("writes", 7)])
        self.says("The collector received 69 events, 1 more than the 68 sent.", 19)
        self.says("`reads` `clean_orders` in 7 runs, and `writes` `daily_sales` in 7 runs", 19)
        retimed = D.send(self.week, lose_ack=["build_daily_sales COMPLETE 2026-09-10"], at_least_once=True, restamp=True)
        [run] = [r for r in I.objects(I.normalise(retimed.events)).runs.values() if r["job"].endswith("build_daily_sales") and r["started"].startswith("2026-09-10")]
        self.assertEqual(run["ended"], "2026-09-10T02:30:52Z")
        self.says("The run early on Thursday 10 started at 02:30:00 and now ends at 02:30:52. Runs of `build_daily_sales` take 21 seconds. This one seems to take 52 seconds.", 19)
        [d] = I.dedupe(retimed.events, "run").dropped
        self.assertEqual((d["event time"][11:19], d["kept event time"][11:19]), ("02:30:52", "02:30:21"))
        self.says("By run, one event is dropped: the `COMPLETE` with the time 02:30:52. The event kept has the time 02:30:21.", 19)
        self.assertEqual(I.dedupe(retimed.events, "content").dropped, [])
        ended = lambda events: [r["ended"] for r in I.objects(I.normalise(events)).runs.values() if r["job"].endswith("build_daily_sales") and r["started"].startswith("2026-09-10")]
        self.assertEqual((ended(I.dedupe(retimed.events, "content")), ended(I.dedupe(retimed.events, "run"))), (["2026-09-10T02:30:52Z"], ["2026-09-10T02:30:21Z"]))
        self.says("The run early on Thursday 10 still ends at 02:30:52.", 19)
        self.says("In the cell below it, the run early on Thursday 10 ends at 02:30:21 again.", 19)
        self.says("So `record_return` starts twice for the one change, 25 seconds apart.", 19)
        side = I.edges_side_by_side("shop/record_return", label="notice", once=D.week_events(self.week), twice=D.week_events(shop.run_week(["returns", "twice"])))
        runs = {(r["notice"], r["edge"], r["dataset"].rsplit("/", 1)[-1]): r["runs"] for r in side}
        self.assertEqual((runs[("once", "writes", "shop.analytics.returns")], runs[("twice", "writes", "shop.analytics.returns")]), (5, 6))
        self.assertEqual((runs[("once", "reads", "r-202.json")], runs[("twice", "reads", "r-202.json")]), (2, 3))
        self.says("In the lineage, `record_return` now writes `returns` in 6 runs, not 5.", 19)
        self.says("It reads `r-202.json` in 3 runs, not 2.", 19)

    def test_chapter_20(self):
        D, I = self.D, self.I
        late = D.send(self.week, delay={"build_daily_sales COMPLETE 2026-09-09": 26 * 3600})
        times = {(r["type"], r["event time"]): r["arrived"] for r in late.received() if r["job"] == "build_daily_sales"}
        self.assertEqual(times[("COMPLETE", "2026-09-09T02:30:21Z")], "2026-09-10T04:30:24Z")
        self.assertEqual(times[("COMPLETE", "2026-09-10T02:30:21Z")], "2026-09-10T02:30:24Z")
        self.says("Wednesday 9's `COMPLETE` arrived at 04:30:24 on Thursday 10, after Thursday 10's, which arrived at 02:30:24.", 20)
        self.says("is held up for 26 hours on its way to the collector. Every other event takes 2 seconds.", 20)
        self.assertEqual(D.LATENCY, 2)
        seen = I.normalise(late.until("2026-09-10T09:00:00Z"))
        self.assertEqual([r["run ended"] for r in I.objects(seen, order="arrival").last_write("daily_sales")], ["2026-09-09T02:30:21Z"])
        self.assertEqual([r["run ended"] for r in I.objects(seen, order="event").last_write("daily_sales")], ["2026-09-10T02:30:21Z"])
        shorter = D.send(self.week, delay={"build_daily_sales COMPLETE 2026-09-09": 20 * 3600})
        self.assertIn({"arrived": "2026-09-09T22:30:24Z", "job": "build_daily_sales", "type": "COMPLETE", "event time": "2026-09-09T02:30:21Z"}, shorter.received(job="build_daily_sales", type="COMPLETE"))
        self.assertEqual([r["run ended"] for r in I.objects(I.normalise(shorter.until("2026-09-10T09:00:00Z")), order="arrival").last_write("daily_sales")], ["2026-09-10T02:30:21Z"])
        self.says("Wednesday 9's `COMPLETE` now arrives at 22:30:24 on Wednesday 9, before Thursday 10's. By arrival, the last write is Thursday's run again, ended at 02:30:21 on Thursday 10.", 20)
        self.says("By event time, the run that last wrote `daily_sales` ended at 02:30:21 on Thursday 10.", 20)
        self.says("By arrival, it ended at 02:30:21 on Wednesday 9: a day earlier.", 20)
        early = D.send(self.week, delay={"build_daily_sales START 2026-09-09": 60})
        times = {(r["type"], r["event time"]): r["arrived"] for r in early.received() if r["job"] == "build_daily_sales"}
        self.assertEqual((times[("START", "2026-09-09T02:30:00Z")], times[("COMPLETE", "2026-09-09T02:30:21Z")]), ("2026-09-09T02:31:03Z", "2026-09-09T02:30:24Z"))
        self.says("It arrives at 02:31:03, after its own `COMPLETE`, which arrived at 02:30:24.", 20)
        [r] = I.objects(I.normalise(early.events), order="arrival").runs_of(state="START", columns=["started", "ended"])
        self.assertEqual((r["started"], r["ended"]), ("2026-09-09T02:30:00Z", "2026-09-09T02:30:21Z"))
        self.says("The run early on Wednesday 9 has an end time of 02:30:21, and its state is `START`.", 20)
        held = D.send(shop.run_week(["returns", "withdrawn"]), delay={"record_return START 2026-09-13": 12 * 3600, "record_return COMPLETE 2026-09-13": 12 * 3600})
        self.assertIn("2026-09-14T09:15:05Z", [r["arrived"] for r in held.received() if r["job"] == "record_return"])
        self.says("They arrive at 09:15 on Monday 14, after the events of the `remove_return` run at 08:50.", 20)
        self.says("By event time, its last change is `deleted`, at 08:50:02 on Monday 14", 20)

    def test_chapter_21(self):
        C = self.C
        held = C.claims("2026-09-14T18:00:00Z")
        self.assertEqual(len(held), 5)
        self.says("There are five claims.", 21)
        self.assertEqual((C.CATALOGUE_SYNC, C.SHEET_IMPORT, C.RECORDS_CHANGED[11:16], C.SHEET_EDITED[:10]), ("03:30", "04:00", "16:40", "2026-08-28"))
        self.says("Nobody has edited it since 28 August. It is imported every night at 04:00", 21)
        self.says("its catalogue, read every night at 03:30", 21)
        self.assertEqual(C.TABLE_ALTERED[11:], "02:30:21Z")
        self.says("The warehouse's content changes every night, at 02:30:21", 21)
        tuesday = C.claims("2026-09-15T09:00:00Z")
        chosen = lambda rule, held=tuesday: {r["attribute"]: r["value"] for r in C.resolve(held, rule)}
        self.assertEqual(chosen("newest"), {"columns": "day, revenue", "owner": "data team"})
        self.assertEqual(chosen("as of"), {"columns": "day, revenue_pence", "owner": "etl_service"})
        self.assertEqual(chosen("ranked"), {"columns": "day, revenue_pence", "owner": "j.marsh"})
        self.assertEqual(len(C.resolve(tuesday, "all")), 5)
        self.assertEqual({r["source"]: r["sent"] for r in tuesday}, {"team sheet": "2026-09-15T04:00:00Z", "warehouse": "2026-09-15T03:30:00Z", "records": "2026-09-14T16:40:00Z"})
        self.says("The team sheet's claims were sent at 04:00 on Tuesday 15, the warehouse's at 03:30, and your records' at 16:40 on Monday 14.", 21)
        self.says("The owner is `etl_service` and the columns are `day, revenue_pence`, both from the warehouse.", 21)
        self.assertEqual(chosen("ranked", C.claims("2026-09-14T12:00:00Z"))["owner"], "data team")
        self.says("At 12:00 on Monday 14, before your records were sent, `ranked` gave the owner `data team`, from the team sheet.", 21)
        self.says("The cell lists every claim the shop holds, with its source and its two times: five rows.", 21)

    def test_chapter_22(self):
        A = self.A
        self.assertEqual([len(A.merge(r)) for r in A.RULES], [6, 5, 1, 3])
        self.says("Under that rule, all six become one entity.", 22)
        self.says("The result has five entities.", 22)
        self.says("The result has three entities. One of them holds four references", 22)

    def test_chapter_23(self):
        S = self.S
        [m] = S.measure(self.week)
        self.says("The week holds 11 assets, 6 jobs, 34 runs, 68 events, 67 edges by run and 14 edges by job, over 7 days. An event takes 1492 bytes on average.", 23)
        self.assertEqual((m["assets"], m["events"], m["bytes per event"]), (11, 68, 1492))
        self.assertEqual(round(m["events"] / m["days"] / m["assets"], 1), 0.9)
        self.says("about 0.9 events per asset per day", 23)
        top = S.reach(self.week)
        self.assertEqual([(r["edges followed"], r["share"]) for r in top[:2]], [(6, 0.43), (4, 0.29)])
        self.says("From `orders.jsonl`, a traversal downstream follows 6 of the 14 edges by job: 0.43, the widest share. From `clean_orders`, it follows 4: 0.29.", 23)
        self.assertEqual((S.FANOUT, S.FANOUT ** S.DEPTH), (3, 81))
        self.says("so 4 steps follow at most 81 edges", 23)
        self.assertEqual((S.BUDGET, S.RETENTION_DAYS, S.DEPTH, S.SIZES[-1]), (1_000_000, 90, 4, 10_000_000))
        self.says("pass the limit first, at 100,000 assets", 23)
        self.says("the latest run reads 31 records at 10,000,000 assets: about 30 steps down the index, then one record", 23)
        self.says("At 10,000,000 assets, the projection holds 794,805,210 events.", 23)
        self.says("The output shows 68 events, of which 28 are kept.", 23)
        self.says("`record_return` reads it, in 1 run, first and last at 14:20:05 on Tuesday 8", 23)
        events = self.D.week_events(self.week)
        found = lambda now: self.I.edges(self.I.objects(self.I.normalise(S.retain(events, 90, now)))).by_run
        self.assertEqual((len(S.lineage_of(found("2026-12-07T14:20:00Z"), "r-201.json")), len(S.lineage_of(found("2026-12-07T14:21:00Z"), "r-201.json"))), (1, 0))
        self.says("With 90 days, that run's events would be deleted after 14:20 on Monday 7 December.", 23)
        self.assertEqual([r["return_id"] for r in self.week.warehouse.sql("SELECT return_id FROM returns WHERE return_id = 'r-201'")], ["r-201"])


class TheWordsOfPartVI(unittest.TestCase):
    """Chapters 24 to 28: every number the prose states about the reader's pieces, computed again."""

    def says(self, phrase: str, chapter: int) -> None:
        self.assertIn(flat(phrase), flat(TEXT[chapter]))

    @staticmethod
    def pieces(module, which, names):
        ns = {"shop": shop}
        for name in names:
            exec((module.STUBS if which == "stub" else module.REFERENCE)[name], ns)
        return ns

    def test_chapter_24(self):
        from shop import store as S

        week = shop.run_week(["returns"])
        self.assertEqual((len(S.documents(week)), len(S.expected(week))), (17, 11))
        stub = S.check(week, S.documents(week), self.pieces(S, "stub", ["documents"])["readers_of"])
        ref = S.check(week, S.documents(week), self.pieces(S, "reference", ["documents"])["readers_of"])
        self.assertEqual((stub.right, ref.right, ref.read), (3, 11, 187))
        self.says("As it stands, the check below it finds 3 of 11 datasets right: the 3 that no program reads.", 24)
        self.says("With the loop changed, the check finds 11 of 11 datasets right. The loop reads 187 documents: all 17 documents for each of the 11 datasets.", 24)
        table = S.check(week, S.tables(week), self.pieces(S, "reference", ["tables"])["query"])
        self.assertEqual((table.right, table.read), (11, 154))
        self.says("154 rows, 14 for each of the 11 datasets", 24)
        tables = S.tables(week)
        exec(S.REFERENCE["index"], {"tables": tables})
        self.assertEqual(S.check(week, tables, self.pieces(S, "reference", ["tables"])["query"]).read, 14)
        self.says("With the index on `dataset`, the query reads 14 rows in all", 24)
        graph = S.check(week, S.graph(week), self.pieces(S, "stub", ["graph"])["readers_of"])
        self.assertEqual(graph.right, 6)
        self.says("the check finds 6 of 11 right", 24)
        self.says("What reads `clean_orders`: 17 documents, 2 rows of the table, 2 edges of the graph.", 24)
        self.says("What `build_daily_sales` reads: 1 document, 14 rows of the table, 2 edges of the graph.", 24)

    def test_chapter_25(self):
        from shop import collector as C

        week = shop.run_week(["returns"])
        self.assertEqual(len(C.faults(week)), 5)
        self.says("The next cell lists the 5 arrivals the faults touch", 25)
        counts = []
        for key, newer in (("stub", "stub"), ("reference", "stub"), ("reference", "reference")):
            ns = {"shop": shop}
            exec((C.STUBS if key == "stub" else C.REFERENCE)["key"], ns)
            exec((C.STUBS if newer == "stub" else C.REFERENCE)["newer"], ns)
            counts.append(C.check(week, ns["key"], ns["newer"]).passed)
        self.assertEqual(counts, [2, 4, 5])
        self.says("As the cells stand, 2 of 5 pass", 25)
        self.says("4 of 5 pass", 25)
        self.says("5 of 5 pass", 25)
        ns = self.pieces(C, "reference", ["key", "newer"])
        exec(C.STUBS["start"], ns)
        restarted = C.run(week, ns["key"], ns["newer"], ns["start"])
        self.assertEqual((C.check(week, ns["key"], ns["newer"], ns["start"]).passed, len(restarted.file)), (4, 69))
        self.says("the check shows 4 of 6 passing", 25)
        self.assertEqual(C.RESTART, "2026-09-12T16:50:20Z")
        self.says("the collector restarts on Saturday 12 at 16:50:20", 25)

    def test_chapter_26(self):
        from shop import lineage_graph as L

        week = shop.run_week(["returns", "source"])
        self.assertEqual(len(L.stored(week)), 82)
        self.says("82 events", 26)
        self.assertEqual(L.check(week, self.pieces(L, "stub", ["add"])["add"]).passed, 2)
        self.says("As `add` stands, 2 pass.", 26)
        graph = L.build(week, self.pieces(L, "reference", ["add"])["add"])
        rows = {r["dataset"].rsplit("/", 1)[-1]: (r["runs"], r["first"], r["last"]) for r in L.table(graph, "build_daily_sales")}
        self.assertEqual(rows["shop.analytics.clean_orders"], (5, "2026-09-08T02:30:00Z", "2026-09-12T02:30:21Z"))
        self.assertEqual(rows["clean_orders_copy.csv"], (2, "2026-09-13T02:30:00Z", "2026-09-14T02:30:21Z"))
        self.says("`build_daily_sales` reads `clean_orders` in 5 runs, first at 02:30:00 on Tuesday 8 and last at 02:30:21 on Saturday 12.", 26)

    def test_chapter_27(self):
        from shop import query as Q

        week = shop.run_week(list(Q.WEEK))
        self.assertEqual(Q.check_downstream(week, self.pieces(Q, "stub", ["downstream"])["downstream"]).passed, 1)
        ns = self.pieces(Q, "reference", ["downstream"])
        self.assertEqual(sorted(ns["downstream"](Q.graph(week), "orders.jsonl")), ["clean_orders", "clean_orders_copy.csv", "daily_sales", "sales_dashboard"])
        self.says("Downstream of `orders.jsonl` are `clean_orders`, `clean_orders_copy.csv`, `daily_sales` and `sales_dashboard`.", 27)
        stale = [r["asset"] for r in shop.observe.freshness(week) if r["hours before"] > 24]
        self.assertEqual(stale, ["daily_sales", "returns"])
        dash = next(r for r in shop.observe.freshness(week) if r["asset"] == "sales_dashboard")
        self.assertEqual((dash["last written"], dash["hours before"], dash["latest day"]), ("2026-09-14T03:00:09Z", 6.0, "2026-09-12"))
        self.says("it was last written at 03:00:09 on Monday 14, 6 hours before. Its latest day is Saturday 12", 27)

    def test_chapter_28(self):
        from shop import interface as I

        self.assertEqual((I.writers("daily_sales"), len(I.runs())), (["shop/build_daily_sales"], 41))
        self.says("The file holds 41 runs in all.", 28)
        self.assertEqual(len(self.pieces(I, "stub", ["run_history"])["run_history"]("daily_sales")), 6)
        self.assertEqual(len(self.pieces(I, "reference", ["run_history"])["run_history"]("daily_sales")), 7)
        self.says("The check finds 6 runs, and not Monday's.", 28)
        self.says("The check finds 7 runs, the `FAIL` among them.", 28)
        self.assertEqual(len(I.SECTIONS), 7)


class TheWordsOfPartIV(unittest.TestCase):
    """Chapters 14 to 17: every number and run the prose states, computed again."""

    @classmethod
    def setUpClass(cls):
        from shop import cause, impact, provenance, quality

        cls.Q, cls.P, cls.I, cls.C = quality, provenance, impact, cause
        cls.week = shop.run_week()

    def says(self, phrase: str, chapter: int) -> None:
        self.assertIn(flat(phrase), flat(TEXT[chapter]))

    def test_chapter_14_the_counts(self):
        m = self.Q.measurements(self.week, "orders.jsonl")
        self.assertEqual((m[0]["rows"], m[-1]["rows"]), (6, 48))
        self.says("6 rows on Tuesday 8, 48 on Monday 14", 14)
        self.assertEqual([r["night"] for r in m if r["order_id twice"] == 1][0], "2026-09-10")
        self.assertEqual([r["night"] for r in m if r["no customer_id"] == 3][0], "2026-09-11")
        self.assertEqual({r["quantity 0 or less"] for r in m}, {0})
        self.says("From Thursday 10, `order_id twice` is 1: one order appears twice in the file", 14)
        self.says("From Friday 11, `no customer_id` is 3: Thursday's three orders with no customer id", 14)

    def test_chapter_14_the_assertions(self):
        table = self.Q.check(self.week, "clean_orders", "no customer_id")
        self.assertEqual((len(table), {r["passed"] for r in table}), (7, {"yes"}))
        self.says("It passed on all 7 runs.", 14)
        self.assertIn("customer_id IS NOT NULL", shop.week.CLEAN_ORDERS)
        failed = [r["night"] for r in self.Q.check(self.week, "orders.jsonl", "no customer_id") if r["passed"] == "no"]
        self.assertEqual(failed, ["2026-09-11", "2026-09-12", "2026-09-13", "2026-09-14"])
        self.says("On `orders.jsonl`, 4 runs fail: Friday 11, Saturday 12, Sunday 13 and Monday 14, each with a count of 3.", 14)
        r = {x["night"]: x for x in self.Q.reconcile(self.week)}
        self.assertEqual((r["2026-09-10"]["rows read"], r["2026-09-10"]["rows written"], r["2026-09-10"]["left out"]), (20, 19, 0))
        self.assertEqual(tuple(r["2026-09-11"][k] for k in ("rows read", "rows written", "repeats", "left out")), (27, 23, 1, 3))
        self.says("On Friday 11: 27 read, 23 written, 1 repeat, 3 left out.", 14)
        self.assertEqual([x["met"] for x in self.Q.readings(self.week)], ["no", "yes", "no"])
        self.assertEqual(list(self.Q.left_out(self.week)), [{"day": "2026-09-10", "orders": 3, "pence": 15400}])
        self.says("Thursday's total leaves out 3 completed orders, worth 15400 pence", 14)
        f = self.Q.facets(self.week, "run-014")
        self.assertEqual((f["facets"]["dataQualityMetrics"]["rowCount"], f["facets"]["dataQualityMetrics"]["columnMetrics"]["order_id"]["distinctCount"]), (27, 26))
        self.says("`rowCount` is 27.", 14)
        self.says("For `order_id`, `distinctCount` is 26: the 27 rows less the 1 repeat.", 14)

    def test_chapter_15_thursday(self):
        steps = self.P.trace(self.week, "2026-09-10")
        self.assertEqual([r["made by"] for r in steps[:3]], ["run-028, refresh_dashboard", "run-015, build_daily_sales", "run-026, build_clean_orders"])
        self.assertEqual((steps[2]["rows"], steps[3]["rows"], {r["pence"] for r in steps}), ("7020, 7022, 7024, 7026", "lines 21, 23, 25, 27", {5150}))
        self.says("Lines 21, 23, 25 and 27 of `orders.jsonl`, in the version the export wrote at 01:00:41 on Friday 11.", 15)
        self.says("The table was last written by `run-026` early on Monday 14.", 15)
        self.says("Each step adds up to 5150 pence.", 15)
        left = [r for r in self.P.trace(self.week, "2026-09-10", dropped=True) if r["asset"].startswith("left out")]
        self.assertEqual([r["rows"][:19] for r in left], ["line 22, order 7021", "line 24, order 7023", "line 26, order 7025"])
        self.assertEqual(sum(r["pence"] for r in left), 15400)
        self.says("With `dropped=True`, three more rows list lines 22, 24 and 26 of the same version of `orders.jsonl`", 15)

    def test_chapter_15_sunday(self):
        week = shop.run_week(["corrected"])
        steps = self.P.trace(week, "2026-09-13")
        self.assertEqual([r["pence"] for r in steps], [6925, 6925, 9775, -1425, 9775])
        self.assertEqual(steps[1]["made by"], "run-034, build_daily_sales")
        self.says("8350 is not 6925.", 15)
        read = self.P.trace(week, "2026-09-13", as_read=True)
        self.assertEqual((read[3]["made by"], read[3]["pence"]), ("run-031", -2850))
        self.says("9775 less 2850 is 6925", 15)
        self.assertEqual([(v["at"], v["quantity"]) for v in self.P.object_versions(week, "r-205")], [("2026-09-13T18:10:00Z", 2), ("2026-09-14T08:40:00Z", 1)])
        from shop.runs import executions

        [run] = [e for r, e in executions(week) if r == "run-034"]
        self.assertEqual(run.started, "2026-09-14T02:30:00Z")

    def test_chapter_16_the_rename(self):
        w0 = shop.run_week(["copy"])
        down = self.I.downstream(w0, "clean_orders")
        self.assertEqual([(r["step"], r["program"]) for r in down], [(1, "copy_clean_orders"), (1, "build_daily_sales"), (2, "refresh_dashboard")])
        cols = self.I.downstream_columns(w0, "clean_orders", "customer_id")
        self.assertEqual(len(cols), 1)
        status = {r["column"] for r in self.I.downstream_columns(w0, "clean_orders", "status")}
        self.assertTrue({"daily_sales.day", "daily_sales.revenue_pence", "sales_dashboard.day", "sales_dashboard.revenue_pence"} <= status)
        got = {r["output"]: r for r in self.I.readers(w0, shop.run_week(["copy", "customer"]))}
        self.assertEqual(got["daily_sales"]["after"], "7 rows, 100798 pence")
        self.assertEqual(got["Jo Marsh's query result"]["before"], "7 rows, 41 orders")
        self.says("7 rows, 100798 pence", 16)
        self.says("before, 7 rows, one for each country, 41 orders; after, the error `no such column: o.customer_id`.", 16)
        self.assertEqual(len(w0.warehouse.sql("SELECT DISTINCT country FROM clean_customers")), 7)

    def test_chapter_16_the_withdrawn_return(self):
        week = shop.run_week(["withdrawn"])
        made = self.I.made_from(week, "r-206")
        self.assertEqual([r["by"] for r in made[:2]], ["run-031, record_return", "run-034, build_daily_sales"])
        [row] = week.warehouse.sql("SELECT revenue_pence FROM daily_sales WHERE day = '2026-09-13'")
        self.assertEqual(row["revenue_pence"], 8575)
        self.says("It holds 8575 pence, and Sunday's five orders add up to 9775 pence.", 16)
        self.assertEqual({v["day"]: v["revenue"] for v in week.reporting.dashboard()["values"]}["2026-09-13"], "£85.75")
        self.says("The dashboard still shows £85.75 for Sunday 13.", 16)

    def test_chapter_17_the_searches(self):
        thu = self.C.search(self.week, "2026-09-10")
        self.assertEqual([r["pence"] for r in thu[:4]], [5150, 5150, 5150, 20550])
        self.assertEqual(thu[2]["made by"], "run-014, build_clean_orders")
        self.says("holds 20550 pence", 17)
        week = shop.run_week(["refunds"])
        sat = self.C.search(week, "2026-09-12")
        self.assertEqual(([r["pence"] for r in sat[:3]], sat[1]["made by"]), ([21549, 21549, 19149], "run-023, build_daily_sales"))
        self.says("21549 pence, where `clean_orders` holds 19149 for Saturday", 17)
        [o] = week.warehouse.sql("SELECT quantity, price_pence, status FROM clean_orders WHERE order_id = 7037")
        self.assertEqual((o["quantity"], o["quantity"] * o["price_pence"], o["status"]), (2, 2400, "cancelled"))
        self.says("Saturday's cancelled order 7037, 2 pairs of brake pads, 2400 pence", 17)
        tue = self.C.search(week, "2026-09-08")
        self.assertEqual({r["pence"] for r in tue[:4]}, {16225})
        self.says("16225 pence at every step", 17)
        [c] = week.warehouse.sql("SELECT status FROM clean_orders WHERE order_id = 7009")
        self.assertEqual(c["status"], "cancelled")


class TheWordsOfChapter13(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from shop import observe

        cls.O = observe
        cls.text = flat(TEXT[13])

    def says(self, phrase: str) -> None:
        self.assertIn(flat(phrase), self.text)

    def test_the_failed_night(self):
        week = shop.run_week(["failed"])
        obs = self.O.observations(week)
        self.assertEqual(len(obs), 28)
        [failed] = [r for r in obs if r["status"] == "failed"]
        self.assertEqual((failed["run"], failed["program"], failed["started"], failed["seconds"], failed["error"], failed["rows written"]), ("run-027", "build_daily_sales", "2026-09-14T02:30:00Z", 21, "database is locked", None))
        self.says("One failed: `run-027`, `build_daily_sales`, at 02:30 on Monday 14, after 21 seconds, with the error `database is locked`.")
        [after] = [r for r in obs if r["run"] == "run-028"]
        self.assertEqual((after["program"], after["status"], after["rows read"], after["rows written"]), ("refresh_dashboard", "succeeded", 6, 6))
        f = {r["asset"]: (r["hours before"], r["latest day"]) for r in self.O.freshness(week)}
        self.assertEqual(f, {"orders.jsonl": (8.0, "2026-09-13"), "clean_orders": (6.9, "2026-09-13"), "daily_sales": (30.5, "2026-09-12"), "sales_dashboard": (6.0, "2026-09-12")})
        self.says("By the time it was last written, the dashboard is the most recent of the four: 6.0 hours before 09:00 on Monday.")
        self.assertEqual([r["met"] for r in self.O.readings(week)], ["yes", "no", "no"])
        self.says("The second and third readings are not met.")
        self.says("`daily_sales` was last written at 02:30:21 on Sunday 13, before `clean_orders` was, at 02:05:52 on Monday 14.")

    def test_a_night_that_wrote_nothing(self):
        week = shop.run_week(["renamed"])
        empty = [r for r in self.O.observations(week) if r["rows written"] == 0]
        self.assertEqual(len(empty), 4)
        self.assertEqual([r["met"] for r in self.O.readings(week)], ["yes", "yes", "no"])
        self.assertEqual(self.O.latest_day(week, "sales_dashboard"), "2026-09-11")
        self.says("The dashboard's latest day is Friday 11, two days before Sunday 13.")
        rows = {r["started"][:10]: (r["rows read"], r["rows written"]) for r in self.O.observations(week) if r["program"] == "build_clean_orders"}
        self.assertEqual((rows["2026-09-12"][1], rows["2026-09-13"], rows["2026-09-14"]), (31, (43, 0), (48, 0)))
        self.says("`build_clean_orders` read 43 rows and then 48, and wrote 0 each time. On Saturday 12 it had written 31.")

    def test_two_clocks_and_a_table_written_at_any_hour(self):
        week = shop.run_week(["clock"])
        self.assertEqual(self.O.last_written(week, "sales_dashboard"), "2026-09-14T02:20:09Z")
        self.assertEqual(self.O.last_run(week, "sales_dashboard"), "2026-09-14T03:00:09Z")
        self.assertIn('by="stores"', SOURCE[13])
        self.says("The reporting tool records the dashboard's last refresh at 02:20:09 on Monday. `daily_sales` was last written at 02:30:21.")
        week = shop.run_week(["returns"])
        [r] = [r for r in self.O.freshness(week) if r["asset"] == "returns"]
        self.assertEqual((r["last written"], r["hours before"]), ("2026-09-12T16:50:04Z", 40.2))
        self.assertEqual(self.O.source_changed(week), "2026-09-12T16:50:00Z")
        self.says("`returns` was last written at 16:50:04 on Saturday 12, 40.2 hours before 09:00 on Monday.")
        self.says("The table was written 4 seconds later.")


class TheWordsAboutThePage(unittest.TestCase):
    """The menu of changes offers the engine's changes. Each page's warning states what was measured
    on the pages; test_jupyterlite.py checks it against docs/notes/notebook-prototype.md."""

    def test_the_menu_offers_the_engines_changes(self):
        [menu] = [
            n
            for n in ast.walk(ast.parse(SOURCE[2]))
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr == "dropdown"
        ]
        options = ast.literal_eval(next(k.value for k in menu.keywords if k.arg == "options"))
        self.assertEqual(list(options.values()), [[], ["copy"], ["refunds"], ["failed"]])
        self.assertEqual([c for v in options.values() for c in v], list(shop.CHANGES[:3]))
        self.assertEqual(
            list(options),
            [
                "The shop stays as it is",
                "An analyst copies clean_orders every night",
                "From Saturday, the daily_sales job keeps unrefunded orders",
                "The daily_sales job fails on the last night",
            ],
        )


class TheWordsKeepTheRules(unittest.TestCase):
    """The writing standard's checkable parts (AGENTS.md, scripts/prose.mjs, CLAUDE.md)."""

    def learner_text(self, *chapters: int) -> list[str]:
        # The markdown, and every string with a space in it: labels, options, placeholders. Code
        # identifiers and SQL keywords are not prose, and SQL has no prohibited phrase.
        return [
            t
            for chapter in chapters or CHAPTERS
            for t in CELLS[chapter]
            + [s for s in strings(chapter) if " " in s and not s.lstrip().upper().startswith(("SELECT", "\n"))]
        ]

    def test_no_prohibited_phrase(self):
        source = (ROOT / "scripts" / "prose.mjs").read_text(encoding="utf-8")
        phrases = re.findall(r'phrase: "([^"]+)"', source) + ["the lab ", "the lab's", "Metadata Lab"]
        self.assertGreater(len(phrases), 10)
        found = [(p, t[:60]) for t in self.learner_text() for p in phrases if p.lower() in t.lower()]
        self.assertEqual(found, [])

    def test_no_filler(self):
        # CLAUDE.md, "Silence is preferable to filler": the forms the author named, as
        # apps/course/src/strings.test.ts holds the front page to them.
        filler = [
            r"\byou have (what you need|everything)\b",
            r"\beverything (is )?in place\b",
            r"\bnow you can (begin|start)\b",
            r"\bwhere things get interesting\b",
            r"\basks nothing of you\b",
            r"\bkept to hand\b",
            r"\b(is|are) (quietly )?waiting\b",
            r"\bquietly\b",
            r"\byou (have been|were) told\b",
            r"\b(as )?you already know\b",
            r"\blet's\b",
        ]
        found = [(f, t[:60]) for t in self.learner_text() for f in filler if re.search(f, t, re.I)]
        self.assertEqual(found, [])

    def test_no_em_dash_and_no_placeholder(self):
        self.assertEqual([t[:60] for t in self.learner_text() if "—" in t], [])
        for source in SOURCE.values():
            self.assertNotIn("[[", source)

    def test_terms_arrive_where_the_chapter_introduces_them(self):
        # Chapter 1 introduces "asset", Chapter 2 "metadata", at its "Records made at the time".
        # A link's address is not read: the course's address has "metadata" in it.
        chapter = [re.sub(r"\]\([^)]*\)", "]", c) for c in CELLS[1] + CELLS[2]]
        first = lambda word: next(i for i, c in enumerate(chapter) if re.search(rf"\b{word}", c, re.I))
        records = next(i for i, c in enumerate(chapter) if c.startswith("## Records made at the time"))
        self.assertGreaterEqual(records, len(CELLS[1]))
        self.assertEqual(first("metadata"), records)
        self.assertTrue(chapter[first("asset")].startswith("An asset is one thing the platform holds"))
        self.assertLess(first("asset"), len(CELLS[1]))
        # Chapter 3 introduces "descriptive", "operational" and "schema" where it sets the reader's
        # record beside what the systems record; Chapter 4 its four terms where it asks what the
        # records describe. Neither uses its terms before then, objectives included.
        for number, heading, words in (
            (3, "## What the platform keeps", ("descriptive", "operational", "schema")),
            (4, "## What the records describe", ("entity", "attribute", "identifier", "dataset")),
            (5, "## The records as a graph", ("node", "edge", "graph")),
            (5, "## Following edges", ("traversal",)),
            (6, "## Lineage", ("lineage",)),
            (6, "The cell above follows edges from `orders.jsonl`", ("downstream", "upstream")),
            (7, "## Events", ("event",)),
            (8, "## A form other programs can read", ("OpenLineage",)),
            (8, "The first event's `eventType`", ("namespace", "producer", "facet")),
            (9, "## From events to a graph", ("ingestion",)),
            (9, "## Normalise", ("normalise",)),
            (10, "Lineage between columns", ("column lineage",)),
            (11, "## The schema over time", ("schema evolution",)),
            (11, "Compare the counts with what you wrote.", ("breaking change",)),
            (12, "## A run in development", ("environment",)),
            (12, "## The same asset?", ("identity",)),
            (12, "In pair 1, both names refer", ("qualified name",)),
            (13, "## What each run recorded", ("observation",)),
            (13, "## How recent each asset is", ("freshness",)),
            (14, "The file grows each night", ("data quality",)),
            (14, "## A test on every run", ("assertion",)),
            (15, "Thursday's total goes back through four steps", ("provenance",)),
            (16, "Step 1 is the programs", ("impact analysis",)),
            (17, "## Two causes", ("root cause",)),
            (18, "## From the programs to the collector", ("collector", "delivery")),
            (18, "The open run of `remove_return`", ("at least once",)),
            (19, "The run early on Thursday 10 started at 02:30:00", ("deduplication",)),
            (19, "Change `\"content\"` to `\"run\"`", ("idempotent",)),
            (20, "## Two times", ("event time", "arrival time")),
            (21, "The team sheet's claims were sent at 04:00 on Tuesday 15", ("precedence",)),
            (22, "Under that rule, all six become one entity.", ("entity resolution",)),
            (22, "## What each system states", ("alias",)),
            (23, "The two questions that read every stored event", ("index", "partition")),
            (23, "## Keeping less", ("retention",)),
            (23, "The row is still in `returns`.", ("compaction",)),
        ):
            # The chapter's title is the plan's, and may name its term ("Metadata as a graph").
            cells = [re.sub(r"^# Chapter \d+: .*$", "", re.sub(r"\]\([^)]*\)", "]", c), flags=re.M) for c in CELLS[number]]
            home = next(i for i, c in enumerate(cells) if c.startswith(heading))
            for word in words:
                found = next(i for i, c in enumerate(cells) if re.search(rf"\b{word}", c, re.I))
                self.assertEqual(found, home, (number, word))
                self.assertIn(f"**{word}**", cells[home], (number, word))

    def test_no_term_of_a_later_chapter(self):
        # The course's term gate (content/plan/plan.ts), chapter by chapter, with the course's
        # one exemption: "run" as the verb (run a cell); the noun arrives in Chapter 7.
        plan = (ROOT / "content" / "plan" / "plan.ts").read_text(encoding="utf-8")
        terms = {
            term: int(number)
            for number, introduces in re.findall(r'C\((\d+), \d+, "[^"]+"(?:, \[([^\]]*)\])?\)', plan)
            for term in re.findall(r'"([^"]+)"', introduces or "")
        }
        self.assertGreater(len(terms), 40)
        self.assertEqual((terms["asset"], terms["metadata"], terms["run"]), (1, 2, 7))
        # A second exemption, at the author's decision of 12 October 2026: Chapter 2's closing
        # paragraph names what later chapters build, "lineage" (Chapter 6) and a "run" of a job
        # (Chapter 7), once each, so a reader sees where the course goes. Nowhere else.
        closing = re.compile(r"Chapter 3 starts making them:[^\n]*")
        [preview] = closing.findall(TEXT[2])
        self.assertEqual((len(re.findall(r"\blineage\b", preview)), len(re.findall(r"\beach run of a job\b", preview))), (1, 1))
        found = [
            (chapter, term, t[:60])
            for chapter in CHAPTERS
            for term, home in terms.items()
            if home > chapter and term != "run"
            for t in self.learner_text(chapter)
            if re.search(rf"\b{re.escape(term)}", closing.sub("", re.sub(r"\]\([^)]*\)", "]", t)), re.I)
        ]
        self.assertEqual(found, [])


if __name__ == "__main__":
    unittest.main()
