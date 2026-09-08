# DDKG Agent

This repository provides public tools for working with the NIH Common Fund Data Ecosystem **Data Distillery Knowledge Graph (DDKG)**. The DDKG is a semantic graph framework for cross-domain biomedical discovery that integrates information across genetics, genomics, phenotypes, cohorts, single-cell data, proteomics, metabolomics, clinical resources, and related biomedical knowledge sources.

The repository currently contains two distinct projects:

- [`ddkg-agent-skill/`](ddkg-agent-skill/) contains the portable **DDKG Agent Skill** for generating release-aware Cypher queries from biomedical questions.
- [`website-version/`](website-version/) contains the developing browser-based DDKG query assistant. This is a development scaffold and is not yet a public production service.

## Quick start

To use the DDKG Agent Skill, you need two things:

1. a local or institutional DDKG Neo4j instance; and
2. the `ddkg.skill` file from this repository loaded into an Agent Skills-compatible AI client.

The skill **does not connect to the DDKG and does not execute Cypher**. It generates Cypher and validation guidance for you to run against your DDKG instance.

---

# 1. Install the DDKG

## Step 1: Obtain a free UMLS license

The DDKG distribution uses the UMLS access mechanism.

1. Obtain a UMLS license from the U.S. National Library of Medicine:  
   https://www.nlm.nih.gov/databases/umls.html
2. Save the UMLS credentials or key associated with your account.

## Step 2: Review the DDKG and UBKG documentation

Before installing the graph, review these resources:

- **DDKG User Guide and Data Dictionary, July 2026 schema:**  
  https://github.com/nih-cfde/data-distillery/tree/main/DataDistillery09July2026
- **UBKG context guide:**  
  https://ubkg.docs.xconsortia.org/contexts
- **UBKG documentation:**  
  https://ubkg.docs.xconsortia.org/

The DDKG User Guide includes a tutorial and release-specific examples. The UBKG context documentation is useful for understanding the graph organization and the source-specific contexts that are incorporated into DDKG.

## Step 3: Download the DDKG December 2025 release

1. Go to the DDKG/UBKG downloads site:  
   https://ubkg-downloads.xconsortia.org/
2. Log in using your UMLS account.
3. Download the most recent DDKG  release available to you.

```text
DataDistillery_2025_04_DEC_NEO.zip or
DataDistillery_2025_04_DEC_CSV.zip
```
Because DDKG releases are versioned, this skill build is focused on December 2025 release. If you are using a different release, there should be a skill file in this repo for your particular release.

## Step 4: Install and run the Docker instance

Follow the UBKG installation instructions for your download:

https://ubkg.docs.xconsortia.org/downloads/

A machine with **at least 16 GB of memory available** is recommended in the DDKG installation materials. The graph can be hosted on a server or on a sufficiently capable local computer.

After installation, connect to the Neo4j instance using the connection details created during your Docker setup. You can use Neo4j Browser or another Neo4j client to run Cypher.

## Schema and release compatibility

The DDKG Agent Skill in this repository currently targets the **December 2025 DDKG release** (`DataDistillery_2025_04_DEC`) and the DDKG schema used for releases after August 2025.

Use the August 2025 documentation for this release family:

https://github.com/nih-cfde/data-distillery/blob/main/DataDistillery29August2025

For original Petagraph builds or DDKG Docker builds from before August 2025, the older documentation is here:

https://github.com/nih-cfde/data-distillery/tree/main/DataDistillery03Jan2025
https://github.com/nih-cfde/data-distillery/tree/main/DataDistillery09July2026 

The DDKG project is transitioning toward the JSON Knowledge Graph (JKG) representation. Future DDKG releases will  therefore require a corresponding update to this skill in 2026.

---

# 2. Install the DDKG Agent Skill

The public skill package is:

[`ddkg-agent-skill/ddkg.skill`](ddkg-agent-skill/ddkg.skill)

You can obtain it either by cloning this repository or by downloading the file from GitHub.

## Clone the repository

```bash
git clone https://github.com/TaylorResearchLab/ddkg-agent.git
cd ddkg-agent/ddkg-agent-skill
```

The directory contains the current skill archive plus the public test protocol and versioned test results.

## Load the skill into your AI client

