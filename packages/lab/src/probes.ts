// Copyright © 2026 Christopher Snow

// What a prediction asks the lab. Each probe is run when the learner commits. A probe that names
// what it found (an account, a total that is more) answers with that word, and the figure picks
// the option that stands for it; a probe that counts answers with the count, and the figure picks
// the option whose range holds it. Either way the page never stores an answer: it computes it.

import { PROGRAM_ACCOUNT, type AssetId } from "./shop/assets";
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
  | { readonly kind: "clean-fits" };

export type ProbeResult =
  | {
      readonly kind: "owner-kind";
      readonly answer: "account" | "person" | "team" | "none";
      readonly value: string | null;
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
    };

/** The people and teams the shop has, for telling an account from a person. */
const PEOPLE = new Set(["j.marsh", "k.adeyemi", "r.novak", "s.lund"]);
const TEAMS = new Set(["finance", "analytics"]);

export function runProbe(probe: Probe, w: Week): ProbeResult {
  switch (probe.kind) {
    case "owner-kind": {
      const r = recordOf(storage(w), probe.asset);
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
      return { kind: "owner-kind", answer, value };
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
