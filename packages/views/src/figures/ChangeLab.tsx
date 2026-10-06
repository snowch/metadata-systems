// Copyright © 2026 Christopher Snow

// Change the shop, run the week again, and compare. The learner picks one change (or none); the
// lab runs the whole week with it and the figure shows three things, each computed: what storage
// shows differently from the plain week; the learner's own query from the construction section
// (or the course's, if theirs does not pass yet) against the new target; and every query in the
// builder's choices that rebuilds the target now. Each change's outcome text shows only once that
// change has run, and the closing text once all have.

import { useState } from "react";
import { z } from "zod";

import {
  ASSET_IDS,
  CHANGE_IDS,
  catalogueFor,
  checkRows,
  formatValue,
  runOver,
  storage,
  sumReconstructions,
  sumSql,
  week,
  type AssetId,
  type ChangeId,
  type Week,
} from "@ms/lab";
import { Prose, useStored, type InteractiveProps } from "@platform/lesson-runtime";
import { FaultInjector, StateInspector } from "@platform/primitives";

import { answersOf, describeSum, sumChoiceOf } from "../choices";
import { grade } from "../grade";
import { withProps } from "../props";
import { showDay, showTime } from "../show";
import { format, useViewStrings, type ViewStrings } from "../strings";

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
});

/** What storage shows differently in a changed week, as sentences. */
export function storageDifferences(plain: Week, changed: Week, strings: ViewStrings): string[] {
  const before = new Map(storage(plain).map((r) => [r.asset, r]));
  const out: string[] = [];
  for (const r of storage(changed)) {
    const b = before.get(r.asset);
    if (!b) {
      out.push(format(strings.newAsset, { asset: r.asset, location: r.location }));
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

export const ChangeLab = withProps(
  Props,
  function ChangeLab({ data, lesson, store }: InteractiveProps & { data: z.infer<typeof Props> }) {
    const strings = useViewStrings();
    const stored = useStored(store);
    const [chosen, setChosen] = useState(-1);
    const [ran, setRan] = useState<{ index: number; id: ChangeId | null }[]>([]);
    const last = ran[ran.length - 1];
    const challenge = lesson.challenges.find((c) => c.id === data.challengeId);

    // The learner's own query, if it passes; the course's otherwise.
    const saved = stored.challenges[data.challengeId]?.artifact;
    const own = challenge && saved && grade(challenge, saved).passed;
    const choice = challenge
      ? sumChoiceOf(answersOf(challenge, own && saved ? saved : challenge.reference))
      : undefined;

    const run = () =>
      setRan((r) => [
        ...r,
        { index: chosen, id: chosen >= 0 ? (data.changes[chosen]?.id ?? null) : null },
      ]);
    const allRan = data.changes.every((c) => ran.some((r) => r.id === c.id));

    let result: React.ReactNode = null;
    if (last) {
      const changed = week(last.id ? [last.id] : []);
      const diffs = storageDifferences(week(), changed, strings);
      const target = changed.tables.get(data.target as AssetId);
      const mine = choice ? runOver(sumSql(choice), catalogueFor(changed)) : undefined;
      const checks = target
        ? checkRows(mine && "table" in mine ? mine.table : undefined, target)
        : [];
      // "Rebuilds" means every row the target has, as the question map counts it: after a failed
      // night the query still rebuilds all six rows, and gives one more.
      const fits = sumReconstructions(changed, data.target, "covers");
      const change = last.id ? data.changes.find((c) => c.id === last.id) : undefined;
      result = (
        <div className="change-result">
          <p role="status" className="change-status">
            {format(strings.ranWith, { change: change?.label ?? strings.noChange })}
          </p>
          <section aria-label={strings.storageDiffHeading}>
            <h4>{strings.storageDiffHeading}</h4>
            {diffs.length ? (
              <ul className="change-diffs">
                {diffs.map((d) => (
                  <li key={d}>{d}</li>
                ))}
              </ul>
            ) : (
              <p>{strings.noDiff}</p>
            )}
          </section>
          <section aria-label={strings.yourQueryHeading}>
            <h4>{strings.yourQueryHeading}</h4>
            <p className="change-note">{own ? strings.usingYours : strings.usingCourse}</p>
            <div
              className="data-scroll"
              role="region"
              aria-label={strings.yourQueryHeading}
              tabIndex={0}
            >
              <StateInspector
                className="days-table"
                caption={strings.yourQueryHeading}
                headings={[strings.day, strings.yours, data.target, strings.same]}
                rows={checks.map((c) => ({
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
          </section>
          <section aria-label={strings.fitsHeading}>
            <h4>{strings.fitsHeading}</h4>
            {fits.length ? (
              <ul className="change-fits">
                {fits.map((f) => (
                  <li key={JSON.stringify(f)}>{describeSum(f, challenge, strings)}</li>
                ))}
              </ul>
            ) : (
              <p>{strings.fitsNone}</p>
            )}
          </section>
          {change && <Prose markdown={change.outcome} className="change-outcome" />}
        </div>
      );
    }

    return (
      <div className="change-lab" data-ran={ran.length}>
        <FaultInjector
          name="change"
          legend={strings.changeLegend}
          noneLabel={strings.noChange}
          faults={data.changes}
          chosen={chosen}
          onChoose={setChosen}
        />
        <button type="button" className="button primary" onClick={run}>
          {strings.runWeek}
        </button>
        {result}
        {allRan && data.afterAll && <Prose markdown={data.afterAll} className="change-after-all" />}
      </div>
    );
  },
);

// The changes this figure can offer, for the content tests.
export const CHANGE_LAB_CHANGES: readonly ChangeId[] = CHANGE_IDS;
