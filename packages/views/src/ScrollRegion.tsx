// Copyright © 2026 Christopher Snow

// A box that scrolls sideways inside the page, never the page itself, and says so: when its
// contents are wider than the box, a line above it tells the reader to scroll. The box can be
// reached and scrolled with the keyboard. A screen reader reads the whole table either way, so the
// line is hidden from it.

import { useEffect, useRef, useState, type ReactNode } from "react";

import { useViewStrings } from "./strings";

export function ScrollRegion({
  label,
  children,
}: {
  /** The region's accessible name: usually the caption of the table inside it. */
  label: string;
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
