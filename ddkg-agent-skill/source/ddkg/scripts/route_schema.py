#!/usr/bin/env python3
"""Find short DDKG schema routes between source abbreviations (SABs).

This is an R9 prototype. It searches the small source/predicate graph, not the
full DDKG node graph. The sparse source graph is loaded from bundled release
assets and can also be exported as a binary SAB-to-SAB adjacency matrix.

Examples:

    python route_schema.py GO HGNC
    python route_schema.py HGNC MP --top-k 5 --max-hops 6
    python route_schema.py --neighbors HGNC
    python route_schema.py --stats
    python route_schema.py --matrix-out /tmp/ddkg_sab_matrix.tsv
    python route_schema.py GO HGNC --transition-file /tmp/schema_transitions.csv

A returned path is a structural candidate, not by itself a biologically valid
query. Production use must add entity-role, species, and other guardrails so
that Concept-level identifier co-residence cannot create a false comparison.
"""

from __future__ import annotations

import argparse
import csv
import json
from collections import defaultdict, deque
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
DCC_TRIPLES = ASSETS / "sab_triples_dcc.csv"
DICTIONARY_TRIPLES = ASSETS / "data_dictionary_triples.json"
COMPILED_TRANSITIONS = ASSETS / "schema_transitions.csv"


@dataclass(frozen=True)
class Transition:
    subject_sab: str
    predicate: str
    edge_sab: str
    object_sab: str
    origin: str
    count: int | None = None

    @property
    def structural_key(self) -> tuple[str, str, str, str]:
        return (
            self.subject_sab,
            self.predicate,
            self.edge_sab,
            self.object_sab,
        )


def parse_count(value: object) -> int | None:
    if value in (None, ""):
        return None
    try:
        return int(str(value).strip())
    except (TypeError, ValueError):
        return None


