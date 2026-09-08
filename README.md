# DDKG Agent

This repository provides public tools for working with the NIH Common Fund Data Ecosystem **Data Distillery Knowledge Graph (DDKG)**. The DDKG is a semantic graph framework for cross-domain biomedical discovery that integrates information across genetics, genomics, phenotypes, cohorts, single-cell data, proteomics, metabolomics, clinical resources, and related biomedical knowledge sources.

The repository contains two distinct projects:

| Project | Purpose | Current release target |
| --- | --- | --- |
| [`ddkg-agent-skill/`](ddkg-agent-skill/) | Portable DDKG Agent Skill for release-aware query planning and Cypher generation | December 2025 DDKG (`DataDistillery_2025_04_DEC`) |
| [`ddkg-mcp-server/`](ddkg-mcp-server/) | Developing MCP server for controlled, read-only access to a live DDKG instance | Forthcoming JKG-era 2026 DDKG |

These projects are complementary but are not currently a single production system. The skill provides DDKG-specific reasoning and query guidance. The MCP server is being developed to provide controlled execution against an actual graph.

## Start here

If you want to **use the current DDKG Agent Skill**, see:

- [`ddkg-agent-skill/README.md`](ddkg-agent-skill/README.md)
- [`ddkg-agent-skill/ddkg.skill`](ddkg-agent-skill/ddkg.skill)

If you want to **develop or inspect the MCP server**, see:

- [`ddkg-mcp-server/README.md`](ddkg-mcp-server/README.md)
- [`ddkg-mcp-server/docs/ARCHITECTURE.md`](ddkg-mcp-server/docs/ARCHITECTURE.md)
- [`ddkg-mcp-server/docs/OPERATING_MODEL.md`](ddkg-mcp-server/docs/OPERATING_MODEL.md)

## Obtain a DDKG instance

### 1. Obtain a free UMLS license

The distributed DDKG/UBKG packages use the UMLS access mechanism.

- U.S. National Library of Medicine UMLS licensing:  
  https://www.nlm.nih.gov/databases/umls.html

### 2. Review the DDKG and UBKG documentation

- **DDKG User Guide and Data Dictionary, July 2026 schema:**  
  https://github.com/nih-cfde/data-distillery/tree/main/DataDistillery09July2026
- **UBKG context guide:**  
  https://ubkg.docs.xconsortia.org/contexts
- **UBKG documentation:**  
  https://ubkg.docs.xconsortia.org/

The DDKG User Guide includes a tutorial and release-specific examples. The UBKG context documentation is useful for understanding graph organization and integrated source contexts.

### 3. Download the December 2025 DDKG release

Go to:

https://ubkg-downloads.xconsortia.org/

Log in using your UMLS account and download the appropriate December 2025 package:

```text
DataDistillery_2025_04_DEC_NEO.zip
or
DataDistillery_2025_04_DEC_CSV.zip
```

Follow the UBKG installation instructions:

https://ubkg.docs.xconsortia.org/downloads/

A machine with **at least 16 GB of memory available** is recommended in the DDKG installation materials.

The December 2025 release is the graph currently targeted by the public DDKG Agent Skill. The MCP server is being developed for the forthcoming JKG-era release and should not be assumed to use the same schema conventions.

## Release and schema compatibility

DDKG releases are versioned, and both projects in this repository are intentionally release-aware.

The public skill currently targets:

```text
DataDistillery_2025_04_DEC
```

using the post-August-2025 DDKG schema family documented here:

https://github.com/nih-cfde/data-distillery/tree/main/DataDistillery09July2026

Older Petagraph/DDKG documentation is available at:

- https://github.com/nih-cfde/data-distillery/tree/main/DataDistillery03Jan2025
- https://github.com/nih-cfde/data-distillery/blob/main/DataDistillery29August2025

The DDKG project is transitioning toward the [JSON Knowledge Graph (JKG)](https://github.com/x-atlas-consortia/json-knowledge-graph/tree/main) representation. That transition changes graph representation and requires release-specific updates to the skill and MCP compatibility layer.

## Skill versus MCP server

The two subprojects address different parts of the workflow:

```text
DDKG Agent Skill
    biomedical question
          ↓
release-aware DDKG reasoning
query plan / Cypher / validation guidance

DDKG MCP Server
    MCP-compatible client
          ↓
release/schema checks
validation and guardrails
bounded read-only execution
          ↓
      DDKG Neo4j
```

The **skill does not execute Cypher**. It generates and explains DDKG-aware queries for a user to run against a compatible DDKG instance.

The **MCP server** is intended to execute approved, bounded, read-only graph requests while keeping database credentials and execution policy outside the language model. It is currently an early development project.

For detailed usage, limitations, architecture, and validation information, use the README in the relevant subdirectory rather than this repository landing page.

## DDKG resources

- **DDKG repository:** https://github.com/nih-cfde/data-distillery
- **DDKG preprint:** https://doi.org/10.1101/2025.08.11.666099v3
- **UBKG documentation:** https://ubkg.docs.xconsortia.org/
- **UBKG contexts:** https://ubkg.docs.xconsortia.org/contexts/
- **DDKG downloads:** https://ubkg-downloads.xconsortia.org/
- **UBKG and Petagraph publication:** https://doi.org/10.1038/s41597-024-04070-w
- **HSCLO publication:** https://doi.org/10.1038/s41597-024-04358-x
- **Developer and ETL resources:** https://ubkg.docs.xconsortia.org/#developers
- **JKG repository:** https://github.com/x-atlas-consortia/json-knowledge-graph/tree/main
- **JKG RFC:** https://docs.google.com/document/d/1lQF0e8C134gmLB5aHsqYqPYWpC7n__PYMTiRayZ4Bbw

## Contact

For DDKG questions, contact **Deanne Taylor** at `taylordm@chop.edu`.

## Data access and repository hygiene

DDKG data access and redistribution remain subject to the licenses and access requirements of the integrated source resources. Do not commit database credentials, licensed source data, protected institutional configuration, protected health information, or controlled-access biomedical data to this repository.
