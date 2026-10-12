# Copyright © 2026 Christopher Snow

"""Every number Chapter 2's notebook states, read off the engine.

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
        counts = [len(shop.queries_that_rebuild(shop.run_week([c]), fit="covers")) for c in ("copy", "refunds", "failed")]
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


class TheNewColumn(unittest.TestCase):
    """Chapter 3's change: from Saturday's row, `daily_sales` gains a column the records do not describe."""

    def test_the_column_arrives_with_saturdays_row(self):
        week = shop.run_week(["column"])
        rows = week.warehouse.sql("SELECT * FROM daily_sales ORDER BY day")
        self.assertEqual([r["order_count"] for r in rows], [None] * 5 + [7, 5])
        self.assertEqual([r["revenue_pence"] for r in rows], [r["revenue_pence"] for r in shop.run_week().warehouse.sql("SELECT * FROM daily_sales ORDER BY day")])
        columns = [r["column_name"] for r in week.warehouse.sql("SELECT column_name FROM information_schema.columns WHERE table_name = 'daily_sales' ORDER BY ordinal_position")]
        self.assertEqual(columns, ["day", "revenue_pence", "order_count"])
        self.assertEqual(week.reporting.dashboard()["values"], shop.run_week().reporting.dashboard()["values"])


class TheRecords(unittest.TestCase):
    """Chapter 3's records and their check, and Chapter 4's records, model and owners."""

    @classmethod
    def setUpClass(cls):
        cls.week = shop.run_week()

    def test_a_line_is_an_asset_a_column_a_field_and_a_value(self):
        r = shop.records("daily_sales revenue_pence unit: pence\ns3://shop-raw/products.csv responsible: Sam Lund\n# a note\n\nnot a fact")
        self.assertEqual(
            [(x["line"], x["asset"], x["column"], x["field"], x["value"]) for x in r],
            [(1, "daily_sales", "revenue_pence", "unit", "pence"), (2, "s3://shop-raw/products.csv", None, "responsible", "Sam Lund")],
        )
        self.assertEqual(r.unread, [{"line": 5, "text": "not a fact"}])
        self.assertEqual(r.sql("SELECT value FROM records WHERE field = 'unit'"), [{"value": "pence"}])

    def test_the_check_wants_a_description_of_every_column(self):
        empty = shop.records("")
        problems = empty.check(self.week.warehouse)
        self.assertEqual(len(problems), 14)
        dots = shop.records("daily_sales day means: ........\ndaily_sales revenue_pence means: the value")
        self.assertEqual([(p["asset"], p["column"]) for p in dots.check(self.week.warehouse, "daily_sales")], [("daily_sales", "day")])
        wrong = shop.records("daily_sales profit means: x\nmonthly_sales means: x\ns3://shop-raw/products.csv means: the catalogue")
        self.assertEqual([p["line"] for p in wrong.check(self.week.warehouse) if p["line"]], [1, 2])

    def test_a_check_cannot_see_a_change_of_meaning(self):
        mine = shop.records("daily_sales day means: a day\ndaily_sales revenue_pence means: completed orders")
        self.assertEqual(mine.check(self.week.warehouse, "daily_sales"), [])
        self.assertEqual(mine.check(shop.run_week(["refunds"]).warehouse, "daily_sales"), [])
        [p] = mine.check(shop.run_week(["column"]).warehouse, "daily_sales")
        self.assertEqual(p["column"], "order_count")

    def test_the_model_finds_missing_things_and_unknown_attributes(self):
        model = shop.model("dataset responsible: person or team\nperson name: text\nteam name: text")
        records = shop.typed_records(
            "dataset daily_sales responsible: Jo Marsh\ndataset daily_sales responsible: j.marsh\n"
            "dataset daily_sales drops: x\nperson j.marsh name: Jo Marsh\nshop bikes name: x"
        )
        problems = [(p["line"], p["problem"]) for p in model.check(records)]
        self.assertEqual([line for line, _ in problems], [1, 3, 5])
        self.assertEqual(shop.model("person team: team").check(shop.typed_records(""))[0]["line"], 1)

    def test_the_owners_by_three_readings(self):
        records = shop.typed_records(
            "dataset daily_sales responsible: j.marsh\nperson j.marsh team: finance\nteam finance name: Finance\n"
            "dataset clean_orders responsible: data_engineering\nteam data_engineering name: Data engineering\n"
            "dataset s3://shop-raw/products.csv responsible: s.lund\nperson s.lund name: Sam Lund\n"
            "dataset clean_customers responsible: a\ndataset clean_customers responsible: b"
        )
        got = {o["asset"]: (o["one_owner"], o["one_person"], o["one_team"]) for o in shop.owners(self.week, records)}
        self.assertEqual(len(got), 7)
        self.assertEqual(got["daily_sales"], ("yes", "yes", "yes"))
        self.assertEqual(got["clean_orders"], ("yes", "no", "yes"))
        self.assertEqual(got["s3://shop-raw/products.csv"], ("yes", "yes", "no"))
        self.assertEqual(got["clean_customers"], ("no", "no", "no"))
        self.assertEqual(got["s3://shop-raw/orders.jsonl"], ("no", "no", "no"))


class TheGraph(unittest.TestCase):
    """Chapter 5's graph and its walks; Chapter 6's lineage over jobs."""

    MODEL = "dataset responsible: person or team\ncolumn of: dataset\nperson team: team\nteam name: text\njob reads: dataset\njob writes: dataset or dashboard\ndashboard responsible: person or team\ndataset means: text\nperson name: text\n"
    RECORDS = (
        "dataset a responsible: p\ndataset b responsible: p\ncolumn a.x of: a\nperson p team: t\nteam t name: T\n"
        "dataset f means: a file\njob j reads: f\njob j writes: a\njob k reads: a\njob k writes: d\ndashboard d responsible: nobody\n"
    )

    def setUp(self):
        self.g = shop.graph(shop.typed_records(self.RECORDS), shop.model(self.MODEL))

    def test_nodes_and_edges(self):
        self.assertEqual(len(self.g.nodes()), 9)
        # A value that names nothing the records describe makes no edge.
        self.assertNotIn("nobody", {e["to"] for e in self.g.edges()})
        self.assertEqual(len(self.g.edges()), 8)

    def test_a_walk_follows_only_the_edges_it_is_given(self):
        self.assertEqual([r["node"] for r in self.g.traverse("a", {"responsible": "out", "team": "out"})], ["p", "t"])
        both = [r["node"] for r in self.g.traverse("a", {"responsible": "both"})]
        self.assertEqual(both, ["p", "b"])
        self.assertEqual(self.g.traverse("a", {"responsible": "both"})[1]["path"], "a -responsible-> p <-responsible- b")
        with self.assertRaises(ValueError):
            self.g.traverse("a", {"responsible": "sideways"})
        with self.assertRaises(KeyError):
            self.g.traverse("zzz")

    def test_downstream_and_upstream(self):
        self.assertEqual([r["node"] for r in self.g.downstream("f")], ["j", "a", "k", "d"])
        self.assertEqual([r["node"] for r in self.g.upstream("d")], ["k", "a", "j", "f"])
        self.assertEqual(list(self.g.downstream("b")), [])

    def test_the_drawing_is_an_image_with_its_own_dark_colours(self):
        html = self.g.only(["reads", "writes"], ["dataset", "dashboard", "job"]).drawing(label="the map")._repr_html_()
        self.assertTrue(html.startswith('<img class="ms-svg" alt="the map" src="data:image/svg+xml;base64,'))
        import base64

        svg = base64.b64decode(html.split("base64,")[1].rstrip('">')).decode()
        self.assertIn("prefers-color-scheme:dark", svg)
        self.assertIn('viewBox="0 0 340 ', svg)


class TheRepository(unittest.TestCase):
    """Chapter 6's jobs' code, and the change that makes it read the analyst's copy."""

    def test_the_code_is_the_code_that_runs(self):
        repo = shop.repository(shop.run_week())
        self.assertEqual([r["job"] for r in repo], ["build_clean_customers", "build_clean_orders", "build_daily_sales", "refresh_dashboard"])
        found = {r["job"]: shop.reads_and_writes(r["code"]) for r in repo}
        self.assertEqual(found["build_clean_orders"], {"reads": ["s3://shop-raw/orders.jsonl"], "writes": ["clean_orders"]})
        self.assertEqual(found["build_daily_sales"], {"reads": ["clean_orders"], "writes": ["daily_sales"]})
        self.assertEqual(found["refresh_dashboard"], {"reads": ["daily_sales"], "writes": ["sales_dashboard"]})
        from shop import week

        self.assertIn(week.CLEAN_ORDERS, repo[1]["code"])
        self.assertIn(week.DAILY_SALES, repo[2]["code"])

    def test_the_source_change(self):
        plain, source = shop.run_week(), shop.run_week(["source"])
        self.assertEqual(source.changes, ("copy", "source"))
        rows = lambda w: w.warehouse.sql("SELECT * FROM daily_sales ORDER BY day")
        self.assertEqual(rows(plain), rows(source))
        code = shop.repository(source)[2]["code"]
        self.assertEqual(shop.reads_and_writes(code)["reads"], [shop.COPY])

    def test_compare_with_code(self):
        lines = "job build_daily_sales reads: clean_orders\njob build_daily_sales writes: daily_sales\n"
        self.assertEqual(shop.compare_with_code(shop.typed_records(lines), shop.repository(shop.run_week()))[0]["job"], "build_clean_customers")
        only = lambda rows: [r for r in rows if r["job"] == "build_daily_sales"]
        self.assertEqual(only(shop.compare_with_code(shop.typed_records(lines), shop.repository(shop.run_week()))), [])
        wrong = shop.typed_records(lines + "job build_daily_sales reads: clean_customers\njob nightly_backup reads: clean_orders\n")
        found = shop.compare_with_code(wrong, shop.repository(shop.run_week()))
        self.assertEqual([(r["job"], r["says"]) for r in found if r["line"]], [("build_daily_sales", "reads: clean_customers")])
        self.assertIn("nightly_backup", {r["job"] for r in found})
        stale = only(shop.compare_with_code(shop.typed_records(lines), shop.repository(shop.run_week(["source"]))))
        self.assertEqual([(r["says"], r["code"]) for r in stale], [("reads: clean_orders", ""), ("", f"reads: {shop.COPY}")])



