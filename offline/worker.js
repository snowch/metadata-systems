// Copyright © 2026 Christopher Snow

// Keep JupyterLite's filesystem/stdin bridge. Our earlier listener handles only static course
// files; API requests continue to its own service worker. Caches are private to this course URL.
importScripts("./jupyterlite/python-progress.js");

const scope = self.registration.scope;
const prefix = `ms:metadata-systems:offline:${scope}:`;
const stateURL = new URL("__offline_state__", scope).href;
const manifestURL = new URL("offline-manifest.json", scope).href;

async function saved(request, event) {
  const meta = await caches.open(`${prefix}meta`);
  const record = await meta.match(stateURL);
  if (!record) return;
  const state = await record.json();
  const client = event.resultingClientId || event.clientId;
  const pinURL = new URL(`__offline_client__/${client}`, scope).href;
  const pin = client && (await meta.match(pinURL));
  const pinned = pin ? (await pin.json()).version : state.version;
  if (client && !pin && pinned) await meta.put(pinURL, Response.json({ version: pinned }));
  // Never fall through to an unrelated release when a pinned asset is missing.
  for (const version of [pinned].filter(Boolean)) {
    const cache = await caches.open(`${prefix}${version}`);
    const response = await cache.match(request, { ignoreSearch: true });
    if (response) return response;
  }
  if (pin && (state.version || state.pending))
    return new Response("Release asset unavailable; restart this tab", { status: 409 });
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
        return (await saved(key, event)) || new Response("", { status: 503 });
      }
      const cached = await saved(key, event);
      if (cached) return self.msTrackPython(request, cached);
      return self.msTrackPython(request, await fetch(request));
    })(),
  );
});

self.addEventListener("message", (event) => {
  if (
    event.data?.type === "MS_OFFLINE_BIND" &&
    /^[a-f0-9]{20}$/.test(event.data.version) &&
    event.source?.id
  )
    event.waitUntil(
      (async () => {
        const meta = await caches.open(`${prefix}meta`);
        await meta.put(
          new URL(`__offline_client__/${event.source.id}`, scope).href,
          Response.json({ version: event.data.version }),
        );
        event.ports[0]?.postMessage({ bound: true });
      })(),
    );
  if (event.data?.type === "MS_OFFLINE_ACTIVATE") event.waitUntil(self.skipWaiting());
  if (event.data?.type === "MS_OFFLINE_CLAIM")
    event.waitUntil(
      (async () => {
        // Pin every already-open client before publishing a new selected snapshot. Persist pins
        // in the app's metadata cache because service workers can stop between requests.
        const meta = await caches.open(`${prefix}meta`);
        const record = await meta.match(stateURL);
        const state = record ? await record.json() : {};
        for (const client of await self.clients.matchAll({
          includeUncontrolled: true,
          type: "all",
        })) {
          if (!client.url.startsWith(scope) || !state.version) continue;
          const key = new URL(`__offline_client__/${client.id}`, scope).href;
          if (!(await meta.match(key)))
            await meta.put(
              key,
              Response.json({
                version: state.pending ? state.version : state.previous || state.version,
              }),
            );
        }
        await self.clients.claim();
        event.ports[0]?.postMessage({ claimed: true });
      })(),
    );
});

// Supplied by the pinned JupyterLite build, not a copied implementation of its protocol.
// The pinned upstream install handler calls skipWaiting unconditionally. Its precache list
// is empty; handle installation here so subsequent workers wait for the reader's update action.
self.addEventListener("install", (event) => event.stopImmediatePropagation());
importScripts("./jupyterlite/service-worker.js");
