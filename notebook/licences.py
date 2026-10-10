# Copyright © 2026 Christopher Snow

"""Every Python package an exported page bundles carries an open licence.

The exports resolve their packages when they run, so this reads every wheel in the site, wherever
it sits (marimo's `packages/`, JupyterLite's `pypi/` and `static/pyodide/`), from its own metadata
(its SPDX licence expression, else its licence field, else its licence classifiers) and fails on a
package under a licence nobody checked, as scripts/licences.mjs does for the course's npm
packages. The notebook's own package, `shop`, is the author's. Pyodide (MPL-2.0, with CPython
under the PSF licence) and the front ends (marimo's, Apache-2.0; JupyterLite's, BSD-3-Clause) are
not wheels: docs/sources.md records them.

Usage: python3 licences.py SITE_DIR
"""

import email.parser
import sys
import zipfile
from pathlib import Path

OPEN = {
    "MIT",
    "MIT License",
    "BSD-2-Clause",
    "BSD-3-Clause",
    "BSD License",
    "Apache-2.0",
    "Apache Software License",
    "MPL-2.0",
    "Mozilla Public License 2.0 (MPL 2.0)",
    "Mozilla Public License Version 2.0",
    "Public Domain",
    # The first line of the licence's own text, or a short spelling, which some packages put in
    # the field.
    "BSD 2-Clause License",
    "BSD 3-Clause License",
    "Apache 2.0",
}


def licences(wheel: Path) -> tuple[str, list[str]]:
    """The licences a wheel states: its SPDX expression; else its licence field and classifiers;
    else the first line of a licence file it carries, as JupyterLite's own stand-in wheels do."""
    with zipfile.ZipFile(wheel) as z:
        names = z.namelist()
        meta = email.parser.Parser().parsestr(
            z.read(next(n for n in names if n.endswith(".dist-info/METADATA"))).decode("utf-8", "replace")
        )
        files = [n for n in names if ".dist-info/" in n and n.rsplit("/", 1)[-1].upper().startswith(("LICENSE", "LICENCE", "COPYING"))]
        texts = [z.read(n).decode("utf-8", "replace").strip().splitlines()[0].strip() for n in files]
    if meta.get("License-Expression"):
        return meta["Name"], [c.strip("() ") for c in meta["License-Expression"].split(" OR ")]
    found = [meta["License"].strip().splitlines()[0]] if meta.get("License") else []
    found += [c.split("::")[-1].strip() for c in meta.get_all("Classifier") or [] if c.startswith("License ::")]
    return meta["Name"], found or texts


site = Path(sys.argv[1])
problems, checked = [], 0
for wheel in sorted(site.rglob("*.whl")):
    name, found = licences(wheel)
    if name == "shop":
        continue
    checked += 1
    if not any(choice in OPEN for choice in found):
        problems.append(f"{wheel.name}: {', '.join(found) or 'no licence stated'}")
if problems:
    sys.exit("These bundled packages are not under a licence on the open list:\n  " + "\n  ".join(problems))
print(f"{checked} bundled Python wheels, all under open licences.")
