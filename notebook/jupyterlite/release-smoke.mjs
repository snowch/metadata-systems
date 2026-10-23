// Copyright © 2026 Christopher Snow

import assert from "node:assert/strict";

export async function checkRelease(browser, base) {
  const context = await browser.newContext({
    serviceWorkers: "block",
    viewport: { width: 360, height: 800 },
  });
  try {
    const page = await context.newPage();
    let deployed = (await (await fetch(`${base}/release.json`)).json()).commit;
    let fail = false;
    await context.route("**/release.json", (route) => {
      assert.equal(route.request().headers()["x-ms-offline-download"], "release-check");
      return fail
        ? route.abort("internetdisconnected")
        : route.fulfill({ json: { commit: deployed } });
    });
    await page.goto(`${base}/notebooks/index.html?path=chapter_01.ipynb`);
    const badge = page.locator(".ms-Release");
    await page.locator('.ms-Release[data-state="latest"]').waitFor({ timeout: 120000 });
    assert.match(await badge.innerText(), new RegExp(`${deployed.slice(0, 7)} ✓`));
    assert.equal(
      await badge.locator("a").getAttribute("href"),
      `https://github.com/snowch/metadata-systems/commit/${deployed}`,
    );
    // The extension's stylesheet and Lumino layout can settle after the network check.
    await page.waitForFunction(() => {
      const node = document.querySelector(".ms-Release");
      const bounds = node.getBoundingClientRect();
      const link = node.querySelector("a").getBoundingClientRect();
      return bounds.height >= 24 && link.top >= bounds.top && link.bottom <= bounds.bottom;
    });
    const loaded = deployed;
    deployed = "a".repeat(40) === loaded ? "b".repeat(40) : "a".repeat(40);
    await page.evaluate(() => window.dispatchEvent(new Event("focus")));
    await page.locator('.ms-Release[data-state="updateAvailable"]').waitFor();
    assert.match(await badge.innerText(), new RegExp(`${loaded.slice(0, 7)} ✗`));
    fail = true;
    await page.evaluate(() => window.dispatchEvent(new Event("offline")));
    await page.locator('.ms-Release[data-state="cannotCheck"]').waitFor();
    await page.evaluate(() => window.dispatchEvent(new Event("online")));
    await page.locator('.ms-Release[data-state="cannotCheck"]').waitFor();
    assert.match(await badge.innerText(), /\? Cannot check/);
    fail = false;
    deployed = loaded;
    await page.evaluate(() => window.dispatchEvent(new Event("online")));
    await page.locator('.ms-Release[data-state="latest"]').waitFor();
    assert.equal(
      await badge.evaluate((node) => node.getBoundingClientRect().right <= window.innerWidth),
      true,
    );
    // Exercise the online-only path without turning an ordinary refresh into a full-course download.
    await page
      .locator('.ms-Startup[data-phase="ready"],.ms-Startup[data-phase="hidden"]')
      .waitFor({ state: "attached", timeout: 120000 });
    deployed = "b".repeat(40) === loaded ? "c".repeat(40) : "b".repeat(40);
    await page.evaluate(() => {
      window.releaseUpdateMarker = "not reloaded";
      window.dispatchEvent(new Event("focus"));
    });
    const update = page.getByRole("button", { name: "Update and reload", exact: true });
    await update.waitFor();
    await page.waitForFunction(() => !document.querySelector(".ms-Release button").disabled);
    const example = page.locator(".ms-Example").first();
    const editor = example.locator(".cm-content");
    const savedCode = (await editor.innerText()) + "\n# Retained by Update and reload";
    const answer = page.locator('textarea[data-answer="ch01.daily_sales"]');
    await answer.fill("My answer before Update and reload");
    await example.evaluate((node) => (node.dataset.unsaved = "true"));
    await update.click();
    await page
      .getByText(
        "Cannot reload because some edits could not be saved. Use Export answers and Download code before trying again.",
        { exact: true },
      )
      .waitFor();
    assert.equal(await page.evaluate(() => window.releaseUpdateMarker), "not reloaded");
    await example.evaluate((node) => delete node.dataset.unsaved);
    fail = true;
    await update.click();
    await page
      .getByText("Could not update. Your current version is still available. Try again.", {
        exact: true,
      })
      .waitFor();
    assert.equal(await page.evaluate(() => window.releaseUpdateMarker), "not reloaded");
    fail = false;
    await editor.fill("import time\ntime.sleep(3)");
    await example.getByRole("button", { name: "Run", exact: true }).click();
    await page.waitForFunction(() => document.querySelector(".ms-Release button").disabled);
    await page.waitForFunction(() => !document.querySelector(".ms-Release button").disabled, null, {
      timeout: 120000,
    });
    await editor.fill(savedCode);
    const html = await (await fetch(`${base}/notebooks/index.html`)).text();
    await context.route("**/notebooks/index.html?*", (route) =>
      route.fulfill({ contentType: "text/html", body: html.replace(loaded, deployed) }),
    );
    let fullDownloads = 0;
    page.on("request", (request) => {
      if (request.url().includes("offline-manifest.json")) fullDownloads++;
    });
    await update.click();
    await page.waitForFunction(
      (commit) => document.querySelector('meta[name="ms-commit"]')?.content === commit,
      deployed,
      { timeout: 120000 },
    );
    await page.locator('.ms-Release[data-state="latest"]').waitFor();
    await editor.waitFor({ timeout: 120000 });
    await answer.waitFor({ state: "attached" });
    assert.equal(await editor.innerText(), savedCode);
    assert.equal(await answer.inputValue(), "My answer before Update and reload");
    assert.equal(fullDownloads, 0);
    console.log(
      "ok update button: unsaved drafts and running code block reload; network failure keeps the page; online reload retains answers/code without downloading the full course",
    );
    // A worker can still be waiting even when the loaded HTML already has the latest commit.
    await page.evaluate(() => {
      navigator.serviceWorker.getRegistrations = async () => [
        { waiting: { scriptURL: new URL("../python-worker.js", location.href).href } },
      ];
      window.dispatchEvent(new Event("focus"));
    });
    await page.getByRole("button", { name: "Reload to update", exact: true }).waitFor();
    console.log(
      "ok release: loaded commit, current tick, outdated cross, offline unknown and reconnect; fits a 360px header",
    );
  } finally {
    await context.close();
  }
}