class TheReturnsDesk(unittest.TestCase):
    """Chapter 7's change: returns as objects with versions, and two functions."""

    @classmethod
    def setUpClass(cls):
        cls.week = shop.run_week(["returns"])

    def test_the_default_week_is_unchanged(self):
        plain = shop.run_week()
        self.assertEqual(plain.storage.ls("s3://shop-returns/"), [])
        self.assertEqual(len(plain.warehouse.sql("SELECT * FROM information_schema.tables")), 3)
        self.assertEqual({e.writer for e in plain.executions} - {"export"}, {"clean_customers", "clean_orders", "daily_sales", "dashboard_refresh"})

    def test_versions_and_the_table(self):
        versions = self.week.storage.versions("s3://shop-returns/")
        self.assertEqual(len(versions), 6)
        self.assertEqual([v["deleted"] for v in versions if v["key"].endswith("r-203.json")], [False, True])
        self.assertEqual(len([v for v in versions if v["key"].endswith("r-202.json")]), 2)
        rows = {r["return_id"]: r["quantity"] for r in self.week.warehouse.sql("SELECT * FROM returns")}
        self.assertEqual(rows, {"r-201": 1, "r-202": 1, "r-204": 1})

    def test_the_functions_run_once_per_change_and_are_in_the_repository(self):
        functions = [e for e in self.week.executions if e.night is None]
        self.assertEqual([e.change for e in functions], ["created", "created", "created", "overwritten", "created", "deleted"])
        self.assertEqual([e.reads for e in functions][-1], ())
        files = [r["file"] for r in shop.repository(self.week)]
        self.assertEqual(files[-2:], ["functions/record_return.py", "functions/remove_return.py"])

    def test_the_week_is_deterministic(self):
        again = shop.run_week(["returns"])
        self.assertEqual(again.storage.versions("s3://"), self.week.storage.versions("s3://"))


