// Copyright © 2026 Christopher Snow

import { appStatus } from "../../offline/status.js";

const valid = (commit) => typeof commit === "string" && /^[a-f0-9]{40}$/.test(commit);

export function releaseState(loaded, deployed) {
  if (!valid(loaded) || !valid(deployed)) return "cannotCheck";
  return loaded === deployed ? "latest" : "updateAvailable";
}

// The loaded commit comes from the HTML, not a fetched config which may already be newer.
// Only a successful network comparison earns a tick; an offline snapshot cannot prove freshness.
export function releaseIndicator(base, options = {}) {
  return appStatus(options.courseBase || new URL("../", base).href, {
    ...options,
    releaseURL: new URL("release.json", base),
  });
}
