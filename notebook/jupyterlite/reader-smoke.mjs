// Copyright © 2026 Christopher Snow

// Exercise the reading surface against the real Python runtime and native code editors.
import assert from "node:assert/strict";
import { spawn } from "node:child_process";
import { pathToFileURL } from "node:url";
import { resolve } from "node:path";
import { existsSync } from "node:fs";
import { chromium } from "playwright";

export async function checkReader(browser, base, check) {
  const context = await browser.newContext({
    viewport: { width: 390, height: 844 },
    colorScheme: "dark",
  });
  const page = await context.newPage();
  const errors = [];
  page.on("pageerror", (error) => {
    const detail = error.stack || String(error);
    console.log("reader browser error", detail);
    errors.push(detail);
  });
  const open = async () => {
    await page.goto(`${base}/notebooks/index.html?path=chapter_01b.ipynb`);
    await page.waitForSelector('.ms-Example[data-example="daily_sales"]', { timeout: 120_000 });
  };
  const example = (id) => page.locator(`.ms-Example[data-example="${id}"]`);
  const code = (id) => example(id).locator(".cm-content");
  const read = (id) => code(id).innerText();
  const edit = async (id, source) => {
    const editor = code(id);
    await editor.fill(source);
  };
  const run = async (id, keyboard = false) => {
    const cell = example(id);
    if (keyboard) await code(id).press("Shift+Enter");
    else await cell.getByRole("button", { name: "Run", exact: true }).click();
    await page.waitForFunction(
      () => !document.querySelector('[data-reader-action="run"]:disabled'),
      null,
      { timeout: 120_000 },
    );
    check(
      (await cell.locator(".ms-Example-status").innerText()) === "Example finished.",
      `reader: ${id} runs with its output immediately below the editor`,
    );
    check((await cell.locator(".jp-mod-error").count()) === 0, `reader: ${id} has no Python error`);
  };
  try {
    const published = await Promise.all(
      ["chapter_01.ipynb", "chapter_01b.ipynb"].map(async (file) =>
        (await fetch(`${base}/files/${file}`)).json(),
      ),
    );
    const examplesOf = (nb) =>
      nb.cells
        .filter((cell) => cell.cell_type === "code" && !cell.metadata.ms?.setup)
        .map((cell) => cell.source);
    check(
      JSON.stringify(examplesOf(published[0])) === JSON.stringify(examplesOf(published[1])),
      "reader: comparison examples are identical to the original Chapter 1",
    );
    await open();
    assert.equal(await page.locator(".ms-Example").count(), 6);
    check(
      (await page.locator(".ms-Buttons > [data-action]").count()) === 0,
      "reader: the chapter has per-example controls and no notebook Run all/Run below/Save row",
    );
    check(
      !(await page.locator("#jp-top-bar").isVisible()) &&
        (await page.locator(".ms-Reader .jp-cell-toolbar:visible").count()) === 0,
      "reader: notebook document chrome and cell management controls are hidden",
    );
    const originals = Object.fromEntries(
      await Promise.all(
        ["products", "customers", "orders", "clean_customers", "clean_orders", "daily_sales"].map(
          async (id) => [id, await read(id)],
        ),
      ),
    );
    await edit("orders", originals.orders.replace("2026-09-07", "2026-09-10"));
    await example("daily_sales").getByRole("button", { name: "Run", exact: true }).click();
    await edit("products", originals.products + "\n# My saved change");
    await page.waitForFunction(
      () => !document.querySelector('[data-reader-action="run"]:disabled'),
      null,
      { timeout: 120_000 },
    );
    check(
      (await example("daily_sales").locator("tbody tr").count()) === 7,
      "reader: the last example runs first after automatic setup",
    );
    // Neither changed example has been run or explicitly saved before refreshing.
    await page.reload();
    await page.waitForSelector('.ms-Example[data-example="daily_sales"]', { timeout: 120_000 });
    check(
      (await read("orders")).includes("2026-09-10") &&
        (await read("products")).includes("My saved change"),
      "reader: code edits survive immediate refresh before their first execution",
    );
    check(
      (await page.locator(".ms-Example .jp-OutputArea-output").count()) === 0,
      "reader: refresh clears old results while retaining code",
    );
    await run("orders", true);
    check(
      (await example("orders").locator("tbody tr").count()) === 7,
      "reader: Shift+Enter runs only the edited example, showing Thursday's seven raw orders",
    );
    await edit("orders", "this is not valid Python !!!");
    await example("orders")
      .getByText("The code has changed. Run again to update the result.", { exact: true })
      .waitFor();
    await example("orders").getByRole("button", { name: "Run", exact: true }).click();
    await example("orders")
      .getByText("The example stopped with an error. See the details below.", { exact: true })
      .waitFor({ timeout: 120_000 });
    check(
      (await example("orders").locator(".jp-OutputArea-output").innerText()).includes(
        "SyntaxError",
      ),
      "reader: an invalid edit shows an inline error and releases the controls",
    );
    await example("orders").getByRole("button", { name: "Reset example" }).click();
    check(
      (await read("orders")) === originals.orders &&
        (await example("orders").locator(".jp-OutputArea-output").count()) === 0 &&
        (await read("products")).includes("My saved change"),
      "reader: Reset restores only its example and clears its result",
    );
    for (const id of Object.keys(originals)) await run(id);

    const h1 = page.locator(".jp-MarkdownOutput h1");
    await h1.dblclick();
    const count = await page.locator(".jp-Cell").count();
    await page.keyboard.press("Escape");
    await page.keyboard.type("ddb");
    check(
      (await h1.isVisible()) &&
        (await page.locator(".jp-Cell").count()) === count &&
        (await page.locator(".jp-MarkdownCell .cm-content:visible").count()) === 0,
      "reader: prose stays rendered and notebook shortcuts cannot delete or insert cells",
    );

    // Deny persistent writes without changing the editor or replacing Python.
    await page.evaluate(() => {
      const set = Storage.prototype.setItem;
      Storage.prototype.setItem = function (key, value) {
        if (key.startsWith("ms:metadata-systems:code:"))
          throw new DOMException("Storage full", "QuotaExceededError");
        return set.call(this, key, value);
      };
    });
    await edit("products", originals.products + "\n# Unsaved export copy");
    await example("products")
      .getByText("Your edits are not saved. Copy the code before leaving this page.", {
        exact: true,
      })
      .waitFor();
    const downloaded = page.waitForEvent("download");
    await page.getByRole("button", { name: "Download code", exact: true }).click();
    const stream = await (await downloaded).createReadStream();
    const chunks = [];
    for await (const chunk of stream) chunks.push(chunk);
    check(
      Buffer.concat(chunks).toString().includes("Unsaved export copy"),
      "reader: storage failure is visible and Download code retains the live draft",
    );

    await page.locator('textarea[data-answer="ch01.daily_sales"]').fill("My comparison answer");
    await page.goto(`${base}/notebooks/index.html?path=chapter_02.ipynb`);
    await page.waitForSelector(".jp-Notebook .jp-Cell", { timeout: 120_000 });
    // The normal chapter still windows distant cells.
    await page.evaluate(async () => {
      const outer = document.querySelector(".jp-WindowedPanel-outer");
      for (let y = 0; y < outer.scrollHeight; y += 500) {
        outer.scrollTop = y;
        await new Promise((resolve) => setTimeout(resolve, 40));
        if (document.querySelector('textarea[data-answer="ch01.daily_sales"]')) return;
      }
    });
    check(
      (await page.locator('textarea[data-answer="ch01.daily_sales"]').first().inputValue()) ===
        "My comparison answer",
      "reader: Chapter 2 recalls the same exercise answers from Chapter 1b",
    );
    await open();
    for (const width of [360, 1280]) {
      await page.setViewportSize({ width, height: 844 });
      await page.emulateMedia({ colorScheme: width === 360 ? "dark" : "light" });
      await page.waitForFunction(
        (light) => document.body.dataset.jpThemeLight === String(light),
        width !== 360,
      );
      check(
        await page.evaluate(() => {
          const outer = document.querySelector(".jp-WindowedPanel-outer");
          const controls = [
            ...document.querySelectorAll(".ms-Example button, .ms-Reader-nav button"),
          ];
          return (
            outer.scrollWidth <= outer.clientWidth + 1 &&
            controls.every((button) => button.getBoundingClientRect().height >= 44)
          );
        }),
        `reader: ${width}px layout fits the screen and controls are at least 44px tall`,
      );
      await page.screenshot({ path: `/tmp/metadata-reader-${width}.png` });
    }
    check(errors.length === 0, `reader: no browser error (${errors.join("; ")})`);
  } catch (error) {
    console.log(
      await page
        .evaluate(() => ({
          startup: document.querySelector(".ms-Startup")?.textContent,
          examples: [...document.querySelectorAll(".ms-Example-status")].map(
            (node) => node.textContent,
          ),
          errors: [...document.querySelectorAll(".jp-mod-error")].map((node) => node.textContent),
        }))
        .catch(() => null),
    );
    await page.screenshot({ path: "/tmp/metadata-reader-failure.png" }).catch(() => {});
    throw error;
  } finally {
    await context.close();
  }
  await checkQueuedReader(browser, base, check);
}