Import or upload `ddkg.skill` using the normal skill-installation mechanism for an **Agent Skills-compatible** AI client. The exact interface depends on the client. See [Agent Skills](https://agentskills.io/home)

For best results, start a new conversation with the DDKG skill enabled and tell the model which DDKG release you are using if it differs from the December 2025 release.

---

# 3. Use the skill to generate DDKG Cypher

Ask a biomedical question in natural language. You can explicitly ask for Cypher, or ask the skill to help translate the question into a DDKG query.

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

The skill is designed to use DDKG-specific identifiers, predicates, source abbreviations, and graph structure rather than generic Neo4j assumptions. It also includes release-specific guidance for known schema and identifier conventions.

## Run the generated query against your DDKG

A typical workflow is:

1. Ask the skill for a DDKG query.
2. Review the proposed graph path, source assumptions, and any biological caveats.
3. Copy the Cypher into Neo4j Browser or your preferred Neo4j client.
4. Run the query against your DDKG instance.
5. If the query fails or returns an unexpected result, give the error message or result summary back to the AI and ask it to revise or validate the query.
6. Do not treat a predicted result as a graph-derived result until the Cypher has actually been executed.

This distinction is important. The skill can generate and explain queries, but the DDKG instance remains the source of truth for what the graph actually contains.

## Ambiguous biological questions

Some abbreviations and biomedical terms have multiple meanings. For example, `ASD` may refer to atrial septal defect or autism spectrum disorder. The skill is designed to resolve important ambiguities before constructing a query rather than silently selecting one interpretation.

## Working with DDKG source subsets

Many DDKG analyses begin by identifying the relevant **SAB** values, where SAB is the source abbreviation used to identify an integrated source. Researchers commonly export a relevant subset from the larger DDKG warehouse and perform downstream computation locally.

Neo4j Graph Data Science (GDS) can also be installed for graph algorithms and rapid prototyping when appropriate. See the Neo4j GDS documentation for installation and supported algorithms.

---

# 4. What the DDKG Agent Skill does not do

The current public skill:

- does not contain or redistribute the DDKG database;
- does not store your UMLS credentials;
- does not connect directly to Neo4j;
- does not execute Cypher;
- does not make an unexecuted query equivalent to a verified graph result;
- does not replace biological interpretation or domain-expert review; and
- is release-specific, so queries should be checked when used with a different DDKG release or schema.

For behavioral validation of the skill, see:

- [`ddkg-agent-skill/ddkg_test_protocol.md`](ddkg-agent-skill/ddkg_test_protocol.md)
- [`ddkg-agent-skill/ddkg_test_results_2026-08-18.md`](ddkg-agent-skill/ddkg_test_results_2026-08-18.md)

---

# 5. Website version

[`website-version/`](website-version/) contains a separate browser-oriented implementation under development. Its planned execution path is:

```text
Natural-language question
        ↓
Typed DDKG query plan
        ↓
Schema-aware deterministic compiler
        ↓
Static validation
        ↓
Neo4j EXPLAIN and bounded preview
        ↓
Bounded read-only execution
        ↓
Results, graph path, sources, and limitations
```

This component is intended to become a natural-language interface that can execute bounded queries against a DDKG instance. It is distinct from the portable `ddkg.skill` package and is not currently presented as a public production website.

---

# 6. DDKG resources

- **DDKG repository:** https://github.com/nih-cfde/data-distillery
- **DDKG preprint:** https://doi.org/10.1101/2025.08.11.666099v3
- **UBKG documentation:** https://ubkg.docs.xconsortia.org/
- **UBKG contexts:** https://ubkg.docs.xconsortia.org/contexts/
- **DDKG downloads:** https://ubkg-downloads.xconsortia.org/
- **UBKG and Petagraph publication:** https://doi.org/10.1038/s41597-024-04070-w
- **HSCLO publication:** https://doi.org/10.1038/s41597-024-04358-x
- **Developer and ETL resources:** https://ubkg.docs.xconsortia.org/#developers
- **JKG RFC:** https://docs.google.com/document/d/1lQF0e8C134gmLB5aHsqYqPYWpC7n__PYMTiRayZ4Bbw

## Contact

For DDKG questions, contact **Deanne Taylor** at `taylordm@chop.edu`.

## Data access and repository hygiene

DDKG data access and redistribution remain subject to the licenses and access requirements of the integrated source resources. Do not commit database credentials, licensed source data, protected institutional configuration, protected health information, or controlled-access biomedical data to this repository.
