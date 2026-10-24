// Copyright © 2026 Christopher Snow

import words from "./status-words.json";
import { createOffline } from "./client.js";
import { activateWorker } from "./activate.js";

export const validCommit = (value) => typeof value === "string" && /^[a-f0-9]{40}$/.test(value);
export const validBuild = (value) => typeof value === "string" && /^[a-f0-9]{20}$/.test(value);
export function validateRelease(value) {
  if (
    !value ||
    (value.commit !== "" && value.commit !== null && !validCommit(value.commit)) ||
    value.schema !== 1 ||
    !validBuild(value.build)
  )
    throw Error("Invalid deployed release");
  return value;
}

// Framework-free adapter: the same controls, state and safety rules serve both app shells.
export function appStatus(
  base,
  {
    blocked = () => null,
    workerURL = new URL("offline-worker.js", base),
    resize = () => {},
    releaseURL = new URL("release.json", base),
  } = {},
) {
  base = String(base);
  const offline = createOffline(base);
  const commit = document.querySelector('meta[name="ms-commit"]')?.content;
  const build = document.querySelector('meta[name="ms-build"]')?.content;
  const node = document.createElement("div");
  node.className = "ms-AppStatus ms-Release";
  const trigger = document.createElement("button");
  trigger.type = "button";
  trigger.setAttribute("aria-haspopup", "dialog");
  const identity = document.createElement("a");
  identity.textContent = validCommit(commit)
    ? commit.slice(0, 7)
    : validBuild(build)
      ? build.slice(0, 7)
      : words.unknownVersion;
  if (validCommit(commit)) {
    identity.href = `https://github.com/snowch/metadata-systems/commit/${commit}`;
    identity.target = "_blank";
    identity.rel = "noopener";
  }
  node.append(trigger, identity);
  const sizeObserver = new ResizeObserver(() => {
    const height = `${Math.ceil(Math.max(52, trigger.getBoundingClientRect().height + 8))}px`;
    node.style.minHeight = node.style.maxHeight = height;
    resize();
  });
  sizeObserver.observe(trigger);
  const dialog = document.createElement("dialog");
  dialog.className = "ms-AppStatus-dialog jp-ThemedContainer";
  dialog.setAttribute("aria-label", words.title);
  const make = (tag, text, parent = dialog) => {
    const el = document.createElement(tag);
    if (text) el.textContent = text;
    parent.append(el);
    return el;
  };
  make("h2", words.title);
  const close = make("button", words.close);
  close.type = "button";
  close.onclick = () => dialog.close();
  make("h3", words.version);
  make(
    "p",
    words.loadedVersion.replace(
      "{commit}",
      validBuild(build) ? `${identity.textContent} · ${build}` : identity.textContent,
    ),
  );
  const versionState = make("p");
  versionState.setAttribute("role", "status");
  const actions = make("div");
  const button = (text, action, parent = actions) => {
    const el = make("button", text, parent);
    el.type = "button";
    el.addEventListener("click", action);
    return el;
  };
  const checkButton = button(words.check, () => void check(true));
  const update = button(words.update, () => void begin(true));
  const restart = button(words.restart, () => void reload());
  const later = button(words.later, () => dialog.close());
  make("p", words.restartHelp);
  make("h3", words.offlineAccess);
  const offlineState = make("p");
  offlineState.setAttribute("role", "status");
  make("p", offline.supported() ? words.offlineHelp : words.offlineUnavailableHelp);
  make("p", words.storageNote);
  const size = make("p");
  const download = button(words.download, () => void begin(false), dialog);
  const remove = button(
    words.remove,
    () => {
      confirm.hidden = false;
      confirmYes.focus();
    },
    dialog,
  );
  const confirm = make("div");
  confirm.hidden = true;
  make("p", words.removeConfirm, confirm);
  const confirmYes = button(
    words.remove,
    async () => {
      confirm.hidden = true;
      try {
        await offline.remove();
        pending = null;
        state = latest && latest.build === build ? "upToDate" : "updateAvailable";
        say(words.removed);
        await refresh();
      } catch {
        say(words.removeFailed);
      }
    },
    confirm,
  );
  button(
    words.keep,
    () => {
      confirm.hidden = true;
      remove.focus();
    },
    confirm,
  );
  const progress = make("progress");
  progress.setAttribute("aria-label", words.progressLabel);
  progress.hidden = true;
  const cancel = button(words.cancelDownload, () => operation?.abort(), dialog);
  const message = make("p");
  message.setAttribute("role", "status");
  document.body.append(dialog);
  let disposed = false,
    request,
    operation,
    latest,
    available,
    pending,
    composing = false;
  let state = "checking",
    saved = { ready: false },
    lastCheck = 0;
  const channel =
    typeof BroadcastChannel === "undefined"
      ? null
      : new BroadcastChannel(`ms:metadata-systems:updates:${base}`);
  const write = (element, text) => {
    if (element.textContent !== text) element.textContent = text;
  };
  const say = (text) => write(message, text);
  function render() {
    node.dataset.state = pending ? "ready" : state;
    write(trigger, `${words.title} · ${pending ? words.updateReady : words[state]}`);
    write(versionState, pending ? words.updateReady : words[state]);
    write(checkButton, state === "checkFailed" ? words.retry : words.check);
    checkButton.disabled = !!request || !!operation;
    update.hidden = !!pending || state !== "updateAvailable";
    update.disabled = !!operation || navigator.onLine === false;
    restart.hidden = later.hidden = !pending;
    restart.disabled = !!operation || !!blocked() || composing;
    offlineState.dataset.offlineReady = String(saved.ready);
    write(
      offlineState,
      !offline.supported()
        ? words.offlineUnavailable
        : operation && operation.kind === "offline"
          ? words.saving
          : saved.ready
            ? words.availableOffline
            : saved.hasDownload && !pending
              ? words.incomplete
              : words.notSaved,
    );
    write(download, saved.hasDownload && !saved.ready ? words.resume : words.download);
    download.hidden = saved.ready || !!pending || !offline.supported();
    download.disabled = !!operation || !available || navigator.onLine === false;
    remove.hidden = !saved.hasDownload;
    remove.disabled = !!operation;
    cancel.hidden = !operation || operation.kind === "restart";
    progress.hidden = !operation;
    write(size, available ? words.size.replace("{size}", (available.bytes / 1e6).toFixed(1)) : "");
    resize();
  }
  async function refresh() {
    if (disposed) return;
    try {
      if (offline.supported()) {
        if (validBuild(build)) await offline.loaded(build);
        saved = await offline.snapshot();
        if (!saved.hasDownload) pending = null;
        if (saved.pendingIncomplete || (pending === saved.version && !saved.ready)) {
          pending = null;
          if (!operation) {
            state = "updateAvailable";
            say(words.updateFailed);
          }
        }
        if (saved.pending) pending = saved.pending;
      }
      available = await offline.manifest();
    } catch {
      saved = { ready: false };
      pending = null;
      say(words.offlineCheckFailed);
    }
    if (!disposed) render();
  }
  async function check(force = false) {
    if (disposed || request || operation || document.visibilityState === "hidden") return;
    if (navigator.onLine === false) {
      state = "cannotCheck";
      render();
      return;
    }
    if (!force && Date.now() - lastCheck < 5000) return;
    lastCheck = Date.now();
    const controller = new AbortController();
    request = controller;
    const timer = setTimeout(() => controller.abort(), 8000);
    state = "checking";
    render();
    try {
      const response = await fetch(releaseURL, {
        cache: "no-store",
        headers: { "X-MS-Offline-Download": "release-check" },
        signal: controller.signal,
      });
      if (!response.ok) throw Error("Release unavailable");
      const release = validateRelease(await response.json());
      if (disposed || controller.signal.aborted || request !== controller) return;
      latest = release;
      state = validBuild(build)
        ? build === release.build && (!validCommit(commit) || commit === release.commit)
          ? "upToDate"
          : "updateAvailable"
        : "unknownVersion";
    } catch {
      if (!disposed && request === controller)
        state = navigator.onLine === false ? "cannotCheck" : "checkFailed";
    } finally {
      clearTimeout(timer);
      if (request === controller) request = null;
      if (!disposed) render();
    }
  }
  async function begin(isUpdate) {
    if (operation || disposed) return;
    const controller = new AbortController();
    controller.kind = isUpdate ? "update" : "offline";
    operation = controller;
    progress.removeAttribute("value");
    if (isUpdate) state = "downloadingUpdate";
    say("");
    render();
    try {
      const value = await offline.manifest(true);
      if (!value || (latest && isUpdate && value.release?.build !== latest.build))
        throw Error("Release changed; check again");
      available = value;
      const prepare = isUpdate || (validBuild(build) && value.release?.build !== build);
      await offline.download(
        value,
        controller.signal,
        (bytes) => {
          progress.max = value.bytes;
          progress.value = bytes;
          say(
            words.progress
              .replace("{done}", (bytes / 1e6).toFixed(1))
              .replace("{total}", (value.bytes / 1e6).toFixed(1)),
          );
        },
        prepare,
      );
      controller.signal.throwIfAborted();
      if (prepare) {
        pending = value.version;
        channel?.postMessage({ type: "ready", version: pending, commit: value.release?.commit });
      }
      say(prepare ? words.updateReady : words.availableOffline);
    } catch {
      say(controller.signal.aborted ? words.cancelled : words.downloadFailed);
      if (isUpdate) state = "updateAvailable";
    } finally {
      operation = null;
      await refresh();
    }
  }
  async function reload() {
    const reason = blocked();
    if (operation || !pending || reason || composing) {
      say(reason === "busy" ? words.busy : words.unsaved);
      return;
    }
    const controller = new AbortController();
    controller.kind = "restart";
    operation = controller;
    say(words.restarting);
    render();
    try {
      await activateWorker(workerURL);
      controller.signal.throwIfAborted();
      if (disposed) return;
      if (blocked() || composing) throw Error("Unsafe restart");
      await offline.select(pending);
      controller.signal.throwIfAborted();
      if (disposed) return;
      if (blocked() || composing) throw Error("Unsafe restart");
      // Same URL preserves the chapter, section, installed-window path and query string.
      window.location.reload();
    } catch {
      say(words.restartFailed);
      operation = null;
      render();
    }
  }
  trigger.onclick = () => {
    dialog.showModal();
    void check(true);
    void refresh();
  };
  dialog.addEventListener("close", () => trigger.focus());
  const compositionStart = () => {
    composing = true;
    render();
  };
  const compositionEnd = () => {
    composing = false;
    render();
  };
  const offlineEvent = () => {
    const stale = request;
    request = null;
    lastCheck = 0;
    stale?.abort();
    state = "cannotCheck";
    render();
  };
  const visible = () => {
    if (document.visibilityState !== "hidden") {
      void check();
      void refresh();
    }
  };
  channel?.addEventListener("message", (event) => {
    if (event.data?.type === "ready" && validBuild(event.data.version)) {
      pending = event.data.version;
      render();
    }
  });
  navigator.serviceWorker?.addEventListener("controllerchange", visible);
  window.addEventListener("online", visible);
  window.addEventListener("offline", offlineEvent);
  window.addEventListener("focus", visible);
  document.addEventListener("visibilitychange", visible);
  document.addEventListener("compositionstart", compositionStart);
  document.addEventListener("compositionend", compositionEnd);
  const timer = setInterval(() => void check(), 60000);
  const guards = setInterval(() => {
    if (dialog.open) render();
  }, 500);
  render();
  void check();
  void refresh();
  return {
    node,
    open: () => trigger.click(),
    dispose() {
      sizeObserver.disconnect();
      disposed = true;
      request?.abort();
      operation?.abort();
      channel?.close();
      clearInterval(timer);
      clearInterval(guards);
      navigator.serviceWorker?.removeEventListener("controllerchange", visible);
      window.removeEventListener("online", visible);
      window.removeEventListener("offline", offlineEvent);
      window.removeEventListener("focus", visible);
      document.removeEventListener("visibilitychange", visible);
      document.removeEventListener("compositionstart", compositionStart);
      document.removeEventListener("compositionend", compositionEnd);
      dialog.remove();
      node.remove();
    },
  };
}
