---
name: ddkg
description: Turn plain-language biological questions into accurate Cypher for the December 2025 Data Distillery Knowledge Graph release (DataDistillery_2025_04_DEC), which uses the August 2025 HAS_CODE schema. Use whenever the user asks to query, traverse, diagnose, or write Cypher against that DDKG release, including Common Fund DCC data such as GTEx, 4DN, LINCS, IDG, GlyGen, Kids First, ERCC/exRNA, HuBMAP, MoTrPAC, SPARC, or Metabolomics Workbench. Also use it to resolve DDKG entities, explain empty results, inspect release-specific schema or source coverage, or help a user install a compatible local build. Reach for this even when the user says neither "knowledge graph" nor "Cypher" if the question concerns relationships among genes, diseases, tissues, compounds, or genomic features in the December 2025 DDKG release.
---

# DDKG query assistant

Turns biological questions into Cypher for the **December 2025 DDKG CSV
release (`DataDistillery_2025_04_DEC`)**, which uses the August 2025
`HAS_CODE` schema, and helps users get a compatible build running if needed.

**This skill never connects to the graph.** The user's DDKG runs on their own
machine or their institution's server, often behind an organisational
firewall, and such an instance should not be opened to an outbound connection
for convenience. Everything produced here is text they paste into Neo4j
Browser, `cypher-shell`, a driver, or the REST API.

That is the expected mode, not a limitation to work around. Correctness comes
from knowing the schema, and from handing the user a query plus the means to
tell whether it went wrong — never from asserting what the graph contains.

## Which release and schema this skill targets

This skill targets the **December 2025 CSV release
(`DataDistillery_2025_04_DEC`)**. That release uses the August 2025 schema,
whose Concept-to-Code edge is `HAS_CODE`.

A schema discriminator and a release identifier answer different questions:

| Build | Status for this skill |
| --- | --- |
| December 2025 CSV release, `DataDistillery_2025_04_DEC` | **Target release** — validated counts, source inventories, modelling idioms, and query patterns |
| Another build using `HAS_CODE`, `HAS_TERM`, `HAS_SEMANTIC`, `HAS_DEFINITION` | Same structural schema family; profile it before trusting release-specific counts, sources, predicates, or endpoint assumptions |
| Old build using `CODE`, `PREF_TERM`, `STY`, `DEF` | Out of scope; generated queries return zero silently |
| JKG generation | Out of scope; the Code-node topology changes |

When the release is uncertain, ask for its identifier if available and run the
structural discriminator:

```cypher
CALL db.relationshipTypes() YIELD relationshipType
WHERE relationshipType IN ['CODE','HAS_CODE']
RETURN collect(relationshipType) AS concept_code_edge
```

`HAS_CODE` establishes structural compatibility, **not** identity with the
December 2025 release. `CODE` establishes an old-schema build, which is out of
scope. Say so plainly rather than translating queries and pretending the
release-specific registries still apply.

## Read the source, not your recollection

Document-derived facts in `references/` trace to the primary copies in
`sources/`. Release-specific counts, endpoint inventories, and query behaviour
trace instead to live enumerations and executed validation recorded in
`assets/` and references 13, 16, 17, and 18. The precedence when they disagree is
in `01_sources_and_precedence.md`. The critical case: UBKG documentation names
the structural edges `CODE`,
`PREF_TERM`, `STY`, `DEF`. **This build uses `HAS_CODE`, `HAS_TERM`,
`HAS_SEMANTIC`, `HAS_DEFINITION`.** The documented names return zero rows
with no error.

Where the guide is silent, say so rather than inferring.

## Why the obvious query fails

Every biomedical entity is a `Concept`. There is no `:Gene`, no `:Disease`,
no `:Tissue`. What a Concept *is* comes from the `Code` nodes attached to
it; what an edge *means* comes from the `SAB` on the relationship. So:

```cypher
MATCH (g:Gene)-[:expressed_in]->(t:Tissue) RETURN g, t
```

returns nothing — and nothing looks exactly like a biological negative, so
the failure is silent and the pull toward explaining it from background
biology is strong. Do not.

For GTEx expression on the target release, the release-specific shape is a
measurement Concept with separate gene, tissue, and value legs:

