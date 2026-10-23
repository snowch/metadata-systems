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
const htmlPath = join(site, "jupyterlite/notebooks/index.html");
const releasePath = join(site, "jupyterlite/release.json");
const workerPath = join(site, "offline-worker.js");
const originalHTML = await readFile(htmlPath, "utf8");
const originalRelease = await readFile(releasePath, "utf8");
const originalWorker = await readFile(workerPath, "utf8");
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
  const selector = `textarea[data-answer="${id}"]`;
  await page.waitForSelector(selector, { state: "attached", timeout: 120000 });
  return page.locator(selector).first();
};
const chapter = async (page, number) => {
  await page.goto(
    `${base}jupyterlite/notebooks/index.html?path=chapter_${String(number).padStart(2, "0")}.ipynb`,
  );
  await page.waitForSelector(".jp-MarkdownOutput h1", { timeout: 120_000 });
  await page.click('button[data-reader-action="runAll"]');
  await page.waitForFunction(
    () => !document.querySelector('button[data-reader-action="runAll"]:disabled'),
    null,
    { timeout: 120_000 },
  );
  assert.equal(
    await page.locator(".ms-Reader-progress").textContent(),
    "All examples finished successfully.",
  );
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
  await page.goto(`${base}jupyterlite/notebooks/index.html?path=chapter_01.ipynb`);
  await page.waitForSelector('.ms-Example[data-example="daily_sales"]', { timeout: 120_000 });
  const reader = page.locator('.ms-Example[data-example="daily_sales"]');
  await page.getByRole("button", { name: "Run all", exact: true }).click();
  await page
    .getByText("All examples finished successfully.", { exact: true })
    .waitFor({ timeout: 120_000 });
  assert.equal(await reader.locator("tbody tr").count(), 7);
  const readerCode = reader.locator(".cm-content");
  await readerCode.fill((await readerCode.innerText()) + "\n# My offline edit");
  await page.reload();
  await page.waitForSelector('.ms-Example[data-example="daily_sales"]', { timeout: 120_000 });
  assert.match(await readerCode.innerText(), /My offline edit/);
  ok("Chapter 1 runs all examples offline and retains an unrun code edit across refresh");
  await chapter(page, 1);
  await page.locator('.ms-Release[data-state="cannotCheck"]').waitFor();
  assert.match(await page.locator(".ms-Release").innerText(), /\? Cannot check/);
  ok("the offline reader shows its commit without claiming it is the latest deployment");
  assert.equal(
    await (await findAnswer(page, "ch01.daily_sales")).inputValue(),
    "My offline explanation",
  );
  await (await findAnswer(page, "ch01.daily_sales")).fill("Changed without a connection");
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
  const updatedCommit = "abcdef0123".repeat(4);
  const updatedHTML = originalHTML.replace(
    /(<meta name="ms-commit" content=")[a-f0-9]{40}/,
    "$1" + updatedCommit,
  );
  await writeFile(htmlPath, updatedHTML);
  await writeFile(releasePath, JSON.stringify({ commit: updatedCommit }));
  // A changed worker must activate while both old reader tabs remain open.
  await writeFile(workerPath, originalWorker + "\n// A new published worker.\n");
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
  next.files = next.files.map((file) =>
    file.path !== "jupyterlite/notebooks/index.html"
      ? file
      : {
          ...file,
          size: Buffer.byteLength(updatedHTML),
          sha256: createHash("sha256").update(updatedHTML).digest("hex"),
        },
  );
  next.bytes = next.files.reduce((sum, file) => sum + file.size, 0);
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
  await chapter(page, 1);
  try {
    await page.locator('.ms-Release[data-state="updateAvailable"]').waitFor();
  } catch (error) {
    console.log(
      "update detection",
      await page.evaluate(async () => ({
        online: navigator.onLine,
        commit: document.querySelector('meta[name="ms-commit"]')?.content,
        badge: document.querySelector(".ms-Release")?.outerHTML,
        release: await fetch(new URL("../release.json", location.href), {
          headers: { "X-MS-Offline-Download": "release-check" },
          cache: "no-store",
        })
          .then((r) => r.text())
          .catch(String),
      })),
    );
    throw error;
  }
  const other = await context.newPage();
  await chapter(other, 2);
  const otherDraft = other.locator(".ms-Example .cm-content").first();
  await otherDraft.fill((await otherDraft.innerText()) + "\n# Kept in another open tab");
  await other.evaluate(() => {
    window.updateTabMarker = "still open";
    window.controllerUpdates = 0;
    navigator.serviceWorker.addEventListener("controllerchange", () => window.controllerUpdates++);
  });
  const home = await context.newPage();
  await home.goto(base);
  await home.locator(".offline-course").waitFor();
  await home.evaluate(() => (window.updateHomeMarker = "still open"));
  await page.bringToFront();
  await page.waitForFunction(
    async () => Boolean((await navigator.serviceWorker.getRegistration())?.waiting),
    null,
    { timeout: 30000 },
  );
  await page.evaluate(() => {
    window.controllerUpdates = 0;
    navigator.serviceWorker.addEventListener("controllerchange", () => window.controllerUpdates++);
  });
  await page.getByRole("button", { name: "Update and reload", exact: true }).click();
  await page.waitForFunction(
    (commit) => document.querySelector('meta[name="ms-commit"]')?.content === commit,
    updatedCommit,
    { timeout: 180000 },
  );
  await page.locator('.ms-Release[data-state="latest"]').waitFor();
  assert.match(
    await page.locator('.ms-Example[data-example="daily_sales"] .cm-content').innerText(),
    /My offline edit/,
  );
  assert.equal(
    await (await findAnswer(page, "ch01.daily_sales")).inputValue(),
    "Changed without a connection",
  );
  assert.equal(
    await other.evaluate(() => window.updateTabMarker),
    "still open",
    "another tab must never be reloaded automatically",
  );
  assert.ok(
    (await other.evaluate(() => window.controllerUpdates)) > 0,
    "the new worker claims other open tabs without closing them",
  );
  assert.equal(await home.evaluate(() => window.updateHomeMarker), "still open");
  await home.getByRole("button", { name: "Reload to update", exact: true }).waitFor();
  await home.getByRole("button", { name: "Reload to update", exact: true }).click();
  await home.waitForFunction(() => window.updateHomeMarker === undefined);
  await ready(home);
  await home.close();
  await other.getByRole("button", { name: "Reload to update", exact: true }).waitFor();
  await other.bringToFront();
  await other.getByRole("button", { name: "Reload to update", exact: true }).click();
  await other.waitForFunction(
    (commit) => document.querySelector('meta[name="ms-commit"]')?.content === commit,
    updatedCommit,
    { timeout: 180000 },
  );
  await other.locator(".ms-Example .cm-content").first().waitFor();
  assert.match(
    await other.locator(".ms-Example .cm-content").first().innerText(),
    /Kept in another open tab/,
  );
  await other.close();
  ok(
    "Update and reload verifies the offline snapshot, activates a waiting worker with two tabs open, retains answers/code, and lets the other tab choose when to reload",
  );
  await context.setOffline(true);
  assert.equal(
    await page.evaluate(async (url) => (await fetch(url)).text(), base + extra),
    content.toString(),
  );
  ok("a completed update is published atomically and serves its new files offline");
  // Retrying an already complete release must retain the previous snapshot for old open tabs.
  const sharedClient = await readFile(new URL("../offline/client.js", import.meta.url), "utf8");
  await page.evaluate(
    async ({ source, manifest, base }) => {
      const create = new Function(
        source.replace("export function createOffline", "function createOffline") +
          ";return createOffline;",
      )();
      const prefix = `ms:metadata-systems:offline:${base}:`;
      const stateURL = new URL("__offline_state__", base).href;
      const meta = await caches.open(prefix + "meta");
      const before = await (await meta.match(stateURL)).json();
      if (!before.previous) throw new Error("Missing previous snapshot before retry");
      await create(base).download(manifest, new AbortController().signal, () => {});
      const after = await (await meta.match(stateURL)).json();
      if (
        after.previous !== before.previous ||
        !(await caches.keys()).includes(prefix + before.previous)
      )
        throw new Error("Retry discarded the previous snapshot");
    },
    { source: sharedClient, manifest: next, base },
  );
  ok("retrying the same release keeps the previous snapshot for other open tabs");
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
  const savedNotebook = (seed = false) =>
    page.evaluate(async (seed) => {
      const { name } = (await indexedDB.databases()).find((db) =>
        db.name.startsWith("JupyterLite Storage"),
      );
      return new Promise((resolve, reject) => {
        const open = indexedDB.open(name);
        open.onerror = () => reject(open.error);
        open.onsuccess = () => {
          const db = open.result;
          const files = db
            .transaction("files", seed ? "readwrite" : "readonly")
            .objectStore("files");
          if (seed)
            files.put(
              {
                type: "notebook",
                format: "json",
                content: {
                  cells: [
                    {
                      cell_type: "code",
                      source: ["# Stored notebook retained independently of the course download"],
                      metadata: {},
                      outputs: [],
                      execution_count: null,
                    },
                  ],
                  metadata: {},
                  nbformat: 4,
                  nbformat_minor: 5,
                },
              },
              "kept-notebook.ipynb",
            );
          const request = files.get("kept-notebook.ipynb");
          request.onsuccess = () => {
            db.close();
            resolve(request.result);
          };
          request.onerror = () => reject(request.error);
        };
      });
    }, seed);
  const notebookBefore = await savedNotebook(true);
  assert(notebookBefore?.content?.cells?.length);
  await page.getByRole("button", { name: "Remove downloaded course", exact: true }).click();
  await page.waitForFunction(() => !document.querySelector(".offline-course button:disabled"));
  assert(await page.evaluate(() => caches.has("another-project")));
  assert(await page.evaluate(() => navigator.serviceWorker.getRegistration("/unrelated/")));
  assert.deepEqual(await savedNotebook(), notebookBefore);
  assert.match(
    await page.evaluate(() =>
      localStorage.getItem("ms:metadata-systems:code:v1:chapter_01.ipynb:daily_sales"),
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
  await writeFile(htmlPath, originalHTML);
  await writeFile(releasePath, originalRelease);
  await writeFile(workerPath, originalWorker);
  await rm(join(site, extra), { force: true });
  await rm(temp, { recursive: true, force: true });
}
