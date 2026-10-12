# Copyright © 2026 Christopher Snow

"""Every sentence of the notebooks that states a fact, pinned against the engine, and the prose rules.

Chapters 1 to 4 are a notebook each. Their words are their markdown cells and the labels in their
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
}
SOURCE = {chapter: path.read_text(encoding="utf-8") for chapter, path in CHAPTERS.items()}


def markdown_cells(chapter: int) -> list[str]:
    """The text of every `mo.md(...)` cell of a chapter, in the notebook's order."""
    out = []
    for node in ast.parse(SOURCE[chapter]).body:
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
        self.assertEqual(names, ["chapter_01.ipynb", "chapter_02.ipynb", "chapter_03.ipynb", "chapter_04.ipynb"])
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

    def test_each_chapter_opens_and_ends_with_the_way_back_to_the_course(self):
        # Relative links in a notebook open as files of the site, so the course's address is whole.
        nav = {
            1: "[Back to contents](https://snowch.github.io/metadata-systems/) · [Next: Chapter 2](chapter_02.ipynb)",
            2: "[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 1](chapter_01.ipynb) · [Next: Chapter 3](chapter_03.ipynb)",
            3: "[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 2](chapter_02.ipynb) · [Next: Chapter 4](chapter_04.ipynb)",
            4: "[Back to contents](https://snowch.github.io/metadata-systems/) · [Previous: Chapter 3](chapter_03.ipynb)",
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
        self.assertLess(holds.index("information_schema.columns WHERE table_name"), holds.index("The cells showed"))
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
        self.says('The requirement is: "Every table must have an owner." The warehouse records `etl_service` as the owner of all three tables.')

    def test_the_reconstruction_and_thursday(self):
        self.assertEqual(len(shop.queries_that_rebuild(self.week)), 1)
        self.assertEqual(len(self.w.sql("SELECT * FROM daily_sales")), 7)
        self.says("It reproduces `daily_sales` exactly, all seven rows.")
        gap = shop.day_gap(self.week, "2026-09-10")
        self.assertEqual((gap["left"], gap["left_pence"]), (3, 15400))
        self.says("It also explains Thursday.")

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
        count = "SELECT COUNT(DISTINCT value) AS owners FROM records WHERE attribute = 'responsible'"
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
        ):
            cells = [re.sub(r"\]\([^)]*\)", "]", c) for c in CELLS[number]]
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
