# DDKG Agent

A Git-managed, release-specific natural-language query assistant for the Data Distillery Knowledge Graph (DDKG).

## Initial objective

Prove one reproducible, CPU-only path from a natural-language biomedical question to:

1. a typed query plan,
2. validated and bounded Cypher,
3. read-only execution against the DDKG,
4. transparent results with source and path information.

The architecture is deliberately designed to expand from validated examples to composable motifs and schema-constrained query generation without replacing the core plan, compiler, validation, or audit interfaces.

## Working principles

- Git is the source of truth for code, schemas, configuration, and tests.
- Notion records sprints, decisions, reviews, and formal run evidence.
- The language model produces a typed plan, not executable database commands.
- Cypher is compiled and validated deterministically.
- Neo4j access is read-only and bounded by timeout and result limits.
- Initial delivery is intentionally compact and reproducible, not a production-scale platform.

## Repository layout

- `src/ddkg_agent/`: application code
- `schemas/`: typed query-plan and release-specific schema definitions
- `examples/`: validated questions, plans, motifs, and expected outputs
- `tests/`: unit, regression, integration, and adversarial tests
- `deploy/`: local and CHOP DMZ deployment configuration
- `docs/`: architecture, scope, and operating procedures

## Current status

Foundation scaffold only. VM inventory, DDKG release details, Ollama model selection, and Neo4j connection settings will be added after the existing VM is redeployed.
