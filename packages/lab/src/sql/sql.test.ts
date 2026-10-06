// Copyright © 2026 Christopher Snow

import { describe, expect, it } from "vitest";

import type { Table } from "../table";
import { DATE, INT32, INT64, STRING, TIMESTAMP, decimal, formatValue } from "../values";
import { SqlError, catalogueOf, formatQuery, parseQuery, runSql } from "./index";

const orders: Table = {
  columns: [
    { name: "order_id", type: INT64 },
    { name: "customer_id", type: INT64 },
    { name: "quantity", type: INT32 },
    { name: "price", type: decimal(10, 2) },
    { name: "status", type: STRING },
    { name: "ordered_at", type: TIMESTAMP },
  ],
  rows: [
    [1, 10, 2, 650, "completed", "2026-09-07T08:00:00Z"],
    [2, null, 1, 3200, "completed", "2026-09-07T09:00:00Z"],
    [3, 11, 3, 1999, "cancelled", "2026-09-08T10:00:00Z"],
    [3, 11, 3, 1999, "cancelled", "2026-09-08T10:00:00Z"],
    [4, 12, 1, 1200, "completed", "2026-09-08T11:00:00Z"],
  ],
};
const cat = catalogueOf({ orders, "orders.parquet": orders });

const problem = (fn: () => unknown) => {
  try {
    fn();
  } catch (e) {
    if (e instanceof SqlError) return e.problem;
    throw e;
  }
  throw new Error("expected a SqlError");
};

describe("the course's SQL subset", () => {
  it("sums decimals exactly, per day", () => {
    const t = runSql(
      `SELECT CAST(ordered_at AS DATE) AS day, SUM(price * quantity) AS revenue
       FROM orders WHERE status = 'completed' GROUP BY CAST(ordered_at AS DATE) ORDER BY day`,
      cat,
    );
    expect(t.columns.map((c) => c.name)).toEqual(["day", "revenue"]);
    expect(t.columns[1]?.type).toEqual(decimal(18, 2));
    expect(t.rows).toEqual([
      ["2026-09-07", 4500],
      ["2026-09-08", 1200],
    ]);
    expect(formatValue(t.rows[0]?.[1] ?? null, t.columns[1]!.type)).toBe("45.00");
  });

  it("treats NULL as SQL does: a comparison with NULL keeps nothing", () => {
    expect(runSql("SELECT order_id FROM orders WHERE customer_id = NULL", cat).rows).toEqual([]);
    expect(runSql("SELECT order_id FROM orders WHERE customer_id IS NULL", cat).rows).toEqual([
      [2],
    ]);
    expect(runSql("SELECT COUNT(*) AS n, COUNT(customer_id) AS c FROM orders", cat).rows).toEqual([
      [5, 4],
    ]);
  });

  it("keeps one copy of a repeated row with DISTINCT", () => {
    expect(runSql("SELECT DISTINCT order_id FROM orders", cat).rows).toEqual([[1], [2], [3], [4]]);
  });

  it("reads a file by its quoted name, and groups by an alias", () => {
    const t = runSql(
      `SELECT status, COUNT(*) AS orders FROM "orders.parquet" GROUP BY status ORDER BY orders DESC`,
      cat,
    );
    expect(t.rows).toEqual([
      ["completed", 3],
      ["cancelled", 2],
    ]);
  });

  it("binds a named parameter", () => {
    const t = runSql("SELECT order_id FROM orders WHERE CAST(ordered_at AS DATE) = :day", cat, {
      day: { type: DATE, value: "2026-09-08" },
    });
    expect(t.rows).toEqual([[3], [3], [4]]);
  });

  it("gives one row of NULLs for a sum over no rows, and no rows for a group over none", () => {
    expect(runSql("SELECT SUM(quantity) AS q FROM orders WHERE order_id > 99", cat).rows).toEqual([
      [null],
    ]);
    expect(
      runSql(
        "SELECT status, SUM(quantity) AS q FROM orders WHERE order_id > 99 GROUP BY status",
        cat,
      ).rows,
    ).toEqual([]);
  });

  it("refuses what it cannot run, saying which problem and where", () => {
    expect(problem(() => runSql("SELECT price FROM customers", cat))).toEqual({
      code: "unknown-table",
      name: "customers",
    });
    expect(problem(() => runSql("SELECT email FROM orders", cat))).toEqual({
      code: "unknown-column",
      column: "email",
      table: "orders",
    });
    expect(
      problem(() => runSql("SELECT status, quantity, COUNT(*) FROM orders GROUP BY status", cat)),
    ).toEqual({
      code: "not-grouped",
      expression: "quantity",
    });
    expect(
      problem(() => runSql("SELECT order_id FROM orders WHERE SUM(quantity) > 1", cat)),
    ).toMatchObject({
      code: "aggregate-in-where",
    });
    expect(problem(() => runSql("SELECT status * 2 FROM orders", cat))).toEqual({
      code: "type",
      operation: "*",
      types: "string and int64",
    });
    expect(
      problem(() => runSql("SELECT order_id FROM orders WHERE ordered_at > :day", cat)),
    ).toEqual({
      code: "missing-parameter",
      name: "day",
    });
    expect(problem(() => runSql("SELECT a FROM orders JOIN customers", cat))).toEqual({
      code: "unsupported",
      what: "JOIN",
    });
    expect(problem(() => runSql("SELECT FROM orders", cat))).toEqual({
      code: "syntax",
      expected: "a value, a column or an expression",
      found: "FROM",
    });
    const e = (() => {
      try {
        runSql("SELECT order_id\nFROM orders\nWHERE nope = 1", cat);
      } catch (x) {
        return x as SqlError;
      }
      return undefined;
    })();
    expect(e?.at).toMatchObject({ line: 3, column: 7 });
  });

  it("writes a parsed query back as text that parses to the same query", () => {
    const text = `select distinct order_id, price * quantity as revenue from "orders.parquet"
      where customer_id is not null and (quantity > 0 or status <> 'cancelled') order by revenue desc`;
    const formatted = formatQuery(parseQuery(text));
    expect(formatted).toBe(
      [
        "SELECT DISTINCT order_id, price * quantity AS revenue",
        'FROM "orders.parquet"',
        "WHERE customer_id IS NOT NULL AND (quantity > 0 OR status <> 'cancelled')",
        "ORDER BY revenue DESC",
      ].join("\n"),
    );
    expect(formatQuery(parseQuery(formatted))).toBe(formatted);
  });
});
