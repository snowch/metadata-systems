#!/usr/bin/env bash
# Copyright © 2026 Christopher Snow

# Builds Chapter 1 as a JupyterLite site, into the directory given, for comparison with the marimo
# notebooks: the same prose and the same `shop` package, as two Jupyter notebooks, one per part of
# the chapter, in JupyterLite's Notebook interface, with Pyodide and every package the pages use
# inside the site, so they fetch nothing from a third party. Both workflows run this; it needs the
# packages in requirements.txt and network access to PyPI and to Pyodide's CDN at build time.
#
#   notebook/jupyterlite/build.sh OUT_DIR

set -euo pipefail
out="$(realpath -m "$1")"
here="$(cd "$(dirname "$0")" && pwd)"
work="$(mktemp -d)"
trap 'rm -rf "$work"' EXIT

# Pyodide's runtime and the packages the kernel loads when it starts, into the lite folder's
# static/pyodide/, where the build finds and copies them.
rm -rf "$here/static/pyodide"
python3 "$here/fetch_pyodide.py" "$here/static/pyodide"

# The three packages the notebook installs from the site: the shop's platform, and ipywidgets with
# the one dependency the kernel does not already have.
python3 "$here/make_wheel.py" "$work/wheels"
python3 -m pip download --quiet --no-deps --dest "$work/wheels" "ipywidgets==8.1.9" "comm==0.2.3"

# The notebooks, from the marimo notebooks; each runs once here, in CPython, as a check.
python3 "$here/build_ipynb.py" "$work/content" --check

cd "$work"
jupyter lite build --lite-dir "$here" --contents "$work/content" --output-dir "$out" \
  --apps notebooks --apps tree --no-sourcemaps --no-unused-shared-packages \
  $(for w in "$work"/wheels/*.whl; do printf -- '--piplite-wheels %s ' "$w"; done)

# Every Python package the page can load carries an open licence.
python3 "$here/../licences.py" "$out"
