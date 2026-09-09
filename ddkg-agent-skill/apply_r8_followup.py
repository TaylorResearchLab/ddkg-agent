#!/usr/bin/env python3
"""Resolve a label-guidance inconsistency found during R8 review."""

from pathlib import Path

path = Path(__file__).resolve().parent / "source" / "ddkg" / "references" / "11_interpreting_results.md"
text = path.read_text(encoding="utf-8")
old = """Return enough names to be useful, prefer the shortest as a display label, and\ndo not assume the first is canonical.\n"""
new = """Use one verified source-specific preferred-term edge as the display label when\nthat edge is known. Synonyms may be returned as additional audit information,\nbut do not choose the first or shortest synonym as the entity name. If no\npreferred-term edge is verified, display the source `CodeID`.\n"""
if new in text:
    print("label-guidance follow-up already applied")
elif old in text:
    path.write_text(text.replace(old, new, 1), encoding="utf-8")
    print("updated source/ddkg/references/11_interpreting_results.md")
else:
    raise SystemExit("Expected label-guidance text not found")
