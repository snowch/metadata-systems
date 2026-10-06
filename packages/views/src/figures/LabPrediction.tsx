// Copyright © 2026 Christopher Snow

// Predict, then let the lab answer. The learner commits to one option before anything is shown;
// the lab then runs the prediction's probe on the week, and the page says what the lab found,
// whether it matched, and the evidence. The answer is computed when the learner commits; the
// lesson's data never holds it.

import { z } from "zod";

import { ASSET_IDS, CHANGE_IDS, KEEP, runProbe, week, type ProbeResult } from "@ms/lab";
import { Prose, useSlot, type InteractiveProps } from "@platform/lesson-runtime";
import { PredictionChallenge, StateInspector } from "@platform/primitives";

import { withProps } from "../props";
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
]);

const Props = z.object({
  question: z.string().min(1),
  options: z.array(z.object({ value: z.string(), label: z.string() })).min(2),
  probe: Probe,
  explain: z.string().default(""),
  changes: z.array(z.enum(CHANGE_IDS)).default([]),
});

function Evidence({ result, strings }: { result: ProbeResult; strings: ViewStrings }) {
  // The owner prediction's explanation names the owner itself; a line before it would repeat it.
  if (result.kind === "owner-kind") return null;
  return (
    <div className="data-scroll" role="region" aria-label={strings.daysCaption} tabIndex={0}>
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
    </div>
  );
}

export const LabPrediction = withProps(
  Props,
  function LabPrediction({
    data,
    interactive,
    store,
  }: InteractiveProps & { data: z.infer<typeof Props> }) {
    const strings = useViewStrings();
    const [stored, setStored] = useSlot<{ choice: string }>(store, interactive.id);
    const result = stored ? runProbe(data.probe, week(data.changes)) : undefined;
    const label = (value: string) => data.options.find((o) => o.value === value)?.label ?? value;
    return (
      <div className="lab-prediction" data-committed={stored ? "true" : "false"}>
        <Prose markdown={data.question} />
        <PredictionChallenge
          name={`${interactive.id}-choice`}
          options={data.options}
          committed={stored?.choice}
          onCommit={(choice) => setStored({ choice })}
          onAgain={() => setStored(undefined)}
          legend={strings.yourPrediction}
          commitLabel={strings.checkPrediction}
          againLabel={strings.predictAgain}
        />
        {stored && result && (
          <div className="prediction-outcome">
            <p
              role="status"
              className={
                result.answer === stored.choice ? "prediction-match" : "prediction-nomatch"
              }
            >
              {format(strings.youSaid, { choice: label(stored.choice) })}{" "}
              {format(strings.labFound, { answer: label(result.answer) })}{" "}
              {result.answer === stored.choice ? strings.match : strings.noMatch}
            </p>
            <Evidence result={result} strings={strings} />
            {data.explain && <Prose markdown={data.explain} />}
          </div>
        )}
      </div>
    );
  },
);
