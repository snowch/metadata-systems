// Copyright © 2026 Christopher Snow
//
// Tests for scripts/prose.mjs, the prose regression check. Run by `node --test` through
// `npm run check:prose`, so CI runs them with the check itself.
//
// The check is a narrow backstop: known-bad phrases fail; clear prose passes; suspicious but
// legitimate wording (a short sentence, a "nothing", a metaphor the standard allows) must not.

import test from "node:test";
import assert from "node:assert/strict";
import { execFileSync } from "node:child_process";
import { mkdtempSync, mkdirSync, writeFileSync, rmSync } from "node:fs";
import { dirname, join } from "node:path";
import { tmpdir } from "node:os";

const PROSE = new URL("./prose.mjs", import.meta.url).pathname;

/** Every file the check scans; a temp repository must have them all. */
const ALL_FILES = [
  "content/lessons/invisible-system.prose.ts",
  "content/lessons/invisible-system.labels.ts",
  "content/lessons/invisible-system.ts",
  "packages/views/src/strings.ts",
  "apps/course/src/strings.ts",
];

/** Runs the check in a temp copy of the repository layout, with the given file contents. */
function runCheck(files) {
  const dir = mkdtempSync(join(tmpdir(), "prose-"));
  try {
    for (const name of ALL_FILES) {
      mkdirSync(dirname(join(dir, name)), { recursive: true });
      writeFileSync(join(dir, name), files[name] ?? "export const STUB = 1;\n");
    }
    const out = execFileSync(process.execPath, [PROSE, dir], { encoding: "utf8" });
    return { code: 0, out };
  } catch (e) {
    return { code: e.status ?? 1, out: (e.stdout ?? "") + (e.stderr ?? "") };
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
}

test("a known prohibited phrase is rejected, with file and phrase in the output", () => {
  const { code, out } = runCheck({
    "content/lessons/invisible-system.prose.ts":
      'export const PROSE = {\n  prediction:\n    "A wrong belief, once tested, tells you something; an untested one tells you nothing.",\n',
  });
  assert.notEqual(code, 0, "the check must fail on a prohibited phrase");
  assert.match(out, /invisible-system\.prose\.ts:\d+/);
  assert.match(out, /A wrong belief, once tested/);
  assert.match(out, /rule 1/);
});

test("normal, clear technical prose passes", () => {
  const { code, out } = runCheck({
    "content/lessons/invisible-system.prose.ts":
      'export const PROSE = {\n  plain:\n    "The warehouse records an owner for every table. You read the owner field for daily_sales in the inspector.",\n',
  });
  assert.equal(code, 0, out);
});

test("suspicious but legitimate wording is not a hard failure", () => {
  // "Nothing" used precisely; a short sentence; a metaphor the standard allows when accurate.
  const { code } = runCheck({
    "content/lessons/invisible-system.prose.ts":
      'export const PROSE = {\n  fine:\n    "Nothing in the warehouse identifies who is responsible. The check passed.",\n',
    "packages/views/src/strings.ts":
      'export const V = { ok: "The data suggests it. This is evidence, not proof." };\n',
  });
  assert.equal(code, 0, "legitimate wording must not fail the check");
});

test("the personifying nothing-says construction is rejected", () => {
  const { code, out } = runCheck({
    "packages/views/src/strings.ts":
      'export const V = { q: "Nothing so far says who created it." };\n',
  });
  assert.notEqual(code, 0);
  assert.match(out, /Nothing so far says/);
  assert.match(out, /rule 4/);
});

test("curriculum narration and summary scaffolding are rejected", () => {
  const { code, out } = runCheck({
    "content/lessons/invisible-system.prose.ts":
      'export const P = { a: "This chapter works through five ideas. The one-sentence version: state is not history." };\n',
  });
  assert.notEqual(code, 0);
  assert.match(out, /This chapter works through/);
  assert.match(out, /rule 12/);
  assert.match(out, /The one-sentence version/);
});

test("technical prose that reads plainly does not fail", () => {
  const { code } = runCheck({
    "content/lessons/invisible-system.prose.ts":
      'export const P = { a: "The design principle behind the schedule is recorded in the runbook." };\n',
  });
  // Only the exact scaffold phrases fail; ordinary prose passes.
  assert.equal(code, 0);
});

test("the whole-file scan reports the file and enough context to find the line", () => {
  const { code, out } = runCheck({
    "apps/course/src/strings.ts":
      'export const STRINGS = {\n  landing: "One thing to take away from all of this.",\n};\n',
  });
  assert.notEqual(code, 0);
  assert.match(out, /apps\/course\/src\/strings\.ts:2/);
  assert.match(out, /One thing to take away/);
  assert.match(out, /rule 2/);
});

test("the page names no lab: 'the lab' and 'Metadata Lab' are rejected, 'the label' is not", () => {
  const bad = runCheck({
    "content/lessons/invisible-system.prose.ts":
      'export const P = { a: "The figures on this page are computed by the Metadata Lab.", b: "Compare what the lab shows." };\n',
  });
  assert.notEqual(bad.code, 0);
  assert.match(bad.out, /Metadata Lab/);
  assert.match(bad.out, /the lab /);
  assert.match(bad.out, /no lab on the page/);
  const fine = runCheck({
    "content/lessons/invisible-system.prose.ts":
      'export const P = { a: "Read the label on the card, then the labour of the night\'s programs." };\n',
  });
  assert.equal(fine.code, 0, fine.out);
});

test("an apostrophe in a comment does not hide the strings after it", () => {
  // The scanner once opened a string at a comment's apostrophe ("a platform's state") and read
  // the real strings as its contents, so a prohibited phrase after such a comment passed.
  const { code, out } = runCheck({
    "content/lessons/invisible-system.prose.ts":
      "// An essay on what a platform's state records.\n/* and what it can't say */\nexport const P = {\n  a: \"In the lab's platform, a system records what its own work needs.\",\n};\n",
  });
  assert.notEqual(code, 0, "the phrase after the comment must be found");
  assert.match(out, /invisible-system\.prose\.ts:4/);
  assert.match(out, /the lab's/);
});
