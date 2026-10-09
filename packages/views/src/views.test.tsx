// @vitest-environment jsdom
// Copyright © 2026 Christopher Snow

// The figures' own logic: the grader's verdicts, what storage shows differently after a change,
// how a list of names is written, and the figures that wait for a pass, take a prediction before
// they answer, or hide a challenge's answer until it is solved, driven through Chapter 1's page.

import { fireEvent, render, within } from "@testing-library/react";
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
  grade,
  runtimeStrings,
  showTime,
  storageDifferences,
} from "./index";
import { listOf } from "./figures/QuestionMap";

const lesson = parseLesson(LESSONS[0]!);
const rebuild = lesson.challenges.find((c) => c.id === "rebuild-daily-sales") as Challenge;
const rules = lesson.challenges.find((c) => c.id === "clean-orders-rules") as Challenge;

describe("the grader", () => {
  it("says why a query cannot run, instead of failing every day", () => {
    const v = grade(rebuild, {
      answers: { source: "customers.parquet", keep: "all", measure: "revenue", per: "day" },
    });
    expect(v.passed).toBe(false);
    expect(v.failures).toEqual([]);
    // The first column the query needs, in the order it is written, is the day it groups by.
    expect(v.blocked).toBe("customers.parquet has no column called ordered_at.");
  });

  it("reports a day with no row in the learner's result as 'no row'", () => {
    const v = grade(rebuild, {
      answers: { source: "clean_orders", keep: "cancelled", measure: "revenue", per: "day" },
    });
    expect(v.failures.length).toBeGreaterThan(0);
    expect(Object.values(v.failures[0]!.actual)).toEqual([V.noRow]);
  });

  it("names the orders a set of cleaning rules drops or keeps wrongly", () => {
    const v = grade(rules, {
      answers: { duplicates: "one", missingCustomer: "drop", cancelled: "drop", quantity: "keep" },
    });
    expect(v.failures).toHaveLength(1);
    expect(v.failures[0]!.detail).toBe(
      "Your rules drop 2 rows that clean_orders keeps, orders 7009, 7037.",
    );
  });
});

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
  type Labelled = { id?: string; value?: string; label: string };
  const props = (id: string) =>
    lesson.sections.flatMap((s) => s.interactives).find((x) => x.id === id)?.props as Record<
      string,
      unknown
    >;
  const changeLabel = (id: string) =>
    (props("changes")["changes"] as Labelled[]).find((c) => c.id === id)!.label;
  const passing = (id: string) => (store: LessonStore) =>
    store.setChallenge(id, (c) => ({
      ...c,
      artifact: lesson.challenges.find((x) => x.id === id)!.reference,
    }));

  it("starts the failure experiment only once the learner's own query passes", () => {
    const locked = show();
    expect(locked.figure("changes").textContent).toContain(
      format(V.locked, { title: rebuild.title }),
    );
    expect(within(locked.figure("changes")).queryAllByRole("radio")).toEqual([]);
    locked.page.unmount();

    const { figure } = show(passing("rebuild-daily-sales"));
    expect(within(figure("changes")).getAllByRole("radio").length).toBeGreaterThan(1);
  });

  it("asks for a prediction before a change runs, then answers it from the lab", () => {
    const { figure } = show(passing("rebuild-daily-sales"));
    const f = within(figure("changes"));
    fireEvent.click(f.getByLabelText(changeLabel("copy")));
    const run = f.getByRole("button", { name: V.runWithChange });
    expect(run).toHaveProperty("disabled", true);
    expect(figure("changes").querySelector(".change-result")).toBeNull();
    const options = (props("changes")["prediction"] as { options: Labelled[] }).options;
    fireEvent.click(f.getByLabelText(options.find((o) => o.value === "twoOrMore")!.label));
    fireEvent.click(run);
    expect(f.getByRole("status").textContent).toContain(V.match);
    expect(figure("changes").querySelectorAll(".change-fits li")).toHaveLength(2);
  });

  it("marks a row only the learner's query gives as extra, not as a difference", () => {
    const { figure } = show(passing("rebuild-daily-sales"));
    const f = within(figure("changes"));
    fireEvent.click(f.getByLabelText(changeLabel("failed")));
    const options = (props("changes")["prediction"] as { options: Labelled[] }).options;
    fireEvent.click(f.getByLabelText(options.find((o) => o.value === "one")!.label));
    fireEvent.click(f.getByRole("button", { name: V.runWithChange }));
    // Six days the same, and Sunday's row, which daily_sales lacks after the failed night: the
    // query still rebuilds daily_sales, so Sunday is extra, not a difference.
    const marks = [...figure("changes").querySelectorAll(".days-table tbody tr")].map(
      (r) => r.lastElementChild,
    );
    expect(marks.map((m) => m?.textContent)).toEqual([...Array<string>(6).fill(V.yes), V.extraRow]);
    expect(marks[6]?.className).toBe("is-extra");
  });

  it("shows the rows the rules keep only once the rules on screen are run", () => {
    const run = runtimeStrings().challenge.run;
    const section = (container: HTMLElement) =>
      container.querySelector<HTMLElement>(
        'section.challenge[data-challenge="clean-orders-rules"]',
      )!;
    const fresh = section(show().page.container);
    expect(fresh.querySelector(".choice-rows")).toBeNull();
    expect(fresh.textContent).toContain(V.keptAfterRun);
    fireEvent.click(within(fresh).getByRole("button", { name: run }));
    expect(fresh.querySelector(".choice-rows")).not.toBeNull();
    expect(fresh.textContent).not.toContain(V.keptAfterRun);
    // A change to a rule drops what the run showed until the tests run again.
    const field = rules.fields[0]!;
    const select = within(fresh).getByLabelText(field.label) as HTMLSelectElement;
    const other = (field.options ?? []).find((o) => o.value !== select.value)!;
    fireEvent.change(select, { target: { value: other.value } });
    expect(fresh.querySelector(".choice-rows")).toBeNull();
    expect(fresh.textContent).toContain(V.keptAfterRun);
    // Saved rules are graded as the page loads, so what they keep shows at once.
    const saved = section(show(passing("clean-orders-rules")).page.container);
    const kept = week().tables.get("clean_orders")!.rows.length;
    expect(saved.textContent).toContain(format(V.keptRows, { count: kept }));
  });

  it('answers "I can\'t tell yet" with what the lab found, and marks it neither right nor wrong', () => {
    const p = props("predict-days") as {
      options: Labelled[];
      undecided: Labelled & { line: string };
    };
    const { figure } = show((store) => store.setSlot("predict-days", { choice: "undecided" }));
    const status = figure("predict-days").querySelector("[role=status]")!;
    expect(status.textContent).toBe(
      format(p.undecided.line, { answer: p.options.find((o) => o.value === "different")!.label }),
    );
    expect(status.textContent).not.toContain(V.match);
    expect(status.textContent).not.toContain(V.noMatch);
  });

  it("treats a prediction saved against options the lesson no longer offers as not made", () => {
    const { figure } = show((store) => store.setSlot("predict-days", { choice: "some" }));
    expect(figure("predict-days").querySelector("[role=status]")).toBeNull();
    expect(
      within(figure("predict-days")).getByRole("button", { name: V.checkPrediction }),
    ).toBeTruthy();
  });

  it("opens on the situation and the lab, then the map with its count, then the week", () => {
    const { page, figure } = show();
    const opening = page.container.querySelector<HTMLElement>('section[data-kind="question"]')!;
    // How the lab runs waits behind a control, closed, between the lab's paragraph and the map.
    const details = opening.querySelector<HTMLDetailsElement>("details.lesson-details")!;
    expect(details.open).toBe(false);
    expect(details.querySelector("summary")?.textContent).toBe(
      lesson.sections[0]!.details?.summary,
    );
    const after = (a: Node, b: Node) =>
      Boolean(a.compareDocumentPosition(b) & Node.DOCUMENT_POSITION_FOLLOWING);
    expect(after(details, figure("platform"))).toBe(true);
    expect([...opening.querySelectorAll("figure.interactive")].map((f) => f.id)).toEqual([
      "ix-platform",
      "ix-week",
      "ix-explore",
      "ix-dashboard",
    ]);
    // The map counts what it shows, kind by kind and in all, as the lab counts it.
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

  it("badges every figure by what it asks of the learner, and opens that role's line alone", () => {
    const { figure } = show();
    for (const x of lesson.sections.flatMap((s) => s.interactives)) {
      const role = x.role ?? "";
      expect(figure(x.id).dataset["role"], x.id).toBe(role);
      expect(figure(x.id).querySelector("figcaption .badge")?.textContent, x.id).toBe(
        V.roles[role],
      );
      // A role with a line opens it; a reference has none, and its badge opens nothing.
      const toggle = within(figure(x.id)).queryByRole("button", {
        name: format(V.roleBadgeLabel, { role: V.roles[role] ?? "" }),
      });
      expect(toggle !== null, x.id).toBe(Boolean(V.roleNotes[role]));
    }
    const explore = figure("explore");
    fireEvent.click(
      within(explore).getByRole("button", {
        name: format(V.roleBadgeLabel, { role: V.roles["inspect"] ?? "" }),
      }),
    );
    const note = explore.querySelector(".time-model-note")!;
    expect(note.hasAttribute("hidden")).toBe(false);
    expect(note.textContent?.trim()).toBe(V.roleNotes["inspect"]);
    // The lab is explained once, where the chapter first names it, and behind no badge.
    expect(note.textContent).not.toContain("Metadata Lab");
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
