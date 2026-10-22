// Copyright © 2026 Christopher Snow

import assert from "node:assert/strict";
import { test } from "node:test";
import { createStartup } from "./startup.js";

const tick = async () => {
  for (let n = 0; n < 6; n++) await Promise.resolve();
};
const deferred = () => {
  let resolve, reject;
  const promise = new Promise((yes, no) => {
    resolve = yes;
    reject = no;
  });
  return { promise, resolve, reject };
};

function fixture(start) {
  const frames = [];
  const timers = new Map();
  let next = 0;
  const controller = createStartup({
    start,
    render: (state) => frames.push(state),
    setTimer: (fn, delay) => {
      const id = ++next;
      timers.set(id, { fn, delay });
      return id;
    },
    clearTimer: (id) => timers.delete(id),
  });
  return {
    controller,
    frames,
    timers,
    fire(delay) {
      for (const [id, timer] of [...timers])
        if (timer.delay === delay) {
          timers.delete(id);
          timer.fn();
        }
    },
  };
}

test("slow startup stays pending, reports stages, and can finish after the retry threshold", async () => {
  const work = deferred();
  let attempt;
  const f = fixture((value) => {
    attempt = value;
    return work.promise;
  });
  const ready = f.controller.begin();
  await tick();
  assert.equal(f.frames.at(-1).phase, "loading");
  f.fire(10_000);
  assert.equal(f.frames.at(-1).slow, true);
  attempt.preparing();
  assert.equal(f.frames.at(-1).phase, "preparing");
  f.fire(120_000);
  assert.equal(f.frames.at(-1).stalled, true);
  assert.equal(f.frames.at(-1).phase, "preparing");
  work.resolve();
  assert.equal(await ready, true);
  assert.equal(f.frames.at(-1).phase, "ready");
  f.fire(3000);
  assert.equal(f.frames.at(-1).phase, "hidden");
  assert.equal(f.timers.size, 0);
});

test("a failure releases queued runs, clears timers, and retry can succeed", async () => {
  let tries = 0;
  const f = fixture(({ retry }) => {
    if (++tries === 1) throw Error("download failed");
    assert.equal(retry, true);
  });
  f.controller.begin();
  assert.equal(await f.controller.ready(), false);
  assert.equal(f.frames.at(-1).phase, "failed");
  assert.equal(f.timers.size, 0);
  assert.equal(await f.controller.begin(true), true);
  assert.equal(f.frames.at(-1).phase, "ready");
});

test("retry cancels a stalled attempt and ignores its late progress or failure", async () => {
  const old = deferred();
  const fresh = deferred();
  const attempts = [];
  const f = fixture((attempt) => {
    attempts.push(attempt);
    return attempts.length === 1 ? old.promise : fresh.promise;
  });
  const first = f.controller.begin();
  await tick();
  const second = f.controller.begin(true);
  await tick();
  assert.equal(await first, false);
  assert.equal(attempts[0].signal.aborted, true);
  attempts[0].preparing();
  old.reject(Error("old worker stopped"));
  await tick();
  assert.equal(f.frames.at(-1).phase, "loading");
  fresh.resolve();
  assert.equal(await second, true);
});

test("closing a notebook cancels waiters and prevents later status updates", async () => {
  const work = deferred();
  const f = fixture(() => work.promise);
  const pending = f.controller.begin();
  await tick();
  f.controller.dispose();
  assert.equal(await pending, false);
  const count = f.frames.length;
  work.resolve();
  await tick();
  assert.equal(f.frames.length, count);
  assert.equal(f.timers.size, 0);
  assert.equal(await f.controller.begin(true), false);
});

test("runtime percentages measure download only and ignore replaced attempts", async () => {
  const work = deferred();
  const f = fixture(() => work.promise);
  f.controller.begin();
  await tick();
  f.controller.download({ id: "first", started: Date.now(), loaded: 25, total: 100 });
  assert.equal(f.frames.at(-1).download.percent, 25);
  f.controller.download({ id: "other-tab", started: Date.now(), loaded: 90, total: 100 });
  assert.equal(f.frames.at(-1).download.percent, 25);
  f.controller.download({ id: "first", started: Date.now(), loaded: 100, total: 100 });
  assert.equal(f.frames.at(-1).download.percent, 99);
  f.controller.download({
    id: "first",
    started: Date.now(),
    loaded: 100,
    total: 100,
    complete: true,
  });
  assert.equal(f.frames.at(-1).download.percent, 100);
  assert.equal(f.frames.at(-1).phase, "loading");
  f.controller.begin(true);
  await tick();
  f.controller.download({ id: "first", started: 1, loaded: 100, total: 100, complete: true });
  assert.equal(f.frames.at(-1).download, undefined);
  f.controller.download({ id: "retry", started: Date.now(), loaded: 10, total: 100 });
  assert.equal(f.frames.at(-1).download.percent, 10);
  work.resolve();
  await tick();
  assert.equal(f.frames.at(-1).phase, "ready");
  f.controller.dispose();
});
