// Copyright © 2026 Christopher Snow

// The lab's behaviour that the course relies on. The numbers a chapter's prose states are pinned
// in that chapter's facts test; this file pins the mechanisms.

import { describe, expect, it } from "vitest";

import {
  ARRIVAL,
  ASSET_IDS,
  DAYS,
  DUPLICATED,
  NIGHTS,
  PROGRAMS,
  QUESTION_IDS,
  cleanReconstructions,
  columnValues,
  parseQuery,
  platformMap,
  optionForAnswer,
  optionForCount,
  mapTally,
  questionMap,
  recordKindOf,
  recordOf,
  runProbe,
  runWeek,
  sameNumbers,
  storage,
  storageAnswer,
  sumReconstructions,
  week,
  weekTimeline,
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

  it("compares a day's raw orders with the rows a rebuild keeps, order by order", () => {
    // Thursday: three orders are not among the rows the rebuild keeps, and are worth the whole
    // difference; the four it keeps have the same value, on the same day.
    expect(
      runProbe(
        {
          kind: "day-gap",
          source: "orders.parquet",
          via: "clean_orders",
          keep: "completed",
          target: "daily_sales",
          day: "2026-09-10",
        },
        week(),
      ),
    ).toEqual({
      kind: "day-gap",
      answer: ["left"],
      orders: 7,
      kept: 4,
      left: 3,
      lower: 0,
      moved: 0,
      leftTotal: "154.00",
      difference: "154.00",
    });
  });

  it("answers the predictions from the lab", () => {
    // Every table in the warehouse records the programs' account as its owner.
    expect(runProbe({ kind: "owner-kind", asset: "daily_sales" }, week())).toMatchObject({
      answer: "account",
      value: "etl_service",
      tables: 3,
      owned: 3,
    });
    const thursday = runProbe(
      {
        kind: "day-total",
        source: "orders.parquet",
        keep: "all",
        target: "daily_sales",
        day: "2026-09-10",
      },
      week(),
    );
    expect(thursday).toMatchObject({ answer: "more", day: "2026-09-10" });
    if (thursday.kind === "day-total") {
      expect(thursday.checks).toHaveLength(7);
      expect(thursday.checks.filter((c) => c.same)).toHaveLength(3);
    }
    const monday = runProbe(
      {
        kind: "day-total",
        source: "orders.parquet",
        keep: "all",
        target: "daily_sales",
        day: "2026-09-07",
      },
      week(),
    );
    expect(monday).toMatchObject({ answer: "same" });
    expect(runProbe({ kind: "clean-fits" }, week())).toEqual({ kind: "clean-fits", count: 2 });
  });

  it("maps the platform by system, in the order data moves, with no asset made from another", () => {
    const m = platformMap(week());
    expect(m.systems.map((s) => s.system)).toEqual(["object-storage", "warehouse", "reporting"]);
    expect(m.systems.map((s) => s.assets.map((a) => a.id))).toEqual([
      ["customers.parquet", "orders.parquet", "products.parquet"],
      ["clean_customers", "clean_orders", "daily_sales"],
      ["sales_dashboard"],
    ]);
    expect(m.flows).toEqual([
      { from: "object-storage", to: "warehouse" },
      { from: "warehouse", to: "reporting" },
    ]);
    // A flow names two systems and nothing else: no asset, no program.
    for (const f of m.flows) expect(Object.keys(f).sort()).toEqual(["from", "to"]);
    expect(platformMap(week(["copy"])).systems[0]?.assets.map((a) => a.id)).toContain(
      "clean_orders_copy.parquet",
    );
  });

  it("counts the map's assets by kind, in the order the map shows them", () => {
    expect(mapTally(platformMap(week()))).toEqual({
      kinds: [
        { kind: "file", count: 3 },
        { kind: "table", count: 3 },
        { kind: "dashboard", count: 1 },
      ],
      total: 7,
    });
    expect(mapTally(platformMap(week(["copy"]))).kinds[0]).toEqual({ kind: "file", count: 4 });
    expect(mapTally(platformMap(week(["copy"]))).total).toBe(8);
  });

  it("lays out the week: seven days, a night of work after each, and the morning you start", () => {
    const t = weekTimeline(week());
    expect(t.days).toEqual([...DAYS]);
    expect(t.nights.map((n) => n.after)).toEqual([...DAYS]);
    expect(t.nights.map((n) => n.date)).toEqual([...NIGHTS]);
    for (const n of t.nights) {
      // Each night's work falls in the early hours of the date after its day.
      expect(n.started.slice(0, 10)).toBe(n.date);
      expect(n.finished.slice(0, 10)).toBe(n.date);
      expect(n.started < n.finished).toBe(true);
      expect(n.finished.slice(11, 13) < "06").toBe(true);
      // It says when, and nothing about who wrote what.
      expect(Object.keys(n).sort()).toEqual(["after", "date", "finished", "started"]);
    }
    // The last night ends before the learner starts, and no write storage shows comes after it.
    const last = t.nights[t.nights.length - 1]!;
    expect(last.date).toBe("2026-09-14");
    expect(t.arrival).toBe(ARRIVAL);
    expect(last.finished < t.arrival).toBe(true);
    expect([...week().lastWritten.values()].every((at) => at <= last.finished)).toBe(true);
  });

  it("picks the option that stands for an answer, and none where two do", () => {
    const options = [
      { value: "yes", means: ["person", "team"] },
      { value: "no", means: ["account", "none"] },
    ];
    expect(optionForAnswer("team", options)).toBe("yes");
    expect(optionForAnswer("account", options)).toBe("no");
    expect(optionForAnswer("robot", options)).toBeUndefined();
    expect(optionForAnswer("same", [{ value: "same" }, { value: "more" }])).toBe("same");
    expect(
      optionForAnswer("x", [
        { value: "a", means: ["x"] },
        { value: "b", means: ["x"] },
      ]),
    ).toBeUndefined();
  });

  it("picks the option whose range holds a count, and none where two or none do", () => {
    const options = [
      { value: "few", range: [0, 3] as const },
      { value: "many", range: [4, 7] as const },
    ];
    expect(optionForCount(3, options)).toBe("few");
    expect(optionForCount(4, options)).toBe("many");
    expect(optionForCount(8, options)).toBeUndefined();
    expect(optionForCount(3, [...options, { value: "also", range: [3, 3] as const }])).toBe(
      undefined,
    );
  });

  it("asks every asset, the dashboard too, the same eight questions, with an answer to each", () => {
    for (const asset of ASSET_IDS) {
      const w = week(asset === "clean_orders_copy.parquet" ? ["copy"] : []);
      const r = recordOf(storage(w), asset);
      for (const q of QUESTION_IDS) expect(storageAnswer(q, r).kind).toBeTruthy();
    }
    const dashboard = recordOf(storage(week()), "sales_dashboard");
    expect(storageAnswer("computed", dashboard)).toEqual({
      kind: "title",
      title: "Sales, last 7 days",
    });
    expect(storageAnswer("responsible", dashboard)).toEqual({ kind: "creator", person: "j.marsh" });
    expect(storageAnswer("unit", dashboard)).toMatchObject({ kind: "types", column: "revenue" });
  });

  it("gives every question the kind of record that would answer it", () => {
    expect(Object.fromEntries(QUESTION_IDS.map((q) => [q, recordKindOf(q)]))).toEqual({
      "last-written": "what-happened",
      "made-from": "made-from-what",
      computed: "made-from-what",
      "read-by": "made-from-what",
      worked: "what-happened",
      responsible: "what-it-is",
      unit: "what-it-is",
      changed: "what-happened",
    });
  });
});
