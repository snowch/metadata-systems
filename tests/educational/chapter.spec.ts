// Copyright © 2026 Christopher Snow

// The educational tests: every chapter renders whole; every challenge is completable through the
// page with its reference and refuses a wrong attempt; completion is recomputed on load and
// cannot be bypassed through storage; a reset clears the work; hints come one rung at a time; a
// prediction is committed before the lab answers it; a figure that runs the learner's own work
// waits for it to pass; a change runs only after a prediction, and its outcome waits for it; the
// questions are sorted before the lab places them. Each runs at desktop and phone widths.

import { expect, test, type Page } from "@playwright/test";

import { PLAN } from "@ms/content";

import { STRINGS } from "../../apps/course/src/strings";
import { testCount } from "@platform/lesson-schema";

import {
  CHAPTER,
  LESSONS,
  S,
  V,
  challenge,
  challengeData,
  choose,
  figureProps,
  format,
  openChapter,
  pass,
  runTests,
  status,
  storageKey,
} from "./helpers";

type Labelled = { id?: string; value?: string; label: string };

function watchConsole(page: Page): string[] {
  const errors: string[] = [];
  page.on("console", (m) => {
    if (m.type() === "error") errors.push(m.text());
  });
  page.on("pageerror", (e) => errors.push(e.message));
  return errors;
}

const pageWidth = (page: Page) =>
  page.evaluate(
    () => [document.documentElement.scrollWidth, document.documentElement.clientWidth] as const,
  );

test.describe("the chapter pages", () => {
  for (const lesson of LESSONS) {
    test(`${lesson.id} renders its ten sections and every figure, with no errors`, async ({
      page,
    }) => {
      const errors = watchConsole(page);
      await openChapter(page, lesson.id);
      const figures = lesson.sections.flatMap((s) => s.interactives);
      await expect(page.locator("figure.interactive")).toHaveCount(figures.length);
      await expect(page.locator(".interactive-problem, .interactive-missing")).toHaveCount(0);
      await expect(page.locator("section.challenge")).toHaveCount(lesson.challenges.length);
      const [scroll, client] = await pageWidth(page);
      expect(scroll).toBeLessThanOrEqual(client + 1);
      expect(errors).toEqual([]);
    });

    test(`${lesson.id} stays inside a phone's width after every figure has been used`, async ({
      page,
      isMobile,
    }) => {
      test.skip(!isMobile, "the phone's width is the one that overflows");
      test.setTimeout(240_000);
      await openChapter(page, lesson.id);
      // Pass every challenge first, so every figure that waits for one is open.
      for (const c of lesson.challenges) await pass(page, c.id, lesson);
      // Run every change, each after a prediction, so every outcome is shown at least once.
      const lab = page.locator("figure.interactive:has(.change-lab)");
      if (await lab.count()) {
        const changes = lab.locator(".fault-choices").getByRole("radio");
        for (let i = 1; i < (await changes.count()); i++) {
          await changes.nth(i).check();
          await lab.locator(".prediction-options").getByRole("radio").first().check();
          await lab.getByRole("button", { name: V.runWithChange }).click();
        }
      }
      const figures = page.locator("figure.interactive");
      for (let f = 0; f < (await figures.count()); f++) {
        const figure = figures.nth(f);
        await figure.scrollIntoViewIfNeeded();
        // Twice: some controls (a sort's weeks, a prediction's verdict) appear only after others.
        for (let pass = 0; pass < 2; pass++) {
          const radios = figure.getByRole("radio");
          for (let i = 0; i < (await radios.count()); i++) {
            const radio = radios.nth(i);
            if (await radio.isEnabled()) await radio.check({ timeout: 500 }).catch(() => {});
          }
          const selects = figure.locator("select");
          for (let i = 0; i < (await selects.count()); i++) {
            const options = await selects
              .nth(i)
              .locator("option")
              .evaluateAll((os) => os.map((o) => (o as HTMLOptionElement).value));
            for (const v of options) await selects.nth(i).selectOption(v);
          }
          const buttons = figure.locator("button:visible");
          for (let i = 0; i < (await buttons.count()) && i < 40; i++) {
            const b = buttons.nth(i);
            if (
              !(await b.isVisible().catch(() => false)) ||
              !(await b.isEnabled().catch(() => false))
            )
              continue;
            // Leave the work in place: a reset or "predict again" would undo what was shown.
            const name = (await b.textContent()) ?? "";
            if ([S.challenge.reset, STRINGS.startAgain].some((n) => name.startsWith(n))) continue;
            await b.click({ timeout: 500 }).catch(() => {});
          }
        }
      }
      const [scroll] = await pageWidth(page);
      expect(scroll).toBeLessThanOrEqual(page.viewportSize()!.width);
    });
  }

  test("the front page lists every chapter of the plan, with progress for the written ones", async ({
    page,
  }) => {
    await page.goto("#/");
    await expect(page.locator(".chapter-list li")).toHaveCount(PLAN.length);
    const link = page.locator(".chapter-list a.chapter-link", { hasText: CHAPTER.title });
    await expect(link).toBeVisible();
    await expect(link.locator(".meta")).toHaveText(
      `0 of ${CHAPTER.challenges.length} challenges complete`,
    );
    await expect(page.locator(".chapter-to-write")).toHaveCount(PLAN.length - LESSONS.length);
  });
});

