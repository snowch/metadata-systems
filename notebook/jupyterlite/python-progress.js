// Copyright © 2026 Christopher Snow

// The build supplies the decoded WASM size. Content-Length may describe compressed bytes,
// whereas a fetch response stream contains decoded bytes. Track the same units throughout.
const runtimeBytes = Number("MS_PYTHON_RUNTIME_BYTES");
self.msTrackPython = (request, response) => {
  if (
    !new URL(request.url).pathname.endsWith("/pyodide.asm.wasm") ||
    !response.ok ||
    !response.body
  )
    return response;
  const id = crypto.randomUUID();
  const started = Date.now();
  const reader = response.body.getReader();
  let loaded = 0;
  let last = 0;
  let pending;
  const announce = (complete = false) => {
    const now = Date.now();
    if (!complete && loaded && now - last < 150) {
      if (!pending)
        pending = setTimeout(
          () => {
            pending = null;
            announce();
          },
          150 - (now - last),
        );
      return;
    }
    clearTimeout(pending);
    pending = null;
    last = now;
    const received = loaded;
    const finished = complete && received === runtimeBytes;
    void self.clients.matchAll({ type: "window", includeUncontrolled: true }).then((clients) => {
      for (const client of clients)
        if (client.url.startsWith(self.registration.scope))
          client.postMessage({
            type: "MS_PYTHON_DOWNLOAD",
            id,
            started,
            loaded: received,
            total: runtimeBytes,
            complete: finished,
          });
    });
  };
  announce();
  const stream = new ReadableStream({
    async pull(controller) {
      try {
        const chunk = await reader.read();
        if (chunk.done) {
          announce(true);
          controller.close();
        } else {
          loaded += chunk.value.byteLength;
          announce();
          controller.enqueue(chunk.value);
        }
      } catch (error) {
        clearTimeout(pending);
        controller.error(error);
      }
    },
    cancel(reason) {
      clearTimeout(pending);
      return reader.cancel(reason);
    },
  });
  const headers = new Headers(response.headers);
  headers.delete("content-encoding");
  headers.delete("content-length");
  return new Response(stream, {
    status: response.status,
    statusText: response.statusText,
    headers,
  });
};
