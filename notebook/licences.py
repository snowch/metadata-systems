# Copyright © 2026 Christopher Snow

"""Every Python package the exported page bundles carries an open licence.

The export resolves its packages when it runs, so this reads each bundled wheel's own metadata
(its SPDX licence expression, else its licence field, else its licence classifiers) and fails on a
package under a licence nobody checked, as scripts/licences.mjs does for the course's npm
packages. The notebook's own package, `shop`, is the author's. Pyodide (MPL-2.0, with CPython
under the PSF licence) and marimo's front end (Apache-2.0) are not wheels: docs/sources.md
records them.

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
}


def licences(wheel: Path) -> tuple[str, list[str]]:
    with zipfile.ZipFile(wheel) as z:
        name = next(n for n in z.namelist() if n.endswith(".dist-info/METADATA"))
        meta = email.parser.Parser().parsestr(z.read(name).decode("utf-8", "replace"))
    if meta.get("License-Expression"):
        return meta["Name"], [c.strip("() ") for c in meta["License-Expression"].split(" OR ")]
    if meta.get("License"):
        return meta["Name"], [meta["License"].strip().splitlines()[0]]
    classifiers = meta.get_all("Classifier") or []
    return meta["Name"], [c.split("::")[-1].strip() for c in classifiers if c.startswith("License ::")]


site = Path(sys.argv[1])
problems, checked = [], 0
for wheel in sorted(site.glob("packages/*/*.whl")):
    name, found = licences(wheel)
    if name == "shop":
        continue
    checked += 1
    if not any(choice in OPEN for choice in found):
        problems.append(f"{wheel.name}: {', '.join(found) or 'no licence stated'}")
if problems:
    sys.exit("These bundled packages are not under a licence on the open list:\n  " + "\n  ".join(problems))
print(f"{checked} bundled Python packages, all under open licences.")
