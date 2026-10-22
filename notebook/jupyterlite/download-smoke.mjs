// Copyright © 2026 Christopher Snow

// Exercise real service-worker byte reporting. The HTTP server pauses part-way through WASM;
// page routes cannot intercept requests initiated by a controlling service worker reliably.
import assert from "node:assert/strict";
import { createServer } from "node:http";
import { readFile, stat } from "node:fs/promises";
import { existsSync } from "node:fs";
import { resolve, extname } from "node:path";
import { chromium } from "playwright";

const root = resolve(process.argv[2]);
const lite = existsSync(resolve(root, "jupyter-lite.json")) ? "" : "/jupyterlite";
let release;
const gate = new Promise((done) => (release = done));
let blocked = false;
const server = createServer(async (request, response) => {
  try {
    const pathname = decodeURIComponent(new URL(request.url, "http://localhost").pathname);
    let file = resolve(root, "." + pathname);
    if (!file.startsWith(root + "/") && file !== root) throw Error("Outside site");
    if ((await stat(file)).isDirectory()) file = resolve(file, "index.html");
    const bytes = await readFile(file);
    const mime =
      {
        ".js": "text/javascript",
        ".mjs": "text/javascript",
        ".css": "text/css",
        ".json": "application/json",
        ".html": "text/html",
        ".wasm": "application/wasm",
      }[extname(file)] || "application/octet-stream";
    response.writeHead(200, { "Content-Type": mime, "Content-Length": bytes.length });
    if (file.endsWith("/pyodide.asm.wasm") && !blocked) {
      blocked = true;
      const stop = Math.floor(bytes.length / 4);
      for (let offset = 0; offset < stop; offset += 65536) {
        if (response.destroyed) return;
        response.write(bytes.subarray(offset, Math.min(offset + 65536, stop)));
        await new Promise((done) => setTimeout(done, 8));
      }
      await gate;
      if (!response.destroyed) response.end(bytes.subarray(stop));
    } else response.end(bytes);
  } catch {
    if (!response.headersSent) response.writeHead(404);
    response.end();
  }
});
await new Promise((done) => server.listen(8869, "127.0.0.1", done));
const browser = await chromium.launch();
try {
  const context = await browser.newContext({ viewport: { width: 390, height: 844 } });
  const page = await context.newPage();
  const errors = [];
  page.on("pageerror", (error) => errors.push(error.message));
  await page.goto(`http://127.0.0.1:8869${lite}/notebooks/index.html?path=chapter_01.ipynb`);
  await page.waitForFunction(
    () => {
      const node = document.querySelector('.ms-Startup[data-phase="loading"]');
      return node && Number(node.dataset.percent) >= 10 && Number(node.dataset.percent) <= 26;
    },
    null,
    { timeout: 120000 },
  );
  assert(blocked);
  const banner = page.locator(".ms-Startup");
  const percent = Number(await banner.getAttribute("data-percent"));
  assert.match(await banner.innerText(), /Downloading Python's main runtime file: \d+%/);
  assert.equal(Number(await banner.locator("progress").getAttribute("value")), percent);
  assert(await page.locator('textarea[data-answer="ch01.daily_sales"]').isEditable());
  await page
    .locator('textarea[data-answer="ch01.daily_sales"]')
    .fill("My answer during the download");
  await banner.screenshot({ path: "/tmp/metadata-python-download.png" });
  await page.getByRole("button", { name: "Run all", exact: true }).click();
  assert(await page.getByRole("button", { name: "Run all", exact: true }).isDisabled());
  console.log(
    `ok download: actual streamed bytes show ${percent}% while Python remains unavailable`,
  );
  release();
  await page
    .getByText("All examples finished successfully.", { exact: true })
    .waitFor({ timeout: 120000 });
  assert.equal(
    await page.locator('textarea[data-answer="ch01.daily_sales"]').inputValue(),
    "My answer during the download",
  );
  assert.equal(await page.locator('.ms-Example[data-example="daily_sales"] tbody tr').count(), 7);
  assert.deepEqual(errors, []);
  console.log(
    "ok download: releasing the stream starts Python, runs the queued examples and retains answers",
  );
  await context.close();
} finally {
  release();
  await browser.close();
  server.closeAllConnections();
  await new Promise((done) => server.close(done));
}
