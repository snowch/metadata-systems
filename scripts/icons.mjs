// Copyright © 2026 Christopher Snow

// The course's icon, drawn here and written to apps/course/public: the SVG a browser's tab shows,
// and the PNGs the web app manifest, an older browser and iOS's home screen take. Chromium, the
// one Playwright runs the educational tests in, renders the PNGs from the same drawing. Run it
// after changing the drawing, and commit what it writes: `node scripts/icons.mjs`, or with a
// directory to write somewhere else first and look.
//
// The drawing is the course's own: a label tag, the plainest sign of a thing described, in white
// on the page's accent. Two layouts of it:
//
// - rounded: the tag on a rounded square with clear corners, for a tab and wherever a platform
//   shows the icon as drawn;
// - full: the tag a little smaller on a square filled to its edges, for the manifest's maskable
//   icon and for iOS, which each cut their own shape from it. What the manifest specification
//   keeps visible under any mask is a circle about the centre with a radius of two fifths of the
//   icon's size; the tag stays inside it, and the educational tests check that from the pixels.

import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";

import { chromium } from "@playwright/test";

const out = process.argv[2] ?? "apps/course/public";

// The light theme's accent and the ink set on it, from the tokens, so the icon keeps the page's.
const tokens = readFileSync("apps/course/src/styles/tokens.css", "utf8");
const accent = /--accent:\s*(#[0-9a-f]{6})/i.exec(tokens)?.[1];
const ink = /--accent-fg:\s*(#[0-9a-f]{6})/i.exec(tokens)?.[1];
if (!accent || !ink) throw new Error("tokens.css sets no --accent or --accent-fg");

/**
 * The tag in a 512 square: drawn pointing left, then turned to point up and left. It is drawn 42
 * units left of the centre so that, turned, its box is centred: its tip is one point and its back
 * two corners. A stroke in the fill's colour rounds every corner alike; the hole shows the ground.
 */
const tag = (scale) =>
  `<g transform="translate(256 256) rotate(45) scale(${scale})">` +
  `<path d="M-182 0 L-97 -85 H98 V85 H-97 Z" fill="${ink}" stroke="${ink}" stroke-width="40" stroke-linejoin="round"/>` +
  `<circle cx="-85" cy="0" r="32" fill="${accent}"/>` +
  `</g>`;

const svg = (body) => `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">${body}</svg>`;
const rounded = svg(`<rect width="512" height="512" rx="112" fill="${accent}"/>${tag(1.1)}`);
const full = svg(`<rect width="512" height="512" fill="${accent}"/>${tag(0.9)}`);

/** Each PNG: its file, its layout and its size in pixels. */
const PNGS = [
  ["favicon-32.png", rounded, 32],
  ["icon-192.png", rounded, 192],
  ["icon-512.png", rounded, 512],
  ["icon-maskable-512.png", full, 512],
  ["apple-touch-icon.png", full, 180],
];

mkdirSync(out, { recursive: true });
writeFileSync(join(out, "icon.svg"), `<!-- Copyright © 2026 Christopher Snow -->\n${rounded}\n`);

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 640, height: 640 }, deviceScaleFactor: 1 });
for (const [file, art, size] of PNGS) {
  await page.setContent(
    `<!doctype html><style>html,body{margin:0;background:transparent}` +
      `svg{display:block;width:${size}px;height:${size}px}</style>${art}`,
  );
  await page.screenshot({
    path: join(out, file),
    clip: { x: 0, y: 0, width: size, height: size },
    omitBackground: true,
  });
}
await browser.close();
console.log(`Wrote icon.svg and ${PNGS.length} PNGs to ${out}`);
