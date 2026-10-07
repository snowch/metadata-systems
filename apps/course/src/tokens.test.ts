// Copyright © 2026 Christopher Snow

// The colour tokens, held to WCAG 2.2 in each theme: text at 4.5:1 or more on every surface the
// stylesheets set it on, and a control's edge at 3:1 or more on the surfaces controls sit on
// (non-text contrast). Read from tokens.css itself, so a changed value is checked the day it
// lands; the explicit dark block is the one the dark theme's toggle uses, and the system-dark
// block must say the same. The colours index.html and the web app manifest give a browser are
// held to the same tokens.

import { readFileSync } from "node:fs";

import { describe, expect, it } from "vitest";

// Vitest runs from the repository root, as the check script does.
const css = readFileSync("apps/course/src/styles/tokens.css", "utf8");

function tokens(block: string): Record<string, string> {
  const out: Record<string, string> = {};
  for (const m of block.matchAll(/--([a-z-]+):\s*(#[0-9a-f]{6})\s*;/gi)) out[m[1]!] = m[2]!;
  return out;
}

/** The body of the first rule whose selector is exactly this, braces matched. */
function rule(selector: string): string {
  const at = css.indexOf(`${selector} {`);
  if (at < 0) throw new Error(`no rule ${selector}`);
  let depth = 0;
  for (let i = css.indexOf("{", at); i < css.length; i++) {
    if (css[i] === "{") depth++;
    if (css[i] === "}" && --depth === 0) return css.slice(at, i);
  }
  throw new Error(`unclosed rule ${selector}`);
}

const luminance = (hex: string) => {
  const [r, g, b] = [1, 3, 5].map((i) => {
    const c = parseInt(hex.slice(i, i + 2), 16) / 255;
    return c <= 0.03928 ? c / 12.92 : ((c + 0.055) / 1.055) ** 2.4;
  });
  return 0.2126 * r! + 0.7152 * g! + 0.0722 * b!;
};
const contrast = (a: string, b: string) => {
  const [hi, lo] = [luminance(a), luminance(b)].sort((x, y) => y - x);
  return (hi! + 0.05) / (lo! + 0.05);
};

const light = tokens(rule(":root"));
const dark = tokens(rule(':root[data-theme="dark"]'));
const systemDark = tokens(rule(':root:not([data-theme="light"])'));

/** Ink, and the surfaces the stylesheets set it on. */
const TEXT: readonly [string, readonly string[]][] = [
  ["fg", ["bg", "bg-raised", "bg-sunken", "bg-inset", "note-bg", "accent-soft"]],
  ["fg-muted", ["bg", "bg-raised", "bg-sunken", "note-bg", "accent-soft"]],
  ["accent", ["bg", "bg-raised", "accent-soft"]],
  ["accent-fg", ["accent"]],
  ["ok", ["ok-bg", "bg-raised"]],
  ["warn", ["warn-bg"]],
  ["bad", ["bad-bg", "bg-raised"]],
];
/** A control's edge, and the surfaces controls sit on. */
const EDGES: readonly [string, readonly string[]][] = [["border-control", ["bg", "bg-raised"]]];

// The colours a browser takes from outside the stylesheets: index.html's theme-color tags, for the
// browser's own bar, and the web app manifest's, for an installed course's title bar and the
// screen it shows while the course loads. Each is the page's: the bar is the header's colour, the
// loading screen the page's ground.
const manifest = JSON.parse(readFileSync("apps/course/public/manifest.webmanifest", "utf8")) as {
  theme_color: string;
  background_color: string;
  color_scheme_dark: { theme_color: string; background_color: string };
};
const html = readFileSync("apps/course/index.html", "utf8");
const bars = [...html.matchAll(/<meta\s[^>]*name="theme-color"[^>]*>/g)].map((m) => ({
  colour: /content="([^"]*)"/.exec(m[0])?.[1],
  media: /media="([^"]*)"/.exec(m[0])?.[1],
}));

describe("the colour tokens", () => {
  it("defines the same tokens for the dark theme whether chosen or from the system", () => {
    expect(systemDark).toEqual(dark);
    expect(Object.keys(dark).sort()).toEqual(
      Object.keys(light)
        .filter((k) => k in dark)
        .sort(),
    );
  });

  for (const [theme, t] of [
    ["light", light],
    ["dark", { ...light, ...dark }],
  ] as const) {
    it(`gives text at least 4.5:1 on its surfaces, in the ${theme} theme`, () => {
      const short: string[] = [];
      for (const [ink, surfaces] of TEXT)
        for (const s of surfaces) {
          const r = contrast(t[ink]!, t[s]!);
          if (r < 4.5) short.push(`${ink} on ${s}: ${r.toFixed(2)}`);
        }
      expect(short).toEqual([]);
    });

    it(`gives a control's edge at least 3:1 on its surfaces, in the ${theme} theme`, () => {
      const short: string[] = [];
      for (const [edge, surfaces] of EDGES)
        for (const s of surfaces) {
          const r = contrast(t[edge]!, t[s]!);
          if (r < 3) short.push(`${edge} on ${s}: ${r.toFixed(2)}`);
        }
      expect(short).toEqual([]);
    });
  }
});

describe("the colours a browser takes from outside the stylesheets", () => {
  it("gives the browser's bar the header's colour in each theme", () => {
    expect(bars).toEqual([
      { colour: light["bg-raised"], media: "(prefers-color-scheme: light)" },
      { colour: dark["bg-raised"], media: "(prefers-color-scheme: dark)" },
    ]);
  });

  it("gives an installed course the header's colour and the page's ground in each theme", () => {
    expect([manifest.theme_color, manifest.background_color]).toEqual([
      light["bg-raised"],
      light.bg,
    ]);
    expect(manifest.color_scheme_dark).toEqual({
      theme_color: dark["bg-raised"],
      background_color: dark.bg,
    });
  });
});
