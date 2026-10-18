// Copyright © 2026 Christopher Snow

// Keep JupyterLite's filesystem/stdin bridge. Our earlier listener handles only static course
// files; API requests continue to its own service worker. Caches are private to this course URL.
const scope = self.registration.scope;
const prefix = `ms:metadata-systems:offline:${scope}:`;
const stateURL = new URL("__offline_state__", scope).href;
const manifestURL = new URL("offline-manifest.json", scope).href;

async function saved(request) {
  const meta = await caches.open(`${prefix}meta`);
  const record = await meta.match(stateURL);
  if (!record) return;
  const state = await record.json();
  for (const version of [state.version, state.previous].filter(Boolean)) {
    const cache = await caches.open(`${prefix}${version}`);
    const response = await cache.match(request, { ignoreSearch: true });
    if (response) return response;
  }
}

async function network(request) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), 4000);
  try {
    return await fetch(request, { signal: controller.signal });
  } finally {
    clearTimeout(timer);
  }
}

self.addEventListener("fetch", (event) => {
  const request = event.request;
  const url = new URL(request.url);
  if (
    request.method !== "GET" ||
    !url.href.startsWith(scope) ||
    url.pathname.includes("/api/drive") ||
    url.pathname.includes("/api/stdin/") ||
    request.headers.has("X-MS-Offline-Download")
  )
    return;
  event.stopImmediatePropagation();
  // Query strings select the notebook, not its HTML shell. Wheel checksums also refer to the
  // same file. Only URLs inside this registration's scope are normalised.
  url.search = "";
  if (url.pathname.endsWith("/")) url.pathname += "index.html";
  const key = url.href;
  event.respondWith(
    (async () => {
      if (key === manifestURL) {
        try {
          const response = await network(request);
          if (response.ok) return response;
        } catch {
          /* An existing snapshot remains usable without a network. */
        }
        return (await saved(key)) || new Response("", { status: 503 });
      }
      const cached = await saved(key);
      if (cached) return cached;
      return fetch(request);
    })(),
  );
});

self.addEventListener("message", (event) => {
  if (event.data?.type === "MS_OFFLINE_CLAIM") event.waitUntil(self.clients.claim());
});

// Supplied by the pinned JupyterLite build, not a copied implementation of its protocol.
importScripts("./jupyterlite/service-worker.js");
