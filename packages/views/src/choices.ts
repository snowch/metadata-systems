// Copyright © 2026 Christopher Snow

// A challenge's answers read as the lab's choices, and described in the challenge's own words.
// The words for each option are the challenge's (its fields' option labels), so a figure that
// describes a query says it the way the builder offered it.

import { CLEAN_SPACE, KEEP, MEASURE, PER, type CleanChoice, type SumChoice } from "@ms/lab";
import type { Artifact, Challenge } from "@platform/lesson-schema";

import { format, type ViewStrings } from "./strings";

/** The answers a challenge is graded on: its starting answers, then the learner's. */
export function answersOf(challenge: Challenge, artifact: Artifact): Record<string, string> {
  return { ...(challenge.initial.answers ?? {}), ...(artifact.answers ?? {}) };
}

const oneOf = <T extends string>(values: readonly T[], v: string | undefined): T | undefined =>
  values.includes(v as T) ? (v as T) : undefined;

/** The sum a learner chose, or undefined while a choice is missing. */
export function sumChoiceOf(answers: Readonly<Record<string, string>>): SumChoice | undefined {
  const keep = oneOf(KEEP, answers["keep"]);
  const measure = oneOf(MEASURE, answers["measure"]);
  const per = oneOf(PER, answers["per"]);
  const source = answers["source"];
  if (!keep || !measure || !per || !source) return undefined;
  return { source: source as SumChoice["source"], keep, measure, per };
}

/** The cleaning rules a learner chose, or undefined while a choice is missing. */
export function cleanChoiceOf(answers: Readonly<Record<string, string>>): CleanChoice | undefined {
  const pick = CLEAN_SPACE.find(
    (c) =>
      c.duplicates === answers["duplicates"] &&
      c.missingCustomer === answers["missingCustomer"] &&
      c.cancelled === answers["cancelled"] &&
      c.quantity === answers["quantity"],
  );
  return pick;
}

/** A field's label for one of its options, or the value itself. */
export function optionLabel(
  challenge: Challenge | undefined,
  field: string,
  value: string,
): string {
  const f = challenge?.fields.find((x) => x.id === field);
  return f?.options?.find((o) => o.value === value)?.label ?? value;
}

/** A sum described in the builder's words: "from clean_orders, completed orders only, ...". */
export function describeSum(
  c: SumChoice,
  challenge: Challenge | undefined,
  strings: ViewStrings,
): string {
  return format(strings.describeQuery, {
    source: optionLabel(challenge, "source", c.source),
    keep: optionLabel(challenge, "keep", c.keep),
    measure: optionLabel(challenge, "measure", c.measure),
    per: optionLabel(challenge, "per", c.per),
  });
}
