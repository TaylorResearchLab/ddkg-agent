# Architecture

## Durable execution path

Natural-language question → typed query plan → deterministic compiler → static validation →
Neo4j `EXPLAIN` → bounded preview → bounded read-only execution → transparent result package.

## Capability progression

1. Validated examples and parameterized plans
2. Composition of validated graph motifs
3. Schema-constrained generation of novel typed plans
4. Iterative repair based on validation and preview failures

All levels use the same typed plan, compiler, validator, execution broker, and audit interfaces.

## Trust boundary

The model has no Neo4j credentials and does not submit Cypher. Only the execution broker may
connect to Neo4j. User text is represented as data and passed through parameterized queries.
