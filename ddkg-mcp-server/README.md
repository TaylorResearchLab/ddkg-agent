# DDKG MCP Server

A release-aware Model Context Protocol (MCP) server for controlled access to the Data Distillery Knowledge Graph (DDKG).

This project is intended to allow MCP-compatible AI clients to interact with a live DDKG instance through a constrained server interface. The MCP server, not the language model, owns the database connection and enforcement of query limits. The DDKG Neo4j instance remains the source of truth for returned graph results.

The initial target is the **December 2025 DDKG release** (`DataDistillery_2025_04_DEC`). The server must remain explicitly release-aware because future DDKG releases, including the planned JKG-based generation, will use a different schema and will require corresponding compatibility updates.

## Project objective

The first objective is to establish one reproducible path from an MCP client request to:

1. release and schema identification;
2. a typed DDKG query request or plan;
3. deterministic validation and bounded Cypher construction or acceptance;
4. read-only execution against the DDKG;
5. transparent results with graph-path, source, provenance, and limitation information.

The server is not intended to provide unrestricted database access. It should expose a small, auditable set of DDKG capabilities through MCP tools and resources.

## Planned architecture

```text
MCP-compatible client
(ChatGPT, Claude, Codex, or another MCP client)
                ↓
         DDKG MCP Server
                ↓
      release/schema checks
      request validation
      query guardrails
      Neo4j EXPLAIN/preview
      bounded read-only execution
                ↓
           DDKG Neo4j
                ↓
 results + sources + provenance + limitations
```

The language model should not receive or manage Neo4j credentials. Only the MCP server's controlled execution layer may connect to Neo4j.

## Relationship to the DDKG Agent Skill

This repository also contains the release-specific [`../ddkg-agent-skill/`](../ddkg-agent-skill/) package. The two components have different roles.

### DDKG Agent Skill

The skill provides the AI client with release-specific knowledge about:

- DDKG schema structure;
- identifier conventions;
- source abbreviations (SABs);
- predicates and graph motifs;
- query construction guidance;
- known semantic caveats and ambiguity handling.

The skill does **not** connect to Neo4j and does **not** execute queries.

### DDKG MCP Server

The MCP server is intended to provide:

- controlled access to an actual DDKG instance;
- release and schema inspection;
- identifier and concept resolution against the graph;
- bounded read-only query execution;
- graph-derived results rather than predicted results;
- source, provenance, and limitation information suitable for downstream interpretation.

An MCP client may eventually use both components together: the skill for DDKG-specific reasoning and the MCP server for live graph access.

## Candidate MCP capabilities

The exact public tool and resource names are not yet fixed. The initial server should focus on a small set of typed capabilities rather than unrestricted Cypher execution. Candidate capabilities include:

- report the DDKG release and schema generation;
- inspect available DDKG source abbreviations and source metadata;
- resolve identifiers and labels to graph entities;
- search concepts or codes;
- inspect relationships and predicates available for a resolved entity;
- validate a proposed DDKG query plan;
- execute approved, bounded, read-only queries;
- return query provenance, source information, and limitations with results.

A general read-only Cypher tool may be considered later, but it should not be the only or primary public interface unless validation, timeout, path, and row limits are enforced server-side.

## Execution and safety principles

- The MCP server is read-only with respect to the DDKG.
- The model does not receive Neo4j credentials.
- User-provided values should be passed as query parameters rather than interpolated into Cypher strings.
- Requests should be checked against the supported DDKG release and schema.
- Query execution should be bounded by timeout, row count, path depth, and response-size limits.
- Static validation and Neo4j `EXPLAIN` or an equivalent preview step should precede nontrivial execution where appropriate.
- Returned answers must distinguish graph-derived results from model interpretation.
- Provenance and SAB/source information should be preserved where available.
- Ambiguous biomedical terminology should be resolved before execution when it materially changes the graph query.
- No database credentials, licensed source data, protected institutional configuration, PHI, or controlled-access biomedical data may be committed to this repository.

## Release compatibility

The initial implementation is being developed for:

```text
DDKG release: DataDistillery_2025_04_DEC
Public shorthand: DDKG December 2025
Schema family: pre-JKG DDKG/UBKG-derived schema
```

Future DDKG releases should not silently reuse this compatibility layer. When the DDKG moves to the JKG-based schema, the MCP server should expose or record the active release and use a corresponding release-specific schema registry, query motifs, tests, and compatibility declaration.

The server should eventually be able to answer a basic introspection request such as "Which DDKG release are you connected to?" from the live deployment configuration rather than from model recall.

## Current repository scaffold

The current directory was originally scaffolded around a browser-oriented natural-language DDKG assistant. That implementation plan has now been superseded by the MCP-server objective. The useful typed planning, validation, schema, testing, and bounded-execution concepts are being retained, while the transport and public interface will be refactored around MCP.

