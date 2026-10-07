// Copyright © 2026 Christopher Snow

// Sort the questions about one asset, then let the lab place them.
//
// The learner puts each question in one of three groups (storage records it, the data suggests
// it, or only a record kept at the time answers it) and commits. The lab then places every
// question by running the storage view and the query builder's search over the week, and the
// figure shows its placement with the evidence for each, marking where the learner's differs. A
// week selector runs the same placement on each change from the failure experiment, so a question
// visibly leaves a group when the shop changes. A question only a record can answer is tagged
// with the kind of record that would answer it. A query and its source are named only once the
// learner's own query passes, so the map does not hand over the construction challenge.

import { useId, useState } from "react";
import { z } from "zod";

import {
  ASSET_IDS,
  CHANGE_IDS,
  QUESTION_IDS,
  questionMap,
  recordKindOf,
  week,
  type Evidence,
  type Place,
  type QuestionId,
} from "@ms/lab";
import type { Challenge } from "@platform/lesson-schema";
import { useSlot, type InteractiveProps } from "@platform/lesson-runtime";
import { FaultInjector } from "@platform/primitives";

import { describeSum } from "../choices";
import { usePassed } from "../passed";
import { withProps } from "../props";
import { Rich, code } from "../Rich";
import { showDay, showTime } from "../show";
import { format, useViewStrings, type ViewStrings } from "../strings";

const Props = z.object({
  asset: z.enum(ASSET_IDS).default("daily_sales"),
  /** The construction challenge: its words describe a query, and its pass names one. */
  challengeId: z.string().min(1),
  /** The changes the week selector offers, with the failure experiment's labels. */
  weeks: z.array(z.object({ id: z.enum(CHANGE_IDS), label: z.string().min(1) })).default([]),
});

const PLACES: readonly Place[] = ["storage", "suggested", "record"];

interface Sort {
  readonly placed: Partial<Record<QuestionId, Place>>;
  readonly checked: boolean;
}

/** Names as a list a reader says: "a", "a and b", "a, b and c". */
export function listOf(names: readonly string[]): string {
  if (names.length < 2) return names.join("");
  return `${names.slice(0, -1).join(", ")} and ${names[names.length - 1]}`;
}

export function evidenceText(
  question: QuestionId,
  e: Evidence,
  challenge: Challenge | undefined,
  strings: ViewStrings,
  named: boolean,
): string {
  switch (e.kind) {
    case "time":
      return format(strings.e["time"] ?? "", { time: showTime(e.time) });
    case "queries": {
      const first = e.candidates[0];
      if (!first) return strings.e["noQuery"] ?? "";
      const sources = [...new Set(e.candidates.map((c) => c.source))];
      if (question === "made-from") {
        if (sources.length === 1)
          return named
            ? format(strings.e["oneSource"] ?? "", { source: first.source })
            : (strings.e["oneSourceHidden"] ?? "");
        return format(strings.e[named ? "manySources" : "manySourcesHidden"] ?? "", {
          count: sources.length,
          sources: listOf(sources.map(code)),
        });
      }
      if (e.candidates.length === 1)
        return named
          ? format(strings.e["oneQuery"] ?? "", { query: describeSum(first, challenge, strings) })
          : (strings.e["oneQueryHidden"] ?? "");
      return format(strings.e[named ? "manyQueries" : "manyQueriesHidden"] ?? "", {
        count: e.candidates.length,
        sources: listOf(sources.map(code)),
      });
    }
    case "readers":
      return e.assets.length
        ? format(strings.e["readers"] ?? "", { assets: listOf(e.assets.map(code)) })
        : (strings.e["noReaders"] ?? "");
    case "night":
      return e.looksDone
        ? format(strings.e["nightDone"] ?? "", {
            time: showTime(e.lastWritten),
            day: showDay(e.expectedRow, strings.weekdays),
          })
        : format(strings.e["nightMissing"] ?? "", {
            time: showTime(e.lastWritten),
            latest: e.latestRow ? showDay(e.latestRow, strings.weekdays) : strings.noRow,
            expected: showDay(e.expectedRow, strings.weekdays),
          });
    case "account":
      return format(strings.e["account"] ?? "", { role: e.role });
    case "types":
      return format(strings.e["types"] ?? "", { column: e.column, type: e.type });
    case "current-only":
      return strings.e["currentOnly"] ?? "";
  }
}

