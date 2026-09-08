# DDKG MCP Server

A release-aware **Model Context Protocol (MCP)** server for controlled access to the NIH Common Fund Data Ecosystem **Data Distillery Knowledge Graph (DDKG)**.

This project is intended to allow MCP-compatible AI clients to interact with a live DDKG instance through a constrained server interface. The MCP server, not the language model, owns the database connection and enforcement of query limits. The DDKG Neo4j instance remains the source of truth for returned graph results.

## Status

This directory is an **early development scaffold**, not a public production MCP service.

The initial target is the forthcoming **JKG-era 2026 DDKG release**, which is not yet released as of September 2026. The server is intentionally release-aware because the JKG representation changes important aspects of the DDKG schema and future releases will require explicit compatibility updates.

The currently published [`ddkg-agent-skill`](../ddkg-agent-skill/) targets the December 2025 DDKG release. The skill and MCP server are complementary projects, but they should not be assumed to be cross-release compatible until that compatibility is explicitly tested.

## Project objective

The first objective is to establish one reproducible path from an MCP client request to:

1. release and schema identification;
2. a typed DDKG query request or plan;
3. deterministic validation and bounded Cypher construction or acceptance;
4. read-only execution against the DDKG;
5. transparent results with graph-path, source, provenance, and limitation information.

The server will expose a small, auditable set of DDKG capabilities through MCP tools and resources rather than unrestricted database access.

## Planned architecture

```text
MCP-compatible AI client
(ChatGPT, Claude, Codex, or another MCP client)
                ↓
         DDKG MCP Server
                ↓
      release/schema checks
      typed request validation
      deterministic compilation
      static validation
      Neo4j EXPLAIN / preview
      bounded read-only execution
                ↓
           DDKG Neo4j
                ↓
 results + sources + provenance + limitations
```

The durable execution path is described in [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md):

```text
natural-language question
→ typed query plan
→ deterministic compiler
→ static validation
→ Neo4j EXPLAIN
→ bounded preview
→ bounded read-only execution
→ transparent result package
```

## Trust boundary

The design keeps Neo4j credentials outside the language model.

The model should not directly own the database connection or submit arbitrary Cypher to Neo4j. Only the controlled execution layer may connect to the graph. User text is treated as data and should pass through typed plans, validation, parameterized queries, limits, and execution policy before reaching Neo4j.

This separation is central to the project. The goal is not merely to make DDKG queryable through MCP, but to make graph access **bounded, auditable, release-aware, and reproducible**.

## Planned capabilities

Candidate MCP capabilities include:

- report the active DDKG release and schema generation;
- inspect available DDKG source abbreviations and source metadata;
- resolve identifiers and labels to graph entities;
- search concepts or codes;
- inspect relationships and predicates available for a resolved entity;
- validate a proposed DDKG query plan;
- execute approved, bounded, read-only queries; and
- return graph-path, source, provenance, and limitation information with results.

Initial work is intentionally focused on a small set of typed capabilities rather than unrestricted Cypher execution.

## Relationship to the DDKG Agent Skill

The two projects in this repository serve different layers:

- the **DDKG Agent Skill** supplies release-specific DDKG semantics, identifier conventions, query guidance, and biological caveats;
- the **DDKG MCP Server** supplies controlled access to a live DDKG instance and returns results derived from actual graph execution.

A future MCP-compatible client may use both together, but the present public skill and server development target different DDKG release generations.

A browser or website could later be built as one client of the MCP server. The primary deliverable in this directory is the MCP server itself.

## Release compatibility

The first MCP implementation is being developed for the JKG-era DDKG release.

Relevant specifications:

- [JSON Knowledge Graph repository](https://github.com/x-atlas-consortia/json-knowledge-graph/tree/main)
- [JKG specification / RFC](https://docs.google.com/document/d/1lQF0e8C134gmLB5aHsqYqPYWpC7n__PYMTiRayZ4Bbw)

Do not assume that Cypher patterns or schema conventions from the December 2025 DDKG release remain valid for the JKG-era release without an explicit compatibility layer.

## Development setup

The current package requires **Python 3.11 or newer**. Its development dependencies are defined in [`pyproject.toml`](pyproject.toml).

From this directory:

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
pytest
```

This installs and tests the current scaffold. It does **not** imply that a complete production MCP service is available yet.

## Repository layout

```text
ddkg-mcp-server/
├── README.md
├── .env.example
├── pyproject.toml
├── deploy/
├── docs/
│   ├── ARCHITECTURE.md
│   └── OPERATING_MODEL.md
├── examples/
├── schemas/
├── src/
└── tests/
```

The design documentation under `docs/` should remain the durable source for architecture and operating-model details as the implementation grows.

## Security and operating constraints

The intended production model is:

- read-only graph access;
- bounded requests and result sizes;
- explicit release/schema checks;
- parameterized handling of user-provided text;
- deterministic validation before execution;
- transparent provenance and limitations in returned results; and
- no model-held Neo4j credentials.

These are design requirements, not a claim that every control is already implemented in the current scaffold.

## License and data access

A project software license has not yet been selected.

DDKG data access and redistribution remain subject to the licenses and access requirements of the integrated source resources. Do not commit database credentials, licensed source data, protected institutional configuration, protected health information, or controlled-access biomedical data to this repository.

For shared DDKG installation links, project resources, and contact information, see the repository-level [README](../README.md).
