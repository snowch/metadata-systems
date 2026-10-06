// Copyright © 2026 Christopher Snow

// Every number Chapter 1's words state, read off the lab. If the shop's data or programs change,
// this fails until the words change with them (docs/notes/chapter-01/facts.md is the brief the
// words were drafted from).

import { describe, expect, it } from "vitest";

import {
  checkRows,
  cleanReconstructions,
  columnValues,
  formatValue,
  recordOf,
  runOver,
  storage,
  sumReconstructions,
  sumSql,
  catalogueFor,
  week,
} from "@ms/lab";

import { PROSE } from "./invisible-system.prose";

const revenue = (changes: Parameters<typeof week>[0] = []) => {
  const t = week(changes).tables.get("daily_sales")!;
  return Object.fromEntries(
    t.rows.map((r) => [String(r[0]), formatValue(r[1] ?? null, t.columns[1]!.type)]),
  );
};

describe("the facts Chapter 1 states", () => {
  it("has seven assets with the stated row counts", () => {
    const view = storage();
    expect(view).toHaveLength(7);
    const rows = Object.fromEntries(view.map((r) => [r.asset, r.rows]));
    expect(rows).toEqual({
      "customers.parquet": 10,
      "orders.parquet": 48,
      "products.parquet": 8,
      clean_customers: 9,
      clean_orders: 44,
      daily_sales: 7,
      sales_dashboard: 7,
    });
  });

  it("matches raw orders to daily_sales on three days of seven, the ones the prose names", () => {
    const w = week();
    const r = runOver(
      sumSql({ source: "orders.parquet", keep: "all", measure: "revenue", per: "day" }),
      catalogueFor(w),
    );
    if (!("table" in r)) throw new Error("query failed");
    const checks = checkRows(r.table, w.tables.get("daily_sales")!);
    expect(checks.filter((c) => c.same).map((c) => c.key)).toEqual([
      "2026-09-07",
      "2026-09-11",
      "2026-09-13",
    ]);
    expect(PROSE.p2Explain).toContain("three days: Monday, Friday, and Sunday");
    expect(PROSE.p2Explain).toContain("the other four days");
  });

  it("names etl_service as the owner of all three tables", () => {
    for (const t of ["clean_customers", "clean_orders", "daily_sales"] as const)
      expect(recordOf(storage(), t).ownerRole).toBe("etl_service");
    expect(PROSE.p1Explain).toContain("`etl_service` as the owner of all three tables");
  });

  it("has one query that rebuilds daily_sales, the one the hints give", () => {
    expect(sumReconstructions(week(), "daily_sales")).toEqual([
      { source: "clean_orders", keep: "completed", measure: "revenue", per: "day" },
    ]);
    expect(PROSE.c1Hints[4]).toContain(
      "`clean_orders`, keep completed orders only, add up price times quantity",
    );
  });

  it("states the analyst's copy as the lab makes it", () => {
    const copy = recordOf(storage(week(["copy"])), "clean_orders_copy.parquet");
    expect(copy.rows).toBe(44);
    expect(copy.location).toBe("s3://shop-scratch/clean_orders_copy.parquet");
    expect(copy.lastWritten).toBe("2026-09-14T02:15:17Z");
    expect(sumReconstructions(week(["copy"]), "daily_sales")).toHaveLength(2);
    expect(PROSE.outcomeCopy).toContain("last modified at 02:15, with the same 44 rows");
  });

  it("states the edit for refunds as the lab makes it", () => {
    const before = revenue();
    const after = revenue(["refunds"]);
    expect([before["2026-09-12"], after["2026-09-12"]]).toEqual(["191.49", "215.49"]);
    expect(after["2026-09-13"]).toBe("97.75");
    expect(before["2026-09-13"]).toBe("97.75");
    const changed = recordOf(storage(week(["refunds"])), "daily_sales");
    expect(changed.rows).toBe(7);
    expect(changed.lastWritten).toBe(recordOf(storage(), "daily_sales").lastWritten);
    expect(sumReconstructions(week(["refunds"]), "daily_sales", "covers")).toEqual([]);
    expect(PROSE.outcomeRefunds).toContain("215.49, not 191.49");
    expect(PROSE.outcomeRefunds).toContain("unchanged at 97.75");
    expect(PROSE.outcomeRefunds).toContain("the same 7 rows");
  });

  it("states the failed night as the lab makes it", () => {
    const w = week(["failed"]);
    const ds = recordOf(storage(w), "daily_sales");
    expect(ds.rows).toBe(6);
    expect(ds.lastWritten).toBe("2026-09-13T02:30:21Z");
    expect(columnValues(ds.content, "day")).not.toContain("2026-09-13");
    const dash = recordOf(storage(w), "sales_dashboard");
    expect(dash.rows).toBe(6);
    expect(dash.lastWritten.slice(0, 16)).toBe("2026-09-14T03:00");
    expect(sumReconstructions(w, "daily_sales", "covers")).toHaveLength(1);
    expect(PROSE.outcomeFailed).toContain("6 rows, with no row for Sunday");
    expect(PROSE.outcomeFailed).toContain("Sunday 13 September at 02:30");
    expect(PROSE.outcomeFailed).toContain("on Monday at 03:00 as usual and shows 6 values");
  });

  it("finds the quantity rule untestable this week, as the reflection says", () => {
    const fits = cleanReconstructions(week());
    expect(new Set(fits.map((c) => c.quantity))).toEqual(new Set(["keep", "drop"]));
    const raw = week().tables.get("orders.parquet")!;
    expect(columnValues(raw, "quantity").every((q) => Number(q) > 0)).toBe(true);
    expect(PROSE.reflection).toContain("quantity of 0 or less");
  });

  it("states order 7015 as the order written twice", () => {
    const ids = columnValues(week().tables.get("orders.parquet")!, "order_id");
    expect(ids.filter((id) => id === 7015)).toHaveLength(2);
    expect(PROSE.c2Hints[2]).toContain("order 7015 appears twice");
  });

  it("gives the first and last days of the week and the learner's first morning", () => {
    expect(PROSE.question).toContain("Monday 14 September 2026, 09:00");
    expect(PROSE.question).toContain("Monday 7 September");
    expect(Object.keys(revenue())).toEqual([
      "2026-09-07",
      "2026-09-08",
      "2026-09-09",
      "2026-09-10",
      "2026-09-11",
      "2026-09-12",
      "2026-09-13",
    ]);
  });
});
