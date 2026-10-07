// Copyright © 2026 Christopher Snow

// Change the shop, predict, run the week again, and compare.
//
// The experiment re-runs the learner's own query from the construction challenge, so the figure
// starts once that query passes its tests. The learner picks a change and commits to a prediction
// (how many of the query builder's choices will rebuild the target); committing runs the whole
// week with the change in place. The figure then shows, each computed: every query in the
// builder's choices that rebuilds the target now, which answers the prediction; what storage holds
// on Monday morning, with the comparison against the week as it first ran labelled as the lab's,
// because storage in the changed week holds only its own values; and the learner's query against
// the new target. A change's outcome text shows once its prediction is committed, and the closing
// text once every change has run.

import { useState } from "react";
import { z } from "zod";

import {
  ASSET_IDS,
  CHANGE_IDS,
  catalogueFor,
  checkRows,
  formatValue,
  optionForCount,
  runOver,
  storage,
  sumReconstructions,
  sumSql,
  week,
  type AssetId,
  type ChangeId,
  type Week,
} from "@ms/lab";
import { Prose, useSlot, useStored, type InteractiveProps } from "@platform/lesson-runtime";
import { FaultInjector, PredictionChallenge, StateInspector } from "@platform/primitives";

import { answersOf, describeSum, sumChoiceOf } from "../choices";
import { challengeTitle, usePassed } from "../passed";
import { withProps } from "../props";
import { Rich, plain } from "../Rich";
import { ScrollRegion } from "../ScrollRegion";
import { matchCell, showDay, showTime } from "../show";
import { format, useViewStrings, type ViewStrings } from "../strings";

const CountOption = z.object({
  value: z.string().min(1),
  label: z.string().min(1),
  range: z.tuple([z.number().int().min(0), z.number().int().min(0)]),
});

const Props = z.object({
  changes: z
    .array(
      z.object({ id: z.enum(CHANGE_IDS), label: z.string().min(1), outcome: z.string().min(1) }),
    )
    .min(1),
  afterAll: z.string().default(""),
  /** The construction challenge whose query the figure runs. */
  challengeId: z.string().min(1),
  target: z.enum(ASSET_IDS).default("daily_sales"),
  /** Asked before each change runs; answered by how many queries rebuild the target. */
  prediction: z.object({ question: z.string().min(1), options: z.array(CountOption).min(2) }),
});

/**
 * What storage holds in a changed week that differs from the week as it first ran, as sentences
 * that give the value storage holds now and, labelled, the value the lab found in the first run.
 */
export function storageDifferences(plain: Week, changed: Week, strings: ViewStrings): string[] {
  const before = new Map(storage(plain).map((r) => [r.asset, r]));
  const out: string[] = [];
  for (const r of storage(changed)) {
    const b = before.get(r.asset);
    if (!b) {
      out.push(
        format(strings.newAsset, {
          asset: r.asset,
          location: r.location,
          time: showTime(r.lastWritten),
        }),
      );
      continue;
    }
    if (r.lastWritten !== b.lastWritten)
      out.push(
        format(strings.changedTime, {
          asset: r.asset,
          after: showTime(r.lastWritten),
          before: showTime(b.lastWritten),
        }),
      );
    if (r.rows !== b.rows)
      out.push(format(strings.changedRows, { asset: r.asset, after: r.rows, before: b.rows }));
    else {
      // Same number of rows: say which rows read differently, by their first column.
      const [k, v] = r.content.columns;
      if (!k || !v || r.content.columns.length !== 2) continue;
      r.content.rows.forEach((row, i) => {
        const was = b.content.rows[i];
        if (!was || JSON.stringify(row) === JSON.stringify(was)) return;
        out.push(
          format(strings.changedValue, {
            asset: r.asset,
            day: showDay(String(row[0]), strings.weekdays),
            after: formatValue(row[1] ?? null, v.type),
            before: formatValue(was[1] ?? null, v.type),
          }),
        );
      });
    }
  }
  return out;
}

type Predictions = Partial<Record<ChangeId, string>>;

