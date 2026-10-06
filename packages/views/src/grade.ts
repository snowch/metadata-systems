// Copyright © 2026 Christopher Snow

// The book's grader: a challenge's answers run against the lab, case by case.
//
// - "reproduces": the learner's sum over one asset, compared with the target's row for each day.
// - "same-rows": the learner's cleaning rules over the raw orders, compared with clean_orders row
//   by row, as multisets: nothing missing, nothing extra.
//
// The lab computes what each case expects; the lesson's data holds no number.

import {
  catalogueFor,
  checkRows,
  cleanSql,
  diffRows,
  runOver,
  sumSql,
  week,
  type AssetId,
  type SqlProblem,
} from "@ms/lab";
import type { Artifact, Challenge } from "@platform/lesson-schema";
import type { Verdict, VerdictFailure } from "@platform/lesson-runtime";

import { answersOf, cleanChoiceOf, sumChoiceOf } from "./choices";
import { DEFAULT_VIEW_STRINGS, format, type ViewStrings } from "./strings";
import { showDay } from "./show";

/** A query's problem in the figures' words. */
export function problemText(p: SqlProblem, strings: ViewStrings = DEFAULT_VIEW_STRINGS): string {
  const template = strings.p[p.code] ?? strings.p["other"] ?? "";
  return format(template, p as unknown as Record<string, string>);
}

export function grade(
  challenge: Challenge,
  artifact: Artifact,
  strings = DEFAULT_VIEW_STRINGS,
): Verdict {
  const t = challenge.tests;
  if (t.kind !== "answers") throw new Error(`${challenge.id} is not graded case by case`);
  const total = t.cases.length;
  const answers = answersOf(challenge, artifact);
  const w = week();
  const catalogue = catalogueFor(w);
  if (t.grader === "reproduces") {
    const choice = sumChoiceOf(answers);
    if (!choice) return { passed: false, total, failures: [], blocked: strings.p["other"] ?? "" };
    const r = runOver(sumSql(choice), catalogue);
    if ("problem" in r)
      return { passed: false, total, failures: [], blocked: problemText(r.problem, strings) };
    const failures: VerdictFailure[] = [];
    t.cases.forEach((c, index) => {
      const target = w.tables.get(String(c.given["target"] ?? "daily_sales") as AssetId);
      if (!target) throw new Error(`${challenge.id}: no target`);
      const day = String(c.given["day"]);
      const check = checkRows(r.table, target).find((x) => x.key === day);
      if (check?.same) return;
      const valueName = r.table.columns[1]?.name ?? "";
      const targetName = target.columns[1]?.name ?? "";
      failures.push({
        index,
        label: c.label,
        inputs: { day: showDay(day, strings.weekdays) },
        actual: { [valueName]: check?.actual ?? strings.noRow },
        expected: { [targetName]: check?.expected ?? strings.noRow },
      });
    });
    return { passed: failures.length === 0, total, failures };
  }
  if (t.grader === "same-rows") {
    const choice = cleanChoiceOf(answers);
    if (!choice) return { passed: false, total, failures: [], blocked: strings.p["other"] ?? "" };
    const r = runOver(cleanSql(choice), catalogue);
    if ("problem" in r)
      return { passed: false, total, failures: [], blocked: problemText(r.problem, strings) };
    const target = w.tables.get("clean_orders");
    if (!target) throw new Error("no clean_orders");
    const diff = diffRows(r.table, target);
    const failures: VerdictFailure[] = [];
    t.cases.forEach((c, index) => {
      const missing = "missing" in c.expect;
      const ids = missing ? diff.missing : diff.extra;
      if (ids.length === 0) return;
      failures.push({
        index,
        label: c.label,
        inputs: {},
        actual: {},
        expected: {},
        detail: format(missing ? strings.missingRows : strings.extraRows, {
          count: ids.length,
          ids: ids.join(", "),
        }),
      });
    });
    return { passed: failures.length === 0, total, failures };
  }
  throw new Error(`${challenge.id}: no grader ${t.grader}`);
}
