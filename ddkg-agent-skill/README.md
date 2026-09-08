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

## The skill is not a single Markdown prompt

`ddkg.skill` is an installable archive containing a small, self-routed knowledge and validation system. `SKILL.md` is the controller, but most of the DDKG-specific knowledge is deliberately separated into curated references, primary source documents, machine-readable registries, and a routing layer.

The current R6 package contains **38 bundled files**. Its internal routing graph contains **239 relationships** checked by `route.py --check`.

A simplified view of the archive is:

```text
ddkg/
├── SKILL.md                  # controller, behavior contract, workflow, output rules
├── scripts/
│   └── route.py              # topic routing and internal consistency checks
├── references/               # 18 curated working-knowledge documents
├── sources/                  # 8 bundled primary documentation sources
└── assets/                   # 10 machine-readable registries and routing assets
    └── skill_graph.tsv       # topic-to-evidence relationship index
```

This structure is intentional. A large graph such as DDKG contains many source-specific conventions that are easy for a language model to confuse. Putting all of them into one long prompt would make maintenance, precedence, validation, and release-specific repair difficult. The package instead separates **behavior**, **navigation**, **curated interpretation**, **primary evidence**, and **machine-readable facts**.

## How the skill was designed

### 1. `SKILL.md` is the controller, not the whole knowledge base

`SKILL.md` defines when the skill should activate, the expected DDKG schema family, the query-generation workflow, fixed query rules, output behavior, and maintenance expectations. It acts as a behavior contract for the AI client.

The controller directs the model toward supporting material rather than expecting it to recall every DDKG convention from one document.

### 2. The routing layer determines what supporting material must be read

The navigation layer consists primarily of:

- `scripts/route.py`, which traverses and validates the skill graph; and
- `assets/skill_graph.tsv`, which links user topics to the references needed to answer them safely.

The routing graph does more than map a keyword to a page. It records relationships such as:

- `answers`
- `must_read_with`
- `demonstrated_by`
- `invalidated_by`
- `supersedes`

That allows a topic such as a phenotype, tissue, cell type, compound, eQTL, pathway, or source-specific query to pull in not only an answer pattern but also required caveats and prerequisites. It also provides a maintenance mechanism: when a finding invalidates an older assumption, the dependency can be represented rather than silently leaving contradictory guidance in the package.

`route.py` also provides mechanical checks so broken file or heading targets can be caught before a skill build is accepted.

### 3. Curated references contain working DDKG knowledge

The `references/` directory contains the operational knowledge needed to query this release correctly. These files cover topics such as:

- source and documentation precedence;
- the DDKG/UBKG data model and actual release schema;
- identifier conventions and entity resolution;
- source abbreviation (`SAB`) behavior;
- predicates and inverse-predicate handling;
- Data Coordinating Center and other source-specific endpoint models;
- validated query patterns and task indexing;
- query-construction rules;
- interpretation of returned evidence;
- setup and access behavior; and
- later failure classes discovered during live testing, including row multiplicity, identity sinks, minted Concept twins, result grain, and source-specific topology.

These references are curated working knowledge rather than copies of external documentation. They encode what was learned by reconciling documentation with the behavior of the actual DDKG release.

### 4. Primary documentation is bundled separately from interpretation

The `sources/` directory contains primary DDKG and UBKG documentation used to verify claims and settle conflicts, including the DDKG User Guide and relevant UBKG documentation for APIs, contexts, the data model, downloads, glossary, ingest formats, and versioning.

Keeping primary sources separate from curated references makes the provenance of a rule clearer. The skill can distinguish a statement taken from project documentation from an operational rule derived from testing the actual graph.

### 5. Machine-readable assets constrain composition

The `assets/` directory contains registries and tables that are better represented as structured data than prose. These include resources for items such as:

- node and edge SABs;
- predicates;
- inverse-predicate pairs;
- evidence classes;
- DDKG endpoint mappings;
- curated triples and sample codes; and
- the skill routing graph itself.

These assets reduce the need for the model to reconstruct graph facts from prose or memory when composing a query.

## Runtime workflow

The skill uses a staged query workflow rather than immediately asking the language model to invent Cypher from scratch:

1. **Find the closest validated query pattern.** Start from the validated task/query index where possible rather than composing entirely from memory.
2. **Resolve and disambiguate the entity.** Prefer stable DDKG identifiers such as `CodeID`; clarify scientific ambiguity when it changes the intended query.
3. **Profile the anchor.** Inspect which predicates and sources actually touch the selected entity when the route is uncertain.
4. **Compose the graph route.** Use the endpoint, predicate, and SAB registries and traverse through real DDKG intermediates.
5. **Apply fixed query rules.** Handle relationship direction, inverse pairs, nullable properties, species, bins, grouping, row grain, limits, and other known silent-failure modes.
6. **Hand over a runnable query.** The intended product is executable Cypher with appropriate audit information, not a predicted database answer.
7. **Interpret the returned result.** Only after execution should the assistant discuss evidence type, source scope, independence, truncation, coverage, or the possible meanings of an empty result.

A central design rule is that **the graph, not the model, determines the result**. Worked examples teach query shape and interpretation. They are not cached answers to be repeated as though they were current graph output.

## Why the skill has so many guardrails

Many important DDKG query failures are *silent*. A syntactically valid Cypher query can return zero rows or the wrong number of rows without producing an error. Examples encountered during development included stale structural edge names, source-specific predicate direction, identifier conventions, duplicated assertions across minted Concept twins, hidden row multiplication, parent-term fan-out, placeholder identifiers, species-specific sources, and source models that require an intermediate association node.

For that reason, the skill was designed around **falsifiability and inspection**, not just fluent query generation. A good-looking query is not considered evidence that the query is correct.

The package also distinguishes **result grain** from query syntax. Before returning a list or table, the query should make explicit what one row represents and key the output on the biological identifier the user intends to count or inspect. This prevents a Concept-level fan-out from masquerading as multiple biological entities.

## Validation-driven development

The skill has been developed iteratively against real DDKG instances. Behavioral tests are used to find failures that cannot be detected reliably by reading the generated Cypher alone.

The test protocol includes regression, novel, adversarial, ambiguity, evidence-semantics, scale, and result-grain cases. Tests are run in fresh conversations, generated queries are captured verbatim, and the queries are executed against the target DDKG release. The model's own claim that a query is correct is not a pass criterion.

Later skill revisions incorporated failures discovered during these live tests. For example, the R6 revision repaired two documented assumptions that produced silent-zero queries, added source-specific topology for DisGeNET, clarified mouse knockout and orthology evidence, and expanded routing for anatomy, cell-type, and marker questions. This is why the skill should be viewed as a **versioned, release-calibrated query instrument**, not a static prompt.

The current archive is an engineered and curated Agent Skill package. It is not a separately fine-tuned language model and does not modify model weights. Its performance comes from the package's controller, routing graph, curated evidence, structured registries, validated query patterns, and iterative testing against the DDKG release.

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

The dated 18 August 2026 results file is only an example of the types of tests we used to test the performance of the skill. It predates several later skill repairs and states that its pass/fail results do not transfer to the current archive. It is included so users can see an example of the multi-step testing protocol.

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
