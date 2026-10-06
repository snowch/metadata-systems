// Copyright © 2026 Christopher Snow

// What the data suggests: inference from contents alone.
//
// The learner's two constructions in Chapter 1 are searches the lab can run exhaustively: a sum
// over one asset (which rows, which number, per what), and a set of cleaning rules over the raw
// orders. Each choice is written as SQL in the course's subset and run over Monday's storage, so
// the lab can list every choice that reproduces an asset, and a figure can show that two different
// sources fit equally well, or that none does.

import { SqlError, execute, parseQuery, quoteName, type Catalogue, type SqlProblem } from "./sql";
import { formatRow, rowKey, type Table } from "./table";
import { formatValue } from "./values";
import { ASSET_IDS, ASSETS, type AssetId } from "./shop/assets";
import type { Week } from "./shop/week";
import { catalogueFor } from "./lab";

export const KEEP = ["all", "completed", "cancelled"] as const;
export const MEASURE = ["revenue", "quantity", "rows"] as const;
export const PER = ["day", "customer", "product"] as const;
export type Keep = (typeof KEEP)[number];
export type Measure = (typeof MEASURE)[number];
export type Per = (typeof PER)[number];

/** A sum over one asset: which rows to keep, what to add up, and per what. */
export interface SumChoice {
  readonly source: AssetId;
  readonly keep: Keep;
  readonly measure: Measure;
  readonly per: Per;
}

const KEY: Record<Per, { expr: string; alias: string }> = {
  day: { expr: "CAST(ordered_at AS DATE)", alias: "day" },
  customer: { expr: "customer_id", alias: "customer_id" },
  product: { expr: "product_id", alias: "product_id" },
};

const VALUE: Record<Measure, string> = {
  revenue: "SUM(price * quantity) AS revenue",
  quantity: "SUM(quantity) AS quantity",
  rows: "COUNT(*) AS orders",
};

export function sumSql(c: SumChoice): string {
  const key = KEY[c.per];
  const select = c.per === "day" ? `${key.expr} AS ${key.alias}` : key.expr;
  const where = c.keep === "all" ? "" : `\nWHERE status = '${c.keep}'`;
  return `SELECT ${select}, ${VALUE[c.measure]}\nFROM ${quoteName(c.source)}${where}\nGROUP BY ${key.expr}\nORDER BY ${key.alias}`;
}

export type Outcome = { readonly table: Table } | { readonly problem: SqlProblem };

/** Runs SQL over Monday's storage: the table, or the problem that stopped it. */
export function runOver(sql: string, catalogue: Catalogue): Outcome {
  try {
    return { table: execute(parseQuery(sql), catalogue) };
  } catch (e) {
    if (e instanceof SqlError) return { problem: e.problem };
    throw e;
  }
}

/** One row of a target compared with a reconstruction, by its first column. */
export interface RowCheck {
  readonly key: string;
  readonly expected: string | null;
  readonly actual: string | null;
  readonly same: boolean;
}

/** The value of each row by its key, both as the lab writes them. */
function byKey(t: Table): Map<string, string> {
  const out = new Map<string, string>();
  const [k, v] = t.columns;
  if (!k || !v) return out;
  for (const row of t.rows)
    out.set(formatValue(row[0] ?? null, k.type), formatValue(row[1] ?? null, v.type));
  return out;
}

/**
 * The target's rows, each compared with the reconstruction's row of the same key, followed by
 * any key the reconstruction has and the target lacks.
 */
export function checkRows(result: Table | undefined, target: Table): RowCheck[] {
  const want = byKey(target);
  const got = result ? byKey(result) : new Map<string, string>();
  const out: RowCheck[] = [];
  for (const [key, expected] of want) {
    const actual = got.get(key) ?? null;
    out.push({ key, expected, actual, same: actual === expected });
  }
  for (const [key, actual] of got)
    if (!want.has(key)) out.push({ key, expected: null, actual, same: false });
  return out;
}

/** "exact": the same rows. "covers": every row the target has, perhaps with more. */
export type Fit = "exact" | "covers";

export function fits(result: Table | undefined, target: Table, fit: Fit): boolean {
  const checks = checkRows(result, target);
  if (fit === "exact") return checks.length > 0 && checks.every((c) => c.same);
  const own = checks.filter((c) => c.expected !== null);
  return own.length > 0 && own.every((c) => c.same);
}

