// Copyright © 2026 Christopher Snow

// The look of the page, held to rules a reader needs: no visible text under 11 pixels, every
// control at least 40 pixels tall on a phone, no line of prose much over 85 characters, and a map
// of the platform whose names stay whole and whose systems stay even at every width.

import { expect, test } from "@playwright/test";

import { CHAPTER, openChapter } from "./helpers";

for (const where of ["#/", `#/chapter/${CHAPTER.id}`]) {
  test(`no visible text under 11 pixels on ${where}`, async ({ page }) => {
    await page.goto(where);
    await page.evaluate(async () => {
      await document.fonts.ready;
    });
    const small = await page.evaluate(() => {
      const out: string[] = [];
      const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
      for (let n = walker.nextNode(); n; n = walker.nextNode()) {
        const text = n.textContent?.trim();
        const el = n.parentElement;
        if (!text || !el) continue;
        const style = getComputedStyle(el);
        const r = el.getBoundingClientRect();
        if (
          style.visibility === "hidden" ||
          style.display === "none" ||
          r.width === 0 ||
          r.height === 0
        )
          continue;
        if (el.closest(".visually-hidden, [hidden]")) continue;
        if (parseFloat(style.fontSize) < 11)
          out.push(`${parseFloat(style.fontSize)}px: ${text.slice(0, 40)}`);
      }
      return out;
    });
    expect(small).toEqual([]);
  });
}

test("every control is at least 40 pixels tall on a phone", async ({ page, isMobile }) => {
  test.skip(!isMobile, "the rule is for touch");
  await openChapter(page);
  const short = await page.evaluate(() => {
    const out: string[] = [];
    const controls = document.querySelectorAll(
      "button, select, summary, a.button, .prediction-option, .fault-choice, .shell-header nav a",
    );
    for (const el of controls) {
      const r = el.getBoundingClientRect();
      if (r.width === 0 || r.height === 0) continue;
      if (r.height < 40)
        out.push(
          `${Math.round(r.height)}px: ${el.tagName} ${(el.textContent ?? "").trim().slice(0, 40)}`,
        );
    }
    return out;
  });
  expect(short).toEqual([]);
});

test("no line of prose is much over 85 characters", async ({ page, isMobile }) => {
  test.skip(isMobile, "a phone's lines are shorter");
  await openChapter(page);
  const long = await page.evaluate(() => {
    const out: string[] = [];
    for (const p of document.querySelectorAll(".prose p, .prose li")) {
      const style = getComputedStyle(p);
      const lineHeight = parseFloat(style.lineHeight);
      const lines = Math.round(p.getBoundingClientRect().height / lineHeight);
      const text = (p.textContent ?? "").trim();
      if (lines < 3) continue;
      // The text's length over its full lines: the last line is on average half full.
      const perLine = text.length / (lines - 0.5);
      if (perLine > 88) out.push(`${Math.round(perLine)}: ${text.slice(0, 40)}`);
    }
    return out;
  });
  expect(long).toEqual([]);
});

test("the map keeps every name whole at every width, and its systems even", async ({
  page,
  isMobile,
}) => {
  test.skip(isMobile, "the test sets each width itself");
  await openChapter(page);
  for (const width of [320, 360, 390, 480, 560, 600, 640, 700, 768, 800, 834, 1024, 1280]) {
    await page.setViewportSize({ width, height: 900 });
    const found = await page.evaluate(() => {
      const map = document.querySelector("#ix-platform .platform-map");
      if (!map) return { problems: ["no map"], row: false, widths: [] as number[] };
      const problems: string[] = [];
      const systems = [...map.querySelectorAll(".map-system")];
      for (const s of systems) {
        const box = s.getBoundingClientRect();
        const assets = [...s.querySelectorAll(".map-asset")];
        for (const a of assets) {
          const name = a.querySelector("span");
          if (!name) continue;
          const r = name.getBoundingClientRect();
          if (r.height > parseFloat(getComputedStyle(name).lineHeight) * 1.5)
            problems.push(`${name.textContent} breaks`);
          if (r.right > box.right - 1) problems.push(`${name.textContent} leaves its box`);
        }
        // One name to a line, or all on one line: never a line of two over a line of one.
        const lines = new Set(assets.map((a) => Math.round(a.getBoundingClientRect().top))).size;
        if (lines !== 1 && lines !== assets.length)
          problems.push(`${s.querySelector(".map-system-name")?.textContent} mixes lines`);
      }
      const tops = systems.map((s) => Math.round(s.getBoundingClientRect().top));
      return {
        problems,
        row: new Set(tops).size === 1,
        widths: systems.map((s) => Math.round(s.getBoundingClientRect().width)),
      };
    });
    expect(found.problems, `at ${width} pixels`).toEqual([]);
    // In a row, the systems share one width, whichever has an arrow beside it.
    if (found.row) expect(new Set(found.widths).size, `at ${width} pixels`).toBe(1);
    if (width >= 1024) expect(found.row, `at ${width} pixels`).toBe(true);
    if (width <= 480) expect(found.row, `at ${width} pixels`).toBe(false);
  }
});

test("the map's button never covers the page's foot on a phone", async ({ page, isMobile }) => {
  test.skip(isMobile, "the test sets each width itself");
  await openChapter(page);
  for (const width of [320, 360, 375, 390, 414]) {
    await page.setViewportSize({ width, height: 800 });
    await page.evaluate(() => window.scrollTo(0, document.documentElement.scrollHeight));
    await expect(page.locator(".map-dock")).toBeVisible();
    const covered = await page.evaluate(() => {
      const dock = document.querySelector(".map-dock")!.getBoundingClientRect();
      const out: string[] = [];
      for (const p of document.querySelectorAll(".shell-footer p, .pager, .start-again")) {
        const range = document.createRange();
        range.selectNodeContents(p);
        for (const r of range.getClientRects())
          if (
            r.right > dock.left &&
            r.left < dock.right &&
            r.bottom > dock.top &&
            r.top < dock.bottom
          )
            out.push((p.textContent ?? "").trim().slice(0, 30));
      }
      return out;
    });
    expect(covered, `at ${width} pixels`).toEqual([]);
  }
});

test("a challenge's choices fill their rows: never three and one left over", async ({
  page,
  isMobile,
}) => {
  test.skip(isMobile, "the test sets each width itself");
  await openChapter(page);
  for (const width of [480, 640, 700, 768, 834, 960, 1024, 1280]) {
    await page.setViewportSize({ width, height: 900 });
    const rows = await page.evaluate(() =>
      [...document.querySelectorAll(".choice-fields")].map((g) => {
        const perRow = new Map<number, number>();
        for (const f of g.querySelectorAll(".choice-field")) {
          const top = Math.round(f.getBoundingClientRect().top);
          perRow.set(top, (perRow.get(top) ?? 0) + 1);
        }
        return [...perRow.values()];
      }),
    );
    for (const counts of rows)
      expect(new Set(counts).size, `at ${width} pixels: ${counts}`).toBe(1);
  }
});
