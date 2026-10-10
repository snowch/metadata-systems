// Copyright © 2026 Christopher Snow

// The educational tests: every chapter renders whole; every challenge is completable through the
// page with its reference and refuses a wrong attempt; completion is recomputed on load and
// cannot be bypassed through storage; a reset clears the work; hints come one rung at a time; a
// prediction is committed before the lab answers it; a figure that runs the learner's own work
// waits for it to pass; a change runs only after a prediction, and its outcome waits for it; the
// questions are sorted before the lab places them. Each runs at desktop and phone widths.

import { expect, test, type Page } from "@playwright/test";

import { PARTS, PLAN } from "@ms/content";

import { STRINGS } from "../../apps/course/src/strings";

import { CHAPTER, LESSONS, S, V, openChapter, pass } from "./helpers";

/** Commits the Thursday prediction, which the investigation's decisions wait for. */

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
    // A chapter with challenges shows its progress; one without says so.
    await expect(link.locator(".meta")).toHaveText(
      CHAPTER.challenges.length > 0
        ? `0 of ${CHAPTER.challenges.length} challenges complete`
        : STRINGS.noChallenges,
    );
    await expect(page.locator(".chapter-to-write")).toHaveCount(PLAN.length - LESSONS.length);
    // The band shows the question the course starts from: Chapter 1's dashboard, computed from
    // the shop's data, with no badge and no control; then the contents by part, the part of the
    // chapter the button names open and the rest closed.
    const hero = page.locator("#ix-cover-dashboard");
    await expect(hero).toHaveAttribute("data-time-model", "none");
    await expect(hero.locator(".badge")).toHaveCount(0);
    await expect(hero.locator(".bars li")).toHaveCount(7);
    expect(await hero.locator("button, input, select").count()).toBe(0);
    const parts = page.locator("details.part");
    await expect(parts).toHaveCount(PARTS.length);
    expect(await parts.evaluateAll((ds) => ds.map((d) => (d as HTMLDetailsElement).open))).toEqual(
      PARTS.map((_, i) => i === 0),
    );
    await parts.nth(1).locator("summary").click();
    await expect(parts.nth(1).locator(".chapter-to-write").first()).toBeVisible();
  });
});
