// Copyright © 2026 Christopher Snow

// What goes wrong with a query, as data. The lab says which problem and where; the words a
// learner reads are the figures' (`@ms/views`), chosen by `code` and filled from `slots`. The
// message is for a developer reading a test's output.

export interface Pos {
  readonly line: number;
  readonly column: number;
  readonly offset: number;
}

export type SqlProblem =
  | { readonly code: "syntax"; readonly expected: string; readonly found: string }
  | { readonly code: "unsupported"; readonly what: string }
  | { readonly code: "unknown-table"; readonly name: string }
  | { readonly code: "unknown-column"; readonly column: string; readonly table: string }
  | { readonly code: "not-grouped"; readonly expression: string }
  | { readonly code: "aggregate-in-where"; readonly expression: string }
  | { readonly code: "type"; readonly operation: string; readonly types: string }
  | { readonly code: "missing-parameter"; readonly name: string }
  | { readonly code: "order-by"; readonly expression: string };

export class SqlError extends Error {
  constructor(
    readonly problem: SqlProblem,
    readonly at?: Pos,
  ) {
    const where = at ? ` (line ${at.line}, column ${at.column})` : "";
    super(`${problem.code}: ${JSON.stringify(problem)}${where}`);
    this.name = "SqlError";
  }
}
