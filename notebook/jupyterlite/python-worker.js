// Copyright © 2026 Christopher Snow

importScripts("./python-progress.js");
self.addEventListener("fetch", (event) => {
  if (
    event.request.method !== "GET" ||
    !new URL(event.request.url).pathname.endsWith("/pyodide.asm.wasm")
  )
    return;
  event.stopImmediatePropagation();
  event.respondWith(
    fetch(event.request).then((response) => self.msTrackPython(event.request, response)),
  );
});
self.addEventListener("message", (event) => {
  if (event.data?.type === "MS_OFFLINE_ACTIVATE") event.waitUntil(self.skipWaiting());
  if (event.data?.type === "MS_OFFLINE_CLAIM")
    event.waitUntil(
      self.clients.claim().then(() => event.ports[0]?.postMessage({ claimed: true })),
    );
});
// The pinned upstream install handler calls skipWaiting unconditionally. Its precache list
// is empty; handle installation here so subsequent workers wait for the reader's update action.
self.addEventListener("install", (event) => event.stopImmediatePropagation());
importScripts("./service-worker.js");
