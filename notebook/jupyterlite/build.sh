#!/usr/bin/env bash
# Copyright © 2026 Christopher Snow

# Builds all written chapters as a JupyterLite site, into the directory given: one notebook per
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

# The packages the site serves: the shop's platform, which the notebook installs, and comm, which
# the Pyodide kernel installs when it starts and which Pyodide does not ship.
python3 "$here/make_wheel.py" "$work/wheels"
python3 -m pip download --quiet --no-deps --dest "$work/wheels" "comm==0.2.3"

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

# Stream real download progress for the runtime in standalone and complete-course builds.
python3 - "$here" "$out" <<'PYTHON'
import json, sys
from pathlib import Path
source, out = map(Path, sys.argv[1:])
size = (out / "static/pyodide/pyodide.asm.wasm").stat().st_size
(out / "python-progress.js").write_text((source / "python-progress.js").read_text().replace("MS_PYTHON_RUNTIME_BYTES", str(size)))
(out / "python-worker.js").write_bytes((source / "python-worker.js").read_bytes())
# Redirect the retired comparison URL before Jupyter tries to open a missing notebook.
p = out / "notebooks/index.html"
redirect = """<script>(function () {
  var url = new URL(window.location.href);
  if (url.searchParams.get("path") === "chapter_01b.ipynb") {
    url.searchParams.set("path", "chapter_01.ipynb");
    window.location.replace(url.href);
  }
})();</script>"""
p.write_text(p.read_text().replace("<head>", "<head>" + redirect, 1))
(out / "files/chapter_01b.ipynb").unlink(missing_ok=True)
p = out / "jupyter-lite.json"
config = json.loads(p.read_text())
config["jupyter-config-data"]["msOfflineWorker"] = "python-worker.js"
p.write_text(json.dumps(config))
PYTHON

# Every Python package the page can load carries an open licence.
python3 "$here/../licences.py" "$out"