Current layout:

```text
.
├── deploy/                   # Deployment configuration and operating notes
├── docs/                     # Architecture and operating procedures
├── examples/                 # Validated requests, plans, motifs, and expected outputs
├── schemas/                  # Typed query-plan and release-specific schema definitions
├── src/ddkg_agent/           # Current Python source scaffold
├── tests/                    # Unit, regression, integration, and adversarial tests
├── .env.example              # Non-secret environment variable template
└── pyproject.toml            # Python package and test configuration
```

The existing Python package name `ddkg_agent` is retained for the moment because this is still an early scaffold. It can be renamed when the MCP server implementation and public package boundary are stabilized.

Key existing documents:

- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)
- [`docs/OPERATING_MODEL.md`](docs/OPERATING_MODEL.md)
- [`schemas/query_plan.schema.json`](schemas/query_plan.schema.json)
- [`examples/README.md`](examples/README.md)
- [`deploy/README.md`](deploy/README.md)

Some of these documents still reflect the earlier browser-oriented plan and will need to be updated as the MCP implementation proceeds.

## Current status

**Stage:** early scaffold / MCP refactor

Already present:

- Python source layout;
- typed query-plan model;
- JSON Schema v0.1;
- initial smoke test;
- architecture and operating-model placeholders;
- environment and deployment placeholders;
- Git and Notion audit workflow.

Not yet implemented:

- an MCP server transport;
- a stable public MCP tool/resource contract;
- live Neo4j execution through MCP;
- release introspection from a deployed DDKG instance;
- general DDKG identifier-resolution tools;
- production authentication or deployment hardening.

The current code should therefore be treated as a development scaffold, not as a working public MCP endpoint.

## Local development

Python 3.11 or later is required.

```bash
git clone https://github.com/TaylorResearchLab/ddkg-agent.git
cd ddkg-agent/ddkg-mcp-server
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e '.[dev]'
python -m pytest -q
```

The current smoke test does not require an MCP client, Neo4j, DDKG credentials, or network access.

## Development roadmap

A sensible implementation sequence is:

1. **MCP contract and server skeleton**: define the first small set of resources/tools and establish the server transport.
2. **Release and schema registry**: make DDKG release compatibility explicit and machine-readable.
3. **Read-only Neo4j adapter**: establish controlled connection handling, parameterization, timeouts, limits, and `EXPLAIN`/preview behavior.
4. **Typed DDKG tools**: implement identifier resolution, source/schema inspection, concept search, and bounded graph-query capabilities.
5. **Client integration**: validate the server with one or more MCP-compatible AI clients.
6. **Evaluation and hardening**: regression, adversarial, semantic, performance, security, and failure-mode testing.
7. **Pilot deployment**: deploy a documented read-only instance when the preceding gates are satisfied.

A browser interface is not the primary deliverable. A website could later be implemented as one possible client of the MCP server if useful.

## Development and review workflow

Work is organized into bounded sprints with explicit objectives, deliverables, dependencies, tests, and exit gates.

- Deanne approves project scope and sprint exit gates.
- GPT and Claude act as coding and review collaborators.
- Source changes are committed to Git.
- Meaningful runs are tied to a branch and commit SHA.
- Formal executions are recorded with environment, command, inputs, outputs, metrics, and review status.
- No sprint is complete until its deliverables are committed and its exit gate is satisfied.

Short-lived feature branches and reviewed merges are preferred once more than one developer is making concurrent code changes. Secrets, credentials, protected host information, and institutional configuration must not be committed.

## Project coordination

Project management and run evidence are maintained in the DDKG Agent Notion workspace:

- [DDKG Agent project page](https://app.notion.com/p/39f2918780088130828fcaa45c81e7d9)
- [Sprint plan and Kanban board](https://app.notion.com/p/8dbfeb1699f2417086d193df9cf1c454)
- [Collaborative Developer Log](https://app.notion.com/p/af5e464943f24731897fba734f7357d5)
- [Test Run Audit Log](https://app.notion.com/p/de919accdbf64ffab3e6d0912eb86da8)
- [Repository and Environment Manifest](https://app.notion.com/p/39f2918780088118b38feb1e1ea42141)

These pages may require access to the associated Notion workspace.

## Scope boundaries

The following are outside the initial MCP-server scope:

- database writes or graph mutation;
- direct language-model access to Neo4j credentials;
- unrestricted shell or file-system access;
- unrestricted graph traversal;
- large-scale public concurrency before the bounded server is validated;
- causal interpretation of returned associations;
- replacement of domain-expert review for novel biomedical analyses.

## License and data access

A project software license has not yet been selected. DDKG data access and redistribution remain subject to the licenses and access requirements of the integrated source resources. No database credentials, licensed source data, protected institutional configuration, protected health information, or controlled-access biomedical data should be committed to this repository.
