# Copyright © 2026 Christopher Snow

"""The front page's dashboard is the engine's: the JSON the page ships is what
notebook/front_dashboard.py writes from the shop's week."""

import unittest

import front_dashboard


class TheFrontPage(unittest.TestCase):
    def test_the_dashboard_the_page_ships_is_the_engines(self):
        self.assertEqual(front_dashboard.OUT.read_text(encoding="utf-8"), front_dashboard.text())

    def test_it_shows_the_week_with_thursday_lowest(self):
        values = front_dashboard.dashboard()["values"]
        self.assertEqual([v["day"] for v in values][0::6], ["2026-09-07", "2026-09-13"])
        self.assertEqual(min(values, key=lambda v: v["pence"])["day"], "2026-09-10")


if __name__ == "__main__":
    unittest.main()
