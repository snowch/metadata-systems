// Copyright © 2026 Christopher Snow

// An asset's rows, as storage holds them: one column per column, each value written by its type,
// NULL marked. A table wider than its box scrolls inside it (ScrollRegion), never the page.

import { formatRow, type Table } from "@ms/lab";

import { ScrollRegion } from "./ScrollRegion";

export function DataTable({
  table,
  caption,
  mark,
}: {
  table: Table;
  caption: string;
  /** Rows to mark, by index, with the reason as a class name. */
  mark?: ReadonlyMap<number, string>;
}) {
  return (
    <ScrollRegion label={caption}>
      <table className="data-table">
        <caption>{caption}</caption>
        <thead>
          <tr>
            {table.columns.map((c) => (
              <th key={c.name} scope="col">
                {c.name}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {table.rows.map((row, i) => (
            <tr key={i} className={mark?.get(i)}>
              {formatRow(table, row).map((text, k) => (
                <td key={k} className={row[k] === null ? "cell-null" : undefined}>
                  {text}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </ScrollRegion>
  );
}