test.describe("challenges", () => {
  for (const c of CHAPTER.challenges) {
    test(`${c.id} is completable with its reference through the page`, async ({ page }) => {
      await openChapter(page);
      const section = challenge(page, c.id);
      await section.scrollIntoViewIfNeeded();
      await expect(status(section)).toHaveText(S.challenge.notRun);
      await choose(section, c.reference.answers ?? {}, c.id);
      await runTests(section);
      await expect(status(section)).toHaveText(
        format(S.challenge.passing, { total: testCount(c) }),
      );
      await expect(section.locator(".challenge-complete")).toHaveText(S.challenge.complete);
    });

    test(`${c.id} refuses its starting point, naming what failed`, async ({ page }) => {
      await openChapter(page);
      const section = challenge(page, c.id);
      await runTests(section);
      await expect(status(section)).not.toHaveText(
        format(S.challenge.passing, { total: testCount(c) }),
      );
      await expect(section.locator(".verdict-failure").first()).toBeVisible();
      await expect(section.locator(".challenge-complete")).toHaveCount(0);
    });
  }

  test("a sum over the raw orders fails on the four days the prose names", async ({ page }) => {
    await openChapter(page);
    const section = challenge(page, "rebuild-daily-sales");
    await runTests(section);
    await expect(status(section)).toHaveText(format(S.challenge.failing, { passed: 3, total: 7 }));
    await expect(section.locator(".verdict-failure h4")).toHaveText([
      "Tuesday 8 September",
      "Wednesday 9 September",
      "Thursday 10 September",
      "Saturday 12 September",
    ]);
  });

  test("saved work is graded again on load; a saved mark alone earns nothing", async ({ page }) => {
    const c = challengeData("rebuild-daily-sales");
    await openChapter(page);
    const section = challenge(page, c.id);
    await choose(section, c.reference.answers ?? {}, c.id);
    await runTests(section);
    await expect(section.locator(".challenge-complete")).toBeVisible();

    await page.reload();
    await expect(page.locator("section.lesson-section")).toHaveCount(10);
    await expect(challenge(page, c.id).locator(".challenge-complete")).toBeVisible();

    // Tamper: keep the mark, break the work.
    await page.evaluate(
      ([key, id]) => {
        const stored = JSON.parse(localStorage.getItem(key) ?? "{}");
        stored.challenges[id].artifact = {
          answers: { source: "orders.parquet", keep: "all", measure: "revenue", per: "day" },
        };
        stored.challenges[id].firstPassedAt = "2020-01-01T00:00:00.000Z";
        localStorage.setItem(key, JSON.stringify(stored));
      },
      [storageKey(), c.id] as const,
    );
    await page.reload();
    await expect(page.locator("section.lesson-section")).toHaveCount(10);
    await expect(challenge(page, c.id).locator(".challenge-complete")).toHaveCount(0);
    await expect(status(challenge(page, c.id))).toHaveText(
      format(S.challenge.failing, { passed: 3, total: 7 }),
    );
    await page.goto("#/");
    await expect(
      page.locator(".chapter-list a.chapter-link", { hasText: CHAPTER.title }).locator(".meta"),
    ).toHaveText(`0 of ${CHAPTER.challenges.length} challenges complete`);
  });

  test("a reset clears the work in two steps", async ({ page }) => {
    const c = challengeData("clean-orders-rules");
    await openChapter(page);
    const section = challenge(page, c.id);
    await choose(section, c.reference.answers ?? {}, c.id);
    await runTests(section);
    await expect(section.locator(".challenge-complete")).toBeVisible();
    await section.getByRole("button", { name: new RegExp(`^${S.challenge.reset}`) }).click();
    await section.getByRole("button", { name: S.challenge.resetCancel }).click();
    await expect(section.locator(".challenge-complete")).toBeVisible();
    await section.getByRole("button", { name: new RegExp(`^${S.challenge.reset}`) }).click();
    await section.getByRole("button", { name: S.challenge.resetConfirm }).click();
    await expect(status(section)).toHaveText(S.challenge.resetDone);
    await expect(section.locator(".challenge-complete")).toHaveCount(0);
    await expect(section.getByLabel(c.fields[0]!.label, { exact: true })).toHaveValue(
      c.initial.answers?.["duplicates"] ?? "",
    );
    const stored = await page.evaluate((key) => localStorage.getItem(key), storageKey());
    expect(JSON.parse(stored ?? "{}").challenges?.[c.id]).toBeUndefined();
  });

  test("hints come one rung at a time and the ladder is remembered", async ({ page }) => {
    await openChapter(page);
    const section = challenge(page, "rebuild-daily-sales");
    await expect(section.locator(".hints-list li")).toHaveCount(0);
    await section.getByRole("button", { name: format(S.hints.show, { n: 1, total: 5 }) }).click();
    await expect(section.locator(".hints-list li")).toHaveCount(1);
    await section.getByRole("button", { name: format(S.hints.show, { n: 2, total: 5 }) }).click();
    await page.reload();
    await expect(challenge(page, "rebuild-daily-sales").locator(".hints-list li")).toHaveCount(2);
  });

  test("the builder shows the query as SQL and its result before the tests run", async ({
    page,
  }) => {
    await openChapter(page);
    const section = challenge(page, "rebuild-daily-sales");
    await expect(section.locator("pre.sql")).toContainText('FROM "orders.parquet"');
    await section
      .getByLabel(challengeData("rebuild-daily-sales").fields[0]!.label, { exact: true })
      .selectOption("customers.parquet");
    await expect(section.locator(".query-problem")).toContainText(
      "customers.parquet has no column called",
    );
  });
});

