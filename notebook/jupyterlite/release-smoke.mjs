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
    console.log(
      "ok release: loaded commit, current tick, outdated cross, offline unknown and reconnect; fits a 360px header",
    );
  } finally {
    await context.close();
  }
}
