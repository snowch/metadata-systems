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

/** Commits the Thursday prediction, which the investigation's decisions wait for. */
async function commitThursday(page: Page): Promise<void> {
  const figure = page.locator("#ix-predict-days");
  await figure.getByRole("radio").first().check();
  await figure.getByRole("button", { name: V.checkPrediction }).click();
}

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
  test("a requirement is questioned before the warehouse answers, and no reading is called wrong", async ({
    page,
  }) => {
    await openChapter(page);
    const figure = page.locator("#ix-predict-owner");
    const props = figureProps("predict-owner");
    const options = props["options"] as (Labelled & { short: string })[];
    const buttons = props["buttons"] as { choose: string; show: string };
    const text = props["text"] as { mine: string };
    // A choice is not a prediction, and its button does not say so.
    await expect(figure.getByRole("button", { name: V.checkPrediction })).toHaveCount(0);
    const choose = figure.getByRole("button", { name: buttons.choose });
    await expect(choose).toBeDisabled();
    await expect(figure.locator("[role=status]")).toHaveCount(0);
    await expect(figure.locator("table")).toHaveCount(0);
    // A team: what many would store, and not what this shop's warehouse holds.
    const team = options.find((o) => o.value === "team")!;
    await figure.getByLabel(team.label).check();
    await choose.click();
    await expect(figure.locator("[role=status]")).toHaveText(
      format(text.mine, { choice: team.label }),
    );
    // What the requirement could mean, the learner's own reading marked, before the warehouse.
    await expect(figure.locator("tbody tr")).toHaveCount(options.length);
    await expect(figure.locator("tr.is-chosen")).toContainText(team.short);
    await expect(figure).not.toContainText("etl_service");
    await figure.getByRole("button", { name: buttons.show }).click();
    await expect(figure.locator("[role=status]").last()).toContainText("etl_service");
    const answers = figure.locator("tbody tr td:last-child");
    await expect(answers).toHaveText([V.no, V.no, V.no, V.yes]);
    await expect(figure).not.toContainText(V.match);
    await expect(figure).not.toContainText(V.noMatch);
    // Both presses stand: the options locked, no button but the badge, the same after a reload.
    await expect(figure.getByRole("button")).toHaveCount(1);
    await expect(figure.getByRole("radio").first()).toBeDisabled();
    await page.reload();
    await expect(page.locator("#ix-predict-owner tbody tr td:last-child")).toHaveText([
      V.no,
      V.no,
      V.no,
      V.yes,
    ]);
  });

  test("a prediction must be committed before the lab answers, and says whether it was right", async ({
    page,
  }) => {
    await openChapter(page);
    const figure = page.locator("#ix-predict-days");
    const commit = figure.getByRole("button", { name: V.checkPrediction });
    await expect(commit).toBeDisabled();
    await expect(figure.locator("[role=status]")).toHaveCount(0);
    const options = figureProps("predict-days")["options"] as Labelled[];
    await figure.getByLabel(options.find((o) => o.value === "same")!.label).check();
    await commit.click();
    await expect(figure.locator("[role=status]")).toContainText(V.noMatch);
    await page.reload();
    await expect(page.locator("#ix-predict-days [role=status]")).toContainText(V.noMatch);
  });

  test("the Thursday prediction is answered by the raw orders against daily_sales", async ({
    page,
  }) => {
    await openChapter(page);
    const figure = page.locator("#ix-predict-days");
    const options = figureProps("predict-days")["options"] as Labelled[];
    await figure.getByLabel(options.find((o) => o.value === "different")!.label).check();
    await figure.getByRole("button", { name: V.checkPrediction }).click();
    await expect(figure.locator("[role=status]")).toContainText(V.match);
    await expect(figure.locator(".days-table tbody tr")).toHaveCount(7);
    await expect(figure).toContainText("205.50");
  });

  test('"I can\'t tell yet" is answered by the lab and marked neither right nor wrong', async ({
    page,
  }) => {
    await openChapter(page);
    const figure = page.locator("#ix-predict-days");
    const props = figureProps("predict-days");
    const undecided = props["undecided"] as Labelled & { line: string };
    const options = props["options"] as Labelled[];
    await figure.getByLabel(undecided.label).check();
    await figure.getByRole("button", { name: V.checkPrediction }).click();
    const status = figure.locator("[role=status]");
    await expect(status).toHaveText(
      format(undecided.line, { answer: options.find((o) => o.value === "different")!.label }),
    );
    await expect(status).not.toContainText(V.match);
    await expect(status).not.toContainText(V.noMatch);
    await expect(figure).toContainText("205.50");
  });

  test("every figure's badge says what it asks of the learner, and opens that role's line alone", async ({
    page,
  }) => {
    await openChapter(page);
    for (const x of CHAPTER.sections.flatMap((s) => s.interactives)) {
      const figure = page.locator(`#ix-${x.id}`);
      await expect(figure).toHaveAttribute("data-role", x.role ?? "");
      await expect(figure.locator("figcaption .badge")).toHaveText(V.roles[x.role ?? ""] ?? "");
    }
    const storage = page.locator("#ix-storage");
    await storage
      .getByRole("button", { name: format(V.roleBadgeLabel, { role: V.roles["inspect"] ?? "" }) })
      .click();
    await expect(storage.locator(".time-model-note")).toBeVisible();
    await expect(storage.locator(".time-model-note")).toHaveText(V.roleNotes["inspect"] ?? "");
    // The lab is explained once, where the chapter first names it: behind no badge, and not
    // again at the foot. A reference's badge opens nothing.
    await expect(page.locator(".time-model-note", { hasText: "Metadata Lab" })).toHaveCount(0);
    await expect(page.locator(".lesson-model-note")).toHaveCount(0);
    await expect(page.locator("#ix-platform .time-model-toggle")).toHaveCount(0);
  });

  test("every figure that runs the lab carries the lab's mark, named as the opening names it", async ({
    page,
  }) => {
    await openChapter(page);
    const marks = await page
      .locator('figure.interactive[data-time-model="lab"]')
      .evaluateAll((fs) =>
        fs.map((f) => {
          const caption = f.querySelector("figcaption")!;
          const flask = getComputedStyle(caption, "::before");
          return {
            name: getComputedStyle(caption, "::after").content,
            flask: flask.maskImage || flask.webkitMaskImage,
            width: flask.width,
          };
        }),
      );
    const figures = CHAPTER.sections.flatMap((s) => s.interactives);
    expect(marks).toHaveLength(figures.length);
    for (const m of marks) {
      expect(m.name).toContain("Metadata Lab");
      expect(m.flask).toMatch(/^url\(/);
      expect(m.width).toBe("15px");
    }
    // The name is the one the opening explains, where the chapter first names the lab.
    expect(CHAPTER.sections[0]!.prose).toContain("Metadata Lab");
  });

  test("the opening keeps how the lab runs behind a control, then shows the map, the week and the question", async ({
    page,
  }) => {
    await openChapter(page);
    const opening = page.locator('section.lesson-section[data-kind="question"]');
    const details = opening.locator("details.lesson-details");
    await expect(details).toHaveCount(1);
    const body = details.locator(".prose");
    await expect(body).toBeHidden();
    await details.locator("summary").click();
    await expect(body).toBeVisible();
    await expect(body).toContainText("query engine");
    await details.locator("summary").click();
    await expect(body).toBeHidden();
    expect(
      await opening.locator("figure.interactive").evaluateAll((fs) => fs.map((f) => f.id)),
    ).toEqual(["ix-platform", "ix-week", "ix-dashboard"]);
    // The week keeps every name whole and inside its figure, with a bar for every night.
    const week = page.locator("#ix-week");
    await expect(week.locator(".week-night")).toHaveCount(7);
    const problems = await week.evaluate((f) => {
      const box = f.getBoundingClientRect();
      const out: string[] = [];
      for (const e of f.querySelectorAll<HTMLElement>(
        ".week-day, .week-night, .week-start, .week-start-label, .week-key li",
      )) {
        const r = e.getBoundingClientRect();
        if (r.left < box.left - 0.5 || r.right > box.right + 0.5)
          out.push(`${e.className} ${e.textContent} leaves the figure`);
        if (e.scrollWidth > e.clientWidth + 1) out.push(`${e.textContent} is cut`);
      }
      const days = [...f.querySelectorAll(".week-day")].map((d) => d.getBoundingClientRect());
      days.forEach((d, i) => {
        const next = days[i + 1];
        if (next && d.right > next.left + 0.5) out.push(`day ${i} runs into the next`);
      });
      return out;
    });
    expect(problems).toEqual([]);
  });

  test("the investigation starts where the learner chooses to look, and the inspector opens there", async ({
    page,
  }) => {
    await openChapter(page);
    const decide = page.locator("#ix-where-first");
    const props = figureProps("where-first");
    const dashboard = (props["options"] as Labelled[]).find((o) => o.value === "dashboard")!;
    const opened = page.locator("#ix-storage .asset-button[aria-pressed=true]");
    await expect(opened).toHaveText("orders.parquet");
    // It states what the Thursday prediction found, so it waits for that answer.
    await expect(decide.locator(".figure-locked")).toBeVisible();
    await expect(decide).not.toContainText("205.50");
    await commitThursday(page);
    await decide.getByLabel(dashboard.label).check();
    await decide.getByRole("button", { name: props["commit"] as string }).click();
    await expect(decide.locator("[role=status]")).toHaveText(
      format(props["mine"] as string, { choice: dashboard.label }),
    );
    await expect(decide).not.toContainText("154.00");
    await expect(opened).toHaveText("sales_dashboard");
    await page.reload();
    await expect(page.locator("#ix-storage .asset-button[aria-pressed=true]")).toHaveText(
      "sales_dashboard",
    );
  });

  test("an explanation for Thursday is chosen, tested by the learner, and checked after the rebuild", async ({
    page,
  }) => {
    await openChapter(page);
    await commitThursday(page);
    const where = page.locator("#ix-where-first");
    await where.getByRole("radio").first().check();
    await where
      .getByRole("button", { name: figureProps("where-first")["commit"] as string })
      .click();
    const choose = page.locator("#ix-why-thursday");
    const props = figureProps("why-thursday");
    const options = props["options"] as Labelled[];
    const moved = options.find((o) => o.value === "moved")!.label;
    await choose.getByLabel(moved).check();
    await choose.getByRole("button", { name: props["commit"] as string }).click();
    await expect(choose.locator("[role=status]")).toHaveText(
      format(props["mine"] as string, { choice: moved }),
    );
    await expect(choose).not.toContainText("154.00");
    // The rows are read only after the learner's own query rebuilds daily_sales.
    const check = page.locator("#ix-why-thursday-check");
    await expect(check.locator(".figure-locked")).toHaveText(
      format(V.locked, { title: challengeData("rebuild-daily-sales").title }),
    );
    await pass(page, "rebuild-daily-sales");
    await check
      .getByRole("button", { name: figureProps("why-thursday-check")["button"] as string })
      .click();
    await expect(check.locator("tbody tr td:last-child")).toHaveText([V.yes, V.no, V.no]);
    await expect(check.locator("tr.is-chosen")).toContainText(moved);
    await expect(check.locator("[role=status]")).toContainText("154.00");
    await page.reload();
    await expect(page.locator("#ix-why-thursday-check tbody tr td:last-child")).toHaveText([
      V.yes,
      V.no,
      V.no,
    ]);
  });

  test("nothing the learner does leaves the browser: the page asks only for the course's files", async ({
    page,
    baseURL,
  }) => {
    // The opening says so: the lab runs in the page and the learner's work stays in the browser.
    const sent: string[] = [];
    page.on("request", (r) => {
      if (r.method() !== "GET" || !r.url().startsWith(baseURL ?? ""))
        sent.push(`${r.method()} ${r.url()}`);
    });
    await openChapter(page);
    await commitThursday(page);
    const where = page.locator("#ix-where-first");
    await where.getByRole("radio").first().check();
    await where
      .getByRole("button", { name: figureProps("where-first")["commit"] as string })
      .click();
    await page.locator("#ix-storage").getByRole("button", { name: "daily_sales" }).click();
    await pass(page, "rebuild-daily-sales");
    await page.reload();
    await expect(page.locator("section.lesson-section")).toHaveCount(10);
    expect(sent).toEqual([]);
  });

  test("the map stays to hand: a button opens it once its place is scrolled past", async ({
    page,
  }) => {
    await openChapter(page);
    const map = page.locator("#ix-platform .platform-map");
    await expect(map.locator(".map-asset")).toHaveCount(7);
    await expect(map.locator(".map-system-name")).toHaveText(
      ["object-storage", "warehouse", "reporting"].map((s) => V.systems[s]!),
    );
    const open = page.getByRole("button", { name: V.mapOpen });
    // Before the learner reaches the map, and while it is in view, there is no button.
    await expect(open).toHaveCount(0);
    await map.scrollIntoViewIfNeeded();
    await expect(open).toHaveCount(0);
    // Past it, the button opens the same map over the page, and Escape closes it again.
    await challenge(page, "rebuild-daily-sales").scrollIntoViewIfNeeded();
    await expect(open).toBeVisible();
    await expect(open).toHaveAttribute("aria-expanded", "false");
    await open.click();
    const panel = page.locator("#map-dock-panel");
    await expect(panel.locator(".map-asset")).toHaveCount(7);
    await expect(page.getByRole("button", { name: V.mapClose })).toBeFocused();
    await page.keyboard.press("Escape");
    await expect(panel).toHaveCount(0);
    await expect(open).toBeFocused();
    await open.click();
    await page.getByRole("button", { name: V.mapClose }).click();
    await expect(panel).toHaveCount(0);
    // Back at the map, the button goes.
    await map.scrollIntoViewIfNeeded();
    await expect(open).toHaveCount(0);
    // A jump from above the map to far below it, which never shows it, still brings the button.
    await page.evaluate(() => window.scrollTo(0, 0));
    await page.reload();
    await expect(page.locator("section.lesson-section")).toHaveCount(10);
    await page.locator("#ix-predict-rules").scrollIntoViewIfNeeded();
    await expect(open).toBeVisible();
    const [scroll, client] = await pageWidth(page);
    expect(scroll).toBeLessThanOrEqual(client + 1);
  });

  test("starting the chapter again clears every prediction and all work, after a second press", async ({
    page,
  }) => {
    await openChapter(page);
    const owner = page.locator("#ix-predict-owner");
    await owner.getByRole("radio").first().check();
    const buttons = figureProps("predict-owner")["buttons"] as { choose: string };
    await owner.getByRole("button", { name: buttons.choose }).click();
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
    // More than one setting passes: the quantity rule decides no row this week.
    await figure
      .getByLabel(options.find((o) => o.value === "more")!.label, { exact: true })
      .check();
    await figure.getByRole("button", { name: V.checkPrediction }).click();
    await expect(figure.locator("[role=status]")).toContainText(V.match);
  });
});
