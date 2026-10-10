#!/usr/bin/env bash
# Copyright © 2026 Christopher Snow

# Exactly what CI runs. Run it before pushing: `npm run check`.
#
# CI invokes this same script, so a laptop and CI cannot drift. Each stage says what it protects,
# because a check nobody understands is a check somebody eventually deletes.
set -euo pipefail
cd "$(dirname "$0")/.."

echo "== formatting =="
# One formatter, pinned, so a diff is never a reformat. Prose files keep their own line breaks.
npx prettier --check .

echo "== copyright =="
# Every source file carries its author's copyright line; `node scripts/copyright.mjs` adds it.
node scripts/copyright.mjs --check

echo "== the platform copy is unedited =="
# platform/ is the learning platform's packages at the commit platform/SOURCE.json records. A fix
# to the platform is made in snowch/learning-platform and synced here, never made here.
node scripts/sync-platform.mjs --check

echo "== licences =="
# Every package the built site can include carries an open licence.
node scripts/licences.mjs

echo "== types =="
# Strict TypeScript over the lab, the views, the content, the app, the platform and the tests.
npx tsc --noEmit -p tsconfig.json

echo "== unit and integration tests =="
# The lab and the schema under Node with no DOM; the runtime, the figures and every chapter under
# jsdom. Every chapter is parsed, its references pass, its starting points fail, its numbers are
# pinned to the lab, and it renders whole.
npx vitest run

echo "== the notebook prototype's engine and words =="
# Chapter 1 as a notebook (notebook/): the shop's platform in Python, and every number and
# sentence the notebook states, pinned against it. Standard library only, so any Python 3.12 or
# later runs it. The WebAssembly export itself needs marimo and a browser, and runs in its own
# workflow (.github/workflows/notebook.yml) and in the deploy.
python3 -m unittest discover -s notebook/tests -t notebook

echo "== learner-facing prose =="
# The known-bad phrases the writing standard (AGENTS.md) rejects: a narrow regression check for
# confirmed wording, not a style judge. Its own tests run with it.
npm run check:prose

echo "== the course builds =="
# The production bundle, under the base path GitHub Pages serves it from.
npm run build -w @ms/course

echo "== educational tests, in a browser =="
# Every challenge completable and refusing a wrong attempt, predictions committed before they are
# answered, work graded again on load, no console error, no horizontal scroll, at desktop and
# phone widths. Needs Playwright's Chromium; CI installs it.
npx playwright test

echo
echo "All checks passed."
