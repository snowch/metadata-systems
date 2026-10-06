// Copyright © 2026 Christopher Snow

// Runs a parsed query over the lab's tables.
//
// Types are worked out before any row is read, so a query that cannot run fails the same way on
// an empty table as on a full one. Values follow SQL's rules: NULL in arithmetic or a comparison
// gives NULL, WHERE keeps a row only when its condition is true, SUM and MIN ignore NULLs and give
// NULL for no values, COUNT(*) counts rows. Decimals are whole numbers of their smallest unit, so
// a sum of prices is exact.

import type { Table } from "../table";
import {
  BOOLEAN,
  INT64,
  STRING,
  compareValues,
  decimal,
  isNumeric,
  parseDecimal,
  scaleOf,
  typeName,
  type SqlType,
  type Value,
} from "../values";
import { AGGREGATES, hasAggregate, sameExpr, type Expr, type Query, type SelectItem } from "./ast";
import { SqlError } from "./errors";
import { formatExpr } from "./format";
import { parseQuery } from "./parser";

export interface Catalogue {
  /** The table or file a query names, or undefined. */
  find(name: string): Table | undefined;
}

export type Params = Readonly<Record<string, { readonly type: SqlType; readonly value: Value }>>;

/** A table from a map of names, for tests and figures. */
export function catalogueOf(tables: Readonly<Record<string, Table>>): Catalogue {
  return { find: (name) => tables[name] };
}

/** Parses and runs a query. */
export function runSql(sql: string, catalogue: Catalogue, params: Params = {}): Table {
  return execute(parseQuery(sql), catalogue, params);
}

/** The type the NULL literal has until something gives it one. */
type Typed = SqlType | null;

const SUM_PRECISION = 18;

