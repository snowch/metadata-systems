// Copyright © 2026 Christopher Snow

import { test } from "node:test";
import assert from "node:assert/strict";
import { answerStore, legacyGuesses, recoverGuesses, PREFIX } from "./answers.js";

function fixture() {
  const values = new Map();
  const storage = {
    getItem: (key) => values.get(key) ?? null,
    setItem: (key, value) => values.set(key, value),
  };
  const events = new EventTarget();
  return { values, storage, events, open: () => answerStore(() => storage, events) };
}

test("answers survive reopening; revisions and concurrent different fields preserve originals", () => {
  const f = fixture();
  const one = f.open();
  one.write("ch01.daily_sales", "I suspect a daily sum.");
  one.dispose();
  const two = f.open();
  assert.equal(two.read("ch01.daily_sales").text, "I suspect a daily sum.");
  const otherTab = f.open();
  two.write("ch02.daily_sales.revision", "Matching rows does not prove the source.");
  otherTab.write("ch01.clean_orders", "Possibly the raw orders.");
  assert.equal(two.read("ch01.clean_orders").text, "Possibly the raw orders.");
  assert.equal(
    otherTab.read("ch02.daily_sales.revision").text,
    "Matching rows does not prove the source.",
  );
  assert.equal(two.read("ch01.daily_sales").text, "I suspect a daily sum.");
});

test("blocked or full storage keeps an unsaved draft available to export", () => {
  const f = fixture();
  f.storage.setItem = () => {
    throw new Error("Quota exceeded");
  };
  const store = f.open();
  assert.equal(store.write("ch01.daily_sales", "An unsaved answer"), false);
  assert.deepEqual(store.read("ch01.daily_sales"), {
    text: "An unsaved answer",
    exists: true,
    saved: false,
  });
  assert.equal(JSON.parse(store.export()).answers["ch01.daily_sales"], "An unsaved answer");
  f.storage.setItem = (key, value) => f.values.set(key, value);
  assert.equal(store.write("ch01.daily_sales", "Recovered"), true);
  const blocked = answerStore(() => {
    throw new Error("SecurityError");
  }, f.events);
  assert.equal(blocked.read("ch01.clean_orders").saved, false);
  assert.equal(blocked.write("ch01.clean_orders", "Still editable"), false);
  assert.equal(JSON.parse(blocked.export()).answers["ch01.clean_orders"], "Still editable");
});

test("export/import restores missing and explicitly reset answers, preserving existing work", () => {
  const f = fixture();
  const old = f.open();
  old.write("ch01.daily_sales", "Original <script> text");
  old.write("ch02.report", "My report");
  const backup = old.export();
  const fresh = fixture().open();
  fresh.write("ch02.report", "A newer report");
  fresh.write("ch01.daily_sales", "");
  assert.equal(fresh.import(backup), true);
  assert.equal(fresh.read("ch01.daily_sales").text, "Original <script> text");
  assert.equal(fresh.read("ch02.report").text, "A newer report");
  assert.throws(() =>
    fresh.import(
      JSON.stringify({
        course: "metadata-systems",
        version: 1,
        answers: { "ch01.clean_orders": "Should not be written", unknown: "bad" },
      }),
    ),
  );
  assert.equal(fresh.read("ch01.clean_orders").exists, false);
  assert.throws(() => fresh.import('{"course":"another-course","version":1,"answers":{}}'));
  assert.throws(() => fresh.import("not JSON"));
});

test("other tabs notify subscribers without losing an unsaved local draft", () => {
  const f = fixture();
  const store = f.open();
  let changes = 0;
  store.subscribe(() => {
    changes += 1;
  });
  f.values.set(PREFIX + "ch01.daily_sales", "Another tab");
  const event = new Event("storage");
  Object.defineProperty(event, "key", { value: PREFIX + "ch01.daily_sales" });
  f.events.dispatchEvent(event);
  assert.equal(changes, 1);
  assert.equal(store.read("ch01.daily_sales").text, "Another tab");
  store.dispose();
  f.events.dispatchEvent(event);
  assert.equal(changes, 1);
});

test("legacy recovery reads plain text without evaluating Python and ignores placeholders", async () => {
  const source =
    'guesses = """\nclean_customers: made from ........ because ........\nclean_orders: file A because ids match\ndaily_sales: __import__("os").system("never execute")\n"""';
  const notebook = { cells: [{ cell_type: "code", source }] };
  const extracted = legacyGuesses(notebook);
  assert.deepEqual(extracted, {
    "ch01.clean_orders": "file A because ids match",
    "ch01.daily_sales": '__import__("os").system("never execute")',
  });
  const f = fixture();
  const store = f.open();
  store.write("ch01.daily_sales", ""); // explicit reset must not resurrect an old notebook answer
  const contents = {
    get: async (path) => ({
      content: path
        ? notebook
        : [{ name: "chapter_01 (your copy).ipynb", last_modified: "2026-10-17" }],
    }),
  };
  await recoverGuesses(contents, store);
  assert.equal(store.read("ch01.clean_orders").text, "file A because ids match");
  assert.equal(store.read("ch01.daily_sales").text, "");
  assert.equal(store.read("ch01.clean_customers").exists, false);
  store.write("ch01.clean_orders", "My new answer");
  await recoverGuesses(contents, store);
  assert.equal(store.read("ch01.clean_orders").text, "My new answer");
});
