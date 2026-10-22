// Copyright © 2026 Christopher Snow

// Test a complete published build at a GitHub Pages subpath. Restart the browser and clear its
// HTTP cache before taking the network away, so successful runs must use the offline snapshot.
import assert from "node:assert/strict";
import { spawn } from "node:child_process";
import { createHash } from "node:crypto";
import { mkdtemp, readFile, writeFile, rm, symlink } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";
import { chromium } from "playwright";

const site = resolve(process.argv[2] || "apps/course/dist");
const temp = await mkdtemp(join(tmpdir(), "ms-offline-"));
await symlink(site, join(temp, "metadata-systems"));
await writeFile(join(temp, "unrelated-worker.js"), 'self.addEventListener("fetch", () => {});');
const base = "http://127.0.0.1:8877/metadata-systems/";
const server = spawn("python3", ["-m", "http.server", "8877", "--bind", "127.0.0.1"], {
  cwd: temp,
  stdio: "ignore",
});
const manifestPath = join(site, "offline-manifest.json");
const original = await readFile(manifestPath, "utf8");
const first = JSON.parse(original);
const extra = "offline-test-revision.txt";
let context;
const ok = (text) => console.log(`ok  offline: ${text}`);
const launch = () =>
  chromium.launchPersistentContext(join(temp, "profile"), {
    viewport: { width: 390, height: 844 },
  });
const ready = (page) => page.waitForSelector('[data-offline-ready="true"]', { timeout: 180_000 });
const done = (page) =>
  page.waitForFunction(() => !document.querySelector(".offline-course progress"), null, {
    timeout: 180_000,
  });
