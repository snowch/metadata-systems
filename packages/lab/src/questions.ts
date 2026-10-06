// Copyright © 2026 Christopher Snow

// The questions Chapter 1 asks of the shop, and what can answer each.
//
// For one asset, a question is answered by what storage records, suggested by the data, or
// answered only by a record somebody kept at the time. The lab works out which by running the
// storage view and the inference searches, so a figure's three groups are computed, and they
// move when the shop changes: after an unrecorded edit to a program, the data no longer suggests
// where daily_sales comes from.
//
// Separately, each question has the kind of record that would answer it for certain: a record
// of what the asset is, of what happened, or of what was made from what. That is the course's
// classification, not a computation; the chapter derives its three kinds of metadata from it.

import { PROGRAM_ACCOUNT, type AssetId } from "./shop/assets";
import { PROGRAM_IDS } from "./shop/programs";
import { ARRIVAL, DAYS } from "./shop/data";
import type { Week } from "./shop/week";
import { recordOf, type StorageRecord } from "./storage";
import { storage } from "./lab";
import { sameNumbers, sumReconstructions, type SumChoice } from "./infer";
import { typeName } from "./values";

export const QUESTION_IDS = [
  "last-written",
  "made-from",
  "computed",
  "read-by",
  "worked",
  "responsible",
  "unit",
  "changed",
] as const;
export type QuestionId = (typeof QUESTION_IDS)[number];

/** What storage alone says about one asset, for the inspector. */
export type StorageAnswer =
  | { readonly kind: "answered"; readonly time: string }
  | { readonly kind: "columns"; readonly count: number }
  | { readonly kind: "title"; readonly title: string }
  | { readonly kind: "owner-role"; readonly role: string }
  | { readonly kind: "creator"; readonly person: string }
  | { readonly kind: "types"; readonly column: string; readonly type: string }
  | { readonly kind: "time-only"; readonly time: string }
  | { readonly kind: "nothing" };

export function storageAnswer(q: QuestionId, r: StorageRecord): StorageAnswer {
  switch (q) {
    case "last-written":
      return { kind: "answered", time: r.lastWritten };
    case "computed":
      // What storage holds about a calculation: a dashboard's title, a table's or a file's column
      // names. Neither says how the values were worked out.
      return r.title
        ? { kind: "title", title: r.title }
        : { kind: "columns", count: r.columns.length };
    case "responsible":
      if (r.ownerRole) return { kind: "owner-role", role: r.ownerRole };
      if (r.createdBy) return { kind: "creator", person: r.createdBy };
      return { kind: "nothing" };
    case "unit": {
      const money = r.columns.find((c) => c.type.kind === "decimal");
      return money
        ? { kind: "types", column: money.name, type: typeName(money.type) }
        : { kind: "nothing" };
    }
    case "worked":
      return { kind: "time-only", time: r.lastWritten };
    default:
      return { kind: "nothing" };
  }
}

export type Place = "storage" | "suggested" | "record";

export type Evidence =
  | { readonly kind: "time"; readonly time: string }
  | { readonly kind: "queries"; readonly candidates: readonly SumChoice[] }
  | { readonly kind: "readers"; readonly assets: readonly AssetId[] }
  | {
      readonly kind: "night";
      readonly lastWritten: string;
      readonly latestRow: string | null;
      readonly expectedRow: string;
      readonly looksDone: boolean;
    }
  | { readonly kind: "account"; readonly role: string; readonly programs: number }
  | { readonly kind: "types"; readonly column: string; readonly type: string }
  | { readonly kind: "current-only" };

export interface MapEntry {
  readonly question: QuestionId;
  readonly place: Place;
  readonly evidence: Evidence;
}

/** Each question about `asset`, placed by what can answer it, with the evidence. */
export function questionMap(w: Week, asset: AssetId = "daily_sales"): MapEntry[] {
  const r = recordOf(storage(w), asset);
  const candidates = sumReconstructions(w, asset, "covers");
  const readers = sameNumbers(w, asset);
  const latestRow = r.content.rows.length
    ? String(r.content.rows[r.content.rows.length - 1]?.[0] ?? null)
    : null;
  const expectedRow = DAYS[DAYS.length - 1] as string;
  const arrivalDay = ARRIVAL.slice(0, 10);
  const money = r.columns.find((c) => c.type.kind === "decimal");
  return QUESTION_IDS.map((question): MapEntry => {
    switch (question) {
      case "last-written":
        return { question, place: "storage", evidence: { kind: "time", time: r.lastWritten } };
      case "made-from":
      case "computed":
        return {
          question,
          place: candidates.length ? "suggested" : "record",
          evidence: { kind: "queries", candidates },
        };
      case "read-by":
        return {
          question,
          place: readers.length ? "suggested" : "record",
          evidence: { kind: "readers", assets: readers },
        };
      case "worked":
        return {
          question,
          place: "suggested",
          evidence: {
            kind: "night",
            lastWritten: r.lastWritten,
            latestRow,
            expectedRow,
            looksDone: r.lastWritten.slice(0, 10) === arrivalDay && latestRow === expectedRow,
          },
        };
      case "responsible":
        return {
          question,
          place: "record",
          evidence: {
            kind: "account",
            role: r.ownerRole ?? PROGRAM_ACCOUNT,
            programs: PROGRAM_IDS.length,
          },
        };
      case "unit":
        return {
          question,
          place: "record",
          evidence: money
            ? { kind: "types", column: money.name, type: typeName(money.type) }
            : { kind: "current-only" },
        };
      case "changed":
        return { question, place: "record", evidence: { kind: "current-only" } };
    }
  });
}

/** The kinds of record that answer a question for certain. */
export const RECORD_KINDS = ["what-it-is", "what-happened", "made-from-what"] as const;
export type RecordKind = (typeof RECORD_KINDS)[number];

const KIND_OF: Record<QuestionId, RecordKind> = {
  "last-written": "what-happened",
  "made-from": "made-from-what",
  computed: "made-from-what",
  "read-by": "made-from-what",
  worked: "what-happened",
  responsible: "what-it-is",
  unit: "what-it-is",
  changed: "what-happened",
};

/** The kind of record that would answer a question for certain, whatever storage holds. */
export function recordKindOf(q: QuestionId): RecordKind {
  return KIND_OF[q];
}
