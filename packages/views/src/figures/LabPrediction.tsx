// Copyright © 2026 Christopher Snow

// Predict, then let the lab answer. The learner commits to one option before anything is shown;
// the lab then runs the prediction's probe on the week, and the page says what the lab found,
// whether it matched, and the evidence. A probe that counts answers with a number, and the option
// whose range holds it is the lab's answer. The answer is computed when the learner commits; the
// lesson's data never holds it. A prediction about a challenge's result can wait for the learner's
// own work on that challenge to pass.

import { z } from "zod";

import {
  ASSET_IDS,
  CHANGE_IDS,
  KEEP,
  optionForCount,
  runProbe,
  week,
  type ProbeResult,
} from "@ms/lab";
import { Prose, useSlot, type InteractiveProps } from "@platform/lesson-runtime";
import { PredictionChallenge, StateInspector } from "@platform/primitives";

import { challengeTitle, usePassed } from "../passed";
import { withProps } from "../props";
import { ScrollRegion } from "../ScrollRegion";
import { showDay } from "../show";
import { format, useViewStrings, type ViewStrings } from "../strings";

const Probe = z.discriminatedUnion("kind", [
  z.object({ kind: z.literal("owner-kind"), asset: z.enum(ASSET_IDS) }),
  z.object({
    kind: z.literal("days-matching"),
    source: z.enum(ASSET_IDS),
    keep: z.enum(KEEP),
    target: z.enum(ASSET_IDS),
  }),
  z.object({ kind: z.literal("clean-fits") }),
]);

const Props = z.object({
  question: z.string().min(1),
  options: z
    .array(
      z.object({
        value: z.string(),
        label: z.string(),
        /** For a probe that counts: the counts this option stands for, inclusive. */
        range: z.tuple([z.number().int().min(0), z.number().int().min(0)]).optional(),
      }),
    )
    .min(2),
  probe: Probe,
  explain: z.string().default(""),
  changes: z.array(z.enum(CHANGE_IDS)).default([]),
  /** A challenge whose work must pass before the prediction is asked. */
  requires: z.string().optional(),
});

/** The option the lab's result stands for. */
export function labAnswer(
  result: ProbeResult,
  options: z.infer<typeof Props>["options"],
): string | undefined {
  return result.kind === "owner-kind" ? result.answer : optionForCount(result.count, options);
}

function Evidence({ result, strings }: { result: ProbeResult; strings: ViewStrings }) {
  // Only the days prediction has a table of evidence; the others' explanations say it.
  if (result.kind !== "days-matching") return null;
  return (
    <ScrollRegion label={strings.daysCaption}>
      <StateInspector
        className="days-table"
        caption={strings.daysCaption}
        headings={[strings.day, strings.addedUp, "daily_sales", strings.same]}
        rows={result.checks.map((c) => ({
          key: c.key,
          name: showDay(c.key, strings.weekdays),
          cells: [
            { text: c.actual ?? strings.noRow },
            { text: c.expected ?? strings.noRow },
            {
              text: c.same ? strings.yes : strings.no,
              className: c.same ? "is-same" : "is-different",
            },
          ],
        }))}
      />
    </ScrollRegion>
  );
}

export const LabPrediction = withProps(
  Props,
  function LabPrediction({
    data,
    interactive,
    lesson,
    store,
  }: InteractiveProps & { data: z.infer<typeof Props> }) {
    const strings = useViewStrings();
    const [saved, setStored] = useSlot<{ choice: string }>(store, interactive.id);
    // A choice saved against options the lesson no longer offers is no commitment at all.
    const stored = data.options.some((o) => o.value === saved?.choice) ? saved : undefined;
    const ready = usePassed(lesson, store, data.requires ?? "") || data.requires === undefined;
    if (!ready)
      return (
        <p className="figure-locked" role="note">
          {format(strings.locked, { title: challengeTitle(lesson, data.requires ?? "") })}
        </p>
      );
    const result = stored ? runProbe(data.probe, week(data.changes)) : undefined;
    const answer = result ? labAnswer(result, data.options) : undefined;
    const label = (value: string) => data.options.find((o) => o.value === value)?.label ?? value;
    return (
      <div className="lab-prediction" data-committed={stored ? "true" : "false"}>
        <Prose markdown={data.question} />
        <PredictionChallenge
          name={`${interactive.id}-choice`}
          options={data.options}
          committed={stored?.choice}
          onCommit={(choice) => setStored({ choice })}
          legend={strings.yourPrediction}
          commitLabel={strings.checkPrediction}
        />
        {stored && result && (
          <div className="prediction-outcome">
            <p
              role="status"
              className={answer === stored.choice ? "prediction-match" : "prediction-nomatch"}
            >
              {format(strings.youSaid, { choice: label(stored.choice) })}{" "}
              {format(strings.labFound, { answer: answer ? label(answer) : "" })}{" "}
              {answer === stored.choice ? strings.match : strings.noMatch}
            </p>
            <Evidence result={result} strings={strings} />
            {data.explain && <Prose markdown={data.explain} />}
          </div>
        )}
      </div>
    );
  },
);