def load_compiled(path: Path) -> list[Transition]:
    """Load a transition CSV produced by build_schema_transitions.py."""
    rows: list[Transition] = []
    with path.open(newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        required = {"subject_sab", "predicate", "edge_sab", "object_sab"}
        if not required.issubset(reader.fieldnames or []):
            raise ValueError(
                f"{path}: expected columns {sorted(required)}; found {reader.fieldnames}"
            )
        for lineno, row in enumerate(reader, 2):
            subject = (row.get("subject_sab") or "").strip()
            predicate = (row.get("predicate") or "").strip()
            edge_sab = (row.get("edge_sab") or "").strip()
            obj = (row.get("object_sab") or "").strip()
            if not all((subject, predicate, edge_sab, obj)):
                raise ValueError(f"{path}:{lineno}: empty required field")
            origin = (row.get("provenance") or path.name).strip()
            count = parse_count(row.get("observed_count") or row.get("edge_count"))
            rows.append(
                Transition(
                    subject_sab=subject,
                    predicate=predicate,
                    edge_sab=edge_sab,
                    object_sab=obj,
                    origin=origin,
                    count=count,
                )
            )
    return rows


def load_dcc() -> list[Transition]:
    """Load live DCC subject/predicate/edge-SAB/object triples."""
    rows: list[Transition] = []
    with DCC_TRIPLES.open(newline="", encoding="utf-8") as handle:
        reader = csv.reader(handle)
        for lineno, row in enumerate(reader, 1):
            if not row:
                continue
            if len(row) != 4:
                raise ValueError(
                    f"{DCC_TRIPLES.name}:{lineno}: expected 4 columns, found {len(row)}"
                )
            subject, predicate, edge_sab, obj = (value.strip() for value in row)
            if not all((subject, predicate, edge_sab, obj)):
                raise ValueError(f"{DCC_TRIPLES.name}:{lineno}: empty field")
            rows.append(
                Transition(
                    subject_sab=subject,
                    predicate=predicate,
                    edge_sab=edge_sab,
                    object_sab=obj,
                    origin="sab_triples_dcc.csv",
                )
            )
    return rows


def load_dictionary() -> list[Transition]:
    """Load selected source-to-source triples from the release data dictionary.

    This asset does not carry edge SAB as a separate field. Those transitions
    remain useful for reachability but are marked with an empty edge_sab so the
    caller can distinguish them from fully source-qualified transitions.
    """
    raw = json.loads(DICTIONARY_TRIPLES.read_text(encoding="utf-8"))
    rows: list[Transition] = []
    for index, item in enumerate(raw, 1):
        subject = str(item.get("subject_sab", "")).strip()
        predicate = str(item.get("predicate", "")).strip()
        obj = str(item.get("object_sab", "")).strip()
        if not all((subject, predicate, obj)):
            raise ValueError(
                f"{DICTIONARY_TRIPLES.name}: record {index} lacks subject/predicate/object"
            )
        count = parse_count(item.get("count"))
        section = str(item.get("section", "data dictionary")).strip()
        rows.append(
            Transition(
                subject_sab=subject,
                predicate=predicate,
                edge_sab="",
                object_sab=obj,
                origin=section or "data_dictionary_triples.json",
                count=count,
            )
        )
    return rows


def deduplicate(rows: Iterable[Transition]) -> list[Transition]:
    """Keep one copy of each structural transition, preferring richer records."""
    chosen: dict[tuple[str, str, str, str], Transition] = {}
    for row in rows:
        key = row.structural_key
        current = chosen.get(key)
        if current is None:
            chosen[key] = row
            continue
        current_score = (
            1 if current.edge_sab else 0,
            current.count if current.count is not None else -1,
        )
        row_score = (
            1 if row.edge_sab else 0,
            row.count if row.count is not None else -1,
        )
        if row_score > current_score:
            chosen[key] = row
    return sorted(
        chosen.values(),
        key=lambda t: (
            t.subject_sab,
            t.object_sab,
            t.predicate,
            t.edge_sab,
            t.origin,
        ),
    )


def load_transitions(source: str, transition_file: Path | None) -> list[Transition]:
    if transition_file is not None:
        return deduplicate(load_compiled(transition_file))

    if source == "auto":
        if COMPILED_TRANSITIONS.is_file():
            return deduplicate(load_compiled(COMPILED_TRANSITIONS))
        source = "both"

    if source == "compiled":
        if not COMPILED_TRANSITIONS.is_file():
            raise FileNotFoundError(
                f"{COMPILED_TRANSITIONS} does not exist; run build_schema_transitions.py"
            )
        return deduplicate(load_compiled(COMPILED_TRANSITIONS))

    rows: list[Transition] = []
    if source in {"dcc", "both"}:
        rows.extend(load_dcc())
    if source in {"dictionary", "both"}:
        rows.extend(load_dictionary())
    return deduplicate(rows)


def build_adjacency(
    transitions: Iterable[Transition], *, require_edge_sab: bool = False
) -> dict[str, list[Transition]]:
    adjacency: dict[str, list[Transition]] = defaultdict(list)
    for transition in transitions:
        if require_edge_sab and not transition.edge_sab:
            continue
        adjacency[transition.subject_sab].append(transition)
    for sab in adjacency:
        adjacency[sab].sort(
            key=lambda t: (t.object_sab, t.predicate, t.edge_sab, t.origin)
        )
    return dict(adjacency)


def shortest_paths(
    adjacency: dict[str, list[Transition]],
    start: str,
    target: str,
    *,
    top_k: int,
    max_hops: int,
) -> list[list[Transition]]:
    """Return up to top_k shortest simple SAB paths using breadth-first search."""
    if start == target:
        return [[]]

    queue: deque[tuple[str, list[Transition], frozenset[str]]] = deque()
    queue.append((start, [], frozenset({start})))
    answers: list[list[Transition]] = []
    best_hops: int | None = None

    while queue:
        current, path, visited = queue.popleft()
        if len(path) >= max_hops:
            continue
        if best_hops is not None and len(path) + 1 > best_hops:
            continue

        for transition in adjacency.get(current, []):
            nxt = transition.object_sab
            if nxt in visited:
                continue
            new_path = [*path, transition]
            if nxt == target:
                if best_hops is None:
                    best_hops = len(new_path)
                if len(new_path) == best_hops:
                    answers.append(new_path)
                    if len(answers) >= top_k:
                        return answers
                continue
            queue.append((nxt, new_path, visited | {nxt}))

    return answers


def all_sabs(transitions: Iterable[Transition]) -> list[str]:
    return sorted(
        {t.subject_sab for t in transitions} | {t.object_sab for t in transitions}
    )


def canonical_sab(query: str, sabs: Iterable[str]) -> str:
    """Resolve a SAB case-insensitively while preserving its stored spelling."""
    lookup = {sab.upper(): sab for sab in sabs}
    normalized = query.strip().upper()
    return lookup.get(normalized, normalized)


def export_binary_matrix(transitions: list[Transition], output: Path) -> None:
    """Export A[i,j] = 1 when at least one transition SAB_i -> SAB_j exists."""
    sabs = all_sabs(transitions)
    present = {(t.subject_sab, t.object_sab) for t in transitions}
    with output.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(["SAB", *sabs])
        for subject in sabs:
            writer.writerow(
                [subject, *("1" if (subject, obj) in present else "0" for obj in sabs)]
            )


def print_path(start: str, path: list[Transition], index: int) -> None:
    print(f"Route {index}: {len(path)} transition(s)")
    print(f"  {start}")
    for transition in path:
        source = f" [{transition.edge_sab}]" if transition.edge_sab else ""
        count = f"; count={transition.count}" if transition.count is not None else ""
        print(
            f"    --{transition.predicate}{source}--> {transition.object_sab}"
            f"   ({transition.origin}{count})"
        )


def print_neighbors(adjacency: dict[str, list[Transition]], sab: str) -> int:
    rows = adjacency.get(sab, [])
    if not rows:
        print(f"No outgoing transitions recorded for {sab}.")
        return 1
    print(f"# outgoing transitions from {sab}\n")
    for transition in rows:
        source = transition.edge_sab or "edge SAB unavailable"
        print(
            f"{sab}\t{transition.predicate}\t{source}\t{transition.object_sab}"
            f"\t{transition.origin}"
        )
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("start", nargs="?", help="starting node SAB")
    parser.add_argument("target", nargs="?", help="target node SAB")
    parser.add_argument(
        "--source",
        choices=("auto", "compiled", "dcc", "dictionary", "both"),
        default="auto",
        help="transition source (default: compiled asset when present, else both seeds)",
    )
    parser.add_argument(
        "--transition-file",
        type=Path,
        help="explicit schema transition CSV; overrides --source",
    )
    parser.add_argument("--top-k", type=int, default=3, help="shortest paths to return")
    parser.add_argument("--max-hops", type=int, default=6, help="maximum transitions")
    parser.add_argument(
        "--require-edge-sab",
        action="store_true",
        help="use only transitions whose edge SAB is explicitly recorded",
    )
    parser.add_argument("--neighbors", metavar="SAB", help="list outgoing transitions")
    parser.add_argument(
        "--matrix-out", type=Path, help="write binary SAB-to-SAB matrix as TSV"
    )
    parser.add_argument("--stats", action="store_true", help="print transition graph size")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.top_k < 1 or args.max_hops < 1:
        raise SystemExit("--top-k and --max-hops must be >= 1")

    transitions = load_transitions(args.source, args.transition_file)
    adjacency = build_adjacency(
        transitions, require_edge_sab=args.require_edge_sab
    )
    active = [t for rows in adjacency.values() for t in rows]
    sabs = all_sabs(active)

    if args.stats:
        print(f"SABs: {len(sabs)}")
        print(f"Transitions: {len(active)}")
        print(
            "Source-qualified transitions: "
            f"{sum(1 for transition in active if transition.edge_sab)}"
        )

    if args.matrix_out:
        export_binary_matrix(active, args.matrix_out)
        print(f"Wrote {args.matrix_out}")

    if args.neighbors:
        return print_neighbors(adjacency, canonical_sab(args.neighbors, sabs))

    if args.start or args.target:
        if not (args.start and args.target):
            raise SystemExit("provide both start and target SABs")
        start = canonical_sab(args.start, sabs)
        target = canonical_sab(args.target, sabs)
        paths = shortest_paths(
            adjacency,
            start,
            target,
            top_k=args.top_k,
            max_hops=args.max_hops,
        )
        if not paths:
            print(
                f"No route found from {start} to {target} "
                f"within {args.max_hops} transition(s)."
            )
            return 1
        print(f"# {start} -> {target}\n")
        for index, path in enumerate(paths, 1):
            print_path(start, path, index)
            if index != len(paths):
                print()
        return 0

    if not (args.stats or args.matrix_out):
        raise SystemExit("provide start/target SABs or use --neighbors/--stats/--matrix-out")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
