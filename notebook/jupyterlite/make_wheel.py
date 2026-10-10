# Copyright © 2026 Christopher Snow

"""Packs notebook/shop into a wheel the JupyterLite page installs, the same bytes on every build.

The shop's platform is pure Python with the standard library only, so the wheel is a zip of its
modules with the three metadata files a wheel needs. Every entry gets one fixed time, so the same
source always gives the same file.

Usage: python3 make_wheel.py OUT_DIR
"""

import base64
import hashlib
import sys
import zipfile
from pathlib import Path

SHOP = Path(__file__).resolve().parent.parent / "shop"
NAME, VERSION = "shop", "0.0.0"
DIST = f"{NAME}-{VERSION}.dist-info"
WHEN = (2026, 1, 1, 0, 0, 0)


def record_line(path: str, data: bytes) -> str:
    digest = base64.urlsafe_b64encode(hashlib.sha256(data).digest()).rstrip(b"=").decode()
    return f"{path},sha256={digest},{len(data)}"


def build(out_dir: Path) -> Path:
    files = {f"shop/{p.name}": p.read_bytes() for p in sorted(SHOP.glob("*.py"))}
    files[f"{DIST}/METADATA"] = (
        f"Metadata-Version: 2.1\nName: {NAME}\nVersion: {VERSION}\n"
        "Summary: The shop's data platform for Metadata Systems, Chapter 1\n"
    ).encode()
    files[f"{DIST}/WHEEL"] = b"Wheel-Version: 1.0\nGenerator: make_wheel.py\nRoot-Is-Purelib: true\nTag: py3-none-any\n"
    record = [record_line(path, data) for path, data in files.items()] + [f"{DIST}/RECORD,,"]
    files[f"{DIST}/RECORD"] = ("\n".join(record) + "\n").encode()
    out_dir.mkdir(parents=True, exist_ok=True)
    wheel = out_dir / f"{NAME}-{VERSION}-py3-none-any.whl"
    with zipfile.ZipFile(wheel, "w", zipfile.ZIP_DEFLATED) as z:
        for path, data in files.items():
            info = zipfile.ZipInfo(path, WHEN)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o644 << 16
            z.writestr(info, data)
    return wheel


if __name__ == "__main__":
    print(build(Path(sys.argv[1])))
