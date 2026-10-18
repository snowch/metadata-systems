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

echo "== licences =="
# Every package the built site can include carries an open licence.
node scripts/licences.mjs

echo "== types =="
# Strict TypeScript over the course's plan, the front page and the tests.
npx tsc --noEmit -p tsconfig.json

echo "== unit and integration tests =="
# The plan against docs/plan.md, each notebook's heading against the plan, and the front page's
# words, icon and tokens.
npx vitest run
node --test notebook/buttons/answers.test.mjs notebook/buttons/startup.test.mjs

echo "== the chapters' engine and words =="
# The chapters are notebooks (notebook/): the shop's platform in Python, every number and sentence
# the notebooks state, pinned against it, and the dashboard the front page shows. Standard library only, so any Python 3.12 or
# later runs it. The JupyterLite site itself needs JupyterLite's packages and the network, and is
# built in its own workflow (.github/workflows/notebook.yml) and in the deploy.
python3 -m unittest discover -s notebook/tests -t notebook

echo "== learner-facing prose =="
# The known-bad phrases the writing standard (AGENTS.md) rejects: a narrow regression check for
# confirmed wording, not a style judge. Its own tests run with it.
npm run check:prose

echo "== the course builds =="
# The production bundle, under the base path GitHub Pages serves it from.
npm run build -w @ms/course

echo "== the front page, in a browser =="
# Its links lead to the chapters' notebooks, a former chapter address leads to its notebook, and
# it has no console error, no horizontal scroll, no text under 11 pixels and, on a phone, no control
# under 40 pixels tall, at desktop and phone widths. Needs Playwright's Chromium; CI installs it.
npx playwright test

echo
echo "All checks passed."
