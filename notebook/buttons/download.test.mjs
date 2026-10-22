// Copyright © 2026 Christopher Snow

import { test } from "node:test";
import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { runInNewContext } from "node:vm";
import { webcrypto } from "node:crypto";

const source = readFileSync(new URL("../jupyterlite/python-progress.js", import.meta.url), "utf8");
function tracker(total) {
  const messages = [];
  const self = {
    registration: { scope: "https://course.example/book/" },
    clients: {
      matchAll: async () => [
        {
          url: "https://course.example/book/notebooks/",
          postMessage: (value) => messages.push(value),
        },
        {
          url: "https://course.example/another-book/",
          postMessage: () => assert.fail("Unrelated course received progress"),
        },
      ],
    },
  };
  runInNewContext(source.replace("MS_PYTHON_RUNTIME_BYTES", String(total)), {
    self,
    crypto: webcrypto,
    URL,
    Response,
    Headers,
    ReadableStream,
    setTimeout,
    clearTimeout,
    Date,
  });
  return { self, messages };
}
const request = { url: "https://course.example/book/static/pyodide/pyodide.asm.wasm" };

test("runtime progress preserves decoded WASM and ignores compressed Content-Length", async () => {
  const { self, messages } = tracker(8);
  const original = new Response(new Uint8Array([0, 97, 115, 109, 1, 0, 0, 0]), {
    headers: {
      "Content-Type": "application/wasm",
      "Content-Encoding": "gzip",
      "Content-Length": "4",
    },
  });
  const response = self.msTrackPython(request, original);
  assert.equal(response.headers.get("Content-Type"), "application/wasm");
  assert.equal(response.headers.get("Content-Length"), null);
  assert.equal(response.headers.get("Content-Encoding"), null);
  assert.deepEqual(
    [...new Uint8Array(await response.arrayBuffer())],
    [0, 97, 115, 109, 1, 0, 0, 0],
  );
  assert.equal(messages[0].loaded, 0);
  assert.equal(messages.at(-1).loaded, 8);
  assert.equal(messages.at(-1).total, 8);
  assert.equal(messages.at(-1).complete, true);
});

test("a truncated runtime never reports a complete download", async () => {
  const { self, messages } = tracker(8);
  await self.msTrackPython(request, new Response(new Uint8Array([0, 1]))).arrayBuffer();
  assert.equal(messages.at(-1).loaded, 2);
  assert.equal(messages.at(-1).complete, false);
});

test("cancelling the runtime stream cancels its source without announcing completion", async () => {
  const { self, messages } = tracker(8);
  let cancelled = false;
  const original = new Response(
    new ReadableStream({
      cancel() {
        cancelled = true;
      },
    }),
  );
  await self.msTrackPython(request, original).body.cancel();
  assert.equal(cancelled, true);
  assert.equal(
    messages.some((message) => message.complete),
    false,
  );
});
