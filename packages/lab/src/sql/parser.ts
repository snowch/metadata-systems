// Copyright © 2026 Christopher Snow

// Parses the course's SQL subset into a `Query`. A construct outside the subset (a join, a
// LIMIT, a HAVING) is refused as unsupported, by name, not as a confusing parse error.
//
//   query    := SELECT [DISTINCT] (* | item {, item}) FROM name [WHERE expr]
//               [GROUP BY expr {, expr}] [ORDER BY expr [ASC|DESC] {, ...}]
//   item     := expr [AS name]
//   expr     := and {OR and}            and := not {AND not}        not := NOT not | compare
//   compare  := sum [(= | <> | < | <= | > | >=) sum | IS [NOT] NULL]
//   sum      := product {(+ | -) product}            product := unary {(* | /) unary}
//   unary    := - unary | primary
//   primary  := number | 'string' | NULL | TRUE | FALSE | :param | name
//             | name ( [* | expr {, expr}] ) | CAST ( expr AS type ) | ( expr )

import { decimal, BOOLEAN, DATE, INT32, INT64, STRING, TIMESTAMP, type SqlType } from "../values";
import {
  FUNCTIONS,
  type BinaryOp,
  type Expr,
  type OrderItem,
  type Query,
  type SelectItem,
} from "./ast";
import { SqlError } from "./errors";
import { tokenise, type Token } from "./lexer";

export function parseQuery(text: string): Query {
  const p = new Parser(tokenise(text));
  const q = p.query();
  p.expectEnd();
  return q;
}

/** One expression on its own, for a figure that shows or builds a single expression. */
export function parseExpression(text: string): Expr {
  const p = new Parser(tokenise(text));
  const e = p.expr();
  p.expectEnd();
  return e;
}

const UNSUPPORTED: Record<string, string> = {
  JOIN: "JOIN",
  ON: "JOIN",
  LIMIT: "LIMIT",
  HAVING: "HAVING",
  UNION: "UNION",
};

class Parser {
  private i = 0;
  constructor(private readonly tokens: readonly Token[]) {}

  private peek(): Token {
    return this.tokens[this.i] ?? (this.tokens[this.tokens.length - 1] as Token);
  }

  private next(): Token {
    const t = this.peek();
    if (t.kind !== "end") this.i++;
    return t;
  }

  private isKeyword(word: string): boolean {
    const t = this.peek();
    return t.kind === "keyword" && t.text === word;
  }

  private isOp(op: string): boolean {
    const t = this.peek();
    return t.kind === "op" && t.text === op;
  }

  private found(t: Token): string {
    if (t.kind === "end") return "the end of the query";
    if (t.kind === "string") return `'${t.text}'`;
    return t.text;
  }

  private fail(expected: string): never {
    const t = this.peek();
    if (t.kind === "keyword" && UNSUPPORTED[t.text])
      throw new SqlError({ code: "unsupported", what: UNSUPPORTED[t.text] as string }, t.at);
    throw new SqlError({ code: "syntax", expected, found: this.found(t) }, t.at);
  }

  private keyword(word: string): Token {
    if (!this.isKeyword(word)) this.fail(word);
    return this.next();
  }

  private op(op: string): Token {
    if (!this.isOp(op)) this.fail(`"${op}"`);
    return this.next();
  }

  private name(what: string): Token {
    const t = this.peek();
    if (t.kind !== "name") this.fail(what);
    return this.next();
  }

  expectEnd(): void {
    if (this.isOp(";")) this.next();
    if (this.peek().kind !== "end") this.fail("the end of the query");
  }

  query(): Query {
    this.keyword("SELECT");
    const distinct = this.isKeyword("DISTINCT") ? (this.next(), true) : false;
    let items: SelectItem[] | undefined;
    if (this.isOp("*")) this.next();
    else {
      items = [this.item()];
      while (this.isOp(",")) {
        this.next();
        items.push(this.item());
      }
    }
    this.keyword("FROM");
    const table = this.name("a table or file name");
    let where: Expr | undefined;
    if (this.isKeyword("WHERE")) {
      this.next();
      where = this.expr();
    }
    const groupBy: Expr[] = [];
    if (this.isKeyword("GROUP")) {
      this.next();
      this.keyword("BY");
      groupBy.push(this.expr());
      while (this.isOp(",")) {
        this.next();
        groupBy.push(this.expr());
      }
    }
    const orderBy: OrderItem[] = [];
    if (this.isKeyword("ORDER")) {
      this.next();
      this.keyword("BY");
      for (;;) {
        const expr = this.expr();
        let descending = false;
        if (this.isKeyword("ASC")) this.next();
        else if (this.isKeyword("DESC")) {
          this.next();
          descending = true;
        }
        orderBy.push({ expr, descending });
        if (!this.isOp(",")) break;
        this.next();
      }
    }
    return {
      distinct,
      ...(items ? { items } : {}),
      from: { name: table.text, at: table.at },
      ...(where ? { where } : {}),
      groupBy,
      orderBy,
    };
  }

  private item(): SelectItem {
    const expr = this.expr();
    if (this.isKeyword("AS")) {
      this.next();
      return { expr, alias: this.name("a name after AS").text };
    }
    return { expr };
  }

