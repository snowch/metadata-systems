#!/usr/bin/env bash
# Copyright © 2026 Christopher Snow

# Builds Chapters 1 and 2 as a JupyterLite site, into the directory given: a Jupyter notebook per
# chapter, made from the two source files in notebook/, with the `shop` package, in
# JupyterLite's Notebook interface, with Pyodide and every package the pages use inside the site,
# so they fetch nothing from a third party. Both workflows run this; it needs the packages in
# requirements.txt, Node and npm, and network access to PyPI, to npm and to Pyodide's CDN at build
# time.
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

# The notebooks, from the source files; each runs once here, in CPython, as a check.
python3 "$here/build_ipynb.py" "$work/content" --check

# The row of large buttons above each notebook's cells (notebook/buttons/), a JupyterLab extension
# built with JupyterLab's builder, into notebook/buttons/labextension/.
buttons="$(cd "$here/../buttons" && pwd)"
(cd "$buttons" && npm ci --no-audit --no-fund && npm run build)

cd "$work"
jupyter lite build --lite-dir "$here" --contents "$work/content" --output-dir "$out" \
  --apps notebooks --apps tree --no-sourcemaps --no-unused-shared-packages \
  --LiteBuildConfig.federated_extensions="$buttons/labextension" \
  $(for w in "$work"/wheels/*.whl; do printf -- '--piplite-wheels %s ' "$w"; done)

# Every Python package the page can load carries an open licence.
python3 "$here/../licences.py" "$out"
