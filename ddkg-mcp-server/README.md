# DDKG MCP Server

A release-aware Model Context Protocol (MCP) server for controlled access to the Data Distillery Knowledge Graph (DDKG).

This project is intended to allow MCP-compatible AI clients to interact with a live DDKG instance through a constrained server interface. The MCP server, not the language model, owns the database connection and enforcement of query limits. The DDKG Neo4j instance remains the source of truth for returned graph results.

The initial target is a server that works with the **JKG 2026 DDKG release** (not released yet, Sept 2026). The server must remain explicitly release-aware because future DDKG releases will use a different schema and will require corresponding compatibility updates. 

## Project objective

The first objective is to establish one reproducible path from an MCP client request to:

1. release and schema identification;
2. a typed DDKG query request or plan;
3. deterministic validation and bounded Cypher construction or acceptance;
4. read-only execution against the DDKG;
5. transparent results with graph-path, source, provenance, and limitation information.

The server will expose a small, auditable set of DDKG capabilities through MCP tools and resources.

## Planned architecture

```text
MCP-compatible client
(ChatGPT, Claude, Codex, or another MCP client)
                ↓
         DDKG MCP Server
                ↓
      release/schema checks
      request validation
      query evaluation/cleanup 
      Neo4j EXPLAIN/preview
      bounded read-only execution
                ↓
           DDKG Neo4j
                ↓
 results + sources + provenance + limitations
```

### Capabilities

The MCP server's controlled execution layer will connect to Neo4j and will provide:

- controlled access to an actual DDKG instance;
- release and schema inspection;
- identifier and concept resolution against the graph;
- bounded read-only query execution;
- graph-derived results rather than predicted results;
- source, provenance, and limitation information suitable for downstream interpretation.

An MCP client may eventually use both components together: the skill for DDKG-specific reasoning and the MCP server for live graph access. Initial work will focus on a small set of typed capabilities rather than unrestricted Cypher execution. Candidate capabilities include:

- report the DDKG release and schema generation;
- inspect available DDKG source abbreviations and source metadata;
- resolve identifiers and labels to graph entities;
- search concepts or codes;
- inspect relationships and predicates available for a resolved entity;
- validate a proposed DDKG query plan;
- execute approved, bounded, read-only queries;
- return query provenance, source information, and limitations with results.

## Release compatibility

The initial implementation is being developed for DDKG using DDKG-JKG 2026
See the [JKG Specification](https://docs.google.com/document/d/1lQF0e8C134gmLB5aHsqYqPYWpC7n__PYMTiRayZ4Bbw) and the [JKG github repo](https://github.com/x-atlas-consortia/json-knowledge-graph/tree/main)

## License and data access

A project software license has not yet been selected. DDKG data access and redistribution remain subject to the licenses and access requirements of the integrated source resources. No database credentials, licensed source data, protected institutional configuration, protected health information, or controlled-access biomedical data should be committed to this repository.
