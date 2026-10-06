// @vitest-environment jsdom
// Copyright © 2026 Christopher Snow

// The figures' own logic, apart from any chapter: the grader's verdicts, what storage shows
// differently after a change, and how a list of names is written.

import { describe, expect, it } from "vitest";

import { week } from "@ms/lab";
import type { Challenge } from "@platform/lesson-schema";
import { parseLesson } from "@platform/lesson-schema";

import { LESSONS } from "@ms/content";

import { DEFAULT_VIEW_STRINGS as V, grade, storageDifferences } from "./index";
import { listOf } from "./figures/QuestionMap";

const lesson = parseLesson(LESSONS[0]!);
const rebuild = lesson.challenges.find((c) => c.id === "rebuild-daily-sales") as Challenge;
const rules = lesson.challenges.find((c) => c.id === "clean-orders-rules") as Challenge;

describe("the grader", () => {
  it("says why a query cannot run, instead of failing every day", () => {
    const v = grade(rebuild, {
      answers: { source: "customers.parquet", keep: "all", measure: "revenue", per: "day" },
    });
    expect(v.passed).toBe(false);
    expect(v.failures).toEqual([]);
    // The first column the query needs, in the order it is written, is the day it groups by.
    expect(v.blocked).toBe("customers.parquet has no column called ordered_at.");
  });

  it("reports a day with no row in the learner's result as 'no row'", () => {
    const v = grade(rebuild, {
      answers: { source: "clean_orders", keep: "cancelled", measure: "revenue", per: "day" },
    });
    expect(v.failures.length).toBeGreaterThan(0);
    expect(Object.values(v.failures[0]!.actual)).toEqual([V.noRow]);
  });

  it("names the orders a set of cleaning rules drops or keeps wrongly", () => {
    const v = grade(rules, {
      answers: { duplicates: "one", missingCustomer: "drop", cancelled: "drop", quantity: "keep" },
    });
    expect(v.failures).toHaveLength(1);
    expect(v.failures[0]!.detail).toBe(
      "Your rules drop 2 rows that clean_orders keeps, orders 7009, 7037.",
    );
  });
});

describe("what storage shows differently", () => {
  it("names the new file, the changed rows and the changed times", () => {
    expect(storageDifferences(week(), week(["copy"]), V)).toEqual([
      "A new file, clean_orders_copy.parquet, at s3://shop-scratch/clean_orders_copy.parquet.",
    ]);
    expect(storageDifferences(week(), week(["refunds"]), V)).toEqual([
      "In daily_sales, the row for Sat 12 reads 215.49, not 191.49.",
      "In sales_dashboard, the row for Sat 12 reads 215.49, not 191.49.",
    ]);
    expect(storageDifferences(week(), week(["failed"]), V)).toEqual([
      "daily_sales last written at 2026-09-13 02:30:21 UTC, not 2026-09-14 02:30:21 UTC.",
      "daily_sales has 6 rows, not 7.",
      "sales_dashboard has 6 rows, not 7.",
    ]);
    expect(storageDifferences(week(), week(), V)).toEqual([]);
  });
});

describe("a list of names", () => {
  it("joins the last two with 'and'", () => {
    expect(listOf([])).toBe("");
    expect(listOf(["a"])).toBe("a");
    expect(listOf(["a", "b"])).toBe("a and b");
    expect(listOf(["a", "b", "c"])).toBe("a, b and c");
  });
});
