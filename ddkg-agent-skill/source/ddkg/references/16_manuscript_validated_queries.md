# Validated queries from the DDKG manuscript (S7)

Eleven queries indexed here were validated 28–29 August 2026 against the
**December 2025 CSV release (`DataDistillery_2025_04_DEC`)**, `HAS_CODE` schema, Neo4j 5.26.28
Community.

These summarize the most recently validated Cypher associated with this
skill, and they demonstrate patterns the User Guide examples do not: per-hop
staging with per-row caps, symmetric-predicate walk-back guards, cross-species bridges, and
neighbourhood proximity scoring. Prefer them where they cover the question.

The full text of each query lives in the manuscript's Supplementary Note S7
and is not duplicated in this package. What follows is the pattern each one
establishes; use it as release-specific design evidence, not as a claim that
the exact deposited query text is present here.

## Contents

1. [Patterns established](#patterns-established)
2. [Query index](#query-index)
3. [Facts confirmed](#facts-confirmed)
4. [Why manuscript queries bind ACR and MTH_ACR](#why-manuscript-queries-bind-acr-and-mth-acr)

## Patterns established

### Per-hop staged form with per-row caps

Q07 and Q04 use a `CALL { ... }` subquery with `LIMIT` inside it, so each
parent row expands a bounded amount rather than the planner choosing a join
order across the whole pattern:

```cypher
CALL {
  WITH g
  MATCH (g)-[:expressed_in {SAB:'GTEXEXP'}]-(m:Concept)
  WITH DISTINCT g, m LIMIT 20
  MATCH (m)-[:expressed_in {SAB:'GTEXEXP'}]-(t:Concept)
  WHERE t <> g
  WITH DISTINCT m, t LIMIT 20
  ...
  LIMIT 3
}
```

Two things are load-bearing. `WITH DISTINCT ... LIMIT n` between hops caps
per-entity expansion. And `WHERE t <> g` guards the walk-back: `expressed_in`
is symmetric and connects the measurement to both the gene and the tissue, so
without the guard the second hop returns to the gene it came from.

### Caps can amputate

Q08 carries an explicit warning worth generalising: *a zero result under caps
is not conclusive, because the caps can amputate rare paths.* When a capped
query returns nothing, re-run it as a staged funnel with one leg per statement
and read the counts — the first zero is the dead constraint.

### Neighbourhood proximity scoring

Q11 scores genes by shared-neighbour count from a phenotype anchor:

```cypher
MATCH (pc:Code {CodeID:'HP:0001636'})<-[:HAS_CODE]-(p:Concept)
MATCH (p)-[]-(x:Concept)
WITH DISTINCT p, x
MATCH (x)-[]-(g:Concept)
WHERE g <> p
WITH p, g, count(DISTINCT x) AS cn_score
```

Unbound predicates on both hops, deliberately — the score is topological. Runs
16–17 s per anchor. The `WITH DISTINCT p, x` between hops is what makes it
finish.

### Cross-species bridge

Q10 chains Kids First cohort variants to mouse phenotypes and back to a human
phenotype: `KF` → `HCOP` 1:1 orthologs → `MPMGI` → `MP` → **`HPOMP`
`is_approximately_equivalent_to`** → `HP`. Q09 does the rat equivalent through
`RATHCOP` `has_human_ortholog`.

These are the verified routes for deliberate cross-species work — as opposed
to the accidental mouse contamination documented in
`05_entity_resolution.md#species`.

### Return the SAB rather than binding it

Q04 writes `-[gp:gene_product_of]-` unbound and returns `gp.SAB AS
gene_product_source`, which surfaces that `gene_product_of` carries both
`UNIPROTKB` (20,208 edges) and `GENCODE` (73). Binding `{SAB:'UNIPROTKB'}`
silently drops the GENCODE assertions.

### Labels optional throughout

Q03's comment states the rule directly: *drug label OPTIONAL — labels are
decoration, never constraints.* For `PUBCHEM:2247`, the UMLS Concept carries
no term edge while the minted twin carries the term and LINCS regulation
edges. A required term match on the untwinned Concept zeroed the chain.

## Query index

| Query | Use case | Pattern |
| --- | --- | --- |
| Q01 | Chromatin loops × eQTLs | `shortestPath` over `precedes_1kbp_band` between loop anchors; node SAB `4DNL`, edge SAB `4DN` |
| Q02 | FTD biomarkers | Phenotype → gene → ENCODE RBS → RBP → biofluid, with a `correlated_in` triangle closure |
| Q03 | Compound perturbation | `PUBCHEM` anchor → LINCS regulation → RBP → biofluid |
| Q04 | Glycosyltransferase expression | `has_enzyme_protein` (reaction → enzyme) → gene → GTEx, staged |
| Q05 | Asthma → genes → compounds | LINCS with numeric `evidence_class` |
| Q06 | Target-family bioactivity | `UNIPROTKB` `PT` term scan → IDGP compounds |
| Q07 | Single-target compounds and expression | Per-hop staged with per-row caps |
| Q08 | Metabolite → condition | MW chain with hard caps between stages |
| Q09 | Rat exercise → human eQTL | `RATHCOP` `has_human_ortholog` |
| Q10 | Cohort variants → mouse phenotype | `HCOP` / `MPMGI` / `HPOMP` bridge |
| Q11 | Cross-disease gene proximity | Shared-neighbour `cn_score`, four phenotype anchors |

## Facts confirmed

- `has_enzyme_protein` direction is **reaction → enzyme**.
- 4DN loop predicates emit **from** the loop Concept.
- `located_in {SAB:'GTEXEQTL'}` should be matched **undirected**.
- LINCS `evidence_class` carries numeric strings (`0.0177`); IDGP carries
  assay types (`Ki`, `IC50`).
- `GLYCANS` is edge-only, 182 `has_enzyme_protein` edges.
- `predicted_in {ERCCRBP}` has 268 edges against 462K for
  `molecularly_interacts_with` — thin legs are real, and census presence says
  nothing about conjunction coverage.

## Why manuscript queries bind ACR and MTH_ACR

`13_empirical_findings_aug2025_validation.md` states: bind `ACR` alone for
symbols, because `MTH_ACR` appends `" gene"` and binding both doubles rows.

Manuscript queries Q05, Q09 and Q10 bind `[:ACR|MTH_ACR]`. This is deliberate
rather than a contradiction: on the July 2025 build `[:ACR]` alone does not
resolve, so binding both makes a query run on either build. Symbol lists come
back doubled there — `"FUT5"` alongside `"FUT5 gene"` — which the manuscript
queries absorb downstream. See
`12_setup_and_access.md#comparing-releases-on-an-old-schema-build`.

**So:** when generating a symbol lookup for the December 2025 release, bind
`ACR` alone. When reproducing a manuscript query, reproduce it verbatim and
say the double binding is for cross-release portability rather than an error.
