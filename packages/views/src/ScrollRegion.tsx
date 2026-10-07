// Copyright © 2026 Christopher Snow

// A box that scrolls sideways inside the page, never the page itself, and says so: when its
// contents are wider than the box, a line above it tells the reader to scroll. The box can be
// reached and scrolled with the keyboard. A screen reader reads the whole table either way, so the
// line is hidden from it. A table's title sits above the box, where it wraps to the figure's
// width; a caption inside the box would scroll away with the rows and be cut at the box's edge,
// so there the caption is kept for a screen reader only, and the title is hidden from one.

import { useEffect, useRef, useState, type ReactNode } from "react";

import { useViewStrings } from "./strings";

export function ScrollRegion({
  label,
  title,
  children,
}: {
  /** The region's accessible name: usually the caption of the table inside it. */
  label: string;
  /** Shown above the box: the table's caption, which the box's own styles hide. */
  title?: string;
  children: ReactNode;
}) {
  const strings = useViewStrings();
  const ref = useRef<HTMLDivElement>(null);
  const [overflows, setOverflows] = useState(false);
  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const check = () => setOverflows(el.scrollWidth > el.clientWidth + 1);
    check();
    if (typeof ResizeObserver === "undefined") return;
    const observer = new ResizeObserver(check);
    observer.observe(el);
    if (el.firstElementChild) observer.observe(el.firstElementChild);
    return () => observer.disconnect();
  }, []);
  return (
    <>
      {title && (
        <p className="scroll-title" aria-hidden="true">
          {title}
        </p>
      )}
      {overflows && (
        <p className="scroll-cue" aria-hidden="true">
          {strings.scrollCue}
        </p>
      )}
      <div
        ref={ref}
        className="data-scroll"
        role="region"
        aria-label={label}
        tabIndex={0}
        data-overflows={overflows ? "true" : "false"}
      >
        {children}
      </div>
    </>
  );
}
