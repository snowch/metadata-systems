// Copyright © 2026 Christopher Snow

// The educational tests: the built course, driven in a browser.
//
// They hold every chapter to the educational level: every challenge completable with its
// reference and refusing a wrong attempt, a prediction committed before it is answered, saved
// work graded again on load and not bypassable through storage, resettable, no console error,
// no horizontal scroll. They run against the production build served under the course's base
// path, as GitHub Pages serves it, on a desktop viewport and on a phone.
import { defineConfig } from "@playwright/test";

const port = 4173;
const base = "/metadata-systems/";

export default defineConfig({
  testDir: "tests/educational",
  fullyParallel: false,
  workers: 1,
  retries: 0,
  timeout: 60_000,
  reporter: [["list"]],
  use: {
    baseURL: `http://localhost:${port}${base}`,
    trace: "retain-on-failure",
  },
  webServer: {
    command: `npm run preview -w @ms/course -- --port ${port} --strictPort`,
    url: `http://localhost:${port}${base}`,
    reuseExistingServer: !process.env.CI,
    timeout: 120_000,
  },
  projects: [
    {
      name: "desktop",
      use: { browserName: "chromium", viewport: { width: 1280, height: 800 } },
    },
    {
      name: "phone",
      use: {
        browserName: "chromium",
        viewport: { width: 375, height: 812 },
        isMobile: true,
        hasTouch: true,
      },
    },
  ],
});
