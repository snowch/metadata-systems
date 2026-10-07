// Copyright © 2026 Christopher Snow

// The theme follows the system unless the learner picks one; the choice is kept in this browser.

import { useEffect, useState } from "react";

export type Theme = "auto" | "light" | "dark";
const KEY = "ms:v1:theme";

function read(): Theme {
  try {
    const v = localStorage.getItem(KEY);
    return v === "light" || v === "dark" ? v : "auto";
  } catch {
    return "auto";
  }
}

/** Each theme-color tag's own colour, as index.html gives it, kept before a choice changes it. */
const own = new WeakMap<HTMLMetaElement, string>();

/**
 * The browser's own bar takes the header's colour in the theme the page shows. index.html gives
 * one colour for each system scheme; a learner's choice gives every tag the chosen theme's colour.
 */
function paintBar(theme: Theme): void {
  const tags = [...document.querySelectorAll<HTMLMetaElement>('meta[name="theme-color"]')];
  for (const tag of tags) if (!own.has(tag)) own.set(tag, tag.content);
  const chosen = tags.find((tag) => (tag.getAttribute("media") ?? "").includes(theme));
  for (const tag of tags) {
    const colour = theme === "auto" ? own.get(tag) : chosen && own.get(chosen);
    if (colour) tag.content = colour;
  }
}

export function useTheme(): [Theme, (t: Theme) => void] {
  const [theme, setTheme] = useState<Theme>(read);
  useEffect(() => {
    const root = document.documentElement;
    if (theme === "auto") root.removeAttribute("data-theme");
    else root.setAttribute("data-theme", theme);
    paintBar(theme);
    try {
      if (theme === "auto") localStorage.removeItem(KEY);
      else localStorage.setItem(KEY, theme);
    } catch {
      // No storage: the choice lasts for the visit.
    }
  }, [theme]);
  return [theme, setTheme];
}
