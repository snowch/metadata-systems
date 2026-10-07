// Copyright © 2026 Christopher Snow

// The shop's assets: where each lives and what kind of thing it is. An asset is anything in the
// platform that can be stored, described, changed, related to another or depended on; the shop's
// are files, tables and a dashboard.

export const ASSET_IDS = [
  "customers.parquet",
  "orders.parquet",
  "products.parquet",
  "clean_customers",
  "clean_orders",
  "daily_sales",
  "sales_dashboard",
  // Only when the analyst's copy is among a week's changes.
  "clean_orders_copy.parquet",
] as const;
export type AssetId = (typeof ASSET_IDS)[number];

export type AssetKind = "file" | "table" | "dashboard";
export type StorageSystem = "object-storage" | "warehouse" | "reporting";

export interface Asset {
  readonly id: AssetId;
  readonly kind: AssetKind;
  readonly system: StorageSystem;
  /** Where the asset lives, as its own system names it. */
  readonly location: string;
  /** When the warehouse table or the dashboard was created. */
  readonly created?: string;
}

export const ASSETS: Readonly<Record<AssetId, Asset>> = {
  "customers.parquet": {
    id: "customers.parquet",
    kind: "file",
    system: "object-storage",
    location: "s3://shop-raw/customers.parquet",
  },
  "orders.parquet": {
    id: "orders.parquet",
    kind: "file",
    system: "object-storage",
    location: "s3://shop-raw/orders.parquet",
  },
  "products.parquet": {
    id: "products.parquet",
    kind: "file",
    system: "object-storage",
    location: "s3://shop-raw/products.parquet",
  },
  clean_customers: {
    id: "clean_customers",
    kind: "table",
    system: "warehouse",
    location: "shop.analytics.clean_customers",
    created: "2026-09-01T10:12:00Z",
  },
  clean_orders: {
    id: "clean_orders",
    kind: "table",
    system: "warehouse",
    location: "shop.analytics.clean_orders",
    created: "2026-09-01T10:14:00Z",
  },
  daily_sales: {
    id: "daily_sales",
    kind: "table",
    system: "warehouse",
    location: "shop.analytics.daily_sales",
    created: "2026-09-01T10:20:00Z",
  },
  sales_dashboard: {
    id: "sales_dashboard",
    kind: "dashboard",
    system: "reporting",
    location: "reports/sales_dashboard",
    created: "2026-09-02T15:41:00Z",
  },
  "clean_orders_copy.parquet": {
    id: "clean_orders_copy.parquet",
    kind: "file",
    system: "object-storage",
    location: "s3://shop-scratch/clean_orders_copy.parquet",
  },
};

/** The account every program runs as, which the warehouse records as each table's owner. */
export const PROGRAM_ACCOUNT = "etl_service";
/** The member of staff who built the dashboard, which the reporting tool records. */
export const DASHBOARD_CREATOR = "j.marsh";
/** The dashboard's title in the reporting tool. */
export const DASHBOARD_TITLE = "Sales, last 7 days";
