// Copyright © 2026 Christopher Snow

// Unit and integration tests, under Vitest.
//
// The lab and the lesson schema run under Node with no DOM: the lab is a model of a data platform
// and must not touch a browser, and running it here is what enforces that. Tests of React
// components opt into a DOM with a `// @vitest-environment jsdom` comment at the top of the file.
// The educational tests drive the built site in a browser and live under tests/educational, run
// by Playwright, not here. The platform's own tests run here too, against this course's
// dependencies, so the copy in platform/ is proved to work in this repository.
import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    include: [
      "packages/**/*.test.ts",
      "packages/**/*.test.tsx",
      "platform/**/*.test.ts",
      "platform/**/*.test.tsx",
      "content/**/*.test.ts",
      "content/**/*.test.tsx",
      "apps/**/*.test.ts",
      "apps/**/*.test.tsx",
    ],
    environment: "node",
    setupFiles: ["./tests/vitest.setup.ts"],
    passWithNoTests: false,
  },
});
