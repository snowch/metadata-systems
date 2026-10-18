// Copyright © 2026 Christopher Snow

import { readFileSync } from "node:fs";
const words = JSON.parse(readFileSync(new URL("../buttons/status.json", import.meta.url), "utf8"));

// Real worker downloads are delayed or corrupted, rather than replacing the startup controller.
// Each scenario gets a fresh browser cache and storage. Page clocks shorten the two-minute wait.
export async function checkStartup(browser, base, check) {
  const open = async (context) => {
    const page = await context.newPage();
    await page.clock.install();
    await page.goto(`${base}/notebooks/index.html?path=chapter_01.ipynb`);
    await page.waitForSelector('.ms-Startup[data-phase="loading"]', { timeout: 120_000 });
    return page;
  };
  const find = async (page, selector) => {
    for (let n = 0; n < 3; n++) {
      const found = await page.evaluate(async (selector) => {
        const outer = document.querySelector(".jp-WindowedPanel-outer");
        for (let y = 0; y <= outer.scrollHeight; y += 400) {
          outer.scrollTop = y;
          await new Promise((resolve) => setTimeout(resolve, 60));
          const nodes = [...document.querySelectorAll(selector)];
          if (nodes.some((node) => node.getBoundingClientRect().height > 0)) return true;
        }
        return false;
      }, selector);
      if (found) return page.locator(`${selector}:visible`).first();
    }
    throw Error(`Missing field during Python startup: ${selector}`);
  };
  const ready = (page) =>
    page.waitForFunction(
      () => ["ready", "hidden"].includes(document.querySelector(".ms-Startup")?.dataset.phase),
      null,
      { timeout: 120_000 },
    );

  const slow = await browser.newContext({
    viewport: { width: 360, height: 800 },
    colorScheme: "dark",
    reducedMotion: "reduce",
    serviceWorkers: "block",
  });
  let release;
  const gate = new Promise((resolve) => (release = resolve));
  let downloads = 0;
  await slow.route("**/pyodide.asm.wasm", async (route) => {
    downloads++;
    if (downloads === 1) {
      await gate;
      await route.abort().catch(() => {});
    } else await route.continue();
  });
  try {
    const page = await open(slow);
    await page.waitForFunction(() => document.querySelector(".jp-MarkdownOutput h1"));
    await page.clock.fastForward(10_001);
    await page.getByText(words.slow, { exact: true }).waitFor();
    check(
      (await page.locator(".ms-Startup-busy").count()) === 1,
      "startup: a delayed download shows an indeterminate indicator and slow-connection guidance",
    );
    const answer = 'textarea[data-answer="ch01.daily_sales"]';
    await (await find(page, answer)).fill("My answer while Python downloads");
    const editor = await find(page, '.jp-CodeCell .cm-content[contenteditable="true"]');
    await editor.fill("# Unsaved edit retained through retry\n1 + 1");
    await page.evaluate(() => {
      window.startupPageMarker = "same page";
    });
    await page.click('button[data-action="runAll"]');
    check(
      await page.locator('button[data-action="runAll"]').isDisabled(),
      "startup: Run all waits for Python while Save remains available",
    );
    check(
      await page.locator('button[data-action="save"]').isEnabled(),
      "startup: notebook edits can be saved during loading",
    );
    await page.clock.fastForward(120_001);
    const retry = page.locator(".ms-Startup-retry");
    await retry.waitFor();
    check(
      await page.evaluate(() => {
        const banner = document.querySelector(".ms-Startup");
        const notebook = document.querySelector(".jp-Notebook");
        const button = banner.querySelector("button");
        return (
          banner.scrollWidth <= banner.clientWidth &&
          button.getBoundingClientRect().height >= 44 &&
          banner.getBoundingClientRect().bottom <= notebook.getBoundingClientRect().top + 1 &&
          banner.querySelector('[role="status"]').getAttribute("aria-live") === "polite" &&
          getComputedStyle(banner.querySelector('[role="status"] > div'), "::before")
            .animationName === "none"
        );
      }),
      "startup: status and retry fit a dark phone view, respect reduced motion, and leave the chapter uncovered",
    );
    await retry.click();
    release();
    await ready(page);
    check(
      await page.evaluate(() => window.startupPageMarker === "same page"),
      "startup: retry starts Python without reloading the page",
    );
    check(
      (await (await find(page, answer)).inputValue()) === "My answer while Python downloads",
      "startup: retry preserves answers written during the download",
    );
    check(
      (
        await (await find(page, '.jp-CodeCell .cm-content[contenteditable="true"]')).innerText()
      ).includes("Unsaved edit retained through retry"),
      "startup: retry preserves unsaved notebook edits",
    );
    check(downloads >= 2, "startup: retry requests Python again after a stalled download");
    await page.click('button[data-action="runAll"]');
    await page.waitForFunction(
      () => !document.querySelector('button[data-action="runAll"]:disabled'),
      null,
      { timeout: 120_000 },
    );
    check(
      (await page.locator(".ms-Status").textContent()) === words.done,
      "startup: Run all succeeds after retry",
    );
  } finally {
    release();
    await slow.close();
  }

  const failed = await browser.newContext({
    viewport: { width: 1280, height: 900 },
    serviceWorkers: "block",
  });
  let broken = true;
  let intercepted = 0;
  await failed.route("**/shop-0.0.0-py3-none-any.whl*", (route) => {
    intercepted++;
    return broken
      ? route.fulfill({
          status: 200,
          contentType: "application/zip",
          body: "invalid wheel for startup failure test",
        })
      : route.continue();
  });
  try {
    const page = await open(failed);
    await page.click('button[data-action="runAll"]');
    await page
      .waitForSelector('.ms-Startup[data-phase="failed"]', { timeout: 120_000 })
      .catch(async (error) => {
        console.log("startup failure diagnostic", {
          intercepted,
          status: await page.locator(".ms-Startup").textContent(),
        });
        throw error;
      });
    check(intercepted > 0, "startup: the failed package download was intercepted");
    check(
      (await page.locator(".ms-Startup").innerText()).includes(words.failed),
      "startup: a failed chapter setup displays a clear error and Retry",
    );
    await page.waitForFunction(
      () => !document.querySelector('button[data-action="runAll"]:disabled'),
    );
    check(
      (await page.locator(".ms-Startup-busy").count()) === 0,
      "startup: failure stops the spinner and releases a queued run",
    );
    broken = false;
    await page.locator(".ms-Startup-retry").click();
    await ready(page);
    check(
      await page.locator(".ms-Startup-retry").isHidden(),
      "startup: a successful retry clears the error and retry control",
    );
  } finally {
    await failed.close();
  }
}
