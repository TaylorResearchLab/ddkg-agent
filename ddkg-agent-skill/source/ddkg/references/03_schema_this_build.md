# December 2025 release on the August 2025 schema

What the graph actually contains. Enumerated from a live December 2025
build, cross-checked against the DDKG User Guide. Where this disagrees with
the UBKG model documentation, **this file wins** — the model doc predates the
rename.

## Identifying the schema

The discriminator is the Concept-to-Code edge, not the build date:

- `HAS_CODE` → compatible structural schema family; the December 2025 release
  remains the validated target.
- `CODE` → old schema, out of scope; everything here returns zero rows.

CSV builds up to July 2025 are old-schema; Docker builds from July 2025
onward are not. Ask for the query, not the date.

## Scale

Measured on the December 2025 CSV release (`DataDistillery_2025_04_DEC`),
Neo4j 5.26.28 Community. Counts, sources, predicates, endpoint coverage, and
source-specific modelling may drift across releases even when the structural
edge family remains `HAS_CODE`.

Note that a CSV release is not necessarily old-schema: the July 2025 cutover
applies to CSV builds up to that date, and this December 2025 CSV release is
on `HAS_CODE`.

| | Count |
| --- | --- |
| Code nodes | 20,644,187 |
| Concepts (with at least one Code) | 19,437,089 |
| Relationships | 186,651,416 |
| Node SABs | 289 |
| Edge SABs | 143 |
| Relationship types | 2,101 |

Larger than the 32M nodes / 118M relationships in the Petagraph paper, which
describes an earlier build. Cite the enumerated figures, not the published
ones, and say which build they came from.

## Structural edges — the current names

| Edge | Connects | Count | Documented as |
| --- | --- | --- | --- |
| `HAS_CODE` | `Concept` → `Code` | 21,279,506 | `CODE` |
| `HAS_TERM` | `Code` → `Term` | 11,114,862 | term-type edges |
| `HAS_SEMANTIC` | `Concept` → `Semantic` | 3,825,077 | `STY` |
| `HAS_DEFINITION` | → `Definition` | 688,689 | `DEF` |

**`CODE`, `PREF_TERM`, `STY`, and `DEF` do not exist in the August 2025
schema.** A query
using them returns zero rows and no error, which is indistinguishable from a
biological negative.

## Direction

Two rules, and confusing them returns nothing.

**Structural edges point outward from the Concept:**

```cypher
(concept:Concept)-[:HAS_CODE]->(code:Code)-[:PT]->(term:Term)   // correct
(code:Code)-[:HAS_CODE]->(concept:Concept)                       // nothing
(code:Code)<-[:HAS_CODE]-(concept:Concept)                       // correct
```

Matching them undirected is safe and is what the User Guide does throughout.

**Concept-to-Concept assertions are bidirectional** and should be matched
undirected:

```cypher
(a:Concept)-[r {SAB:'GTEXEXP'}]-(b:Concept)
```

Because they are stored as inverse pairs, an *unbound* undirected match
returns every assertion twice. Bind the predicate, aggregate with
`collect(DISTINCT ...)`, or consult `assets/inverse_pairs.json`.

## Term edges

`HAS_TERM` is the general lexical edge at 11.1M. Alongside it sit ~40 typed
variants, and **which one applies depends on the source**:

| SAB | Edge | Carries |
| --- | --- | --- |
| `HGNC` | `ACR` | gene symbol — `SHH` |
| `HGNC` | `PT` | descriptive name — "sonic hedgehog signaling molecule" |
| `HP` | `PT`, `PT_HPOMP` | phenotype label, under two edges |
| `MONDO` | `SY`, `PT_MONDO_SIMPLE` | disease label |
| `DOID` | `SY` | disease label |
| `OMIM` | `PTCS`, `PHENO`, `ETAL` | disease label |
| `SNOMEDCT_US` | `PT` | clinical label |

`PT` covers 2.2M edges against `HAS_TERM`'s 11.1M, so binding only `PT`
misses most labels in the graph. **Do not bind a term edge on an unfamiliar
source** — leave it open and return `type(tr)`.

The `PT_<SAB>` variants follow the documented non-steward rule
(`02_data_model.md`).

## Relationship properties

| Property | On | Note |
| --- | --- | --- |
| `SAB` | 1,855 predicates | The asserting source |
| `CUI` | 199 predicates | Code-to-Term edges carry this instead of `SAB` |
| `evidence_class` | 42 predicates | **Heterogeneous** — see below. Not a single vocabulary. |