export const QuestionMap = withProps(
  Props,
  function QuestionMap({
    data,
    lesson,
    interactive,
    store,
  }: InteractiveProps & { data: z.infer<typeof Props> }) {
    const strings = useViewStrings();
    const id = useId();
    const [sort, setSort] = useSlot<Sort>(store, interactive.id);
    const [shownWeek, setShownWeek] = useState(-1);
    const named = usePassed(lesson, store, data.challengeId);
    const challenge = lesson.challenges.find((c) => c.id === data.challengeId);
    // Only places the figure offers count: anything else in storage is no placement at all.
    const placed = Object.fromEntries(
      Object.entries(sort?.placed ?? {}).filter(([, p]) => PLACES.includes(p as Place)),
    ) as Partial<Record<QuestionId, Place>>;
    const first = questionMap(week(), data.asset);
    const placeIn = (q: QuestionId, entries = first) =>
      entries.find((e) => e.question === q)?.place;

    if (!sort?.checked) {
      const complete = QUESTION_IDS.every((q) => placed[q] !== undefined);
      return (
        <div className="question-sort">
          <fieldset className="sort-questions">
            <legend>
              <Rich text={format(strings.sortLegend, { asset: data.asset })} />
            </legend>
            {QUESTION_IDS.map((q) => (
              <div key={q} className="choice-field">
                <label className="choice-label" htmlFor={`${id}-${q}`}>
                  {strings.q[q]}
                </label>
                <select
                  id={`${id}-${q}`}
                  value={placed[q] ?? ""}
                  onChange={(e) =>
                    setSort({
                      checked: false,
                      placed: { ...placed, [q]: (e.target.value || undefined) as Place },
                    })
                  }
                >
                  <option value="">{strings.sortPick}</option>
                  {PLACES.map((p) => (
                    <option key={p} value={p}>
                      {strings.place[p]}
                    </option>
                  ))}
                </select>
              </div>
            ))}
          </fieldset>
          <button
            type="button"
            className="button primary"
            disabled={!complete}
            onClick={() => setSort({ placed, checked: true })}
          >
            {strings.checkSort}
          </button>
        </div>
      );
    }

    const change = shownWeek >= 0 ? data.weeks[shownWeek] : undefined;
    const entries = change ? questionMap(week([change.id]), data.asset) : first;
    const matching = QUESTION_IDS.filter((q) => placed[q] === placeIn(q)).length;
    return (
      <div className="question-sort" data-checked="true">
        <p role="status" className="sort-score">
          {format(strings.sortScore, { matching, total: QUESTION_IDS.length })}
        </p>
        {data.weeks.length > 0 && (
          <FaultInjector
            name={`${interactive.id}-week`}
            legend={strings.weekLegend}
            noneLabel={strings.firstWeek}
            faults={data.weeks}
            chosen={shownWeek}
            onChoose={setShownWeek}
          />
        )}
        <div className="question-map" data-week={change?.id ?? "first"}>
          {PLACES.map((place) => (
            <section
              key={place}
              className={`map-column map-${place}`}
              aria-label={strings.place[place]}
            >
              <h4>{strings.place[place]}</h4>
              <ul>
                {entries
                  .filter((e) => e.place === place)
                  .map((e) => {
                    const mine = placed[e.question];
                    const was = placeIn(e.question);
                    return (
                      <li key={e.question}>
                        <strong className="map-question">{strings.q[e.question]}</strong>
                        <span className="map-evidence">
                          <Rich
                            text={evidenceText(e.question, e.evidence, challenge, strings, named)}
                          />
                        </span>
                        {place === "record" && (
                          <span className="map-kind">
                            {format(strings.needsRecord, {
                              kind: strings.recordKind[recordKindOf(e.question)] ?? "",
                            })}
                          </span>
                        )}
                        {change && was && was !== place && (
                          <span className="map-moved">
                            {format(strings.movedFrom, { place: strings.place[was] ?? "" })}
                          </span>
                        )}
                        {!change && mine && mine !== place && (
                          <span className="map-yours">
                            {format(strings.youPlaced, { place: strings.place[mine] ?? "" })}
                          </span>
                        )}
                      </li>
                    );
                  })}
              </ul>
            </section>
          ))}
        </div>
      </div>
    );
  },
);
