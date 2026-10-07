// @vitest-environment jsdom
// Copyright © 2026 Christopher Snow

// The figures' own logic: the grader's verdicts, what storage shows differently after a change,
// how a list of names is written, and the figures that wait for a pass, take a prediction before
// they answer, or hide a challenge's answer until it is solved, driven through Chapter 1's page.

import { fireEvent, render, within } from "@testing-library/react";
import { describe, expect, it } from "vitest";

import { sumReconstructions, week } from "@ms/lab";
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

  it("takes the learner's sort of the questions before the lab places them, then moves them by week", () => {
    const { figure } = show();
    const f = within(figure("map"));
    const check = f.getByRole("button", { name: V.checkSort });
    expect(check).toHaveProperty("disabled", true);
    for (const select of f.getAllByRole("combobox"))
      fireEvent.change(select, { target: { value: "storage" } });
    fireEvent.click(check);
    expect(f.getByRole("status").textContent).toBe(format(V.sortScore, { matching: 1, total: 8 }));
    const weeks = props("map")["weeks"] as Labelled[];
    fireEvent.click(f.getByLabelText(weeks.find((w) => w.id === "refunds")!.label));
    const record = figure("map").querySelector(".map-record")!;
    expect(record.textContent).toContain(V.q["made-from"]);
    expect(record.textContent).toContain(
      format(V.movedFrom, { place: V.place["suggested"] ?? "" }),
    );
  });

  it("treats a prediction saved against options the lesson no longer offers as not made", () => {
    const { figure } = show((store) => store.setSlot("predict-days", { choice: "some" }));
    expect(figure("predict-days").querySelector("[role=status]")).toBeNull();
    expect(
      within(figure("predict-days")).getByRole("button", { name: V.checkPrediction }),
    ).toBeTruthy();
  });

  it("questions the requirement before it shows the warehouse, and marks only what it answers", () => {
    type Reading = { value: string; label: string; short: string; means: string[] };
    const p = props("predict-owner") as {
      options: Reading[];
      undecided: Labelled;
      buttons: { choose: string; show: string };
    };
    const { figure } = show();
    const f = within(figure("predict-owner"));
    expect(figure("predict-owner").querySelector("table")).toBeNull();
    const team = p.options.find((o) => o.value === "team")!;
    fireEvent.click(f.getByLabelText(team.label));
    fireEvent.click(f.getByRole("button", { name: p.buttons.choose }));
    // The four meanings, the learner's own marked, and nothing yet of what the warehouse holds.
    const rows = () => [...figure("predict-owner").querySelectorAll("tbody tr")];
    expect(rows()).toHaveLength(4);
    expect(rows().filter((r) => r.classList.contains("is-chosen"))).toHaveLength(1);
    expect(figure("predict-owner").querySelectorAll("thead th")).toHaveLength(2);
    expect(figure("predict-owner").textContent).not.toContain("etl_service");
    fireEvent.click(f.getByRole("button", { name: p.buttons.show }));
    expect(figure("predict-owner").querySelectorAll("thead th")).toHaveLength(3);
    expect(rows().map((r) => r.lastElementChild?.textContent)).toEqual([V.no, V.no, V.no, V.yes]);
    expect(figure("predict-owner").textContent).toContain("etl_service");
    expect(f.queryByRole("button", { name: p.buttons.show })).toBeNull();
  });

  it("takes 'nothing yet' as a choice, and forgets one the lesson no longer offers", () => {
    const p = props("predict-owner") as { undecided: Labelled; buttons: { choose: string } };
    const { page, figure } = show();
    const f = within(figure("predict-owner"));
    fireEvent.click(f.getByLabelText(p.undecided.label));
    fireEvent.click(f.getByRole("button", { name: p.buttons.choose }));
    expect(figure("predict-owner").querySelectorAll("tbody tr")).toHaveLength(4);
    expect(figure("predict-owner").querySelector(".is-chosen")).toBeNull();
    page.unmount();

    const stale = show((store) => store.setSlot("predict-owner", { choice: "some", shown: true }));
    expect(stale.figure("predict-owner").querySelector("table")).toBeNull();
    expect(
      within(stale.figure("predict-owner")).getByRole("button", { name: p.buttons.choose }),
    ).toBeTruthy();
  });

  it("asks how many rule settings pass only once the learner's rules pass", () => {
    expect(show().figure("predict-rules").textContent).toContain(
      format(V.locked, { title: rules.title }),
    );
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
