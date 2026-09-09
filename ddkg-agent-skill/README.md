# DDKG Agent Skill

The **DDKG Agent Skill** is a portable, release-specific Agent Skill for translating biomedical questions into Cypher queries for the NIH Common Fund Data Ecosystem **Data Distillery Knowledge Graph (DDKG)**.

The skill provides DDKG-specific schema semantics, identifier conventions, source abbreviations, validated query patterns, query guardrails, and biological interpretation guidance. It is intended to reduce failures that occur when a general-purpose language model guesses how a particular DDKG release is organized.

## Current release target

The public skill currently targets the **December 2025 DDKG release**:

```text
DataDistillery_2025_04_DEC
```

It uses the post-August-2025 DDKG structural schema documented by the DDKG and UBKG projects.

Relevant documentation:

- [DDKG User Guide and Data Dictionary](https://github.com/nih-cfde/data-distillery/tree/main/DataDistillery09July2026)
- [UBKG context guide](https://ubkg.docs.xconsortia.org/contexts)
- [UBKG documentation](https://ubkg.docs.xconsortia.org/)

The DDKG project is moving toward the [JSON Knowledge Graph (JKG)](https://github.com/x-atlas-consortia/json-knowledge-graph/tree/main) representation. Later DDKG releases will therefore require corresponding skill versions rather than assuming that this release's query rules remain valid.

**Current R8 release candidate:** 305,719 bytes  
**SHA-256:** `a8f24199de1855cb95fc2d0391ab6d1674ef00b7942dd40e9dfbdf27eac97486`

See [`R8_BUILD.md`](R8_BUILD.md) for the build record and freeze requirement.

## What the skill does

The skill helps an Agent Skills-compatible AI client:

- translate biomedical questions into DDKG-aware Cypher;
- use DDKG-specific identifiers, predicates, source abbreviations, and graph structure;
- resolve important ambiguities before constructing a query;
- distinguish release-specific conventions from generic Neo4j assumptions;
- inspect the graph when a route, identifier, or source is uncertain;
- apply rules for relationship direction, inverse predicates, species, bins, grouping, row grain, and truncation;
- state biological and evidence-semantics caveats that affect interpretation; and
- preserve the distinction between a proposed query and a result actually returned by the graph.

The graph, not the model, determines the result.

## The skill is not a single Markdown prompt

`ddkg.skill` is an installable archive containing a small, self-routed knowledge and validation system. `SKILL.md` is the controller, but most DDKG-specific knowledge is deliberately separated into curated references, primary source documents, machine-readable registries, and a routing layer.

The R8 release candidate contains **38 bundled files** and **258 routing relationships** checked by `route.py --check`.

A simplified view is:

```text
ddkg/
├── SKILL.md                  # controller, behavior contract, workflow, output rules
├── scripts/
│   └── route.py              # topic routing and internal consistency checks
├── references/               # 18 curated working-knowledge documents
├── sources/                  # 8 primary DDKG/UBKG documentation sources
└── assets/                   # 10 machine-readable registries and routing assets
    └── skill_graph.tsv       # topic-to-evidence relationship index
```

This structure separates **behavior**, **navigation**, **curated interpretation**, **primary evidence**, and **machine-readable graph facts**. It also makes individual rules and source-specific patterns easier to repair without rewriting one large prompt.

## How the compositional library works

### Controller

`SKILL.md` defines the supported DDKG schema family, the query-generation workflow, fixed rules, output behavior, and maintenance expectations. It directs the model toward supporting material rather than attempting to hold every DDKG convention in one document.

### Routing layer

The navigation layer consists primarily of:

- `scripts/route.py`, which traverses and validates the routing graph; and
- `assets/skill_graph.tsv`, which links user topics to the materials needed to answer them safely.

Routing relationships include:

- `answers`
- `must_read_with`
- `demonstrated_by`
- `invalidated_by`
- `supersedes`

A topic can therefore retrieve both a useful query pattern and the prerequisites or caveats required to use it correctly. `route.py --check` verifies that routing targets and Markdown anchors still resolve.

### Curated references and primary sources

The `references/` directory contains operational DDKG knowledge, including schema behavior, identifier conventions, SAB and predicate use, DCC endpoint models, entity resolution, validated query patterns, result interpretation, and failure classes found during testing.

The `sources/` directory contains primary DDKG and UBKG documentation. Keeping primary documentation separate from curated working knowledge makes it possible to distinguish a documented claim from a rule learned by running queries against the target release.

### Structured assets

The `assets/` directory contains data better represented as structured tables or registries than prose, including node and edge SABs, predicates, inverse-predicate pairs, evidence classes, endpoint mappings, sample codes, DCC triples, and the routing graph itself.

## Runtime workflow

The skill uses a staged workflow rather than immediately inventing Cypher from scratch:

1. **Find the closest validated query pattern.**
2. **Resolve and disambiguate the entity.** Prefer stable DDKG identifiers when possible.
3. **Profile the anchor.** Inspect which predicates and sources actually touch the entity when the route is uncertain.
4. **Compose the graph route.** Use the endpoint, predicate, and SAB registries and traverse through real DDKG intermediates.
5. **Apply fixed rules.** Check direction, inverse pairs, nullable properties, species, bins, grouping, row grain, limits, and other known silent-failure modes.
6. **Hand over a runnable query.** The skill does not execute it or predict its result.
7. **Interpret the returned result.** Biological interpretation follows execution, not the other way around.

Worked examples teach query shape and interpretation. They are not cached answers.

## R7 portability and query-cost repair

R7 was prompted by a failure discovered during execution-based testing. Earlier guidance incorrectly generalized the index configuration of one development deployment and also exposed an institutional deployment reference in a public skill. R7 removes that assumption entirely.

The public skill now begins query-cost reasoning by asking the active Neo4j deployment what indexes it actually has:

```cypher
SHOW INDEXES YIELD name, type, entityType, labelsOrTypes, properties
```

Deployments may have property indexes on fields such as `Code.CodeID`, `Code.SAB`, and `Concept.CUI`, and may have a TEXT index on `Term.name`. Other deployments may not. Query-cost advice is therefore deployment-neutral.

R7 also changes entity-resolution guidance. Expressions such as `toLower(t.name)` and `trim(toLower(t.name))` prevent a plain index on `Term.name` from directly serving that predicate. The skill now prefers a verified identifier or a source/identifier reduction before tolerant name matching, and recommends staging expensive resolution rather than embedding an unconstrained name scan inside a large traversal.

Use `EXPLAIN` or `PROFILE` when query cost matters.

## Why the skill has guardrails

Many important DDKG query failures are silent. A syntactically valid query can return zero rows or the wrong number of biological entities without raising an error. Failure classes found during development include stale structural-edge names, source-specific predicate direction, incorrect identifier assumptions, duplicated Concept representations, hidden row multiplication, term fan-out, species contamination, source-specific intermediate nodes, and poorly staged high-cost traversals.

For that reason, a query that merely looks plausible is not treated as evidence that it is correct.

The skill also treats **result grain** explicitly. Before returning a list or table, the query should make clear what one row represents and key results on the biological identifier the user intends to count or inspect.

## Requirements

You need:

1. access to a compatible DDKG Neo4j instance; and
2. an AI client that can load an [Agent Skills](https://agentskills.io/home) skill archive.

For DDKG access and installation, see the repository-level [README](../README.md).

## Install the skill

The installable public archive is:

[`ddkg.skill`](ddkg.skill)

You can download the file directly from GitHub or clone the repository:

```bash
git clone https://github.com/TaylorResearchLab/ddkg-agent.git
cd ddkg-agent/ddkg-agent-skill
```

Load `ddkg.skill` using the normal skill-import mechanism for your Agent Skills-compatible AI client.

If you are using a DDKG release other than `DataDistillery_2025_04_DEC`, treat compatibility as unverified unless a corresponding skill build has been tested for that release.

## Use the skill

Ask a biomedical question in natural language. Examples include:

```text
Write me Cypher to find the gene SHH in the DDKG.
```

```text
Which genes are both expressed in heart tissue and associated with a congenital heart defect phenotype?
```

```text
Find eQTLs within chromatin loops on chromosome 22.
```

```text
What metabolites are associated with kidney disease?
```

A typical workflow is:

1. Ask for a DDKG query or query plan.
2. Review the proposed graph path, identifiers, source assumptions, and biological caveats.
3. Run the Cypher in Neo4j Browser or another Neo4j client.
4. If the query fails or returns an unexpected result, provide the error or result summary back to the AI for inspection or revision.
5. Treat only executed graph output as a DDKG-derived result.

## Behavioral validation

The public test materials include:

- [`ddkg_test_protocol.md`](ddkg_test_protocol.md)
- [`ddkg_test_results_TEMPLATE.md`](ddkg_test_results_TEMPLATE.md)
- [`ddkg_test_results_2026-08-18.md`](ddkg_test_results_2026-08-18.md)

The protocol requires fresh conversations, verbatim query capture, and execution of generated queries against a real DDKG instance. The model's own statement that a query is correct is not a pass criterion.

The 18 August 2026 results file predates later repairs and is retained only as an example of the testing method. Its pass/fail results do not transfer to R7.

The orthogonal Tier 7 evaluation discussed in the accompanying manuscript was performed on an earlier R5b-rebased archive, SHA-256 `c092480a61f2e46efb3586aacfe2240a3cebb83a0c769c5dfa0eb5ea54b8c52b`. Those results likewise must not be presented as validation of R7. The complete Tier 7 record accompanies the manuscript as supplementary material.

New behavioral results should be stored in a new dated results file and stamped with the SHA-256 of the exact `ddkg.skill` archive under test.

## Reproducible source and release checks

The unpacked public source for the archive is kept under [`source/ddkg/`](source/ddkg/).

- `build_skill.py` rebuilds `ddkg.skill` deterministically after running `route.py --check`.
- `check_public_skill_hygiene.py` scans a source tree or built archive for generic local/private artifacts and can accept an external deployment-specific denylist at release time.
- [`R7_BUILD.md`](R7_BUILD.md) records the exact R7 archive size, checksum, routing count, and repair summary.

Deployment-specific denylist terms should be kept outside the repository so that the release check does not itself publish private hostnames or institutional infrastructure names.

## What the skill does not do

The public skill:

- does not contain or redistribute the DDKG database;
- does not store UMLS or Neo4j credentials;
- does not connect directly to Neo4j;
- does not execute Cypher;
- does not make an unexecuted query equivalent to a graph-derived result;
- does not replace biological interpretation or domain-expert review; and
- should not be assumed compatible with a different DDKG release or schema.

## Directory contents

```text
ddkg-agent-skill/
├── README.md
├── R7_BUILD.md
├── build_skill.py
├── check_public_skill_hygiene.py
├── ddkg.skill
├── source/
│   └── ddkg/                    # unpacked source used to build ddkg.skill
├── ddkg_test_protocol.md
├── ddkg_test_results_2026-08-18.md
└── ddkg_test_results_TEMPLATE.md
```

`ddkg.skill` is the installable artifact. The source tree makes the archive inspectable and reproducible rather than leaving the public skill as an opaque binary package.

## Relationship to the DDKG MCP Server

The skill and the [`ddkg-mcp-server`](../ddkg-mcp-server/) project have complementary roles but are not currently one production system.

- The **skill** provides release-specific DDKG reasoning, identifiers, source semantics, query guidance, and biological caveats.
- The **MCP server** is being developed to provide controlled access to a live DDKG instance and return results derived from actual graph execution.

The current skill targets the December 2025 release. The MCP server is being developed for the forthcoming JKG-era DDKG release.

## Data access and repository hygiene

DDKG data access and redistribution remain subject to the licenses and access requirements of the integrated source resources. Do not commit database credentials, licensed source data, protected institutional configuration, protected health information, controlled-access biomedical data, private hostnames, or internal infrastructure paths to this repository.

For general DDKG resources and contact information, see the repository-level [README](../README.md).
