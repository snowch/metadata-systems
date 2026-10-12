// Copyright © 2026 Christopher Snow

// Opens the built JupyterLite site in Chromium as a phone, with touch, and presses the row of
// buttons (notebook/buttons/) as the chapters' texts tell a reader to. For each chapter: the menu bar
// and the notebook's toolbar are hidden; the row shows the labels buttons.json gives, each button
// at least 44 pixels tall; a press disables the row and marks the pressed button busy until the
// run ends; Run all runs every visible code cell, with no error in any output, and leaves the
// notebook where it was scrolled; the warning and the steps for running the page are boxes; in
// Chapter 1 a printed file keeps one record per line, scrolling inside its box, and the page never
// scrolls sideways. In Chapter 2, Run below from a selected cell does the same. In Chapter 3 the
// reader's record, typed in, passes its check, and in Chapter 4 the merge, typed in, leaves the
// model's check 3 problems. A browser set to dark gets the dark theme, and one set to light the
// light. The page
// logs no error, and the notebooks' earlier names lead to their chapters. The notebook workflow
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

  for (const chapter of [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]) {
    const stem = `chapter_${String(chapter).padStart(2, "0")}`;
    await page.goto(`http://127.0.0.1:${port}/notebooks/index.html?path=${stem}.ipynb`);
    await page.waitForFunction(() => document.querySelector(".jp-MarkdownOutput h1"), null, {
      timeout: 120_000,
    });
    await page.waitForTimeout(1000);
    check(
      !(await shown("#menu-panel-wrapper")) && !(await shown(".jp-NotebookPanel-toolbar")),
      `Chapter ${chapter}: the menu bar and the toolbar are hidden`,
    );
    const row = await page.evaluate(() =>
      [...document.querySelectorAll(".ms-Buttons-button")].map((b) => ({
        label: b.textContent,
        height: b.getBoundingClientRect().height,
      })),
    );
    check(
      JSON.stringify(row.map((b) => b.label)) === JSON.stringify(labels),
      `Chapter ${chapter}: the row's buttons are ${labels.join(", ")}`,
    );
    check(
      row.every((b) => b.height >= 44),
      `Chapter ${chapter}: every button is at least 44 pixels tall`,
    );
    // The figures are in Markdown cells, drawn when the site was built: they show before anything
    // runs, with no code cell for any of them, and the week's words are readable on a phone.
    const figures = await page.evaluate(async () => {
      const outer = document.querySelector(".jp-WindowedPanel-outer");
      const found = new Map();
      for (let y = 0; y <= outer.scrollHeight; y += 400) {
        outer.scrollTop = y;
        await new Promise((r) => setTimeout(r, 60));
        for (const f of document.querySelectorAll(".jp-RenderedMarkdown figure.ms-figure")) {
          const caption = f.querySelector("figcaption").textContent;
          const img = f.querySelector("img.ms-svg");
          found.set(caption, {
            shown: f.getBoundingClientRect().height > 40,
            image: img ? img.complete && img.naturalWidth > 0 : null,
            width: img ? img.getBoundingClientRect().width : null,
          });
        }
      }
      outer.scrollTop = 0;
      const stubs = [...document.querySelectorAll(".jp-CodeCell")].filter((c) =>
        c.textContent.includes("figures."),
      ).length;
      return { figures: [...found.values()], stubs };
    });
    check(
      figures.figures.length === ({ 1: 3, 2: 2, 7: 2 }[chapter] ?? 1) &&
        figures.figures.every((f) => f.shown && f.image !== false) &&
        figures.stubs === 0,
      `Chapter ${chapter}: its ${figures.figures.length} figures show before anything runs, with no code cell`,
    );
    if (chapter === 1) {
      // On a phone 360 pixels wide, the narrowest common width, the week's 14-unit text in its
      // 340-unit drawing must show at 11 pixels or more.
      await page.setViewportSize({ width: 360, height: 800 });
      await page.waitForTimeout(300);
      const width = await page.evaluate(() => {
        const img = document.querySelector("img.ms-svg");
        img.scrollIntoView();
        return img.getBoundingClientRect().width;
      });
      const size = (14 * width) / 340;
      check(
        size >= 11,
        `Chapter 1: at 360 pixels wide the week's words show at ${size.toFixed(1)} pixels`,
      );
      // No name set as code in the text breaks across two lines, and none runs past the page.
      const names = await page.evaluate(async () => {
        const outer = document.querySelector(".jp-WindowedPanel-outer");
        const broken = new Set();
        let wide = false;
        for (let y = 0; y <= outer.scrollHeight; y += 400) {
          outer.scrollTop = y;
          await new Promise((r) => setTimeout(r, 60));
          for (const c of document.querySelectorAll(".jp-RenderedMarkdown :not(pre) > code")) {
            if (c.getClientRects().length > 1) broken.add(c.textContent);
          }
          wide ||= document.documentElement.scrollWidth > document.documentElement.clientWidth;
        }
        outer.scrollTop = 0;
        return { broken: [...broken], wide };
      });
      check(
        names.broken.length === 0 && !names.wide,
        `Chapter 1: at 360 pixels wide no name in the text breaks across lines${names.broken.length ? `: ${names.broken.join(", ")}` : ""}`,
      );
      await page.setViewportSize({ width: 390, height: 844 });
      await page.waitForTimeout(300);
    }
    await page.evaluate(() => {
      document.querySelector(".jp-WindowedPanel-outer").scrollTop = 300;
    });
    await run("Run all", `Chapter ${chapter}, Run all`);
    const cells = await page.evaluate(() =>
      [...document.querySelectorAll(".jp-CodeCell")]
        .filter((c) => !c.querySelector(".jp-InputArea.lm-mod-hidden, .jp-Placeholder"))
        .map((c) => c.querySelector(".jp-InputPrompt")?.textContent.trim() ?? ""),
    );
    check(
      cells.length > 0 && cells.every((p) => /^\[\d+\]:$/.test(p)),
      `Chapter ${chapter}: every visible code cell ran (${cells.length})`,
    );
    const failed = await page
      .locator(
        '[data-mime-type="application/vnd.jupyter.stderr"], .jp-OutputArea-output.jp-mod-error',
      )
      .count();
    check(failed === 0, `Chapter ${chapter}: no output is an error`);
    // The warning and the steps are boxes, drawn by the course's stylesheet.
    const boxes = await page.evaluate(() =>
      [...document.querySelectorAll(".jp-RenderedMarkdown .ms-box")].map((b) => ({
        name: b.className,
        tinted: getComputedStyle(b).backgroundColor !== "rgba(0, 0, 0, 0)",
      })),
    );
    check(
      boxes.length === 2 && boxes.every((b) => b.tinted),
      `Chapter ${chapter}: the warning and the steps are boxes (${boxes.map((b) => b.name).join("; ")})`,
    );
    if (chapter === 1) {
      // A printed file keeps one record per line: the line scrolls inside its box, and the page
      // does not scroll sideways.
      const printed = page
        .locator(".jp-CodeCell")
        .filter({ has: page.locator(".jp-InputArea", { hasText: "customers.jsonl" }) })
        .first();
      await printed.scrollIntoViewIfNeeded();
      const lines = await printed.evaluate((cell) => {
        const pre = cell.querySelector('[data-mime-type="application/vnd.jupyter.stdout"] pre');
        if (!pre) return null;
        // The lines as drawn: the distinct tops of the text's line boxes.
        const range = document.createRange();
        range.selectNodeContents(pre);
        const tops = new Set(
          [...range.getClientRects()].filter((r) => r.width > 0).map((r) => Math.round(r.top)),
        );
        return {
          records: pre.textContent.trim().split("\n").length,
          shown: tops.size,
          scrolls: pre.scrollWidth > pre.clientWidth,
        };
      });
      check(
        lines !== null && lines.records === lines.shown && lines.scrolls,
        `Chapter 1: a printed file keeps one record per line, scrolling inside its box (${JSON.stringify(lines)})`,
      );
      const sideways = await page.evaluate(
        () => document.documentElement.scrollWidth > document.documentElement.clientWidth,
      );
      check(!sideways, "Chapter 1: the page does not scroll sideways");
    }
    // After a run, with every output and control drawn, the page still fits a phone 360 pixels
    // wide: nothing in the notebook, a collapsed cell's first line included, scrolls it sideways.
    await page.setViewportSize({ width: 360, height: 800 });
    const sideways = await page.evaluate(async () => {
      const outer = document.querySelector(".jp-WindowedPanel-outer");
      const before = outer.scrollTop;
      let wide = false;
      for (let y = 0; y <= outer.scrollHeight; y += 400) {
        outer.scrollTop = y;
        await new Promise((r) => setTimeout(r, 60));
        wide ||= document.documentElement.scrollWidth > document.documentElement.clientWidth;
        wide ||= outer.scrollWidth > outer.clientWidth;
      }
      outer.scrollTop = before;
      return wide;
    });
    check(
      !sideways,
      `Chapter ${chapter}: after Run all, at 360 pixels wide, the page does not scroll sideways`,
    );
    await page.setViewportSize({ width: 390, height: 844 });
    await page.waitForTimeout(300);
    if (chapter === 2) {
      const day = page.locator(".jp-CodeCell", { hasText: 'day = "2026-09-10"' }).first();
      await day.scrollIntoViewIfNeeded();
      await day.locator(".jp-InputPrompt").tap();
      await run("Run below", "Chapter 2, Run below from the day's cell");
    }
    // Chapters 3 to 5 ask the reader to change a cell and press Run below: the record's dots in
    // Chapter 3, two spellings in Chapter 4, a direction in Chapter 5. Typed as a reader would.
    const rewrite = async (hasText, from, to) => {
      // Held as an element: once its text changes, a locator by its text would find nothing.
      const cell = await page
        .locator(".jp-CodeCell", { has: page.locator(".jp-InputArea", { hasText }) })
        .first()
        .elementHandle();
      await cell.scrollIntoViewIfNeeded();
      const editor = await cell.$(".cm-content");
      // Near its first character: a long line makes the editor wider than the phone's screen, and
      // its centre can fall outside it.
      await editor.tap({ position: { x: 8, y: 8 } });
      await page.keyboard.press("ControlOrMeta+a");
      const text = (await editor.innerText()).replace(/\u00a0/g, " ");
      await page.keyboard.insertText(from.reduce((t, f, i) => t.replaceAll(f, to[i]), text));
      await (await cell.$(".jp-InputPrompt")).tap();
    };
    const output = async (hasText) => {
      const cell = page
        .locator(".jp-CodeCell", { has: page.locator(".jp-InputArea", { hasText }) })
        .first();
      await cell.scrollIntoViewIfNeeded();
      await page.waitForTimeout(300);
      return cell.locator(".jp-OutputArea").innerText();
    };
    if (chapter === 3) {
      await rewrite(
        "daily_sales means: ........",
        [
          "daily_sales means: ........",
          "responsible: ........",
          "day means: ........",
          "revenue_pence means: ........",
          "unit: ........",
        ],
        [
          "daily_sales means: the value of every completed order",
          "responsible: Jo Marsh",
          "day means: the UTC date",
          "revenue_pence means: the value of the day's completed orders",
          "unit: pence",
        ],
      );
      await run("Run below", "Chapter 3, Run below from the record");
      const checked = await output('records.check(warehouse, "daily_sales")');
      check(
        checked.includes("No problems found."),
        `Chapter 3: the filled record passes its check (${checked.slice(0, 60)})`,
      );
      const who = await output("field = 'responsible'");
      check(who.includes("Jo Marsh"), "Chapter 3: the record names Jo Marsh");
    }
    if (chapter === 5) {
      const before = await output('graph.traverse("j.marsh"');
      check(
        before.includes("sales_dashboard"),
        "Chapter 5: against its arrows, the traversal from j.marsh reaches the dashboard",
      );
      await rewrite('graph.traverse("j.marsh"', ['"responsible": "in"'], ['"responsible": "out"']);
      await run("Run below", "Chapter 5, Run below from the traversal");
      const after = await output('graph.traverse("j.marsh"');
      check(
        after.includes("No rows."),
        `Chapter 5: along its arrows, it reaches no node (${after.slice(0, 40)})`,
      );
    }
    if (chapter === 6) {
      const walk = await output('lineage.downstream("s3://shop-raw/orders.jsonl")');
      check(
        walk.includes("sales_dashboard"),
        "Chapter 6: downstream of orders.jsonl reaches the dashboard",
      );
    }
    if (chapter === 7) {
      await rewrite("lineage = shop.lineage", ['"reads", "writes"'], ['"writes"']);
      await run("Run below", "Chapter 7, Run below without reads");
      const up = await output("lineage = shop.lineage");
      check(
        up.includes("refresh_dashboard") && !up.includes("orders.jsonl"),
        "Chapter 7: without reads, the traversal stops at refresh_dashboard",
      );
    }
    if (chapter === 8) {
      await rewrite(
        '"eventType": "START"',
        ['"name": "analytics.clean_orders"'],
        ['"name": "shop.analytics.clean_orders"'],
      );
      await run("Run below", "Chapter 8, Run below with the jobs' name");
      const up = await output("joined = shop.openlineage");
      check(
        up.includes("orders.jsonl"),
        "Chapter 8: with one name for the table, the traversal reaches orders.jsonl",
      );
    }
    if (chapter === 9) {
      await rewrite(
        "known = dict(",
        ['# known["shop_objectChange"]'],
        ['known["shop_objectChange"]'],
      );
      await run("Run below", "Chapter 9, Run below with the facet known");
      const unknown = await output("objs.unknown");
      check(
        unknown.includes("The stage knows every facet in the events."),
        "Chapter 9: with the facet known, no facet is unknown",
      );
    }
    if (chapter === 10) {
      await rewrite("catalogue = None", ["# catalogue = warehouse"], ["catalogue = warehouse"]);
      await run("Run below", "Chapter 10, Run below with the catalogue");
      const named = await output("catalogue = None");
      check(
        named.includes("daily_sales.revenue_pence") && !named.includes("column 1"),
        "Chapter 10: with the catalogue, the parser names daily_sales's columns",
      );
    }
    if (chapter === 11) {
      await rewrite('column = "quantity"', ['column = "quantity"'], ['column = "customer_id"']);
      await run("Run below", "Chapter 11, Run below for customer_id");
      const readers = await output("shop.schemas.readers");
      check(
        readers.includes("customer_id") && readers.includes("build_clean_orders"),
        "Chapter 11: build_clean_orders reads customer_id",
      );
    }
    if (chapter === 12) {
      await rewrite(
        "databases = {}",
        ["# databases[shop.openlineage.DEV_PRODUCER]"],
        ["databases[shop.openlineage.DEV_PRODUCER]"],
      );
      await run("Run below", "Chapter 12, Run below with a database for each producer");
      const parted = await output("databases = {}");
      check(
        parted.includes("shop_dev.analytics.daily_sales"),
        "Chapter 12: the development run writes shop_dev's daily_sales",
      );
    }
    if (chapter === 13) {
      await rewrite('by="stores"', ['by="stores"'], ['by="runs"']);
      await run("Run below", "Chapter 13, Run below by the runs' clock");
      const chain = await output('by="runs"');
      check(
        chain.includes("03:00:09"),
        "Chapter 13: by the runs' clock, the refresh finished at 03:00:09",
      );
    }
    if (chapter === 4) {
      await rewrite(
        "dataset daily_sales means:",
        ["responsible: Jo Marsh", "responsible: Sam Lund"],
        ["responsible: j.marsh", "responsible: s.lund"],
      );
      await run("Run below", "Chapter 4, Run below from the records");
      const problems = (await output("model.check(records)"))
        .split("\n")
        .filter((l) => /^\d+\t/.test(l)).length;
      check(problems === 3, `Chapter 4: after the merge the check lists 3 problems (${problems})`);
      if (problems !== 3) console.log((await output("model.check(records)")).slice(0, 400));
    }
  }
  check(errors.length === 0, `the page logs no error${errors.length ? `: ${errors[0]}` : ""}`);
  // The notebooks follow the reader's light or dark setting (overrides.json).
  for (const scheme of ["dark", "light"]) {
    const other = await browser.newContext({
      viewport: { width: 390, height: 844 },
      isMobile: true,
      hasTouch: true,
      colorScheme: scheme,
    });
    const themed = await other.newPage();
    await themed.goto(`http://127.0.0.1:${port}/notebooks/index.html?path=chapter_01.ipynb`);
    await themed.waitForFunction(() => document.body.dataset.jpThemeLight !== undefined, null, {
      timeout: 120_000,
    });
    const light = await themed.evaluate(() => document.body.dataset.jpThemeLight);
    check(
      light === String(scheme === "light"),
      `a browser set to ${scheme} gets the ${scheme} theme`,
    );
    await other.close();
  }
  // The notebooks' earlier names lead to their chapters. Each is looked up first, which can log
  // that the file is missing, so this comes after the check for errors.
  await page.goto(`http://127.0.0.1:${port}/notebooks/index.html?path=chapter_01_part_2.ipynb`);
  await page.waitForURL(/path=chapter_02\.ipynb/, { timeout: 60_000 }).catch(() => {});
  check(
    page.url().endsWith("path=chapter_02.ipynb"),
    "an earlier notebook name leads to its chapter",
  );
} finally {
  await browser.close();
  server.kill();
}
if (failures.length) {
  console.error(`${failures.length} check(s) failed`);
  process.exit(1);
}