```cypher
MATCH (gene:Concept)-[:HAS_CODE]->(:Code {CodeID:'HGNC:10848'})
MATCH (gene)-[:expressed_in {SAB:'GTEXEXP'}]-(measurement:Concept)
MATCH (measurement)-[:expressed_in {SAB:'GTEXEXP'}]-(tissue:Concept)
MATCH (tissue)-[:HAS_CODE]->(tc:Code {SAB:'UBERON'})
OPTIONAL MATCH (measurement)-[:has_expression {SAB:'GTEXEXP'}]-
               (bin_concept:Concept)-[:HAS_CODE]->(bin:Code {SAB:'EXPBINS'})
RETURN gene.CUI, tc.CodeID, bin.CodeID AS expression_bin
LIMIT 25
```

Pin the far endpoints by Code SAB. The predicate name and arrow direction do
not distinguish the gene leg from the tissue leg in this source.

## Before opening any reference: route

This skill has eighteen references, eight source documents, and ten assets —
far more than fits in context. Choosing what to read by filename is how the
gene-symbol lookup sat unread in the query examples while the same problem was
solved from scratch.

`assets/skill_graph.tsv` is a relationship index over this skill's own
sections. A keyword index says where something is documented; this also says
**what you will be wrong without**, which is the question nobody thinks to
ask.

```bash
python scripts/route.py "expression"       # what to read, and its prerequisites
python scripts/route.py --list             # entry points
python scripts/route.py --stale "JKG generation"   # what a change invalidates
```

The prerequisites matter more than the answers. Every silent failure recorded
in this skill was a missing one:

| Doing this | Without this, you are wrong |
| --- | --- |
| GTEx expression | half of all gene-tissue pairs are exact zero; `EXPBINS` carries no numeric properties; adult tissue censors developmental genes |
| Pathway queries | a SAB is a source not a kind of thing; Reactome mixes human and mouse |
| Resolving a name | `CODE` formatting varies by source; the name may be a mouse vocabulary |
| Any intersection | cost on an unindexed build; errors amplify across hops |
| Ranking by source | a CLINGEN hit can be `Disputed` — negative, not support |
| An empty result | old edge names return nothing silently; profile the anchor first |
| A string filter | false friends — `cardiac` catches the gastroesophageal junction |

If `route.py` cannot run, grep the graph directly: entries are
`subject <TAB> edge <TAB> object <TAB> note`, and `must_read_with` is the edge
that carries the warnings.

## Maintaining this skill

Everything here came from running a query, finding a defect, and writing it
down. That loop is the skill's only growth mechanism, so it needs to keep
running.

### When a query fails or misleads

Sort the failure before fixing it — the categories need different work:

| Failure | Fix |
| --- | --- |
| A reference states something false | Correct the file. Check the source in `sources/` before rewriting. |
| The fact was here but not consulted | Content is fine; add a `must_read_with` edge to `assets/skill_graph.tsv`. |
| The fact is absent | New content, and check whether a source already documents it. |
| Correct but unhelpful | Framing, not accuracy. |

The second row has been the most common by a wide margin. Before adding
content, check whether the fact already exists somewhere and simply was not
reached.

### Adding to the graph

Add an edge whenever a failure would have been prevented by reading something
alongside something else:

```
topic	must_read_with	11_interpreting_results.md#section-anchor	one line on what goes wrong
```

Anchors are GitHub-style slugs of the heading. Then always:

```bash
python scripts/route.py --check
```

A broken link is worse than no link. Run it after any heading rename too — the
graph points at anchors and does not follow them.

Use `invalidated_by` when a claim depends on something that will change, so
`--stale` can find it later.

### Recording an observed result

Observed results are illustrations, never answers. Attach the disclaimer in
the same breath as the value, not in a general policy elsewhere — a gene list,
a source list, a classification, or a count reads as a lookup table unless it
says otherwise. See `11_interpreting_results.md` for the wording that has held
up.

An example may show **shape**. It must not supply **values** a user would
otherwise obtain from their own run.

### Verifying rather than asserting

Four times in this skill's history the answer was already in a document in
`sources/` and was not read: `ACR` for gene symbols, LINCS coverage, the
curated triple tables, the non-human SABs. Before writing that something is
undocumented, grep `sources/`.

Claims about the graph need a query behind them. Claims about the documents
need a quotation. Neither should come from recall.

### When the schema changes

`01_sources_and_precedence.md` records which files are schema-dependent and
which port. `route.py --stale "JKG generation"` returns the sections that a
topology change invalidates. Start there rather than re-deriving.

## Workflow

### 1. Look for a target-release validation first

Open `references/16_manuscript_validated_queries.md` first. Its eleven indexed
query patterns were validated against the December 2025 target release and
encode the current staging, cap, direction, and walk-back rules.

