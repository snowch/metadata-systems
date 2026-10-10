// Copyright © 2026 Christopher Snow

// Every number Chapter 1's words state, read off the lab. If the shop's data or programs change,
// this fails until the words change with them (docs/notes/chapter-01/facts.md is the brief the
// words were drafted from). A number spelled as a word ("three days", "all seven rows") is pinned
// like a number written in figures, and so is a sentence that states what a record holds.

import { describe, expect, it } from "vitest";

import {
  ARRIVAL,
  DAYS,
  KEEP,
  NIGHTS,
  PROGRAM_IDS,
  QUESTION_IDS,
  catalogueFor,
  checkRows,
  cleanReconstructions,
  columnValues,
  formatValue,
  mapTally,
  platformMap,
  questionMap,
  recordOf,
  runOver,
  runProbe,
  storage,
  sumReconstructions,
  sumSql,
  week,
  weekTimeline,
} from "@ms/lab";

import { invisibleSystem } from "./invisible-system";
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
const [MON, TUE, WED, THU, FRI, SAT, SUN] = DAYS as readonly [
  string,
  string,
  string,
  string,
  string,
  string,
  string,
];

describe("the facts Chapter 1 states", () => {
  it("has seven assets with the stated row counts, four of them on the page's cards", () => {
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
    const bySystem = (system: string) => view.filter((r) => r.system === system).length;
    expect([bySystem("object-storage"), bySystem("warehouse"), bySystem("reporting")]).toEqual([
      3, 3, 1,
    ]);
    // The map in the opening counts them, kind by kind, as the lab does.
    expect(mapTally(platformMap(week()))).toEqual({
      kinds: [
        { kind: "file", count: 3 },
        { kind: "table", count: 3 },
        { kind: "dashboard", count: 1 },
      ],
      total: 7,
    });
    const opening = invisibleSystem.sections[0]!.interactives!;
    const map = opening.find((x) => x.id === "platform")!;
    expect(map.props).toMatchObject({ tally: true });
    // The cards show four of the seven, each an asset storage holds.
    const cards = (opening.find((x) => x.id === "explore")!.props as { cards: { id: string }[] })
      .cards;
    expect(cards.map((c) => c.id)).toEqual([
      "orders.parquet",
      "clean_orders",
      "daily_sales",
      "sales_dashboard",
    ]);
    for (const c of cards) expect(rows).toHaveProperty(c.id);
    expect(LABELS.captions.explore).toContain("Four of the platform's seven assets");
    expect(QUESTION_IDS).toHaveLength(8);
    expect(questionMap(week())).toHaveLength(8);
  });

  it("names three systems in the order data moves, with the assets the map counts", () => {
    const m = platformMap(week());
    expect(m.systems.map((s) => s.system)).toEqual(["object-storage", "warehouse", "reporting"]);
    expect(m.systems.map((s) => s.assets.length)).toEqual([3, 3, 1]);
    expect(PROSE.question).toContain(
      "three systems: object storage, which holds files; a warehouse, which holds tables; and a reporting tool, which holds a dashboard",
    );
    expect(PROSE.platformLead).toContain(
      "The three systems, in the order data moves through them each night",
    );
  });

  it("gives the first and last days of the week and the learner's first morning", () => {
    expect(ARRIVAL).toBe("2026-09-14T09:00:00Z");
    expect(PROSE.question).toContain("Monday 14 September 2026 at 09:00");
    expect(DAYS[0]).toBe("2026-09-07");
    expect(PROSE.question).toContain("a week ago, on Monday 7 September");
    expect(Object.keys(revenue())).toEqual([...DAYS]);
    expect(DAYS[DAYS.length - 1]).toBe("2026-09-13");
    expect(PROSE.weekLead).toContain("Monday 7 to Sunday 13 September");
    expect(LABELS.captions.dashboard).toContain("7 to 13 September");
    // The week's last night ends early on the Monday morning the learner arrives: every time
    // storage shows falls inside the week or that night, and the week's figure draws it so.
    expect(NIGHTS[NIGHTS.length - 1]).toBe("2026-09-14");
    const times = [...week().lastWritten.values()];
    expect(times.every((t) => t >= "2026-09-07" && t < "2026-09-14T06:00")).toBe(true);
    const line = weekTimeline(week());
    expect(line.nights.map((n) => n.date)).toEqual([...NIGHTS]);
    expect(line.nights[line.nights.length - 1]!.finished < ARRIVAL).toBe(true);
    expect(PROSE.weekLead).toContain("The last night ends early on Monday 14 September");
    // The opening, in the order the page gives it: the situation names the lab in its own prose;
    // how the lab runs waits behind a control; the word "asset" arrives under the map, and not
    // before; the week's dates come before any sentence speaks of its nights.
    expect(PROSE.labDetails).toContain("query engine");
    for (const before of [PROSE.question, PROSE.labDetails, PROSE.platformLead])
      expect(before).not.toMatch(/\basset/i);
    expect(PROSE.platformAfter.startsWith("An asset is")).toBe(true);
    const weekProse = PROSE.weekLead.toLowerCase();
    const dates = weekProse.indexOf("monday 7 to sunday 13 september");
    const night = weekProse.indexOf("night");
    expect(dates).toBeGreaterThan(-1);
    expect(dates).toBeLessThan(night);
  });

  it("shows Thursday's total against the days either side of it", () => {
    const r = revenue();
    expect([r[WED], r[THU], r[FRI]]).toEqual(["153.75", "51.50", "204.24"]);
    expect(PROSE.dashboardAfter).toBe(
      "Thursday shows 51.50, against 153.75 on Wednesday and 204.24 on Friday.",
    );
  });

  it("adds up the raw orders per day as the prose states: three days match, four do not", () => {
    const checks = rawChecks();
    const same = checks.filter((c) => c.same).map((c) => c.key);
    const differ = checks.filter((c) => !c.same).map((c) => c.key);
    expect(same).toEqual([MON, FRI, SUN]);
    expect(differ).toEqual([TUE, WED, THU, SAT]);
    const thu = checks.find((c) => c.key === THU)!;
    expect([thu.actual, thu.expected]).toEqual(["205.50", "51.50"]);
    expect((Number(thu.actual) - Number(thu.expected)).toFixed(2)).toBe("154.00");
    expect(PROSE.prediction).toContain("Thursday's orders add up to 205.50");
    expect(PROSE.prediction).toContain("its Thursday row says 51.50; the dashboard shows the same");
    expect(PROSE.prediction).toContain("154.00 went missing");
    expect(PROSE.prediction).toContain(
      "On Monday, Friday and Sunday the raw orders add up to the day's row in `daily_sales`. On Tuesday, Wednesday, Thursday and Saturday they do not.",
    );
    // The dashboard shows daily_sales's rows, value for value.
    const dash = recordOf(storage(), "sales_dashboard");
    expect(checkRows(dash.content, week().tables.get("daily_sales")!).every((c) => c.same)).toBe(
      true,
    );
    expect(PROSE.generalisation).toContain("the dashboard reads `daily_sales`");
  });

  it("reads the record of daily_sales as the warehouse keeps it, and no more", () => {
    const ds = recordOf(storage(), "daily_sales");
    expect(ds.content.columns.map((c) => c.name)).toEqual(["day", "revenue"]);
    expect(ds.rows).toBe(7);
    expect(ds.sizeBytes).toBeGreaterThan(0);
    expect(ds.created?.slice(0, 10)).toBe("2026-09-01");
    expect(ds.lastWritten).toBe("2026-09-14T02:30:21Z");
    expect(ds.ownerRole).toBe("etl_service");
    // The record has these fields and no others the prose would have to name.
    expect(Object.keys(ds).sort()).toEqual(
      [
        "asset",
        "columns",
        "content",
        "created",
        "kind",
        "lastWritten",
        "location",
        "ownerRole",
        "rows",
        "sizeBytes",
        "system",
      ].sort(),
    );
    expect(PROSE.investigation).toContain(
      "two columns, `day` and `revenue`, with their types; 7 rows and a size in bytes; a created time, 1 September, and a last-altered time, 02:30 on Monday 14 September; and an owner, `etl_service`",
    );
    expect(PROSE.handover).toContain(
      "two column names, a row count, a size, two times and an account",
    );
    // A file's record: location, size and last-modified; no owner, creator or title.
    const file = recordOf(storage(), "orders.parquet");
    expect(file.location).toMatch(/^s3:\/\//);
    expect(file.sizeBytes).toBeGreaterThan(0);
    expect(file.lastWritten.slice(0, 10)).toBe("2026-09-14");
    for (const k of ["ownerRole", "created", "createdBy", "title"])
      expect(file).not.toHaveProperty(k);
    expect(PROSE.investigation).toContain("its location, its size and when it was last modified");
    // The dashboard's record: title, creator, created, last refreshed, and the values.
    const dash = recordOf(storage(), "sales_dashboard");
    expect(dash.title).toBeTruthy();
    expect(dash.createdBy).toBeTruthy();
    expect(dash.created).toBeTruthy();
    expect(dash.lastWritten).toBe("2026-09-14T03:00:09Z");
    expect(dash.rows).toBe(7);
    expect(PROSE.investigation).toContain(
      "the dashboard's title, who created it and when, when it last refreshed, and the values it shows",
    );
  });

  it("names etl_service as the owner of all three tables, the account four programs share", () => {
    for (const t of ["clean_customers", "clean_orders", "daily_sales"] as const)
      expect(recordOf(storage(), t).ownerRole).toBe("etl_service");
    expect(PROGRAM_IDS).toHaveLength(4);
    const found = runProbe({ kind: "owner-kind", asset: "daily_sales" }, week());
    // The record names an account: not a person, not a team, not nothing.
    expect(found).toMatchObject({ answer: "account", value: "etl_service" });
    expect(PROSE.construction).toContain(
      "The warehouse answers `etl_service`, the account that all four of the shop's programs log in as",
    );
    expect(PROSE.construction).toContain("which account controls the table");
    // The question the owner finding answers is one of the four the motivation asks.
    expect(PROSE.motivation).toContain("- Who should I ask about `daily_sales`?");
    expect(PROSE.construction).toContain('"Who should I ask about `daily_sales`?"');
  });

  it("names the one query that rebuilds daily_sales, and the three orders it explains", () => {
    expect(sumReconstructions(week(), "daily_sales")).toEqual([
      { source: "clean_orders", keep: "completed", measure: "revenue", per: "day" },
    ]);
    expect(PROSE.failureExperiment).toContain(
      "read `clean_orders`, keep the completed orders, add up price times quantity per day. It reproduces `daily_sales` exactly, all seven rows",
    );
    expect(PROSE.generalisation).toContain(
      "`daily_sales` is built from the completed orders in `clean_orders`",
    );
    const raw = week().tables.get("orders.parquet")!;
    const noCustomer = raw.rows.filter((r) => r[1] === null && String(r[6]).startsWith(THU));
    expect(noCustomer.map((r) => r[0])).toEqual([7021, 7023, 7025]);
    const worth = noCustomer.reduce((s, r) => s + Number(r[3]) * Number(r[4]), 0);
    expect(formatValue(worth, raw.columns[4]!.type)).toBe("154.00");
    const gap = runProbe(
      {
        kind: "day-gap",
        source: "orders.parquet",
        via: "clean_orders",
        keep: "completed",
        target: "daily_sales",
        day: THU,
      },
      week(),
    );
    expect(gap).toMatchObject({ orders: 7, kept: 4, left: 3, lower: 0, moved: 0 });
    expect(gap.kind === "day-gap" && [gap.leftTotal, gap.difference]).toEqual(["154.00", "154.00"]);
    expect(PROSE.failureExperiment).toContain(
      "three of Thursday's orders arrived with no customer id, `clean_orders` does not have them, and they are worth 154.00",
    );
  });

  it("states the analyst's copy as the lab makes it: two sources fit the same query", () => {
    const w = week(["copy"]);
    expect(sumReconstructions(w, "daily_sales")).toEqual([
      { source: "clean_orders", keep: "completed", measure: "revenue", per: "day" },
      { source: "clean_orders_copy.parquet", keep: "completed", measure: "revenue", per: "day" },
    ]);
    const copy = recordOf(storage(w), "clean_orders_copy.parquet");
    expect(copy.location).toMatch(/^s3:\/\/shop-scratch\//);
    expect(copy.rows).toBe(recordOf(storage(w), "clean_orders").rows);
    expect(PROSE.failureExperiment).toContain(
      "An analyst copies `clean_orders` to a scratch bucket every night. Now the same query over the copy reproduces `daily_sales` too.",
    );
  });

  it("states the edited program as the lab makes it: Saturday changes, the record does not", () => {
    const before = revenue();
    const after = revenue(["refunds"]);
    expect([before[SAT], after[SAT]]).toEqual(["191.49", "215.49"]);
    for (const d of DAYS) if (d !== SAT) expect(after[d]).toBe(before[d]);
    const ds = recordOf(storage(week(["refunds"])), "daily_sales");
    const base = recordOf(storage(), "daily_sales");
    expect(ds.rows).toBe(7);
    expect(ds.lastWritten).toBe(base.lastWritten);
    expect(sumReconstructions(week(["refunds"]), "daily_sales")).toEqual([]);
    // Saturday changes because cancelled orders count from then on; the shop has no refunds.
    const raw = week().tables.get("orders.parquet")!;
    const status = columnValues(raw, "status");
    expect(status).not.toContain("refunded");
    expect(raw.rows.some((r) => r[5] === "cancelled" && String(r[6]).startsWith(SAT))).toBe(true);
    expect(PROSE.failureExperiment).toContain(
      "from Saturday every order counts, cancelled ones included. Saturday's row becomes 215.49 instead of 191.49. The table still has 7 rows and the same last-altered time, and no simple query over the week's assets reproduces it any more.",
    );
    // What "no simple query" means, as the note says: the sums' three ways of keeping rows.
    expect([...KEEP]).toEqual(["all", "completed", "cancelled"]);
    expect(PROSE.modelVsReality).toContain(
      "none that keeps every row, completed orders or cancelled orders of one asset",
    );
  });

  it("states the failed night as the lab makes it", () => {
    const w = week(["failed"]);
    const ds = recordOf(storage(w), "daily_sales");
    expect(ds.rows).toBe(6);
    expect(ds.lastWritten.slice(0, 16)).toBe("2026-09-13T02:30");
    expect(columnValues(ds.content, "day")).not.toContain(SUN);
    expect(recordOf(storage(w), "clean_orders").lastWritten.slice(0, 10)).toBe("2026-09-14");
    expect(time(recordOf(storage(w), "clean_orders").lastWritten)).toBe("02:05");
    const dash = recordOf(storage(w), "sales_dashboard");
    expect(dash.rows).toBe(6);
    expect(dash.lastWritten).toBe("2026-09-14T03:00:09Z");
    // "As usual": the dashboard refreshed at the same time on the week as it first ran.
    expect(time(recordOf(storage(), "sales_dashboard").lastWritten)).toBe("03:00");
    expect(sumReconstructions(w, "daily_sales", "covers")).toHaveLength(1);
    expect(PROSE.failureExperiment).toContain(
      "The table has 6 rows, none for Sunday, and was last altered on Sunday at 02:30, a day earlier than `clean_orders` and the dashboard. The dashboard refreshed at 03:00 on Monday as usual and shows the 6 values it found.",
    );
  });

  it("counts the three changes' outcomes as the close states them", () => {
    const counts = (["copy", "refunds", "failed"] as const).map(
      (c) => sumReconstructions(week([c]), "daily_sales", "covers").length,
    );
    expect(counts).toEqual([2, 0, 1]);
    expect(PROSE.failureExperiment).toContain("three small changes to the shop");
    expect(PROSE.reflection).toContain(
      "three ordinary changes made it ambiguous, made it wrong, or left a failed night looking like a normal one",
    );
  });

  it("finds two settings of the cleaning rules that pass, differing only in the quantity rule", () => {
    const fits = cleanReconstructions(week());
    expect(fits).toHaveLength(2);
    expect(new Set(fits.map((c) => c.quantity))).toEqual(new Set(["keep", "drop"]));
    expect(fits.every((c) => c.duplicates === "one")).toBe(true);
    expect(fits.every((c) => c.missingCustomer === "drop")).toBe(true);
    expect(fits.every((c) => c.cancelled === "keep")).toBe(true);
    const raw = week().tables.get("orders.parquet")!;
    expect(columnValues(raw, "quantity").every((q) => Number(q) > 0)).toBe(true);
    const ids = columnValues(raw, "order_id");
    expect(ids.filter((id) => id === 7015)).toHaveLength(2);
    expect(PROSE.explanation).toContain(
      "keep one row of an order the export wrote twice, drop orders with no customer id, keep cancelled orders, and drop orders with a quantity of 0 or less",
    );
    expect(PROSE.explanation).toContain("No order in the week has a quantity of 0 or less");
  });
});
