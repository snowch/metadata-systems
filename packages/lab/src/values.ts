// Copyright © 2026 Christopher Snow

// Values and their types, as the lab's tables and its SQL hold them.
//
// A value is null, a boolean, a number or a string; what it means is its column's type. An
// integer is a whole number. A decimal is held as a whole number of its smallest unit (pennies,
// for a price with two places), so sums are exact. A date is "YYYY-MM-DD" and a timestamp
// "YYYY-MM-DDTHH:MM:SSZ", always UTC, so both sort as text and format the same in every browser.

export type SqlType =
  | { readonly kind: "integer"; readonly bits: 32 | 64 }
  | { readonly kind: "decimal"; readonly precision: number; readonly scale: number }
  | { readonly kind: "string" }
  | { readonly kind: "boolean" }
  | { readonly kind: "date" }
  | { readonly kind: "timestamp" };

export type Value = null | boolean | number | string;

export const INT32: SqlType = { kind: "integer", bits: 32 };
export const INT64: SqlType = { kind: "integer", bits: 64 };
export const STRING: SqlType = { kind: "string" };
export const BOOLEAN: SqlType = { kind: "boolean" };
export const DATE: SqlType = { kind: "date" };
export const TIMESTAMP: SqlType = { kind: "timestamp" };
export const decimal = (precision: number, scale: number): SqlType => ({
  kind: "decimal",
  precision,
  scale,
});

/** The type as a storage system writes it: int64, decimal(10,2), string, date, timestamp. */
export function typeName(t: SqlType): string {
  switch (t.kind) {
    case "integer":
      return `int${t.bits}`;
    case "decimal":
      return `decimal(${t.precision},${t.scale})`;
    default:
      return t.kind;
  }
}

export function sameType(a: SqlType, b: SqlType): boolean {
  return typeName(a) === typeName(b);
}

export const isNumeric = (t: SqlType) => t.kind === "integer" || t.kind === "decimal";

/** The number of decimal places a numeric type keeps: 0 for an integer. */
export const scaleOf = (t: SqlType) => (t.kind === "decimal" ? t.scale : 0);

/** A decimal written with its places, from a whole number of its smallest unit: 1250 → "12.50". */
export function formatDecimal(units: number, scale: number): string {
  const negative = units < 0;
  const digits = String(Math.abs(units)).padStart(scale + 1, "0");
  const whole = digits.slice(0, digits.length - scale);
  const places = digits.slice(digits.length - scale);
  return `${negative ? "-" : ""}${whole}${scale > 0 ? `.${places}` : ""}`;
}

/** "12.5" as a whole number of the smallest unit of a decimal with `scale` places: 1250. */
export function parseDecimal(text: string, scale: number): number {
  const m = /^(-?)(\d+)(?:\.(\d+))?$/.exec(text.trim());
  if (!m) throw new Error(`not a decimal: ${text}`);
  const places = (m[3] ?? "").padEnd(scale, "0");
  if (places.length > scale) throw new Error(`${text} has more than ${scale} places`);
  const units = Number(`${m[2]}${places}`);
  return m[1] === "-" ? -units : units;
}

/** A value as the lab shows it: a decimal with its places, NULL for null, a time as stored. */
export function formatValue(v: Value, t: SqlType): string {
  if (v === null) return "NULL";
  if (t.kind === "decimal" && typeof v === "number") return formatDecimal(v, t.scale);
  return String(v);
}

/** Two values compared as their type orders them; null sorts first. */
export function compareValues(a: Value, b: Value): number {
  if (a === b) return 0;
  if (a === null) return -1;
  if (b === null) return 1;
  if (typeof a === "number" && typeof b === "number") return a - b;
  return String(a) < String(b) ? -1 : 1;
}
