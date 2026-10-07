// Copyright © 2026 Christopher Snow

// The colour tokens, held to WCAG 2.2 in each theme: text at 4.5:1 or more on every surface the
// stylesheets set it on, and a control's edge at 3:1 or more on the surfaces controls sit on
// (non-text contrast). Read from tokens.css itself, so a changed value is checked the day it
// lands; the explicit dark block is the one the dark theme's toggle uses, and the system-dark
// block must say the same.

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
  ["fg-muted", ["bg", "bg-raised", "bg-sunken", "note-bg"]],
  ["accent", ["bg", "bg-raised", "accent-soft"]],
  ["accent-fg", ["accent"]],
  ["ok", ["ok-bg", "bg-raised"]],
  ["warn", ["warn-bg"]],
  ["bad", ["bad-bg", "bg-raised"]],
];
/** A control's edge, and the surfaces controls sit on. */
const EDGES: readonly [string, readonly string[]][] = [["border-control", ["bg", "bg-raised"]]];

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
