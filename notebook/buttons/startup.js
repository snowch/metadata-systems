// Copyright © 2026 Christopher Snow

// Track startup independently of cell execution and chapter-update notices. A timeout offers
// retry without pretending a slow download has failed. Superseded attempts cannot update the UI
// or keep a queued Run all waiting. No download totals are exposed by the worker's kernel API.
export function createStartup({ start, render, setTimer = setTimeout, clearTimer = clearTimeout }) {
  let attempt;
  let disposed = false;
  const clear = () => attempt?.timers.forEach(clearTimer);
  return {
    begin(retry = false) {
      if (disposed) return Promise.resolve(false);
      clear();
      attempt?.abort.abort();
      attempt?.finish(false);
      const current = {
        phase: "loading",
        slow: false,
        stalled: false,
        timers: [],
        abort: new AbortController(),
      };
      current.promise = new Promise((resolve) => (current.finish = resolve));
      attempt = current;
      const active = () => !disposed && attempt === current;
      const show = () =>
        render({ phase: current.phase, slow: current.slow, stalled: current.stalled });
      show();
      for (const [delay, flag] of [
        [10_000, "slow"],
        [120_000, "stalled"],
      ]) {
        current.timers.push(
          setTimer(() => {
            if (!active()) return;
            current[flag] = true;
            show();
          }, delay),
        );
      }
      Promise.resolve()
        .then(() =>
          start({
            retry,
            active,
            signal: current.abort.signal,
            preparing() {
              if (!active()) return;
              current.phase = "preparing";
              show();
            },
          }),
        )
        .then(
          () => {
            if (!active()) return;
            clear();
            current.phase = "ready";
            show();
            current.finish(true);
            current.timers.push(
              setTimer(() => {
                if (active()) render({ phase: "hidden" });
              }, 3000),
            );
          },
          () => {
            if (!active()) return;
            clear();
            current.phase = "failed";
            show();
            current.finish(false);
          },
        );
      return current.promise;
    },
    ready() {
      return attempt?.promise ?? Promise.resolve(false);
    },
    dispose() {
      disposed = true;
      clear();
      attempt?.abort.abort();
      attempt?.finish(false);
    },
  };
}
