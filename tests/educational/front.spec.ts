// Copyright © 2026 Christopher Snow

// The front page, driven in a browser at desktop and phone widths: it lists every chapter of the
// plan by part, a written chapter's title opens its notebook, the band starts Chapter 1 and shows
// the shop's dashboard, a former chapter address leads to its notebook, and the page logs no error
// and never scrolls sideways.

import { readFileSync } from "node:fs";

import { expect, test, type Page } from "@playwright/test";

import { CHAPTER_PAGES, NOTEBOOKS, PARTS, PLAN } from "@ms/content";

import { STRINGS } from "../../apps/course/src/strings";

const NOTEBOOK = "/metadata-systems/jupyterlite/notebooks/index.html?path=";
const data = JSON.parse(readFileSync("apps/course/src/dashboard.json", "utf8")) as {
  values: { shown: string }[];
};

function watchConsole(page: Page): string[] {
  const errors: string[] = [];
  page.on("console", (m) => {
    if (m.type() === "error") errors.push(m.text());
  });
  page.on("pageerror", (e) => errors.push(e.message));
  return errors;
}

test("the front page lists every chapter, and a written chapter's title opens its notebook", async ({
  page,
}) => {
  const errors = watchConsole(page);
  await page.goto("#/");
  await expect(page.locator(".chapter-list > li")).toHaveCount(PLAN.length);
  await expect(page.locator(".chapter-to-write")).toHaveCount(PLAN.length - NOTEBOOKS.size);
  for (const [number, file] of NOTEBOOKS) {
    const title = PLAN.find((c) => c.number === number)!.title;
    const link = page.locator("a.chapter-link", { hasText: `${number}. ${title}` });
    await expect(link).toHaveAttribute("href", `${NOTEBOOK}${file}`);
  }
  await expect(page.locator(".contents-note")).toHaveText(STRINGS.contentsNote);
  await expect(page.locator(".hero-start")).toHaveAttribute(
    "href",
    `${NOTEBOOK}${NOTEBOOKS.get(1)}`,
  );
  // The band shows the shop's dashboard, from the engine's values, with no control in it; the
  // contents follow by part, the first part open.
  const hero = page.locator("#ix-cover-dashboard");
  await expect(hero.locator(".bars li")).toHaveCount(data.values.length);
  await expect(hero.locator(".bar-value").nth(3)).toHaveText(data.values[3]!.shown);
  expect(await hero.locator("button, input, select").count()).toBe(0);
  const parts = page.locator("details.part");
  await expect(parts).toHaveCount(PARTS.length);
  await expect(parts.first()).toHaveAttribute("open", "");
  const [scroll, width] = await page.evaluate(
    () => [document.documentElement.scrollWidth, document.documentElement.clientWidth] as const,
  );
  expect(scroll).toBeLessThanOrEqual(width);
  expect(errors).toEqual([]);
});

for (const [id, chapter] of CHAPTER_PAGES)
  test(`a former chapter address, #/chapter/${id}, leads to the chapter's notebook`, async ({
    page,
  }) => {
    await page.goto(`#/chapter/${id}`);
    await page.waitForURL((u) => u.href.includes(`path=${NOTEBOOKS.get(chapter)}`));
  });

test("an address the course does not have says so", async ({ page }) => {
  await page.goto("#/nowhere");
  await expect(page.locator("main h1")).toContainText("/nowhere");
});

test("the skip link stays off the page until the keyboard reaches it", async ({ page }) => {
  await page.goto("");
  const skip = page.locator("a.skip-link");
  await expect(skip).not.toBeInViewport();
  await page.keyboard.press("Tab");
  await expect(skip).toBeFocused();
  await expect(skip).toBeInViewport();
});
