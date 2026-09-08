#!/usr/bin/env python3
"""Check a DDKG skill source tree or archive for accidental local/private details.

The built-in checks target classes of material that should never be needed in a
public skill. Maintainers can provide a deployment-specific denylist at release
time without storing those private terms in the repository.
"""

from __future__ import annotations

import argparse
import os
import re
from pathlib import Path
from zipfile import ZipFile

TEXT_SUFFIXES = {".md", ".txt", ".tsv", ".csv", ".json", ".py", ".yaml", ".yml"}
GENERIC_PATTERNS = {
    "Notion URL": re.compile(r"https?://(?:www\.)?(?:notion\.so|notion\.site|app\.notion\.com)/", re.I),
    "local Unix path": re.compile(r"(?<![A-Za-z0-9])/(?:mnt|home|Users)/[^\s`'\"]+"),
    "loopback host": re.compile(r"\b(?:localhost|127\.0\.0\.1)\b", re.I),
}


def iter_source(path: Path):
    if path.is_dir():
        for item in sorted(path.rglob("*")):
            if item.is_file() and item.suffix.lower() in TEXT_SUFFIXES:
                yield item.relative_to(path).as_posix(), item.read_text(encoding="utf-8", errors="replace")
        return

    if path.suffix == ".skill" or path.suffix == ".zip":
        with ZipFile(path) as zf:
            for name in sorted(zf.namelist()):
                if name.endswith("/") or Path(name).suffix.lower() not in TEXT_SUFFIXES:
                    continue
                yield name, zf.read(name).decode("utf-8", errors="replace")
        return

    raise SystemExit(f"Expected a source directory or .skill/.zip archive: {path}")


def private_terms(args) -> list[str]:
    terms = list(args.forbid or [])
    env = os.environ.get("DDKG_PRIVATE_DENYLIST", "")
    terms.extend(line.strip() for line in env.splitlines() if line.strip())
    if args.forbid_file:
        terms.extend(
            line.strip()
            for line in Path(args.forbid_file).read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        )
    # preserve order, remove duplicates
    return list(dict.fromkeys(terms))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("path", type=Path)
    ap.add_argument("--forbid", action="append", help="private literal to reject; repeatable")
    ap.add_argument("--forbid-file", help="external newline-separated denylist; do not commit this file")
    args = ap.parse_args()

    deny = private_terms(args)
    findings: list[str] = []

    for name, text in iter_source(args.path):
        for label, pattern in GENERIC_PATTERNS.items():
            for m in pattern.finditer(text):
                line = text.count("\n", 0, m.start()) + 1
                findings.append(f"{name}:{line}: {label}")
        lower = text.lower()
        for literal in deny:
            pos = lower.find(literal.lower())
            if pos >= 0:
                line = text.count("\n", 0, pos) + 1
                findings.append(f"{name}:{line}: deployment-specific denylist match")

    if findings:
        print(f"Public-skill hygiene check failed with {len(findings)} finding(s):")
        for finding in findings:
            print(f"  {finding}")
        return 1

    print("Public-skill hygiene check passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
