// Copyright © 2026 Christopher Snow

// Every number Chapter 1's words state, read off the lab. If the shop's data or programs change,
// this fails until the words change with them (docs/notes/chapter-01/facts.md is the brief the
// words were drafted from). A number spelled as a word ("three days", "two settings") is pinned
// like a number written in figures.

import { describe, expect, it } from "vitest";

import {
  DAYS,
  PROGRAM_IDS,
  QUESTION_IDS,
  catalogueFor,
  checkRows,
  cleanReconstructions,
  columnValues,
  formatValue,
  platformMap,
  questionMap,
  recordOf,
  runOver,
  runProbe,
  storage,
  sumReconstructions,
  sumSources,
  sumSql,
  week,
} from "@ms/lab";
import { DEFAULT_VIEW_STRINGS } from "@ms/views";

import { LABELS } from "./invisible-system.labels";
import { PROSE } from "./invisible-system.prose";

const revenue = (changes: Parameters<typeof week>[0] = []) => {
  const t = week(changes).tables.get("daily_sales")!;
  return Object.fromEntries(
    t.rows.map((r) => [String(r[0]), formatValue(r[1] ?? null, t.columns[1]!.type)]),
  );
};

/** The raw orders added up per day, against daily_sales. */
const rawChecks = () => {
  const w = week();
  const r = runOver(
    sumSql({ source: "orders.parquet", keep: "all", measure: "revenue", per: "day" }),
    catalogueFor(w),
  );
  if (!("table" in r)) throw new Error("query failed");
  return checkRows(r.table, w.tables.get("daily_sales")!);
};

const time = (ts: string) => ts.slice(11, 16);

