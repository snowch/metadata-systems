# Copyright © 2026 Christopher Snow

"""Makes exported notebooks run their cells when the page loads.

marimo's html-wasm export embeds marimo's default configuration, in which a notebook does not run
its cells on load: the page shows the outputs saved at export time, every cell is marked as needing
a run, and the change menu and the handover note do nothing until the reader presses "run all".
The chapter needs Python behind every cell from the start, so this sets `auto_instantiate` in the
page's embedded configuration. It fails if the setting is not there exactly once, so that a new
marimo version that moves it stops the build instead of shipping a page that does not run.

Usage: python3 run_on_load.py SITE/index.html [SITE/part-2.html ...]
"""

import sys

OFF = '"auto_instantiate": false'
ON = '"auto_instantiate": true'

for path in sys.argv[1:]:
    with open(path, encoding="utf-8") as f:
        page = f.read()
    if page.count(OFF) != 1:
        sys.exit(f"{path}: expected {OFF} once in the embedded configuration, found {page.count(OFF)}")
    with open(path, "w", encoding="utf-8") as f:
        f.write(page.replace(OFF, ON))
    print(f"{path}: the cells run when the page loads")
