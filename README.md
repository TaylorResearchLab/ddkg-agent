# DDKG Agents

This repository contains two related but independently deliverable projects for the Data Distillery Knowledge Graph (DDKG).

## Objective 1: DDKG Cypher Query Skill

`objective-1-skill/` contains a portable Agent Skill that generates accurate, runnable Cypher on demand from a User's biological question for the **December 2025 DDKG release** (`DataDistillery_2025_04_DEC`).

The skill does not connect to or execute against the graph. It produces Cypher and validation guidance for the User to run against a local or institutional DDKG instance. The exact incoming `.skill` archive, canonical model-neutral source, deterministic draft package, validation tools, and review records are versioned together.

## Objective 2: Locally hosted DDKG query assistant

`objective-2-agent/` contains the application scaffold for a reproducible browser interface, typed query planning, deterministic Cypher compilation, validation, bounded read-only Neo4j execution, and result presentation in the CHOP DMZ.

Objective 2 may later reuse selected Objective 1 artifacts through an explicit, pinned interface. It is not assumed to be a wrapper around the current skill.

## Related methods project

The general embedded-epistemic-graph method is developed separately in [`TaylorResearchLab/edges-scientific-ai`](https://github.com/TaylorResearchLab/edges-scientific-ai). DDKG remains an application profile and test bed; the DDKG-specific skill stays in this repository.

## Repository layout

```text
objective-1-skill/   Portable DDKG Cypher Query Skill and its tests
objective-2-agent/   Local application, compiler, validator, and deployment scaffold
```

Git is the source of truth for code, schemas, skill packages, tests, configuration, and release artifacts. Notion records scope, decisions, reviews, handoffs, and formal run evidence.

No database credentials, licensed source data, protected institutional configuration, protected health information, or controlled-access biomedical data may be committed.
