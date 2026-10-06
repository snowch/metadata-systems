// Copyright © 2026 Christopher Snow

// The shop's week, run night by night.
//
// Each night (the early hours of Tuesday 8 to Monday 14 September) the export writes the three
// raw files, then the four programs run in order. The result is every asset's contents and
// last-written time as the learner finds them on Monday morning, and every execution of the week,
// which storage does not keep and which later chapters turn into runs.
//
// A change is applied to the shop's definition before the week runs, so a changed week is as
// deterministic as the plain one.

import { DATE, decimal, type SqlType } from "../values";
import type { Table } from "../table";
import { runSql, catalogueOf } from "../sql";
import { ASSETS, type AssetId } from "./assets";
import { CUSTOMERS, DAYS, DUPLICATED, ORDER_COLUMNS, ORDER_ROWS, PRODUCTS, dayOf } from "./data";
import {
  ANALYST_COPY,
  DAILY_SALES_FOR_REFUNDS,
  NIGHTLY,
  PROGRAMS,
  type ProgramId,
} from "./programs";

export const CHANGE_IDS = ["copy", "refunds", "failed"] as const;
export type ChangeId = (typeof CHANGE_IDS)[number];

/** The nights of the week: the date each night's work starts on, Tuesday 8 to Monday 14. */
export const NIGHTS = [...DAYS.slice(1), "2026-09-14"] as const;

/** The day before a night: the day whose orders that night's daily sales adds up. */
export const dayBefore = (night: string) =>
  DAYS[NIGHTS.indexOf(night as (typeof NIGHTS)[number])] as string;

export type Writer = ProgramId | "export" | "analyst_copy";

export interface Execution {
  readonly writer: Writer;
  readonly night: string;
  /** For daily sales: the day it added up. */
  readonly day?: string;
  readonly started: string;
  readonly finished: string;
  readonly status: "succeeded" | "failed";
  readonly wrote?: AssetId;
  readonly rows?: number;
  readonly sql?: string;
}

export interface Week {
  readonly changes: readonly ChangeId[];
  /** Every asset's contents on Monday morning, for the assets that exist this week. */
  readonly tables: ReadonlyMap<AssetId, Table>;
  readonly lastWritten: ReadonlyMap<AssetId, string>;
  readonly executions: readonly Execution[];
}

/** How long each writer takes, in seconds: fixed, so every time the lab shows is the same. */
const DURATION: Record<Writer, number> = {
  export: 41,
  clean_customers: 38,
  clean_orders: 52,
  analyst_copy: 17,
  daily_sales: 21,
  dashboard_refresh: 9,
};

/** When each writer starts, UTC; the export writes its three files a minute or two apart. */
const STARTS: Record<Exclude<Writer, ProgramId>, string> = {
  export: "01:00",
  analyst_copy: "02:15",
};

export function timestamp(day: string, time: string, plusSeconds = 0): string {
  const [h, m] = time.split(":").map(Number) as [number, number];
  const [y, mo, d] = day.split("-").map(Number) as [number, number, number];
  const ms = Date.UTC(y, mo - 1, d, h, m, 0) + plusSeconds * 1000;
  return new Date(ms).toISOString().replace(".000Z", "Z");
}

const DAILY_SALES_COLUMNS = [
  { name: "day", type: DATE as SqlType },
  { name: "revenue", type: decimal(18, 2) as SqlType },
];

/** The raw orders file as the export writes it on a night: every order placed before it. */
function exportedOrders(night: string): Table {
  const rows: (typeof ORDER_ROWS)[number][] = [];
  for (const row of ORDER_ROWS) {
    if (dayOf(row) >= night) continue;
    rows.push(row);
    if (row[0] === DUPLICATED) rows.push(row);
  }
  return { columns: ORDER_COLUMNS, rows };
}

export function runWeek(changes: readonly ChangeId[] = []): Week {
  const has = (c: ChangeId) => changes.includes(c);
  const tables = new Map<AssetId, Table>([
    ["clean_customers", { columns: CUSTOMERS.columns, rows: [] }],
    ["clean_orders", { columns: ORDER_COLUMNS, rows: [] }],
    ["daily_sales", { columns: DAILY_SALES_COLUMNS, rows: [] }],
    ["sales_dashboard", { columns: DAILY_SALES_COLUMNS, rows: [] }],
  ]);
  const lastWritten = new Map<AssetId, string>();
  for (const id of tables.keys()) {
    const created = ASSETS[id].created;
    if (created) lastWritten.set(id, created);
  }
  const executions: Execution[] = [];
  const catalogue = () => catalogueOf(Object.fromEntries(tables) as Record<string, Table>);

  const write = (asset: AssetId, table: Table, at: string) => {
    tables.set(asset, table);
    lastWritten.set(asset, at);
  };

  for (const night of NIGHTS) {
    // The export: three files, a minute or two apart.
    const files: [AssetId, Table][] = [
      ["orders.parquet", exportedOrders(night)],
      ["customers.parquet", CUSTOMERS],
      ["products.parquet", PRODUCTS],
    ];
    files.forEach(([asset, table], k) => {
      const started = timestamp(night, STARTS.export, k * 120);
      const finished = timestamp(night, STARTS.export, k * 120 + DURATION.export);
      write(asset, table, finished);
      executions.push({
        writer: "export",
        night,
        started,
        finished,
        status: "succeeded",
        wrote: asset,
        rows: table.rows.length,
      });
    });

    for (const id of NIGHTLY) {
      // The analyst's copy runs after clean orders and before daily sales.
      if (id === "daily_sales" && has("copy")) {
        const started = timestamp(night, STARTS.analyst_copy);
        const finished = timestamp(night, STARTS.analyst_copy, DURATION.analyst_copy);
        const copy = runSql(ANALYST_COPY, catalogue());
        write("clean_orders_copy.parquet", copy, finished);
        executions.push({
          writer: "analyst_copy",
          night,
          started,
          finished,
          status: "succeeded",
          wrote: "clean_orders_copy.parquet",
          rows: copy.rows.length,
          sql: ANALYST_COPY,
        });
      }
      const program = PROGRAMS[id];
      const started = timestamp(night, program.at);
      const finished = timestamp(night, program.at, DURATION[id]);
      const day = dayBefore(night);
      if (id === "daily_sales" && has("failed") && night === NIGHTS[NIGHTS.length - 1]) {
        executions.push({
          writer: id,
          night,
          day,
          started,
          finished,
          status: "failed",
          sql: program.sql,
        });
        continue;
      }
      const sql =
        id === "daily_sales" && has("refunds") && day >= "2026-09-12"
          ? DAILY_SALES_FOR_REFUNDS
          : program.sql;
      const result = runSql(sql, catalogue(), { day: { type: DATE, value: day } });
      if (program.mode === "append") {
        const before = tables.get(program.writes) as Table;
        write(
          program.writes,
          { columns: before.columns, rows: [...before.rows, ...result.rows] },
          finished,
        );
      } else {
        write(program.writes, result, finished);
      }
      executions.push({
        writer: id,
        night,
        ...(id === "daily_sales" ? { day } : {}),
        started,
        finished,
        status: "succeeded",
        wrote: program.writes,
        rows: result.rows.length,
        sql,
      });
    }
  }
  return { changes: [...changes], tables, lastWritten, executions };
}
