// Copyright © 2026 Christopher Snow

// A query or an expression written back as text, the way the lab shows SQL: keywords in capitals,
// a name quoted only where it must be.

import { typeName } from "../values";
import { KEYWORDS } from "./lexer";
import type { Expr, Query } from "./ast";

/** A name as SQL must write it: quoted if it holds anything but letters, digits and _. */
export function quoteName(name: string): string {
  return /^[a-z_][a-z0-9_]*$/.test(name) && !KEYWORDS.has(name.toUpperCase())
    ? name
    : `"${name.replace(/"/g, '""')}"`;
}

const PRECEDENCE: Record<string, number> = {
  OR: 1,
  AND: 2,
  "=": 4,
  "<>": 4,
  "<": 4,
  "<=": 4,
  ">": 4,
  ">=": 4,
  "+": 5,
  "-": 5,
  "*": 6,
  "/": 6,
};

function precedence(e: Expr): number {
  if (e.kind === "binary") return PRECEDENCE[e.op] ?? 9;
  if (e.kind === "unary" && e.op === "NOT") return 3;
  if (e.kind === "isNull") return 4;
  return 9;
}

export function formatExpr(e: Expr): string {
  const wrap = (x: Expr, min: number) =>
    precedence(x) < min ? `(${formatExpr(x)})` : formatExpr(x);
  switch (e.kind) {
    case "column":
      return quoteName(e.name);
    case "literal":
      return e.type === "string" ? `'${e.text.replace(/'/g, "''")}'` : e.text;
    case "param":
      return `:${e.name}`;
    case "unary":
      return e.op === "NOT" ? `NOT ${wrap(e.arg, 3)}` : `-${wrap(e.arg, 9)}`;
    case "isNull":
      return `${wrap(e.arg, 5)} IS ${e.negated ? "NOT " : ""}NULL`;
    case "binary": {
      const p = PRECEDENCE[e.op] ?? 9;
      return `${wrap(e.left, p)} ${e.op} ${wrap(e.right, p + 1)}`;
    }
    case "call":
      return `${e.name.toUpperCase()}(${e.star ? "*" : e.args.map(formatExpr).join(", ")})`;
    case "cast":
      return `CAST(${formatExpr(e.arg)} AS ${typeName(e.to).toUpperCase()})`;
  }
}

/** A query on several lines: one clause per line, as the lab shows its programs. */
export function formatQuery(q: Query): string {
  const lines: string[] = [];
  const items = q.items
    ? q.items.map((it) =>
        it.alias ? `${formatExpr(it.expr)} AS ${quoteName(it.alias)}` : formatExpr(it.expr),
      )
    : ["*"];
  lines.push(`SELECT ${q.distinct ? "DISTINCT " : ""}${items.join(", ")}`);
  lines.push(`FROM ${quoteName(q.from.name)}`);
  if (q.where) lines.push(`WHERE ${formatExpr(q.where)}`);
  if (q.groupBy.length) lines.push(`GROUP BY ${q.groupBy.map(formatExpr).join(", ")}`);
  if (q.orderBy.length)
    lines.push(
      `ORDER BY ${q.orderBy.map((o) => `${formatExpr(o.expr)}${o.descending ? " DESC" : ""}`).join(", ")}`,
    );
  return lines.join("\n");
}
