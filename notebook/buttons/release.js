// Copyright © 2026 Christopher Snow

import words from "./release-words.json";
import { createOffline } from "../../offline/client.js";
import { activateWorker } from "../../offline/activate.js";

const valid = (commit) => typeof commit === "string" && /^[a-f0-9]{40}$/.test(commit);

export function releaseState(loaded, deployed) {
  if (!valid(loaded) || !valid(deployed)) return "cannotCheck";
  return loaded === deployed ? "latest" : "updateAvailable";
}

// The loaded commit comes from the HTML, not a fetched config which may already be newer.
// Only a successful network comparison earns a tick; an offline snapshot cannot prove freshness.
export function releaseIndicator(
  base,
  {
    workerURL = new URL("python-worker.js", base),
    courseBase = new URL("../", base).href,
    blocked = () => null,
    resize = () => {},
  } = {},
) {
  const commit = document.querySelector('meta[name="ms-commit"]')?.content;
  const node = document.createElement("div");
  node.className = "ms-Release";
  // Lumino's notebook header resets widget size limits; reserve this line explicitly.
  node.style.minHeight = "24px";
  node.style.maxHeight = "24px";
  const body = document.createElement("div");
  body.className = "ms-Release-body";
  node.append(body);
  const link = document.createElement("a");
  link.target = "_blank";
  link.rel = "noopener";
  if (valid(commit)) link.href = `https://github.com/snowch/metadata-systems/commit/${commit}`;
  const action = document.createElement("button");
  action.type = "button";
  action.hidden = true;
  action.title = words.help;
  const cancel = document.createElement("button");
  cancel.type = "button";
  cancel.textContent = words.cancel;
  cancel.hidden = true;
  const message = document.createElement("span");
  message.className = "ms-Release-message";
  message.setAttribute("role", "status");
  message.hidden = true;
  body.append(link, action, cancel, message);
  const size = new ResizeObserver(() => {
    const height = `${Math.ceil(body.getBoundingClientRect().height)}px`;
    if (node.style.minHeight === height) return;
    node.style.minHeight = height;
    node.style.maxHeight = height;
    resize();
  });
  size.observe(body);
  const offline = createOffline(courseBase);
  const channel =
    typeof BroadcastChannel === "undefined"
      ? null
      : new BroadcastChannel(`ms:metadata-systems:updates:${courseBase}`);
  let busy = false;
  let ready = false;
  let latest;
  let abort;
  const say = (text) => {
    message.textContent = text;
    message.hidden = !text;
  };
  const controls = () => {
    action.textContent = ready ? words.reload : words.update;
    action.hidden = !ready && node.dataset.state !== "updateAvailable";
    action.disabled = busy || blocked() === "busy";
    cancel.hidden = !busy || !abort;
  };
  const changed = (event) => {
    if (event.data?.type !== "ready" || !valid(event.data.commit) || event.data.commit === commit)
      return;
    ready = true;
    say(words.ready);
    controls();
  };
  channel?.addEventListener("message", changed);
  cancel.addEventListener("click", () => abort?.abort());
  const reload = () => {
    if (disposed) return;
    const reason = blocked();
    if (reason) {
      say(reason === "busy" ? words.pythonBusy : words.unsavedEdits);
      return;
    }
    window.location.reload();
  };
  action.addEventListener("click", async () => {
    if (busy) return;
    const reason = blocked();
    if (reason) {
      say(reason === "busy" ? words.pythonBusy : words.unsavedEdits);
      return;
    }
    busy = true;
    abort = new AbortController();
    controls();
    try {
      if (!ready) {
        const response = await fetch(new URL("release.json", base), {
          cache: "no-store",
          headers: { "X-MS-Offline-Download": "release-check" },
          signal: AbortSignal.any([abort.signal, AbortSignal.timeout(8000)]),
        });
        const release = response.ok ? await response.json() : null;
        if (!valid(release?.commit)) throw new Error("No current release");
        latest = release.commit;
      }
      if (!ready && offline.supported() && (await offline.snapshot()).version) {
        const manifest = await offline.manifest(true);
        if (!manifest) throw new Error("No current manifest");
        await offline.download(manifest, abort.signal, (bytes) =>
          say(
            words.progress.replace(
              "{percent}",
              String(Math.min(100, Math.floor((bytes / manifest.bytes) * 100))),
            ),
          ),
        );
      }
      abort.signal.throwIfAborted();
      abort = null;
      controls();
      say(words.activating);
      await activateWorker(workerURL);
      ready = true;
      channel?.postMessage({ type: "ready", commit: latest });
      reload();
    } catch {
      say(abort?.signal.aborted ? words.cancelled : words.failed);
    } finally {
      busy = false;
      abort = null;
      controls();
    }
  });
  const render = (state) => {
    node.dataset.state = state;
    link.textContent = words[state].replace("{commit}", valid(commit) ? commit.slice(0, 7) : "?");
    controls();
  };
  let disposed = false;
  let request;
  const check = async () => {
    if (disposed || busy || request || document.visibilityState === "hidden") return;
    if (navigator.onLine === false) {
      render("cannotCheck");
      return;
    }
    const controller = new AbortController();
    request = controller;
    const timer = setTimeout(() => controller.abort(), 8000);
    render("checking");
    try {
      const response = await fetch(new URL("release.json", base), {
        cache: "no-store",
        // Existing course workers already pass download requests straight to the network.
        // This also avoids a false tick when upgrading from an older offline worker.
        headers: { "X-MS-Offline-Download": "release-check" },
        signal: controller.signal,
      });
      if (!response.ok) throw new Error("Release check failed");
      const release = await response.json();
      latest = release.commit;
      const state = releaseState(commit, release.commit);
      if (state === "latest" && "serviceWorker" in navigator) {
        const registrations = await navigator.serviceWorker.getRegistrations().catch(() => []);
        if (
          registrations.some(
            (registration) => registration.waiting?.scriptURL === String(workerURL),
          )
        ) {
          ready = true;
          say(words.ready);
        }
      }
      if (!disposed) render(state);
    } catch {
      if (!disposed) render("cannotCheck");
    } finally {
      clearTimeout(timer);
      request = undefined;
    }
  };
  const unknown = () => {
    request?.abort();
    render("cannotCheck");
  };
  render("checking");
  void check();
  const repeat = setInterval(check, 60000);
  const usability = setInterval(controls, 500);
  window.addEventListener("online", check);
  window.addEventListener("offline", unknown);
  window.addEventListener("focus", check);
  document.addEventListener("visibilitychange", check);
  return {
    node,
    dispose() {
      disposed = true;
      request?.abort();
      clearInterval(repeat);
      clearInterval(usability);
      size.disconnect();
      channel?.close();
      abort?.abort();
      window.removeEventListener("online", check);
      window.removeEventListener("offline", unknown);
      window.removeEventListener("focus", check);
      document.removeEventListener("visibilitychange", check);
    },
  };
}