Then consult `references/09_query_task_index.md` for the 51 User Guide
examples. Those examples are valuable historical patterns and were known to
run on the guide's build, but they were not all revalidated on the December
2025 release; several legacy forms failed or hung during the later validation
campaign. In particular, retain Query 24's `ACR` gene-symbol anchor but do not
reuse its `GTEXEXP` CodeID parsing. Prefer the current release-specific
patterns whenever the two disagree.

**Do this silently.** The user does not know a query index exists and has no
use for the fact that one was consulted. Never open with "no validated query
covers this" — it is bookkeeping, and it reads as pre-excusing a failure.

Where the absence carries real information, express it as confidence in the
*answer* rather than as a note about the files. "This join isn't one I can
check against a known-good example, so confirm the bin resolutions match
before trusting the result" tells the user something actionable. "There is no
validated query for this" tells them about a filing system.

The same applies to the rest of the workflow: consult the registries, the
endpoint map, and the interpretation guidance without narrating that you did.

**Watch the vocabulary too.** Words this skill uses internally do not mean
anything to the person asking:

| Internal | Say instead |
| --- | --- |
| "in this build" | nothing — just state it: "Metabolomics Workbench asserts…" |
| "the December 2025 release" or "the August 2025 schema" | nothing, unless release compatibility is materially at issue |
| "the registries", "the endpoint map" | nothing |
| "no validated query for this" | nothing, or express it as confidence in the answer |
| "SAB" | "source", on first use at least |

"In this build" is the most tempting and the least useful. It raises a
question the user cannot answer — *which* build? — and implies another might
say otherwise, without giving them any way to check. Reserve it for the case
where builds genuinely differ, such as warning that an older schema returns
nothing.

### 2. Resolve the entity, and disambiguate with the user

`references/05_entity_resolution.md`. Leave the term edge unbound and return
`type(tr)` while resolving; there is no default that works across sources.
Once the source is known, bind its verified term edge — `ACR` for HGNC
symbols, per `04_identifier_conventions.md`. Anchor on
`CodeID`, not `CODE` — see `04_identifier_conventions.md`.

Ambiguous abbreviations go back to the user. "ASD" is atrial septal defect
and autism spectrum disorder, and choosing silently produces a fluent answer
to a question nobody asked.

**Ask about the question, never about the sources.** The user knows what they
are asking; they do not know how NIH organises its data, and that asymmetry
is why this skill exists.

Legitimate to ask:

- Which entity a name refers to, when genuinely ambiguous.
- Which *question* they mean, when routes give different answers — "genes
  directly associated with this phenotype, or genes causing syndromes that
  feature it?" Those return different gene sets and the difference is
  biological.
- Where they will run the query, once per session.

Not legitimate to ask:

- "Which sources would you like — OMIM, HPO, ClinVar?" This is a SAB
  allowlist with the choosing handed to someone with less information. Run it
  unfiltered, return `collect(DISTINCT r.SAB)`, and let the graph report which
  sources participate. Then explain what each one's evidence means.
- Which predicate to use. Look it up.
- Whether they want the fast or slow version. Give the fast one.

A clarifying question should narrow *intent*. If it narrows *implementation*,
answer it yourself.

### 3. Profile the anchor

One query returning every predicate and source touching the anchor. It
decides whether the question is answerable for *this* entity, which no
registry can tell you: a gene may have edges from a dozen sources and none
from the one the question needs.

Hand the query over and let the user run it. Do not state what the profile
will show.

### 4. Compose

`08_dcc_endpoints.md` for what connects which identifier spaces,
`07_predicate_registry.md` for predicates and their properties,
`06_sab_registry.md` for source names and which are edge-only.

If nothing connects the two spaces directly, chain through an intermediate
rather than inventing a predicate. A predicate can be one hop from the
anchor and two from the answer — see the OMIM example in
`05_entity_resolution.md`.

### 5. Apply the fixed rules

Ten that decide whether a query returns the right rows. Everything else is
routed: `route.py <topic>` returns the rules bearing on this question, and
`references/15_query_rules.md` holds the full set.

- **`HAS_CODE`, `HAS_TERM`, `HAS_SEMANTIC`, `HAS_DEFINITION`.** The documented
  names `CODE`, `PREF_TERM`, `STY`, `DEF` match nothing.
- **Anchor on `CodeID`.** `CODE` formatting varies by source.
- **Match assertions undirected**, `-[r]-`. Structural edges point outward
  from the Concept. A wrong arrow returns zero silently.