const findAnswer = async (page, id) => {
  for (let attempt = 0; attempt < 3; attempt++) {
    const found = await page.evaluate(async (id) => {
      const outer = document.querySelector(".jp-WindowedPanel-outer");
      for (let y = 0; y <= outer.scrollHeight; y += 450) {
        outer.scrollTop = y;
        await new Promise((resolve) => setTimeout(resolve, 50));
        if (document.querySelector(`textarea[data-answer="${id}"]`)) return true;
      }
      return false;
    }, id);
    if (found) return page.locator(`textarea[data-answer="${id}"]`).first();
  }
  throw Error("Missing answer field");
};
const chapter = async (page, number) => {
  await page.goto(
    `${base}jupyterlite/notebooks/index.html?path=chapter_${String(number).padStart(2, "0")}.ipynb`,
  );
  await page.waitForSelector(".jp-MarkdownOutput h1", { timeout: 120_000 });
  await page.click('button[data-action="runAll"]');
  await page.waitForFunction(
    () => !document.querySelector('button[data-action="runAll"]:disabled'),
    null,
    { timeout: 120_000 },
  );
  assert.equal(await page.locator(".ms-Status").textContent(), "Every cell has run.");
  assert.equal(await page.locator(".jp-OutputArea-output.jp-mod-error").count(), 0);
};
try {
  for (let i = 0; i < 100; i++) {
    if (
      await fetch(base).then(
        (r) => r.ok,
        () => false,
      )
    )
      break;
    await new Promise((resolve) => setTimeout(resolve, 100));
  }
  context = await launch();
  let page = context.pages()[0];
  page.on("pageerror", (error) => console.log("page error", error.message));
  page.on("console", (message) => {
    if (message.type() === "error") console.log("browser error", message.text());
  });
  await page.goto(base);
  await page.getByRole("button", { name: "Download full course", exact: true }).waitFor();
  assert.equal(
    await page.locator("[data-offline-ready]").getAttribute("data-offline-ready"),
    "false",
  );
  // Other projects on this origin and learner answers must survive cache management.
  await page.evaluate(async () => {
    await navigator.serviceWorker.register("/unrelated-worker.js", { scope: "/unrelated/" });
    await (await caches.open("another-project")).put("/unrelated", new Response("keep"));
    localStorage.setItem(
      "ms:metadata-systems:answers:v1:ch01.daily_sales",
      "My offline explanation",
    );
  });
  await page.getByRole("button", { name: "Download full course", exact: true }).click();
  await page.getByRole("progressbar").waitFor();
  await page.getByRole("button", { name: "Cancel download" }).click();
  await done(page);
  assert.match(await page.locator('.offline-course [role="status"]').textContent(), /cancelled/);
  assert.equal(
    await page.locator("[data-offline-ready]").getAttribute("data-offline-ready"),
    "false",
  );
  ok("an interrupted download is resumable and never reports ready");
  await page.getByRole("button", { name: "Download full course", exact: true }).click();
  await ready(page);
  await done(page);
  assert(await page.evaluate(() => caches.has("another-project")));
  assert(
    await page.evaluate(() => {
      const section = document.querySelector(".offline-course");
      return (
        section.scrollWidth <= section.clientWidth &&
        [...section.querySelectorAll("button")].every(
          (button) => button.getBoundingClientRect().height >= 44,
        )
      );
    }),
  );
  ok(`complete ${first.files.length}-file download fits a phone and leaves other projects intact`);
  const cdp = await context.newCDPSession(page);
  await cdp.send("Network.clearBrowserCache");
  await context.close();
  context = await launch();
  await context.setOffline(true);
  page = context.pages()[0];
  page.on("pageerror", (error) => console.log("offline page error", error.message));
  page.on("requestfailed", (request) => console.log("offline request failed", request.url()));
  await page.goto(base);
  await ready(page);
  assert.match(await page.locator('.offline-course [role="status"]').textContent(), /offline/);
  ok("the home page survives a browser restart offline with an empty HTTP cache");
  await page.goto(`${base}jupyterlite/notebooks/index.html?path=chapter_01b.ipynb`);
  await page.waitForSelector('.ms-Example[data-example="daily_sales"]', { timeout: 120_000 });
  const reader = page.locator('.ms-Example[data-example="daily_sales"]');
  await reader.getByRole("button", { name: "Run", exact: true }).click();
  await page.waitForFunction(
    () => !document.querySelector('[data-reader-action="run"]:disabled'),
    null,
    { timeout: 120_000 },
  );
  assert.equal(await reader.locator("tbody tr").count(), 7);
  const readerCode = reader.locator(".cm-content");
  await readerCode.fill((await readerCode.innerText()) + "\n# My offline edit");
  await page.reload();
  await page.waitForSelector('.ms-Example[data-example="daily_sales"]', { timeout: 120_000 });
  assert.match(await readerCode.innerText(), /My offline edit/);
  ok("Chapter 1b executes offline and retains an unrun code edit across refresh");
  await chapter(page, 1);
  assert.equal(
    await (await findAnswer(page, "ch01.daily_sales")).inputValue(),
    "My offline explanation",
  );
  await (await findAnswer(page, "ch01.daily_sales")).fill("Changed without a connection");
  await page.click('button[data-action="save"]');
  await page.waitForFunction(() => !document.querySelector('button[data-action="save"]:disabled'));
  await page.reload();
  await page.waitForSelector(".jp-MarkdownOutput h1");
  assert.equal(
    await (await findAnswer(page, "ch01.daily_sales")).inputValue(),
    "Changed without a connection",
  );
  await chapter(page, 2);
  assert.equal(
    await (await findAnswer(page, "ch01.daily_sales")).inputValue(),
    "Changed without a connection",
  );
  await chapter(page, 33);
  assert(await page.evaluate(() => navigator.serviceWorker.getRegistration("/unrelated/")));
  ok("Python runs in new chapters offline; answers survive saving, refresh and chapter navigation");
  await context.setOffline(false);
  const content = Buffer.from("A second complete offline release.");
  const next = {
    ...first,
    version: "0123456789abcdef0123",
    bytes: first.bytes + content.length,
    files: [
      ...first.files,
      {
        path: extra,
        size: content.length,
        sha256: createHash("sha256").update(content).digest("hex"),
      },
    ],
  };
  await writeFile(manifestPath, JSON.stringify(next));
  await page.goto(base);
  await page.getByRole("button", { name: "Download update", exact: true }).waitFor();
  await page.getByRole("button", { name: "Download update", exact: true }).click();
  await done(page);
  assert.match(
    await page.locator('.offline-course [role="status"]').textContent(),
    /Could not complete/,
  );
  assert.equal(
    await page.locator("[data-offline-ready]").getAttribute("data-offline-ready"),
    "true",
  );
  await context.setOffline(true);
  await chapter(page, 3);
  ok("a failed update preserves the previous complete course and its Python runtime");
  await context.setOffline(false);
  // A successful HTTP response with the wrong bytes must also leave the working copy intact.
  await writeFile(join(site, extra), Buffer.alloc(content.length, 120));
  await page.goto(base);
  await page.getByRole("button", { name: "Download update", exact: true }).click();
  await done(page);
  assert.match(
    await page.locator('.offline-course [role="status"]').textContent(),
    /Could not complete/,
  );
  assert.equal(
    await page.locator("[data-offline-ready]").getAttribute("data-offline-ready"),
    "true",
  );
  ok("a checksum mismatch cannot publish a corrupt update");
  await writeFile(join(site, extra), content);
  await page.goto(base);
  await page.getByRole("button", { name: "Download update", exact: true }).click();
  await done(page);
  await ready(page);
  await context.setOffline(true);
  assert.equal(
    await page.evaluate(async (url) => (await fetch(url)).text(), base + extra),
    content.toString(),
  );
  ok("a completed update is published atomically and serves its new files offline");
  // Simulate an evicted asset without trusting a localStorage ready flag.
  await context.setOffline(false);
  await page.goto(base);
  await page.evaluate(async (base) => {
    const cache = await caches.open(`ms:metadata-systems:offline:${base}:0123456789abcdef0123`);
    await cache.delete(new URL("jupyterlite/static/pyodide/pyodide.asm.wasm", base).href);
  }, base);
  await page.reload();
  await page.getByRole("button", { name: "Download full course", exact: true }).waitFor();
  assert.equal(
    await page.locator("[data-offline-ready]").getAttribute("data-offline-ready"),
    "false",
  );
  ok("readiness checks detect an incomplete or evicted cache");
  const savedNotebook = () =>
    page.evaluate(async () => {
      const { name } = (await indexedDB.databases()).find((db) =>
        db.name.startsWith("JupyterLite Storage"),
      );
      return new Promise((resolve, reject) => {
        const open = indexedDB.open(name);
        open.onerror = () => reject(open.error);
        open.onsuccess = () => {
          const db = open.result;
          const request = db.transaction("files").objectStore("files").get("chapter_01.ipynb");
          request.onsuccess = () => {
            db.close();
            resolve(request.result);
          };
          request.onerror = () => reject(request.error);
        };
      });
    });
  const notebookBefore = await savedNotebook();
  assert(notebookBefore?.content?.cells?.length);
  await page.getByRole("button", { name: "Remove downloaded course", exact: true }).click();
  await page.waitForFunction(() => !document.querySelector(".offline-course button:disabled"));
  assert(await page.evaluate(() => caches.has("another-project")));
  assert(await page.evaluate(() => navigator.serviceWorker.getRegistration("/unrelated/")));
  assert.deepEqual(await savedNotebook(), notebookBefore);
  assert.match(
    await page.evaluate(() =>
      localStorage.getItem("ms:metadata-systems:code:v1:chapter_01b.ipynb:daily_sales"),
    ),
    /My offline edit/,
  );
  assert.equal(
    await page.evaluate(() =>
      localStorage.getItem("ms:metadata-systems:answers:v1:ch01.daily_sales"),
    ),
    "Changed without a connection",
  );
  ok("removing downloaded files preserves answers, saved notebooks and unrelated workers/caches");
  console.log("Offline checks passed.");
} finally {
  await context?.close();
  server.kill();
  await writeFile(manifestPath, original);
  await rm(join(site, extra), { force: true });
  await rm(temp, { recursive: true, force: true });
}
