// Copyright © 2026 Christopher Snow

// Splits a query into tokens. Keywords and unquoted names are case-insensitive and folded to
// lower case; a name in double quotes keeps its case and may hold dots, as in "orders.parquet".

import { SqlError, type Pos } from "./errors";

export type TokenKind = "keyword" | "name" | "number" | "string" | "param" | "op" | "end";

export interface Token {
  readonly kind: TokenKind;
  /** Keywords upper-cased, unquoted names lower-cased, strings without their quotes. */
  readonly text: string;
  readonly quoted?: boolean;
  readonly at: Pos;
}

export const KEYWORDS = new Set([
  "SELECT",
  "DISTINCT",
  "FROM",
  "WHERE",
  "GROUP",
  "BY",
  "ORDER",
  "ASC",
  "DESC",
  "AS",
  "AND",
  "OR",
  "NOT",
  "IS",
  "NULL",
  "TRUE",
  "FALSE",
  "CAST",
  "JOIN",
  "ON",
  "LIMIT",
  "HAVING",
  "UNION",
]);

const OPS = ["<>", "!=", "<=", ">=", "=", "<", ">", "+", "-", "*", "/", "(", ")", ",", ".", ";"];

export function tokenise(text: string): Token[] {
  const tokens: Token[] = [];
  let i = 0;
  let line = 1;
  let lineStart = 0;
  const pos = (offset: number): Pos => ({ line, column: offset - lineStart + 1, offset });
  while (i < text.length) {
    const c = text[i] as string;
    if (c === "\n") {
      i++;
      line++;
      lineStart = i;
      continue;
    }
    if (/\s/.test(c)) {
      i++;
      continue;
    }
    if (c === "-" && text[i + 1] === "-") {
      while (i < text.length && text[i] !== "\n") i++;
      continue;
    }
    const at = pos(i);
    if (/[A-Za-z_]/.test(c)) {
      let j = i;
      while (j < text.length && /[A-Za-z0-9_]/.test(text[j] as string)) j++;
      const word = text.slice(i, j);
      const upper = word.toUpperCase();
      tokens.push(
        KEYWORDS.has(upper)
          ? { kind: "keyword", text: upper, at }
          : { kind: "name", text: word.toLowerCase(), at },
      );
      i = j;
      continue;
    }
    if (c === '"') {
      let j = i + 1;
      let name = "";
      for (;;) {
        if (j >= text.length)
          throw new SqlError({ code: "syntax", expected: "a closing quote", found: "the end" }, at);
        if (text[j] === '"') {
          if (text[j + 1] === '"') {
            name += '"';
            j += 2;
            continue;
          }
          break;
        }
        name += text[j];
        j++;
      }
      tokens.push({ kind: "name", text: name, quoted: true, at });
      i = j + 1;
      continue;
    }
    if (c === "'") {
      let j = i + 1;
      let s = "";
      for (;;) {
        if (j >= text.length)
          throw new SqlError({ code: "syntax", expected: "a closing quote", found: "the end" }, at);
        if (text[j] === "'") {
          if (text[j + 1] === "'") {
            s += "'";
            j += 2;
            continue;
          }
          break;
        }
        s += text[j];
        j++;
      }
      tokens.push({ kind: "string", text: s, at });
      i = j + 1;
      continue;
    }
    if (/[0-9]/.test(c)) {
      let j = i;
      while (j < text.length && /[0-9]/.test(text[j] as string)) j++;
      if (text[j] === "." && /[0-9]/.test(text[j + 1] ?? "")) {
        j++;
        while (j < text.length && /[0-9]/.test(text[j] as string)) j++;
      }
      tokens.push({ kind: "number", text: text.slice(i, j), at });
      i = j;
      continue;
    }
    if (c === ":" && /[A-Za-z_]/.test(text[i + 1] ?? "")) {
      let j = i + 1;
      while (j < text.length && /[A-Za-z0-9_]/.test(text[j] as string)) j++;
      tokens.push({ kind: "param", text: text.slice(i + 1, j).toLowerCase(), at });
      i = j;
      continue;
    }
    const op = OPS.find((o) => text.startsWith(o, i));
    if (op) {
      tokens.push({ kind: "op", text: op === "!=" ? "<>" : op, at });
      i += op.length;
      continue;
    }
    throw new SqlError(
      { code: "syntax", expected: "a word, a number or an operator", found: c },
      at,
    );
  }
  tokens.push({ kind: "end", text: "", at: pos(i) });
  return tokens;
}
