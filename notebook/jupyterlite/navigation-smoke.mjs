// Copyright © 2026 Christopher Snow

// Run against a built site served at the supplied URL. Chapter changes must preserve the
// worker, isolate Python variables, retain drafts/answers and support browser history.
import assert from "node:assert/strict";
import { chromium } from "playwright";
import { pathToFileURL } from "node:url";
import { resolve } from "node:path";
export async function checkNavigation(browser, base) {
  const page = await browser.newPage({ viewport: { width: 390, height: 844 } });
  try {
    const errors = [];
    page.on("pageerror", (error) => errors.push(error.message));
    let workers = 0;
    page.on("worker", () => workers++);
    const ready = () =>
      page.waitForSelector('.ms-Startup[data-phase="ready"],.ms-Startup[data-phase="hidden"]', {
        state: "attached",
        timeout: 120000,
      });
    const run = async (example) => {
      await example.getByRole("button", { name: "Run", exact: true }).click();
      await example.getByText("Example finished.", { exact: true }).waitFor({ timeout: 120000 });
    };
    await page.goto(`${base}/notebooks/index.html?path=chapter_01.ipynb`);
    await ready();
    console.log("ready: chapter 1");
    const originalWorkers = workers;
    assert.equal(originalWorkers, 1);
    const first = page.locator('.ms-Example[data-example="products"]');
    const draft = 'course_navigation_marker = 123\nprint("Chapter one draft")';
    await first.locator(".cm-content").fill(draft);
    await run(first);
    await page
      .locator('textarea[data-answer="ch01.daily_sales"]')
      .fill("My saved Chapter 1 answer");
    const documentMarker = await page.evaluate(() => (window.navigationTestMarker = Math.random()));
    await page.locator(".ms-Buttons-next").click();
    await page.waitForURL(/path=chapter_02.ipynb/);
    await ready();
    console.log("ready: chapter 2");
    assert.equal(workers, originalWorkers);
    assert.equal(await page.evaluate(() => window.navigationTestMarker), documentMarker);
    await page.waitForSelector('textarea[data-answer="ch01.daily_sales"]', { state: "attached" });
    assert.equal(
      await page.locator('textarea[data-answer="ch01.daily_sales"]').inputValue(),
      "My saved Chapter 1 answer",
    );
    const second = page.locator(".ms-Example").first();
    await second.locator(".cm-content").fill('print("course_navigation_marker" in globals())');
    await run(second);
    assert.match(await second.innerText(), /False/);
    await second.getByRole("button", { name: "Reset example", exact: true }).click();
    await page.getByRole("button", { name: "Run all", exact: true }).click();
    await page
      .getByText("All examples finished successfully.", { exact: true })
      .waitFor({ timeout: 120000 });
    console.log("executed: chapter 2");
    await page.goBack();
    await page.waitForSelector('.ms-Example[data-example="products"]', { timeout: 120000 });
    await ready();
    assert.equal(
      await page.locator('.ms-Example[data-example="products"] .cm-content').innerText(),
      draft,
    );
    assert.equal(
      await page.locator('textarea[data-answer="ch01.daily_sales"]').inputValue(),
      "My saved Chapter 1 answer",
    );
    console.log("restored: chapter 1");
    await page.locator(".ms-Buttons-contents").click();
    const dialog = page.getByRole("dialog", { name: "Contents", exact: true });
    await dialog.locator('a[href$="path=chapter_03.ipynb"]').click();
    await page.waitForURL(/path=chapter_03.ipynb/);
    await ready();
    await page.getByRole("button", { name: "Run all", exact: true }).click();
    await page
      .getByText("All examples finished successfully.", { exact: true })
      .waitFor({ timeout: 120000 });
    await page.locator('.jp-RenderedMarkdown a[href*="chapter_04.ipynb"]').first().click();
    await page.waitForURL(/path=chapter_04.ipynb/);
    await ready();
    assert.equal(
      await page.locator("body").evaluate((node) => node.classList.contains("ms-Reading")),
      true,
    );
    assert.equal(
      await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth),
      true,
    );
    assert.equal(workers, originalWorkers);
    assert.deepEqual(errors, []);
    assert.equal(await page.locator(".ms-Startup").count(), 1);
    console.log(
      "ok navigation: one Python worker across chapters, fresh variables, retained drafts/answers, Run all, Contents and Back",
    );
  } finally {
    await page.close();
  }
}

if (process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href) {
  const browser = await chromium.launch();
  try {
    await checkNavigation(browser, process.argv[2]);
  } finally {
    await browser.close();
  }
}
