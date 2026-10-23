// Copyright © 2026 Christopher Snow

import assert from "node:assert/strict";
import { mkdtemp, readFile, writeFile, rm } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";

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

// Use a real profile rather than Playwright storageState: IndexedDB notebook copies, localStorage,
// service workers and their upgrade behaviour must survive an actual browser process restart.
export async function checkAnswerUpdate(browserType, base, site) {
  const profile = await mkdtemp(join(tmpdir(), "ms-answer-update-"));
  const originals = new Map();
  const files = new Map();
  const updates = new Map();
  for (const number of [1, 2]) {
    const path = `chapter_0${number}.ipynb`;
    const text = await readFile(join(site, "files", path), "utf8");
    files.set(path, text);
    const original = JSON.parse(text);
    originals.set(path, original);
    const updated = structuredClone(original);
    updated.cells.unshift({
      cell_type: "markdown",
      id: "new-prose",
      metadata: {},
      source: ["New explanation."],
    });
    for (const [index, cell] of updated.cells.entries()) cell.id = `new-${index}`;
    updated.metadata.ms.version = `answer-update-${number}`;
    updates.set(path, updated);
  }
  let context;
  const launch = async () => {
    context = await browserType.launchPersistentContext(profile, {
      viewport: { width: 390, height: 844 },
    });
    return context.pages()[0];
  };
  const open = async (page, number) => {
    await page.goto(`${base}/notebooks/index.html?path=chapter_0${number}.ipynb`);
    await page
      .locator("textarea[data-answer]")
      .first()
      .waitFor({ state: "attached", timeout: 120000 });
  };
  const answers = new Map();
  try {
    let page = await launch();
    for (const number of [1, 2]) {
      await open(page, number);
      for (const field of await page.locator("textarea[data-answer]:not([readonly])").all()) {
        const id = await field.getAttribute("data-answer");
        const text = `My saved answer: ${id}\nSecond line with £ and café.`;
        await field.fill(text);
        answers.set(id, text);
      }
      // Force the update path which replaces a browser-owned notebook, rather than merely
      // reopening a remote file. These copies predate the next publication.
      await page.evaluate(
        async ({ path, content }) => {
          const { name } = (await indexedDB.databases()).find((db) =>
            db.name.startsWith("JupyterLite Storage"),
          );
          const db = await new Promise((resolve, reject) => {
            const request = indexedDB.open(name);
            request.onsuccess = () => resolve(request.result);
            request.onerror = () => reject(request.error);
          });
          const tx = db.transaction("files", "readwrite");
          const now = new Date().toISOString();
          tx.objectStore("files").put(
            {
              name: path,
              path,
              type: "notebook",
              format: "json",
              content,
              writable: true,
              created: now,
              last_modified: now,
              mimetype: null,
            },
            path,
          );
          await new Promise((resolve, reject) => {
            tx.oncomplete = resolve;
            tx.onerror = () => reject(tx.error);
          });
          db.close();
        },
        { path: `chapter_0${number}.ipynb`, content: originals.get(`chapter_0${number}.ipynb`) },
      );
    }
    assert.equal(answers.size, 6);
    await context.close();
    for (const [path, content] of updates)
      await writeFile(join(site, "files", path), JSON.stringify(content));
    page = await launch();
    for (const number of [1, 2]) {
      await open(page, number);
      for (const field of await page.locator("textarea[data-answer]").all()) {
        const id = await field.getAttribute("data-answer");
        assert.equal(
          await field.inputValue(),
          answers.get(id),
          `published update and restart retain ${id}`,
        );
      }
      // Verify that the new publication was actually opened, not an unchanged cached document.
      await page
        .locator(".jp-RenderedMarkdown")
        .getByText("New explanation.", { exact: true })
        .waitFor({ state: "attached" });
    }
    console.log(
      "ok exercise answers: all six fields survive browser restart and replacement of saved notebooks; Chapter 2 also retains Chapter 1 originals",
    );
  } finally {
    await context?.close();
    for (const [path, text] of files) await writeFile(join(site, "files", path), text);
    await rm(profile, { recursive: true, force: true });
  }
}
