// Copyright © 2026 Christopher Snow

import assert from "node:assert/strict";

export async function checkRetiredChapter(browser, base) {
  assert.equal((await fetch(`${base}/files/chapter_01b.ipynb`)).status, 404);
  const context = await browser.newContext();
  try {
    await context.addInitScript(() => {
      localStorage.setItem(
        "ms:metadata-systems:code:v1:chapter_01b.ipynb:products",
        'print("My old 1b draft")',
      );
      localStorage.setItem(
        "ms:metadata-systems:answers:v1:ch01.daily_sales",
        "My saved exercise answer",
      );
    });
    const page = await context.newPage();
    const errors = [];
    page.on("pageerror", (error) => errors.push(error.message));
    await page.goto(`${base}/notebooks/index.html?path=chapter_01b.ipynb`);
    await page.waitForURL(/path=chapter_01.ipynb/);
    const editor = page.locator('.ms-Example[data-example="products"] .cm-content');
    await editor.waitFor({ timeout: 120000 });
    assert.equal(await editor.innerText(), 'print("My old 1b draft")');
    await page.waitForSelector('textarea[data-answer="ch01.daily_sales"]', { state: "attached" });
    assert.equal(
      await page.locator('textarea[data-answer="ch01.daily_sales"]').inputValue(),
      "My saved exercise answer",
    );
    await editor.fill('print("My newer Chapter 1 draft")');
    await page.goto(`${base}/notebooks/index.html?path=chapter_01b.ipynb`);
    await page.waitForURL(/path=chapter_01.ipynb/);
    await editor.waitFor({ timeout: 120000 });
    assert.equal(await editor.innerText(), 'print("My newer Chapter 1 draft")');
    assert.deepEqual(errors, []);
    console.log(
      "ok retired chapter: no 1b notebook; old links redirect, old drafts import, newer Chapter 1 drafts and answers are preserved",
    );
  } finally {
    await context.close();
  }
}
