// Copyright © 2026 Christopher Snow

// Opens the built JupyterLite site in Chromium as a phone, with touch, and presses the row of
// buttons (notebook/buttons/) as the chapters' texts tell a reader to. For each chapter: the menu
// bar and the notebook's toolbar are hidden; the row shows the labels buttons.json gives, each
// button at least 44 pixels tall, and arrows to the chapters either side, which open in a new tab,
// the row fitting 360 pixels, with a link to the contents between them from 390 pixels wide; a
// press disables the row and marks the pressed button busy until the run ends; Run all runs every
// visible code cell, with no error in any output, and leaves the notebook where it was scrolled;
// the warning and the steps for running the page are boxes, and from Chapter 2 the requirement the
// chapter questions is one too, in a colour of its own; in Chapter 1 a printed file keeps one
// record per line, scrolling inside its box, and the page never scrolls sideways. In Chapter 2, Run
// below from a selected cell does the same. In Chapter 3 the reader's record, typed in, passes its
// check, and in Chapter 4 the merge, typed in, leaves the model's check 3 problems; in Chapters 10
// to 22 each chapter's change to a cell gives its result. A browser set to dark gets the dark
// theme, and one set to light the light. The page logs no error, and the notebooks' earlier names
// lead to their chapters. The notebook workflow runs it after the build, with Playwright from the
// course's dependencies.
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

  const chapters = [
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26,
    27, 28, 29, 30, 31, 32, 33,
  ];
  // SMOKE_CHAPTERS=24,25 drives only those chapters, for a quick run while writing them; CI drives all.
  const only = (process.env.SMOKE_CHAPTERS || "").split(",").filter(Boolean).map(Number);
  for (const chapter of chapters.filter((c) => !only.length || only.includes(c))) {
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
    // The arrows to the chapters either side: none before the first chapter or after the last,
    // each 44 pixels tall, and the row fits a phone 360 pixels wide without scrolling.
    const stemOf = (n) => `chapter_${String(n).padStart(2, "0")}.ipynb`;
    const expected = [
      chapter > chapters[0] && `Previous: Chapter ${chapter - 1}|${stemOf(chapter - 1)}`,
      chapter < chapters.at(-1) && `Next: Chapter ${chapter + 1}|${stemOf(chapter + 1)}`,
    ].filter(Boolean);
    await page
      .waitForFunction(
        (n) => document.querySelectorAll(".ms-Buttons-link:not(.ms-Buttons-contents)").length === n,
        expected.length,
        { timeout: 10_000 },
      )
      .catch(() => {});
    await page.setViewportSize({ width: 360, height: 800 });
    await page.waitForTimeout(300);
    const arrows = await page.evaluate(() => {
      const bar = document.querySelector(".ms-Buttons");
      return {
        links: [...bar.querySelectorAll(".ms-Buttons-link:not(.ms-Buttons-contents)")].map((a) => ({
          name: `${a.getAttribute("aria-label")}|${new URL(a.href).searchParams.get("path")}`,
          height: a.getBoundingClientRect().height,
          tab: a.target,
        })),
        fits: bar.scrollWidth <= bar.clientWidth,
        contents: bar.querySelector(".ms-Buttons-contents")?.getBoundingClientRect().width ?? -1,
      };
    });
    // From 390 pixels wide, a link to the contents between the arrows, which opens the course's
    // front page in a new tab: an icon below 600 pixels and the word from there, the row fitting at
    // every width; at 360 it does not show.
    for (const [width, word] of [
      [390, false],
      [500, false],
      [600, true],
    ]) {
      await page.setViewportSize({ width, height: 900 });
      await page.waitForTimeout(300);
      const shown = await page.evaluate(() => {
        const bar = document.querySelector(".ms-Buttons");
        const links = [...bar.querySelectorAll(".ms-Buttons-link")];
        const at = links.findIndex((a) => a.classList.contains("ms-Buttons-contents"));
        const link = links[at];
        const visible = (sel) => link.querySelector(sel).getBoundingClientRect().width > 0;
        return link
          ? {
              name: link.getAttribute("aria-label"),
              word: visible(".ms-Buttons-contents-text"),
              icon: visible(".ms-Buttons-contents-icon"),
              to: new URL(link.href).pathname,
              tab: link.target,
              height: link.getBoundingClientRect().height,
              between:
                links.slice(0, at).every((a) => a.classList.contains("ms-Buttons-previous")) &&
                links.slice(at + 1).every((a) => a.classList.contains("ms-Buttons-next")),
              fits: bar.scrollWidth <= bar.clientWidth,
            }
          : null;
      });
      check(
        shown?.name === "Back to contents" &&
          shown.word === word &&
          shown.icon === !word &&
          shown.to === "/" &&
          shown.tab === "_blank" &&
          shown.height >= 44 &&
          shown.between &&
          shown.fits,
        `Chapter ${chapter}: at ${width} pixels wide, the contents link (${word ? "its word" : "an icon"}) between the arrows opens the front page in a new tab, and the row fits (${JSON.stringify(shown)})`,
      );
    }
    await page.setViewportSize({ width: 390, height: 844 });
    await page.waitForTimeout(300);
    check(
      arrows.contents === 0,
      `Chapter ${chapter}: at 360 pixels wide, the contents link does not show`,
    );
    check(
      JSON.stringify(arrows.links.map((a) => a.name)) === JSON.stringify(expected) &&
        arrows.links.every((a) => a.height >= 44 && a.tab === "_blank"),
      `Chapter ${chapter}: the arrows lead to ${expected.map((e) => e.split("|")[0]).join(" and ")}, in a new tab`,
    );
    check(arrows.fits, `Chapter ${chapter}: at 360 pixels wide the row fits without scrolling`);
    if (chapter === 1) {
      const opened = page.context().waitForEvent("page", { timeout: 30_000 });
      await page.locator(".ms-Buttons-next").tap();
      const next = await opened;
      await next.waitForFunction(() => document.querySelector(".jp-MarkdownOutput h1"), null, {
        timeout: 120_000,
      });
      const heading = await next.locator(".jp-MarkdownOutput h1").first().textContent();
      check(
        heading.startsWith("Chapter 2:") && page.url().endsWith(stemOf(1)),
        "Chapter 1: its Next arrow opens Chapter 2 in a new tab",
      );
      await next.close();
    }
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
    // The warning and the steps are boxes, drawn by the course's stylesheet; from Chapter 2, so is
    // the requirement the chapter questions, in a colour of its own. The notebook draws only the
    // cells near the view, so the page is scrolled through to find every box.
    const boxes = await page.evaluate(async () => {
      const outer = document.querySelector(".jp-WindowedPanel-outer");
      const kept = outer.scrollTop;
      const found = new Map();
      for (let y = 0; y <= outer.scrollHeight; y += 400) {
        outer.scrollTop = y;
        await new Promise((r) => setTimeout(r, 60));
        for (const b of document.querySelectorAll(".jp-RenderedMarkdown .ms-box")) {
          const style = getComputedStyle(b);
          found.set(b.textContent.trim().slice(0, 60), {
            name: b.className.replace("ms-box ", ""),
            tinted: style.backgroundColor !== "rgba(0, 0, 0, 0)",
            edge: style.borderLeftColor,
          });
        }
      }
      outer.scrollTop = kept;
      return [...found.values()];
    });
    const named = (name) => boxes.filter((b) => b.name === name);
    check(
      named("ms-box-warning").length === 1 &&
        named("ms-box-steps").length === 1 &&
        boxes.every((b) => b.tinted),
      `Chapter ${chapter}: the warning and the steps are boxes (${boxes.map((b) => b.name).join("; ")})`,
    );
    const requirement = named("ms-box-requirement");
    check(
      // Chapter 33 questions three of the ferry's requirements, each before building to it.
      requirement.length === (chapter === 33 ? 3 : chapter > 1 ? 1 : 0) &&
        requirement.every((r) => boxes.filter((b) => b.edge === r.edge).length === 1),
      `Chapter ${chapter}: ${chapter > 1 ? "the requirement is a box in a colour of its own" : "no requirement box"}`,
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
      // In the middle of the screen: a cell scrolled only just into view can sit under the row of
      // buttons, which stays at the top, and a tap there misses the editor.
      await cell.evaluate((e) => e.scrollIntoView({ block: "center" }));
      await page.waitForTimeout(300);
      const editor = await cell.$(".cm-content");
      // Near its first character: a long line makes the editor wider than the phone's screen, and
      // its centre can fall outside it.
      await editor.tap({ position: { x: 8, y: 8 } });
      await page.keyboard.press("ControlOrMeta+a");
      const text = (await editor.innerText()).replace(/\u00a0/g, " ");
      const changed = from.reduce((t, f, i) => t.replaceAll(f, to[i]), text);
      await page.keyboard.insertText(changed);
      const typed = (await editor.innerText()).replace(/\u00a0/g, " ");
      check(
        to.every((t) => typed.includes(t)),
        `the edit to the cell with ${JSON.stringify(hasText)} is in its editor`,
      );
      await (await cell.$(".jp-InputPrompt")).tap();
    };
    // The output of the first code cell holding `hasText`, or of a later one, counted from 0.
    const output = async (hasText, nth = 0) => {
      const cell = page
        .locator(".jp-CodeCell", { has: page.locator(".jp-InputArea", { hasText }) })
        .nth(nth);
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
    if (chapter === 14) {
      await rewrite(
        'dataset = "clean_orders"',
        ['dataset = "clean_orders"'],
        ['dataset = "orders.jsonl"'],
      );
      await run("Run below", "Chapter 14, Run below on the file");
      // Found by code the edit leaves as it was: text just typed in may not be drawn yet.
      const failed = await output("shop.quality.check(week14, dataset");
      check(
        (failed.match(/\tno$/gm) ?? []).length === 4,
        "Chapter 14: on the file, the assertion fails on 4 runs",
      );
    }
    if (chapter === 15) {
      await rewrite("dropped=False", ["dropped=False"], ["dropped=True"]);
      await run("Run below", "Chapter 15, Run below with the rows left out");
      const left = await output("dropped=");
      check(
        left.includes("customer_id IS NOT NULL is false"),
        "Chapter 15: the trace lists the rows left out",
      );
      await rewrite("as_read=False", ["as_read=False"], ["as_read=True"]);
      await run("Run below", "Chapter 15, Run below with returns as it was");
      const read = await output("as_read=");
      check(
        read.includes("rebuilt as at 2026-09-14T02:30:00Z"),
        "Chapter 15: returns is rebuilt as it was",
      );
    }
    if (chapter === 16) {
      await rewrite("downstream_columns", ['"customer_id"'], ['"status"']);
      await run("Run below", "Chapter 16, Run below for status");
      const down = await output("downstream_columns");
      check(
        down.includes("filter in build_daily_sales"),
        "Chapter 16: status decides the rows of daily_sales",
      );
    }
    if (chapter === 17) {
      await rewrite('day = "2026-09-12"', ['day = "2026-09-12"'], ['day = "2026-09-08"']);
      await run("Run below", "Chapter 17, Run below for Tuesday");
      const tuesday = await output("shop.cause.search(week17r, day)");
      check(
        tuesday.includes("16225") && !tuesday.includes("21549"),
        "Chapter 17: Tuesday's figure is the same at every step",
      );
    }
    // Part V: each chapter's change to a cell, and the result its text states.
    if (chapter === 18) {
      await rewrite("again = shop.delivery.send", ["lose=["], ["lose_ack=["]);
      await run("Run below", "Chapter 18, Run below with the acknowledgement lost");
      const again = await output("again.retried()");
      check(
        again.includes("2026-09-12T16:50:07Z") && again.includes("2026-09-12T16:50:37Z"),
        "Chapter 18: with the acknowledgement lost, the COMPLETE arrives twice",
      );
    }
    if (chapter === 19) {
      await rewrite("shop.ingest.dedupe(retimed.events", ['"content"'], ['"run"']);
      await run("Run below", "Chapter 19, Run below by run");
      const dropped = await output("shop.ingest.dedupe(retimed.events");
      check(
        dropped.includes("02:30:52"),
        "Chapter 19: by run, the retry with a new time is dropped",
      );
    }
    if (chapter === 20) {
      await rewrite("late.until(", ['order="event"'], ['order="arrival"']);
      await run("Run below", "Chapter 20, Run below by arrival");
      const last = await output("late.until(");
      check(
        last.includes("2026-09-09T02:30:21Z"),
        "Chapter 20: by arrival, daily_sales was last written a day earlier",
      );
      await rewrite("late.until(", ["26 * 3600"], ["20 * 3600"]);
      await run("Run below", "Chapter 20, Run below with a shorter hold-up");
      const shorter = await output("late.until(");
      check(
        shorter.includes("2026-09-10T02:30:21Z"),
        "Chapter 20: held up 20 hours, the last write by arrival is Thursday's",
      );
      await rewrite("shop.delivery.object_states(held.events", ['"arrival"'], ['"event"']);
      await run("Run below", "Chapter 20, Run below by event time");
      const states = await output("shop.delivery.object_states(held.events");
      check(/r-206\.json\tdeleted/.test(states), "Chapter 20: by event time, r-206 is deleted");
    }
    if (chapter === 21) {
      await rewrite("shop.claims.resolve(tuesday, rule)", ['rule = "as of"'], ['rule = "ranked"']);
      await run("Run below", "Chapter 21, Run below ranked");
      const ranked = await output("shop.claims.resolve(tuesday, rule)");
      check(
        ranked.includes("j.marsh") && ranked.includes("day, revenue_pence"),
        "Chapter 21: ranked, the owner is j.marsh and the columns the warehouse's",
      );
    }
    if (chapter === 22) {
      await rewrite("shop.aliases.merge(", ['"last part"'], ['"aliases"']);
      await run("Run below", "Chapter 22, Run below by aliases");
      const merged = await output("shop.aliases.merge(");
      check(
        merged.includes("warehouse, events, transformation tool, reporting tool"),
        "Chapter 22: by aliases, four references are one entity",
      );
    }
    // Part VI: each piece the reader writes, typed as the reference, and the check that then passes.
    if (chapter === 24) {
      await rewrite(
        "def readers_of(documents, dataset):",
        [
          'def readers_of(documents, dataset):\n    found = []\n    for doc in documents:\n        pass  # add doc["job"] when the document\'s "reads" lists the dataset\n    return found',
        ],
        [
          'def readers_of(documents, dataset):\n    found = []\n    for doc in documents:\n        if dataset in doc.get("reads", []):\n            found.append(doc["job"])\n    return found',
        ],
      );
      await run("Run below", "Chapter 24, Run below with the loop");
      const docs = await output("shop.store.check(week24, documents, readers_of)");
      check(
        docs.includes("11 of 11 datasets right; 187 documents read"),
        "Chapter 24: the loop is right, and reads 187 documents",
      );
      await rewrite(
        'query = "SELECT job FROM edges"',
        ['query = "SELECT job FROM edges"'],
        ["query = \"SELECT job FROM edges WHERE edge = 'reads' AND dataset = :dataset\""],
      );
      await run("Run below", "Chapter 24, Run below with the query");
      await rewrite(
        "CREATE INDEX edges_index ON edges(job)",
        ['tables.sql("CREATE INDEX edges_index ON edges(job)")'],
        ['tables.sql("CREATE INDEX edges_index ON edges(dataset)")'],
      );
      await run("Run below", "Chapter 24, Run below with the index");
      const indexed = await output("shop.store.check(week24, tables, query)", 1);
      check(
        indexed.includes("11 of 11 datasets right; 14 rows read in all"),
        "Chapter 24: with the index on dataset, the query reads 14 rows",
      );
      await rewrite(
        "def readers_of(graph, dataset):",
        ['def readers_of(graph, dataset):\n    return [e["job"] for e in graph.edges_at(dataset)]'],
        [
          'def readers_of(graph, dataset):\n    return [e["job"] for e in graph.edges_at(dataset) if e["edge"] == "reads"]',
        ],
      );
      await run("Run below", "Chapter 24, Run below with the graph");
      const graph = await output("shop.store.check(week24, shop.store.graph(week24), readers_of)");
      check(
        graph.includes("11 of 11 datasets right; 14 edges read"),
        "Chapter 24: the graph is right, and reads 14 edges",
      );
    }
    if (chapter === 25) {
      await rewrite(
        "def key(event):",
        ["return json.dumps(event, sort_keys=True)"],
        ['return (event["run"]["runId"], event["eventType"])'],
      );
      await run("Run below", "Chapter 25, Run below with the key");
      await rewrite(
        "def newer(event, current):",
        ["def newer(event, current):\n    return True"],
        ['def newer(event, current):\n    return event["eventTime"] >= current["eventTime"]'],
      );
      await run("Run below", "Chapter 25, Run below with newer");
      const five = await output("shop.collector.check(week25, key, newer)");
      check(five.includes("5 of 5 tests pass"), "Chapter 25: with key and newer, 5 of 5 pass");
      await rewrite(
        "def start(stored):",
        ["def start(stored):\n    return set()"],
        ["def start(stored):\n    return {key(event) for event in stored}"],
      );
      await run("Run below", "Chapter 25, Run below with start");
      const six = await output("shop.collector.check(week25, key, newer, start)");
      check(
        six.includes("6 of 6 tests pass"),
        "Chapter 25: with start, 6 of 6 pass after the restart",
      );
    }
    if (chapter === 26) {
      await rewrite(
        "def add(edges, event):",
        [
          'def add(edges, event):\n    for key in shop.lineage_graph.edges_of(event):\n        edge = edges.setdefault(key, {"runs": set(), "first": event["eventTime"], "last": event["eventTime"]})\n        edge["runs"].add(event["run"]["runId"])\n        edge["last"] = event["eventTime"]',
        ],
        [
          'def add(edges, event):\n    for key in shop.lineage_graph.edges_of(event):\n        edge = edges.setdefault(key, {"runs": set(), "first": event["eventTime"], "last": event["eventTime"]})\n        edge["runs"].add(event["run"]["runId"])\n        edge["first"] = min(edge["first"], event["eventTime"])\n        edge["last"] = max(edge["last"], event["eventTime"])',
        ],
      );
      await run("Run below", "Chapter 26, Run below with add");
      const three = await output("shop.lineage_graph.check(week26, add)");
      check(three.includes("3 of 3 tests pass"), "Chapter 26: with add, 3 of 3 pass");
    }
    if (chapter === 27) {
      await rewrite(
        "def downstream(graph, asset):",
        ["def downstream(graph, asset):\n    return shop.query.next_assets(graph, asset)"],
        [
          "def downstream(graph, asset):\n    found, todo = set(), [asset]\n    while todo:\n        for nxt in shop.query.next_assets(graph, todo.pop()):\n            if nxt not in found:\n                found.add(nxt)\n                todo.append(nxt)\n    return found",
        ],
      );
      await run("Run below", "Chapter 27, Run below with the traversal");
      const down = await output("shop.query.check_downstream(week27, downstream)");
      check(down.includes("3 of 3 tests pass"), "Chapter 27: the traversal finds all three");
      await rewrite(
        "def owner(asset):",
        ['def owner(asset):\n    return {"owner": shop.query.owners(asset)["account"]}'],
        [
          'def owner(asset):\n    return {"owner": shop.query.owners(asset)["responsible"], "meaning": "responsible"}',
        ],
      );
      await run("Run below", "Chapter 27, Run below with the owner");
      const own = await output("shop.query.check_owner(owner)");
      check(own.includes("1 of 1 tests pass"), "Chapter 27: the owner names its meaning");
    }
    if (chapter === 28) {
      await rewrite(
        "def run_history(asset):",
        [
          'def run_history(asset):\n    return [r for r in shop.interface.runs() if asset in r["writes"]]',
        ],
        [
          'def run_history(asset):\n    jobs = shop.interface.writers(asset)\n    return [r for r in shop.interface.runs() if r["job"] in jobs]',
        ],
      );
      await run("Run below", "Chapter 28, Run below with the run history");
      const history = await output("shop.interface.check(run_history)");
      check(
        history.includes("holds each of its 7 runs once"),
        "Chapter 28: the run history holds 7 runs, the failed one among them",
      );
    }
    if (chapter === 29) {
      await rewrite('order = "arrival"', ['order = "arrival"'], ['order = "event time"']);
      await run("Run below", "Chapter 29, Run below with the order");
      const friday = await output("shop.consumers.check(week29, order)");
      check(
        friday.includes("1 of 1 tests pass"),
        "Chapter 29: in event-time order, Friday 11's run agrees",
      );
    }
    if (chapter === 30) {
      await rewrite(
        'name_format = "$QUERY_ID"',
        [
          'name_format = "$QUERY_ID"',
          '"build_clean_customers": "shop-nightly"',
          '"build_clean_orders": "shop-nightly"',
          '"build_daily_sales": "shop-nightly"',
          '"refresh_dashboard": "shop-nightly"',
        ],
        [
          'name_format = "$SOURCE"',
          '"build_clean_customers": "clean-customers"',
          '"build_clean_orders": "clean-orders"',
          '"build_daily_sales": "daily-sales"',
          '"refresh_dashboard": "dashboard"',
        ],
      );
      await run("Run below", "Chapter 30, Run below with the name format");
      const jobs = await output("shop.integrations.check_trino(week30, name_format, source_of)");
      check(
        jobs.includes("2 of 2 tests pass"),
        "Chapter 30: one job for build_daily_sales, its runs only",
      );
    }
    if (chapter === 31) {
      await rewrite(
        "types = {",
        [
          '"account": "urn:li:ownershipType:__system__technical_owner"',
          '"responsible": "urn:li:ownershipType:__system__technical_owner"',
        ],
        [
          '"account": "urn:li:ownershipType:warehouse_account"',
          '"responsible": "urn:li:ownershipType:__system__business_owner"',
        ],
      );
      await run("Run below", "Chapter 31, Run below with the types");
      const types = await output("shop.platforms.check(types)");
      check(types.includes("2 of 2 tests pass"), "Chapter 31: three owners, three types");
    }
    if (chapter === 32) {
      await rewrite("where = ", ["2026-09-13"], ["2026-09-11"]);
      await run("Run below", "Chapter 32, Run below with the condition");
      const digest = await output("shop.ml.check(week32, where)");
      check(
        digest.includes("1 of 1 tests pass"),
        "Chapter 32: the rows up to Friday 11 give the run's digest",
      );
    }
    if (chapter === 33) {
      await rewrite(
        "def inputs(change):",
        [
          'def inputs(change):\n    batch = {"namespace": change["bucket"], "name": change["key"]}\n    if change["change"] == "deleted":\n        return []\n    return [batch]',
        ],
        [
          'def inputs(change):\n    batch = {"namespace": change["bucket"], "name": change["key"]}\n    if change["change"] == "deleted":\n        batch["facets"] = {"version": shop.ferry.version_facet(change["previous"])}\n    else:\n        batch["facets"] = {"version": shop.ferry.version_facet(change["version"])}\n    return [batch]',
        ],
      );
      await run("Run below", "Chapter 33, Run below with inputs");
      const inputs = await output("shop.ferry.check_inputs(platform, inputs)");
      check(inputs.includes("3 of 3 tests pass"), "Chapter 33: each run names the version it read");
      await rewrite(
        "def suspect(run):",
        ['def suspect(run):\n    return run["state"] == "FAIL"'],
        ['def suspect(run):\n    return run["scans_read"] > 0 and run["rows_written"] == 0'],
      );
      await run("Run below", "Chapter 33, Run below with suspect");
      const suspect = await output("shop.ferry.check_suspect(collected, suspect)");
      check(suspect.includes("2 of 2 tests pass"), "Chapter 33: Thursday's two runs, and no other");
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
