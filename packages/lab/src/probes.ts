// Copyright © 2026 Christopher Snow

// What a prediction asks the lab. Each probe is run when the learner commits, and its answer is
// one of the prediction's option values, so the page never stores an answer: it computes it.

import { PROGRAM_ACCOUNT, type AssetId } from "./shop/assets";
import type { Week } from "./shop/week";
import { recordOf } from "./storage";
import { catalogueFor, storage } from "./lab";
import { checkRows, runOver, sumSql, type Keep, type RowCheck } from "./infer";

export type Probe =
  | { readonly kind: "owner-kind"; readonly asset: AssetId }
  | {
      readonly kind: "days-matching";
      readonly source: AssetId;
      readonly keep: Keep;
      readonly target: AssetId;
    };

export type ProbeResult =
  | {
      readonly kind: "owner-kind";
      readonly answer: "account" | "person" | "team" | "none";
      readonly value: string | null;
    }
  | {
      readonly kind: "days-matching";
      readonly answer: "all" | "some" | "none";
      readonly matching: number;
      readonly total: number;
      readonly checks: readonly RowCheck[];
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
    case "days-matching": {
      const target = w.tables.get(probe.target);
      if (!target) throw new Error(`no ${probe.target} this week`);
      const r = runOver(
        sumSql({ source: probe.source, keep: probe.keep, measure: "revenue", per: "day" }),
        catalogueFor(w),
      );
      const checks = checkRows("table" in r ? r.table : undefined, target).filter(
        (c) => c.expected !== null,
      );
      const matching = checks.filter((c) => c.same).length;
      const answer = matching === checks.length ? "all" : matching === 0 ? "none" : "some";
      return { kind: "days-matching", answer, matching, total: checks.length, checks };
    }
  }
}
