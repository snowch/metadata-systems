// Copyright © 2026 Christopher Snow

import words from "./release-words.json";

const valid = (commit) => typeof commit === "string" && /^[a-f0-9]{40}$/.test(commit);

export function releaseState(loaded, deployed) {
  if (!valid(loaded) || !valid(deployed)) return "cannotCheck";
  return loaded === deployed ? "latest" : "updateAvailable";
}

// The loaded commit comes from the HTML, not a fetched config which may already be newer.
// Only a successful network comparison earns a tick; an offline snapshot cannot prove freshness.
export function releaseIndicator(base) {
  const commit = document.querySelector('meta[name="ms-commit"]')?.content;
  const node = document.createElement("div");
  node.className = "ms-Release";
  // Lumino's notebook header resets widget size limits; reserve this line explicitly.
  node.style.minHeight = "24px";
  node.style.maxHeight = "24px";
  node.setAttribute("role", "status");
  const link = document.createElement("a");
  link.target = "_blank";
  link.rel = "noopener";
  if (valid(commit)) link.href = `https://github.com/snowch/metadata-systems/commit/${commit}`;
  node.append(link);
  const render = (state) => {
    node.dataset.state = state;
    link.textContent = words[state].replace("{commit}", valid(commit) ? commit.slice(0, 7) : "?");
  };
  let disposed = false;
  let request;
  const check = async () => {
    if (disposed || request || document.visibilityState === "hidden") return;
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
      if (!disposed) render(releaseState(commit, release.commit));
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
      window.removeEventListener("online", check);
      window.removeEventListener("offline", unknown);
      window.removeEventListener("focus", check);
      document.removeEventListener("visibilitychange", check);
    },
  };
}
