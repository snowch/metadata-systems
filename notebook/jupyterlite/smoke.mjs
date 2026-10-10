// Copyright © 2026 Christopher Snow

// Opens the built JupyterLite site in Chromium as a phone, with touch, and presses the row of
// buttons (notebook/buttons/) as the chapter's texts tell a reader to. For each part: the menu bar
// and the notebook's toolbar are hidden; the row shows the labels buttons.json gives, each button
// at least 44 pixels tall; a press disables the row and marks the pressed button busy until the
// run ends; Run all runs every visible code cell, with no error in any output, and leaves the
// notebook where it was scrolled. In part 2, Run below from a selected cell does the same. The page
// logs no error. The notebook workflow
// runs it after the build, with Playwright from the course's dependencies.
//
//   node notebook/jupyterlite/smoke.mjs SITE_DIR

import { spawn } from "node:child_process";
import { readFileSync } from "node:fs";
import { chromium } from "playwright";

const site = process.argv[2];
const port = 8765;
const labels = Object.values(
  JSON.parse(readFileSync(new URL("../buttons/buttons.json", import.meta.url), "utf8")),
);
const server = spawn("python3", ["-m", "http.server", String(port), "--bind", "127.0.0.1"], {
  cwd: site,
  stdio: "ignore",
});
const failures = [];
const check = (ok, what) => {
  console.log(`${ok ? "ok  " : "FAIL"} ${what}`);
  if (!ok) failures.push(what);
};

const browser = await chromium.launch();
try {
  for (let i = 0; ; i += 1) {
    const up = await fetch(`http://127.0.0.1:${port}/jupyter-lite.json`).then(
      (r) => r.ok,
      () => false,
    );
    if (up) break;
    if (i === 100) throw new Error("the site's server did not start");
    await new Promise((resolve) => setTimeout(resolve, 100));
  }
  const page = await browser.newPage({
    viewport: { width: 390, height: 844 },
    deviceScaleFactor: 2,
    isMobile: true,
    hasTouch: true,
  });
  const errors = [];
  page.on("pageerror", (e) => errors.push(e.message));
  page.on("console", (m) => m.type() === "error" && errors.push(m.text()));
  const button = (label) => page.locator(".ms-Buttons-button", { hasText: label });
  const scrolled = () =>
    page.evaluate(() => Math.round(document.querySelector(".jp-WindowedPanel-outer").scrollTop));
  // Presses a button, checks the row shows the run under way, waits for it to end, and checks the
  // notebook did not move.
  const run = async (label, what) => {
    const before = await scrolled();
    await button(label).tap();
    const busy = await page.evaluate((label) => {
      const row = [...document.querySelectorAll(".ms-Buttons-button")];
      const pressed = row.find((b) => b.textContent === label);
      return row.every((b) => b.disabled) && pressed?.getAttribute("aria-busy") === "true";
    }, label);
    check(busy, `${what}: the row is disabled and the button busy while it runs`);
    await page.waitForFunction(
      () =>
        !document.querySelector(".ms-Buttons-button[aria-busy], .ms-Buttons-button:disabled") &&
        ![...document.querySelectorAll(".jp-InputPrompt")].some((p) => p.textContent.includes("*")),
      null,
      { timeout: 120_000, polling: 200 },
    );
    check((await scrolled()) === before, `${what}: the notebook stays where it was scrolled`);
  };
  const shown = (selector) =>
    page.evaluate((selector) => {
      const e = document.querySelector(selector);
      return !!e && e.getBoundingClientRect().height > 0;
    }, selector);

  for (const part of [1, 2]) {
    await page.goto(
      `http://127.0.0.1:${port}/notebooks/index.html?path=chapter_01_part_${part}.ipynb`,
    );
    await page.waitForFunction(() => document.querySelector(".jp-MarkdownOutput h1"), null, {
      timeout: 120_000,
    });
    await page.waitForTimeout(1000);
    check(
      !(await shown("#menu-panel-wrapper")) && !(await shown(".jp-NotebookPanel-toolbar")),
      `part ${part}: the menu bar and the toolbar are hidden`,
    );
    const row = await page.evaluate(() =>
      [...document.querySelectorAll(".ms-Buttons-button")].map((b) => ({
        label: b.textContent,
        height: b.getBoundingClientRect().height,
      })),
    );
    check(
      JSON.stringify(row.map((b) => b.label)) === JSON.stringify(labels),
      `part ${part}: the row's buttons are ${labels.join(", ")}`,
    );
    check(
      row.every((b) => b.height >= 44),
      `part ${part}: every button is at least 44 pixels tall`,
    );
    await page.evaluate(() => {
      document.querySelector(".jp-WindowedPanel-outer").scrollTop = 300;
    });
    await run("Run all", `part ${part}, Run all`);
    const cells = await page.evaluate(() =>
      [...document.querySelectorAll(".jp-CodeCell")]
        .filter((c) => !c.querySelector(".jp-InputArea.lm-mod-hidden, .jp-Placeholder"))
        .map((c) => c.querySelector(".jp-InputPrompt")?.textContent.trim() ?? ""),
    );
    check(
      cells.length > 0 && cells.every((p) => /^\[\d+\]:$/.test(p)),
      `part ${part}: every visible code cell ran (${cells.length})`,
    );
    const failed = await page
      .locator(
        '[data-mime-type="application/vnd.jupyter.stderr"], .jp-OutputArea-output.jp-mod-error',
      )
      .count();
    check(failed === 0, `part ${part}: no output is an error`);
    if (part === 2) {
      const day = page.locator(".jp-CodeCell", { hasText: 'day = "2026-09-10"' }).first();
      await day.scrollIntoViewIfNeeded();
      await day.locator(".jp-InputPrompt").tap();
      await run("Run below", "part 2, Run below from the day's cell");
    }
  }
  check(errors.length === 0, `the page logs no error${errors.length ? `: ${errors[0]}` : ""}`);
} finally {
  await browser.close();
  server.kill();
}
if (failures.length) {
  console.error(`${failures.length} check(s) failed`);
  process.exit(1);
}
