// @vitest-environment jsdom
// Copyright © 2026 Christopher Snow

// The figures' own logic: the grader's verdicts, what storage shows differently after a change,
// how a list of names is written, and the figures that wait for a pass, take a prediction before
// they answer, or hide a challenge's answer until it is solved, driven through Chapter 1's page.

import { render, within } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { mapTally, platformMap, sumReconstructions, week, weekTimeline } from "@ms/lab";
import type { Challenge } from "@platform/lesson-schema";
import { parseLesson } from "@platform/lesson-schema";
import { LessonStore, LessonView, memoryStorage } from "@platform/lesson-runtime";

import { LESSONS } from "@ms/content";

import {
  DEFAULT_VIEW_STRINGS as V,
  createBook,
  evidenceText,
  format,
  runtimeStrings,
  showTime,
  storageDifferences,
} from "./index";
import { listOf } from "./figures/QuestionMap";

const lesson = parseLesson(LESSONS[0]!);
const rebuild = lesson.challenges.find((c) => c.id === "rebuild-daily-sales") as Challenge;

describe("what storage shows differently", () => {
  it("names the new file, the changed rows and the changed times, with the first run's values", () => {
    expect(storageDifferences(week(), week(["copy"]), V)).toEqual([
      format(V.newAsset, {
        asset: "clean_orders_copy.parquet",
        location: "s3://shop-scratch/clean_orders_copy.parquet",
        time: showTime("2026-09-14T02:15:17Z"),
      }),
    ]);
    const sat = { day: "Sat 12", after: "215.49", before: "191.49" };
    expect(storageDifferences(week(), week(["refunds"]), V)).toEqual([
      format(V.changedValue, { asset: "daily_sales", ...sat }),
      format(V.changedValue, { asset: "sales_dashboard", ...sat }),
    ]);
    expect(storageDifferences(week(), week(["failed"]), V)).toEqual([
      format(V.changedTime, {
        asset: "daily_sales",
        after: showTime("2026-09-13T02:30:21Z"),
        before: showTime("2026-09-14T02:30:21Z"),
      }),
      format(V.changedRows, { asset: "daily_sales", after: 6, before: 7 }),
      format(V.changedRows, { asset: "sales_dashboard", after: 6, before: 7 }),
    ]);
    expect(storageDifferences(week(), week(), V)).toEqual([]);
  });

  it("writes a time whose date cannot break across two lines", () => {
    expect(showTime("2026-09-14T02:30:21Z")).toBe("2026\u201109\u201114 02:30:21 UTC");
  });
});

describe("the map's evidence", () => {
  const candidates = sumReconstructions(week(), "daily_sales", "covers");
  const e = { kind: "queries" as const, candidates };

  it("names no query or source until the construction challenge passes", () => {
    expect(evidenceText("computed", e, rebuild, V, false)).toBe(V.e["oneQueryHidden"]);
    expect(evidenceText("made-from", e, rebuild, V, false)).toBe(V.e["oneSourceHidden"]);
    expect(evidenceText("made-from", e, rebuild, V, true)).toBe(
      format(V.e["oneSource"] ?? "", { source: candidates[0]?.source ?? "" }),
    );
  });
});

describe("the figures on Chapter 1's page", () => {
  const book = createBook(LESSONS);
  const show = (prepare?: (store: LessonStore) => void) => {
    const storage = memoryStorage();
    prepare?.(new LessonStore(storage, book.id, lesson.id));
    const page = render(
      <LessonView book={book} lesson={lesson} storage={storage} strings={runtimeStrings()} />,
    );
    const figure = (id: string) => page.container.querySelector<HTMLElement>(`#ix-${id}`)!;
    return { page, figure };
  };

  it("opens on the situation, then the map with its count, then the week", () => {
    const { page, figure } = show();
    const opening = page.container.querySelector<HTMLElement>('section[data-kind="question"]')!;
    // Nothing waits behind a control: the page has no lab to explain.
    expect(opening.querySelector("details.lesson-details")).toBeNull();
    expect([...opening.querySelectorAll("figure.interactive")].map((f) => f.id)).toEqual([
      "ix-platform",
      "ix-week",
      "ix-explore",
      "ix-dashboard",
    ]);
    // The map counts what it shows, kind by kind and in all, as the engine counts it.
    const tally = mapTally(platformMap(week()));
    const counted = figure("platform").querySelector(".map-tally")?.textContent ?? "";
    for (const k of tally.kinds) {
      const forms = V.mapTally[k.kind]!;
      expect(counted).toContain(
        format(k.count === 1 ? forms.one : forms.other, { count: k.count }),
      );
    }
    expect(counted).toContain(format(V.mapTally["asset"]!.other, { count: tally.total }));
    // The week: a column a day and one for the morning you start, a bar at every night's work in
    // the early hours after its day, and one line at the morning you start.
    const t = weekTimeline(week());
    const w = figure("week");
    expect(w.querySelectorAll(".week-day")).toHaveLength(t.days.length + 1);
    expect(w.querySelector(".week-day.is-start")?.textContent).toContain("14");
    const bars = [...w.querySelectorAll<HTMLElement>(".week-night")];
    expect(bars).toHaveLength(t.nights.length);
    const columns = (t.days.length + 1) * 24;
    bars.forEach((bar, i) =>
      expect(parseFloat(bar.style.left)).toBeCloseTo((((i + 1) * 24 + 1) / columns) * 100, 2),
    );
    expect(parseFloat(w.querySelector<HTMLElement>(".week-start")!.style.left)).toBeCloseTo(
      ((t.days.length * 24 + 9) / columns) * 100,
      2,
    );
    expect(w.querySelector(".week-start-label")?.textContent).toBe(
      format(V.weekStart, { time: t.arrival.slice(11, 16) }),
    );
    // A screen reader hears the drawing as one sentence, with the week's first and last days.
    const heard = w.querySelector(".week-strip")?.getAttribute("aria-label") ?? "";
    for (const day of ["Mon 7", "Sun 13", "Mon 14", "09:00"]) expect(heard).toContain(day);
    // The week names no asset: it says when the nights were, not what they wrote.
    for (const id of ["orders.parquet", "clean_orders", "daily_sales", "sales_dashboard"])
      expect(w.textContent).not.toContain(id);
  });

  it("shows no badge, no mark and no note on any figure, and names no lab", () => {
    const { page, figure } = show();
    for (const x of lesson.sections.flatMap((s) => s.interactives)) {
      const f = figure(x.id);
      expect(f.dataset["timeModel"], x.id).toBe("none");
      expect(f.dataset["role"], x.id).toBeUndefined();
      expect(f.querySelector("figcaption .badge"), x.id).toBeNull();
      expect(f.querySelector(".time-model-note"), x.id).toBeNull();
      expect(within(f).queryAllByRole("button", { name: /this figure/ }), x.id).toEqual([]);
    }
    // The foot states no model note, and the page never names a lab.
    expect(page.container.querySelector(".lesson-model-note")).toBeNull();
    expect(page.container.textContent).not.toMatch(/\blab\b|Metadata Lab/i);
  });
});

describe("a list of names", () => {
  it("joins the last two with 'and'", () => {
    expect(listOf([])).toBe("");
    expect(listOf(["a"])).toBe("a");
    expect(listOf(["a", "b"])).toBe("a and b");
    expect(listOf(["a", "b", "c"])).toBe("a, b and c");
  });
});
