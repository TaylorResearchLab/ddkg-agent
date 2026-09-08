# DDKG Agent Skill

The **DDKG Agent Skill** is a portable, release-aware skill for translating biomedical questions into Cypher queries for the NIH Common Fund Data Ecosystem **Data Distillery Knowledge Graph (DDKG)**.

The skill provides DDKG-specific schema semantics, identifier conventions, source abbreviations, validated query patterns, and biological interpretation guidance. It is intended to reduce common failure modes that arise when a general-purpose language model guesses how a DDKG release is organized.

## Current release target

The public skill in this directory currently targets the **December 2025 DDKG release**:

```text
DataDistillery_2025_04_DEC
```

and the DDKG schema used for releases after August 2025.

Relevant documentation for this release family:

- [DDKG User Guide and Data Dictionary, July 2026 schema](https://github.com/nih-cfde/data-distillery/tree/main/DataDistillery09July2026)
- [UBKG context guide](https://ubkg.docs.xconsortia.org/contexts)
- [UBKG documentation](https://ubkg.docs.xconsortia.org/)

For older Petagraph or DDKG Docker builds, use the documentation that matches that release rather than assuming the current skill conventions apply unchanged.

The DDKG project is transitioning toward the [JSON Knowledge Graph (JKG)](https://github.com/x-atlas-consortia/json-knowledge-graph/tree/main) representation. Future DDKG releases will therefore require corresponding updates to the skill.

## What the skill does

The skill helps an Agent Skills-compatible AI client:

- translate biomedical questions into DDKG-aware Cypher;
- use DDKG-specific identifiers, predicates, source abbreviations, and graph structure;
- resolve important ambiguities before constructing a query;
- distinguish release-specific conventions from generic Neo4j assumptions;
- suggest validation and inspection queries when a graph path or identifier is uncertain;
- state biological and evidence-semantics caveats that affect interpretation; and
- preserve the distinction between a proposed query and a result actually returned by the graph.

The skill is especially useful for questions that require combining information across multiple DDKG sources rather than querying a single ontology or database in isolation.

## What the skill does not do

The current public skill:

- does not contain or redistribute the DDKG database;
- does not store UMLS credentials;
- does not connect directly to Neo4j;
- does not execute Cypher;
- does not make an unexecuted query equivalent to a verified graph result;
- does not replace biological interpretation or domain-expert review; and
- is release-specific, so queries should be rechecked when used with a different DDKG release or schema.

The DDKG instance remains the source of truth for what the graph actually contains.

## Requirements

You need:

1. access to a compatible DDKG Neo4j instance; and
2. an AI client that can load an [Agent Skills](https://agentskills.io/home) skill archive.

For the December 2025 DDKG distribution, obtain a UMLS license and download the appropriate DDKG package through the UBKG/DDKG distribution mechanism. The repository-level [README](../README.md) contains the shared DDKG access and installation links.

## Install the skill

The public skill archive is:

[`ddkg.skill`](ddkg.skill)

You can download that file directly from GitHub or clone this repository:

```bash
git clone https://github.com/TaylorResearchLab/ddkg-agent.git
cd ddkg-agent/ddkg-agent-skill
```

Load `ddkg.skill` using the normal skill-import mechanism for your Agent Skills-compatible AI client.

For best results, start a new conversation with the skill enabled. If the DDKG release you are using differs from `DataDistillery_2025_04_DEC`, tell the model explicitly and treat compatibility as unverified unless that release has a corresponding tested skill build.

## Using the skill

Ask a biomedical question in natural language. You can ask directly for Cypher or ask the skill to help translate the question into a DDKG query plan.

Examples:

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

```text
Which drugs target proteins encoded by genes in the RAS/MAPK pathway?
```

A typical workflow is:

1. Ask the skill for a DDKG query or query plan.
2. Review the proposed graph path, identifiers, source assumptions, and biological caveats.
3. Copy the Cypher into Neo4j Browser or another Neo4j client.
4. Execute the query against the DDKG instance.
5. If it fails or returns an unexpected result, give the error message or result summary back to the AI and ask it to revise or validate the query.
6. Treat only executed graph output as a DDKG-derived result.

## Ambiguous biological questions

Biomedical abbreviations and labels can be ambiguous. For example, `ASD` may refer to atrial septal defect or autism spectrum disorder. The skill is designed to resolve important ambiguity before constructing a query rather than silently selecting one interpretation.

## Working with DDKG source subsets

Many DDKG analyses begin by identifying the relevant **SAB** values, where SAB is the source abbreviation used to identify an integrated source. Researchers may then export a relevant subset from the larger DDKG warehouse for downstream computation.

Neo4j Graph Data Science can also be used for graph algorithms and prototyping when appropriate, but GDS is separate from the skill itself.

## Behavioral validation

This directory includes a versioned behavioral test protocol:

- [`ddkg_test_protocol.md`](ddkg_test_protocol.md)
- [`ddkg_test_results_TEMPLATE.md`](ddkg_test_results_TEMPLATE.md)
- [`ddkg_test_results_2026-08-18.md`](ddkg_test_results_2026-08-18.md)

The protocol requires fresh conversations, verbatim query capture, and execution of generated queries against a real DDKG instance. A query that merely looks plausible is not considered validated.

The dated 18 August 2026 results file is only an example of the types of tests we used to test the performance of the skill.  It predates several later skill repairs and states that its pass/fail results do not transfer to the current R2 archive. We're including it here so you can see an example of how we tested the skill using a multi-step testing protocol.  

New behavioral results should be stored in a new dated results file and stamped with the SHA-256 of the exact `ddkg.skill` archive under test.

## Directory contents

```text
ddkg-agent-skill/
├── README.md
├── ddkg.skill
├── ddkg_test_protocol.md
├── ddkg_test_results_2026-08-18.md
└── ddkg_test_results_TEMPLATE.md
```

`ddkg.skill` is the installable public artifact. The protocol and result files document how behavior is evaluated without treating an older test run as evidence for a newer archive.

## Relationship to the DDKG MCP Server

The skill and the [`ddkg-mcp-server`](../ddkg-mcp-server/) project have complementary roles, but they are not currently a single production system.

- The **skill** provides DDKG-specific reasoning, release semantics, identifier conventions, query guidance, and biological caveats.
- The **MCP server** is being developed to provide controlled access to a live DDKG instance and return results derived from actual graph execution.

The current skill targets the December 2025 release, while the MCP-server project is being developed for the forthcoming JKG-era DDKG release. Do not assume cross-release compatibility without explicit validation.

## Data access and repository hygiene

DDKG data access and redistribution remain subject to the licenses and access requirements of the integrated source resources. Do not commit database credentials, licensed source data, protected institutional configuration, protected health information, or controlled-access biomedical data to this repository.

For general DDKG resources and contact information, see the repository-level [README](../README.md).
