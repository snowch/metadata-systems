// Copyright © 2026 Christopher Snow

// The course's icon and its web app manifest, held to what a browser needs to show the course in
// a tab and to install it: every icon index.html or the manifest names is in public/, a PNG at the
// size it claims; the manifest names the course as its pages do; and it keeps to the course's own
// path, on an origin the author's other courses share. tokens.test.ts holds the colours; the
// educational tests fetch the same files from the built site and check their pixels.

import { existsSync, readFileSync } from "node:fs";

import { describe, expect, it } from "vitest";

import { STRINGS } from "./strings";

interface Icon {
  src: string;
  sizes: string;
  type: string;
  purpose?: string;
}
interface Manifest {
  name: string;
  short_name: string;
  description: string;
  start_url: string;
  scope: string;
  id?: string;
  icons: Icon[];
}

// Vitest runs from the repository root, as the check script does.
const PUBLIC = "apps/course/public";
const html = readFileSync("apps/course/index.html", "utf8");
const manifest = JSON.parse(readFileSync(`${PUBLIC}/manifest.webmanifest`, "utf8")) as Manifest;

/** Every tag of one name in index.html, as its attributes. */
function tags(name: string): Record<string, string>[] {
  return [...html.matchAll(new RegExp(`<${name}\\s([^>]*)>`, "g"))].map((m) =>
    Object.fromEntries([...(m[1] ?? "").matchAll(/([a-z-]+)="([^"]*)"/g)].map((a) => [a[1], a[2]])),
  );
}

/** A PNG's width and height, from its header. */
function pngSize(file: string): number[] {
  const b = readFileSync(file);
  if (
    b.subarray(0, 8).toString("hex") !== "89504e470d0a1a0a" ||
    b.toString("latin1", 12, 16) !== "IHDR"
  )
    throw new Error(`${file} is not a PNG`);
  return [b.readUInt32BE(16), b.readUInt32BE(20)];
}

const purposes = (icon: Icon) => (icon.purpose ?? "any").split(" ");
const size = (sizes: string) => sizes.split("x").map(Number);

describe("the course's icon and manifest", () => {
  it("names the course as its pages do", () => {
    const meta = (name: string) => tags("meta").find((t) => t.name === name)?.content;
    expect(manifest.name).toBe(STRINGS.brand);
    expect(/<title>([^<]*)<\/title>/.exec(html)?.[1]).toBe(STRINGS.brand);
    expect(manifest.description).toBe(meta("description"));
    // The label under a home-screen icon: a phone cuts a longer one short, and iOS takes it from
    // its own tag.
    expect(manifest.short_name.length).toBeLessThanOrEqual(12);
    expect(meta("apple-mobile-web-app-title")).toBe(manifest.short_name);
  });

  it("keeps to the course's own path", () => {
    // Both resolve against the manifest's own address, so they name the course's path whatever
    // base the site is built for.
    expect([manifest.start_url, manifest.scope]).toEqual(["./", "./"]);
    // An id resolves against the origin, which the author's courses share; with none, a browser
    // takes the start URL, which is this course's own.
    expect(manifest.id).toBeUndefined();
  });

  it("names only icons that are there, at the sizes it claims", () => {
    for (const icon of manifest.icons) {
      expect(icon.type).toBe("image/png");
      expect(pngSize(`${PUBLIC}/${icon.src}`)).toEqual(size(icon.sizes));
      for (const p of purposes(icon)) expect(["any", "maskable", "monochrome"]).toContain(p);
    }
    // Chromium offers to install a site only if its manifest has icons of 192 and 512 pixels,
    // among other things; a maskable one lets a phone cut its own shape.
    const plain = manifest.icons.filter((i) => purposes(i).includes("any")).map((i) => i.sizes);
    expect(plain).toEqual(expect.arrayContaining(["192x192", "512x512"]));
    expect(manifest.icons.some((i) => purposes(i).includes("maskable"))).toBe(true);
  });

  it("links only icons that are there, at the sizes it claims", () => {
    const rels = ["icon", "apple-touch-icon", "manifest"];
    const links = tags("link").filter((t) => rels.includes(t.rel ?? ""));
    expect(links.map((t) => t.rel).sort()).toEqual([
      "apple-touch-icon",
      "icon",
      "icon",
      "manifest",
    ]);
    for (const link of links) {
      const file = `${PUBLIC}${link.href ?? ""}`;
      expect(existsSync(file), file).toBe(true);
      if (link.sizes) expect(pngSize(file)).toEqual(size(link.sizes));
    }
    // 180 pixels, the largest home-screen size Apple's guide lists; a device that wants a smaller
    // one takes the smallest larger one there is, this.
    const touch = links.find((t) => t.rel === "apple-touch-icon");
    expect(pngSize(`${PUBLIC}${touch?.href ?? ""}`)).toEqual([180, 180]);
  });
});
