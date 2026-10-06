// Copyright © 2026 Christopher Snow

// The shop's programs, in the course's SQL subset. Each runs every night at its time, as the
// warehouse account `etl_service`, reads the assets its query names and writes one asset: it
// replaces the asset, or (daily sales) appends the rows for the day before.

import type { AssetId } from "./assets";

export const PROGRAM_IDS = [
  "clean_customers",
  "clean_orders",
  "daily_sales",
  "dashboard_refresh",
] as const;
export type ProgramId = (typeof PROGRAM_IDS)[number];

export interface Program {
  readonly id: ProgramId;
  readonly reads: readonly AssetId[];
  readonly writes: AssetId;
  /** Its time each night, UTC. */
  readonly at: string;
  readonly mode: "replace" | "append";
  readonly sql: string;
}

export const PROGRAMS: Readonly<Record<ProgramId, Program>> = {
  clean_customers: {
    id: "clean_customers",
    reads: ["customers.parquet"],
    writes: "clean_customers",
    at: "02:00",
    mode: "replace",
    sql: `SELECT customer_id, name, LOWER(email) AS email, country, signed_up
FROM "customers.parquet"
WHERE email IS NOT NULL`,
  },
  clean_orders: {
    id: "clean_orders",
    reads: ["orders.parquet"],
    writes: "clean_orders",
    at: "02:05",
    mode: "replace",
    sql: `SELECT DISTINCT order_id, customer_id, product_id, quantity, price, status, ordered_at
FROM "orders.parquet"
WHERE customer_id IS NOT NULL AND quantity > 0`,
  },
  daily_sales: {
    id: "daily_sales",
    reads: ["clean_orders"],
    writes: "daily_sales",
    at: "02:30",
    mode: "append",
    sql: `SELECT CAST(ordered_at AS DATE) AS day, SUM(price * quantity) AS revenue
FROM clean_orders
WHERE status = 'completed' AND CAST(ordered_at AS DATE) = :day
GROUP BY CAST(ordered_at AS DATE)`,
  },
  dashboard_refresh: {
    id: "dashboard_refresh",
    reads: ["daily_sales"],
    writes: "sales_dashboard",
    at: "03:00",
    mode: "replace",
    sql: `SELECT day, revenue
FROM daily_sales
ORDER BY day`,
  },
};

/** The order the programs run in each night. */
export const NIGHTLY: readonly ProgramId[] = [
  "clean_customers",
  "clean_orders",
  "daily_sales",
  "dashboard_refresh",
];

/**
 * The change to daily sales that the "refunds" scenario makes: every order whose status is not
 * "refunded", where the program kept completed orders. The shop has no refunds yet.
 */
export const DAILY_SALES_FOR_REFUNDS = `SELECT CAST(ordered_at AS DATE) AS day, SUM(price * quantity) AS revenue
FROM clean_orders
WHERE status <> 'refunded' AND CAST(ordered_at AS DATE) = :day
GROUP BY CAST(ordered_at AS DATE)`;

/** The analyst's copy: every row of clean_orders, written to the scratch bucket. */
export const ANALYST_COPY = `SELECT *
FROM clean_orders`;
