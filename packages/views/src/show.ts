// Copyright © 2026 Christopher Snow

// How the figures write the lab's values: times as storage writes them, sizes in kilobytes, days
// with their weekday. Nothing here depends on the browser's locale or time zone.

import { DAYS } from "@ms/lab";

/** The non-breaking hyphen, so a date never breaks across two lines. */
const NB_HYPHEN = "\u2011";

/** "2026-09-14T02:30:21Z" as "2026-09-14 02:30:21 UTC", with hyphens that do not break. */
export function showTime(timestamp: string): string {
  return `${timestamp.slice(0, 10).replaceAll("-", NB_HYPHEN)} ${timestamp.slice(11, 19)} UTC`;
}

/** Bytes as kilobytes with one place: "3.5 kB". */
export function showSize(bytes: number): string {
  return `${(Math.round(bytes / 100) / 10).toFixed(1)} kB`;
}

/** Midnight UTC of a date written "2026-09-10", in milliseconds. */
const midnight = (day: string) =>
  Date.UTC(Number(day.slice(0, 4)), Number(day.slice(5, 7)) - 1, Number(day.slice(8, 10)));

/** The weekday of a date, by the figure's names for Monday to Sunday: the week starts on a Monday. */
export function weekdayOf(day: string, names: readonly string[]): string {
  const offset = Math.round((midnight(day) - midnight(DAYS[0])) / 86_400_000);
  if (!Number.isFinite(offset)) return day;
  return names[((offset % 7) + 7) % 7] ?? day;
}

/** "2026-09-10" as "Thu 10", with the figure's weekday names. */
export function showDay(day: string, names: readonly string[]): string {
  return `${weekdayOf(day, names)} ${Number(day.slice(8, 10))}`;
}

/**
 * A day's mark where a query is set beside the asset it should rebuild: the same, different, or a
 * row only the query gives. The last does not stop the query rebuilding the asset, which needs
 * every row the asset has, so it is marked as the query's own, in no colour, not as a difference.
 * Where the question is whether two totals are equal day by day, a missing day is a difference,
 * and the table marks it "No" (the Thursday prediction's).
 */
export function matchCell(
  check: { readonly expected: string | null; readonly same: boolean },
  words: { readonly yes: string; readonly no: string; readonly extraRow: string },
): { text: string; className: string } {
  if (check.same) return { text: words.yes, className: "is-same" };
  if (check.expected === null) return { text: words.extraRow, className: "is-extra" };
  return { text: words.no, className: "is-different" };
}
