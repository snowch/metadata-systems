#!/usr/bin/env bash
# Copyright © 2026 Christopher Snow

# Exports Chapter 1's notebooks as a site that runs Python in the browser, into the directory given:
# Python, every package and the notebooks' own `shop` package are bundled into the site, so a page
# fetches nothing from a third party. The chapter is in two parts, one notebook each: part 1 is the
# site's index.html and part 2 is part-2.html, beside it, so the two pages share one copy of Python
# and the packages. Both workflows run this; it needs marimo, Playwright's Chromium (which resolves
# the packages) and uv (which builds `shop` into a wheel).
#
#   notebook/export.sh OUT_DIR

set -euo pipefail
out="$(realpath -m "$1")"
cd "$(dirname "$0")"

# --mode edit: the reader can change and run every cell. --execute: the outputs are computed here
# and saved into the page. --no-sandbox: the notebook needs nothing beyond marimo and the standard
# library, so it runs in this Python.
marimo export html-wasm chapter_01_part_1.py -o "$out/index.html" --mode edit --offline --execute --no-sandbox -f
marimo export html-wasm chapter_01_part_2.py -o "$out/part-2.html" --mode edit --offline --execute --no-sandbox -f

# marimo copies its notes for its own contributors into the site.
rm -f "$out/CLAUDE.md"

python3 run_on_load.py "$out/index.html" "$out/part-2.html"

# Every package the page bundles carries an open licence.
python3 licences.py "$out"