  expr(): Expr {
    let left = this.and();
    while (this.isKeyword("OR")) {
      const at = this.next().at;
      left = { kind: "binary", op: "OR", left, right: this.and(), at };
    }
    return left;
  }

  private and(): Expr {
    let left = this.not();
    while (this.isKeyword("AND")) {
      const at = this.next().at;
      left = { kind: "binary", op: "AND", left, right: this.not(), at };
    }
    return left;
  }

  private not(): Expr {
    if (this.isKeyword("NOT")) {
      const at = this.next().at;
      return { kind: "unary", op: "NOT", arg: this.not(), at };
    }
    return this.compare();
  }

  private compare(): Expr {
    const left = this.sum();
    const t = this.peek();
    if (t.kind === "op" && ["=", "<>", "<", "<=", ">", ">="].includes(t.text)) {
      this.next();
      return { kind: "binary", op: t.text as BinaryOp, left, right: this.sum(), at: t.at };
    }
    if (this.isKeyword("IS")) {
      const at = this.next().at;
      const negated = this.isKeyword("NOT") ? (this.next(), true) : false;
      this.keyword("NULL");
      return { kind: "isNull", arg: left, negated, at };
    }
    return left;
  }

  private sum(): Expr {
    let left = this.product();
    while (this.isOp("+") || this.isOp("-")) {
      const t = this.next();
      left = { kind: "binary", op: t.text as BinaryOp, left, right: this.product(), at: t.at };
    }
    return left;
  }

  private product(): Expr {
    let left = this.unary();
    while (this.isOp("*") || this.isOp("/")) {
      const t = this.next();
      left = { kind: "binary", op: t.text as BinaryOp, left, right: this.unary(), at: t.at };
    }
    return left;
  }

  private unary(): Expr {
    if (this.isOp("-")) {
      const at = this.next().at;
      return { kind: "unary", op: "-", arg: this.unary(), at };
    }
    return this.primary();
  }

  private primary(): Expr {
    const t = this.peek();
    if (t.kind === "number") {
      this.next();
      return {
        kind: "literal",
        type: t.text.includes(".") ? "decimal" : "integer",
        text: t.text,
        at: t.at,
      };
    }
    if (t.kind === "string") {
      this.next();
      return { kind: "literal", type: "string", text: t.text, at: t.at };
    }
    if (t.kind === "param") {
      this.next();
      return { kind: "param", name: t.text, at: t.at };
    }
    if (t.kind === "keyword") {
      if (t.text === "NULL" || t.text === "TRUE" || t.text === "FALSE") {
        this.next();
        return {
          kind: "literal",
          type: t.text === "NULL" ? "null" : "boolean",
          text: t.text,
          at: t.at,
        };
      }
      if (t.text === "CAST") {
        this.next();
        this.op("(");
        const arg = this.expr();
        this.keyword("AS");
        const to = this.type();
        this.op(")");
        return { kind: "cast", arg, to, at: t.at };
      }
      this.fail("a value, a column or an expression");
    }
    if (t.kind === "op" && t.text === "(") {
      this.next();
      const e = this.expr();
      this.op(")");
      return e;
    }
    if (t.kind === "name") {
      this.next();
      if (this.isOp("(")) {
        if (t.quoted || !FUNCTIONS.has(t.text))
          throw new SqlError({ code: "unsupported", what: `the function ${t.text}` }, t.at);
        this.next();
        if (this.isOp("*")) {
          this.next();
          this.op(")");
          if (t.text !== "count")
            throw new SqlError({ code: "syntax", expected: "an expression", found: "*" }, t.at);
          return { kind: "call", name: t.text, args: [], star: true, at: t.at };
        }
        const args: Expr[] = [];
        if (!this.isOp(")")) {
          args.push(this.expr());
          while (this.isOp(",")) {
            this.next();
            args.push(this.expr());
          }
        }
        this.op(")");
        return { kind: "call", name: t.text, args, star: false, at: t.at };
      }
      if (this.isOp("."))
        throw new SqlError({ code: "unsupported", what: "table.column names" }, t.at);
      return { kind: "column", name: t.text, at: t.at };
    }
    this.fail("a value, a column or an expression");
  }

  private type(): SqlType {
    const t = this.peek();
    const word = t.kind === "name" || t.kind === "keyword" ? t.text.toUpperCase() : "";
    this.next();
    switch (word) {
      case "DATE":
        return DATE;
      case "TIMESTAMP":
        return TIMESTAMP;
      case "INT":
      case "INTEGER":
        return INT32;
      case "BIGINT":
        return INT64;
      case "VARCHAR":
      case "TEXT":
      case "STRING":
        return STRING;
      case "BOOLEAN":
        return BOOLEAN;
      case "DECIMAL":
      case "NUMERIC": {
        this.op("(");
        const p = this.next();
        this.op(",");
        const s = this.next();
        this.op(")");
        if (p.kind !== "number" || s.kind !== "number")
          throw new SqlError(
            { code: "syntax", expected: "DECIMAL(precision, scale)", found: p.text },
            p.at,
          );
        return decimal(Number(p.text), Number(s.text));
      }
      default:
        throw new SqlError(
          { code: "syntax", expected: "a type, such as DATE", found: t.text || "nothing" },
          t.at,
        );
    }
  }
}