- **Unbound undirected matches double** — assertions are stored as inverse
  pairs. Bind the predicate or `collect(DISTINCT ...)`.
- **Decide the result grain before writing the query.** Every variable bound in
  `MATCH` contributes to row multiplicity, even when it is absent from
  `RETURN`. Use `WHERE EXISTS { }` for filter-only constraints, bind one
  source-specific label edge, and return or visibly aggregate informative
  hidden variables; use `RETURN DISTINCT` only as the final backstop.
- **A query spanning groups must aggregate**, not sort differently. If the
  `ORDER BY` column has fewer distinct values than the `LIMIT`, the query is
  wrong.
- **Labels are decoration.** Reach `Term` with `OPTIONAL MATCH` and
  `coalesce(t.name, c.CodeID)`. A required term edge kills a valid chain.
- **Never filter on an optional property without allowing null** —
  `evidence_class`, and the numeric properties on `Code`.
- **Constrain with the endpoint, not a SAB allowlist.** Put the SAB in
  `RETURN` and let the graph report which sources participate.
- **`LIMIT` on everything**, and aggregate before expanding to `Term`.

### 6. Hand it over

`references/14_handing_over_queries.md`. In short: runnable exactly as pasted,
no placeholders, values inlined. Do not predict what the query will return —
not its values, not its shape. Give a falsification criterion instead. Where a
chain needs a decision in the middle, hand over one step, take the result
back, and write the next with the chosen values inlined.

### 7. Interpret it

`references/11_interpreting_results.md`, and this is the part that matters
most. Users know the biology and do not know how NIH organises its data, so
the caveats are part of the answer rather than appended to it.

`route.py <topic>` returns the ones bearing on the question. The recurring
shape: **name the evidence type, not just the source**; **check source
independence before ranking on agreement**; **say what is absent and why**;
**say when a result is truncated**.

## Files

| Path | Purpose |
| --- | --- |
| `references/01_sources_and_precedence.md` | Which document wins when they disagree |
| `references/02_data_model.md` | UBKG model: concepts, synonymy, inverses, business rules |
| `references/03_schema_this_build.md` | **Actual edge names, properties, direction, scale** |
| `references/04_identifier_conventions.md` | CodeID vs CODE, term edges, MTHU, verified anchors |
| `references/05_entity_resolution.md` | Resolve, profile the anchor, two-hop routes |
| `references/06_sab_registry.md` | 289 node SABs, 143 edge SABs, which are edge-only |
| `references/07_predicate_registry.md` | 2,101 predicates, inverse pairs, structural edges |
| `references/08_dcc_endpoints.md` | What each DCC source connects, from 25,682 triples |
| `references/09_query_task_index.md` | **Look here first** — 51 validated queries by task |
| `references/10_query_examples.md` | The queries themselves |
| `references/11_interpreting_results.md` | What a result means and does not mean |
| `references/17_gtex_bins_addendum.md` | EXPBINS and PVALUEBINS structure, occupancy, the `0.1e-12` landmine |
| `references/18_row_multiplicity_and_identity_sinks.md` | Result grain, label fan-out, identity sinks, inverse storage, and runtime probes |
| `references/16_manuscript_validated_queries.md` | **Most recently validated Cypher** — staging, caps, cross-species bridges |
| `references/14_handing_over_queries.md` | Runnable output, no prediction, falsification, staged queries |
| `references/15_query_rules.md` | Rules beyond the ten in step 5 |
| `references/13_empirical_findings_aug2025_validation.md` | **Validation campaign** — query doctrine, verified anchors, nine failure classes |
| `references/12_setup_and_access.md` | Licensing, deployment, REST API, row caps |
| `assets/skill_graph.tsv` | **Relationship index** — what to read, and what you are wrong without |
| `scripts/route.py` | Traverses it: `route.py "expression"`, `--list`, `--stale` |
| `sources/` | The primary documents, for checking rather than trusting |
| `assets/` | Machine-readable registries — grep before saying something does not exist |

## Provenance of the registries

The registries in `references/` were enumerated from a live **December 2025
CSV release (`DataDistillery_2025_04_DEC`)**, Neo4j 5.26.28 Community, which
is on the August 2025 schema. Validated queries come from the DDKG User Guide
and from the manuscript's Supplementary Note S7, both consistent with that
schema.

Counts, source inventories, predicates, endpoint coverage, and some
source-specific modelling details are release-specific and can drift. The
structural edge names stated here were validated for the December 2025 target
release; another `HAS_CODE` build must still be profiled before its results are
interpreted with these registries.
