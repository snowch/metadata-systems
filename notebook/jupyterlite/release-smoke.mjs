// Copyright © 2026 Christopher Snow

import assert from "node:assert/strict";

export async function checkRelease(browser, base) {
  const context = await browser.newContext({
    serviceWorkers: "block",
    hasTouch: true,
    reducedMotion: "reduce",
    viewport: { width: 360, height: 800 },
  });
  try {
    const page = await context.newPage();
    let deployed = await (await fetch(`${base}/release.json`)).json();
    let failure = false;
    let delay = 0;
    await context.route("**/release.json", async (route) => {
      if (delay) await new Promise((resolve) => setTimeout(resolve, delay));
      assert.equal(route.request().headers()["x-ms-offline-download"], "release-check");
      return failure ? route.abort("internetdisconnected") : route.fulfill({ json: deployed });
    });
    await page.goto(`${base}/notebooks/index.html?path=chapter_01.ipynb`);
    const badge = page.locator(".ms-AppStatus");
    await page.locator('.ms-AppStatus[data-state="upToDate"]').waitFor({ timeout: 120000 });
    const loaded = deployed;
    assert.equal(await badge.locator("a").textContent(), loaded.commit.slice(0, 7));
    assert.equal(
      await badge.locator("a").getAttribute("href"),
      `https://github.com/snowch/metadata-systems/commit/${loaded.commit}`,
    );
    await badge.getByRole("button").tap();
    const dialog = page.getByRole("dialog", { name: "App status", exact: true });
    await dialog.getByRole("heading", { name: "Offline access" }).waitFor();
    deployed = {
      ...loaded,
      build: "a".repeat(20) === loaded.build ? "b".repeat(20) : "a".repeat(20),
    };
    await dialog.getByRole("button", { name: "Check for updates", exact: true }).click();
    await page.locator('.ms-AppStatus[data-state="updateAvailable"]').waitFor();
    assert.equal(await badge.locator("a").textContent(), loaded.commit.slice(0, 7));
    await dialog.getByRole("button", { name: "Later", exact: true }).isHidden();
    await page.keyboard.press("Escape");
    assert.match(await badge.innerText(), /Update available/);
    assert.equal(
      await badge.getByRole("button").evaluate((n) => n === document.activeElement),
      true,
    );
    failure = true;
    await badge.getByRole("button").click();
    await page.locator('.ms-AppStatus[data-state="checkFailed"]').waitFor();
    await dialog.getByRole("button", { name: "Retry", exact: true }).waitFor();
    assert.equal(await badge.locator("a").textContent(), loaded.commit.slice(0, 7));
    failure = false;
    deployed = { commit: loaded.commit, build: "invalid", schema: 1 };
    await dialog.getByRole("button", { name: "Retry", exact: true }).click();
    await page.locator('.ms-AppStatus[data-state="checkFailed"]').waitFor();
    await page.evaluate(() => window.dispatchEvent(new Event("offline")));
    await page.locator('.ms-AppStatus[data-state="cannotCheck"]').waitFor();
    deployed = loaded;
    delay = 500;
    await dialog.getByRole("button", { name: "Check for updates", exact: true }).click();
    await page.evaluate(() => window.dispatchEvent(new Event("offline")));
    await page.waitForTimeout(650);
    await page.locator('.ms-AppStatus[data-state="cannotCheck"]').waitFor();
    delay = 0;
    await dialog.getByRole("button", { name: "Check for updates", exact: true }).click();
    await page.locator('.ms-AppStatus[data-state="upToDate"]').waitFor();
    assert(
      await dialog.evaluate(
        (n) => n.scrollWidth <= n.clientWidth && n.getBoundingClientRect().right <= innerWidth,
      ),
    );
    console.log(
      "ok app status: embedded identity, deployed build, pending badge, failure, malformed release, offline uncertainty, keyboard focus and 360px layout",
    );
  } finally {
    await context.close();
  }
}
