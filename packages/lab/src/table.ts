// Copyright © 2026 Christopher Snow

// A table: named, typed columns and rows of values, in the order the rows were written.

import { formatValue, type SqlType, type Value } from "./values";

export interface Column {
  readonly name: string;
  readonly type: SqlType;
}

export interface Table {
  readonly columns: readonly Column[];
  readonly rows: readonly (readonly Value[])[];
}

export function columnIndex(table: Table, name: string): number {
  return table.columns.findIndex((c) => c.name === name);
}

/** One column's values, top to bottom. */
export function columnValues(table: Table, name: string): Value[] {
  const i = columnIndex(table, name);
  if (i < 0) throw new Error(`no column ${name}`);
  return table.rows.map((r) => r[i] ?? null);
}

/** A row as text, each value formatted by its column's type. */
export function formatRow(table: Table, row: readonly Value[]): string[] {
  return table.columns.map((c, i) => formatValue(row[i] ?? null, c.type));
}

/** A key for a row: equal rows have equal keys. */
export const rowKey = (row: readonly Value[]) => JSON.stringify(row);