describe("the facts Chapter 1 states", () => {
  it("has seven assets with the stated row counts, asked eight questions each", () => {
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
    expect(PROSE.question).toContain("seven assets");
    const bySystem = (system: string) => view.filter((r) => r.system === system).length;
    expect([bySystem("object-storage"), bySystem("warehouse"), bySystem("reporting")]).toEqual([
      3, 3, 1,
    ]);
    expect(PROSE.question).toContain(
      "three files in object storage, three tables in the warehouse, one dashboard in the reporting tool",
    );
    expect(QUESTION_IDS).toHaveLength(8);
    expect(PROSE.inspectorLead).toContain("eight questions");
    expect(PROSE.mapLead).toContain("eight questions");
    expect(LABELS.captions.map).toContain("eight questions");
  });

  it("maps three systems in the order data moves, with the assets the prose counts", () => {
    const m = platformMap(week());
    expect(m.systems.map((s) => s.system)).toEqual(["object-storage", "warehouse", "reporting"]);
    expect(m.systems.map((s) => s.assets.length)).toEqual([3, 3, 1]);
    expect(PROSE.question).toContain("has three systems");
    expect(PROSE.question).toContain("in the order data moves through them each night");
  });

  it("gives the first and last days of the week and the learner's first morning", () => {
    expect(PROSE.question).toContain("Monday 14 September 2026 at 09:00");
    expect(PROSE.question).toContain("Monday 7 September");
    expect(Object.keys(revenue())).toEqual([...DAYS]);
    expect(DAYS[0]).toBe("2026-09-07");
    expect(DAYS[DAYS.length - 1]).toBe("2026-09-13");
    expect(LABELS.captions.dashboard).toContain("7 to 13 September");
    expect(DEFAULT_VIEW_STRINGS.labNote).toContain("7 to 13 September 2026");
  });

  it("matches raw orders to daily_sales on three days of seven, the ones the prose names", () => {
    const checks = rawChecks();
    expect(checks.filter((c) => c.same).map((c) => c.key)).toEqual([
      "2026-09-07",
      "2026-09-11",
      "2026-09-13",
    ]);
    expect(checks.filter((c) => !c.same).map((c) => c.key)).toEqual([
      "2026-09-08",
      "2026-09-09",
      "2026-09-10",
      "2026-09-12",
    ]);
    expect(PROSE.p2Explain).toContain("equal on three days (Monday, Friday and Sunday)");
    expect(PROSE.p2Explain).toContain("differ on four (Tuesday, Wednesday, Thursday and Saturday)");
  });

  it("asks about Thursday with the figures the dashboard and the raw orders give", () => {
    const dash = recordOf(storage(), "sales_dashboard");
    const thursday = dash.content.rows.find((r) => r[0] === "2026-09-10")!;
    expect(formatValue(thursday[1] ?? null, dash.content.columns[1]!.type)).toBe("51.50");
    expect(revenue()["2026-09-10"]).toBe("51.50");
    expect(PROSE.p2Question).toContain("The dashboard shows 51.50 for Thursday");
    expect(PROSE.p2Question).toContain("What do you expect the total to be?");
    expect(LABELS.p2Options.same).toMatch(/^51\.50:/);
    const raw = Object.fromEntries(rawChecks().map((c) => [c.key, c.actual]));
    expect([raw["2026-09-09"], raw["2026-09-10"], raw["2026-09-11"]]).toEqual([
      "198.75",
      "205.50",
      "204.24",
    ]);
    expect(PROSE.p2Explain).toContain("add up to 205.50. `daily_sales` holds 51.50 for Thursday");
    expect(PROSE.p2Explain).toContain("Wednesday's (198.75) and Friday's (204.24)");
  });

  it("names etl_service as the owner of all three tables", () => {
    for (const t of ["clean_customers", "clean_orders", "daily_sales"] as const)
      expect(recordOf(storage(), t).ownerRole).toBe("etl_service");
    // The figure's own line says it from the lab ("an owner for 3 of its 3 tables"), and the
    // explanation names the account the programs share.
    expect(PROSE.p1Lab).toContain("an owner for {owned} of its {tables} tables");
    expect(PROGRAM_IDS).toHaveLength(4);
    expect(PROSE.p1Explain).toContain("all four of the shop's programs");
  });

  it("meets the owner requirement as written, and answers only the last of its four readings", () => {
    const found = runProbe({ kind: "owner-kind", asset: "daily_sales" }, week());
    // Every table in the warehouse records an owner: the requirement as written is met.
    expect(found).toMatchObject({ value: "etl_service", tables: 3, owned: 3 });
    expect(PROSE.p1Explain).toContain("Every table has an owner");
    // Of the four readings, in the table's order, only the last is answered by an account.
    const readings = Object.keys(LABELS.p1Asks);
    expect(readings).toEqual(Object.keys(LABELS.p1Options));
    expect(readings).toHaveLength(4);
    expect(found.kind === "owner-kind" && found.answer).toBe(readings[readings.length - 1]);
    expect(PROSE.p1Explain).toContain(
      "Of the four questions above, `etl_service` answers only the last",
    );
    expect(PROSE.p1Meanings).toContain("Each of the first four choices");
    // The question it quotes from the start of the chapter is the motivation's own.
    expect(PROSE.motivation).toContain("Who should I ask about `daily_sales`?");
    expect(PROSE.p1Explain).toContain('"Who should I ask about `daily_sales`?"');
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
    expect(time(copy.lastWritten)).toBe("02:15");
    expect(sumReconstructions(week(["copy"]), "daily_sales", "covers")).toHaveLength(2);
    // The lead says the builder's choices cover every asset in storage that week.
    expect(sumSources(week(["copy"]), "daily_sales")).toContain("clean_orders_copy.parquet");
    expect(PROSE.changeLead).toContain("cover every asset in storage that week");
    expect(PROSE.outcomeCopy).toContain("last modified at 02:15, with the same 44 rows");
    expect(PROSE.outcomeCopy).toContain("Now 2 queries rebuild");
    expect(PROSE.afterAll).toContain("two assets fit equally well");
  });

  it("states the edit for refunds as the lab makes it", () => {
    const before = revenue();
    const after = revenue(["refunds"]);
    // The label says the edit holds from Saturday's row on: no earlier row changes.
    const changed = DAYS.filter((d) => before[d] !== after[d]);
    expect(changed).toEqual(["2026-09-12"]);
    expect(DAYS.indexOf("2026-09-12")).toBe(5);
    expect(LABELS.changeLabels.refunds).toContain("from Saturday's row on");
    expect([before["2026-09-12"], after["2026-09-12"]]).toEqual(["191.49", "215.49"]);
    expect([before["2026-09-13"], after["2026-09-13"]]).toEqual(["97.75", "97.75"]);
    const record = recordOf(storage(week(["refunds"])), "daily_sales");
    expect(record.rows).toBe(7);
    expect(record.lastWritten).toBe(recordOf(storage(), "daily_sales").lastWritten);
    expect(sumReconstructions(week(["refunds"]), "daily_sales", "covers")).toEqual([]);
    expect(PROSE.outcomeRefunds).toContain("Saturday's row now reads 215.49");
    expect(PROSE.outcomeRefunds).toContain("it read 191.49");
    expect(PROSE.outcomeRefunds).toContain("unchanged, 97.75");
    expect(PROSE.outcomeRefunds).toContain("the same 7 rows");
  });

  it("states the failed night as the lab makes it", () => {
    const w = week(["failed"]);
    const ds = recordOf(storage(w), "daily_sales");
    expect(ds.rows).toBe(6);
    expect(ds.lastWritten.slice(0, 16)).toBe("2026-09-13T02:30");
    expect(columnValues(ds.content, "day")).not.toContain("2026-09-13");
    expect(time(recordOf(storage(w), "clean_orders").lastWritten)).toBe("02:05");
    const dash = recordOf(storage(w), "sales_dashboard");
    expect(dash.rows).toBe(6);
    expect(dash.lastWritten.slice(0, 16)).toBe("2026-09-14T03:00");
    expect(sumReconstructions(w, "daily_sales", "covers")).toHaveLength(1);
    expect(PROSE.outcomeFailed).toContain("6 rows, with no row for Sunday");
    expect(PROSE.outcomeFailed).toContain("Sunday 13 September at 02:30");
    expect(PROSE.outcomeFailed).toContain("`clean_orders` (Monday at 02:05)");
    expect(PROSE.outcomeFailed).toContain("the dashboard (Monday at 03:00)");
    expect(PROSE.outcomeFailed).toContain("shows 6 values");
    expect(PROSE.outcomeFailed).toContain("the 6 rows");
  });

  it("answers the experiment's prediction with the counts the outcomes state", () => {
    const counts = (["copy", "refunds", "failed"] as const).map(
      (c) => sumReconstructions(week([c]), "daily_sales", "covers").length,
    );
    expect(counts).toEqual([2, 0, 1]);
  });

  it("moves two questions about what made daily_sales after the edit, as the prose says", () => {
    const place = (changes: Parameters<typeof week>[0]) =>
      Object.fromEntries(questionMap(week(changes)).map((e) => [e.question, e.place]));
    const before = place([]);
    const after = place(["refunds"]);
    const moved = QUESTION_IDS.filter((q) => before[q] !== after[q]);
    expect(moved).toEqual(["made-from", "computed"]);
    expect(PROSE.generalisation).toContain("two questions about what made `daily_sales`");
  });

  it("finds two settings of the cleaning rules that pass, differing only in the quantity rule", () => {
    const fits = cleanReconstructions(week());
    expect(fits).toHaveLength(2);
    expect(new Set(fits.map((c) => c.quantity))).toEqual(new Set(["keep", "drop"]));
    const raw = week().tables.get("orders.parquet")!;
    expect(columnValues(raw, "quantity").every((q) => Number(q) > 0)).toBe(true);
    expect(PROSE.p3Explain).toContain("Two settings pass");
    expect(PROSE.p3Explain).toContain("quantity of 0 or less");
    expect(PROSE.reflection).toContain("two settings of the rules rebuild `clean_orders`");
  });

  it("closes Thursday with the numbers the lab gives", () => {
    const thu = rawChecks().find((c) => c.key === "2026-09-10")!;
    expect([thu.actual, thu.expected]).toEqual(["205.50", "51.50"]);
    const raw = week().tables.get("orders.parquet")!;
    const noCustomer = raw.rows.filter(
      (r) => r[1] === null && String(r[6]).startsWith("2026-09-10"),
    );
    expect(noCustomer.map((r) => r[0])).toEqual([7021, 7023, 7025]);
    const worth = noCustomer.reduce((s, r) => s + Number(r[3]) * Number(r[4]), 0);
    expect(formatValue(worth, raw.columns[4]!.type)).toBe("154.00");
    expect(PROSE.reflection).toContain("Three orders on Thursday have no customer id");
    expect(PROSE.reflection).toContain("154.00");
    expect(PROSE.reflection).toContain("(205.50)");
    expect(PROSE.reflection).toContain("(51.50)");
  });

  it("states order 7015 as the order that appears twice", () => {
    const ids = columnValues(week().tables.get("orders.parquet")!, "order_id");
    expect(ids.filter((id) => id === 7015)).toHaveLength(2);
    expect(PROSE.c2Hints[2]).toContain("order 7015 appears twice");
  });
});