export const ChangeLab = withProps(
  Props,
  function ChangeLab({
    data,
    lesson,
    interactive,
    store,
  }: InteractiveProps & { data: z.infer<typeof Props> }) {
    const strings = useViewStrings();
    const stored = useStored(store);
    const passed = usePassed(lesson, store, data.challengeId);
    const [predictions, setPredictions] = useSlot<Predictions>(store, interactive.id);
    const [chosen, setChosen] = useState(-1);
    const challenge = lesson.challenges.find((c) => c.id === data.challengeId);

    if (!passed || !challenge)
      return (
        <p className="figure-locked" role="note">
          {format(strings.locked, { title: challengeTitle(lesson, data.challengeId) })}
        </p>
      );

    const saved = stored.challenges[data.challengeId]?.artifact;
    const choice = saved ? sumChoiceOf(answersOf(challenge, saved)) : undefined;
    const change = chosen >= 0 ? data.changes[chosen] : undefined;
    // A prediction saved against options the lesson no longer offers is no commitment at all.
    const savedChoice = change ? predictions?.[change.id] : undefined;
    const committed = data.prediction.options.some((o) => o.value === savedChoice)
      ? savedChoice
      : undefined;
    const label = (value: string) =>
      data.prediction.options.find((o) => o.value === value)?.label ?? value;

    // The week on show: the one the learner ran, or the week as it first ran.
    const shown = change ? (committed ? week([change.id]) : undefined) : week();
    const fits = shown ? sumReconstructions(shown, data.target, "covers") : [];
    const answer = optionForCount(fits.length, data.prediction.options);

    let result: React.ReactNode = null;
    if (shown) {
      const target = shown.tables.get(data.target as AssetId);
      const mine = choice ? runOver(sumSql(choice), catalogueFor(shown)) : undefined;
      const checks = target
        ? checkRows(mine && "table" in mine ? mine.table : undefined, target)
        : [];
      const diffs = change ? storageDifferences(week(), shown, strings) : [];
      result = (
        <div className="change-result">
          <p className="change-status">
            {change ? format(strings.ranWith, { change: change.label }) : strings.firstWeekStatus}
          </p>
          <section aria-label={plain(strings.fitsHeading)}>
            <h4>
              <Rich text={strings.fitsHeading} />
            </h4>
            {fits.length ? (
              <ul className="change-fits">
                {fits.map((f) => (
                  <li key={JSON.stringify(f)}>
                    <Rich text={describeSum(f, challenge, strings)} />
                  </li>
                ))}
              </ul>
            ) : (
              <p>{strings.fitsNone}</p>
            )}
          </section>
          {change && (
            <section aria-label={strings.storageNowHeading}>
              <h4>{strings.storageNowHeading}</h4>
              <p className="change-note">{strings.compareNote}</p>
              {diffs.length ? (
                <ul className="change-diffs">
                  {diffs.map((d) => (
                    <li key={d}>
                      <Rich text={d} />
                    </li>
                  ))}
                </ul>
              ) : (
                <p>{strings.noDiff}</p>
              )}
            </section>
          )}
          <section aria-label={plain(strings.yourQueryHeading)}>
            <h4>
              <Rich text={strings.yourQueryHeading} />
            </h4>
            <ScrollRegion label={plain(strings.yourQueryHeading)}>
              <StateInspector
                className="days-table"
                caption={plain(strings.yourQueryHeading)}
                headings={[strings.day, strings.yours, data.target, strings.same]}
                rows={checks.map((c) => ({
                  key: c.key,
                  name: showDay(c.key, strings.weekdays),
                  cells: [
                    { text: c.actual ?? strings.noRow },
                    { text: c.expected ?? strings.noRow },
                    matchCell(c, strings),
                  ],
                }))}
              />
            </ScrollRegion>
          </section>
          {change && <Prose markdown={change.outcome} className="change-outcome" />}
        </div>
      );
    }

    const allRan = data.changes.every((c) =>
      data.prediction.options.some((o) => o.value === predictions?.[c.id]),
    );
    return (
      <div className="change-lab" data-ran={Object.keys(predictions ?? {}).length}>
        <FaultInjector
          name={`${interactive.id}-change`}
          legend={strings.changeLegend}
          noneLabel={strings.firstWeek}
          faults={data.changes}
          chosen={chosen}
          onChoose={setChosen}
        />
        {change && (
          <div className="change-prediction">
            <Prose markdown={data.prediction.question} />
            <PredictionChallenge
              key={change.id}
              name={`${interactive.id}-${change.id}`}
              options={data.prediction.options}
              committed={committed}
              onCommit={(c) => setPredictions({ ...predictions, [change.id]: c })}
              legend={strings.yourPrediction}
              commitLabel={strings.runWithChange}
              verdict={
                committed !== undefined && (
                  <p
                    role="status"
                    className={answer === committed ? "prediction-match" : "prediction-nomatch"}
                  >
                    {format(strings.youSaid, { choice: label(committed) })}{" "}
                    {answer === committed ? (
                      <strong>{strings.match}</strong>
                    ) : (
                      <>
                        {format(strings.labFound, {
                          answer: answer ? label(answer) : fits.length,
                        })}{" "}
                        <strong>{strings.noMatch}</strong>
                      </>
                    )}
                  </p>
                )
              }
            />
          </div>
        )}
        {result}
        {allRan && data.afterAll && <Prose markdown={data.afterAll} className="change-after-all" />}
      </div>
    );
  },
);

// The changes this figure can offer, for the content tests.
export const CHANGE_LAB_CHANGES: readonly ChangeId[] = CHANGE_IDS;
