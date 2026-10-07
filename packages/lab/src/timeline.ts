// Copyright © 2026 Christopher Snow

// The shop's first week as a newcomer is shown it on Monday morning: the days the shop took
// orders, the night of work after each, and the morning the learner starts. It says when each
// night's work began and ended, and nothing about what a night wrote, which writer ran when, or
// which asset is made from which: Chapter 1 shows that storage cannot tell the last, so the week
// must not tell it either.

import { ARRIVAL, DAYS } from "./shop/data";
import { NIGHTS, dayBefore, type Week } from "./shop/week";

export interface TimelineNight {
  /** The date whose early hours the night's work fell in. */
  readonly date: string;
  /** The day it followed. */
  readonly after: string;
  /** When the night's first write began and its last ended. */
  readonly started: string;
  readonly finished: string;
}

export interface WeekTimeline {
  /** The days the shop took orders, Monday to Sunday. */
  readonly days: readonly string[];
  readonly nights: readonly TimelineNight[];
  /** When the learner starts work. */
  readonly arrival: string;
}

export function weekTimeline(w: Week): WeekTimeline {
  const nights = NIGHTS.map((date) => {
    const work = w.executions.filter((e) => e.night === date);
    if (work.length === 0) throw new Error(`no work on the night of ${date}`);
    const started = work.reduce((a, e) => (e.started < a ? e.started : a), work[0]!.started);
    const finished = work.reduce((a, e) => (e.finished > a ? e.finished : a), work[0]!.finished);
    return { date, after: dayBefore(date), started, finished };
  });
  return { days: [...DAYS], nights, arrival: ARRIVAL };
}
