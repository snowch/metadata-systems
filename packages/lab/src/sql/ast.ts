// Copyright © 2026 Christopher Snow

// A parsed query. Every node keeps where it was written, so a problem can point at it and, from
// Chapter 9, a column's lineage can point at the expression that made it.

import type { Pos } from "./errors";
import type { SqlType } from "../values";

export type BinaryOp = "+" | "-" | "*" | "/" | "=" | "<>" | "<" | "<=" | ">" | ">=" | "AND" | "OR";

export const AGGREGATES = new Set(["sum", "count", "min", "max"]);
export const FUNCTIONS = new Set(["sum", "count", "min", "max", "lower", "upper", "coalesce"]);

export type Expr =
  | { readonly kind: "column"; readonly name: string; readonly at: Pos }
  | {
      readonly kind: "literal";
      readonly type: "integer" | "decimal" | "string" | "boolean" | "null";
      readonly text: string;
      readonly at: Pos;
    }
  | { readonly kind: "param"; readonly name: string; readonly at: Pos }
  | { readonly kind: "unary"; readonly op: "-" | "NOT"; readonly arg: Expr; readonly at: Pos }
  | {
      readonly kind: "binary";
      readonly op: BinaryOp;
      readonly left: Expr;
      readonly right: Expr;
      readonly at: Pos;
    }
  | { readonly kind: "isNull"; readonly arg: Expr; readonly negated: boolean; readonly at: Pos }
  | {
      readonly kind: "call";
      readonly name: string;
      readonly args: readonly Expr[];
      /** COUNT(*). */
      readonly star: boolean;
      readonly at: Pos;
    }
  | { readonly kind: "cast"; readonly arg: Expr; readonly to: SqlType; readonly at: Pos };

export interface SelectItem {
  readonly expr: Expr;
  readonly alias?: string;
}

export interface OrderItem {
  readonly expr: Expr;
  readonly descending: boolean;
}

export interface Query {
  readonly distinct: boolean;
  /** Undefined for `SELECT *`. */
  readonly items?: readonly SelectItem[];
  readonly from: { readonly name: string; readonly at: Pos };
  readonly where?: Expr;
  readonly groupBy: readonly Expr[];
  readonly orderBy: readonly OrderItem[];
}

/** Two expressions that say the same thing, wherever each was written. */
export function sameExpr(a: Expr, b: Expr): boolean {
  return JSON.stringify(strip(a)) === JSON.stringify(strip(b));
}

function strip(e: Expr): unknown {
  const { at: _at, ...rest } = e;
  const out: Record<string, unknown> = { ...rest };
  if ("arg" in e) out["arg"] = strip(e.arg);
  if (e.kind === "binary") {
    out["left"] = strip(e.left);
    out["right"] = strip(e.right);
  }
  if (e.kind === "call") out["args"] = e.args.map(strip);
  return out;
}

/** Whether an expression adds rows up anywhere inside it. */
export function hasAggregate(e: Expr): boolean {
  switch (e.kind) {
    case "call":
      return AGGREGATES.has(e.name) || e.args.some(hasAggregate);
    case "unary":
    case "isNull":
    case "cast":
      return hasAggregate(e.arg);
    case "binary":
      return hasAggregate(e.left) || hasAggregate(e.right);
    default:
      return false;
  }
}
