// Copyright © 2026 Christopher Snow

// Every question about one asset, placed by what can answer it: storage, the data, or only a
// record kept at the time. The lab places each one by running the storage view and the query
// builder's search over the week, so the columns move when the shop changes.

import { z } from "zod";

import { ASSET_IDS, CHANGE_IDS, questionMap, week, type Evidence, type Place } from "@ms/lab";
import type { Challenge } from "@platform/lesson-schema";
import type { InteractiveProps } from "@platform/lesson-runtime";

import { describeSum } from "../choices";
import { withProps } from "../props";
import { showDay, showTime } from "../show";
import { format, useViewStrings, type ViewStrings } from "../strings";

const Props = z.object({
  asset: z.enum(ASSET_IDS).default("daily_sales"),
  changes: z.array(z.enum(CHANGE_IDS)).default([]),
  /** The challenge whose builder words describe a query. */
  challengeId: z.string().min(1),
});

const PLACES: readonly Place[] = ["storage", "suggested", "record"];

/** Names as a list a reader says: "a", "a and b", "a, b and c". */
export function listOf(names: readonly string[]): string {
  if (names.length < 2) return names.join("");
  return `${names.slice(0, -1).join(", ")} and ${names[names.length - 1]}`;
}

function evidenceText(
  question: string,
  e: Evidence,
  challenge: Challenge | undefined,
  strings: ViewStrings,
): string {
  switch (e.kind) {
    case "time":
      return format(strings.e["time"] ?? "", { time: showTime(e.time) });
    case "queries": {
      const first = e.candidates[0];
      if (!first) return strings.e["noQuery"] ?? "";
      const sources = [...new Set(e.candidates.map((c) => c.source))];
      if (question === "made-from")
        return sources.length === 1
          ? format(strings.e["oneSource"] ?? "", { source: first.source })
          : format(strings.e["manySources"] ?? "", {
              count: sources.length,
              sources: listOf(sources),
            });
      if (e.candidates.length === 1)
        return format(strings.e["oneQuery"] ?? "", {
          query: describeSum(first, challenge, strings),
        });
      return format(strings.e["manyQueries"] ?? "", {
        count: e.candidates.length,
        sources: listOf(sources),
      });
    }
    case "readers":
      return e.assets.length
        ? format(strings.e["readers"] ?? "", { assets: e.assets.join(", ") })
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
  function QuestionMap({ data, lesson }: InteractiveProps & { data: z.infer<typeof Props> }) {
    const strings = useViewStrings();
    const entries = questionMap(week(data.changes), data.asset);
    const challenge = lesson.challenges.find((c) => c.id === data.challengeId);
    return (
      <div className="question-map">
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
                .map((e) => (
                  <li key={e.question}>
                    <strong className="map-question">{strings.q[e.question]}</strong>
                    <span className="map-evidence">
                      {evidenceText(e.question, e.evidence, challenge, strings)}
                    </span>
                  </li>
                ))}
            </ul>
          </section>
        ))}
      </div>
    );
  },
);
