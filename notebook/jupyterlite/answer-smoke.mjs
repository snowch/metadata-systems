// Copyright © 2026 Christopher Snow

// Drives the actual JupyterLite extension, including windowed cells and notebook replacement.
export async function checkAnswers(browser, base, check) {
  const context = await browser.newContext({ viewport: { width: 390, height: 844 } });
  const page = await context.newPage();
  const errors = [];
  page.on("pageerror", (error) => errors.push(error.message));
  const open = async (chapter) => {
    await page.goto(`${base}/notebooks/index.html?path=chapter_0${chapter}.ipynb`);
    await page.waitForSelector(".jp-Notebook .jp-Cell", { timeout: 120_000 });
  };
  const find = async (selector) => {
    await page.waitForSelector(selector, { timeout: 120000, state: "attached" });
    return page.locator(selector).first();
  };
  const field = (id) => find(`textarea[data-answer="${id}"]`);
  const original = "My initial explanation <script>window.answerInjected = true</script> typed";
  try {
    await open(1);
    const first = await field("ch01.daily_sales");
    await first.fill(original.slice(0, -6));
    await first.press("End");
    await first.pressSequentially(" typed");
    await first.press("Escape");
    // No Save or Run button: input must reach durable storage before an immediate reload.
    await page.reload();
    await page.waitForSelector(".jp-Notebook .jp-Cell", { timeout: 120_000 });
    check(
      (await (await field("ch01.daily_sales")).inputValue()) === original,
      "exercise: typed answer survives immediate refresh without Save or Run",
    );
    await (await field("ch01.clean_orders")).fill("My cleaning guess");
    await page.click('button[data-reader-action="runAll"]');
    await page.waitForFunction(
      () => !document.querySelector('button[data-reader-action="runAll"]:disabled'),
      null,
      { timeout: 120_000 },
    );
    check(
      (await (await field("ch01.daily_sales")).inputValue()) === original,
      "exercise: Run all and scrolling preserve the edited answer",
    );
    await open(2);
    const recalled = await field("ch01.daily_sales");
    check(
      (await recalled.getAttribute("readonly")) !== null &&
        (await recalled.inputValue()) === original,
      "exercise: Chapter 2 recalls the original answer read-only",
    );
    await (await field("ch02.daily_sales.revision")).fill("My revised explanation");
    await page.reload();
    await page.waitForSelector(".jp-Notebook .jp-Cell", { timeout: 120_000 });
    check(
      (await (await field("ch02.daily_sales.revision")).inputValue()) === "My revised explanation",
      "exercise: revision survives refresh separately from the original",
    );
    check(
      (await (await field("ch01.clean_orders")).inputValue()) === "My cleaning guess",
      "exercise: the second Chapter 2 comparison recalls clean_orders too",
    );
    await (await field("ch02.report")).fill("The discrepancy does not establish a business error.");
    check(
      await page.evaluate(() => window.answerInjected === undefined),
      "exercise: answers render as text, never as HTML",
    );

    const report = page.locator('[data-exercise="report"]');
    const downloadPromise = page.waitForEvent("download");
    await report.getByRole("button", { name: "Export answers" }).click();
    const download = await downloadPromise;
    const stream = await download.createReadStream();
    const parts = [];
    for await (const part of stream) parts.push(part);
    const backup = Buffer.concat(parts);
    check(
      JSON.parse(backup.toString()).answers["ch01.daily_sales"] === original,
      "exercise: export contains original answers and revisions",
    );
    page.once("dialog", (dialog) => dialog.dismiss());
    await report.getByRole("button", { name: "Reset this answer" }).click();
    check(
      (await report.locator("textarea").inputValue()).length > 0,
      "exercise: cancelling reset preserves the response",
    );
    page.once("dialog", (dialog) => dialog.accept());
    await report.getByRole("button", { name: "Reset this answer" }).click();
    await report.locator('input[type="file"]').setInputFiles({
      name: "answers.json",
      mimeType: "application/json",
      buffer: backup,
    });
    await page.waitForFunction(
      () => document.querySelector('textarea[data-answer="ch02.report"]')?.value.length > 0,
    );
    check(
      (await report.locator("textarea").inputValue()) ===
        "The discrepancy does not establish a business error.",
      "exercise: importing an export restores a reset response",
    );

    // Storage failure leaves the draft editable and exportable, and never claims it was saved.
    await page.evaluate(() => {
      const originalSet = Storage.prototype.setItem;
      Storage.prototype.setItem = function (key, value) {
        if (key.startsWith("ms:metadata-systems:answers:"))
          throw new DOMException("Full", "QuotaExceededError");
        return originalSet.call(this, key, value);
      };
    });
    await report.locator("textarea").fill("Unsaved but exportable draft");
    check(
      (await report.innerText()).includes("Browser storage is unavailable or full"),
      "exercise: failed storage shows actionable feedback",
    );
    const failedDownload = page.waitForEvent("download");
    await report.getByRole("button", { name: "Export answers" }).click();
    const failedStream = await (await failedDownload).createReadStream();
    const failedParts = [];
    for await (const part of failedStream) failedParts.push(part);
    check(
      JSON.parse(Buffer.concat(failedParts).toString()).answers["ch02.report"] ===
        "Unsaved but exportable draft",
      "exercise: export preserves a draft even when saving fails",
    );

    await open(1);
    await (await field("ch01.daily_sales")).fill(original);
    // Simulate a newly published chapter, using the real update handler.
    await context.route("**/files/chapter_01.ipynb", async (route) => {
      const response = await route.fetch();
      const notebook = await response.json();
      notebook.metadata.ms.version = "answer-persistence-update";
      await route.fulfill({ response, json: notebook });
    });
    await page.reload();
    await page.waitForSelector(".jp-Notebook .jp-Cell", { timeout: 120_000 });
    check(
      (await (await field("ch01.daily_sales")).inputValue()) === original,
      "exercise: a published chapter update retains the answer",
    );
    await page.setViewportSize({ width: 360, height: 800 });
    check(
      await page.evaluate(() => {
        const root = document.querySelector(".ms-Answers");
        return (
          root &&
          root.scrollWidth <= root.clientWidth &&
          [...root.querySelectorAll("button")].every(
            (button) => button.getBoundingClientRect().height >= 44,
          )
        );
      }),
      "exercise: answer controls fit a phone and keep 44-pixel buttons",
    );
    check(errors.length === 0, `exercise: no browser errors (${errors.join("; ")})`);
  } finally {
    await context.close();
  }
}
