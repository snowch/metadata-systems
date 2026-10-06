// Copyright © 2026 Christopher Snow

// Hash routes, so the site works from GitHub Pages without server rules: `#/` is the front page
// and `#/chapter/<id>` a chapter.

import { useEffect, useState } from "react";

export type Route =
  { kind: "list" } | { kind: "chapter"; id: string } | { kind: "missing"; path: string };

export function parseRoute(hash: string): Route {
  const path = hash.replace(/^#/, "") || "/";
  if (path === "/" || path === "") return { kind: "list" };
  const m = /^\/chapter\/([a-z][a-z0-9-]*)\/?$/.exec(path);
  if (m) return { kind: "chapter", id: m[1] as string };
  return { kind: "missing", path };
}

export const chapterHref = (id: string) => `#/chapter/${id}`;

export function useRoute(): Route {
  const [route, setRoute] = useState<Route>(() => parseRoute(window.location.hash));
  useEffect(() => {
    // A page reached by following a link starts at its top, with focus on the page, so the
    // keyboard and a screen reader start there too. Back and Forward keep the browser's place.
    let followed = false;
    const onClick = (e: MouseEvent) => {
      const link = e.target instanceof Element ? e.target.closest("a") : null;
      if (link?.getAttribute("href")?.startsWith("#/")) followed = true;
    };
    const onChange = () => {
      setRoute(parseRoute(window.location.hash));
      if (!followed) return;
      followed = false;
      window.scrollTo(0, 0);
      document.getElementById("main")?.focus({ preventScroll: true });
    };
    document.addEventListener("click", onClick);
    window.addEventListener("hashchange", onChange);
    return () => {
      document.removeEventListener("click", onClick);
      window.removeEventListener("hashchange", onChange);
    };
  }, []);
  return route;
}
