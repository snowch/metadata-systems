// Copyright © 2026 Christopher Snow

// Unit tests, under Vitest, with no DOM: the plan against docs/plan.md, the notebooks' headings
// against the plan, the front page's words, its icon and its tokens. The front page itself is
// driven in a browser by Playwright (tests/educational); the chapters are notebooks, tested in
// Python (notebook/tests) and in a browser (notebook/jupyterlite/smoke.mjs).
import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    include: ["content/**/*.test.ts", "apps/**/*.test.ts"],
    environment: "node",
    passWithNoTests: false,
  },
});
