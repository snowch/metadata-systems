// Copyright © 2026 Christopher Snow

// The course's visual vocabulary: one small mark per kind of thing, always beside its name, so a
// mark never carries meaning alone. Chapter 1 needs three: a file, a table and a dashboard. Later
// chapters add a job, a run, an event, a column, an observation, an owner and a version, each
// drawn once here. The marks are Google's Material Symbols (Apache 2.0): "description" for a
// file, "table" for a table, "dashboard" for a dashboard, redrawn as paths so the page loads no
// icon font. A glyph is decoration beside the name: hidden from a screen reader, never the only
// way the kind is told, and smaller than the name it marks.
import type { AssetKind } from "@ms/lab";

/** The Material Symbols path for each kind, on the 960 grid the symbols are drawn on. */
const PATHS: Record<AssetKind, string> = {
  // "description": a page with lines of writing.
  file: "M240-80q-33 0-56.5-23.5T160-160v-640q0-33 23.5-56.5T240-880h287q16 0 30.5 6t25.5 17l194 194q11 11 17 25.5t6 30.5v447q0 33-23.5 56.5T720-80H240Zm280-560v-160H240v640h480v-440H560q-17 0-28.5-11.5T520-640ZM360-240h240q17 0 28.5-11.5T640-280q0-17-11.5-28.5T600-320H360q-17 0-28.5 11.5T320-280q0 17 11.5 28.5T360-240Zm0-160h240q17 0 28.5-11.5T640-440q0-17-11.5-28.5T600-480H360q-17 0-28.5 11.5T320-440q0 17 11.5 28.5T360-400Z",
  // "table": a grid of rows and columns.
  table:
    "M120-200v-560q0-33 23.5-56.5T200-840h560q33 0 56.5 23.5T840-760v560q0 33-23.5 56.5T760-120H200q-33 0-56.5-23.5T120-200Zm80-400h560v-160H200v160Zm213 200h134v-120H413v120Zm0 200h134v-120H413v120ZM200-400h133v-120H200v120Zm427 0h133v-120H627v120ZM200-200h133v-120H200v120Zm427 0h133v-120H627v120Z",
  // "dashboard": a frame of panes.
  dashboard:
    "M520-640v-160q0-17 11.5-28.5T560-840h240q17 0 28.5 11.5T840-800v160q0 17-11.5 28.5T800-600H560q-17 0-28.5-11.5T520-640ZM120-480v-320q0-17 11.5-28.5T160-840h240q17 0 28.5 11.5T440-800v320q0 17-11.5 28.5T400-440H160q-17 0-28.5-11.5T120-480Zm400 320v-320q0-17 11.5-28.5T560-520h240q17 0 28.5 11.5T840-480v320q0 17-11.5 28.5T800-120H560q-17 0-28.5-11.5T520-160Zm-400 0v-160q0-17 11.5-28.5T160-360h240q17 0 28.5 11.5T440-320v160q0 17-11.5 28.5T400-120H160q-17 0-28.5-11.5T120-160Z",
};

export function Glyph({ kind }: { kind: AssetKind }) {
  return (
    <svg
      className={`glyph glyph-${kind}`}
      viewBox="0 -960 960 960"
      width="14"
      height="14"
      aria-hidden="true"
      focusable="false"
    >
      <path d={PATHS[kind]} fill="currentColor" />
    </svg>
  );
}
