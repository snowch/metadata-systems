// Copyright © 2026 Christopher Snow

import { useEffect, useRef, useState } from "react";
import { fill } from "../fill";
import { STRINGS } from "../strings";
import { base, download, manifest, register, remove, snapshot, supported } from "../offline";
import type { Manifest, Snapshot } from "../offline";
import { activateWorker } from "../../../../offline/activate.js";

const words = STRINGS.offline;
const mb = (bytes: number) => (bytes / 1e6).toFixed(1);

export function Offline() {
  const [available, setAvailable] = useState<Manifest | null>(null);
  const [saved, setSaved] = useState<Snapshot>({ ready: false });
  const [online, setOnline] = useState(navigator.onLine);
  const [reloadReady, setReloadReady] = useState(false);
  const [busy, setBusy] = useState(false);
  const [done, setDone] = useState(0);
  const [message, setMessage] = useState("");
  const stop = useRef<AbortController | null>(null);
  const canUse = supported();

  useEffect(() => {
    let alive = true;
    const refresh = async () => {
      try {
        const latest = await manifest();
        if (!alive) return;
        setAvailable(latest);
        setOnline(navigator.onLine);
        if (latest && canUse) {
          await register();
          const current = await snapshot();
          if (alive) setSaved(current);
        }
      } catch {
        if (alive) setMessage(words.failed);
      }
    };
    void refresh();
    const updates =
      typeof BroadcastChannel === "undefined"
        ? null
        : new BroadcastChannel(`ms:metadata-systems:updates:${base}`);
    updates?.addEventListener("message", (event) => {
      if (alive && event.data?.type === "ready") {
        setReloadReady(true);
        setMessage(words.updated);
        void refresh();
      }
    });
    const connection = () => {
      setOnline(navigator.onLine);
      setMessage("");
      void refresh();
    };
    window.addEventListener("online", connection);
    window.addEventListener("offline", connection);
    window.addEventListener("focus", connection);
    return () => {
      alive = false;
      updates?.close();
      window.removeEventListener("online", connection);
      window.removeEventListener("offline", connection);
      window.removeEventListener("focus", connection);
    };
  }, [canUse]);

  if (!available) return null;
  const update = saved.ready && saved.version !== available.version;
  const status = !canUse
    ? words.unsupported
    : message ||
      (saved.ready
        ? update && online
          ? words.updateAvailable
          : online
            ? words.ready
            : words.offlineReady
        : online
          ? ""
          : words.incomplete);

  const begin = async () => {
    const controller = new AbortController();
    stop.current = controller;
    setBusy(true);
    setDone(0);
    setMessage("");
    try {
      await download(available, controller.signal, setDone);
      setSaved(await snapshot());
      setMessage(update ? words.updated : words.ready);
      if (update) {
        setReloadReady(true);
        try {
          const response = await fetch(new URL("jupyterlite/release.json", base), {
            cache: "no-store",
            headers: { "X-MS-Offline-Download": "release-check" },
          });
          if (response.ok) {
            const release = await response.json();
            const updates =
              typeof BroadcastChannel === "undefined"
                ? null
                : new BroadcastChannel(`ms:metadata-systems:updates:${base}`);
            updates?.postMessage({ type: "ready", commit: release.commit });
            updates?.close();
          }
        } catch {
          /* A notification failure must not invalidate a verified download. */
        }
      }
    } catch {
      setMessage(controller.signal.aborted ? words.cancelled : words.failed);
      setSaved(await snapshot().catch(() => ({ ready: false })));
      const latest = await manifest().catch(() => null);
      if (latest) setAvailable(latest);
    } finally {
      setBusy(false);
      stop.current = null;
    }
  };
  const reload = async () => {
    setBusy(true);
    try {
      await activateWorker(new URL("offline-worker.js", base));
      window.location.reload();
    } catch {
      setMessage(words.failed);
      setBusy(false);
    }
  };
  const clear = async () => {
    setBusy(true);
    try {
      await remove();
      setSaved({ ready: false });
      setReloadReady(false);
      setMessage("");
    } catch {
      setMessage(words.failed);
    } finally {
      setBusy(false);
    }
  };

  return (
    <section className="offline-course" aria-labelledby="offline-title">
      <h2 id="offline-title">{words.title}</h2>
      <p>{words.intro}</p>
      <p>{fill(words.size, { size: mb(available.bytes) })}</p>
      <div className="offline-actions">
        {reloadReady && (
          <button className="button" disabled={busy} onClick={() => void reload()}>
            {words.reload}
          </button>
        )}
        {canUse && (!saved.ready || update) && (
          <button className="button" disabled={busy || !online} onClick={() => void begin()}>
            {update ? words.update : words.download}
          </button>
        )}
        {busy && stop.current && (
          <button className="button" onClick={() => stop.current?.abort()}>
            {words.cancel}
          </button>
        )}
        {canUse && (saved.ready || saved.hasDownload) && (
          <button className="button" disabled={busy} onClick={() => void clear()}>
            {words.remove}
          </button>
        )}
      </div>
      {busy && stop.current && (
        <div>
          <progress
            max={available.bytes}
            value={Math.min(done, available.bytes)}
            aria-label={words.progressLabel}
          />
          <p>{fill(words.progress, { done: mb(done), total: mb(available.bytes) })}</p>
        </div>
      )}
      <p role="status" aria-live="polite" data-offline-ready={saved.ready}>
        {status}
      </p>
      <p className="offline-note">{words.storageNote}</p>
    </section>
  );
}
