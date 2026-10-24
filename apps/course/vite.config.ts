// Copyright © 2026 Christopher Snow

// The course app. One bundle, built under the base path GitHub Pages serves it from
// (/metadata-systems/ on snowch.github.io, an origin the author's other courses share). BASE_PATH
// lets the deploy workflow pass the path Pages reports, and lets a local build serve at the root.
import { execFileSync } from "node:child_process";
import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

let commit = "";
try {
  commit = execFileSync("git", ["rev-parse", "HEAD"], { encoding: "utf8" }).trim();
} catch {
  /* Source archive. */
}
export default defineConfig({
  base: process.env.BASE_PATH ?? "/metadata-systems/",
  plugins: [
    react(),
    {
      name: "loaded-release",
      transformIndexHtml(html) {
        return html.replace("<head>", `<head><meta name="ms-commit" content="${commit}">`);
      },
    },
  ],
  build: {
    outDir: "dist",
    sourcemap: true,
    target: "es2022",
  },
  server: { port: 5173, strictPort: true },
  preview: { port: 4173, strictPort: true },
});
