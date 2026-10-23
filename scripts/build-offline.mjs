// Copyright © 2026 Christopher Snow

// Run after assembling the front page, notebooks and redirects. The manifest describes every
// runtime file by exact bytes and digest; a release becomes available offline only as a whole.
import { createHash } from "node:crypto";
import { readdir, readFile, writeFile, copyFile, stat } from "node:fs/promises";
import { join, resolve } from "node:path";

const root = resolve(process.argv[2] || "apps/course/dist");
const configPath = join(root, "jupyterlite/jupyter-lite.json");
const config = JSON.parse(await readFile(configPath, "utf8"));
config["jupyter-config-data"].msOfflineWorker = "../offline-worker.js";
await writeFile(configPath, JSON.stringify(config));
await copyFile(new URL("../offline/worker.js", import.meta.url), join(root, "offline-worker.js"));

async function walk(folder = "") {
  const files = [];
  for (const entry of await readdir(join(root, folder), { withFileTypes: true })) {
    const name = join(folder, entry.name);
    if (entry.isDirectory()) files.push(...(await walk(name)));
    else if (
      !name.endsWith(".map") &&
      !["offline-manifest.json", "offline-worker.js", "jupyterlite/release.json"].includes(name)
    ) {
      const bytes = await readFile(join(root, name));
      files.push({
        path: name,
        size: (await stat(join(root, name))).size,
        sha256: createHash("sha256").update(bytes).digest("hex"),
      });
    }
  }
  return files;
}
const chapterCount = (await readdir(new URL("../notebook/", import.meta.url))).filter((name) =>
  /^chapter_\d+\.py$/.test(name),
).length;
const files = (await walk()).sort((a, b) => a.path.localeCompare(b.path));
if (
  !files.some((file) => file.path.endsWith("pyodide.asm.wasm")) ||
  files.filter((file) => /^jupyterlite\/files\/chapter_\d+\.ipynb$/.test(file.path)).length !==
    chapterCount
) {
  throw Error("Offline build requires Python and every chapter");
}
const version = createHash("sha256").update(JSON.stringify(files)).digest("hex").slice(0, 20);
const manifest = { version, bytes: files.reduce((sum, file) => sum + file.size, 0), files };
await writeFile(join(root, "offline-manifest.json"), JSON.stringify(manifest));
console.log(
  `Offline course: ${files.length} files, ${(manifest.bytes / 1e6).toFixed(1)} MB, ${version}`,
);