`evidence_class` appears on `bioactivity`, the four LINCS regulation
predicates, `coexpressed_with`, `interacts_with`, and the ClinGen validity
and actionability set. Full map in
`assets/evidence_class_predicates.json`.

**`evidence_class` does not carry one kind of value.** Verified across
predicates: numeric strings on LINCS regulation edges (e.g. `0.0221`), assay
types on IDGP `bioactivity` (`IC50`, `Ki`), and expert-panel classifications
on CLINGEN (`Definitive` through `Limited`, plus `Disputed`). The property
name is shared; the semantics are per-source.

So **report it, never filter on it, and never assume it is categorical.** A
comparison written for one source's values is meaningless against another's,
and a numeric-looking string is still a string.

**Seven predicates carry it optionally** — including `bioactivity` and all
four LINCS regulation predicates. On those, `WHERE r.evidence_class = '...'`
silently drops every edge lacking the property.

## Node properties

| Label | Properties | Always present |
| --- | --- | --- |
| `Code` | `CodeID`, `SAB` | yes |
| `Code` | `CODE` | no |
| `Code` | `value`, `lowerbound`, `upperbound` (Double) | no |
| `Concept` | `CUI` | yes |
| `Term` | `name` | yes |
| `Semantic` | `name`, `TUI`, `STN`, `DEF` | yes |
| `Definition` | `DEF`, `SAB`, `ATUI` | yes |

`unit` is permitted by the model but was not observed in this build.

### Quantitative values

Continuous quantities are **bin Concepts**: a measurement links to the bin its
value falls in, so a threshold is a question about which bins, not a numeric
comparison.

**The numeric bounds are not properties.** `EXPBINS` Code nodes carry only
`SAB`, `CODE`, and `CodeID` — verified by `keys()`. So this returns null for
every row and no error:

```cypher
// WRONG — EXPBINS carries no bounds
OPTIONAL MATCH (m)-[:has_expression {SAB:'GTEXEXP'}]-(:Concept)-[:HAS_CODE]->(bin:Code {SAB:'EXPBINS'})
WHERE bin.lowerbound >= 5.0
```

`value`, `lowerbound`, and `upperbound` are permitted by the UBKG model and
appear in the schema sampler as optional properties on `Code`, but they are
not populated on `EXPBINS`. Before using them on any bin SAB, confirm with:

```cypher
MATCH (c:Code {SAB:$sab}) RETURN keys(c) AS props, count(*) AS n
```

The bounds are encoded in the CodeID — `EXPBINS:0.1.0.2` is the bin
[0.1, 0.2]. Selecting bins by matching CodeIDs is exact and safe. Recovering
the numeric bounds, however, is possible **only** by parsing that string, and
the delimiter is the same character as the decimal point — so a parse has to
be written against the observed convention for that SAB rather than derived.
Prefer matching; parse only when a numeric value is genuinely needed, and
verify the parse against enumerated CodeIDs first.

**The worst case is `PVALUEBINS`.** `PVALUEBINS:0.1e-12` denotes the interval
**[0, 1e-12]** — a lower bound of `0` and an upper bound of `1e-12`. Read as a
single number it looks like `0.1e-12`, so a naive parse misreads the most
significant bin by an order of magnitude, and does so silently on the bin a
significance query cares about most.

Bin structures and occupancy are decoded in `17_gtex_bins_addendum.md`. See
also `08_dcc_endpoints.md`.

**Why:** the bound properties were introduced *after* the GTEx binned dataset
was ingested, so `EXPBINS` predates the convention it appears to follow. This
is version skew, not a defect in the graph, and it is expected to be corrected
in the JKG generation.

**Thresholding still works — by selecting bins, not by parsing them.** The bin
set is small and enumerable, so list it once and match the CodeIDs wanted:

```cypher
MATCH (c:Code {SAB:'EXPBINS'})
RETURN c.CodeID
ORDER BY c.CodeID
```

Then filter by exact match or prefix against that known set:

```cypher
MATCH (m)-[:has_expression {SAB:'GTEXEXP'}]-(:Concept)-[:HAS_CODE]->(bin:Code {SAB:'EXPBINS'})
WHERE bin.CodeID IN ['EXPBINS:5.0.6.0', 'EXPBINS:6.0.7.0', 'EXPBINS:7.0.8.0']
```

