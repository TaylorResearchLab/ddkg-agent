# R9 schema-level route planner

## Status

Prototype design for a post-R8 DDKG Agent Skill release. This work is isolated on `r9-schema-route-planner` so that the R8 release-candidate archive and its evaluation remain unchanged.

## Motivation

DDKG query construction repeatedly requires the same structural operation: determine whether one source/identifier space can reach another, identify the admissible intermediate sources, and preserve the predicate, edge SAB, and direction of every transition. This should not depend on an LLM rediscovering graph routes from prose or by repeatedly probing the full Neo4j graph.

The proposed R9 planner treats DDKG as a small schema-level transition graph whose states are source abbreviations (SABs) and whose transitions are source-qualified relationship types. The current `assets/data_dictionary_triples.json` already provides a sparse representation of much of this graph:

`subject SAB -> predicate / edge source -> object SAB`

The planner should convert that sparse transition table into an in-memory adjacency structure and use deterministic path search to propose valid routes before Cypher is written.

## Precedent in Petagraph

Petagraph already used a related matrix view of graph connectivity. Figures 5-7 of Stear et al., *Scientific Data* 2024 (doi:10.1038/s41597-024-04070-w), summarize pairwise connectivity among selected Semantic Types using presence/absence, relationship-type-plus-SAB diversity, and relationship counts. R9 applies the same general idea at the operational query-routing level, using SAB/predicate transitions rather than Semantic Type pairs.

## Core representation

The basic sparse transition record is:

```text
subject_sab
predicate
edge_sab
object_sab
direction
count
source/validation status
```

For the first prototype, `data_dictionary_triples.json` supplies subject SAB, predicate, object SAB, count, and source section. The edge SAB is not always explicit in that file and will need to be joined from the predicate/SAB registries or a generated live-schema asset before the planner is considered complete.

A binary adjacency matrix can be derived as:

```text
A[i,j] = 1 if at least one admissible transition connects SAB_i -> SAB_j
```

A more informative sparse tensor is:

```text
T[subject_sab, object_sab, predicate, edge_sab, direction]
```

The dense one-hot matrix is useful for reachability and all-pairs preprocessing. The sparse transition table is retained for reconstructing the exact DDKG route.

## Algorithm

### Phase 1: unweighted routing

Use dynamic reachability / breadth-first search over SAB states to find the minimum number of transitions between a start and target SAB. Retain predecessor transitions so the exact predicate and direction can be reconstructed.

For approximately 200 SABs, the state space is small enough to precompute all-pairs reachability and shortest path lengths if useful.

### Phase 2: weighted routing

Replace pure hop count with a cost function. Candidate penalties include:

- validated direct source-to-source transition: low cost;
- source/identifier normalization bridge: modest cost;
- species transition: modest cost;
- high fan-out or known row-multiplication risk: higher cost;
- synonym/name-resolution requirement: higher cost;
- structurally incompatible entity level: disallowed;
- failed prerequisite diagnostic: disallowed.

This converts route selection from "fewest edges" to "lowest-risk admissible route."

### Phase 3: richer state

SAB alone can be too permissive because several Codes can coexist on one normalized Concept. The production state should therefore be able to distinguish at least:

```text
SAB
entity/biological role
species when relevant
```

This is required to prevent invalid routes such as treating a variant-level OTG endpoint as an HGNC gene merely because both can participate in nearby normalized Concepts.

## Example

The R8 live regression for the ciliary transition zone showed the kind of route R9 should find deterministically:

```text
GO
  -> UNIPROTKB via part_of
UNIPROTKB
  -> HGNC via gene_product_of
HGNC
  -> MGI via in_1_to_1_orthology_relationship_with / HCOP
MGI
  -> MP via involved_in / MPMGI
```

The route existed even though the GO anchor had no direct HGNC connection.

## Division of labor

The intended architecture is:

1. LLM interprets the user's biological question and identifies start/target states plus constraints.
2. Deterministic route planner finds admissible schema paths.
3. LLM constructs Cypher from a returned route rather than inventing the route.
4. Existing DDKG guardrails check identifiers, multiplicity, labels, bins, species, evidence semantics, and result interpretation.

## Initial prototype

`source/ddkg/scripts/route_schema.py` is the first prototype. It reads the existing triple asset, constructs the SAB adjacency graph, and returns shortest routes while preserving the predicate and source section for each transition. It can also export a binary SAB-to-SAB adjacency matrix.

This prototype is deliberately conservative. It does not yet claim that every path it finds is biologically valid. The main engineering goal is to separate deterministic schema navigation from LLM reasoning and then add the entity-level and biological constraints required for production use.

## Acceptance tests for the prototype

At minimum, the planner should recover known routes or correctly report no route for:

- `GO -> HGNC` through `UNIPROTKB` when the relevant transition asset contains the component-to-protein relation;
- `HGNC -> MP` through `HCOP` and `MPMGI`;
- `4DNL -> HSCLO` directly;
- `UNIPROTKB -> HGNC` directly;
- a deliberately incompatible source pair when no admissible route is represented.

The exact route must include every intermediate SAB and predicate. A route is not accepted merely because the endpoint is reachable.

## R8 boundary

No R9 planner code is to be merged into the R8 branch. R8 should finish its focused engineering regressions, freeze, and complete cross-assistant evaluation as planned. R9 can proceed in parallel and be rebased onto the final R8/main lineage after R8 is frozen.
