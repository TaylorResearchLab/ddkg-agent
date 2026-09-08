# Sources and precedence

This skill combines primary documentation with release-specific empirical
evidence. Document claims should trace to the copies in `sources/`; claims
about the December 2025 graph should trace to live enumerations, executed
queries, or explicit unresolved discrepancies in `assets/` and references
13, 16, and 17.

References 13, 16, and 17 are compact evidence summaries. The raw terminal
outputs and manuscript Supplementary Note S7 are not bundled in this package.
Where a result is consequential or marked unresolved, reproduce it against the
target release rather than treating the summary as a substitute for the run.

## Precedence

When two sources disagree, the higher one wins:

| Rank | Source | Authoritative for |
| --- | --- | --- |
| 1 | Executed validation and live enumerations for `DataDistillery_2025_04_DEC` (`assets/`; references 13, 16, 17) | What exists and what runs on the target release; release-specific counts, endpoints, properties, and failure modes |
| 2 | `sources/ddkg_user_guide.md` | Intended schema and worked query patterns; examples are not automatically current-release gold queries |
| 3 | `sources/ubkg_data_model.md` and the other UBKG docs | The model and its semantics: why the graph is shaped this way |
| 4 | `assets/data_dictionary_triples.json` | Curated per-DCC triples and methodology from the earlier August 2025 data dictionary |
| 5 | Published papers (Petagraph, DDKG preprint) | Background and intent |

**The critical case.** UBKG documentation describes the structural edges as
`CODE`, `PREF_TERM`, `DEF`, and `STY`. The August 2025 schema renamed them to
`HAS_CODE`, `HAS_TERM`, `HAS_SEMANTIC`, and `HAS_DEFINITION`. The docs are
authoritative on *what these edges mean* and stale on *what they are called*.
Using the documented names returns zero rows with no error.

The data dictionary is August 2025 — the same schema, an earlier build. Its
methodology notes remain valuable; its counts are historical.

**Dates do not identify the schema.** CSV builds up to July 2025 are
old-schema; Docker builds from July 2025 onward are August 2025 schema. The
discriminator is whether the Concept-to-Code edge is `HAS_CODE` or `CODE`.

## What each source covers

**`ddkg_user_guide.md`** — 51 worked queries, Tips and Tricks performance
guidance, and the renamed structural edges. The examples were known to run on
the guide's build, but they are retained as historical patterns rather than
being treated as current-release gold queries. References 13 and 16 record the
newer December 2025 validation campaign.

**`ubkg_data_model.md`** — concepts and synonymy, the concept subgraph, the
assertion model, inverse derivation via the Relations Ontology, the `PT_SAB`
rule, preferred-concept resolution, and the permitted property set.

**`ubkg_ingest_formats.md`** — how data enters the graph: edges.tsv and
nodes.tsv, node and edge SABs, cross-references versus `isa`, and the
CodeID formatting rules that explain why `CODE` is inconsistent.

**`ubkg_glossary.md`** — terminology, including the inverse-relationship
discussion.

**`ubkg_api.md`** — REST endpoints, including introspection endpoints that
answer schema questions without Cypher. See `12_setup_and_access.md`.

**`ubkg_contexts.md`** — every SAB in each context with licensing and
citation. The reference for "what is this source and may I redistribute it".

**`ubkg_versioning.md`** — how SAB versions are assigned, and the
`UBKGSOURCE` in-graph ontology.

**`ubkg_downloads.md`** — obtaining and deploying a build.

## Schema generations

Three, and this skill covers the middle one.

| Generation | Concept-to-Code | Status |
| --- | --- | --- |
| Old CSV | `CODE`, `PREF_TERM`, `STY`, `DEF` | CSV builds up to July 2025. Out of scope. |
| **August 2025 schema family** | `HAS_CODE`, `HAS_TERM`, `HAS_SEMANTIC`, `HAS_DEFINITION` | Structural family used by the **December 2025 target release**; other builds still require profiling. |
| JKG | Code folded into an edge: `Concept -[code]-> Term` | Separate generation under development; out of scope. |

The JKG generation also corrects known version skew: bin Codes such as
`EXPBINS` were ingested before the `lowerbound`/`upperbound` properties
existed, so numeric values that the model permits are absent from the data.

It removes the `Code` node entirely, carrying the source,
term type, and identifier as edge properties instead. That is a topology
change rather than a rename: `(c:Code {CodeID:...})` — the anchor every query
here begins with — will not exist. It warrants a separate skill, not a
compatibility layer.

## What ports across generations

Worth knowing before that migration, because it is most of the content:

**Schema-independent** — facts about the data, valid whatever the topology:

- `02_data_model.md` — concepts, synonymy, assertions, RO-derived inverses
- `06_sab_registry.md` — which sources exist and what they are
- `08_dcc_endpoints.md` — which sources connect which identifier spaces
- `11_interpreting_results.md` — evidence semantics, coverage, absence
- `12_setup_and_access.md` — licensing, deployment, versioning

**Schema-dependent** — rewritten whenever the topology changes:

- `03_schema_this_build.md` — edge names, direction, properties
- `04_identifier_conventions.md` — mixed: identifier *values* such as
  `MONDO:0006664` survive; the `(c:Code {CodeID:...})` access path does not
- `05_entity_resolution.md` — every recipe
- `07_predicate_registry.md` — mixed: predicates survive, structural edges do not
- `09_query_task_index.md`, `10_query_examples.md` — every query

The generated `assets/` are all schema-dependent in access path and
schema-independent in content: the SAB and predicate inventories remain true
facts about the sources, but the Cypher used to reproduce them will not run.

## Assets

Generated, with their provenance:

| File | From |
| --- | --- |
| `node_sabs.csv` | December 2025 build, `MATCH (c:Code) RETURN c.SAB, count(*)` |
| `edge_sabs.csv` | December 2025 build, derived from `predicates.csv` |
| `predicates.csv` | December 2025 build, `MATCH ()-[r]->() RETURN type(r), r.SAB, count(*)` |
| `sab_triples_dcc.csv` | December 2025 build, DCC-scoped subject/predicate/edge-SAB/object |
| `dcc_endpoints.json` | grouped form of the above |
| `inverse_pairs.json` | derived from `predicates.csv` by morphology and count-tie |
| `evidence_class_predicates.json` | December 2025 build, `db.schema.relTypeProperties()` |
| `data_dictionary_triples.json` | curated tables in the August 2025 data dictionary |
| `ubkg_sabs_sample_codes.csv` | UBKG docs: SAB list with example code formats |

## Rule

Read the source before asserting. Counting entries in a file is not reading
it, and a derived table is evidence about the graph, not a substitute for
the document that explains it.