class TheEventsAndTheirStandard(unittest.TestCase):
    """Chapters 7 to 9: the reader's events, OpenLineage's, and the ingestion stages."""

    def test_every_run_sends_a_start_and_a_finish(self):
        week = shop.run_week(["returns", "failed"])
        events = shop.events(week)
        self.assertEqual(len(events), 2 * 34)
        runs = shop.runs(events)
        self.assertEqual([r["status"] for r in runs].count("failed"), 1)

    def test_every_openlineage_event_keeps_the_rules(self):
        # docs/sources.md: the rules; the published schema itself was checked outside the repository
        # (docs/notes/chapter-08.md, "What was built for it").
        for changes in ([], ["returns", "failed", "source"], ["returns", "copy", "column", "refunds"]):
            week = shop.run_week(changes)
            for event in shop.openlineage.run_events(week) + shop.openlineage.analyst_events(week):
                self.assertEqual(shop.openlineage.problems(event), [], event["job"]["name"])
                for facet in [*event["run"].get("facets", {}).values(), *event["job"].get("facets", {}).values()]:
                    self.assertTrue({"_producer", "_schemaURL"} <= set(facet))

    def test_run_ids_are_version_7_uuids_in_time_order(self):
        events = shop.openlineage.run_events(shop.run_week(["returns"]))
        ids = [e["run"]["runId"] for e in events if e["eventType"] == "START"]
        self.assertTrue(all(i[14] == "7" and i[19] in "89ab" for i in ids))
        self.assertEqual(ids, sorted(ids))
        self.assertEqual(len(set(ids)), 34)

    def test_a_broken_event_is_refused(self):
        bad = {"eventType": "DONE", "eventTime": "yesterday", "run": {"runId": "x"}, "job": {"name": "j"}, "producer": "nowhere", "schemaURL": "x:y"}
        kinds = {k for _, k in shop.openlineage.problems(bad)}
        self.assertEqual(kinds, {"event_type", "time", "run_id", "missing", "uri"})
        self.assertEqual(len(shop.openlineage.Consumer().send(bad).refused), 1)

    def test_ingesting_the_whole_week(self):
        I = shop.ingest
        lines = I.event_lines(shop.run_week(["returns", "copy"]))
        objs = I.objects(I.normalise(I.parse(lines)))
        edges = I.edges(objs)
        self.assertEqual((len(objs.runs), len(edges.by_job)), (41, 16))
        self.assertTrue(all(r["state"] == "COMPLETE" for r in objs.runs.values()))


