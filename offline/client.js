// Copyright © 2026 Christopher Snow

// Shared by the course home and chapter reader; storage keys and verification stay identical.
export function createOffline(base) {
  const prefix = `ms:metadata-systems:offline:${base}:`;
  const stateURL = new URL("__offline_state__", base).href;
  const manifestURL = new URL("offline-manifest.json", base).href;
  const supported = () =>
    window.isSecureContext &&
    "serviceWorker" in navigator &&
    "caches" in window &&
    "locks" in navigator;
  function validate(value) {
    if (
      !/^[a-f0-9]{20}$/.test(value.version) ||
      !Array.isArray(value.files) ||
      !value.files.length ||
      value.files.some(
        (file) =>
          !file.path ||
          new URL(file.path, base).href !== base + file.path ||
          file.path.includes("..") ||
          file.path.includes("?") ||
          file.path.includes("#") ||
          !Number.isSafeInteger(file.size) ||
          file.size < 0 ||
          !/^[a-f0-9]{64}$/.test(file.sha256),
      ) ||
      new Set(value.files.map((file) => file.path)).size !== value.files.length ||
      value.bytes !== value.files.reduce((sum, file) => sum + file.size, 0)
    )
      throw Error("Invalid offline manifest");
    return value;
  }
  async function manifest(networkOnly = false) {
    try {
      const response = await fetch(manifestURL, {
        cache: networkOnly ? "no-store" : "no-cache",
        headers: networkOnly ? { "X-MS-Offline-Download": "update-check" } : {},
        signal: AbortSignal.timeout(6000),
      });
      if (response.ok) {
        const data = await response.json();
        return data ? validate(data) : null;
      }
    } catch {
      /* The current downloaded manifest also works without a network. */
    }
    if (networkOnly || !supported()) return null;
    const state = await (await caches.open(`${prefix}meta`)).match(stateURL);
    if (!state) return null;
    const { version } = await state.json();
    const saved = await (await caches.open(`${prefix}${version}`)).match(manifestURL);
    return saved ? validate(await saved.json()) : null;
  }
  async function snapshot() {
    const state = await (await caches.open(`${prefix}meta`)).match(stateURL);
    const hasDownload = (await caches.keys()).some(
      (name) => name.startsWith(prefix) && name !== `${prefix}meta`,
    );
    if (!state) return { ready: false, hasDownload };
    const { version, pending: candidate } = await state.json();
    let pending, pendingIncomplete;
    if (candidate) {
      const cache = await caches.open(`${prefix}${candidate}`);
      const response = await cache.match(manifestURL);
      const value = response && validate(await response.json());
      const keys = new Set((await cache.keys()).map((request) => request.url));
      if (value && value.files.every((file) => keys.has(new URL(file.path, base).href)))
        pending = candidate;
      else pendingIncomplete = candidate;
    }
    if (!version) return { ready: false, pending, pendingIncomplete, hasDownload };
    const cache = await caches.open(`${prefix}${version}`);
    const response = await cache.match(manifestURL);
    if (!response) return { ready: false, hasDownload };
    const saved = validate(await response.json());
    const keys = new Set((await cache.keys()).map((request) => request.url));
    return {
      ready: saved.files.every((file) => keys.has(new URL(file.path, base).href)),
      version,
      pending,
      pendingIncomplete,
      hasDownload,
    };
  }
  async function register() {
    const url = new URL("offline-worker.js", base).href;
    const existing = await navigator.serviceWorker.getRegistration(base);
    const registration = await navigator.serviceWorker
      .register(url, {
        scope: base,
        updateViaCache: "none",
      })
      .catch((error) => {
        if (existing?.scope === base && existing.active?.scriptURL === url) return existing;
        throw error;
      });
    if (!registration.active)
      await new Promise((resolve, reject) => {
        const worker = registration.installing || registration.waiting;
        if (!worker) return reject(Error("Worker unavailable"));
        const timer = setTimeout(() => reject(Error("Worker installation timed out")), 30_000);
        worker.addEventListener("statechange", () => {
          if (worker.state === "activated") {
            clearTimeout(timer);
            resolve();
          }
          if (worker.state === "redundant") {
            clearTimeout(timer);
            reject(Error("Worker installation failed"));
          }
        });
      });
    // Migrate only this course's old JupyterLite registration. Never unregister another project.
    for (const old of await navigator.serviceWorker.getRegistrations()) {
      if (
        old.scope === new URL("jupyterlite/", base).href &&
        ["service-worker.js", "python-worker.js"].some(
          (name) => old.active?.scriptURL === new URL(`jupyterlite/${name}`, base).href,
        )
      )
        await old.unregister();
    }
    registration.active?.postMessage({ type: "MS_OFFLINE_CLAIM" });
  }
  async function download(value, signal, progress, prepare = false) {
    validate(value);
    await navigator.locks.request(prefix, { ifAvailable: true }, async (lock) => {
      if (!lock) throw Error("Another tab is changing the offline download");
      await register();
      // Persistent storage is a browser decision; readiness never promises permanent retention.
      void navigator.storage?.persist?.().catch(() => false);
      const cache = await caches.open(`${prefix}${value.version}`);
      const known = new Set((await cache.keys()).map((request) => request.url));
      const meta = await caches.open(`${prefix}meta`);
      const before = await meta.match(stateURL);
      const prior = before ? await before.json() : undefined;
      const previous = prior?.version;
      const fallback = previous !== value.version ? previous : prior?.previous;
      if (previous && previous !== value.version) {
        const oldCache = await caches.open(`${prefix}${previous}`);
        const oldManifest = await oldCache.match(manifestURL);
        if (oldManifest) {
          const hashes = new Map(
            validate(await oldManifest.json()).files.map((file) => [file.path, file.sha256]),
          );
          for (const file of value.files) {
            signal.throwIfAborted();
            const url = new URL(file.path, base).href;
            if (!known.has(url) && hashes.get(file.path) === file.sha256) {
              const response = await oldCache.match(url);
              if (response) {
                await cache.put(url, response);
                known.add(url);
              }
            }
          }
        }
      }
      // A partial cache is not a success flag. Validate resumed/reused bytes before counting
      // them; a browser eviction or damaged entry must be repaired by the same download.
      for (const file of value.files) {
        const url = new URL(file.path, base).href;
        if (!known.has(url)) continue;
        signal.throwIfAborted();
        const response = await cache.match(url);
        const bytes = response && (await response.arrayBuffer());
        const hash =
          bytes &&
          [...new Uint8Array(await crypto.subtle.digest("SHA-256", bytes))]
            .map((byte) => byte.toString(16).padStart(2, "0"))
            .join("");
        if (!bytes || bytes.byteLength !== file.size || hash !== file.sha256) {
          await cache.delete(url);
          known.delete(url);
        }
      }
      let done = 0;
      let last = 0;
      const report = (force = false) => {
        if (force || Date.now() - last > 100) {
          last = Date.now();
          progress(done);
        }
      };
      for (const file of value.files)
        if (known.has(new URL(file.path, base).href)) done += file.size;
      report(true);
      const pending = value.files.filter((file) => !known.has(new URL(file.path, base).href));
      // Abort sibling downloads on failure and wait for them before releasing the cross-tab lock.
      const group = new AbortController();
      const combined = AbortSignal.any([signal, group.signal]);
      let failure;
      const fetchFiles = async () => {
        while (pending.length) {
          combined.throwIfAborted();
          const file = pending.shift();
          const url = new URL(file.path, base).href;
          const response = await fetch(url, {
            cache: "reload",
            signal: combined,
            headers: { "X-MS-Offline-Download": "1" },
          });
          if (!response.ok || !response.body) throw Error(`Download failed: ${file.path}`);
          const reader = response.body.getReader();
          const chunks = [];
          let length = 0;
          for (;;) {
            const { done: finished, value: chunk } = await reader.read();
            if (finished) break;
            chunks.push(chunk);
            length += chunk.length;
            done += chunk.length;
            report();
          }
          if (length !== file.size) throw Error(`File changed: ${file.path}`);
          const bytes = new Uint8Array(length);
          let offset = 0;
          for (const chunk of chunks) {
            bytes.set(chunk, offset);
            offset += chunk.length;
          }
          const hash = [...new Uint8Array(await crypto.subtle.digest("SHA-256", bytes))]
            .map((byte) => byte.toString(16).padStart(2, "0"))
            .join("");
          if (hash !== file.sha256) throw Error(`File changed: ${file.path}`);
          const headers = new Headers(response.headers);
          headers.delete("content-encoding");
          headers.set("content-length", String(length));
          combined.throwIfAborted();
          await cache.put(url, new Response(bytes, { headers }));
          report(true);
        }
      };
      await Promise.all(
        Array.from({ length: 4 }, () =>
          fetchFiles().catch((error) => {
            failure ??= error;
            group.abort();
          }),
        ),
      );
      if (failure) throw failure;
      signal.throwIfAborted();
      await cache.put(manifestURL, Response.json(value));
      // This single write publishes the complete snapshot. No half-downloaded release is served.
      await meta.put(
        stateURL,
        Response.json(
          prepare
            ? { ...prior, pending: value.version }
            : { version: value.version, previous: fallback },
        ),
      );
      // Retain complete snapshots used by other open windows. Removal is explicitly scoped.
      report(true);
    });
  }
  async function select(version) {
    await navigator.locks.request(prefix, async () => {
      const meta = await caches.open(`${prefix}meta`);
      const record = await meta.match(stateURL);
      const state = record ? await record.json() : {};
      if (version !== state.pending && version !== state.version)
        throw Error("Update no longer ready");
      const cache = await caches.open(`${prefix}${version}`);
      const response = await cache.match(manifestURL);
      if (!response) throw Error("Update missing");
      const value = validate(await response.json());
      for (const file of value.files)
        if (!(await cache.match(new URL(file.path, base).href))) throw Error("Update incomplete");
      await meta.put(stateURL, Response.json({ version, previous: state.version }));
    });
  }
  async function loaded(build) {
    if (!supported() || !/^[a-f0-9]{20}$/.test(build)) return;
    let version = build;
    for (const name of await caches.keys()) {
      if (!name.startsWith(prefix) || name === `${prefix}meta`) continue;
      const response = await (await caches.open(name)).match(manifestURL);
      if (response) {
        const value = await response.json();
        if (value.release?.build === build) {
          version = value.version;
          break;
        }
      }
    }
    await bind(version);
  }
  async function bind(version) {
    const controller = navigator.serviceWorker?.controller;
    if (!controller || !version) return;
    await new Promise((resolve, reject) => {
      const channel = new MessageChannel();
      const timer = setTimeout(() => {
        channel.port1.close();
        reject(Error("Release binding timed out"));
      }, 5000);
      channel.port1.onmessage = () => {
        clearTimeout(timer);
        channel.port1.close();
        resolve();
      };
      controller.postMessage({ type: "MS_OFFLINE_BIND", version }, [channel.port2]);
    });
  }
  async function remove() {
    await navigator.locks.request(prefix, { ifAvailable: true }, async (lock) => {
      if (!lock) throw Error("Another tab is changing the offline download");
      await (await caches.open(`${prefix}meta`)).delete(stateURL);
      for (const name of await caches.keys())
        if (name.startsWith(prefix) && name !== `${prefix}meta`) await caches.delete(name);
    });
  }

  return { supported, manifest, snapshot, register, download, select, bind, loaded, remove };
}
