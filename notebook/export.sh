#!/usr/bin/env bash
# Copyright © 2026 Christopher Snow

# Exports Chapter 1's notebook as a site that runs Python in the browser, into the directory given:
# Python, every package and the notebook's own `shop` package are bundled into the site, so the page
# fetches nothing from a third party. Both workflows run this; it needs marimo, Playwright's
# Chromium (which resolves the packages) and uv (which builds `shop` into a wheel).
#
#   notebook/export.sh OUT_DIR

set -euo pipefail
out="$(realpath -m "$1")"
cd "$(dirname "$0")"

# --mode edit: the reader can change and run every cell. --execute: the outputs are computed here
# and saved into the page. --no-sandbox: the notebook needs nothing beyond marimo and the standard
# library, so it runs in this Python.
marimo export html-wasm chapter_01.py -o "$out" --mode edit --offline --execute --no-sandbox -f

# marimo copies its notes for its own contributors into the site.
rm -f "$out/CLAUDE.md"

python3 run_on_load.py "$out/index.html"

# Every package the page bundles carries an open licence.
python3 licences.py "$out"