class TheColumnLineage(unittest.TestCase):
    """Chapter 10: the shop's parser over the programs' SQL."""

    @classmethod
    def setUpClass(cls):
        from shop import columns

        cls.C = columns
        cls.week = shop.run_week()

    def test_the_select_names_no_column_of_the_table_it_writes(self):
        code = [p["code"] for p in self.C.programs(self.week) if p["job"] == "build_daily_sales"][0]
        self.assertEqual({r["column"] for r in self.C.lineage(code)}, {"daily_sales.column 1", "daily_sales.column 2"})
        named = self.C.lineage(code, self.week.warehouse)
        self.assertEqual({r["column"] for r in named}, {"daily_sales.day", "daily_sales.revenue_pence"})
        revenue = {(r["from"], r["kind"], r["how"]) for r in named if r["column"] == "daily_sales.revenue_pence"}
        self.assertEqual(
            revenue,
            {
                ("clean_orders.price_pence", "value", "aggregated"),
                ("clean_orders.quantity", "value", "aggregated"),
                ("clean_orders.status", "rows", "filter"),
                ("clean_orders.ordered_at", "rows", "filter"),
                ("clean_orders.ordered_at", "rows", "grouping"),
            },
        )

    def test_upstream_to_the_raw_orders(self):
        up = self.C.upstream(self.week, "daily_sales", "revenue_pence", self.week.warehouse)
        raw = {r["column"]: r for r in up if r["dataset"] == "orders.jsonl"}
        self.assertEqual(len(raw), 7)
        self.assertEqual({c for c, r in raw.items() if r["value"] == "yes"}, {"price_pence", "quantity"})
        self.assertEqual(raw["customer_id"]["rows"], "distinct in build_clean_orders; filter in build_clean_orders")
        self.assertIn("filter in build_daily_sales", raw["status"]["rows"])

    def test_a_star_names_no_column_until_the_catalogue_does(self):
        week = shop.run_week(["source"])
        self.assertEqual([r["from"] for r in self.C.lineage(self.C.ANALYST_COPY)], ["clean_orders.*"])
        self.assertEqual(len(self.C.lineage(self.C.ANALYST_COPY, week.warehouse)), 7)
        up = self.C.upstream(week, "daily_sales", "revenue_pence", week.warehouse)
        self.assertEqual([r["dataset"] for r in up][0], "clean_orders_copy.csv")
        self.assertIn("orders.jsonl", {r["dataset"] for r in up})

    def test_a_function_hides_the_table_it_reads(self):
        week = shop.run_week(["net"])
        self.assertEqual(week.warehouse.sql("SELECT * FROM daily_sales"), self.week.warehouse.sql("SELECT * FROM daily_sales"))
        up = self.C.upstream(week, "daily_sales", "revenue_pence", week.warehouse)
        self.assertNotIn("returns", {r["dataset"] for r in up})
        self.assertEqual({r["column"] for r in up if r["dataset"] == "clean_orders" and r["value"] == "yes"}, {"order_id", "product_id", "price_pence", "quantity"})

    def test_the_facet_keeps_both_kinds(self):
        f = self.C.facet(self.week, "daily_sales")
        self.assertEqual(sorted(f["fields"]), ["day", "revenue_pence"])
        self.assertEqual({(x["field"], x["transformations"][0]["subtype"]) for x in f["dataset"]}, {("ordered_at", "FILTER"), ("ordered_at", "GROUP_BY"), ("status", "FILTER")})


class TheSchemaHistory(unittest.TestCase):
    """Chapter 11: the supplier's three changes to the orders file."""

    def test_versions_and_diffs(self):
        from shop import schemas as S

        expected = {
            "added": [("coupon_code", "added")],
            "renamed": [("quantity", "removed"), ("qty", "added")],
            "retyped": [("customer_id", "retyped")],
        }
        for change, diff in expected.items():
            week = shop.run_week([change])
            self.assertEqual([v["writes"] for v in S.versions(week, "orders.jsonl")], [5, 2])
            self.assertEqual([(r["column"], r["change"]) for r in S.diff(week, "orders.jsonl")], diff)
            # The catalogue's record of clean_orders does not change.
            self.assertEqual(len(S.versions(week, "clean_orders")), 1)

    def test_the_warehouse_keeps_only_text_that_is_not_a_number(self):
        # Chapter 11 states it: "101" stored in a column declared INTEGER becomes 101; C101 stays text.
        w = shop.run_week().warehouse
        w.db.execute("CREATE TEMP TABLE probe (n INTEGER)")
        w.db.executemany("INSERT INTO temp.probe VALUES (?)", [("101",), ("C101",)])
        self.assertEqual(w.db.execute("SELECT typeof(n) FROM temp.probe").fetchall(), [("integer",), ("text",)])

    def test_what_each_reader_gets(self):
        from shop import schemas as S

        got = {c: [r[f"with {c}"] for r in S.compare(c)] for c in ("added", "renamed", "retyped")}
        self.assertEqual(got, {"added": [7, 7, 7], "renamed": [5, 5, 0], "retyped": [7, 7, 0]})
        week = shop.run_week(["renamed"])
        self.assertEqual([r["program"] for r in S.readers(week, "orders.jsonl", "quantity")], ["build_clean_orders"])
        self.assertEqual(len(S.readers(week, "orders.jsonl", "qty")), 0)


