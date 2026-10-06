// Copyright © 2026 Christopher Snow

// What storage records: for each asset, exactly the fields its system keeps, as of Monday
// morning (docs/lab.md, "Where its data lives"). This is all Chapter 1's learner can see.
//
// - Object storage keeps a file's location, size and last-modified time; a Parquet file's own
//   footer holds its columns, their types and its row count.
// - The warehouse keeps a table's columns and types, row count, size, last-altered and created
//   times, and the role that owns it.
// - The reporting tool keeps a dashboard's title, who created it and when, when it last
//   refreshed, and the values it shows.

import type { Column, Table } from "./table";
import type { SqlType } from "./values";
import {
  ASSETS,
  ASSET_IDS,
  DASHBOARD_CREATOR,
  DASHBOARD_TITLE,
  PROGRAM_ACCOUNT,
  type AssetId,
  type AssetKind,
  type StorageSystem,
} from "./shop/assets";
import type { Week } from "./shop/week";

export interface StorageRecord {
  readonly asset: AssetId;
  readonly kind: AssetKind;
  readonly system: StorageSystem;
  readonly location: string;
  /** From the file's footer, the warehouse's catalogue, or the chart's values. */
  readonly columns: readonly Column[];
  readonly rows: number;
  /** Files and tables: an estimate from the rows (the lab does not model bytes). */
  readonly sizeBytes?: number;
  /** Last modified, last altered or last refreshed. */
  readonly lastWritten: string;
  readonly created?: string;
  /** The warehouse's owning role. */
  readonly ownerRole?: string;
  /** The reporting tool's creator. */
  readonly createdBy?: string;
  readonly title?: string;
  /** The data itself: the rows, or the values the dashboard shows. */
  readonly content: Table;
}

const WIDTH: Record<SqlType["kind"], number> = {
  integer: 8,
  decimal: 8,
  date: 4,
  timestamp: 8,
  boolean: 1,
  string: 4,
};

/** A deterministic estimate of a file's or a table's size in bytes. */
export function estimateBytes(table: Table): number {
  let bytes = 512 + 64 * table.columns.length;
  for (const row of table.rows)
    table.columns.forEach((c, i) => {
      const v = row[i];
      if (v === null || v === undefined) return;
      const width = c.type.kind === "integer" ? c.type.bits / 8 : WIDTH[c.type.kind];
      bytes += width + (typeof v === "string" && c.type.kind === "string" ? v.length : 0);
    });
  return bytes;
}

export function storageView(week: Week): StorageRecord[] {
  const out: StorageRecord[] = [];
  for (const id of ASSET_IDS) {
    const content = week.tables.get(id);
    const lastWritten = week.lastWritten.get(id);
    if (!content || !lastWritten) continue;
    const a = ASSETS[id];
    const base = {
      asset: id,
      kind: a.kind,
      system: a.system,
      location: a.location,
      columns: content.columns,
      rows: content.rows.length,
      lastWritten,
      content,
    };
    if (a.system === "object-storage") out.push({ ...base, sizeBytes: estimateBytes(content) });
    else if (a.system === "warehouse")
      out.push({
        ...base,
        sizeBytes: estimateBytes(content),
        ...(a.created ? { created: a.created } : {}),
        ownerRole: PROGRAM_ACCOUNT,
      });
    else
      out.push({
        ...base,
        ...(a.created ? { created: a.created } : {}),
        createdBy: DASHBOARD_CREATOR,
        title: DASHBOARD_TITLE,
      });
  }
  return out;
}

export function recordOf(view: readonly StorageRecord[], asset: AssetId): StorageRecord {
  const r = view.find((x) => x.asset === asset);
  if (!r) throw new Error(`no asset ${asset} this week`);
  return r;
}