// Like startup-smoke.mjs, this isolated context blocks service workers so Playwright can delay
// the worker's actual WebAssembly request. All ordinary flows and browser-error checks above
// run with real service workers enabled, including the complete published build's root worker.
async function checkQueuedReader(browser, base, check) {
  const context = await browser.newContext({
    serviceWorkers: "block",
    viewport: { width: 390, height: 844 },
  });
  let release;
  const gate = new Promise((resolve) => (release = resolve));
  await context.route("**/pyodide.asm.wasm", async (route) => {
    await gate;
    await route.continue().catch(() => {});
  });
  try {
    const page = await context.newPage();
    await page.goto(`${base}/notebooks/index.html?path=chapter_01b.ipynb`);
    await page.waitForSelector('.ms-Example[data-example="daily_sales"]', { timeout: 120_000 });
    const last = page.locator('[data-example="daily_sales"]');
    await last.getByRole("button", { name: "Run", exact: true }).click();
    await last
      .getByText("Waiting for Python. This example will run when it is ready.", { exact: true })
      .waitFor();
    check(
      await page.locator('[data-example="products"] [data-reader-action="run"]').isDisabled(),
      "reader: a queued run prevents overlapping runs while Python loads",
    );
    const editor = page.locator('[data-example="orders"] .cm-content');
    await editor.fill((await editor.innerText()).replace("2026-09-07", "2026-09-10"));
    release();
    await page.waitForFunction(
      () => !document.querySelector('[data-reader-action="run"]:disabled'),
      null,
      { timeout: 120_000 },
    );
    check(
      (await last.locator("tbody tr").count()) === 7 &&
        (await editor.innerText()).includes("2026-09-10"),
      "reader: queued execution finishes and keeps edits made during startup",
    );
  } finally {
    release();
    await context.close();
  }
}

if (process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href) {
  const standalone = existsSync(resolve(process.argv[2], "jupyter-lite.json"));
  const server = spawn("python3", ["-m", "http.server", "8866", "--bind", "127.0.0.1"], {
    cwd: process.argv[2],
    stdio: "ignore",
  });
  const browser = await chromium.launch();
  try {
    for (let i = 0; i < 100; i++) {
      if (
        await fetch(
          `http://127.0.0.1:8866/${standalone ? "" : "jupyterlite/"}jupyter-lite.json`,
        ).then(
          (r) => r.ok,
          () => false,
        )
      )
        break;
      await new Promise((resolve) => setTimeout(resolve, 100));
    }
    await checkReader(
      browser,
      `http://127.0.0.1:8866${standalone ? "" : "/jupyterlite"}`,
      (passed, description) => {
        console.log(`${passed ? "ok" : "FAIL"} ${description}`);
        assert(passed, description);
      },
    );
  } finally {
    await browser.close();
    server.kill();
  }
}