class TheIdentities(unittest.TestCase):
    """Chapter 12: references, environments and the development run."""

    def test_the_pairs(self):
        from shop import identity as I

        week = shop.run_week(["returns", "dev", "view"])
        v = [x["version"] for x in week.storage.versions("s3://shop-returns/r-202.json")]
        pairs = [
            ("shop.analytics.daily_sales", "SHOP.ANALYTICS.DAILY_SALES"),
            ("daily_sales", "shop.analytics.daily_sales"),
            ("shop.analytics.daily_sales", "shop_dev.analytics.daily_sales"),
            ("shop.analytics.daily_sales", "shop.analytics.sales_by_day"),
            ("s3://shop-raw/orders.jsonl", "s3://shop-raw/Orders.jsonl"),
            (f"s3://shop-returns/r-202.json@{v[0]}", f"s3://shop-returns/r-202.json@{v[1]}"),
        ]
        got = [(r["same object"], r["same rows"], r["same environment"]) for r in I.compare(week, pairs)]
        self.assertEqual(got, [("yes", "yes", "yes"), ("yes", "yes", "yes"), ("no", "no", "no"), ("no", "yes", "yes"), ("no", "no", "yes"), ("yes", "no", "yes")])

    def test_the_development_run_joins_production_until_the_rule_knows_its_producer(self):
        I = shop.ingest
        week = shop.run_week(["returns", "dev"])
        parsed = I.parse(I.event_lines(week))
        writers = lambda edges: {(r["job"], r["dataset"].rsplit("/", 1)[-1]) for r in edges.by_job if r["edge"] == "writes" and "daily_sales" in r["dataset"]}
        self.assertEqual(writers(I.edges(I.objects(I.normalise(parsed)))), {("shop/build_daily_sales", "shop.analytics.daily_sales"), ("dev/build_daily_sales", "shop.analytics.daily_sales")})
        fixed = I.normalise(parsed, {shop.openlineage.DEV_PRODUCER: "shop_dev"})
        self.assertEqual(writers(I.edges(I.objects(fixed))), {("shop/build_daily_sales", "shop.analytics.daily_sales"), ("dev/build_daily_sales", "shop_dev.analytics.daily_sales")})


class TheObservations(unittest.TestCase):
    """Chapter 13: what runs recorded, and three readings of "fresh"."""

    def test_the_readings_week_by_week(self):
        from shop import observe as O

        met = lambda changes: [r["met"] for r in O.readings(shop.run_week(changes))]
        self.assertEqual(met([]), ["yes", "yes", "yes"])
        self.assertEqual(met(["failed"]), ["yes", "no", "no"])
        self.assertEqual(met(["clock"]), ["yes", "no", "yes"])
        self.assertEqual(met(["renamed"]), ["yes", "yes", "no"])
        # The runs' events carry one clock, and by them the dashboard was refreshed after its input.
        self.assertEqual([r["met"] for r in O.readings(shop.run_week(["clock"]), by="runs")], ["yes", "yes", "yes"])

    def test_a_run_that_succeeded_and_wrote_nothing(self):
        from shop import observe as O

        empty = [r for r in O.observations(shop.run_week(["renamed"])) if r["rows written"] == 0]
        self.assertEqual([(r["program"], r["status"]) for r in empty], [("build_clean_orders", "succeeded"), ("build_daily_sales", "succeeded")] * 2)
        [failed] = [r for r in O.observations(shop.run_week(["failed"])) if r["status"] == "failed"]
        self.assertEqual(failed["error"], "database is locked")


class TheReturnsDeskInOrder(unittest.TestCase):
    """The desk's changes of a day reach `returns` before the night's work, and Monday's before you start."""

    def test_monday_morning_and_the_plain_desk(self):
        w = shop.run_week(["returns"])
        self.assertEqual([r["return_id"] for r in w.warehouse.sql("SELECT return_id FROM returns ORDER BY 1")], ["r-201", "r-202", "r-204"])
        late = shop.run_week(["corrected", "withdrawn"])
        self.assertIn("net", late.changes)
        from shop.provenance import returns_as_of

        before = {r["return_id"]: r["quantity"] for r in returns_as_of(late, "2026-09-14T02:30:00Z")}
        self.assertEqual((before["r-205"], before["r-206"]), (2, 1))
        now = {r["return_id"]: r["quantity"] for r in late.warehouse.sql("SELECT * FROM returns")}
        self.assertEqual((now["r-205"], "r-206" in now), (1, False))


class TheQuality(unittest.TestCase):
    """Chapter 14: what a run measures, and assertions over it."""

    def test_an_assertion_after_the_rule_cannot_fail(self):
        from shop import quality as Q

        w = shop.run_week()
        self.assertEqual({r["passed"] for r in Q.check(w, "clean_orders", "no customer_id")}, {"yes"})
        failed = [r["night"] for r in Q.check(w, "orders.jsonl", "no customer_id") if r["passed"] == "no"]
        self.assertEqual(failed, ["2026-09-11", "2026-09-12", "2026-09-13", "2026-09-14"])
        # The rows the rule removes are the rows the assertion on the table is meant to find.
        self.assertIn("customer_id IS NOT NULL", shop.week.CLEAN_ORDERS)

    def test_the_counts_each_run_recorded(self):
        from shop import quality as Q

        [fri] = [r for r in Q.reconcile(shop.run_week()) if r["night"] == "2026-09-11"]
        self.assertEqual((fri["rows read"], fri["rows written"], fri["repeats"], fri["left out"]), (27, 23, 1, 3))
        self.assertEqual(list(Q.left_out(shop.run_week())), [{"day": "2026-09-10", "orders": 3, "pence": 15400}])
        self.assertEqual([r["met"] for r in Q.readings(shop.run_week())], ["no", "yes", "no"])

    def test_the_facets_name_their_schemas(self):
        from shop import quality as Q

        f = Q.facets(shop.run_week(), "run-014")
        self.assertTrue(f["facets"]["dataQualityMetrics"]["_schemaURL"].startswith("https://openlineage.io/spec/facets/1-0-1/DataQualityMetricsDatasetFacet.json"))
        self.assertEqual(f["facets"]["dataQualityMetrics"]["columnMetrics"]["customer_id"], {"nullCount": 3})
        [a] = f["inputFacets"]["dataQualityAssertions"]["assertions"]
        self.assertEqual((a["assertion"], a["column"], a["success"]), ("not_null", "customer_id", False))


