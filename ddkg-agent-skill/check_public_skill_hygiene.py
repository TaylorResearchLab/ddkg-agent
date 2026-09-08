#!/usr/bin/env python3
"""Check a DDKG skill source tree or archive for accidental local/private details.

The built-in checks target classes of material that should never be needed in a
public skill. Maintainers can also provide a deployment-specific denylist at
release time without storing those private terms in the repository.
"""

from __future__ import annotations

import argparse
import os
import re
from pathlib import Path
from zipfile import ZipFile

TEXT_SUFFIXES = {".md", ".txt", ".tsv", ".csv", ".json", ".py", ".yaml", ".yml"}

# These patterns are intentionally generic. They are not a substitute for a
# deployment-specific denylist, but they catch several classes of accidental
# leakage without publishing private host or institution names in this file.
GENERIC_PATTERNS = {
    "Notion URL": re.compile(
        r"https?://(?:www\.)?(?:notion\.so|notion\.site|app\.notion\.com)/", re.I
    ),
    "local Unix path": re.compile(r"(?<![A-Za-z0-9])/(?:mnt|home|Users)/[^\s`'\"]+"),
    "private deployment wording": re.compile(
        r"\b(?:our|local|internal|private)\s+"
        r"(?:instance|deployment|server|host)\b",
        re.I,
    ),
    # Catch constructions such as an institution acronym immediately naming a
    # graph instance, while allowing the public platform names commonly used in
    # this repository. This would have caught the deployment-attribution defect
    # that motivated R7 without hard-coding the institution itself.
    "named deployment attribution": re.compile(
        r"\b(?!(?:DDKG|UBKG|UMLS|NEO4J|API|REST)\b)"
        r"[A-Z][A-Z0-9]{2,12}\s+(?:instance|deployment)\b"
    ),
}


def iter_source(path: Path):
    if path.is_dir():
        for item in sorted(path.rglob("*")):
            if item.is_file() and item.suffix.lower() in TEXT_SUFFIXES:
                yield (
                    item.relative_to(path).as_posix(),
                    item.read_text(encoding="utf-8", errors="replace"),
                )
        return

    if path.suffix in {".skill", ".zip"}:
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
    return list(dict.fromkeys(terms))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("path", type=Path)
    ap.add_argument("--forbid", action="append", help="private literal to reject; repeatable")
    ap.add_argument(
        "--forbid-file",
        help="external newline-separated denylist; do not commit this file",
    )
    ap.add_argument(
        "--require-denylist",
        action="store_true",
        help="fail if no deployment-specific denylist was supplied",
    )
    args = ap.parse_args()

    deny = private_terms(args)
    if args.require_denylist and not deny:
        print(
            "Public-skill hygiene check failed: a deployment-specific denylist "
            "was required but none was supplied."
        )
        return 2

    findings: list[str] = []

    for name, text in iter_source(args.path):
        for label, pattern in GENERIC_PATTERNS.items():
            for match in pattern.finditer(text):
                line = text.count("\n", 0, match.start()) + 1
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

    suffix = " with deployment-specific denylist" if deny else ""
    print(f"Public-skill hygiene check passed{suffix}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
