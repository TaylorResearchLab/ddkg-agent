# Edge registry

Derived from the live December 2025 build.
**2101 relationship types** across **3244 predicate/SAB combinations**,
totalling 186,651,416 relationships. The guide demonstrates 49 of them.

Full table: `assets/predicates.csv`. Inverse mapping: `assets/inverse_pairs.json`.

## Contents

1. [Structural edges](#structural-edges)
2. [Term edges](#term-edges)
3. [Inverse pairs and direction](#inverse-pairs-and-direction)
4. [Highest-volume assertion predicates](#highest-volume-assertion-predicates)
5. [The long tail](#the-long-tail)

## Structural edges

These four carry no biology and have no SAB. **The names below are the only
correct ones in the August 2025 schema.** `CODE`, `PREF_TERM`, `STY`, and `DEF` do not
exist in this graph — a query using any of them returns nothing, silently.

| Edge | Connects | Count |
| --- | --- | --- |
| `HAS_CODE` | `Concept` to `Code` | 21,279,506 |
| `HAS_TERM` | `Code` to `Term` | 11,114,862 |
| `HAS_SEMANTIC` | `Concept` to `Semantic` | 3,781,935 |
| `HAS_DEFINITION` | to `Definition` | 687,695 |

## Term edges

43 typed lexical edges sit alongside `HAS_TERM`, and they are
source-specific. Binding only `:PT` misses most of the graph's labels —
`PT` covers 2,221,626 edges against `HAS_TERM`'s 11,114,862.

When resolving an unfamiliar source, leave the type unbound and return
`type(tr)` to see which applies.

| Term edge | Count |
| --- | --- |
| `PT_DGN` | 3,702,956 |
| `SY` | 2,515,210 |
| `PT_ERCCREG` | 2,259,986 |
| `PT` | 2,221,626 |
| `FN` | 842,273 |
| `SCN` | 761,692 |
| `PT_GENCODE` | 478,674 |
| `PT_ERCCRBP` | 462,297 |
| `CE` | 325,178 |
| `PT_IDGP` | 324,926 |
| `NM` | 324,067 |
| `PT_IDGD` | 323,901 |
| `AB` | 268,331 |
| `ET` | 212,080 |
| `ACR` | 91,275 |
| `IN` | 68,741 |
| `PT_PROTEOFORM` | 52,450 |
| `MTH_ACR` | 44,067 |
| `PT_GLYCANS` | 33,885 |
| `PT_MONDO_SIMPLE` | 27,444 |
| `PT_EFO` | 26,591 |
| `PT_HCOP` | 22,245 |
| `PT_UBERON_BASE` | 14,671 |
| `PT_MPMGI` | 12,307 |
| `PT_MW` | 9,654 |

## Inverse pairs and direction

**455 predicates are stored as inverse pairs**, and in 433 of those the
two directions have byte-identical counts. Each assertion is materialised
twice, once under each name:

| Forward | Inverse | Count each |
| --- | --- | --- |
| `isa` | `inverse_isa` | 7,589,414 |
| `part_of` | `has_part` | 5,219,616 |
| `regulates` | `regulated_by` | 4,808,470 |
| `expressed_in` | `expresses` | 4,145,663 |
| `above_1kbp_band` | `inverse_above_1kbp_band` | 3,088,297 |
| `precedes_1kbp_band` | `inverse_precedes_1kbp_band` | 3,088,273 |
| `has_expression` | `inverse_has_expression` | 2,073,492 |
| `p_value` | `inverse_p_value` | 1,025,446 |
| `inverse_targets_expression_of_gene` | `targets_expression_of_gene` | 670,529 |
| `inverse_positively_correlated_with_chemical_or_drug` | `positively_correlated_with_chemical_or_drug` | 625,812 |
| `inverse_negatively_correlated_with_chemical_or_drug` | `negatively_correlated_with_chemical_or_drug` | 600,079 |
| `inverse_coexpressed_with` | `coexpressed_with` | 539,017 |

This has a practical consequence the guide does not spell out. Matching
undirected with an **unbound** predicate returns each assertion twice, once
as `isa` and once as `inverse_isa`:

```cypher
// returns duplicate rows
MATCH (a:Concept {CUI:'C0000000'})-[r]-(b:Concept)
RETURN a, type(r), b
```

Either bind the predicate, or filter the mirror out:

```cypher
MATCH (a:Concept {CUI:'C0000000'})-[r]-(b:Concept)
WHERE NOT type(r) STARTS WITH 'inverse_'
RETURN a, type(r), r.SAB, b
LIMIT 25
```

Note that `STARTS WITH 'inverse_'` catches most but not all pairs — some
use distinct names such as `part_of`/`has_part` and `located_in`/`location_of`.
`assets/inverse_pairs.json` maps every pair.

## Highest-volume assertion predicates

2054 assertion predicates exist. These 60 are the largest.

| Predicate | Edges | Inverse |
| --- | --- | --- |
| `refers_to` | 7,872,376 | `inverse_refers_to` |
| `inverse_refers_to` | 7,870,654 | `refers_to` |
| `isa` | 7,589,414 | `inverse_isa` |
| `inverse_isa` | 7,589,414 | `isa` |
| `part_of` | 5,219,616 | `has_part` |
| `has_part` | 5,219,616 | `part_of` |
| `regulates` | 4,808,470 | `regulated_by` |
| `regulated_by` | 4,808,470 | `regulates` |
| `expressed_in` | 4,145,663 | `expresses` |
| `expresses` | 4,145,663 | `expressed_in` |
| `location_of` | 3,494,405 | `located_in` |
| `located_in` | 3,494,403 | `location_of` |
| `above_1kbp_band` | 3,088,297 | `inverse_above_1kbp_band` |
| `inverse_above_1kbp_band` | 3,088,297 | `above_1kbp_band` |
| `precedes_1kbp_band` | 3,088,273 | `inverse_precedes_1kbp_band` |
| `inverse_precedes_1kbp_band` | 3,088,273 | `precedes_1kbp_band` |
| `has_expression` | 2,073,492 | `inverse_has_expression` |
| `inverse_has_expression` | 2,073,492 | `has_expression` |
| `par` | 1,618,262 | — |
| `chd` | 1,618,262 | — |
| `p_value` | 1,025,446 | `inverse_p_value` |
| `inverse_p_value` | 1,025,446 | `p_value` |
| `ro` | 789,730 | — |
| `associated_with` | 719,990 | `inverse_associated_with` |
| `inverse_targets_expression_of_gene` | 670,529 | `targets_expression_of_gene` |
| `targets_expression_of_gene` | 670,529 | `inverse_targets_expression_of_gene` |
| `inverse_associated_with` | 665,878 | `associated_with` |
| `mapped_from` | 649,930 | — |
| `mapped_to` | 649,930 | — |
| `aq` | 633,885 | — |
| `qb` | 633,885 | — |
| `inverse_positively_correlated_with_chemical_or_drug` | 625,812 | `positively_correlated_with_chemical_or_drug` |
| `positively_correlated_with_chemical_or_drug` | 625,812 | `inverse_positively_correlated_with_chemical_or_drug` |
| `inverse_negatively_correlated_with_chemical_or_drug` | 600,079 | `negatively_correlated_with_chemical_or_drug` |
| `negatively_correlated_with_chemical_or_drug` | 600,079 | `inverse_negatively_correlated_with_chemical_or_drug` |
| `inverse_coexpressed_with` | 539,017 | `coexpressed_with` |
| `coexpressed_with` | 539,017 | `inverse_coexpressed_with` |
| `has_inactive_ingredient` | 500,390 | — |
| `inactive_ingredient_of` | 500,390 | — |
| `inverse_pathway_associated_with_gene` | 486,613 | `pathway_associated_with_gene` |
| `pathway_associated_with_gene` | 486,613 | `inverse_pathway_associated_with_gene` |
| `overlaps` | 470,070 | `inverse_overlaps` |
| `inverse_overlaps` | 470,070 | `overlaps` |
| `inverse_involved_in` | 466,820 | `involved_in` |
| `involved_in` | 466,820 | `inverse_involved_in` |
| `molecularly_interacts_with` | 462,297 | `inverse_molecularly_interacts_with` |
| `inverse_molecularly_interacts_with` | 462,297 | `molecularly_interacts_with` |
| `inverse_interacts_with` | 459,496 | `interacts_with` |
| `interacts_with` | 459,496 | `inverse_interacts_with` |
| `inverse_bioactivity` | 428,636 | `bioactivity` |
| `bioactivity` | 428,636 | `inverse_bioactivity` |
| `subset_includes_concept` | 404,979 | — |
| `concept_in_subset` | 404,979 | — |
| `has_component` | 348,567 | `inverse_has_component` |
| `component_of` | 348,484 | — |
| `rn` | 347,069 | — |
| `rb` | 347,069 | — |
| `is_feature_type` | 312,946 | `inverse_is_feature_type` |
| `inverse_is_feature_type` | 312,946 | `is_feature_type` |
| `is_directional_form_of` | 312,867 | `inverse_is_directional_form_of` |

## The long tail

The distribution is steep: the top 250 predicates cover 97.3% of all
relationships, and the remaining ~1,850 share the rest. Most of the tail is
UMLS ontology structure rather than DCC assertions.

Practical consequence: a predicate absent from the tables above is not
absent from the graph. Check `assets/predicates.csv` before telling anyone
a relationship type does not exist.

## Relationship properties

Relationships are first-class objects. Three property patterns exist:

| Property | On | Note |
| --- | --- | --- |
| `SAB` | 1,855 predicates | The asserting source. |
| `CUI` | 199 predicates | Carried by `Code`-to-`Term` edges (`PT`, `SY`, `FN`, `SCN`, `PT_*`) instead of `SAB`. These are lexical, not assertions. |
| `evidence_class` | 42 predicates | Provenance or confidence class on curated assertions. |

### evidence_class

42 predicates carry `evidence_class` alongside `SAB` (23 forward plus their inverses). Returning only `r.SAB` on these
discards the qualifier that makes the assertion interpretable.

| Predicate | `evidence_class` |
| --- | --- |
| `assertion_pending` | always present |
| `autosomal_dominant_inheritance` | always present |
| `autosomal_dominant_inheritance_with_paternal_imprinting_hp_0012274` | always present |
| `autosomal_recessive_inheritance` | always present |
| `bioactivity` | **optional** |
| `characterized_by` | **optional** |
| `coexpressed_with` | always present |
| `definitive_actionability` | always present |
| `gene_disease_validity` | always present |
| `has_variant_associated_with_disease` | always present |
| `in_similarity_relationship_with` | always present |
| `interacts_with` | always present |
| `limited_actionability` | always present |
| `moderate_actionability` | always present |
| `negatively_regulated_by` | **optional** |
| `negatively_regulates` | **optional** |
| `no_assertion__scoring_group_absence` | always present |
| `positively_regulated_by` | **optional** |
| `positively_regulates` | **optional** |
| `semidominant_inheritance` | always present |
| `strong_actionability` | always present |
| `x_linked_inheritance` | always present |
| `x_linked_inheritance_dominant_hp_0001423` | always present |

**The optional ones are a trap.** On these, `WHERE r.evidence_class = '...'`
silently drops every relationship lacking the property, and the result is
indistinguishable from a biological negative:

```
`bioactivity`, `characterized_by`, `inverse_bioactivity`, `negatively_regulated_by`, `negatively_regulates`, `positively_regulated_by`, `positively_regulates`
```

Prefer returning `r.evidence_class` and letting the user see nulls, or use
`WHERE r.evidence_class IS NULL OR r.evidence_class = $wanted` when a filter
is genuinely needed.

Full map: `assets/evidence_class_predicates.json`.

## Node properties

| Label | Property | Type | Always present |
| --- | --- | --- | --- |
| `Code` | `CodeID` | String | yes |
| `Code` | `SAB` | String | yes |
| `Code` | `CODE` | String | no |
| `Code` | `value` | Double | no |
| `Code` | `lowerbound` | Double | no |
| `Code` | `upperbound` | Double | no |
| `Concept` | `CUI` | String | yes |
| `Term` | `name` | String | yes |
| `Semantic` | `name`, `TUI`, `STN`, `DEF` | String | yes |
| `Definition` | `DEF`, `SAB`, `ATUI` | String | yes |

### Quantitative values

`value`, `lowerbound`, and `upperbound` on `Code` are how continuous
quantities are stored. Bin Codes such as `EXPBINS` and `PVALUEBINS` carry a
numeric range, so thresholding is a comparison **on the Code node**, not on
the edge:

```cypher
MATCH (ec:Concept)-[:HAS_CODE]->(eqtl:Code {SAB:'GTEXEQTL'})
MATCH (ec)-[r:p_value {SAB:'GTEXEQTL'}]-(bc:Concept)
MATCH (bc)-[:HAS_CODE]->(bin:Code {SAB:'PVALUEBINS'})
WHERE bin.upperbound <= 0.05
RETURN eqtl.CODE, bin.lowerbound, bin.upperbound, r.SAB
LIMIT 25
```

All three are optional, so a numeric filter excludes every Code without the
property. Check for their presence before relying on them.

## What is still missing

Endpoint pairings for DCC sources are in `08_dcc_endpoints.md`, enumerated from
the graph. UMLS-internal pairings (952,393 further triples) were enumerated
but are not shipped; they are ontology scaffolding rather than assertion.