class TheProvenance(unittest.TestCase):
    """Chapter 15: where one figure came from."""

    def test_thursday_back_to_the_file(self):
        from shop import provenance as P

        steps = P.trace(shop.run_week(), "2026-09-10")
        self.assertEqual([r["pence"] for r in steps], [5150, 5150, 5150, 5150])
        self.assertEqual(steps[2]["rows"], "7020, 7022, 7024, 7026")
        left = [r for r in P.trace(shop.run_week(), "2026-09-10", dropped=True) if r["asset"].startswith("left out")]
        self.assertEqual((sum(r["pence"] for r in left), [r["rows"].endswith("customer_id IS NOT NULL is false") for r in left]), (15400, [True] * 3))
        # The table is read as it is now, written by the last run; the file in the version that was
        # current when the run whose output was read started.
        self.assertEqual(steps[2]["made by"], "run-026, build_clean_orders")

    def test_every_plain_day_adds_up(self):
        from shop import provenance as P

        w = shop.run_week()
        self.assertTrue(all(P.adds_up(w, d) for d in shop.DAYS))

    def test_a_corrected_return_adds_up_only_as_read(self):
        from shop import provenance as P

        w = shop.run_week(["corrected"])
        self.assertEqual(P.trace(w, "2026-09-13")[1]["pence"], 6925)
        self.assertFalse(P.adds_up(w, "2026-09-13"))
        self.assertTrue(P.adds_up(w, "2026-09-13", as_read=True))
        self.assertEqual([r["quantity"] for r in P.object_versions(w, "r-205")], [2, 1])


class TheImpact(unittest.TestCase):
    """Chapter 16: what a change affects, by the graph and in fact."""

    def test_a_renamed_column(self):
        from shop import impact as I

        w0, w1 = shop.run_week(["copy"]), shop.run_week(["copy", "customer"])
        self.assertEqual({r["writes"] for r in I.downstream(w0, "clean_orders")}, {"daily_sales", "sales_dashboard", "s3://shop-scratch/clean_orders_copy.csv"})
        self.assertEqual([r["column"] for r in I.downstream_columns(w0, "clean_orders", "customer_id")], ["s3://shop-scratch/clean_orders_copy.csv.customer_id"])
        changed = {r["output"]: r["changed"] for r in I.readers(w0, w1)}
        self.assertEqual(changed, {"daily_sales": "no", "sales_dashboard": "no", "clean_orders_copy.csv": "yes", "Jo Marsh's query result": "yes"})
        self.assertIn("no such column", I.readers(w0, w1)[-1]["after"])

    def test_a_withdrawn_return(self):
        from shop import impact as I

        w = shop.run_week(["withdrawn"])
        self.assertEqual([r["writes"] for r in I.downstream(w, "s3://shop-returns/r-206.json")], ["returns"])
        self.assertEqual(list(I.downstream(w, "returns")), [])
        self.assertEqual([r["still there"] for r in I.made_from(w, "r-206")], ["no", "yes", "yes"])
        self.assertEqual(w.warehouse.sql("SELECT revenue_pence FROM daily_sales WHERE day = '2026-09-13'"), [{"revenue_pence": 8575}])


class TheCause(unittest.TestCase):
    """Chapter 17: a backwards search."""

    def test_where_each_fault_entered(self):
        from shop import cause as C

        thu = C.search(shop.run_week(), "2026-09-10")
        self.assertEqual([r["differs from its input"] for r in thu[:3]], ["no", "no", "yes"])
        self.assertEqual([r["code changed since the night before"] for r in thu[:3]], ["no", "no", "no"])
        sat = C.search(shop.run_week(["refunds"]), "2026-09-12")
        self.assertEqual([r["differs from its input"] for r in sat[:3]], ["no", "yes", "no"])
        self.assertEqual(sat[1]["code changed since the night before"], "yes")
        tue = C.search(shop.run_week(["refunds"]), "2026-09-08")
        self.assertEqual({r["differs from its input"] for r in tue[:3]}, {"no"})
        self.assertIn("status <> 'refunded'", C.code_change(shop.run_week(["refunds"]), "build_daily_sales", "2026-09-13"))



def _graph(events, order="event"):
    from shop import ingest as I

    objs = I.objects(I.normalise(events), order=order)
    return objs, I.edges(objs)


