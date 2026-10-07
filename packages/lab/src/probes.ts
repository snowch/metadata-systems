// Copyright © 2026 Christopher Snow

// What a prediction asks the lab. Each probe is run when the learner commits. A probe that names
// what it found (an account, a total that is more) answers with that word, and the figure picks
// the option that stands for it; a probe that counts answers with the count, and the figure picks
// the option whose range holds it. Either way the page never stores an answer: it computes it.

import { PROGRAM_ACCOUNT, type AssetId } from "./shop/assets";
import { formatValue } from "./values";
import type { Week } from "./shop/week";
import { recordOf } from "./storage";
import { catalogueFor, storage } from "./lab";
import {
  checkRows,
  cleanReconstructions,
  runOver,
  sumSql,
  type Keep,
  type RowCheck,
} from "./infer";

export type Probe =
  | { readonly kind: "owner-kind"; readonly asset: AssetId }
  | {
      readonly kind: "day-total";
      readonly source: AssetId;
      readonly keep: Keep;
      readonly target: AssetId;
      /** The day whose two totals are compared. */
      readonly day: string;
    }
  | { readonly kind: "clean-fits" }
  | {
      readonly kind: "day-gap";
      /** The raw orders, the asset a rebuild reads and the rows it keeps, and what it rebuilds. */
      readonly source: AssetId;
      readonly via: AssetId;
      readonly keep: Keep;
      readonly target: AssetId;
      readonly day: string;
    };

/** What the rows can show about a difference between a day's raw orders and a rebuilt total. */
export type GapKind = "left" | "lower" | "moved";

export type ProbeResult =
  | {
      readonly kind: "owner-kind";
      readonly answer: "account" | "person" | "team" | "none";
      readonly value: string | null;
      /** The warehouse's tables this week, and how many of them record an owner. */
      readonly tables: number;
      readonly owned: number;
    }
  | {
      readonly kind: "day-total";
      /** The source's total for the day against the target's row: the same, more or less. */
      readonly answer: "same" | "more" | "less" | "none";
      readonly day: string;
      /** Every day's two totals, for the evidence. */
      readonly checks: readonly RowCheck[];
    }
  | {
      readonly kind: "clean-fits";
      /** How many settings of the cleaning rules give clean_orders exactly. */
      readonly count: number;
    }
  | {
      readonly kind: "day-gap";
      /** What the rows show: orders left out, kept at a lower value, or kept on another day. */
      readonly answer: readonly GapKind[];
      /** The day's orders in the source, and how each fared among the rows the rebuild keeps. */
      readonly orders: number;
      readonly kept: number;
      readonly left: number;
      readonly lower: number;
      readonly moved: number;
      /** What the orders left out are worth, and the source's total for the day less the target's. */
      readonly leftTotal: string;
      readonly difference: string;
    };

/** The people and teams the shop has, for telling an account from a person. */
const PEOPLE = new Set(["j.marsh", "k.adeyemi", "r.novak", "s.lund"]);
const TEAMS = new Set(["finance", "analytics"]);

export function runProbe(probe: Probe, w: Week): ProbeResult {
  switch (probe.kind) {
    case "owner-kind": {
      const view = storage(w);
      const r = recordOf(view, probe.asset);
      const tables = view.filter((x) => x.system === "warehouse");
      const value = r.ownerRole ?? r.createdBy ?? null;
      const answer =
        value === null
          ? "none"
          : value === PROGRAM_ACCOUNT
            ? "account"
            : PEOPLE.has(value)
              ? "person"
              : TEAMS.has(value)
                ? "team"
                : "none";
      return {
        kind: "owner-kind",
        answer,
        value,
        tables: tables.length,
        owned: tables.filter((x) => x.ownerRole !== undefined).length,
      };
    }
    case "day-total": {
      const target = w.tables.get(probe.target);
      if (!target) throw new Error(`no ${probe.target} this week`);
      const r = runOver(
        sumSql({ source: probe.source, keep: probe.keep, measure: "revenue", per: "day" }),
        catalogueFor(w),
      );
      const checks = checkRows("table" in r ? r.table : undefined, target).filter(
        (c) => c.expected !== null,
      );
      // Both totals are written by the lab's own formatting, so they read back as numbers.
      const day = checks.find((c) => c.key === probe.day);
      const answer =
        !day || day.actual === null || day.expected === null
          ? "none"
          : day.same
            ? "same"
            : Number(day.actual) > Number(day.expected)
              ? "more"
              : "less";
      return { kind: "day-total", answer, day: probe.day, checks };
    }
    case "day-gap":
      return dayGap(probe, w);
    case "clean-fits":
      return { kind: "clean-fits", count: cleanReconstructions(w).length };
  }
}

