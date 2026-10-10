# Copyright © 2026 Christopher Snow

"""Every number Chapter 1's notebook states, read off the engine.

The same facts the TypeScript chapter's facts test pins, in pence: if the shop's data or programs
change, this fails until the words change with them. Run with `python3 -m unittest discover -s
notebook/tests -t notebook` from the repository root.
"""

import unittest

import shop
from shop import figures


class TheWeekAsItRan(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.week = shop.run_week()
        cls.w = cls.week.warehouse

    def test_seven_assets_in_three_systems(self):
        systems = figures.platform_assets(self.week)
        self.assertEqual([name for name, _ in systems], ["Object storage", "Warehouse", "Reporting tool"])
        self.assertEqual(
            [[a for a, _ in assets] for _, assets in systems],
            [
                ["customers.jsonl", "orders.jsonl", "products.csv"],
                ["clean_customers", "clean_orders", "daily_sales"],
                ["sales_dashboard"],
            ],
        )
        self.assertEqual(figures.tally(systems), "3 files + 3 tables + 1 dashboard = 7 assets")

    def test_row_counts(self):
        counts = {r["table_name"]: r["row_count"] for r in self.w.sql("SELECT * FROM information_schema.tables")}
        self.assertEqual(counts, {"clean_customers": 9, "clean_orders": 44, "daily_sales": 7})
        lines = {r["key"]: len(self.week.storage.records(r["key"])) for r in self.week.storage.ls()}
        self.assertEqual(
            lines,
            {"s3://shop-raw/customers.jsonl": 10, "s3://shop-raw/orders.jsonl": 48, "s3://shop-raw/products.csv": 8},
        )
        self.assertEqual(len(self.week.reporting.dashboard()["values"]), 7)

    def test_daily_sales_in_pence(self):
        rows = self.w.sql("SELECT day, revenue_pence, typeof(revenue_pence) AS t FROM daily_sales ORDER BY day")
        self.assertEqual(
            [(r["day"], r["revenue_pence"]) for r in rows],
            [
                ("2026-09-07", 14700),
                ("2026-09-08", 16225),
                ("2026-09-09", 15375),
                ("2026-09-10", 5150),
                ("2026-09-11", 20424),
                ("2026-09-12", 19149),
                ("2026-09-13", 9775),
            ],
        )
        self.assertTrue(all(r["t"] == "integer" for r in rows))
        shown = [v["revenue"] for v in self.week.reporting.dashboard()["values"]]
        self.assertEqual(shown, ["£147.00", "£162.25", "£153.75", "£51.50", "£204.24", "£191.49", "£97.75"])

    def test_raw_orders_against_daily_sales(self):
        raw = {}
        for o in self.week.storage.records(shop.FILES["orders"]):
            raw[o["ordered_at"][:10]] = raw.get(o["ordered_at"][:10], 0) + o["price_pence"] * o["quantity"]
        daily = {r["day"]: r["revenue_pence"] for r in self.w.sql("SELECT * FROM daily_sales")}
        self.assertEqual(raw["2026-09-10"], 20550)
        self.assertEqual(raw["2026-09-10"] - daily["2026-09-10"], 15400)
        same = [d for d in shop.DAYS if raw[d] == daily[d]]
        self.assertEqual(same, ["2026-09-07", "2026-09-11", "2026-09-13"])

    def test_the_record_of_daily_sales(self):
        [t] = self.w.sql("SELECT * FROM information_schema.tables WHERE table_name = 'daily_sales'")
        self.assertEqual(t["row_count"], 7)
        self.assertGreater(t["bytes"], 0)
        self.assertEqual(t["created"], "2026-09-01T10:20:00Z")
        self.assertEqual(t["last_altered"], "2026-09-14T02:30:21Z")
        self.assertEqual(t["table_owner"], "etl_service")
        cols = self.w.sql("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'daily_sales'")
        self.assertEqual([(c["column_name"], c["data_type"]) for c in cols], [("day", "DATE"), ("revenue_pence", "INTEGER")])

    def test_every_table_is_owned_by_the_account_four_programs_share(self):
        owners = {r["table_owner"] for r in self.w.sql("SELECT table_owner FROM information_schema.tables")}
        self.assertEqual(owners, {"etl_service"})
        programs = {e.writer for e in self.week.executions} - {"export"}
        self.assertEqual(programs, {"clean_customers", "clean_orders", "daily_sales", "dashboard_refresh"})

    def test_what_object_storage_and_the_reporting_tool_record(self):
        ls = {r["key"]: r for r in self.week.storage.ls()}
        self.assertEqual(set(ls["s3://shop-raw/orders.jsonl"]), {"key", "size_bytes", "last_modified"})
        self.assertEqual(ls["s3://shop-raw/orders.jsonl"]["last_modified"], "2026-09-14T01:00:41Z")
        self.assertEqual(ls["s3://shop-raw/orders.jsonl"]["size_bytes"], len(self.week.storage.read_text(shop.FILES["orders"]).encode()))
        d = self.week.reporting.dashboard()
        self.assertEqual((d["title"], d["created_by"], d["created"], d["last_refreshed"]), ("Sales, last 7 days", "j.marsh", "2026-09-02T15:41:00Z", "2026-09-14T03:00:09Z"))

    def test_one_query_rebuilds_daily_sales_and_explains_thursday(self):
        fits = shop.queries_that_rebuild(self.week)
        self.assertEqual([(q["source"], q["keep"], q["measure"], q["per"]) for q in fits], [("clean_orders", "completed", "revenue", "day")])
        rebuilt = self.w.sql(
            "SELECT date(ordered_at) AS day, SUM(price_pence * quantity) AS revenue_pence FROM clean_orders "
            "WHERE status = 'completed' GROUP BY day ORDER BY day"
        )
        self.assertEqual(rebuilt, self.w.sql("SELECT * FROM daily_sales ORDER BY day"))
        self.assertEqual(shop.day_gap(self.week, "2026-09-10"), {"orders": 7, "kept": 4, "left": 3, "left_ids": [7021, 7023, 7025], "left_pence": 15400})

    def test_the_quantity_rule_never_fires(self):
        orders = self.week.storage.records(shop.FILES["orders"])
        self.assertEqual(sum(1 for o in orders if o["quantity"] <= 0), 0)
        fits = shop.cleaning_rules_that_fit(self.week)
        self.assertEqual(len(fits), 2)
        self.assertEqual({r["quantity"] for r in fits}, {"keep", "drop"})
        self.assertTrue(all(r["duplicates"] == "one" and r["missing_customer"] == "drop" and r["cancelled"] == "keep" for r in fits))
        self.assertEqual(sum(1 for o in orders if o["order_id"] == 7015), 2)

    def test_the_week_strip_ends_before_you_start(self):
        nights = shop.timeline(self.week)
        self.assertEqual([n["night"] for n in nights], list(shop.NIGHTS))
        self.assertLess(nights[-1]["finished"], shop.ARRIVAL)
        self.assertEqual(shop.ARRIVAL, "2026-09-14T09:00:00Z")


class TheThreeChanges(unittest.TestCase):
    def test_counts_of_queries_that_give_every_row(self):
        counts = [len(shop.queries_that_rebuild(shop.run_week([c]), fit="covers")) for c in shop.CHANGES]
        self.assertEqual(counts, [2, 0, 1])

    def test_the_analysts_copy(self):
        week = shop.run_week(["copy"])
        sources = [q["source"] for q in shop.queries_that_rebuild(week)]
        self.assertEqual(sources, ["clean_orders", "s3://shop-scratch/clean_orders_copy.csv"])
        [copy] = week.storage.ls("s3://shop-scratch/")
        self.assertEqual(copy["last_modified"], "2026-09-14T02:15:17Z")
        self.assertEqual(len(week.storage.records(shop.COPY)), 44)

    def test_the_edited_program(self):
        before = {r["day"]: r["revenue_pence"] for r in shop.run_week().warehouse.sql("SELECT * FROM daily_sales")}
        week = shop.run_week(["refunds"])
        after = {r["day"]: r["revenue_pence"] for r in week.warehouse.sql("SELECT * FROM daily_sales")}
        self.assertEqual((before["2026-09-12"], after["2026-09-12"]), (19149, 21549))
        self.assertEqual({d for d in shop.DAYS if before[d] != after[d]}, {"2026-09-12"})
        [t] = week.warehouse.sql("SELECT row_count, last_altered FROM information_schema.tables WHERE table_name = 'daily_sales'")
        self.assertEqual((t["row_count"], t["last_altered"]), (7, "2026-09-14T02:30:21Z"))
        self.assertEqual(shop.queries_that_rebuild(week), [])
        statuses = {o["status"] for o in week.storage.records(shop.FILES["orders"])}
        self.assertEqual(statuses, {"completed", "cancelled"})

    def test_the_failed_night(self):
        week = shop.run_week(["failed"])
        tables = {r["table_name"]: r for r in week.warehouse.sql("SELECT * FROM information_schema.tables")}
        self.assertEqual(tables["daily_sales"]["row_count"], 6)
        self.assertEqual(tables["daily_sales"]["last_altered"], "2026-09-13T02:30:21Z")
        self.assertEqual(tables["clean_orders"]["last_altered"], "2026-09-14T02:05:52Z")
        days = [r["day"] for r in week.warehouse.sql("SELECT day FROM daily_sales")]
        self.assertNotIn("2026-09-13", days)
        d = week.reporting.dashboard()
        self.assertEqual((d["last_refreshed"], len(d["values"])), ("2026-09-14T03:00:09Z", 6))


if __name__ == "__main__":
    unittest.main()