class TheDeliveryPath(unittest.TestCase):
    """Chapter 18: an event the path loses, and sending again until acknowledged."""

    @classmethod
    def setUpClass(cls):
        cls.week = shop.run_week(["returns"])

    def test_a_lost_complete_leaves_the_job_graph_and_an_open_run(self):
        from shop import delivery as D

        whole = D.send(self.week)
        self.assertEqual((len(whole.log), len(whole.events), len(whole.lost)), (68, 68, 0))
        lossy = D.send(self.week, lose=["build_daily_sales COMPLETE 2026-09-10"])
        self.assertEqual((len(lossy.events), len(lossy.lost)), (67, 1))
        _, e = _graph(lossy.events)
        _, e0 = _graph(whole.events)
        runs = lambda edges: [(r["edge"], r["runs"]) for r in edges.of("shop/build_daily_sales")]
        self.assertEqual(runs(e0), [("reads", 7), ("writes", 7)])
        self.assertEqual(runs(e), [("reads", 7), ("writes", 6)])
        [open_] = D.open_runs(lossy.events, "2026-09-14T09:00:00Z")
        self.assertEqual(open_, {"job": "build_daily_sales", "started": "2026-09-10T02:30:00Z", "seconds since": 369000, "usual seconds": 21})

    def test_a_lost_complete_of_the_only_run_leaves_no_edge(self):
        from shop import delivery as D

        lossy = D.send(self.week, lose=["remove_return COMPLETE"])
        _, e = _graph(lossy.events)
        _, e0 = _graph(D.send(self.week).events)
        self.assertEqual(list(e.of("shop/remove_return")), [])
        self.assertEqual([(r["edge"], r["dataset"]) for r in e0.of("shop/remove_return")], [("writes", "warehouse://shop-warehouse/shop.analytics.returns")])
        [open_] = D.open_runs(lossy.events, "2026-09-14T09:00:00Z")
        self.assertEqual((open_["started"], open_["usual seconds"]), ("2026-09-12T16:50:02Z", None))

    def test_at_least_once(self):
        from shop import delivery as D

        again = D.send(self.week, lose=["remove_return COMPLETE"], at_least_once=True)
        self.assertEqual((len(again.events), len(again.lost)), (68, 0))
        [row] = [r for r in again.log if r["sendings"] > 1]
        self.assertEqual((row["sendings"], row["received"], row["first arrival"]), (2, 1, "2026-09-12T16:50:37Z"))
        twice = D.send(self.week, lose_ack=["remove_return COMPLETE"], at_least_once=True)
        self.assertEqual(len(twice.events), 69)
        self.assertEqual([r["received"] for r in twice.log if r["received"] > 1], [2])


class TheDuplicates(unittest.TestCase):
    """Chapter 19: an event received twice, a retry with a new time, and a trigger delivered twice."""

    @classmethod
    def setUpClass(cls):
        cls.week = shop.run_week(["returns"])

    def test_a_repeat_changes_no_edge(self):
        from shop import delivery as D

        d = D.send(self.week, lose_ack=["build_daily_sales COMPLETE 2026-09-10"], at_least_once=True)
        self.assertEqual(len(d.events), 69)
        _, e = _graph(d.events)
        _, e0 = _graph(D.send(self.week).events)
        self.assertEqual(list(e.by_job), list(e0.by_job))

    def test_a_retry_with_a_new_time(self):
        from shop import delivery as D, ingest as I

        d = D.send(self.week, lose_ack=["build_daily_sales COMPLETE 2026-09-10"], at_least_once=True, restamp=True)
        objs, _ = _graph(d.events)
        [run] = [r for r in objs.runs.values() if r["job"] == "shop/build_daily_sales" and r["started"].startswith("2026-09-10")]
        self.assertEqual((run["started"], run["ended"]), ("2026-09-10T02:30:00Z", "2026-09-10T02:30:52Z"))
        self.assertEqual(len(I.dedupe(d.events, "content").dropped), 0)
        [dropped] = I.dedupe(d.events, "run").dropped
        self.assertEqual((dropped["event time"], dropped["kept event time"]), ("2026-09-10T02:30:52Z", "2026-09-10T02:30:21Z"))
        objs, _ = _graph(I.dedupe(d.events, "run"))
        [run] = [r for r in objs.runs.values() if r["job"] == "shop/build_daily_sales" and r["started"].startswith("2026-09-10")]
        self.assertEqual(run["ended"], "2026-09-10T02:30:21Z")
        exact = D.send(self.week, lose_ack=["build_daily_sales COMPLETE 2026-09-10"], at_least_once=True)
        self.assertEqual(len(I.dedupe(exact.events, "content").dropped), 1)

    def test_a_trigger_delivered_twice(self):
        from shop import delivery as D, ingest as I

        twice = shop.run_week(["returns", "twice"])
        events = D.week_events(twice)
        self.assertEqual(len(events), 70)
        self.assertEqual(
            list(D.repeated_work(events)),
            [{"object": "s3://shop-returns/r-202.json", "version": "68d7454802de", "change": "overwritten", "runs": 2}],
        )
        self.assertEqual(len(I.dedupe(events, "run").dropped), 0)
        self.assertEqual(
            twice.warehouse.sql("SELECT * FROM returns ORDER BY return_id"),
            self.week.warehouse.sql("SELECT * FROM returns ORDER BY return_id"),
        )
        _, e = _graph(events)
        _, e0 = _graph(D.week_events(self.week))
        runs = lambda edges: {(r["edge"], r["dataset"]): r["runs"] for r in edges.of("shop/record_return")}
        self.assertEqual(runs(e0)[("writes", "warehouse://shop-warehouse/shop.analytics.returns")], 5)
        self.assertEqual(runs(e)[("writes", "warehouse://shop-warehouse/shop.analytics.returns")], 6)