export function execute(query: Query, catalogue: Catalogue, params: Params = {}): Table {
  const source = catalogue.find(query.from.name);
  if (!source) throw new SqlError({ code: "unknown-table", name: query.from.name }, query.from.at);
  const types = new Map<Expr, Typed>();
  const index = new Map(source.columns.map((c, i) => [c.name, i]));

  const typeOf = (e: Expr): Typed => {
    const known = types.get(e);
    if (known !== undefined || types.has(e)) return known ?? null;
    const t = computeType(e);
    types.set(e, t);
    return t;
  };

  const typeError = (e: Expr, operation: string, ts: readonly Typed[]): never => {
    throw new SqlError(
      { code: "type", operation, types: ts.map((t) => (t ? typeName(t) : "NULL")).join(" and ") },
      e.at,
    );
  };

  const computeType = (e: Expr): Typed => {
    switch (e.kind) {
      case "column": {
        const i = index.get(e.name);
        if (i === undefined)
          throw new SqlError(
            { code: "unknown-column", column: e.name, table: query.from.name },
            e.at,
          );
        return (source.columns[i] as { type: SqlType }).type;
      }
      case "literal":
        switch (e.type) {
          case "integer":
            return INT64;
          case "decimal":
            return decimal(SUM_PRECISION, e.text.split(".")[1]?.length ?? 0);
          case "string":
            return STRING;
          case "boolean":
            return BOOLEAN;
          case "null":
            return null;
        }
        return null;
      case "param": {
        const p = params[e.name];
        if (!p) throw new SqlError({ code: "missing-parameter", name: e.name }, e.at);
        return p.type;
      }
      case "unary": {
        const t = typeOf(e.arg);
        if (e.op === "NOT") {
          if (t && t.kind !== "boolean") typeError(e, "NOT", [t]);
          return BOOLEAN;
        }
        if (t && !isNumeric(t)) typeError(e, "-", [t]);
        return t;
      }
      case "binary": {
        const l = typeOf(e.left);
        const r = typeOf(e.right);
        if (e.op === "AND" || e.op === "OR") {
          for (const t of [l, r]) if (t && t.kind !== "boolean") typeError(e, e.op, [l, r]);
          return BOOLEAN;
        }
        if (e.op === "/") throw new SqlError({ code: "unsupported", what: "division" }, e.at);
        if (e.op === "+" || e.op === "-" || e.op === "*") {
          for (const t of [l, r]) if (t && !isNumeric(t)) typeError(e, e.op, [l, r]);
          if (!l || !r) return l ?? r;
          if (l.kind === "integer" && r.kind === "integer") return INT64;
          const scale = e.op === "*" ? scaleOf(l) + scaleOf(r) : Math.max(scaleOf(l), scaleOf(r));
          return decimal(SUM_PRECISION, scale);
        }
        if (l && r && !comparable(l, r, e)) typeError(e, e.op, [l, r]);
        return BOOLEAN;
      }
      case "isNull":
        typeOf(e.arg);
        return BOOLEAN;
      case "call": {
        const args = e.args.map(typeOf);
        const arg = args[0] ?? null;
        switch (e.name) {
          case "count":
            if (!e.star && e.args.length !== 1) typeError(e, "COUNT", args);
            return INT64;
          case "sum":
            if (e.args.length !== 1 || (arg && !isNumeric(arg))) typeError(e, "SUM", args);
            return arg && arg.kind === "decimal" ? decimal(SUM_PRECISION, arg.scale) : INT64;
          case "min":
          case "max":
            if (e.args.length !== 1) typeError(e, e.name.toUpperCase(), args);
            return arg;
          case "lower":
          case "upper":
            if (e.args.length !== 1 || (arg && arg.kind !== "string"))
              typeError(e, e.name.toUpperCase(), args);
            return STRING;
          case "coalesce": {
            const known = args.filter((t): t is SqlType => t !== null);
            const first = known[0] ?? null;
            for (const t of known)
              if (first && typeName(t) !== typeName(first) && !(isNumeric(t) && isNumeric(first)))
                typeError(e, "COALESCE", args);
            return first;
          }
          default:
            throw new SqlError({ code: "unsupported", what: `the function ${e.name}` }, e.at);
        }
      }
      case "cast": {
        const from = typeOf(e.arg);
        if (from && !castable(from, e.to)) typeError(e, `CAST to ${typeName(e.to)}`, [from]);
        return e.to;
      }
    }
  };

  // Rows the WHERE keeps.
  if (query.where) {
    if (hasAggregate(query.where))
      throw new SqlError(
        { code: "aggregate-in-where", expression: formatExpr(query.where) },
        query.where.at,
      );
    const t = typeOf(query.where);
    if (t && t.kind !== "boolean") typeError(query.where, "WHERE", [t]);
  }
  const evalRow = (e: Expr, row: readonly Value[]): Value =>
    evaluate(e, row, index, params, typeOf);
  const kept = query.where
    ? source.rows.filter((r) => evalRow(query.where as Expr, r) === true)
    : source.rows;

  const items: readonly SelectItem[] =
    query.items ??
    source.columns.map((c) => ({
      expr: { kind: "column", name: c.name, at: query.from.at } as Expr,
    }));
  const outTypes = items.map((it) => typeOf(it.expr) ?? STRING);
  const names = items.map(
    (it, k) =>
      it.alias ??
      (it.expr.kind === "column"
        ? it.expr.name
        : it.expr.kind === "call"
          ? it.expr.name
          : `column${k + 1}`),
  );
  for (const g of query.groupBy) typeOf(g);

  const grouped = query.groupBy.length > 0 || items.some((it) => hasAggregate(it.expr));
  let rows: Value[][];
  if (!grouped) {
    rows = kept.map((r) => items.map((it) => evalRow(it.expr, r)));
  } else {
    if (!query.items) throw new SqlError({ code: "not-grouped", expression: "*" }, query.from.at);
    // Every column outside a sum must be one of the GROUP BY expressions (or an alias of one).
    const groupExprs = query.groupBy.map((g) => {
      if (g.kind === "column" && !index.has(g.name)) {
        const k = names.indexOf(g.name);
        if (k >= 0) return (items[k] as { expr: Expr }).expr;
      }
      return g;
    });
    for (const it of items) checkGrouped(it.expr, groupExprs);
    const groups = new Map<string, (readonly Value[])[]>();
    for (const r of kept) {
      const key = JSON.stringify(groupExprs.map((g) => evalRow(g, r)));
      const list = groups.get(key);
      if (list) list.push(r);
      else groups.set(key, [r]);
    }
    // With no GROUP BY, the sums cover every row: one row out, even for no rows in.
    if (query.groupBy.length === 0 && groups.size === 0) groups.set("[]", []);
    rows = [...groups.values()].map((members) =>
      items.map((it) => evaluateGroup(it.expr, members, groupExprs, index, params, typeOf)),
    );
  }

  if (query.distinct) {
    const seen = new Set<string>();
    rows = rows.filter((r) => {
      const k = JSON.stringify(r);
      if (seen.has(k)) return false;
      seen.add(k);
      return true;
    });
  }

  if (query.orderBy.length) {
    const keys = query.orderBy.map((o) => {
      if (o.expr.kind === "column") {
        const k = names.indexOf(o.expr.name);
        if (k >= 0) return { k, descending: o.descending };
      }
      if (o.expr.kind === "literal" && o.expr.type === "integer") {
        const k = Number(o.expr.text) - 1;
        if (k >= 0 && k < items.length) return { k, descending: o.descending };
      }
      const k = items.findIndex((it) => sameExpr(it.expr, o.expr));
      if (k >= 0) return { k, descending: o.descending };
      throw new SqlError({ code: "order-by", expression: formatExpr(o.expr) }, o.expr.at);
    });
    rows = rows
      .map((r, n) => ({ r, n }))
      .sort((a, b) => {
        for (const { k, descending } of keys) {
          const c = compareValues(a.r[k] ?? null, b.r[k] ?? null);
          if (c !== 0) return descending ? -c : c;
        }
        return a.n - b.n;
      })
      .map((x) => x.r);
  }

  return { columns: names.map((name, k) => ({ name, type: outTypes[k] as SqlType })), rows };
}

