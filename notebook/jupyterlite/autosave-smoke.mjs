// Copyright © 2026 Christopher Snow

import assert from "node:assert/strict";
import { chromium } from "playwright";
import { pathToFileURL } from "node:url";
import { resolve } from "node:path";

export async function checkAutosave(browser, base) {
  const page = await browser.newPage();
  try {
    // Shorten only Jupyter's actual background-save timer, leaving Python, editor and
    // navigation timing unchanged. The default interval is two minutes.
    await page.addInitScript(() => {
      const original = window.setTimeout.bind(window);
      window.setTimeout = (callback, delay, ...args) =>
        original(
          callback,
          delay >= 120000 && String(callback).includes("_save") ? 2000 : delay,
          ...args,
        );
    });
    await page.goto(`${base}/notebooks/index.html?path=chapter_01.ipynb`);
    for (const number of [1, 2]) {
      await page.waitForSelector(
        '.ms-Startup[data-phase="ready"],.ms-Startup[data-phase="hidden"]',
        { state: "attached", timeout: 120000 },
      );
      const example = page.locator(".ms-Example").first();
      await example.locator(".cm-content").fill(`print("My chapter ${number} draft")`);
      // Model a newer notebook written by another open tab. A background whole-file save
      // would raise File Changed or overwrite this sentinel; neither belongs in the reader.
      const path = `chapter_0${number}.ipynb`;
      const content = await (await fetch(`${base}/files/${path}`)).json();
      content.metadata.ms.externalConflict = true;
      await page.evaluate(
        async ({ path, content }) => {
          const { name } = (await indexedDB.databases()).find((db) =>
            db.name.startsWith("JupyterLite Storage"),
          );
          const db = await new Promise((resolve) => {
            const request = indexedDB.open(name);
            request.onsuccess = () => resolve(request.result);
          });
          const transaction = db.transaction("files", "readwrite");
          const future = new Date(Date.now() + 60000).toISOString();
          transaction.objectStore("files").put(
            {
              name: path,
              path,
              type: "notebook",
              format: "json",
              content,
              writable: true,
              created: future,
              last_modified: future,
              mimetype: null,
            },
            path,
          );
          await new Promise((resolve, reject) => {
            transaction.oncomplete = resolve;
            transaction.onerror = reject;
          });
          db.close();
        },
        { path, content },
      );
      await page.waitForTimeout(5000);
      assert.equal(
        await page.getByRole("dialog").count(),
        0,
        `Chapter ${number}: no File Changed dialog`,
      );
      assert.equal(
        await page.evaluate(async (path) => {
          const { name } = (await indexedDB.databases()).find((db) =>
            db.name.startsWith("JupyterLite Storage"),
          );
          const db = await new Promise((resolve) => {
            const request = indexedDB.open(name);
            request.onsuccess = () => resolve(request.result);
          });
          const saved = await new Promise((resolve) => {
            const request = db.transaction("files").objectStore("files").get(path);
            request.onsuccess = () => resolve(request.result);
          });
          db.close();
          return saved.content.metadata.ms.externalConflict;
        }, path),
        true,
        "the newer notebook must not be overwritten",
      );
      assert.equal(
        await example.locator(".cm-content").innerText(),
        `print("My chapter ${number} draft")`,
      );
      if (number === 1) {
        await page
          .locator('textarea[data-answer="ch01.daily_sales"]')
          .fill("My answer remains saved");
        await page.locator(".ms-Buttons-next").click();
        await page.waitForURL(/path=chapter_02.ipynb/);
      }
    }
    await page.goto(`${base}/notebooks/index.html?path=chapter_01.ipynb`);
    await page.waitForSelector(".ms-Example .cm-content", { timeout: 120000 });
    assert.equal(
      await page.locator(".ms-Example").first().locator(".cm-content").innerText(),
      'print("My chapter 1 draft")',
    );
    await page.waitForSelector('textarea[data-answer="ch01.daily_sales"]', { state: "attached" });
    assert.equal(
      await page.locator('textarea[data-answer="ch01.daily_sales"]').inputValue(),
      "My answer remains saved",
    );
    console.log(
      "ok autosave: conflicting notebook files do not interrupt initial or navigated chapters; drafts and answers survive refresh",
    );
  } finally {
    await page.close();
  }
}
if (process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href) {
  const browser = await chromium.launch();
  try {
    await checkAutosave(browser, process.argv[2]);
  } finally {
    await browser.close();
  }
}
