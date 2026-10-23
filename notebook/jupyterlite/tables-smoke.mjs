// Copyright © 2026 Christopher Snow

import assert from "node:assert/strict";
import words from "../buttons/table-words.json" with { type: "json" };

export async function checkTables(page, check) {
  const trigger = page.getByRole("button", { name: words.button, exact: true });
  const dialog = page.getByRole("dialog", { name: words.title });
  const select = dialog.getByLabel(words.choose);
  const run = dialog.getByRole("button", { name: words.run, exact: true });
  const status = dialog.locator(".ms-Tables-status");
  const original = page.locator('[data-example="cell-16"] .cm-content');
  await trigger.waitFor();
  const source = await original.innerText();
  const edit = async (text) => {
    // A contenteditable fill can append after a native dialog restores the editor's selection.
    // Use the editor's real select-all shortcut, then replace that selection as a reader would.
    await original.click();
    await original.press("ControlOrMeta+a");
    await page.keyboard.insertText(text);
    assert.equal(await original.innerText(), text);
  };
  const close = () => dialog.getByRole("button", { name: words.close }).click();
  const runQuery = async (message = words.latest) => {
    await run.click();
    await page.waitForFunction(
      () => !document.querySelector('[data-reader-action="runTable"]').disabled,
      null,
      { timeout: 120_000 },
    );
    try {
      await status.getByText(message, { exact: true }).waitFor({ timeout: 120_000 });
    } catch (error) {
      console.log("table status", await status.innerText(), "expected", message);
      console.log(
        "table source",
        await original.innerText(),
        "output",
        await page.locator('[data-example="cell-16"] .jp-OutputArea').innerText(),
      );
      throw error;
    }
  };

  await trigger.click();
  assert.equal(await select.locator("option").count(), 4);
  assert.equal(await status.innerText(), words.empty);
  check(
    (await dialog.locator("table").count()) === 0,
    "tables: opening an unrun table does not execute it",
  );
  await page.keyboard.press("Escape");
  check(
    await trigger.evaluate((node) => node === document.activeElement),
    "tables: Escape returns focus to the header button",
  );

  const link = page.locator('a[href="#ms-table-cell-16"]').first();
  await link.scrollIntoViewIfNeeded();
  const top = await link.evaluate((node) => node.getBoundingClientRect().top);
  await link.click();
  await runQuery();
  assert.equal(await dialog.locator("table tr").count(), 8);
  check(
    (await dialog.locator("table").innerText()).includes("4500"),
    "tables: a nearby link opens the real seven-day comparison without code",
  );
  check(
    (await dialog.locator(".cm-editor").count()) === 0,
    "tables: the overlay shows results without a code editor",
  );

  for (const width of [360, 390, 600, 1280]) {
    await page.setViewportSize({ width, height: 844 });
    check(
      await dialog.evaluate((node) => {
        const rect = node.getBoundingClientRect();
        return (
          rect.left >= 0 && rect.right <= innerWidth && node.scrollWidth <= node.clientWidth + 1
        );
      }),
      `tables: the ${width}px dialog fits while its table scrolls independently`,
    );
    await dialog.screenshot({ path: `/tmp/metadata-tables-${width}.png` });
    if (width === 360) {
      check(
        await dialog.getByText(words.scrollHint, { exact: true }).isVisible(),
        "tables: narrow results explain that more columns are available sideways",
      );
      const frozen = await dialog.locator(".ms-Tables-output").evaluate((node) => {
        const first = node.querySelector("td");
        const left = first.getBoundingClientRect().left;
        node.scrollLeft = 250;
        return Math.abs(first.getBoundingClientRect().left - left) < 2;
      });
      check(frozen, "tables: the day stays visible while scrolling to the difference column");
    }
  }
  await page.setViewportSize({ width: 390, height: 844 });
  await close();
  check(
    Math.abs((await link.evaluate((node) => node.getBoundingClientRect().top)) - top) < 3,
    "tables: closing after running a query preserves the reading position",
  );

  for (const width of [360, 390, 600, 1280]) {
    await page.setViewportSize({ width, height: 844 });
    check(
      await page
        .locator(".ms-Reader-nav")
        .evaluate((node) => node.scrollWidth <= node.clientWidth + 1),
      `tables: the ${width}px header fits with Tables and chapter navigation`,
    );
  }
  await page.setViewportSize({ width: 390, height: 844 });
  await trigger.click();
  await select.selectOption("cell-42");
  await runQuery();
  check(
    (await dialog.locator("table").innerText()).includes("4500"),
    "tables: the chooser also runs and displays the duplicate-order query",
  );
  await close();

  await edit(source.replace("ORDER BY d.day", "WHERE d.day = '2026-09-09'\nORDER BY d.day"));
  await trigger.click();
  await select.selectOption("cell-16");
  await status.getByText(words.stale, { exact: true }).waitFor();
  assert.equal(await dialog.locator("table tr").count(), 8);
  await runQuery();
  check(
    (await dialog.locator("table tr").count()) === 2,
    "tables: edited code is marked outdated, and Run query updates the existing result",
  );
  await select.selectOption("cell-42");
  await status.getByText(words.upstream, { exact: true }).waitFor();
  check(
    (await dialog.locator("table tr").count()) === 2,
    "tables: earlier example changes mark a later table outdated without hiding its previous result",
  );
  await close();

  await edit("raise ValueError('table viewer test')");
  await trigger.click();
  await select.selectOption("cell-16");
  await runQuery(words.error);
  check(
    (await dialog.locator("table").count()) === 0,
    "tables: query errors cannot be mistaken for a successful table",
  );
  await close();
  await edit("print(123)");
  await trigger.click();
  await runQuery(words.noTable);
  check(
    (await dialog.locator("table").count()) === 0,
    "tables: an edited query that returns no table has an explicit empty state",
  );
  await close();

  await edit("import time\ntime.sleep(2)\n" + source);
  await trigger.click();
  await run.click();
  await status.getByText(words.running, { exact: true }).waitFor();
  await select.selectOption("cell-42");
  check(
    await run.isDisabled(),
    "tables: the chooser remains usable during execution but prevents overlapping queries",
  );
  await page.waitForFunction(
    () => !document.querySelector('[data-reader-action="runTable"]').disabled,
    null,
    { timeout: 120_000 },
  );
  await close();
  await page
    .locator('[data-example="cell-16"]')
    .getByRole("button", { name: "Reset example", exact: true })
    .click();
  await trigger.click();
  await select.selectOption("cell-16");
  check(
    (await status.innerText()) === words.empty && (await dialog.locator("table").count()) === 0,
    "tables: Reset example clears the overlay result too",
  );
  await close();
}