function comparable(a: SqlType, b: SqlType, e: Expr): boolean {
  if (isNumeric(a) && isNumeric(b)) return true;
  if (a.kind === b.kind) return true;
  // A date or a time compared with a string literal: the literal is read as a date or a time.
  const literalString = (side: Expr) => side.kind === "literal" && side.type === "string";
  if (e.kind === "binary" && (a.kind === "date" || a.kind === "timestamp") && b.kind === "string")
    return literalString(e.right);
  if (e.kind === "binary" && (b.kind === "date" || b.kind === "timestamp") && a.kind === "string")
    return literalString(e.left);
  return false;
}

function castable(from: SqlType, to: SqlType): boolean {
  if (typeName(from) === typeName(to)) return true;
  if (to.kind === "string") return true;
  if (from.kind === "timestamp" && to.kind === "date") return true;
  if (from.kind === "string" && (to.kind === "date" || to.kind === "timestamp")) return true;
  if (from.kind === "integer" && (to.kind === "decimal" || to.kind === "integer")) return true;
  if (from.kind === "decimal" && to.kind === "decimal") return true;
  return false;
}

function checkGrouped(e: Expr, groups: readonly Expr[]): void {
  if (groups.some((g) => sameExpr(g, e))) return;
  switch (e.kind) {
    case "column":
      throw new SqlError({ code: "not-grouped", expression: e.name }, e.at);
    case "call":
      if (AGGREGATES.has(e.name)) return;
      for (const a of e.args) checkGrouped(a, groups);
      return;
    case "unary":
    case "isNull":
    case "cast":
      checkGrouped(e.arg, groups);
      return;
    case "binary":
      checkGrouped(e.left, groups);
      checkGrouped(e.right, groups);
      return;
    default:
      return;
  }
}

type TypeOf = (e: Expr) => SqlType | null;

/** A numeric value as a whole number at `scale` places. */
function at(value: number, from: number, scale: number): number {
  return value * 10 ** (scale - from);
}

function evaluate(
  e: Expr,
  row: readonly Value[],
  index: ReadonlyMap<string, number>,
  params: Params,
  typeOf: TypeOf,
): Value {
  const ev = (x: Expr) => evaluate(x, row, index, params, typeOf);
  switch (e.kind) {
    case "column":
      return row[index.get(e.name) as number] ?? null;
    case "literal":
      if (e.type === "null") return null;
      if (e.type === "boolean") return e.text === "TRUE";
      if (e.type === "integer") return Number(e.text);
      if (e.type === "decimal") return parseDecimal(e.text, e.text.split(".")[1]?.length ?? 0);
      return e.text;
    case "param":
      return params[e.name]?.value ?? null;
    case "unary": {
      const v = ev(e.arg);
      if (v === null) return null;
      return e.op === "NOT" ? !v : -(v as number);
    }
    case "isNull": {
      const v = ev(e.arg);
      return e.negated ? v !== null : v === null;
    }
    case "binary":
      return binary(e, ev(e.left), ev(e.right), typeOf);
    case "call":
      if (AGGREGATES.has(e.name))
        throw new SqlError({ code: "aggregate-in-where", expression: formatExpr(e) }, e.at);
      return call(e.name, e.args.map(ev));
    case "cast":
      return cast(ev(e.arg), typeOf(e.arg), e.to);
  }
}

