// Copyright © 2026 Christopher Snow

import { test } from "node:test";
import assert from "node:assert/strict";
import { activateWorker } from "./activate.js";

function fixture(t, online = true) {
  const href = "https://example.org/metadata-systems/jupyterlite/notebooks/index.html";
  const expected = "https://example.org/metadata-systems/offline-worker.js";
  const previous = Object.getOwnPropertyDescriptor(globalThis, "navigator");
  const oldWindow = globalThis.window;
  let updates = 0;
  let claims = 0;
  let activations = 0;
  const worker = new EventTarget();
  worker.scriptURL = expected;
  worker.state = "installed";
  const registration = {
    scope: "https://example.org/metadata-systems/",
    active: { scriptURL: expected },
    waiting: worker,
    async update() {
      updates++;
    },
  };
  worker.postMessage = (message, ports) => {
    if (message.type === "MS_OFFLINE_ACTIVATE") {
      activations++;
      registration.active = worker;
      registration.waiting = null;
      worker.state = "activated";
      worker.dispatchEvent(new Event("statechange"));
    } else if (message.type === "MS_OFFLINE_CLAIM") {
      claims++;
      ports[0].postMessage({ claimed: true });
      ports[0].close();
    }
  };
  const unrelated = {
    scope: "https://example.org/other/",
    active: { scriptURL: "https://example.org/other/offline-worker.js" },
    update() {
      throw new Error("Unrelated worker touched");
    },
  };
  Object.defineProperty(globalThis, "navigator", {
    configurable: true,
    value: {
      onLine: online,
      serviceWorker: { getRegistrations: async () => [unrelated, registration] },
    },
  });
  globalThis.window = { location: { href } };
  t.after(() => {
    if (previous) Object.defineProperty(globalThis, "navigator", previous);
    else delete globalThis.navigator;
    if (oldWindow) globalThis.window = oldWindow;
    else delete globalThis.window;
  });
  return { expected, worker, registration, counts: () => ({ updates, claims, activations }) };
}

test("explicit update activates and claims the expected worker, leaving other projects alone", async (t) => {
  const f = fixture(t);
  await activateWorker(f.expected);
  assert.equal(f.registration.active, f.worker);
  assert.equal(f.registration.waiting, null);
  assert.deepEqual(f.counts(), { updates: 1, claims: 1, activations: 1 });
});

test("an already downloaded update can be activated while offline", async (t) => {
  const f = fixture(t, false);
  await activateWorker(f.expected);
  assert.deepEqual(f.counts(), { updates: 0, claims: 1, activations: 1 });
});

test("a missing registration does not update any other worker", async (t) => {
  const f = fixture(t);
  await activateWorker("https://example.org/metadata-systems/missing-worker.js");
  assert.deepEqual(f.counts(), { updates: 0, claims: 0, activations: 0 });
});
