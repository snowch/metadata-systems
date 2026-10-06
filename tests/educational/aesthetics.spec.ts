// Copyright © 2026 Christopher Snow

// The look of the page, held to rules a reader needs: no visible text under 11 pixels, every
// control at least 40 pixels tall on a phone, and no line of prose much over 85 characters.

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
