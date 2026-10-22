// Copyright © 2026 Christopher Snow

// Track startup independently of cell execution and chapter-update notices. A timeout offers
// retry without pretending a slow download has failed. Superseded attempts cannot update the UI
// or keep a queued Run all waiting. Runtime download bytes arrive from the course service worker.
export function createStartup({
  start,
  render,
  setTimer = setTimeout,
  clearTimer = clearTimeout,
  now = () => performance.now(),
}) {
  let attempt;
  let disposed = false;
  const clear = () => {
    attempt?.timers.forEach(clearTimer);
    if (attempt?.clock !== undefined) clearTimer(attempt.clock);
  };
  return {
    begin(retry = false) {
      if (disposed) return Promise.resolve(false);
      clear();
      attempt?.abort.abort();
      attempt?.finish(false);
      const current = {
        phase: "loading",
        since: retry ? Date.now() : 0,
        slow: false,
        stalled: false,
        timers: [],
        abort: new AbortController(),
      };
      current.promise = new Promise((resolve) => (current.finish = resolve));
      attempt = current;
      const active = () => !disposed && attempt === current;
      const show = () =>
        render({
          phase: current.phase,
          slow: current.slow,
          stalled: current.stalled,
          elapsed:
            current.stageSince === undefined
              ? undefined
              : Math.floor((now() - current.stageSince) / 1000),
          download: current.download,
        });
      current.show = show;
      current.stage = () => {
        current.stageSince = now();
      };
      const updateClock = () => {
        if (!active()) return;
        if (current.stageSince !== undefined) show();
        current.clock = setTimer(updateClock, 1000);
      };
      current.clock = setTimer(updateClock, 1000);
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
              current.stage();
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
    download(value) {
      const current = attempt;
      if (disposed || !current || current.phase !== "loading" || value.started < current.since)
        return;
      if (
        !Number.isFinite(value.total) ||
        value.total <= 0 ||
        !Number.isFinite(value.loaded) ||
        value.loaded < 0
      )
        return;
      if (current.downloadId && current.downloadId !== value.id) return;
      current.downloadId = value.id;
      const percent = Math.min(
        value.complete ? 100 : 99,
        Math.floor((value.loaded * 100) / value.total),
      );
      if (current.download && percent <= current.download.percent) return;
      current.download = { percent };
      if (percent === 100) current.stage();
      current.show();
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
