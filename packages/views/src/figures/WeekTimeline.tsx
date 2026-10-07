// Copyright © 2026 Christopher Snow

// The shop's first week on one line: the days it took orders, a mark at each night's work where
// the lab ran it, and the morning the learner starts. Computed by the lab's weekTimeline, so it
// shows when the nights were and nothing about what they wrote.
//
// The line runs from the first day's midnight to the end of the day the learner starts, one
// column a day, and every mark stands where its time falls. Its words are the days' names, one
// line at the learner's morning and a key; a screen reader hears one sentence that says the same.

import type { CSSProperties } from "react";
import { z } from "zod";

import { CHANGE_IDS, week, weekTimeline } from "@ms/lab";
import type { InteractiveProps } from "@platform/lesson-runtime";

import { withProps } from "../props";
import { weekdayOf } from "../show";
import { format, useViewStrings } from "../strings";

const Props = z.object({
  changes: z.array(z.enum(CHANGE_IDS)).default([]),
});

const DAY_MS = 86_400_000;
/** A date ("2026-09-14") as its midnight, or a time ("2026-09-14T09:00:00Z") as itself, in ms. */
const msOf = (t: string) => Date.parse(t.length === 10 ? `${t}T00:00:00Z` : t);

export const WeekTimeline = withProps(
  Props,
  function WeekTimeline({ data }: InteractiveProps & { data: z.infer<typeof Props> }) {
    const strings = useViewStrings();
    const t = weekTimeline(week(data.changes));
    const first = t.days[0];
    const last = t.days[t.days.length - 1];
    const lastNight = t.nights[t.nights.length - 1];
    if (!first || !last || !lastNight) return null;
    const startDay = t.arrival.slice(0, 10);
    const columns = [...t.days, startDay];
    const from = msOf(first);
    const length = columns.length * DAY_MS;
    const at = (time: string) => `${(((msOf(time) - from) / length) * 100).toFixed(3)}%`;
    const across = (a: string, b: string) =>
      `${(((msOf(b) - msOf(a)) / length) * 100).toFixed(3)}%`;
    const day = (d: string) =>
      format(strings.weekDay, {
        weekday: weekdayOf(d, strings.weekdays),
        date: Number(d.slice(8, 10)),
      });
    const time = t.arrival.slice(11, 16);
    return (
      <div className="week-timeline" style={{ "--week-columns": columns.length } as CSSProperties}>
        <div
          className="week-strip"
          role="img"
          aria-label={format(strings.weekSummary, {
            first: day(first),
            last: day(last),
            night: day(lastNight.date),
            start: day(startDay),
            time,
          })}
        >
          <ol className="week-days">
            {columns.map((d) => (
              <li key={d} className={d === startDay ? "week-day is-start" : "week-day"}>
                <span className="week-weekday">{weekdayOf(d, strings.weekdays)}</span>{" "}
                <span className="week-date">{Number(d.slice(8, 10))}</span>
              </li>
            ))}
          </ol>
          <div className="week-track">
            <span className="week-orders" style={{ left: 0, width: across(first, startDay) }} />
            {t.nights.map((n) => (
              <span
                key={n.date}
                className="week-night"
                style={{ left: at(n.started), width: across(n.started, n.finished) }}
              />
            ))}
            <span className="week-start" style={{ left: at(t.arrival) }} />
          </div>
          <p className="week-start-label" style={{ right: `calc(100% - ${at(t.arrival)})` }}>
            {format(strings.weekStart, { time })}
          </p>
        </div>
        <ul className="week-key">
          <li>
            <span className="week-key-orders" aria-hidden="true" />
            {strings.weekOrders}
          </li>
          <li>
            <span className="week-key-night" aria-hidden="true" />
            {strings.weekNight}
          </li>
        </ul>
      </div>
    );
  },
);
