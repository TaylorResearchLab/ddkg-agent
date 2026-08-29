# DDKG Agent

A Git-managed, release-specific natural-language query assistant for the Data Distillery Knowledge Graph (DDKG).

DDKG Agent is being developed to allow researchers to ask biomedical questions in natural language and receive transparent, bounded results from the DDKG without requiring them to write Cypher directly. The initial deployment target is a browser-based interface running within the CHOP institutional DMZ by the beginning of 2027.

## Project objective

The first objective is to establish one reproducible, CPU-only path from a natural-language biomedical question to:

1. a typed DDKG query plan;
2. validated and bounded Cypher;
3. read-only execution against the DDKG;
4. transparent results with graph-path, source, and limitation information.

The initial implementation will begin with validated examples, but the system is being designed from the outset to support progressively more capable query generation without replacing the core planning, compilation, validation, execution, or audit interfaces.

## Durable execution path

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

The language model produces a typed plan, not executable database commands. The model has no Neo4j credentials and does not submit Cypher directly. Only the execution broker may connect to Neo4j.

## Capability progression

The project will expand through four capability levels:

1. **Validated examples and parameterized plans**
2. **Composition of validated graph motifs**
3. **Schema-constrained generation of novel typed plans**
4. **Iterative repair based on validation and preview failures**

All levels use the same typed plan, compiler, validator, execution broker, and audit interfaces. Initial query examples are therefore testable starting points rather than the permanent boundary of the system.

## Design principles

- Git is the source of truth for code, schemas, configuration, and tests.
- Notion records sprints, decisions, reviews, handoffs, and formal run evidence.
- The language model is constrained to structured query planning.
- Cypher is compiled and validated deterministically.
- User-provided values are passed as query parameters rather than inserted into query strings.
- Neo4j access is read-only and bounded by path, timeout, row, and response limits.
- Query execution is preceded by static validation and an `EXPLAIN` or preview step.
- The initial implementation is intentionally compact and reproducible.
- The project will not be expanded into a production-scale platform before the core method is demonstrated.
- The project will not rely on undocumented or irreproducible “vibe coding.”

## Deployment model

The planned deployment is:

```text
Browser user
      ↓
CHOP reverse proxy, authentication, and DMZ controls
      ↓
DDKG Agent web application and execution broker
      ├── local CPU-based Ollama service
      └── read-only DDKG Neo4j service
```

Only the browser application is intended to be externally reachable. Ollama, Neo4j Bolt, and Neo4j Browser will remain internal services.

The initial deployment does not require a GPU. A small local model will be benchmarked for structured query planning after the existing CHOP VM is redeployed. The DDKG and Docker are already installed on that VM.

## Repository layout

```text
.
├── deploy/                   # Local and CHOP DMZ deployment configuration
├── docs/                     # Architecture and operating procedures
├── examples/                 # Validated questions, plans, motifs, and expected outputs
├── schemas/                  # Typed query-plan and release-specific schema definitions
├── src/ddkg_agent/           # Application code
├── tests/                    # Unit, regression, integration, and adversarial tests
├── .env.example              # Non-secret environment variable template
└── pyproject.toml            # Python package and test configuration
```

Key documents:

- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md)
- [`docs/OPERATING_MODEL.md`](docs/OPERATING_MODEL.md)
- [`schemas/query_plan.schema.json`](schemas/query_plan.schema.json)
- [`examples/README.md`](examples/README.md)
- [`deploy/README.md`](deploy/README.md)

## Current status

**Stage:** Sprint 0, Foundation and first end-to-end path

Completed:

- repository initialized under `TaylorResearchLab/ddkg-agent`;
- Python source layout created;
- typed query-plan model created;
- JSON Schema v0.1 created;
- initial smoke test added and passing;
- architecture and operating-model documents added;
- environment and deployment placeholders added;
- Git and Notion audit workflow established.

Pending VM redeployment:

- VM and Neo4j inventory;
- DDKG release and build identification;
- read-only Neo4j account and timeout verification;
- internal CPU-only Ollama installation;
- local model benchmark and digest recording;
- first natural-language-to-DDKG end-to-end execution.

The repository does not yet contain a working user interface, general text-to-Cypher generation, or production deployment automation.

## Local development

Python 3.11 or later is required.

```bash
git clone https://github.com/TaylorResearchLab/ddkg-agent.git
cd ddkg-agent
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e '.[dev]'
python -m pytest -q
```

The current smoke test does not require Ollama, Neo4j, DDKG credentials, or network access.

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

## Initial roadmap

- **Sprint 0:** Foundation and first end-to-end path
- **Sprint 1:** Typed query plan and release-specific schema registry
- **Sprint 2:** Deterministic compiler, validator, and execution broker
- **Sprint 3:** Composable and schema-constrained planning
- **Sprint 4:** Browser user interface
- **Sprint 5:** Hardening and evaluation
- **Sprint 6:** CHOP DMZ pilot release

## Scope boundaries

The following are outside the initial project scope:

- unrestricted text-to-Cypher execution;
- direct language-model access to Neo4j credentials;
- autonomous shell, file-system, or web access;
- Kubernetes or multi-cluster orchestration;
- large-scale public concurrency;
- unrestricted graph traversal;
- causal interpretation of returned associations;
- replacement of domain-expert review for novel biomedical analyses.

## License and data access

A project software license has not yet been selected. DDKG data access and redistribution remain subject to the licenses and access requirements of the integrated source resources. No database credentials, licensed source data, or protected institutional configuration should be committed to this repository.