test.describe("the figures", () => {
  test("a prediction must be committed before the lab answers", async ({ page }) => {
    await openChapter(page);
    const figure = page.locator("#ix-predict-owner");
    const commit = figure.getByRole("button", { name: V.checkPrediction });
    await expect(commit).toBeDisabled();
    await expect(figure.locator("[role=status]")).toHaveCount(0);
    const options = figureProps("predict-owner")["options"] as Labelled[];
    await figure.getByLabel(options.find((o) => o.value === "account")!.label).check();
    await commit.click();
    await expect(figure.locator("[role=status]")).toContainText(V.match);
    await expect(figure).toContainText("etl_service");
    // A commitment stands: no "Predict again", the options locked, and the same after a reload.
    await expect(figure.getByRole("button")).toHaveCount(1); // the Lab badge alone
    await expect(figure.getByRole("radio").first()).toBeDisabled();
    await page.reload();
    await expect(page.locator("#ix-predict-owner [role=status]")).toContainText(V.match);
  });

  test("starting the chapter again clears every prediction and all work, after a second press", async ({
    page,
  }) => {
    await openChapter(page);
    const owner = page.locator("#ix-predict-owner");
    await owner.getByRole("radio").first().check();
    await owner.getByRole("button", { name: V.checkPrediction }).click();
    await pass(page, "rebuild-daily-sales");
    const again = page.getByRole("button", { name: STRINGS.startAgain });
    await again.click();
    await page.getByRole("button", { name: STRINGS.startAgainCancel }).click();
    await expect(owner.locator("[role=status]")).toHaveCount(1);
    await again.click();
    await page.getByRole("button", { name: STRINGS.startAgainConfirm }).click();
    await expect(page.locator(".start-again [role=status]")).toHaveText(STRINGS.startAgainDone);
    await expect(page.locator("#ix-predict-owner [role=status]")).toHaveCount(0);
    await expect(challenge(page, "rebuild-daily-sales").locator(".challenge-complete")).toHaveCount(
      0,
    );
    expect(await page.evaluate((key) => localStorage.getItem(key), storageKey())).toBeNull();
  });

  test("the inspector shows each asset's record, and the rows with no customer id", async ({
    page,
  }) => {
    await openChapter(page);
    const figure = page.locator("#ix-storage");
    await expect(figure.locator(".cell-null")).toHaveCount(3);
    await figure.getByRole("button", { name: "daily_sales" }).click();
    await expect(figure.locator(".record-table")).toContainText("etl_service");
    await expect(figure.locator(".data-table tbody tr")).toHaveCount(7);
  });

  test("the failure experiment waits for the learner's own query to pass", async ({ page }) => {
    const c = challengeData("rebuild-daily-sales");
    await openChapter(page);
    const figure = page.locator("#ix-changes");
    await expect(figure.locator(".figure-locked")).toHaveText(format(V.locked, { title: c.title }));
    await expect(figure.getByRole("radio")).toHaveCount(0);
    await pass(page, c.id);
    await expect(figure.locator(".figure-locked")).toHaveCount(0);
    await expect(figure.getByRole("radio")).not.toHaveCount(0);
  });

  test("a change runs only after a prediction; its outcome waits, and the closing words for all three", async ({
    page,
  }) => {
    await openChapter(page);
    await pass(page, "rebuild-daily-sales");
    const figure = page.locator("#ix-changes");
    const props = figureProps("changes");
    const changes = props["changes"] as Labelled[];
    const options = (props["prediction"] as { options: Labelled[] }).options;
    // How many queries rebuild daily_sales after each change: the copy makes two fit, the edit
    // leaves none, and the failed night leaves the one that rebuilds all six remaining rows, as
    // each outcome's text says.
    const answers: Record<string, string> = { copy: "twoOrMore", refunds: "none", failed: "one" };
    const fits: Record<string, number> = { copy: 2, refunds: 0, failed: 1 };
    for (const [i, change] of changes.entries()) {
      await figure.getByLabel(change.label, { exact: true }).check();
      const run = figure.getByRole("button", { name: V.runWithChange });
      await expect(run).toBeDisabled();
      await expect(figure.locator(".change-outcome")).toHaveCount(0);
      const answer = options.find((o) => o.value === answers[change.id!])!;
      await figure.getByLabel(answer.label, { exact: true }).check();
      await run.click();
      await expect(figure.locator("[role=status]")).toContainText(V.match);
      await expect(figure.locator(".change-outcome")).toBeVisible();
      await expect(figure.locator(".change-fits li")).toHaveCount(fits[change.id!]!);
      if (fits[change.id!] === 0) await expect(figure).toContainText(V.fitsNone);
      if (i < changes.length - 1) await expect(figure.locator(".change-after-all")).toHaveCount(0);
    }
    await expect(figure.locator(".change-after-all")).toBeVisible();
    // A prediction is kept: back on the first change, its result is still there.
    await figure.getByLabel(changes[0]!.label, { exact: true }).check();
    await expect(figure.locator(".change-fits li")).toHaveCount(2);
  });

  test("the questions are sorted before the lab places them, and they move with the week", async ({
    page,
  }) => {
    await openChapter(page);
    const figure = page.locator("#ix-map");
    const check = figure.getByRole("button", { name: V.checkSort });
    await expect(check).toBeDisabled();
    await expect(figure.locator(".question-map")).toHaveCount(0);
    const selects = figure.locator("select");
    for (let i = 0; i < (await selects.count()); i++)
      await selects.nth(i).selectOption("suggested");
    await check.click();
    await expect(figure.locator("[role=status]")).toHaveText(
      format(V.sortScore, { matching: 4, total: 8 }),
    );
    const record = figure.locator(".map-record");
    await expect(record).not.toContainText(V.q["made-from"]!);
    const weeks = figureProps("map")["weeks"] as Labelled[];
    await figure.getByLabel(weeks.find((w) => w.id === "refunds")!.label, { exact: true }).check();
    await expect(record).toContainText(V.q["made-from"]!);
    await expect(record).toContainText(format(V.movedFrom, { place: V.place["suggested"]! }));
    await page.reload();
    await expect(page.locator("#ix-map [role=status]")).toHaveText(
      format(V.sortScore, { matching: 4, total: 8 }),
    );
  });

  test("the rules prediction waits for the learner's rules to pass, then the lab answers it", async ({
    page,
  }) => {
    const c = challengeData("clean-orders-rules");
    await openChapter(page);
    const figure = page.locator("#ix-predict-rules");
    await expect(figure.locator(".figure-locked")).toHaveText(format(V.locked, { title: c.title }));
    await pass(page, c.id);
    const options = figureProps("predict-rules")["options"] as Labelled[];
    await figure.getByLabel(options.find((o) => o.value === "two")!.label, { exact: true }).check();
    await figure.getByRole("button", { name: V.checkPrediction }).click();
    await expect(figure.locator("[role=status]")).toContainText(V.match);
  });
});
