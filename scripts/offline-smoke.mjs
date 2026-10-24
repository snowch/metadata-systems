// Copyright © 2026 Christopher Snow

// Real assembled releases, real service worker, real Python, persistent profile and empty HTTP
// cache. The second release is rebuilt from changed production HTML/assets, never a fake timer.
import assert from "node:assert/strict";
import { spawn, execFileSync } from "node:child_process";
import { mkdtemp, readFile, writeFile, rm, symlink } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";
import { chromium } from "playwright";

const site = resolve(process.argv[2] || "apps/course/dist");
const temp = await mkdtemp(join(tmpdir(), "ms-offline-"));
await symlink(site, join(temp, "metadata-systems"));
await writeFile(join(temp, "unrelated-worker.js"), 'self.addEventListener("fetch", () => {});');
const base = "http://127.0.0.1:8877/metadata-systems/";
const paths = [
  "offline-manifest.json",
  "release.json",
  "jupyterlite/release.json",
  "index.html",
  "jupyterlite/notebooks/index.html",
  "jupyterlite/tree/index.html",
  "offline-worker.js",
];
const originals = new Map(
  await Promise.all(paths.map(async (p) => [p, await readFile(join(site, p))])),
);
const first = JSON.parse(originals.get("offline-manifest.json"));
const releaseA = JSON.parse(originals.get("release.json"));
const server = spawn("python3", ["-m", "http.server", "8877", "--bind", "127.0.0.1"], {
  cwd: temp,
  stdio: "ignore",
});
const ok = (text) => console.log(`ok app status/offline: ${text}`);
let context, onlineBrowser, onlineContext, onlinePage;
const launch = () =>
  chromium.launchPersistentContext(join(temp, "profile"), {
    viewport: { width: 390, height: 844 },
  });
async function open(page) {
  const dialog = page.getByRole("dialog", { name: "App status", exact: true });
  if (!(await dialog.isVisible())) await page.locator(".ms-AppStatus > button").click();
  await dialog.waitFor();
  return dialog;
}
const settled = (page) =>
  page.locator(".ms-AppStatus-dialog progress").waitFor({ state: "hidden", timeout: 180000 });
const ready = (page) =>
  page.waitForSelector('[data-offline-ready="true"]', { state: "attached", timeout: 180000 });