/**
 * The value of the option that stands for a probe's answer: the one whose `means` holds it, if
 * exactly one does, or else the option whose value is the answer itself.
 */
export function optionForAnswer(
  answer: string,
  options: readonly { readonly value: string; readonly means?: readonly string[] }[],
): string | undefined {
  const hits = options.filter((o) => o.means?.includes(answer));
  if (hits.length === 1) return hits[0]?.value;
  if (hits.length > 1) return undefined;
  return options.find((o) => o.value === answer)?.value;
}

/** The value of the option whose range holds a count, if exactly one does. */
export function optionForCount(
  count: number,
  options: readonly { readonly value: string; readonly range?: readonly [number, number] }[],
): string | undefined {
  const hits = options.filter((o) => o.range && o.range[0] <= count && count <= o.range[1]);
  return hits.length === 1 ? hits[0]?.value : undefined;
}

/**
 * A day's raw orders against the rows a rebuild keeps, order by order: kept on the day at the same
 * value, left out, kept at a lower value, or kept on another day. It reads the rows only, as a
 * learner can; it says nothing of why an order was left out.
 */
function dayGap(probe: Extract<Probe, { kind: "day-gap" }>, w: Week): ProbeResult {
  const table = (id: AssetId) => {
    const t = w.tables.get(id);
    if (!t) throw new Error(`no ${id} this week`);
    return t;
  };
  const source = table(probe.source);
  const via = table(probe.via);
  const target = table(probe.target);
  const at = (t: typeof source, name: string) => {
    const i = t.columns.findIndex((c) => c.name === name);
    if (i < 0) throw new Error(`no column ${name}`);
    return i;
  };
  const field = (t: typeof source) => ({
    id: at(t, "order_id"),
    price: at(t, "price"),
    quantity: at(t, "quantity"),
    status: at(t, "status"),
    time: at(t, "ordered_at"),
  });
  const s = field(source);
  const v = field(via);
  const value = (row: readonly unknown[], f: typeof s) =>
    Number(row[f.price] ?? 0) * Number(row[f.quantity] ?? 0);
  const dayOf = (row: readonly unknown[], f: typeof s) => String(row[f.time] ?? "").slice(0, 10);

  // The rows the rebuild keeps, by order id, each to be matched once.
  const kept = new Map<string, (readonly unknown[])[]>();
  for (const row of via.rows)
    if (probe.keep === "all" || row[v.status] === probe.keep) {
      const id = String(row[v.id]);
      kept.set(id, [...(kept.get(id) ?? []), row]);
    }

  let orders = 0;
  let same = 0;
  let left = 0;
  let lower = 0;
  let moved = 0;
  let leftUnits = 0;
  let rawUnits = 0;
  for (const row of source.rows) {
    if (dayOf(row, s) !== probe.day) continue;
    orders++;
    rawUnits += value(row, s);
    const match = kept.get(String(row[s.id]))?.shift();
    if (!match) {
      left++;
      leftUnits += value(row, s);
    } else if (dayOf(match, v) !== probe.day) moved++;
    else if (value(match, v) < value(row, s)) lower++;
    else same++;
  }

  const total = target.rows.find((r) => String(r[0]) === probe.day);
  const type = target.columns[1]?.type;
  if (!total || !type) throw new Error(`no ${probe.target} row for ${probe.day}`);
  const answer: GapKind[] = [];
  if (left) answer.push("left");
  if (lower) answer.push("lower");
  if (moved) answer.push("moved");
  return {
    kind: "day-gap",
    answer,
    orders,
    kept: same,
    left,
    lower,
    moved,
    leftTotal: formatValue(leftUnits, type),
    difference: formatValue(rawUnits - Number(total[1] ?? 0), type),
  };
}
