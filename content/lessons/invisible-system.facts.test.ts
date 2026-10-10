// Copyright © 2026 Christopher Snow

// Every number Chapter 1's words state, read off the lab. If the shop's data or programs change,
// this fails until the words change with them (docs/notes/chapter-01/facts.md is the brief the
// words were drafted from). A number spelled as a word ("three days", "two settings") is pinned
// like a number written in figures.

import { describe, expect, it } from "vitest";

import {
  ARRIVAL,
  DAYS,
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
    // The book's investigation names the seven assets the reader can inspect.
    expect(PROSE.investigation).toContain("Nothing in them says how it came to be");
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
    const map = invisibleSystem.sections[0]!.interactives!.find((x) => x.id === "platform")!;
    expect(map.props).toMatchObject({ tally: true });
    expect(QUESTION_IDS).toHaveLength(8);
    // The generalisation's table lists a row per question, and the data suggests it: the
    // eight rows the lab places are all the questions there are.
    expect(questionMap(week())).toHaveLength(8);
  });

  it("maps three systems in the order data moves, with the assets the prose counts", () => {
    const m = platformMap(week());
    expect(m.systems.map((s) => s.system)).toEqual(["object-storage", "warehouse", "reporting"]);
    expect(m.systems.map((s) => s.assets.length)).toEqual([3, 3, 1]);
    expect(PROSE.platformLead).toContain("three systems");
    expect(PROSE.platformLead).toContain("data moves through them in this order");
  });

  it("gives the first and last days of the week and the learner's first morning", () => {
    expect(PROSE.question).toContain("its first Monday");
    expect(ARRIVAL).toBe("2026-09-14T09:00:00Z");
    expect(PROSE.weekLead).toContain("Monday 7 to Sunday 13 September");
    expect(Object.keys(revenue())).toEqual([...DAYS]);
    expect(DAYS[0]).toBe("2026-09-07");
    expect(DAYS[DAYS.length - 1]).toBe("2026-09-13");
    expect(LABELS.captions.dashboard).toContain("7 to 13 September");
    expect(PROSE.weekLead).toContain("Monday 7 to Sunday 13 September");
    // The week's last night ends early on the Monday morning the learner arrives: every time
    // storage shows falls inside the week or that night, and the week's figure draws it so.
    expect(NIGHTS[NIGHTS.length - 1]).toBe("2026-09-14");
    const times = [...week().lastWritten.values()];
    expect(times.every((t) => t >= "2026-09-07" && t < "2026-09-14T06:00")).toBe(true);
    const line = weekTimeline(week());
    expect(line.nights.map((n) => n.date)).toEqual([...NIGHTS]);
    expect(line.nights[line.nights.length - 1]!.finished < ARRIVAL).toBe(true);
    expect(PROSE.weekLead).toContain("The last night ends early on Monday 14 September");
    // The opening, in the order the page gives it, names the lab in its own prose, says when the
    // shop opened and when you start before any sentence speaks of its nights, and gives the
    // week's dates before any sentence says "the week".
    const opening = [
      PROSE.question,
      PROSE.labDetails,
      PROSE.platformLead,
      PROSE.platformAfter,
      PROSE.weekLead,
    ].join("\n\n");
    expect(PROSE.labDetails).toContain("query engine");
    const opened = opening.indexOf("Monday 7 to Sunday 13 September");
    expect(opened).toBeGreaterThan(-1);
    // The nightly work is discussed only after the week's dates are established: within the
    // week's own lead, the dates come first.
    const weekProse = PROSE.weekLead.toLowerCase();
    const dates = weekProse.indexOf("monday 7 to sunday 13 september");
    const night = weekProse.indexOf("night");
    expect(dates).toBeLessThan(night);
  });

  it("names etl_service as the owner of all three tables", () => {
    for (const t of ["clean_customers", "clean_orders", "daily_sales"] as const)
      expect(recordOf(storage(), t).ownerRole).toBe("etl_service");
    expect(PROGRAM_IDS).toHaveLength(4);
    // The construction states the account all four programs share, as the lab knows it.
    expect(PROSE.construction).toContain("the account its four programs log in as");
  });
  it("concludes only what the warehouse's record establishes about who to ask", () => {
    const found = runProbe({ kind: "owner-kind", asset: "daily_sales" }, week());
    // The record names an account: not a person, not a team, not nothing.
    expect(found).toMatchObject({ answer: "account", value: "etl_service" });
    // The essay states the finding, its evidence, and the question it does not answer.
    expect(PROSE.construction).toContain("records `etl_service` for all three of its tables");
    expect(PROSE.construction).toContain("an account four programs share");
    expect(PROSE.construction).toContain("a different question wearing the same word");
    // The motivation's four questions are the essay's; the construction answers the owner one.
    expect(PROSE.motivation).toContain(
      "Why does this dashboard exist? Whose decision does it serve?",
    );
    expect(PROSE.motivation).toContain("Who created this table, and for what purpose?");
  });
  it("names the one query that rebuilds daily_sales, as the essay claims", () => {
    expect(sumReconstructions(week(), "daily_sales")).toEqual([
      { source: "clean_orders", keep: "completed", measure: "revenue", per: "day" },
    ]);
    expect(PROSE.failureExperiment).toContain(
      "A query over `clean_orders` - keeping completed orders, adding up price times quantity per day - reproduces `daily_sales` exactly",
    );
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
    expect(PROSE.failureExperiment).toContain("6 rows, with no row for Sunday");
    expect(PROSE.failureExperiment).toContain("Sunday at 02:30");
    expect(PROSE.failureExperiment).toContain("a day before `clean_orders` and the dashboard");
    expect(PROSE.failureExperiment).toContain("shows 6 values");
    expect(PROSE.failureExperiment).toContain("a day behind");
  });

  it("answers the experiment's prediction with the counts the outcomes state", () => {
    const counts = (["copy", "refunds", "failed"] as const).map(
      (c) => sumReconstructions(week([c]), "daily_sales", "covers").length,
    );
    expect(counts).toEqual([2, 0, 1]);
  });

  it("finds two settings of the cleaning rules that pass, differing only in the quantity rule", () => {
    const fits = cleanReconstructions(week());
    expect(fits).toHaveLength(2);
    expect(new Set(fits.map((c) => c.quantity))).toEqual(new Set(["keep", "drop"]));
    const raw = week().tables.get("orders.parquet")!;
    expect(columnValues(raw, "quantity").every((q) => Number(q) > 0)).toBe(true);
    expect(PROSE.explanation).toContain("quantity of 0 or less");
    expect(PROSE.explanation).toContain("A rule that never fires leaves no evidence it exists");
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
    // The check gives the numbers, read from the rows: the three are the orders the rebuild's rows
    // leave out, and they are the whole difference.
    const gap = runProbe(
      {
        kind: "day-gap",
        source: "orders.parquet",
        via: "clean_orders",
        keep: "completed",
        target: "daily_sales",
        day: "2026-09-10",
      },
      week(),
    );
    expect(gap).toMatchObject({ orders: 7, kept: 4, left: 3, lower: 0, moved: 0 });
    expect(gap.kind === "day-gap" && [gap.leftTotal, gap.difference]).toEqual(["154.00", "154.00"]);
    expect(PROSE.failureExperiment).toContain(
      "A query over `clean_orders` - keeping completed orders, adding up price times quantity per day - reproduces `daily_sales` exactly",
    );
    // The reflection names them, after the rules challenge: both passing settings drop them.
    expect(PROSE.explanation).toContain("Two settings of the recovered rules pass the check");
    expect(cleanReconstructions(week()).every((r) => r.missingCustomer === "drop")).toBe(true);
  });

  it("states order 7015 as the order that appears twice", () => {
    const ids = columnValues(week().tables.get("orders.parquet")!, "order_id");
    expect(ids.filter((id) => id === 7015)).toHaveLength(2);
  });
});