function binary(e: Extract<Expr, { kind: "binary" }>, l: Value, r: Value, typeOf: TypeOf): Value {
  if (e.op === "AND") {
    if (l === false || r === false) return false;
    if (l === null || r === null) return null;
    return true;
  }
  if (e.op === "OR") {
    if (l === true || r === true) return true;
    if (l === null || r === null) return null;
    return false;
  }
  if (l === null || r === null) return null;
  const lt = typeOf(e.left);
  const rt = typeOf(e.right);
  if (typeof l === "number" && typeof r === "number" && lt && rt) {
    const ls = scaleOf(lt);
    const rs = scaleOf(rt);
    if (e.op === "*") return l * r;
    const s = Math.max(ls, rs);
    const a = at(l, ls, s);
    const b = at(r, rs, s);
    switch (e.op) {
      case "+":
        return a + b;
      case "-":
        return a - b;
      default:
        return compareOp(e.op, a - b);
    }
  }
  return compareOp(e.op, compareValues(l, r));
}

function compareOp(op: string, c: number): boolean {
  switch (op) {
    case "=":
      return c === 0;
    case "<>":
      return c !== 0;
    case "<":
      return c < 0;
    case "<=":
      return c <= 0;
    case ">":
      return c > 0;
    default:
      return c >= 0;
  }
}

function call(name: string, args: readonly Value[]): Value {
  const [a] = args;
  switch (name) {
    case "lower":
      return a === null || a === undefined ? null : String(a).toLowerCase();
    case "upper":
      return a === null || a === undefined ? null : String(a).toUpperCase();
    case "coalesce":
      return args.find((v) => v !== null) ?? null;
    default:
      return null;
  }
}

function cast(v: Value, from: SqlType | null, to: SqlType): Value {
  if (v === null) return null;
  if (to.kind === "date") return String(v).slice(0, 10);
  if (to.kind === "timestamp") return String(v).length === 10 ? `${v}T00:00:00Z` : String(v);
  if (to.kind === "decimal" && typeof v === "number")
    return at(v, from ? scaleOf(from) : 0, to.scale);
  if (to.kind === "string")
    return from && from.kind === "decimal" && typeof v === "number"
      ? formatScaled(v, from.scale)
      : String(v);
  return v;
}

function formatScaled(v: number, scale: number): string {
  const digits = String(Math.abs(v)).padStart(scale + 1, "0");
  return `${v < 0 ? "-" : ""}${digits.slice(0, digits.length - scale)}${scale ? `.${digits.slice(digits.length - scale)}` : ""}`;
}

function evaluateGroup(
  e: Expr,
  members: readonly (readonly Value[])[],
  groups: readonly Expr[],
  index: ReadonlyMap<string, number>,
  params: Params,
  typeOf: TypeOf,
): Value {
  const first = members[0];
  if (groups.some((g) => sameExpr(g, e)))
    return first ? evaluate(e, first, index, params, typeOf) : null;
  const ev = (x: Expr) => evaluateGroup(x, members, groups, index, params, typeOf);
  switch (e.kind) {
    case "call": {
      if (!AGGREGATES.has(e.name)) return call(e.name, e.args.map(ev));
      if (e.star) return members.length;
      const arg = e.args[0] as Expr;
      const values = members
        .map((r) => evaluate(arg, r, index, params, typeOf))
        .filter((v): v is Exclude<Value, null> => v !== null);
      switch (e.name) {
        case "count":
          return values.length;
        case "sum":
          return values.length ? (values as number[]).reduce((s, v) => s + v, 0) : null;
        case "min":
          return values.length ? values.reduce((m, v) => (compareValues(v, m) < 0 ? v : m)) : null;
        default:
          return values.length ? values.reduce((m, v) => (compareValues(v, m) > 0 ? v : m)) : null;
      }
    }
    case "binary":
      return binary(e, ev(e.left), ev(e.right), typeOf);
    case "unary": {
      const v = ev(e.arg);
      if (v === null) return null;
      return e.op === "NOT" ? !v : -(v as number);
    }
    case "isNull": {
      const v = ev(e.arg);
      return e.negated ? v !== null : v === null;
    }
    case "cast":
      return cast(ev(e.arg), typeOf(e.arg), e.to);
    default:
      return first ? evaluate(e, first, index, params, typeOf) : null;
  }
}