**Matching a CodeID is not parsing one.** Decomposing `EXPBINS:0.1.0.2` into
fields is ambiguous, because the separator and the decimal point are the same
character. Comparing it to a string you have seen in the graph is exact.
Enumerate first, then select; never split.

Other bin SABs may differ, since they were ingested at different times. Check
each with `keys()` rather than generalising from `EXPBINS` in either
direction.

## Indexes

**Check the deployment before assuming anything about query cost.**

```cypher
SHOW INDEXES YIELD name, type, entityType, labelsOrTypes, properties
```

DDKG deployments may have different index configurations. A deployment may
include property indexes on fields such as `Code.CodeID`, `Code.SAB`, and
`Concept.CUI`, and may include a TEXT index on `Term.name`. Where appropriate
indexes are present, identifier and source anchors can be served by indexes
rather than full node scans.

Neo4j databases also normally include token `LOOKUP` indexes for node labels
and relationship types. These help resolve labels and relationship types but
do not index node properties.

**Do not wrap an indexed property in a function unless the resulting query
plan has been checked.** Expressions such as `toLower(t.name)` or
`trim(toLower(t.name))` prevent a plain index on `Term.name` from serving that
property predicate. The overall query can still be efficient if another
indexed anchor, such as `Code.SAB` or `Code.CodeID`, first reduces the
candidate set.

When case or whitespace normalization is required, reduce candidates with an
indexable identifier, source, or raw text predicate where possible, then apply
the normalization test to those candidates. If a deployment maintains an
appropriately normalized property or full-text index, use that facility
instead.

The anchoring and staging guidance below applies regardless of deployment.
The expected cost can differ substantially depending on the available indexes.

## Query cost

Anchoring and staging determine whether a query finishes. Check the active
deployment before assigning a cost to a property match. A query that is
logically correct but impractical to execute is not a usable answer.

### What costs what

| Construct | With an applicable property index | Without one |
| --- | --- | --- |
| `(c:Code {CodeID:'X:Y'})` | index-backed anchor | scan of `Code` nodes |
| `(c:Code {SAB:'HP'})` | index-backed but potentially broad | scan of `Code` nodes |
| `(c:Concept {CUI:...})` | index-backed anchor | scan of `Concept` nodes |
| `t.name CONTAINS '…'` | may use a TEXT index | scan of `Term` nodes |
| `toLower(t.name) = '…'` | plain `Term.name` index cannot serve this predicate | scan/filter of `Term` nodes |
| `-[]->(t:Term)` with unbound relationship type | expands every matching term edge | same |
| `-[r:predicate]-` | relationship-type LOOKUP can serve the type | same |

Use `EXPLAIN` or `PROFILE` when query cost matters rather than inferring the
plan from a different DDKG installation.

### Anchor on the smallest enumerable set

"Start from the smaller side" is usually read as "the smaller of the two
things in the question". It means the smallest set you can *name*.

A tissue is three UBERON codes. A phenotype category matched by string is
however many terms contain that substring, which is unknown until it runs.
Anchoring on the three is a different order of magnitude, even though the
tissue looks like the incidental half of the question.

So prefer, in order: specific `CodeID` values enumerated in advance, then a
bound relationship type, then a SAB, and only then a string match.

### Reduce between halves

An intersection query has two halves and they must not both expand before
anything collapses. Put a `WITH DISTINCT` after the first half so the second
runs against a reduced set:

```cypher
MATCH (tissue)-[:expressed_in {SAB:'GTEXEXP'}]-(m)-[:expressed_in {SAB:'GTEXEXP'}]-(gene)
WITH DISTINCT gene          // collapse before the second half
MATCH (gene)-[pr]-(pheno)
```

Without it the planner materialises the full cross product and the first
aggregation happens at the end, by which point the work is done.

### Watch for undirected re-traversal

Where several things hang off one node — a `GTEXEXP` measurement connects to
both a gene and a tissue by `expressed_in` — an undirected match from that
node walks back the way it came as well as onward. Bind the far endpoint's SAB
so the wrong branch is discarded early, or write the direction where it is
known.

### Say when a query is expensive

If a query will scan a bulk label, tell the user before they run it, and give
the cheaper route if one exists. Six hours with no result is worse than a
narrower answer returned in one minute, and the user cannot see the cost from
the Cypher.
