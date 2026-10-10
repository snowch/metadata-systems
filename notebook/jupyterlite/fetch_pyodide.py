# Copyright © 2026 Christopher Snow

"""Puts the part of Pyodide the JupyterLite page uses into the site, so it fetches nothing elsewhere.

The Pyodide kernel loads Pyodide from a CDN unless the site has its own copy in `static/pyodide/`.
The whole distribution is hundreds of megabytes; the page needs Pyodide's runtime and the packages
the kernel loads when it starts (micropip, IPython and jedi, with what they depend on), found by
watching the page load from the CDN. This downloads those, each wheel checked against the sha256
in Pyodide's own lockfile, which it also copies. A package not here and not bundled by the page
cannot be imported, which this page never asks for.

Usage: python3 fetch_pyodide.py OUT_DIR
"""

import hashlib
import json
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

# The Pyodide the kernel was built for (jupyterlite-pyodide-kernel 0.8.6's PYODIDE_VERSION).
VERSION = "314.0.6"
CDN = f"https://cdn.jsdelivr.net/pyodide/v{VERSION}/full/"
CORE = ["pyodide.mjs", "pyodide.asm.mjs", "pyodide.asm.wasm", "python_stdlib.zip", "pyodide-lock.json"]
# What the kernel loads when it starts; their dependencies come from the lockfile.
STARTUP = ["micropip", "ipython", "jedi"]


def get(url: str) -> bytes:
    with urllib.request.urlopen(url, timeout=60) as response:
        return response.read()


def key(name: str) -> str:
    """A package's key in the lockfile, which writes `prompt-toolkit` where a dependency list may
    write `prompt_toolkit`."""
    return name.lower().replace("_", "-").replace(".", "-")


def closure(lock: dict, names: list[str]) -> list[str]:
    packages, todo, seen = lock["packages"], [key(n) for n in names], []
    while todo:
        name = todo.pop()
        if name in seen:
            continue
        seen.append(name)
        todo.extend(key(d) for d in packages[name]["depends"])
    return sorted(seen)


def main(out: Path) -> None:
    out.mkdir(parents=True, exist_ok=True)
    lock_bytes = get(CDN + "pyodide-lock.json")
    lock = json.loads(lock_bytes)
    names = closure(lock, STARTUP)
    wheels = {lock["packages"][n]["file_name"]: lock["packages"][n]["sha256"] for n in names}

    def fetch(name: str) -> str:
        target = out / name
        data = lock_bytes if name == "pyodide-lock.json" else get(CDN + name)
        if name in wheels and hashlib.sha256(data).hexdigest() != wheels[name]:
            raise SystemExit(f"{name}: sha256 differs from Pyodide's lockfile")
        target.write_bytes(data)
        return f"{name} {len(data)}"

    with ThreadPoolExecutor(max_workers=8) as pool:
        for line in pool.map(fetch, CORE + sorted(wheels)):
            print(line)
    print(f"{len(CORE)} runtime files and {len(wheels)} packages: {', '.join(names)}")


if __name__ == "__main__":
    main(Path(sys.argv[1]))
