// Copyright © 2026 Christopher Snow

// A requirement, questioned (CLAUDE.md, "Question the requirement"). The figure shows a
// requirement as it was written and asks what the learner would store to meet it; one option is to
// choose nothing yet. Once they have chosen, it shows the questions the requirement could be
// asking, each beside what it needs stored, with their choice marked. Only at a second press does
// the lab show what the platform records, and which of those questions the record answers. No
// reading is called right or wrong: each is a question somebody could mean, and the requirement
// does not say which. Both presses are kept, as a prediction is.

import { z } from "zod";

import { ASSET_IDS, runProbe, week } from "@ms/lab";
import { Prose, useSlot, type InteractiveProps } from "@platform/lesson-runtime";
import { PredictionChallenge } from "@platform/primitives";

import { withProps } from "../props";
import { Rich } from "../Rich";
import { ScrollRegion } from "../ScrollRegion";
import { format, useViewStrings } from "../strings";

const Props = z.object({
  /** The requirement, in the words it was written in. */
  requirement: z.string().min(1),
  /** What the learner is asked to choose. */
  question: z.string().min(1),
  /** The readings: what each would store, the question it asks, and the lab's answers it fits. */
  options: z
    .array(
      z.object({
        value: z.string(),
        label: z.string(),
        /** What the reading needs stored, for the table. */
        short: z.string().min(1),
        /** The question this reading asks, names between backticks. */
        asks: z.string().min(1),
        /** The kinds of owner the lab may find that answer this reading's question. */
        means: z.array(z.string().min(1)).min(1),
      }),
    )
    .min(2),
  /** The option to choose nothing until the requirement says what it is for. */
  undecided: z.object({ value: z.string(), label: z.string() }),
  probe: z.object({ kind: z.literal("owner-kind"), asset: z.enum(ASSET_IDS) }),
  buttons: z.object({ choose: z.string().min(1), show: z.string().min(1) }),
  headings: z.object({
    asks: z.string().min(1),
    store: z.string().min(1),
    answers: z.string().min(1),
  }),
  text: z.object({
    mine: z.string().includes("{choice}"),
    undecided: z.string().min(1),
    meanings: z.string().min(1),
    lab: z.string().includes("{value}").includes("{owned}").includes("{tables}"),
    explain: z.string().default(""),
  }),
});

export const RequirementLab = withProps(
  Props,
  function RequirementLab({
    data,
    interactive,
    store,
  }: InteractiveProps & { data: z.infer<typeof Props> }) {
    const strings = useViewStrings();
    const [saved, setStored] = useSlot<{ choice: string; shown?: boolean }>(store, interactive.id);
    // A choice saved against options the lesson no longer offers is no choice at all.
    const values = [...data.options.map((o) => o.value), data.undecided.value];
    const stored = saved && values.includes(saved.choice) ? saved : undefined;
    const result = stored?.shown ? runProbe(data.probe, week()) : undefined;
    const found = result?.kind === "owner-kind" ? result : undefined;
    const chosen = data.options.find((o) => o.value === stored?.choice);
    return (
      <div
        className="requirement-lab"
        data-step={!stored ? "choose" : found ? "shown" : "meanings"}
      >
        <div className="requirement">
          <p className="requirement-label">{strings.requirement}</p>
          <blockquote>
            <p>{data.requirement}</p>
          </blockquote>
        </div>
        <Prose markdown={data.question} />
        <PredictionChallenge
          name={`${interactive.id}-choice`}
          options={[...data.options.map(({ value, label }) => ({ value, label })), data.undecided]}
          committed={stored?.choice}
          onCommit={(choice) => setStored({ choice })}
          legend={strings.yourChoice}
          commitLabel={data.buttons.choose}
        />
        {stored && (
          <div className="requirement-meanings">
            <p role="status" className="prediction-compare">
              {chosen ? format(data.text.mine, { choice: chosen.label }) : data.text.undecided}
            </p>
            <Prose markdown={data.text.meanings} />
            <ScrollRegion label={data.requirement}>
              <table className="meanings-table">
                <caption>{data.requirement}</caption>
                <thead>
                  <tr>
                    <th scope="col">{data.headings.asks}</th>
                    <th scope="col">{data.headings.store}</th>
                    {found && <th scope="col">{data.headings.answers}</th>}
                  </tr>
                </thead>
                <tbody>
                  {data.options.map((o) => {
                    const answers = found !== undefined && o.means.includes(found.answer);
                    return (
                      <tr key={o.value} className={o === chosen ? "is-chosen" : undefined}>
                        <th scope="row">
                          <Rich text={o.asks} />
                        </th>
                        <td>
                          {o.short}
                          {o === chosen && (
                            <span className="chosen-mark">{strings.yourChoice}</span>
                          )}
                        </td>
                        {found && (
                          <td className={answers ? "answers-yes" : "answers-no"}>
                            {answers ? strings.yes : strings.no}
                          </td>
                        )}
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </ScrollRegion>
            {!found && (
              <button
                type="button"
                className="button primary"
                onClick={() => setStored({ ...stored, shown: true })}
              >
                {data.buttons.show}
              </button>
            )}
          </div>
        )}
        {found && (
          <div className="prediction-outcome">
            <p role="status" className="prediction-compare">
              <Rich
                text={format(data.text.lab, {
                  value: found.value ?? "",
                  owned: found.owned,
                  tables: found.tables,
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
