// Copyright © 2026 Christopher Snow

// An explanation to test (CLAUDE.md, "Interaction is the explanation": the effect before its
// cause). Once the learner has seen a difference, `hypothesis` asks which explanation they will
// test, keeps their choice and shows nothing more: the testing is theirs, with the figures that
// follow. `hypothesis-check` sits after the learner's own work (a challenge that must pass first)
// and, at a press, reads the rows: which explanations they support and which they rule out, with
// the learner's choice marked. It says what the rows show, never why, which is left to the
// chapter's own investigation. Both presses are kept, as a prediction is.

import { z } from "zod";

import { ASSET_IDS, DAYS, KEEP, runProbe, week } from "@ms/lab";
import { Prose, useSlot, type InteractiveProps } from "@platform/lesson-runtime";
import { PredictionChallenge } from "@platform/primitives";

import { challengeTitle, usePassed } from "../passed";
import { withProps } from "../props";
import { plain, Rich } from "../Rich";
import { ScrollRegion } from "../ScrollRegion";
import { format, useViewStrings } from "../strings";

/** An explanation the learner can choose, and what the rows must show for it to hold. */
const Explanation = z.object({
  value: z.string(),
  label: z.string(),
  /** The kinds of finding (`left`, `lower`, `moved`) that support it. */
  means: z.array(z.string().min(1)).min(1),
});

const Choose = z.object({
  question: z.string().min(1),
  options: z.array(Explanation).min(2),
  commit: z.string().min(1),
  /** After the choice: the learner's line, with `{choice}`, and how to test it. */
  mine: z.string().includes("{choice}"),
  test: z.string().min(1),
});

export const Hypothesis = withProps(
  Choose,
  function Hypothesis({
    data,
    interactive,
    store,
  }: InteractiveProps & { data: z.infer<typeof Choose> }) {
    const strings = useViewStrings();
    const [saved, setStored] = useSlot<{ choice: string }>(store, interactive.id);
    const chosen = data.options.find((o) => o.value === saved?.choice);
    return (
      <div className="hypothesis" data-committed={chosen ? "true" : "false"}>
        <Prose markdown={data.question} />
        <PredictionChallenge
          name={`${interactive.id}-choice`}
          options={data.options.map(({ value, label }) => ({ value, label }))}
          committed={chosen?.value}
          onCommit={(choice) => setStored({ choice })}
          legend={strings.yourChoice}
          commitLabel={data.commit}
        />
        {chosen && (
          <div className="prediction-outcome">
            <p role="status" className="prediction-compare">
              {format(data.mine, { choice: chosen.label })}
            </p>
            <Prose markdown={data.test} />
          </div>
        )}
      </div>
    );
  },
);

const Check = z.object({
  /** The `hypothesis` figure whose choice this checks, and its explanations, in its order. */
  of: z.string().min(1),
  options: z.array(Explanation).min(2),
  /** The challenge whose work must pass before the rows are read. */
  requires: z.string().min(1),
  probe: z.object({
    kind: z.literal("day-gap"),
    source: z.enum(ASSET_IDS),
    via: z.enum(ASSET_IDS),
    keep: z.enum(KEEP),
    target: z.enum(ASSET_IDS),
    day: z.enum(DAYS),
  }),
  button: z.string().min(1),
  headings: z.object({ explanation: z.string().min(1), supported: z.string().min(1) }),
  text: z.object({
    mine: z.string().includes("{choice}"),
    none: z.string().min(1),
    lab: z
      .string()
      .includes("{orders}")
      .includes("{kept}")
      .includes("{left}")
      .includes("{leftTotal}"),
    explain: z.string().default(""),
  }),
});

export const HypothesisCheck = withProps(
  Check,
  function HypothesisCheck({
    data,
    interactive,
    lesson,
    store,
  }: InteractiveProps & { data: z.infer<typeof Check> }) {
    const strings = useViewStrings();
    const [choice] = useSlot<{ choice: string }>(store, data.of);
    const [checked, setChecked] = useSlot<{ shown: boolean }>(store, interactive.id);
    const passed = usePassed(lesson, store, data.requires);
    if (!passed)
      return (
        <p className="figure-locked" role="note">
          {format(strings.locked, { title: challengeTitle(lesson, data.requires) })}
        </p>
      );
    const chosen = data.options.find((o) => o.value === choice?.choice);
    const result = checked?.shown ? runProbe(data.probe, week()) : undefined;
    const found = result?.kind === "day-gap" ? result : undefined;
    return (
      <div className="hypothesis-check" data-checked={found ? "true" : "false"}>
        <p className="prediction-compare">
          {chosen ? format(data.text.mine, { choice: chosen.label }) : data.text.none}
        </p>
        {!found ? (
          <button
            type="button"
            className="button primary"
            onClick={() => setChecked({ shown: true })}
          >
            {data.button}
          </button>
        ) : (
          <div className="prediction-outcome">
            <ScrollRegion label={plain(interactive.caption)}>
              <table className="meanings-table">
                <caption>{plain(interactive.caption)}</caption>
                <thead>
                  <tr>
                    <th scope="col">{data.headings.explanation}</th>
                    <th scope="col">{data.headings.supported}</th>
                  </tr>
                </thead>
                <tbody>
                  {data.options.map((o) => {
                    const supported = o.means.some((m) => (found.answer as string[]).includes(m));
                    return (
                      <tr key={o.value} className={o === chosen ? "is-chosen" : undefined}>
                        <th scope="row">
                          {o.label}
                          {o === chosen && (
                            <span className="chosen-mark">{strings.yourChoice}</span>
                          )}
                        </th>
                        <td className={supported ? "answers-yes" : "answers-no"}>
                          {supported ? strings.yes : strings.no}
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </ScrollRegion>
            <p role="status" className="prediction-compare">
              <Rich
                text={format(data.text.lab, {
                  orders: found.orders,
                  kept: found.kept,
                  left: found.left,
                  leftTotal: found.leftTotal,
                })}
              />
            </p>
            {data.text.explain && <Prose markdown={data.text.explain} />}
          </div>
        )}
      </div>
    );
  },
);
