#!/usr/bin/env python3
"""Build a source-qualified DDKG schema-transition asset for R9 routing.

The builder combines the bundled DCC endpoint triples with selected canonical
source-to-source transitions from the release data dictionary. It infers a
missing edge SAB only when the release predicate registry makes that inference
unambiguous, or when exactly one candidate edge SAB is supported by the source
section label. Optional live Neo4j exports can then replace or supplement these
seed rows.

This script operates on release metadata, not on the full DDKG node graph.

Examples:

    python build_schema_transitions.py --output /tmp/schema_transitions.csv
    python build_schema_transitions.py --live /tmp/live_schema.csv \
        --output /tmp/schema_transitions.csv \
        --unresolved /tmp/schema_unresolved.csv

Expected live CSV columns:

    subject_sab,predicate,edge_sab,object_sab

An optional fifth column named edge_count or observed_count is accepted.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

ROOT = Path(__file__).resolve().parent.parent
ASSETS = ROOT / "assets"
DCC_TRIPLES = ASSETS / "sab_triples_dcc.csv"
DICTIONARY_TRIPLES = ASSETS / "data_dictionary_triples.json"
PREDICATES = ASSETS / "predicates.csv"
INVERSE_PAIRS = ASSETS / "inverse_pairs.json"

OUTPUT_FIELDS = [
    "subject_sab",
    "predicate",
    "edge_sab",
    "object_sab",
    "observed_count",
    "provenance",
    "edge_sab_status",
    "direction_status",
]

UNRESOLVED_FIELDS = [
    "subject_sab",
    "predicate",
    "object_sab",
    "observed_count",
    "section",
    "candidate_edge_sabs",
    "reason",
]


def normalize_predicate(value: str) -> str:
    """Normalize harmless spelling variants without changing stored output."""
    value = value.strip().replace("\\_", "_").replace(" ", "_")
    return value.casefold()


def compact_token(value: str) -> str:
    return re.sub(r"[^A-Z0-9]+", "", value.upper())


def parse_count(value: object) -> int | None:
    if value in (None, ""):
        return None
    try:
        return int(str(value).strip())
    except (TypeError, ValueError):
        return None


@dataclass
class TransitionRecord:
    subject_sab: str
    predicate: str
    edge_sab: str
    object_sab: str
    observed_count: int | None = None
    provenance: set[str] = field(default_factory=set)
    edge_sab_status: set[str] = field(default_factory=set)
    direction_status: set[str] = field(default_factory=lambda: {"stored"})

    @property
    def key(self) -> tuple[str, str, str, str]:
        return (
            self.subject_sab,
            self.predicate,
            self.edge_sab,
            self.object_sab,
        )

    def merge(self, other: "TransitionRecord") -> None:
        if self.key != other.key:
            raise ValueError("cannot merge different structural transitions")
        self.provenance.update(other.provenance)
        self.edge_sab_status.update(other.edge_sab_status)
        self.direction_status.update(other.direction_status)
        counts = [
            value
            for value in (self.observed_count, other.observed_count)
            if value is not None
        ]
        self.observed_count = max(counts) if counts else None


@dataclass(frozen=True)
class UnresolvedRecord:
    subject_sab: str
    predicate: str
    object_sab: str
    observed_count: int | None
    section: str
    candidate_edge_sabs: tuple[str, ...]
    reason: str


def load_predicate_registry() -> tuple[dict[str, set[str]], set[tuple[str, str]]]:
    by_predicate: dict[str, set[str]] = defaultdict(set)
    registered_pairs: set[tuple[str, str]] = set()
    with PREDICATES.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        required = {"predicate", "edge_sab"}
        if not required.issubset(reader.fieldnames or []):
            raise ValueError(f"{PREDICATES.name} missing required columns")
        for row in reader:
            predicate = (row.get("predicate") or "").strip()
            edge_sab = (row.get("edge_sab") or "").strip()
            if not predicate or not edge_sab:
                continue
            key = normalize_predicate(predicate)
            by_predicate[key].add(edge_sab)
            registered_pairs.add((key, edge_sab))
    return dict(by_predicate), registered_pairs


def infer_edge_sab(
    predicate: str,
    section: str,
    predicate_sabs: dict[str, set[str]],
) -> tuple[str | None, str, tuple[str, ...]]:
    """Infer an edge SAB conservatively from release metadata."""
    candidates = sorted(predicate_sabs.get(normalize_predicate(predicate), set()))
    if not candidates:
        return None, "no-predicate-registry-match", (),
    if len(candidates) == 1:
        return candidates[0], "unique-predicate", tuple(candidates)

    section_token = compact_token(section)
    section_matches = [
        candidate
        for candidate in candidates
        if len(compact_token(candidate)) >= 3
        and compact_token(candidate) in section_token
    ]
    if len(section_matches) == 1:
        return section_matches[0], "section-supported", tuple(candidates)

    return None, "ambiguous-predicate", tuple(candidates)


def add_record(
    records: dict[tuple[str, str, str, str], TransitionRecord],
    record: TransitionRecord,
) -> None:
    current = records.get(record.key)
    if current is None:
        records[record.key] = record
    else:
        current.merge(record)


def load_dcc(records: dict[tuple[str, str, str, str], TransitionRecord]) -> None:
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
            add_record(
                records,
                TransitionRecord(
                    subject_sab=subject,
                    predicate=predicate,
                    edge_sab=edge_sab,
                    object_sab=obj,
                    provenance={"dcc-live-endpoints"},
                    edge_sab_status={"explicit"},
                ),
            )


def load_dictionary(
    records: dict[tuple[str, str, str, str], TransitionRecord],
    predicate_sabs: dict[str, set[str]],
) -> list[UnresolvedRecord]:
    raw = json.loads(DICTIONARY_TRIPLES.read_text(encoding="utf-8"))
    unresolved: list[UnresolvedRecord] = []
    for index, item in enumerate(raw, 1):
        subject = str(item.get("subject_sab", "")).strip()
        predicate = str(item.get("predicate", "")).strip()
        obj = str(item.get("object_sab", "")).strip()
        section = str(item.get("section", "")).strip()
        if not all((subject, predicate, obj)):
            raise ValueError(
                f"{DICTIONARY_TRIPLES.name}: record {index} lacks subject/predicate/object"
            )
        observed_count = parse_count(item.get("count"))
        edge_sab, status, candidates = infer_edge_sab(
            predicate, section, predicate_sabs
        )
        if edge_sab is None:
            unresolved.append(
                UnresolvedRecord(
                    subject_sab=subject,
                    predicate=predicate,
                    object_sab=obj,
                    observed_count=observed_count,
                    section=section,
                    candidate_edge_sabs=candidates,
                    reason=status,
                )
            )
            continue

        stored_predicate = normalize_predicate(predicate)
        # Use the exact spelling from the release registry when possible.
        # The normalized spelling is a safe fallback for dictionary variants
        # such as "causally influences" versus "causally_influences".
        exact_predicate = predicate.replace("\\_", "_").replace(" ", "_")
        if not stored_predicate:
            raise ValueError("empty normalized predicate")

        add_record(
            records,
            TransitionRecord(
                subject_sab=subject,
                predicate=exact_predicate,
                edge_sab=edge_sab,
                object_sab=obj,
                observed_count=observed_count,
                provenance={"data-dictionary"},
                edge_sab_status={status},
            ),
        )
    return unresolved


def load_live_csv(
    path: Path,
    records: dict[tuple[str, str, str, str], TransitionRecord],
) -> None:
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
            observed_count = parse_count(
                row.get("edge_count") or row.get("observed_count")
            )
            add_record(
                records,
                TransitionRecord(
                    subject_sab=subject,
                    predicate=predicate,
                    edge_sab=edge_sab,
                    object_sab=obj,
                    observed_count=observed_count,
                    provenance={f"live:{path.name}"},
                    edge_sab_status={"explicit-live"},
                ),
            )


def add_registered_inverses(
    records: dict[tuple[str, str, str, str], TransitionRecord],
    registered_pairs: set[tuple[str, str]],
) -> int:
    inverse_map_raw = json.loads(INVERSE_PAIRS.read_text(encoding="utf-8"))
    inverse_map = {
        normalize_predicate(key): str(value)
        for key, value in inverse_map_raw.items()
    }

    added = 0
    snapshot = list(records.values())
    for record in snapshot:
        inverse_predicate = inverse_map.get(normalize_predicate(record.predicate))
        if not inverse_predicate:
            continue
        if (normalize_predicate(inverse_predicate), record.edge_sab) not in registered_pairs:
            continue
        inverse = TransitionRecord(
            subject_sab=record.object_sab,
            predicate=inverse_predicate,
            edge_sab=record.edge_sab,
            object_sab=record.subject_sab,
            observed_count=record.observed_count,
            provenance={"derived-registered-inverse"},
            edge_sab_status={"explicit-via-forward"},
            direction_status={"derived-inverse"},
        )
        if inverse.key not in records:
            added += 1
        add_record(records, inverse)
    return added


def write_records(
    records: Iterable[TransitionRecord],
    output: Path,
) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    ordered = sorted(
        records,
        key=lambda r: (r.subject_sab, r.object_sab, r.predicate, r.edge_sab),
    )
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS, lineterminator="\n")
        writer.writeheader()
        for record in ordered:
            writer.writerow(
                {
                    "subject_sab": record.subject_sab,
                    "predicate": record.predicate,
                    "edge_sab": record.edge_sab,
                    "object_sab": record.object_sab,
                    "observed_count": ""
                    if record.observed_count is None
                    else record.observed_count,
                    "provenance": ";".join(sorted(record.provenance)),
                    "edge_sab_status": ";".join(sorted(record.edge_sab_status)),
                    "direction_status": ";".join(sorted(record.direction_status)),
                }
            )


def write_unresolved(rows: Iterable[UnresolvedRecord], output: Path) -> None:
    output.parent.mkdir(parents=True, exist_ok=True)
    ordered = sorted(
        rows,
        key=lambda r: (r.section, r.subject_sab, r.predicate, r.object_sab),
    )
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(
            handle, fieldnames=UNRESOLVED_FIELDS, lineterminator="\n"
        )
        writer.writeheader()
        for row in ordered:
            writer.writerow(
                {
                    "subject_sab": row.subject_sab,
                    "predicate": row.predicate,
                    "object_sab": row.object_sab,
                    "observed_count": ""
                    if row.observed_count is None
                    else row.observed_count,
                    "section": row.section,
                    "candidate_edge_sabs": ";".join(row.candidate_edge_sabs),
                    "reason": row.reason,
                }
            )


def export_binary_matrix(records: Iterable[TransitionRecord], output: Path) -> None:
    rows = list(records)
    sabs = sorted(
        {row.subject_sab for row in rows} | {row.object_sab for row in rows}
    )
    present = {(row.subject_sab, row.object_sab) for row in rows}
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, delimiter="\t", lineterminator="\n")
        writer.writerow(["SAB", *sabs])
        for subject in sabs:
            writer.writerow(
                [subject, *("1" if (subject, obj) in present else "0" for obj in sabs)]
            )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--live",
        type=Path,
        action="append",
        default=[],
        help="optional live Neo4j transition CSV; may be supplied more than once",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=ASSETS / "schema_transitions.csv",
        help="combined source-qualified transition CSV",
    )
    parser.add_argument(
        "--unresolved",
        type=Path,
        default=ASSETS / "schema_transitions_unresolved.csv",
        help="dictionary rows whose edge SAB could not be inferred safely",
    )
    parser.add_argument(
        "--matrix-out",
        type=Path,
        help="optional binary SAB-to-SAB adjacency matrix TSV",
    )
    parser.add_argument(
        "--no-derived-inverses",
        action="store_true",
        help="do not add registered inverse relationships",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    predicate_sabs, registered_pairs = load_predicate_registry()

    records: dict[tuple[str, str, str, str], TransitionRecord] = {}
    load_dcc(records)
    unresolved = load_dictionary(records, predicate_sabs)
    for live_path in args.live:
        load_live_csv(live_path, records)

    inverse_added = 0
    if not args.no_derived_inverses:
        inverse_added = add_registered_inverses(records, registered_pairs)

    write_records(records.values(), args.output)
    write_unresolved(unresolved, args.unresolved)
    if args.matrix_out:
        export_binary_matrix(records.values(), args.matrix_out)

    print(f"Transitions: {len(records):,}")
    print(f"Registered inverse transitions added: {inverse_added:,}")
    print(f"Unresolved dictionary rows: {len(unresolved):,}")
    print(f"Wrote: {args.output}")
    print(f"Wrote: {args.unresolved}")
    if args.matrix_out:
        print(f"Wrote: {args.matrix_out}")

    return 0 if not unresolved else 2


if __name__ == "__main__":
    raise SystemExit(main())
