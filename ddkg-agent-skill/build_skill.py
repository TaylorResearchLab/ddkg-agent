#!/usr/bin/env python3
"""Build ddkg.skill deterministically from the unpacked public source tree."""

from __future__ import annotations

import hashlib
import subprocess
import sys
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

HERE = Path(__file__).resolve().parent
SOURCE_ROOT = HERE / "source" / "ddkg"
OUTPUT = HERE / "ddkg.skill"
FIXED_TIME = (1980, 1, 1, 0, 0, 0)


def zip_info(name: str, is_dir: bool = False) -> ZipInfo:
    info = ZipInfo(name + ("/" if is_dir and not name.endswith("/") else ""), FIXED_TIME)
    info.compress_type = ZIP_DEFLATED
    mode = 0o755 if is_dir else 0o644
    info.external_attr = (mode & 0xFFFF) << 16
    return info


def main() -> int:
    if not SOURCE_ROOT.is_dir():
        raise SystemExit(f"Missing source tree: {SOURCE_ROOT}")

    route = SOURCE_ROOT / "scripts" / "route.py"
    subprocess.run([sys.executable, str(route), "--check"], cwd=SOURCE_ROOT, check=True)

    dirs = sorted(p for p in SOURCE_ROOT.rglob("*") if p.is_dir())
    files = sorted(p for p in SOURCE_ROOT.rglob("*") if p.is_file())

    with ZipFile(OUTPUT, "w", compression=ZIP_DEFLATED, compresslevel=9) as zf:
        zf.writestr(zip_info("ddkg", is_dir=True), b"")
        for path in dirs:
            rel = path.relative_to(SOURCE_ROOT).as_posix()
            zf.writestr(zip_info(f"ddkg/{rel}", is_dir=True), b"")
        for path in files:
            rel = path.relative_to(SOURCE_ROOT).as_posix()
            zf.writestr(zip_info(f"ddkg/{rel}"), path.read_bytes())

    digest = hashlib.sha256(OUTPUT.read_bytes()).hexdigest()
    print(f"built {OUTPUT.name}: {OUTPUT.stat().st_size} bytes")
    print(f"bundled files: {len(files)}")
    print(f"sha256: {digest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
