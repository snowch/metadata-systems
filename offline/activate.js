// Copyright © 2026 Christopher Snow

// Activate only this course's worker on an explicit update action. Other projects on the same
// origin and their workers must remain untouched. No tab is closed or reloaded by the worker.
export async function activateWorker(url) {
  if (!("serviceWorker" in navigator)) return;
  const expected = new URL(url, window.location.href).href;
  const registration = (await navigator.serviceWorker.getRegistrations()).find(
    (registration) =>
      window.location.href.startsWith(registration.scope) &&
      [registration.active, registration.waiting, registration.installing].some(
        (worker) => worker?.scriptURL === expected,
      ),
  );
  if (!registration) return;
  if (navigator.onLine !== false) await registration.update();
  const worker = registration.waiting || registration.installing;
  if (worker) {
    await new Promise((resolve, reject) => {
      const timer = setTimeout(() => finish(new Error("Worker activation timed out")), 15000);
      const changed = () => {
        if (worker.state === "installed") worker.postMessage({ type: "MS_OFFLINE_ACTIVATE" });
        if (worker.state === "activated") finish();
        if (worker.state === "redundant") finish(new Error("Worker activation failed"));
      };
      const finish = (error) => {
        clearTimeout(timer);
        worker.removeEventListener("statechange", changed);
        error ? reject(error) : resolve();
      };
      worker.addEventListener("statechange", changed);
      changed();
    });
  }
  const active = registration.active;
  if (!active) throw new Error("No active course worker");
  // Wait for claim, rather than racing reload against the controller change.
  await new Promise((resolve, reject) => {
    const channel = new MessageChannel();
    const timer = setTimeout(() => finish(new Error("Worker claim timed out")), 10000);
    const finish = (error) => {
      clearTimeout(timer);
      channel.port1.close();
      error ? reject(error) : resolve();
    };
    channel.port1.onmessage = () => finish();
    active.postMessage({ type: "MS_OFFLINE_CLAIM" }, [channel.port2]);
  });
}