/** The assets a sum could be over this week: every table or file except the target. */
export function sumSources(w: Week, target: AssetId): AssetId[] {
  return ASSET_IDS.filter(
    (id) => id !== target && w.tables.has(id) && ASSETS[id].kind !== "dashboard",
  );
}

/** Every sum over this week's storage that reproduces the target. */
export function sumReconstructions(w: Week, target: AssetId, fit: Fit = "exact"): SumChoice[] {
  const goal = w.tables.get(target);
  if (!goal) return [];
  const catalogue = catalogueFor(w);
  const out: SumChoice[] = [];
  for (const source of sumSources(w, target))
    for (const keep of KEEP)
      for (const measure of MEASURE)
        for (const per of PER) {
          const c = { source, keep, measure, per };
          const r = runOver(sumSql(c), catalogue);
          if ("table" in r && fits(r.table, goal, fit)) out.push(c);
        }
  return out;
}

/** A set of rules for cleaning the raw orders. */
export interface CleanChoice {
  readonly duplicates: "keep" | "one";
  readonly missingCustomer: "keep" | "drop";
  readonly cancelled: "keep" | "drop";
  readonly quantity: "keep" | "drop";
}

export const ORDER_FIELDS =
  "order_id, customer_id, product_id, quantity, price, status, ordered_at";

export function cleanSql(c: CleanChoice): string {
  const conditions: string[] = [];
  if (c.missingCustomer === "drop") conditions.push("customer_id IS NOT NULL");
  if (c.cancelled === "drop") conditions.push("status <> 'cancelled'");
  if (c.quantity === "drop") conditions.push("quantity > 0");
  const where = conditions.length ? `\nWHERE ${conditions.join(" AND ")}` : "";
  return `SELECT ${c.duplicates === "one" ? "DISTINCT " : ""}${ORDER_FIELDS}\nFROM "orders.parquet"${where}`;
}

/** The rows a cleaning drops that the target keeps, and keeps that the target drops, by order id. */
export interface RowDiff {
  readonly missing: readonly string[];
  readonly extra: readonly string[];
}

/** Compares two tables row by row as multisets, naming rows by their first column. */
export function diffRows(result: Table, target: Table): RowDiff {
  const counts = new Map<string, number>();
  for (const row of target.rows) counts.set(rowKey(row), (counts.get(rowKey(row)) ?? 0) + 1);
  const extra: string[] = [];
  for (const row of result.rows) {
    const k = rowKey(row);
    const n = counts.get(k) ?? 0;
    if (n > 0) counts.set(k, n - 1);
    else extra.push(formatRow(result, row)[0] ?? "");
  }
  const missing: string[] = [];
  for (const row of target.rows) {
    const k = rowKey(row);
    const n = counts.get(k) ?? 0;
    if (n > 0) {
      missing.push(formatRow(target, row)[0] ?? "");
      counts.set(k, n - 1);
    }
  }
  return { missing, extra };
}

export const CLEAN_SPACE: readonly CleanChoice[] = (["keep", "one"] as const).flatMap(
  (duplicates) =>
    (["keep", "drop"] as const).flatMap((missingCustomer) =>
      (["keep", "drop"] as const).flatMap((cancelled) =>
        (["keep", "drop"] as const).map((quantity) => ({
          duplicates,
          missingCustomer,
          cancelled,
          quantity,
        })),
      ),
    ),
);

/** Every set of cleaning rules that turns this week's raw orders into its clean orders. */
export function cleanReconstructions(w: Week): CleanChoice[] {
  const goal = w.tables.get("clean_orders");
  if (!goal) return [];
  const catalogue = catalogueFor(w);
  return CLEAN_SPACE.filter((c) => {
    const r = runOver(cleanSql(c), catalogue);
    if (!("table" in r)) return false;
    const d = diffRows(r.table, goal);
    return d.missing.length === 0 && d.extra.length === 0;
  });
}

/** Assets whose contents show every row of the target, by the same column names. */
export function sameNumbers(w: Week, target: AssetId): AssetId[] {
  const goal = w.tables.get(target);
  if (!goal) return [];
  const names = goal.columns.map((c) => c.name).join(",");
  return ASSET_IDS.filter((id) => {
    if (id === target) return false;
    const t = w.tables.get(id);
    if (!t || t.columns.map((c) => c.name).join(",") !== names) return false;
    return fits(t, goal, "exact");
  });
}
