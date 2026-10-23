// Copyright © 2026 Christopher Snow

import assert from "node:assert/strict";

export async function checkPublishedUpdate(browser, base) {
  const context = await browser.newContext({ serviceWorkers: "block" });
  try {
    const original = await (await fetch(`${base}/files/chapter_02.ipynb`)).json();
    const updated = structuredClone(original);
    updated.cells.unshift({
      cell_type: "markdown",
      id: "inserted-explanation",
      metadata: {},
      source: ["An inserted explanation."],
    });
    for (const [index, cell] of updated.cells.entries()) cell.id = `reordered-${index}`;
    updated.metadata.ms.version = "simulated-new-publication";
    let publishing = false;
    await context.route("**/files/chapter_02.ipynb", (route) =>
      route.fulfill({ json: publishing ? updated : original }),
    );
    const page = await context.newPage();
    const url = `${base}/notebooks/index.html?path=chapter_02.ipynb`;
    await page.goto(url);
    const first = original.cells.find((cell) => cell.metadata?.ms?.example?.editable);
    const id = first.metadata.ms.example.id;
    const editor = page.locator(`.ms-Example[data-example="${id}"] .cm-content`);
    await editor.waitFor({ timeout: 120000 });
    const savedCode = (await editor.innerText()) + "\n# My code saved before publication";
    await editor.fill(savedCode);
    const answer = page.locator("textarea:not([readonly])").first();
    await answer.waitFor({ timeout: 120000 });
    const answerId = await answer.getAttribute("data-answer");
    await answer.fill("My explanation saved before publication");
    const before = await page.evaluate(() =>
      Object.fromEntries(
        Object.entries(localStorage).filter(([key]) => key.startsWith("ms:metadata-systems:")),
      ),
    );
    publishing = true;
    await page.reload();
    await editor.waitFor({ timeout: 120000 });
    assert.equal(await editor.innerText(), savedCode);
    const restored = page.locator(`textarea[data-answer="${answerId}"]`);
    await restored.waitFor({ state: "attached", timeout: 120000 });
    assert.equal(await restored.inputValue(), "My explanation saved before publication");
    const after = await page.evaluate(() =>
      Object.fromEntries(
        Object.entries(localStorage).filter(([key]) => key.startsWith("ms:metadata-systems:")),
      ),
    );
    for (const [key, value] of Object.entries(before))
      assert.equal(after[key], value, `published update must preserve ${key}`);
    assert.equal(await page.getByRole("dialog").count(), 0);
    console.log(
      "ok published update: changed release and reordered notebook cells retain code edits and exercise answers without deleting stored data",
    );
  } finally {
    await context.close();
  }
}