async function home(page) {
  await page.goto(base);
  return open(page);
}
async function chapter(page, number, run = true) {
  await page.goto(
    `${base}jupyterlite/notebooks/index.html?path=chapter_${String(number).padStart(2, "0")}.ipynb`,
  );
  await page.waitForSelector(".jp-MarkdownOutput h1", { timeout: 120000 });
  if (run) {
    await page.click('button[data-reader-action="runAll"]');
    await page.waitForFunction(
      () => !document.querySelector('button[data-reader-action="runAll"]:disabled'),
      null,
      { timeout: 120000 },
    );
    assert.equal(
      await page.locator(".ms-Reader-progress").textContent(),
      "All examples finished successfully.",
    );
    assert.equal(await page.locator(".jp-OutputArea-output.jp-mod-error").count(), 0);
  }
}
try {
  for (let i = 0; i < 100; i++) {
    if (
      await fetch(base).then(
        (r) => r.ok,
        () => false,
      )
    )
      break;
    await new Promise((r) => setTimeout(r, 100));
  }
  context = await launch();
  let page = context.pages()[0];
  page.on("pageerror", (e) => console.log("page error", e.message));
  let dialog = await home(page);
  await dialog.getByRole("button", { name: "Download for offline use", exact: true }).waitFor();
  await page.evaluate(async () => {
    await navigator.serviceWorker.register("/unrelated-worker.js", { scope: "/unrelated/" });
    await (await caches.open("another-project")).put("/unrelated", new Response("keep"));
    localStorage.setItem("ms:metadata-systems:answers:v1:ch01.daily_sales", "Retained answer");
    localStorage.setItem("user-imported-file", "keep");
  });
  await dialog.getByRole("button", { name: "Download for offline use", exact: true }).click();
  await dialog.getByRole("button", { name: "Cancel download", exact: true }).click();
  await settled(page);
  await dialog.getByText(/Download cancelled/).waitFor();
  assert.equal(
    await dialog.locator("[data-offline-ready]").getAttribute("data-offline-ready"),
    "false",
  );
  // A cancellation before the first asset can leave no partial cache; either action is honest.
  await dialog
    .getByRole("button", { name: /^(Resume download|Download for offline use)$/ })
    .click();
  await ready(page);
  await settled(page);
  ok(`cancel/resume verified ${first.files.length} assets, ${(first.bytes / 1e6).toFixed(1)} MB`);
  for (const width of [360, 1280]) {
    await page.setViewportSize({ width, height: 844 });
    assert(await dialog.evaluate((n) => n.scrollWidth <= n.clientWidth));
    assert(
      await dialog
        .locator("button:visible")
        .evaluateAll((ns) => ns.every((n) => n.getBoundingClientRect().height >= 44)),
    );
    await page.screenshot({ path: `/tmp/ms-app-status-${width}.png` });
  }
  await context.close();
  context = await launch();
  page = context.pages()[0];
  const cdp = await context.newCDPSession(page);
  await cdp.send("Network.clearBrowserCache");
  await cdp.detach();
  await context.setOffline(true);
  await page.goto(`${base}jupyterlite/tree/index.html`);
  await open(page);
  assert.equal(
    await page.locator('meta[name="ms-commit"]').getAttribute("content"),
    releaseA.commit,
  );
  await chapter(page, 1);
  const answer = page.locator('textarea[data-answer="ch01.daily_sales"]');
  assert.equal(await answer.inputValue(), "Retained answer");
  await answer.fill("Saved while offline");
  const editor = page.locator(".ms-Example .cm-content").first();
  await editor.click();
  await editor.press("ControlOrMeta+a");
  await page.keyboard.insertText((await editor.innerText()) + "\n# Retained code");
  await chapter(page, 2);
  assert.equal(
    await page.locator('textarea[data-answer="ch01.daily_sales"]').inputValue(),
    "Saved while offline",
  );
  await page.goto(`${base}notebook/index.html`);
  await page.waitForURL(/jupyterlite\/notebooks/, { timeout: 120000 });
  await page.locator(".jp-MarkdownOutput h1").waitFor({ timeout: 120000 });
  dialog = await home(page);
  await ready(page);
  await page.locator('.ms-AppStatus[data-state="cannotCheck"]').waitFor();
  ok(
    "fresh offline launch, empty HTTP cache, old/deep links and previously unvisited Chapter 2 execute Python; answers retained",
  );
  await context.setOffline(false);
  onlineBrowser = await chromium.launch();
  onlineContext = await onlineBrowser.newContext({ viewport: { width: 390, height: 844 } });
  onlinePage = await onlineContext.newPage();
  await home(onlinePage);
  await onlinePage.evaluate(() => localStorage.setItem("work", "online-only work"));
  // Publish a genuine second artifact, keeping a test payload deliberately unavailable first.
  const commitB = releaseA.commit;
  for (const path of [
    "index.html",
    "jupyterlite/notebooks/index.html",
    "jupyterlite/tree/index.html",
  ]) {
    const html = (await readFile(join(site, path), "utf8")).replaceAll(releaseA.commit, commitB);
    await writeFile(join(site, path), html);
  }
  await writeFile(
    join(site, "jupyterlite/release.json"),
    JSON.stringify({ ...releaseA, commit: commitB }),
  );
  await writeFile(join(site, "app-status-test.txt"), "Release B required asset");
  execFileSync("node", ["scripts/build-offline.mjs", site], { stdio: "pipe" });
  const releaseB = JSON.parse(await readFile(join(site, "release.json"), "utf8"));
  assert.notEqual(releaseB.build, releaseA.build);
  ok(`built releases ${releaseA.build} → ${releaseB.build}, same source commit ${commitB}`);
  const next = JSON.parse(await readFile(join(site, "offline-manifest.json"), "utf8"));
  await writeFile(join(site, "app-status-test.txt"), "Wrong bytes");
  await dialog.getByRole("button", { name: "Check for updates", exact: true }).click();
  await page.locator('.ms-AppStatus[data-state="updateAvailable"]').waitFor();
  await dialog.getByRole("button", { name: "Update", exact: true }).click();
  await settled(page);
  await dialog.getByText(/Could not complete the download/).waitFor();
  await ready(page);
  await context.setOffline(true);
  await chapter(page, 3);
  await context.setOffline(false);
  ok("checksum mismatch rejects replacement and leaves previous complete Python course usable");
  dialog = await home(page);
  await page.evaluate(() => {
    window.realCachePut = Cache.prototype.put;
    Cache.prototype.put = async () => {
      throw new DOMException("Test quota", "QuotaExceededError");
    };
  });
  await dialog.getByRole("button", { name: "Update", exact: true }).click();
  await settled(page);
  await dialog.getByText(/Could not complete the download/).waitFor();
  await ready(page);
  await page.evaluate(() => {
    Cache.prototype.put = window.realCachePut;
  });
  ok("storage failure retains the previous complete copy and offers retry");
  await writeFile(join(site, "app-status-test.txt"), "Release B required asset");
  await chapter(page, 1);
  const other = await context.newPage();
  await chapter(other, 2);
  await other.evaluate(() => (window.keepOtherTab = "open"));
  const homeTab = await context.newPage();
  await home(homeTab);
  await homeTab.evaluate(() => (window.keepHome = "open"));
  await page.bringToFront();
  dialog = await open(page);
  await dialog.getByRole("button", { name: "Update", exact: true }).click();
  await settled(page);
  await dialog.getByRole("button", { name: "Restart to update", exact: true }).waitFor();
  assert.equal(await page.locator('meta[name="ms-build"]').getAttribute("content"), releaseA.build);
  await dialog.getByRole("button", { name: "Later", exact: true }).click();
  assert.match(await page.locator(".ms-AppStatus").innerText(), /Update ready/);
  assert.equal(await other.evaluate(() => window.keepOtherTab), "open");
  // Before restart, both tabs must still read release A's exact HTML from the worker.
  assert.match(
    await other.evaluate(
      async (u) => (await fetch(u)).text(),
      base + "jupyterlite/notebooks/index.html",
    ),
    new RegExp(releaseA.build),
  );
  await page.evaluate(
    async ({ base, version }) => {
      await (
        await caches.open(`ms:metadata-systems:offline:${base}:${version}`)
      ).delete(new URL("app-status-test.txt", base).href);
    },
    { base, version: next.version },
  );
  dialog = await open(page);
  await dialog.getByRole("button", { name: "Update", exact: true }).waitFor();
  await dialog.getByRole("button", { name: "Update", exact: true }).click();
  await settled(page);
  await dialog.getByRole("button", { name: "Restart to update", exact: true }).waitFor();
  ok("eviction of a deferred update removes false readiness and repairs it while retaining A");
  dialog = await open(page);
  await page.evaluate(() => {
    window.realWorkerUpdate = ServiceWorkerRegistration.prototype.update;
    ServiceWorkerRegistration.prototype.update = async () => {
      throw Error("activation test failure");
    };
  });
  await dialog.getByRole("button", { name: "Restart to update", exact: true }).click();
  await dialog
    .getByText("Could not restart with the update. This tab has not reloaded. Try again.", {
      exact: true,
    })
    .waitFor();
  assert.equal(await page.locator('meta[name="ms-build"]').getAttribute("content"), releaseA.build);
  await page.evaluate(() => {
    ServiceWorkerRegistration.prototype.update = window.realWorkerUpdate;
  });
  // Interrupt a restart after its async verification begins. The old document must not
  // acquire B's pin when newly unsafe work prevents the final reload.
  await page.evaluate(() => {
    window.realCacheMatch = Cache.prototype.match;
    window.pauseSelect = true;
    Cache.prototype.match = async function (request, options) {
      const url = typeof request === "string" ? request : request.url;
      if (window.pauseSelect && url.endsWith("pyodide.asm.wasm")) {
        window.pauseSelect = false;
        window.selectWaiting = true;
        await new Promise((resolve) => (window.releaseSelect = resolve));
      }
      return window.realCacheMatch.call(this, request, options);
    };
  });
  await dialog.getByRole("button", { name: "Restart to update", exact: true }).click();
  await page.waitForFunction(() => window.selectWaiting);
  await page
    .locator(".ms-Example")
    .first()
    .evaluate((n) => (n.dataset.unsaved = "true"));
  await page.evaluate(() => window.releaseSelect());
  await dialog
    .getByText("Could not restart with the update. This tab has not reloaded. Try again.", {
      exact: true,
    })
    .waitFor();
  assert.equal(await page.locator('meta[name="ms-build"]').getAttribute("content"), releaseA.build);
  assert.match(
    await page.evaluate(
      async (u) => (await fetch(u)).text(),
      base + "jupyterlite/notebooks/index.html",
    ),
    new RegExp(releaseA.build),
  );
  await page.evaluate(() => {
    Cache.prototype.match = window.realCacheMatch;
  });
  await page
    .locator(".ms-Example")
    .first()
    .evaluate((n) => delete n.dataset.unsaved);
  const sample = page.locator(".ms-Example").first();
  await sample.evaluate((n) => (n.dataset.unsaved = "true"));
  await page.waitForFunction(() => document.querySelector(".ms-AppStatus-dialog button") !== null);
  await page.waitForTimeout(600);
  assert(await dialog.getByRole("button", { name: "Restart to update", exact: true }).isDisabled());
  await sample.evaluate((n) => delete n.dataset.unsaved);
  await dialog.getByRole("button", { name: "Close App status", exact: true }).click();
  const busyEditor = sample.locator(".cm-content");
  const retainedCode = await busyEditor.innerText();
  await busyEditor.click();
  await busyEditor.press("ControlOrMeta+a");
  await page.keyboard.insertText("import time\ntime.sleep(3)");
  await sample.getByRole("button", { name: "Run", exact: true }).click();
  dialog = await open(page);
  await page.waitForTimeout(600);
  assert(await dialog.getByRole("button", { name: "Restart to update", exact: true }).isDisabled());
  await page.waitForFunction(
    () =>
      ![...document.querySelectorAll(".ms-AppStatus-dialog button")].find(
        (n) => n.textContent === "Restart to update",
      )?.disabled,
    null,
    { timeout: 30000 },
  );
  await dialog.getByRole("button", { name: "Close App status", exact: true }).click();
  await busyEditor.click();
  await busyEditor.press("ControlOrMeta+a");
  await page.keyboard.insertText(retainedCode);
  dialog = await open(page);
  await page.evaluate(() => document.dispatchEvent(new CompositionEvent("compositionstart")));
  assert(await dialog.getByRole("button", { name: "Restart to update", exact: true }).isDisabled());
  await page.evaluate(() => document.dispatchEvent(new CompositionEvent("compositionend")));
  await dialog.getByRole("button", { name: "Restart to update", exact: true }).click();
  await page.waitForFunction(
    (c) => document.querySelector('meta[name="ms-build"]')?.content === c,
    releaseB.build,
    { timeout: 180000 },
  );
  await page.locator('.ms-AppStatus[data-state="upToDate"]').waitFor({ timeout: 120000 });
  assert.equal(await other.evaluate(() => window.keepOtherTab), "open");
  assert.equal(await homeTab.evaluate(() => window.keepHome), "open");
  assert.match(
    await other.evaluate(
      async (u) => (await fetch(u)).text(),
      base + "jupyterlite/notebooks/index.html",
    ),
    new RegExp(releaseA.build),
  );
  assert.equal(
    await page.locator('textarea[data-answer="ch01.daily_sales"]').inputValue(),
    "Saved while offline",
  );
  assert.match(await page.locator(".ms-Example .cm-content").first().innerText(), /Retained code/);
  await context.setOffline(true);
  assert.equal(
    await page.evaluate(async (u) => (await fetch(u)).text(), base + "app-status-test.txt"),
    "Release B required asset",
  );
  ok(
    "detect → verified download → Later → explicit restart → new running identity, retained answers/code, route and other tabs pinned to A",
  );
  // An originally online-only tab must also get an actionable, deferred update. It must
  // not offer Resume as a shortcut that selects the prepared release before Restart.
  const onlineDialog = await open(onlinePage);
  await onlineDialog.getByRole("button", { name: "Check for updates", exact: true }).click();
  await onlineDialog.getByRole("button", { name: "Update", exact: true }).click();
  await settled(onlinePage);
  await onlineDialog.getByRole("button", { name: "Restart to update", exact: true }).waitFor();
  assert.equal(
    await onlineDialog.getByRole("button", { name: "Resume download", exact: true }).isVisible(),
    false,
  );
  assert.equal(
    await onlinePage.locator('meta[name="ms-build"]').getAttribute("content"),
    releaseA.build,
  );
  await onlineDialog.getByRole("button", { name: "Later", exact: true }).click();
  await open(onlinePage);
  await onlineDialog.getByRole("button", { name: "Restart to update", exact: true }).click();
  await onlinePage.waitForFunction(
    (c) => document.querySelector('meta[name="ms-build"]')?.content === c,
    releaseB.build,
    { timeout: 180000 },
  );
  assert.equal(await onlinePage.evaluate(() => localStorage.getItem("work")), "online-only work");
  ok(
    "online-only update prepares without restarting or publishing via Resume, then explicitly restarts with work retained",
  );
  assert.equal(
    await other.evaluate(
      async ({ base, version }) => {
        const cache = await caches.open(`ms:metadata-systems:offline:${base}:${version}`);
        const url = new URL("jupyterlite/notebooks/index.html", base).href;
        const retained = await cache.match(url);
        await cache.delete(url);
        const response = await fetch(url, { cache: "no-store" });
        await cache.put(url, retained);
        return response.status;
      },
      { base, version: first.version },
    ),
    409,
  );
  ok("an evicted pinned asset fails safely instead of fetching a newer release");
  await other.close();
  await homeTab.close();
  await context.setOffline(false);
  // Eviction is detected on focus and repaired with verified reuse, not an old success flag.
  await page.evaluate(
    async ({ base, version, path }) => {
      await (
        await caches.open(`ms:metadata-systems:offline:${base}:${version}`)
      ).delete(new URL(path, base).href);
    },
    { base, version: next.version, path: "app-status-test.txt" },
  );
  dialog = await open(page);
  await dialog.getByText("Offline download incomplete", { exact: true }).waitFor();
  await dialog.getByRole("button", { name: "Resume download", exact: true }).click();
  await ready(page);
  await settled(page);
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
  await dialog.getByRole("button", { name: "Remove offline copy", exact: true }).click();
  await dialog.getByRole("button", { name: "Keep offline copy", exact: true }).click();
  await ready(page);
  await dialog.getByRole("button", { name: "Remove offline copy", exact: true }).click();
  await dialog.getByRole("button", { name: "Remove offline copy", exact: true }).last().click();
  await dialog.getByText("Not saved for offline use", { exact: true }).waitFor();
  assert.equal(
    await page.evaluate(() =>
      localStorage.getItem("ms:metadata-systems:answers:v1:ch01.daily_sales"),
    ),
    "Saved while offline",
  );
  assert.equal(await page.evaluate(() => localStorage.getItem("user-imported-file")), "keep");
  assert.deepEqual(await savedNotebook(), notebookBefore);
  assert(await page.evaluate(() => caches.has("another-project")));
  assert(await page.evaluate(() => navigator.serviceWorker.getRegistration("/unrelated/")));
  ok("eviction/repair and confirmed scoped removal preserve answers, code and sibling app storage");
} finally {
  await onlineContext?.close();
  await onlineBrowser?.close();
  await context?.close();
  server.kill();
  for (const [path, bytes] of originals) await writeFile(join(site, path), bytes);
  await rm(join(site, "app-status-test.txt"), { force: true });
  await rm(temp, { recursive: true, force: true });
}
