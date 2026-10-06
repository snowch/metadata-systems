// Copyright © 2026 Christopher Snow

// Every package the built site can include carries an open licence.
//
// `npm query .prod` lists the production dependency tree of every workspace; this fails on any
// package whose licence is not on the list below, so a dependency under a licence nobody checked
// cannot reach the site unnoticed. Development tools (the test runners, the type checker, the
// formatter) are not shipped and are not listed. The course's own workspaces are skipped: they
// are the author's.

import { execFileSync } from "node:child_process";

const OPEN = new Set([
  "MIT",
  "ISC",
  "Apache-2.0",
  "BSD-2-Clause",
  "BSD-3-Clause",
  "0BSD",
  "OFL-1.1",
  "CC0-1.0",
  "BlueOak-1.0.0",
  "Unlicense",
]);

const nodes = JSON.parse(execFileSync("npm", ["query", ".prod"], { encoding: "utf8" }));
const problems = [];
let checked = 0;
for (const n of nodes) {
  // The course's own workspaces (the root, apps/, packages/, platform/, content) live outside
  // node_modules; only installed dependencies are checked.
  if (!String(n.location ?? "").includes("node_modules")) continue;
  checked++;
  const licence = typeof n.license === "string" ? n.license : n.license?.type;
  // An SPDX expression such as "(MIT OR Apache-2.0)" passes if any choice is open.
  const choices = String(licence ?? "")
    .replace(/[()]/g, "")
    .split(/\s+OR\s+/);
  if (!choices.some((c) => OPEN.has(c.trim())))
    problems.push(`${n.name}@${n.version}: ${licence ?? "no licence stated"}`);
}
if (problems.length) {
  console.error("These production dependencies are not under a licence on the open list:");
  for (const p of problems) console.error(`  ${p}`);
  process.exit(1);
}
console.log(`${checked} production dependencies, all under open licences.`);
