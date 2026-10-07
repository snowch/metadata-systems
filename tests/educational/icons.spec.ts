// Copyright © 2026 Christopher Snow

// The course's icon as the built site serves it, under the course's own path. Every icon the page
// names loads; the manifest's icons load at the sizes it claims; the two cut by a platform's own
// mask (the maskable icon, and iOS's) have no clear pixel; and the maskable one keeps everything
// but its ground inside the safe zone, which the manifest specification keeps visible under any
// mask: a circle about the centre with a radius of two fifths of the icon's size. And the
// browser's own bar keeps the header's colour in whichever theme the learner picks.

import { expect, test, type Page } from "@playwright/test";

/** An icon counted in the page: its size, its clear pixels, and its marks outside the safe zone. */
async function pixels(page: Page, url: string) {
  return page.evaluate(async (src) => {
    const img = new Image();
    img.src = src;
    await img.decode();
    const canvas = document.createElement("canvas");
    canvas.width = img.naturalWidth;
    canvas.height = img.naturalHeight;
    const context = canvas.getContext("2d");
    if (!context) throw new Error("no 2d context");
    context.drawImage(img, 0, 0);
    const { data, width, height } = context.getImageData(0, 0, canvas.width, canvas.height);
    // The ground is the colour in the corner; a mark is any pixel more than a shade off it.
    const ground = [data[0] ?? 0, data[1] ?? 0, data[2] ?? 0];
    const radius = 0.4 * width;
    let clear = 0;
    let outside = 0;
    for (let y = 0; y < height; y++)
      for (let x = 0; x < width; x++) {
        const i = (y * width + x) * 4;
        if (data[i + 3] !== 255) clear++;
        const mark = ground.some((g, c) => Math.abs((data[i + c] ?? 0) - g) > 2);
        if (mark && Math.hypot(x + 0.5 - width / 2, y + 0.5 - height / 2) > radius) outside++;
      }
    return { width, height, clear, outside };
  }, url);
}

const links = 'link[rel~="icon"], link[rel="apple-touch-icon"], link[rel="manifest"]';

test("every icon the page names loads from the course's own path", async ({ page, baseURL }) => {
  await page.goto("./");
  const hrefs = await page
    .locator(links)
    .evaluateAll((all) => all.map((l) => (l as HTMLLinkElement).href));
  expect(hrefs).toHaveLength(4);
  for (const href of hrefs) {
    expect(href.startsWith(baseURL ?? "")).toBe(true);
    expect((await page.request.get(href)).status(), href).toBe(200);
  }
});

test("the manifest's icons fit their sizes, and the masked ones their masks", async ({
  page,
  baseURL,
}) => {
  await page.goto("./");
  const href = (rel: string) =>
    page.locator(`link[rel="${rel}"]`).evaluate((l) => (l as HTMLLinkElement).href);
  const at = await href("manifest");
  const manifest = (await (await page.request.get(at)).json()) as {
    start_url: string;
    scope: string;
    icons: { src: string; sizes: string; purpose?: string }[];
  };
  // The course opens at its own contents page, and its links stay in the installed course.
  expect(new URL(manifest.start_url, at).href).toBe(baseURL);
  expect(new URL(manifest.scope, at).href).toBe(baseURL);

  // Each icon, and what cuts it: nothing, a platform's mask, or iOS's own.
  const icons = [
    ...manifest.icons.map((i) => ({
      url: new URL(i.src, at).href,
      side: Number(i.sizes.split("x")[0]),
      cut: (i.purpose ?? "any").split(" ").includes("maskable") ? "mask" : "none",
    })),
    { url: await href("apple-touch-icon"), side: 180, cut: "ios" },
  ];
  expect(icons.map((i) => i.cut).sort()).toEqual(["ios", "mask", "none", "none"]);
  for (const icon of icons) {
    const p = await pixels(page, icon.url);
    expect([p.width, p.height], icon.url).toEqual([icon.side, icon.side]);
    if (icon.cut !== "none") expect(p.clear, icon.url).toBe(0);
    if (icon.cut === "mask") expect(p.outside, icon.url).toBe(0);
  }
});

test("the browser's bar takes the header's colour in the theme the learner picks", async ({
  page,
}) => {
  await page.goto("./");
  const bars = () =>
    page
      .locator('meta[name="theme-color"]')
      .evaluateAll((all) => all.map((m) => (m as HTMLMetaElement).content));
  const header = () =>
    page.locator(".shell-header").evaluate((e) => {
      const [r, g, b] = (getComputedStyle(e).backgroundColor.match(/\d+/g) ?? []).map(Number);
      return `#${[r, g, b].map((v) => (v ?? 0).toString(16).padStart(2, "0")).join("")}`;
    });
  const picker = page.locator(".theme-picker select");
  const own = await bars();
  expect(own).toHaveLength(2);
  for (const theme of ["dark", "light"]) {
    await picker.selectOption(theme);
    const colour = await header();
    expect(await bars(), theme).toEqual([colour, colour]);
  }
  await picker.selectOption("auto");
  expect(await bars()).toEqual(own);
});
