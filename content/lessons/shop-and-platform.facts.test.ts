// Copyright © 2026 Christopher Snow

// Every number and name Chapter 1's words state, read off the engine. If the shop's data or
// programs change, this fails until the words change with them (brief AV, in
// docs/notes/chapter-01/briefs/, holds the facts the words were drafted from).

import { describe, expect, it } from "vitest";

import { ARRIVAL, DAYS, NIGHTS, mapTally, platformMap, storage, typeName, week } from "@ms/lab";

import { LABELS } from "./shop-and-platform.labels";
import { PROSE } from "./shop-and-platform.prose";
import { shopAndPlatform } from "./shop-and-platform";

const view = storage();
const record = (asset: string) => view.find((r) => r.asset === asset)!;
const columns = (asset: string) => record(asset).columns.map((c) => c.name);
const time = (ts: string) => ts.slice(11, 16);

describe("the facts Chapter 1 states", () => {
  it("names three systems in the order data moves, and counts the map's seven assets", () => {
    const m = platformMap(week());
    expect(m.systems.map((s) => s.system)).toEqual(["object-storage", "warehouse", "reporting"]);
    expect(PROSE.question).toContain(
      "three systems: object storage, which holds files; a warehouse, which holds tables; and a reporting tool, which holds a dashboard",
    );
    expect(mapTally(m).total).toBe(7);
    expect(PROSE.reflection).toContain("7 assets, 3 files, 3 tables and 1 dashboard");
    expect(m.systems.map((s) => s.assets.length)).toEqual([3, 3, 1]);
    // The word "asset" arrives under the map, and not before.
    for (const before of [PROSE.question, PROSE.platformLead]) expect(before).not.toMatch(/asset/i);
    expect(PROSE.platformAfter.startsWith("An asset is one thing the platform holds")).toBe(true);
  });

  it("gives the morning, the week and its nights as the engine has them", () => {
    expect(ARRIVAL).toBe("2026-09-14T09:00:00Z");
    expect(PROSE.question).toContain("Monday 14 September 2026 at 09:00");
    expect(PROSE.question).toContain("a week ago, on Monday 7 September");
    expect([DAYS[0], DAYS[DAYS.length - 1]]).toEqual(["2026-09-07", "2026-09-13"]);
    expect(PROSE.nights).toContain("Monday 7 to Sunday 13 September");
    expect(NIGHTS[NIGHTS.length - 1]).toBe("2026-09-14");
    const files = ["products.parquet", "customers.parquet", "orders.parquet"];
    const tables = ["clean_customers", "clean_orders", "daily_sales"];
    const times = (assets: string[]) => assets.map((a) => record(a).lastWritten).sort();
    const f = times(files);
    const t = times(tables);
    expect([time(f[0]!), f[f.length - 1]! < "2026-09-14T01:05"]).toEqual(["01:00", true]);
    expect([time(t[0]!), t[t.length - 1]! < "2026-09-14T02:31"]).toEqual(["02:00", true]);
    expect(time(record("sales_dashboard").lastWritten)).toBe("03:00");
    expect(PROSE.nights).toContain(
      "the files were written between 01:00 and 01:05, the three tables between 02:00 and 02:31, and the dashboard was refreshed at 03:00",
    );
  });

  it("describes each file as storage holds it", () => {
    for (const r of view.filter((x) => x.kind === "file"))
      expect(r.location.startsWith("s3://shop-raw/")).toBe(true);
    expect(PROSE.products).toContain("`s3://shop-raw/`");
    expect(record("products.parquet").rows).toBe(8);
    expect(columns("products.parquet")).toEqual([
      "product_id",
      "name",
      "category",
      "list_price",
      "updated_by",
    ]);
    expect(PROSE.products).toContain("with 8 rows, one per product");
    expect(record("customers.parquet").rows).toBe(10);
    expect(columns("customers.parquet")).toEqual([
      "customer_id",
      "name",
      "email",
      "country",
      "signed_up",
    ]);
    expect(PROSE.customers).toContain("It has 10 rows, one per customer, and five columns");
    expect(record("orders.parquet").rows).toBe(48);
    expect(columns("orders.parquet")).toHaveLength(7);
    expect(PROSE.orders).toContain("It has 48 rows, one per order line, and seven columns");
    const statuses = new Set(record("orders.parquet").content.rows.map((r) => r[5]));
    expect([...statuses].sort()).toEqual(["cancelled", "completed"]);
    expect(typeName(record("orders.parquet").columns[4]!.type)).toBe("decimal(10,2)");
  });

  it("describes the warehouse's tables and the dashboard as their systems hold them", () => {
    for (const t of ["clean_customers", "clean_orders", "daily_sales"])
      expect(record(t).location.startsWith("shop.analytics.")).toBe(true);
    expect(columns("clean_customers")).toEqual(columns("customers.parquet"));
    expect(columns("clean_orders")).toEqual(columns("orders.parquet"));
    expect(columns("daily_sales")).toEqual(["day", "revenue"]);
    expect(PROSE.warehouse).toContain(
      "`clean_customers` has the same columns as `customers.parquet`",
    );
    const d = record("sales_dashboard");
    expect([d.title, d.createdBy, d.created?.slice(0, 10)]).toEqual([
      "Sales, last 7 days",
      "j.marsh",
      "2026-09-02",
    ]);
    expect(PROSE.dashboard).toContain(
      'titled "Sales, last 7 days", and `j.marsh` created it on 2 September',
    );
    expect(PROSE.dashboard).toContain("last refreshed at 03:00 on Monday 14 September");
  });

  it("shows each file on its own card, the tables on theirs, and says what no card says", () => {
    const cards = shopAndPlatform.sections.flatMap((s) => s.interactives ?? []);
    const ids = cards
      .filter((x) => x.kind === "asset-cards")
      .flatMap((x) => (x.props as { cards: { id: string }[] }).cards.map((c) => c.id));
    expect(ids).toEqual([
      "products.parquet",
      "customers.parquet",
      "orders.parquet",
      "clean_customers",
      "clean_orders",
      "daily_sales",
    ]);
    // No role or caption says what an asset is made from: Chapter 2 asks what can establish it.
    for (const text of [...Object.values(LABELS.roles), ...Object.values(LABELS.captions)])
      expect(text).not.toMatch(/made from|built from|from the|cleaned|derived/i);
  });
});
