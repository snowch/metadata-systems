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
importScripts("./service-worker.js");
