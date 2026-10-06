// Copyright © 2026 Christopher Snow

// The lab's behaviour that the course relies on. The numbers a chapter's prose states are pinned
// in that chapter's facts test; this file pins the mechanisms.

import { describe, expect, it } from "vitest";

import {
  DUPLICATED,
  NIGHTS,
  PROGRAMS,
  cleanReconstructions,
  columnValues,
  parseQuery,
  questionMap,
  recordOf,
  runProbe,
  runWeek,
  sameNumbers,
  storage,
  sumReconstructions,
  week,
} from "./index";

describe("the shop's week", () => {
  it("is the same on every run", () => {
    expect(JSON.stringify([...runWeek().tables])).toBe(JSON.stringify([...runWeek().tables]));
    expect(runWeek(["copy", "failed"]).executions).toEqual(runWeek(["failed", "copy"]).executions);
  });

  it("writes every program's SQL in the course's subset", () => {
    for (const p of Object.values(PROGRAMS)) expect(() => parseQuery(p.sql)).not.toThrow();
  });

  it("runs seven nights, each writing the raw files and then the four programs", () => {
    const w = week();
    expect(NIGHTS).toHaveLength(7);
    for (const night of NIGHTS) {
      const writers = w.executions.filter((e) => e.night === night).map((e) => e.writer);
      expect(writers).toEqual([
        "export",
        "export",
        "export",
        "clean_customers",
        "clean_orders",
        "daily_sales",
        "dashboard_refresh",
      ]);
    }
  });

  it("keeps the export's repeated order in the raw file and once in clean_orders", () => {
    const w = week();
    const raw = columnValues(w.tables.get("orders.parquet")!, "order_id");
    const clean = columnValues(w.tables.get("clean_orders")!, "order_id");
    expect(raw.filter((id) => id === DUPLICATED)).toHaveLength(2);
    expect(clean.filter((id) => id === DUPLICATED)).toHaveLength(1);
  });

  it("drops the orders the checkout sent with no customer id, all of them on Thursday", () => {
    const w = week();
    const raw = w.tables.get("orders.parquet")!;
    const missing = raw.rows.filter((r) => r[1] === null);
    expect(missing.length).toBeGreaterThan(0);
    expect(new Set(missing.map((r) => String(r[6]).slice(0, 10)))).toEqual(new Set(["2026-09-10"]));
    expect(w.tables.get("clean_orders")!.rows.some((r) => r[1] === null)).toBe(false);
  });

  it("appends one row of daily_sales a night, and misses the last if that night fails", () => {
    expect(week().tables.get("daily_sales")!.rows).toHaveLength(7);
    const failed = week(["failed"]);
    expect(failed.tables.get("daily_sales")!.rows).toHaveLength(6);
    expect(recordOf(storage(failed), "daily_sales").lastWritten.slice(0, 10)).toBe("2026-09-13");
    expect(failed.executions.find((e) => e.status === "failed")?.writer).toBe("daily_sales");
  });
});

describe("what storage records", () => {
  it("gives files no owner, tables the program account, and the dashboard its creator", () => {
    const view = storage();
    expect(recordOf(view, "orders.parquet").ownerRole).toBeUndefined();
    expect(recordOf(view, "orders.parquet").createdBy).toBeUndefined();
    for (const t of ["clean_customers", "clean_orders", "daily_sales"] as const)
      expect(recordOf(view, t).ownerRole).toBe("etl_service");
    expect(recordOf(view, "sales_dashboard").createdBy).toBe("j.marsh");
  });

  it("shows the analyst's copy only in the week that has it", () => {
    expect(storage().some((r) => r.asset === "clean_orders_copy.parquet")).toBe(false);
    expect(storage(week(["copy"])).some((r) => r.asset === "clean_orders_copy.parquet")).toBe(true);
  });
});

describe("what the data suggests", () => {
  const only = { source: "clean_orders", keep: "completed", measure: "revenue", per: "day" };

  it("finds one sum that reproduces daily_sales in the plain week", () => {
    expect(sumReconstructions(week(), "daily_sales")).toEqual([only]);
  });

  it("finds two equally good sources once the analyst's copy exists", () => {
    expect(sumReconstructions(week(["copy"]), "daily_sales").map((c) => c.source)).toEqual([
      "clean_orders",
      "clean_orders_copy.parquet",
    ]);
  });

  it("finds none after the unrecorded edit to daily sales", () => {
    expect(sumReconstructions(week(["refunds"]), "daily_sales", "covers")).toEqual([]);
  });

  it("still finds the source of every row a failed night left", () => {
    expect(sumReconstructions(week(["failed"]), "daily_sales", "exact")).toEqual([]);
    expect(sumReconstructions(week(["failed"]), "daily_sales", "covers")).toEqual([only]);
  });

  it("finds two sets of cleaning rules that fit, differing only in a rule the week never tests", () => {
    const fits = cleanReconstructions(week());
    expect(fits).toHaveLength(2);
    expect(new Set(fits.map((c) => c.quantity))).toEqual(new Set(["keep", "drop"]));
    for (const c of fits)
      expect(c).toMatchObject({ duplicates: "one", missingCustomer: "drop", cancelled: "keep" });
  });

  it("finds the dashboard showing daily_sales' numbers", () => {
    expect(sameNumbers(week(), "daily_sales")).toEqual(["sales_dashboard"]);
  });
});

describe("the questions", () => {
  const places = (changes: Parameters<typeof week>[0]) =>
    Object.fromEntries(questionMap(week(changes)).map((e) => [e.question, e.place]));

  it("places each question by what answers it", () => {
    expect(places([])).toEqual({
      "last-written": "storage",
      "made-from": "suggested",
      computed: "suggested",
      "read-by": "suggested",
      worked: "suggested",
      responsible: "record",
      unit: "record",
      changed: "record",
    });
  });

  it("moves where daily_sales comes from to 'only a record' after the unrecorded edit", () => {
    expect(places(["refunds"])).toMatchObject({ "made-from": "record", computed: "record" });
  });

  it("answers the predictions from the lab", () => {
    expect(runProbe({ kind: "owner-kind", asset: "daily_sales" }, week())).toMatchObject({
      answer: "account",
      value: "etl_service",
    });
    const days = runProbe(
      { kind: "days-matching", source: "orders.parquet", keep: "all", target: "daily_sales" },
      week(),
    );
    expect(days).toMatchObject({ answer: "some", total: 7 });
  });
});
