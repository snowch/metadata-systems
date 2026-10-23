// Copyright © 2026 Christopher Snow

// Exercise the reading surface against the real Python runtime and native code editors.
import { checkPublishedUpdate, checkAnswerUpdate } from "./saved-work-smoke.mjs";
import { checkRelease } from "./release-smoke.mjs";
import { checkRetiredChapter } from "./redirect-smoke.mjs";
import { checkAutosave } from "./autosave-smoke.mjs";
import { checkNavigation } from "./navigation-smoke.mjs";
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
    await page.goto(`${base}/notebooks/index.html?path=chapter_01.ipynb`);
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
    await open();
    const reminder = page
      .locator(".jp-RenderedMarkdown")
      .getByText("Write your guesses now, before continuing to Chapter 2.", {
        exact: true,
      });
    await reminder.waitFor({ state: "attached" });
    await page.waitForSelector('textarea[data-answer="ch01.daily_sales"]', { state: "attached" });
    check(
      (await reminder.count()) === 1 &&
        (await page.locator('textarea[data-answer^="ch01."]').count()) === 3,
      "reader: the Chapter 2 carry-over reminder appears before all three original answer boxes",
    );
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
    const pipeline = page.locator(".ms-pipeline").first();
    for (const width of [360, 640, 800, 1280]) {
      await page.setViewportSize({ width, height: 844 });
      check(
        await pipeline.evaluate((node) => {
          const systems = [...node.querySelectorAll(".ms-system")];
          return (
            systems.every((system) =>
              [...system.querySelectorAll("code")].every((code) => {
                const rect = code.getBoundingClientRect();
                return (
                  code.getClientRects().length === 1 &&
                  rect.right <= system.getBoundingClientRect().right
                );
              }),
            ) &&
            [...node.querySelectorAll(".ms-flow")].every(
              (flow) => flow.textContent.trim() === "→",
            ) &&
            node.querySelectorAll(".ms-pipeline-key > span").length === 4
          );
        }),
        `reader: the ${width}px system diagram keeps names on one line and labels its icons once`,
      );
      await pipeline.screenshot({ path: `/tmp/metadata-pipeline-${width}.png` });
    }
    await page.setViewportSize({ width: 390, height: 844 });
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
    const ids = Object.keys(originals);
    for (const id of ids) {
      const setup =
        id === "products"
          ? '\nreader_order = ["products"]\nimport asyncio\nawait asyncio.sleep(0.25)'
          : `\nreader_order.append(${JSON.stringify(id)})`;
      const show = id === "daily_sales" ? "\nprint(reader_order)" : "";
      await edit(id, originals[id] + setup + show);
    }
    const answer = page.locator('textarea[data-answer="ch01.daily_sales"]');
    await answer.fill("My run all answer");
    const heading = page.getByRole("heading", { name: "The warehouse", exact: true });
    await heading.evaluate((node) => node.scrollIntoView({ block: "center" }));
    const top = (await heading.boundingBox()).y;
    await page.evaluate(() => {
      window.readerProgress = [];
      const node = document.querySelector(".ms-Reader-progress");
      new MutationObserver(() => window.readerProgress.push(node.textContent)).observe(node, {
        childList: true,
        subtree: true,
        characterData: true,
      });
    });
    const all = page.getByRole("button", { name: "Run all", exact: true });
    await all.click();
    check(
      (await all.isDisabled()) &&
        (await example("orders").getByRole("button", { name: "Reset example" }).isDisabled()) &&
        (await page.getByRole("button", { name: "Download code", exact: true }).isEnabled()),
      "reader: Run all prevents overlapping runs and resets while keeping code export available",
    );
    await page
      .getByText("All examples finished successfully.", { exact: true })
      .waitFor({ timeout: 120_000 });
    check(
      (await example("daily_sales").locator(".jp-OutputArea").innerText()).includes(
        "['products', 'customers', 'orders', 'clean_customers', 'clean_orders', 'daily_sales']",
      ),
      "reader: Run all executes edited examples sequentially in document order",
    );
    check(
      await page.evaluate(
        () =>
          window.readerProgress.some((text) => text.includes("1/6")) &&
          window.readerProgress.some((text) => text.includes("5/6")),
      ),
      "reader: Run all reports completed-example progress",
    );
    check(
      Math.abs((await heading.boundingBox()).y - top) <= 3 &&
        (await answer.inputValue()) === "My run all answer" &&
        (await read("products")).includes("reader_order"),
      "reader: Run all preserves the reader's place, edited code and exercise answers",
    );
    const oldResult = await example("clean_customers").locator(".jp-OutputArea").innerText();
    await edit("orders", "this is not valid Python !!!");
    await edit("clean_customers", originals.clean_customers + '\nprint("SHOULD_NOT_RUN")');
    await all.click();
    await page
      .getByText("Run all stopped at The orders. See the error below that example.", {
        exact: true,
      })
      .waitFor({ timeout: 120_000 });
    check(
      (await example("orders").locator(".jp-OutputArea").innerText()).includes("SyntaxError") &&
        (await example("clean_customers").locator(".jp-OutputArea").innerText()) === oldResult &&
        (await example("clean_customers").locator(".ms-Example-status").innerText()).includes(
          "Not run because an earlier example failed",
        ) &&
        (await all.isEnabled()),
      "reader: Run all stops at the first error, labels skipped results and releases the controls",
    );
    for (const id of ids) await example(id).getByRole("button", { name: "Reset example" }).click();

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

    await page.locator('textarea[data-answer="ch01.daily_sales"]').fill("My Chapter 1 answer");
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
        "My Chapter 1 answer",
      "reader: Chapter 2 recalls the same exercise answers from Chapter 1",
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
          const navigation = document.querySelector(".ms-Reader-nav");
          return (
            outer.scrollWidth <= outer.clientWidth + 1 &&
            navigation.scrollWidth <= navigation.clientWidth + 1 &&
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
    await page.goto(`${base}/notebooks/index.html?path=chapter_01.ipynb`);
    await page.waitForSelector('.ms-Example[data-example="daily_sales"]', { timeout: 120_000 });
    const last = page.locator('[data-example="daily_sales"]');
    await page.getByRole("button", { name: "Run all", exact: true }).click();
    await page
      .getByText("Waiting for Python. Examples will run in order when it is ready.", {
        exact: true,
      })
      .waitFor();
    check(
      await page.locator('[data-example="products"] [data-reader-action="run"]').isDisabled(),
      "reader: queued Run all prevents overlapping runs while Python loads",
    );
    const editor = page.locator('[data-example="orders"] .cm-content');
    await editor.fill((await editor.innerText()).replace("2026-09-07", "2026-09-10"));
    release();
    await page
      .getByText("All examples finished successfully.", { exact: true })
      .waitFor({ timeout: 120_000 });
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
    await checkRelease(browser, `http://127.0.0.1:8866${standalone ? "" : "/jupyterlite"}`);
    await checkPublishedUpdate(browser, `http://127.0.0.1:8866${standalone ? "" : "/jupyterlite"}`);
    await checkAnswerUpdate(
      chromium,
      `http://127.0.0.1:8866${standalone ? "" : "/jupyterlite"}`,
      resolve(process.argv[2], standalone ? "" : "jupyterlite"),
    );
    await checkRetiredChapter(browser, `http://127.0.0.1:8866${standalone ? "" : "/jupyterlite"}`);
    await checkReader(
      browser,
      `http://127.0.0.1:8866${standalone ? "" : "/jupyterlite"}`,
      (passed, description) => {
        console.log(`${passed ? "ok" : "FAIL"} ${description}`);
        assert(passed, description);
      },
    );
    await checkNavigation(browser, `http://127.0.0.1:8866${standalone ? "" : "/jupyterlite"}`);
    await checkAutosave(browser, `http://127.0.0.1:8866${standalone ? "" : "/jupyterlite"}`);
  } finally {
    await browser.close();
    server.kill();
  }
}
