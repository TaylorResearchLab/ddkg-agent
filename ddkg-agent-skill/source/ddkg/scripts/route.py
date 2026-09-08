#!/usr/bin/env python3
"""
Route a topic to the sections that answer it, plus the ones you will be wrong
without.

A keyword index tells you where something is documented. This walks the
`must_read_with` edges as well, which is the part that prevents silent
failures: knowing where GTEx expression is documented does not stop you
writing a threshold on a property that does not exist.

    python route.py "gene symbol"
    python route.py expression --depth 2
    python route.py --list
    python route.py --stale "JKG generation"
    python route.py --check          # validate graph rows and file targets

The graph is `assets/skill_graph.tsv`, a flat file. Edit it by hand; it is
meant to be greppable and loadable into a graph tool without this script.
"""

from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GRAPH = ROOT / "assets" / "skill_graph.tsv"

ALLOWED_EDGE_TYPES = frozenset(
    {
        "answers",
        "must_read_with",
        "demonstrated_by",
        "supersedes",
        "invalidated_by",
    }
)
FILE_SUFFIXES = frozenset(
    {".md", ".tsv", ".csv", ".json", ".py", ".txt", ".yaml", ".yml"}
)

Edge = tuple[str, str, str, str]


def load() -> tuple[list[Edge], list[str]]:
    """Load the graph and retain every structural error for `--check`."""
    edges: list[Edge] = []
    errors: list[str] = []
    seen: dict[tuple[str, str, str], int] = {}

    for lineno, raw in enumerate(GRAPH.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.rstrip()
        if not line or line.lstrip().startswith("#"):
            continue

        parts = line.split("\t")
        if len(parts) not in (3, 4):
            errors.append(
                f"line {lineno}: expected 3 or 4 tab-separated fields, found {len(parts)}"
            )
            continue

        subj, edge, obj = (part.strip() for part in parts[:3])
        note = parts[3].strip() if len(parts) == 4 else ""

        if not subj or not edge or not obj:
            errors.append(f"line {lineno}: subject, edge, and object must be non-empty")
            continue
        if edge not in ALLOWED_EDGE_TYPES:
            errors.append(f"line {lineno}: unsupported edge type {edge!r}")
            continue

        key = (subj, edge, obj)
        if key in seen:
            errors.append(
                f"line {lineno}: duplicate edge; first occurrence is line {seen[key]}: "
                f"{subj!r} {edge!r} {obj!r}"
            )
            continue
        seen[key] = lineno
        edges.append((subj, edge, obj, note))

    return edges, errors


def index(edges: list[Edge]):
    out = defaultdict(list)
    for subj, edge, obj, note in edges:
        out[subj.lower()].append((edge, obj, note))
    return out


def file_part(node: str) -> str:
    return node.split("#", 1)[0]


def is_file_node(node: str) -> bool:
    """Return whether a node syntactically names a bundled file."""
    return Path(file_part(node)).suffix.lower() in FILE_SUFFIXES


def resolve_path(node: str) -> Path | None:
    """Map a file node to a bundled file without permitting path escape."""
    name = file_part(node)
    root = ROOT.resolve()
    for base in (ROOT, ROOT / "references"):
        candidate = (base / name).resolve()
        try:
            candidate.relative_to(root)
        except ValueError:
            continue
        if candidate.is_file():
            return candidate
    return None


def markdown_anchors(path: Path) -> set[str]:
    """Return GitHub-style heading slugs for a Markdown file."""
    anchors: set[str] = set()
    counts: defaultdict[str, int] = defaultdict(int)
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("#"):
            continue
        text = line.lstrip("#").strip()
        base = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
        if not base:
            continue
        count = counts[base]
        counts[base] += 1
        anchors.add(base if count == 0 else f"{base}-{count}")
    return anchors


def validate_file_node(node: str) -> str | None:
    """Validate existence and, for Markdown, an optional heading anchor."""
    path = resolve_path(node)
    if path is None:
        return f"unresolved file target {node!r}"

    if "#" not in node:
        return None

    anchor = node.split("#", 1)[1]
    if not anchor:
        return f"empty anchor in target {node!r}"
    if path.suffix.lower() != ".md":
        return f"anchor on non-Markdown target {node!r}"

    anchors = markdown_anchors(path)
    normalized = anchor.replace("--", "-")
    if anchor not in anchors and normalized not in {a.replace("--", "-") for a in anchors}:
        return f"unresolved Markdown anchor {node!r}"
    return None


def walk(idx, start: str, depth: int):
    """Collect answers for a topic, then follow must_read_with transitively."""
    start = start.lower()
    answers, prereqs, demos, seen = [], [], [], set()

    frontier = []
    for edge, obj, note in idx.get(start, []):
        if edge == "answers":
            answers.append((obj, note))
            frontier.append(obj)
        elif edge == "must_read_with":
            prereqs.append((obj, note, start))
            frontier.append(obj)
        elif edge == "demonstrated_by":
            demos.append((obj, note))

    for _ in range(depth):
        nxt = []
        for node in frontier:
            key = node.lower()
            if key in seen:
                continue
            seen.add(key)
            for edge, obj, note in idx.get(key, []):
                if edge == "must_read_with":
                    prereqs.append((obj, note, node))
                    nxt.append(obj)
                elif edge == "demonstrated_by":
                    demos.append((obj, note))
        frontier = nxt

    return answers, prereqs, demos


def cmd_route(idx, topic: str, depth: int) -> int:
    answers, prereqs, demos = walk(idx, topic, depth)
    if not (answers or prereqs or demos):
        near = [k for k in idx if topic.lower() in k or k in topic.lower()]
        print(f"No entry for {topic!r}.")
        if near:
            print("Closest entries: " + ", ".join(sorted(near)[:10]))
        else:
            print("Run --list to see the entry points.")
        return 1

    print(f"# {topic}\n")
    if answers:
        print("Read:")
        for obj, note in answers:
            print(f"  {obj}" + (f"   — {note}" if note else ""))
    if demos:
        print("\nWorking example:")
        for obj, note in demos:
            print(f"  {obj}" + (f"   — {note}" if note else ""))
    if prereqs:
        print("\nYou will be wrong without:")
        seen = set()
        for obj, note, via in prereqs:
            if obj in seen:
                continue
            seen.add(obj)
            why = note or f"required by {via}"
            print(f"  {obj}\n      {why}")
    return 0


def cmd_stale(idx, event: str) -> int:
    """What does a given change invalidate?"""
    hits = []
    for subj, edges in idx.items():
        for edge, obj, note in edges:
            if edge == "invalidated_by" and obj.lower() == event.lower():
                hits.append((subj, note))
    if not hits:
        events = sorted(
            {
                obj
                for edges in idx.values()
                for edge, obj, _ in edges
                if edge == "invalidated_by"
            }
        )
        print(f"Nothing recorded as invalidated by {event!r}.")
        print("Recorded events: " + ", ".join(events))
        return 1
    print(f"# invalidated by: {event}\n")
    for subj, note in sorted(hits):
        print(f"  {subj}" + (f"   — {note}" if note else ""))
    return 0


def cmd_list(idx) -> int:
    topics = sorted(
        k
        for k in idx
        if not k.endswith(".md")
        and not k.endswith(".tsv")
        and not k.endswith(".csv")
        and not k.endswith(".json")
        and "#" not in k
        and "/" not in k
    )
    print("Entry points:\n")
    for topic in topics:
        print(f"  {topic}")
    return 0


def cmd_check(edges: list[Edge], parse_errors: list[str]) -> int:
    """Validate graph rows, edge vocabulary, duplicates, files, and anchors."""
    errors = list(parse_errors)
    checked_nodes: set[str] = set()

    for subj, _, obj, _ in edges:
        for node in (subj, obj):
            if node in checked_nodes or not is_file_node(node):
                continue
            checked_nodes.add(node)
            error = validate_file_node(node)
            if error:
                errors.append(error)

    if errors:
        print(f"Graph validation failed with {len(errors)} error(s):")
        for error in errors:
            print(f"  {error}")
        return 1

    print(f"Graph validation passed: {len(edges)} edges; all file targets resolve.")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("topic", nargs="?", help="what you are trying to do")
    ap.add_argument(
        "--depth", type=int, default=2, help="how far to follow must_read_with (default 2)"
    )
    ap.add_argument("--list", action="store_true", help="show entry points")
    ap.add_argument(
        "--stale", metavar="EVENT", help="what a change invalidates, e.g. 'JKG generation'"
    )
    ap.add_argument(
        "--check",
        action="store_true",
        help="validate graph rows, edge types, duplicates, and file targets",
    )
    args = ap.parse_args()

    if not GRAPH.exists():
        print(f"Missing {GRAPH}", file=sys.stderr)
        return 2

    edges, parse_errors = load()
    if args.check:
        return cmd_check(edges, parse_errors)
    if parse_errors:
        print("Graph structure is invalid; run --check for details.", file=sys.stderr)
        return 2

    idx = index(edges)

    if args.list:
        return cmd_list(idx)
    if args.stale:
        return cmd_stale(idx, args.stale)
    if args.topic:
        return cmd_route(idx, args.topic, args.depth)
    ap.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
