// Copyright © 2026 Christopher Snow

// The shop's data platform at a glance: its systems in the order data moves through them each
// night, the assets each holds, and between them the programs a newcomer cannot see. Computed by
// the lab's platformMap, so it shows no asset made from another: that is what the chapter finds
// storage cannot tell.
//
// The map stays to hand through the chapter. Once the learner has scrolled past its place on the
// page, a button at the foot of the window opens the same map over the page, and closes it again;
// the button goes when the map's place comes back into view. Where the browser cannot tell what is
// in view, the map stays in its place alone.

import { useEffect, useRef, useState, type KeyboardEvent } from "react";
import { createPortal } from "react-dom";
import { z } from "zod";

import { CHANGE_IDS, platformMap, week, type PlatformMap as Map } from "@ms/lab";
import type { InteractiveProps } from "@platform/lesson-runtime";

import { Glyph } from "../Glyph";
import { withProps } from "../props";
import { useViewStrings, type ViewStrings } from "../strings";

const Props = z.object({
  changes: z.array(z.enum(CHANGE_IDS)).default([]),
  /** Whether the map stays to hand, from a button, once its place scrolls away. */
  dock: z.boolean().default(true),
});

function MapBody({ map, strings }: { map: Map; strings: ViewStrings }) {
  return (
    <ol className="platform-map" aria-label={strings.mapLabel}>
      {map.systems.map((s, i) => {
        const next = map.systems[i + 1];
        const flows = next && map.flows.some((f) => f.from === s.system && f.to === next.system);
        return (
          <li key={s.system} className="map-step">
            <div className="map-system">
              <p className="map-system-name">{strings.systems[s.system] ?? s.system}</p>
              <ul className="map-assets">
                {s.assets.map((a) => (
                  <li key={a.id} className="map-asset">
                    <Glyph kind={a.kind} />
                    <span>{a.id}</span>
                  </li>
                ))}
              </ul>
            </div>
            {flows && (
              <p className="map-flow">
                <svg
                  className="map-arrow"
                  viewBox="0 0 16 16"
                  width="16"
                  height="16"
                  aria-hidden="true"
                  focusable="false"
                >
                  <path
                    d="M8 1.5v12 M3.5 9l4.5 4.5 4.5-4.5"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="1.5"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  />
                </svg>
                <span>{strings.mapFlow}</span>
              </p>
            )}
          </li>
        );
      })}
    </ol>
  );
}

function Dock({ map, strings }: { map: Map; strings: ViewStrings }) {
  const [open, setOpen] = useState(false);
  const toggle = useRef<HTMLButtonElement>(null);
  const close = useRef<HTMLButtonElement>(null);
  useEffect(() => {
    if (open) close.current?.focus();
  }, [open]);
  const onKeyDown = (e: KeyboardEvent) => {
    if (e.key !== "Escape" || !open) return;
    setOpen(false);
    toggle.current?.focus();
  };
  return (
    <div className="map-dock" onKeyDown={onKeyDown}>
      {open && (
        <section id="map-dock-panel" className="map-dock-panel" aria-labelledby="map-dock-title">
          <div className="map-dock-head">
            <p id="map-dock-title" className="map-dock-title">
              {strings.mapLabel}
            </p>
            <button
              ref={close}
              type="button"
              className="button map-dock-close"
              onClick={() => {
                setOpen(false);
                toggle.current?.focus();
              }}
            >
              {strings.mapClose}
            </button>
          </div>
          <MapBody map={map} strings={strings} />
        </section>
      )}
      <button
        ref={toggle}
        type="button"
        className="button map-dock-toggle"
        aria-expanded={open}
        aria-controls="map-dock-panel"
        onClick={() => setOpen((o) => !o)}
      >
        {strings.mapOpen}
      </button>
    </div>
  );
}

export const PlatformMap = withProps(
  Props,
  function PlatformMap({ data }: InteractiveProps & { data: z.infer<typeof Props> }) {
    const strings = useViewStrings();
    const map = platformMap(week(data.changes));
    const place = useRef<HTMLDivElement>(null);
    const [away, setAway] = useState(false);
    useEffect(() => {
      const el = place.current;
      if (!data.dock || !el || typeof IntersectionObserver === "undefined") return;
      // Away means scrolled past: above the window. Below it, the learner has not reached it yet.
      // The watched area runs far below the window, so a jump from below the map to above it,
      // which never shows the map, still counts as leaving: the map can only leave upwards.
      const watch = new IntersectionObserver(
        ([entry]) => {
          if (entry) setAway(!entry.isIntersecting && entry.boundingClientRect.top < 0);
        },
        { rootMargin: "0px 0px 1000000px 0px" },
      );
      watch.observe(el);
      return () => watch.disconnect();
    }, [data.dock]);
    return (
      <div ref={place} className="platform-map-place">
        <MapBody map={map} strings={strings} />
        {away && createPortal(<Dock map={map} strings={strings} />, document.body)}
      </div>
    );
  },
);