class TheOrder(unittest.TestCase):
    """Chapter 20: event time against arrival time."""

    def test_a_late_complete(self):
        from shop import delivery as D, ingest as I

        w = shop.run_week(["returns"])
        d = D.send(w, delay={"build_daily_sales COMPLETE 2026-09-09": 26 * 3600})
        seen = d.until("2026-09-10T09:00:00Z")
        last = lambda order: [r["run ended"] for r in I.objects(I.normalise(seen), order=order).written if r["dataset"].endswith("daily_sales")]
        self.assertEqual(last("event"), ["2026-09-10T02:30:21Z"])
        self.assertEqual(last("arrival"), ["2026-09-09T02:30:21Z"])

    def test_a_start_after_its_complete(self):
        from shop import delivery as D, ingest as I

        w = shop.run_week(["returns"])
        d = D.send(w, delay={"build_daily_sales START 2026-09-09": 60})
        state = lambda order: [r["state"] for r in I.objects(I.normalise(d.events), order=order).runs.values() if r["job"].endswith("build_daily_sales") and r["started"].startswith("2026-09-09")]
        self.assertEqual(state("event"), ["COMPLETE"])
        self.assertEqual(state("arrival"), ["START"])

    def test_a_delete_before_its_create(self):
        from shop import delivery as D

        w = shop.run_week(["returns", "withdrawn"])
        d = D.send(w, delay={"record_return START 2026-09-13": 12 * 3600, "record_return COMPLETE 2026-09-13": 12 * 3600})
        exists = lambda order: [r["exists"] for r in D.object_states(d.events, order) if r["object"].endswith("r-206.json")]
        self.assertEqual(exists("event"), ["no"])
        self.assertEqual(exists("arrival"), ["yes"])


class TheClaims(unittest.TestCase):
    """Chapter 21: three sources, and the rule that chooses."""

    def test_newest_wins_changes_overnight(self):
        from shop import claims as C

        pick = lambda at, rule: {r["attribute"]: (r["value"], r["source"]) for r in C.resolve(C.claims(at), rule)}
        self.assertEqual(pick("2026-09-14T18:00:00Z", "newest"), {"columns": ("day, revenue", "team sheet"), "owner": ("j.marsh", "records")})
        self.assertEqual(pick("2026-09-15T09:00:00Z", "newest"), {"columns": ("day, revenue", "team sheet"), "owner": ("data team", "team sheet")})
        self.assertEqual(pick("2026-09-15T09:00:00Z", "as of"), {"columns": ("day, revenue_pence", "warehouse"), "owner": ("etl_service", "warehouse")})
        self.assertEqual(pick("2026-09-15T09:00:00Z", "ranked"), {"columns": ("day, revenue_pence", "warehouse"), "owner": ("j.marsh", "records")})
        self.assertEqual(len(C.resolve(C.claims("2026-09-15T09:00:00Z"), "all")), 5)


class TheAliases(unittest.TestCase):
    """Chapter 22: which references merge, rule by rule."""

    def test_the_rules(self):
        from shop import aliases as A

        sizes = lambda rule: [r["references"] for r in A.merge(rule)]
        self.assertEqual(sizes("exact"), [1, 1, 1, 1, 1, 1])
        self.assertEqual(sizes("qualified"), [2, 1, 1, 1, 1])
        self.assertEqual(sizes("last part"), [6])
        self.assertEqual(sizes("aliases"), [4, 1, 1])
        self.assertEqual(A.merge("aliases")[0]["systems"], "warehouse, events, transformation tool, reporting tool")


class TheScale(unittest.TestCase):
    """Chapter 23: the week's rates, projected, and retention."""

    @classmethod
    def setUpClass(cls):
        cls.week = shop.run_week(["returns"])

    def test_the_week_measured(self):
        from shop import scale as S

        [m] = S.measure(self.week)
        self.assertEqual(m, {"assets": 11, "jobs": 6, "runs": 34, "events": 68, "edges by run": 67, "edges by job": 14, "days": 7, "bytes per event": 1492})
        self.assertEqual((S.reach(self.week)[0]["dataset"], S.reach(self.week)[0]["share"]), ("s3://shop-raw/orders.jsonl", 0.43))

    def test_which_question_passes_the_budget_first(self):
        from shop import scale as S

        first = {r["way"]: r["first over the limit at"] for r in S.first_over(self.week)}
        self.assertEqual(first, {
            "latest run: every event": 100000, "latest run: sorted by job and time": None, "one day: every event": 100000,
            "one day: stored by day": 10000000, "downstream: to the end": 10000000, "downstream: 4 steps": None,
        })
        top = S.project(self.week)[-1]
        self.assertEqual((top["events stored"], top["latest run: sorted by job and time"]), (794805210, 31))

    def test_retention_and_compaction(self):
        from shop import delivery as D, scale as S

        events = D.week_events(self.week)
        kept = S.retain(events, 3, "2026-09-14T09:00:00Z")
        self.assertEqual(len(kept), 28)
        _, all_ = _graph(events)
        _, some = _graph(kept)
        self.assertEqual(len(S.lineage_of(all_.by_run, "r-201.json")), 1)
        self.assertEqual(len(S.lineage_of(some.by_run, "r-201.json")), 0)
        self.assertEqual(len(S.lineage_of(S.compact(events), "r-201.json")), 1)
        self.assertEqual(len(self.week.warehouse.sql("SELECT * FROM returns WHERE return_id = 'r-201'")), 1)


if __name__ == "__main__":
    unittest.main()
