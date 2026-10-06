// Copyright © 2026 Christopher Snow

// The course's visual vocabulary: one small mark per kind of thing, always beside its name, so a
// mark never carries meaning alone. Chapter 1 needs three: a file, a table and a dashboard. Later
// chapters add a job, a run, an event, a column, an observation, an owner and a version, each
// drawn once here.

import type { AssetKind } from "@ms/lab";

const PATHS: Record<AssetKind, string> = {
  // A page with a folded corner.
  file: "M4 1.5h6l3.5 3.5v9.5h-9.5z M10 1.5v3.5h3.5",
  // A grid of rows under a header.
  table: "M2 3h12v10h-12z M2 6.2h12 M2 9.4h12 M6.5 6.2v6.8",
  // A frame with three bars.
  dashboard: "M2 2.5h12v11h-12z M5 11v-3 M8 11v-5.5 M11 11v-4",
};

export function Glyph({ kind }: { kind: AssetKind }) {
  return (
    <svg
      className={`glyph glyph-${kind}`}
      viewBox="0 0 16 16"
      width="16"
      height="16"
      aria-hidden="true"
      focusable="false"
    >
      <path
        d={PATHS[kind]}
        fill="none"
        stroke="currentColor"
        strokeWidth="1.3"
        strokeLinejoin="round"
      />
    </svg>
  );
}
