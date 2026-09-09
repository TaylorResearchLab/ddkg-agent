# DCC endpoint map

What each DCC source actually connects, from 25,682 triples enumerated off
the live graph. This is the table to consult before composing a traversal:
it answers *which identifier spaces sit at either end of this predicate*,
which is the question that cannot be reasoned out and is the usual cause of
a query that runs cleanly and returns nothing.

Raw rows: `assets/sab_triples_dcc.csv`. Grouped form: `assets/dcc_endpoints.json`.
UMLS-internal structure (952,393 further triples) is not shipped; it is
ontology scaffolding rather than DCC assertion.

## How to read a fan-out

Many DCC predicates list 30-60 SABs on one side. That is not 60 distinct
relationships. DCC edges attach to heavily normalised Concepts -- tissues,
diseases, phenotypes -- and those Concepts carry Codes from many
vocabularies at once. `expressed_in {SAB:'GTEXEXP'}` reaching `UBERON`,
`CL`, `FMA` and `CHEBI` means one tissue Concept wearing four identifier
systems.

So the wide side is a **menu of anchors**: pick the vocabulary the user
already has identifiers in. It is not a set of separate biological claims,
and a query should anchor on one of them rather than returning all.

The edge itself remains a first-class object. Match it as `-[r {SAB:'X'}]-`
and return `r` or its properties, not merely the endpoints -- see
`07_predicate_registry.md` for what relationships carry beyond `SAB`.

## Contents

- [4DN](#4dn)
- [Azimuth](#azimuth-az-and-hmaz)
- [CMAP](#cmap)
- [DisGeNET](#disgenet-dgn)
- [ERCCRBP](#erccrbp)
- [ERCCREG](#erccreg)
- [GENCODE](#gencode)
- [GENCODEHSCLO](#gencodehsclo)
- [GLYCANS](#glycans)
- [GLYCOCOO](#glycocoo)
- [GLYCORDF](#glycordf)
- [GTEXCOEXP](#gtexcoexp)
- [GTEXEQTL](#gtexeqtl)
- [GTEXEXP](#gtexexp)
- [HGNCHPO](#hgnchpo)
- [HSCLO](#hsclo)
- [HUBMAP](#hubmap)
- [IDGD](#idgd)
- [IDGP](#idgp)
- [KF](#kf)
- [LINCS](#lincs)
- [MOTRPAC](#motrpac)
- [MW](#mw)
- [NPO](#npo)
- [NPOSKCAN](#nposkcan)
- [PROTEOFORM](#proteoform)

## 4DN

*Chromatin loops and Hi-C datasets*  — 56 triples, 18 predicates.

| Predicate | Subject SABs | Object SABs |
| --- | --- | --- |
| `dataset_involves_cell_type` | `4DND` | `CHV`, `CSP`, `EFO`, `FMA` +15 more |
| `inverse_dataset_involves_cell_type` | `CHV`, `CSP`, `EFO`, `FMA` +15 more | `4DND` |
| `has_assay_type` | `4DND` | `EFO`, `OBI` |
| `inverse_has_assay_type` | `EFO`, `OBI` | `4DND` |
| `dataset_has_file` | `4DND` | `4DNF` |
| `file_has_loop` | `4DNF` | `4DNL` |
| `inverse_dataset_has_file` | `4DNF` | `4DND` |
| `inverse_file_has_loop` | `4DNL` | `4DNF` |
| `loop_ds_end` | `4DNL` | `HSCLO` |
| `loop_ds_start` | `4DNL` | `HSCLO` |
| `loop_has_qvalue_bin` | `4DNL` | `4DNQ` |
| `loop_us_end` | `4DNL` | `HSCLO` |
| `loop_us_start` | `4DNL` | `HSCLO` |
| `inverse_loop_has_qvalue_bin` | `4DNQ` | `4DNL` |
| `inverse_loop_ds_end` | `HSCLO` | `4DNL` |
| `inverse_loop_ds_start` | `HSCLO` | `4DNL` |
| `inverse_loop_us_end` | `HSCLO` | `4DNL` |
| `inverse_loop_us_start` | `HSCLO` | `4DNL` |

Each loop carries four anchor edges: `loop_us_start`, `loop_us_end`,
`loop_ds_start`, and `loop_ds_end`, with 215,822 of each on the target
release. Span-based eQTL overlap saturated at 99.7% of loops; anchor-interval
overlap did not, at 95.4%.

A per-loop `CALL (loop_concept) { ... }` using two short `shortestPath`
traversals ran uncapped over all loops in about one minute. Observed loop
CodeIDs have the form `4DNL:<accession>.<coords>`. That form is descriptive;
do not derive identity by splitting it when a graph edge can supply the
coordinate relationship.

## CMAP

*Connectivity Map signatures*  — 2,268 triples, 4 predicates.

| Predicate | Subject SABs | Object SABs |
| --- | --- | --- |
| `positively_correlated_with_chemical_or_drug` | `AOT`, `CHEBI`, `CHV`, `CSP` +16 more | `ATC`, `CHEBI`, `CHV`, `CPM` +27 more |
| `inverse_positively_correlated_with_chemical_or_drug` | `ATC`, `CHEBI`, `CHV`, `CPM` +27 more | `AOT`, `CHEBI`, `CHV`, `CSP` +16 more |
| `inverse_negatively_correlated_with_chemical_or_drug` | `ATC`, `CHEBI`, `CHV`, `CPM` +27 more | `CHEBI`, `CHV`, `CSP`, `EFO` +15 more |
| `negatively_correlated_with_chemical_or_drug` | `CHEBI`, `CHV`, `CSP`, `EFO` +15 more | `ATC`, `CHEBI`, `CHV`, `CPM` +27 more |

## ERCCRBP

*RNA-binding protein sites*  — 152 triples, 12 predicates.

| Predicate | Subject SABs | Object SABs |
| --- | --- | --- |
| `inverse_overlaps` | `CHEBI`, `CHV`, `CSP`, `EFO` +15 more | `ENCODE.RBS.150.NO.OVERLAP` |
| `overlaps` | `ENCODE.RBS.150.NO.OVERLAP` | `CHEBI`, `CHV`, `CSP`, `EFO` +15 more |
| `inverse_correlated_in` | `ATC`, `CHV`, `CSP`, `FMA` +10 more | `ENCODE.RBS.150.NO.OVERLAP` |
| `inverse_not_correlated_in` | `ATC`, `CHV`, `CSP`, `FMA` +10 more | `ENCODE.RBS.150.NO.OVERLAP` |
| `inverse_not_predicted_in` | `ATC`, `CHV`, `CSP`, `FMA` +10 more | `UNIPROTKB` |
| `inverse_predicted_in` | `ATC`, `CHV`, `CSP`, `FMA` +10 more | `UNIPROTKB` |
| `correlated_in` | `ENCODE.RBS.150.NO.OVERLAP` | `ATC`, `CHV`, `CSP`, `FMA` +10 more |
| `not_correlated_in` | `ENCODE.RBS.150.NO.OVERLAP` | `ATC`, `CHV`, `CSP`, `FMA` +10 more |
| `not_predicted_in` | `UNIPROTKB` | `ATC`, `CHV`, `CSP`, `FMA` +10 more |
| `predicted_in` | `UNIPROTKB` | `ATC`, `CHV`, `CSP`, `FMA` +10 more |
| `inverse_molecularly_interacts_with` | `ENCODE.RBS.150.NO.OVERLAP` | `UNIPROTKB` |
| `molecularly_interacts_with` | `UNIPROTKB` | `ENCODE.RBS.150.NO.OVERLAP` |

`ENCODE.RBS.150.NO.OVERLAP` CodeIDs end in the RBP symbol, identifying
RBP-specific binding sites. Treat the embedded symbol as an observed format
for diagnosis; use graph relationships rather than string parsing for durable
identity.

## ERCCREG

*exRNA regulatory elements*  — 224 triples, 12 predicates.

| Predicate | Subject SABs | Object SABs |
| --- | --- | --- |
| `part_of` | `CHV`, `CL`, `CLINGEN.ALLELE.REGISTRY`, `CSP` +22 more | `ENCODE.CCRE.ACTIVITY`, `GTEXEQTL` |
| `has_part` | `ENCODE.CCRE.ACTIVITY`, `GTEXEQTL` | `CHV`, `CL`, `CLINGEN.ALLELE.REGISTRY`, `CSP` +22 more |
| `regulated_by` | `AOT`, `CHEBI`, `CHV`, `CSP` +17 more | `ENCODE.CCRE.ACTIVITY` |
| `regulates` | `ENCODE.CCRE.ACTIVITY` | `AOT`, `CHEBI`, `CHV`, `CSP` +17 more |
| `negatively_regulated_by` | `CHEBI`, `CHV`, `CSP`, `EFO` +15 more | `GTEXEQTL` |
| `negatively_regulates` | `GTEXEQTL` | `CHEBI`, `CHV`, `CSP`, `EFO` +15 more |
| `positively_regulated_by` | `AOT`, `CHV`, `CSP`, `EFO` +14 more | `GTEXEQTL` |
| `positively_regulates` | `GTEXEQTL` | `AOT`, `CHV`, `CSP`, `EFO` +14 more |
| `isa` | `ENCODE.CCRE.ACTIVITY` | `ENCODE.CCRE.CTCF`, `ENCODE.CCRE.H3K27AC`, `ENCODE.CCRE.H3K4ME3` |
| `inverse_isa` | `ENCODE.CCRE.CTCF`, `ENCODE.CCRE.H3K27AC`, `ENCODE.CCRE.H3K4ME3` | `ENCODE.CCRE.ACTIVITY` |
| `located_in` | `CLINGEN.ALLELE.REGISTRY` | `ENCODE.CCRE` |
| `location_of` | `ENCODE.CCRE` | `CLINGEN.ALLELE.REGISTRY` |

## GENCODE

*Gene and transcript models*  — 728 triples, 18 predicates.

| Predicate | Subject SABs | Object SABs |
| --- | --- | --- |
| `located_in` | `AOT`, `CHEBI`, `CHV`, `CSP` +17 more | `CHV`, `CSP`, `FMA`, `GENCODE_VS` +11 more |
| `location_of` | `CHV`, `CSP`, `FMA`, `GENCODE_VS` +11 more | `AOT`, `CHEBI`, `CHV`, `CSP` +17 more |
| `is_directional_form_of` | `AOT`, `CHEBI`, `CHV`, `CSP` +17 more | `GENCODE_VS` |
| `is_feature_type` | `AOT`, `CHEBI`, `CHV`, `CSP` +17 more | `GENCODE_VS` |
| `transcribed_to` | `AOT`, `CHEBI`, `CHV`, `CSP` +17 more | `ENSEMBL` |
| `transcribed_from` | `ENSEMBL` | `AOT`, `CHEBI`, `CHV`, `CSP` +17 more |
| `inverse_is_directional_form_of` | `GENCODE_VS` | `AOT`, `CHEBI`, `CHV`, `CSP` +17 more |
| `inverse_is_feature_type` | `GENCODE_VS` | `AOT`, `CHEBI`, `CHV`, `CSP` +17 more |
| `is_gene_biotype` | `AOT`, `CHEBI`, `CHV`, `CSP` +16 more | `GENCODE_VS` |
| `inverse_is_gene_biotype` | `GENCODE_VS` | `AOT`, `CHEBI`, `CHV`, `CSP` +16 more |
| `has_gene_product` | `ENSEMBL` | `UNIPROTKB` |
| `has_refseq_id` | `ENSEMBL` | `REFSEQ` |
| `isa` | `ENSEMBL` | `PGO` |
| `is_transcript_biotype` | `ENSEMBL` | `GENCODE_VS` |
| `inverse_is_transcript_biotype` | `GENCODE_VS` | `ENSEMBL` |
| `inverse_isa` | `PGO` | `ENSEMBL` |
| `inverse_has_refseq_id` | `REFSEQ` | `ENSEMBL` |
| `gene_product_of` | `UNIPROTKB` | `ENSEMBL` |

## GENCODEHSCLO

*Gene models on genomic coordinates*  — 84 triples, 4 predicates.

| Predicate | Subject SABs | Object SABs |
| --- | --- | --- |
| `ds_3_prime` | `AOT`, `CHEBI`, `CHV`, `CSP` +17 more | `HSCLO` |
| `us_5_prime` | `AOT`, `CHEBI`, `CHV`, `CSP` +17 more | `HSCLO` |
| `inverse_ds_3_prime` | `HSCLO` | `AOT`, `CHEBI`, `CHV`, `CSP` +17 more |
| `inverse_us_5_prime` | `HSCLO` | `AOT`, `CHEBI`, `CHV`, `CSP` +17 more |

## GLYCANS

*Glycan structures*  — 18 triples, 16 predicates.

| Predicate | Subject SABs | Object SABs |
| --- | --- | --- |
| `has_enzyme_protein` | `GLYCOSYLTRANSFERASE.REACTION`, `GLYGEN.GLYCOSYLATION` | `UNIPROTKB` |
| `inverse_has_enzyme_protein` | `UNIPROTKB` | `GLYCOSYLTRANSFERASE.REACTION`, `GLYGEN.GLYCOSYLATION` |
| `inverse_has_motif` | `GLYCAN.MOTIF` | `GLYTOUCAN` |
| `inverse_synthesized_by` | `GLYCOSYLTRANSFERASE.REACTION` | `GLYTOUCAN` |
| `inverse_has_glycosequence` | `GLYGEN.GLYCOSEQUENCE` | `GLYTOUCAN` |
| `inverse_attached_by` | `GLYGEN.GLYCOSYLATION` | `GLYGEN.RESIDUE` |
| `attached_by` | `GLYGEN.RESIDUE` | `GLYGEN.GLYCOSYLATION` |
| `has_parent` | `GLYGEN.RESIDUE` | `GLYGEN.RESIDUE` |
| `inverse_has_canonical_residue` | `GLYGEN.RESIDUE` | `GLYTOUCAN` |
| `inverse_has_parent` | `GLYGEN.RESIDUE` | `GLYGEN.RESIDUE` |
| `inverse_is_from_source` | `GLYGEN.SRC` | `GLYTOUCAN` |
| `has_canonical_residue` | `GLYTOUCAN` | `GLYGEN.RESIDUE` |
| `has_glycosequence` | `GLYTOUCAN` | `GLYGEN.GLYCOSEQUENCE` |
| `has_motif` | `GLYTOUCAN` | `GLYCAN.MOTIF` |
| `is_from_source` | `GLYTOUCAN` | `GLYGEN.SRC` |
| `synthesized_by` | `GLYTOUCAN` | `GLYCOSYLTRANSFERASE.REACTION` |

`GLYCOSYLTRANSFERASE.REACTION` and `GLYGEN.GLYCOSYLATION` Codes carry no
Term edge, so reaction identity must be displayed by `CodeID`. Both
vocabularies assert `has_enzyme_protein` to the same enzyme as separate
Concepts; for ABO, examples include `RXN00000012` and `RXN00000039`.

## GLYCOCOO

*Glycoconjugate ontology*  — 14 triples, 4 predicates.

| Predicate | Subject SABs | Object SABs |
| --- | --- | --- |
| `isa` | `CODAO`, `FALDO`, `GCO`, `GLYCAN` +1 more | `FALDO`, `GLYCAN`, `SIO`, `UNIPROT` |
| `inverse_isa` | `FALDO`, `GLYCAN`, `SIO`, `UNIPROT` | `CODAO`, `FALDO`, `GCO`, `GLYCAN` +1 more |
| `inverse_refers_to` | `SIO` | `SIO` |
| `refers_to` | `SIO` | `SIO` |

## GLYCORDF

*Glycomics RDF*  — 12 triples, 6 predicates.

| Predicate | Subject SABs | Object SABs |
| --- | --- | --- |
| `inverse_isa` | `FOAF`, `GLYCAN`, `UNIPROT` | `GLYCAN`, `UNIPROT` |
| `isa` | `GLYCAN`, `UNIPROT` | `FOAF`, `GLYCAN`, `UNIPROT` |
| `has_monosaccharide` | `GLYCAN` | `GLYCAN` |
| `has_signal` | `GLYCAN` | `GLYCAN` |
| `inverse_has_monosaccharide` | `GLYCAN` | `GLYCAN` |
| `inverse_has_signal` | `GLYCAN` | `GLYCAN` |

## GTEXCOEXP

*Gene co-expression*  — 376 triples, 2 predicates.

| Predicate | Subject SABs | Object SABs |
| --- | --- | --- |
| `coexpressed_with` | `AOT`, `CHV`, `EFO`, `ENSEMBL` +11 more | `AOT`, `CHV`, `EFO`, `ENSEMBL` +11 more |
| `inverse_coexpressed_with` | `AOT`, `CHV`, `EFO`, `ENSEMBL` +11 more | `AOT`, `CHV`, `EFO`, `ENSEMBL` +11 more |

## GTEXEQTL

*Expression quantitative trait loci*  — 78 triples, 4 predicates.

| Predicate | Subject SABs | Object SABs |
| --- | --- | --- |
| `location_of` | `AOT`, `CHEBI`, `CHV`, `CL` +34 more | `GTEXEQTL` |
| `located_in` | `GTEXEQTL` | `AOT`, `CHEBI`, `CHV`, `CL` +34 more |
| `p_value` | `GTEXEQTL` | `PVALUEBINS` |
| `inverse_p_value` | `PVALUEBINS` | `GTEXEQTL` |

### GTEXEQTL CodeIDs and tissue multiplicity

Observed `GTEXEQTL` CodeIDs embed the tissue, for example a suffix such as
`.b38.Heart.Left.Ventricle`. One variant position carries one Code per tissue;
the record-to-position factor was 1.46 to 1.59 on 4DN anchors.

The embedded tissue is a diagnostic cue, not an identity rule. UBERON gives
durable tissue identity; for per-tissue grain, group by the measurement Code
(see reference 18, section 5), since GTEx measurements also attach to parent
UBERON terms.

## GTEXEXP

*Bulk tissue expression*  — 76 triples, 4 predicates.

| Predicate | Subject SABs | Object SABs |
| --- | --- | --- |
| `expresses` | `AOT`, `CHEBI`, `CHV`, `CL` +33 more | `GTEXEXP` |
| `expressed_in` | `GTEXEXP` | `AOT`, `CHEBI`, `CHV`, `CL` +33 more |
| `inverse_has_expression` | `EXPBINS` | `GTEXEXP` |
| `has_expression` | `GTEXEXP` | `EXPBINS` |

## HGNCHPO

*Gene-to-phenotype associations*  — 2,072 triples, 2 predicates.

| Predicate | Subject SABs | Object SABs |
| --- | --- | --- |
| `inverse_associated_with` | `AOT`, `CCC`, `CCS`, `CCSR_ICD10CM` +56 more | `CHEBI`, `CHV`, `CSP`, `EFO` +15 more |
| `associated_with` | `CHEBI`, `CHV`, `CSP`, `EFO` +15 more | `AOT`, `CCC`, `CCS`, `CCSR_ICD10CM` +56 more |

In manuscript Q02, the mouse genotype-to-phenotype hop is the `MPMGI`
source rather than a separate `IMPC` SAB. `MPMGI` integrates MGI and IMPC
mouse genotype-phenotype evidence.

## HSCLO

*Genomic coordinate lattice*  — 84 triples, 18 predicates.

| Predicate | Subject SABs | Object SABs |
| --- | --- | --- |
| `inverse_contains_chromosome` | `CHV`, `CSP`, `FMA`, `GENCODE_VS` +11 more | `HSCLO` |
| `contains_chromosome` | `HSCLO` | `CHV`, `CSP`, `FMA`, `GENCODE_VS` +11 more |
| `above_1mbp_band` | `CHV`, `CSP`, `FMA`, `GENCODE_VS` +10 more | `HSCLO` |
| `inverse_above_1mbp_band` | `HSCLO` | `CHV`, `CSP`, `FMA`, `GENCODE_VS` +10 more |
| `above_10kbp_band` | `CHV`, `FMA`, `GENCODE_VS`, `GO` +3 more | `HSCLO` |
| `inverse_above_10kbp_band` | `HSCLO` | `CHV`, `FMA`, `GENCODE_VS`, `GO` +3 more |
| `above_100kbp_band` | `HSCLO` | `HSCLO` |
| `above_1kbp_band` | `HSCLO` | `HSCLO` |
| `inverse_above_100kbp_band` | `HSCLO` | `HSCLO` |
| `inverse_above_1kbp_band` | `HSCLO` | `HSCLO` |
| `inverse_precedes_100kbp_band` | `HSCLO` | `HSCLO` |
| `inverse_precedes_10kbp_band` | `HSCLO` | `HSCLO` |
| `inverse_precedes_1kbp_band` | `HSCLO` | `HSCLO` |
| `inverse_precedes_1mbp_band` | `HSCLO` | `HSCLO` |
| `precedes_100kbp_band` | `HSCLO` | `HSCLO` |
| `precedes_10kbp_band` | `HSCLO` | `HSCLO` |
| `precedes_1kbp_band` | `HSCLO` | `HSCLO` |
| `precedes_1mbp_band` | `HSCLO` | `HSCLO` |

## HUBMAP

*Tissue atlas anatomy*  — 1,296 triples, 38 predicates.

| Predicate | Subject SABs | Object SABs |
| --- | --- | --- |
| `isa` | `ALT`, `CHEBI`, `CHV`, `CPM` +35 more | `CHV`, `CSP`, `EFO`, `FMA` +23 more |
| `inverse_isa` | `CHV`, `CSP`, `EFO`, `FMA` +23 more | `ALT`, `CHEBI`, `CHV`, `CPM` +35 more |
| `has_laterality` | `CHV`, `CSP`, `FMA`, `FTU2D` +22 more | `CHV`, `HL7V3.0`, `HUBMAP`, `LNC` +4 more |
| `inverse_has_laterality` | `CHV`, `HL7V3.0`, `HUBMAP`, `LNC` +4 more | `CHV`, `CSP`, `FMA`, `FTU2D` +22 more |
| `has_two_character_code` | `CHV`, `CSP`, `FMA`, `FTU2D` +22 more | `HUBMAP` |
| `inverse_has_two_character_code` | `HUBMAP` | `CHV`, `CSP`, `FMA`, `FTU2D` +22 more |
| `has_active_status` | `HUBMAP`, `LCH_NW`, `MSH`, `NCI` +1 more | `HUBMAP`, `OBI`, `SENNET` |
| `inverse_has_active_status` | `HUBMAP`, `OBI`, `SENNET` | `HUBMAP`, `LCH_NW`, `MSH`, `NCI` +1 more |
| `has_pdr_category` | `HMFIELD`, `HRAVS`, `HUBMAP`, `SENNET` | `HMFIELD`, `HRAVS`, `HUBMAP`, `SENNET` |
| `inverse_has_pdr_category` | `HMFIELD`, `HRAVS`, `HUBMAP`, `SENNET` | `HMFIELD`, `HRAVS`, `HUBMAP`, `SENNET` |
| `inverse_has_fig2_agg_assay_type` | `HMFIELD`, `HRAVS`, `HUBMAP`, `SENNET` | `HRAVS`, `HUBMAP`, `SENNET` |
| `has_fig2_agg_assay_type` | `HRAVS`, `HUBMAP`, `SENNET` | `HMFIELD`, `HRAVS`, `HUBMAP`, `SENNET` |
| `inverse_has_dataset_type` | `CHV`, `HL7V3.0`, `HMFIELD`, `HRAVS` +6 more | `HUBMAP` |
| `has_dataset_type` | `HUBMAP` | `CHV`, `HL7V3.0`, `HMFIELD`, `HRAVS` +6 more |
| `has_fig2_category` | `HMFIELD`, `HRAVS`, `HUBMAP`, `SENNET` | `HUBMAP` |
| `has_fig2_modality` | `HMFIELD`, `HRAVS`, `HUBMAP`, `SENNET` | `HUBMAP` |
| `has_vitessce_hint` | `HMFIELD`, `HRAVS`, `HUBMAP`, `SENNET` | `HUBMAP` |
| `inverse_has_assaytype` | `HMFIELD`, `HRAVS`, `HUBMAP`, `SENNET` | `HUBMAP` |
| `inverse_has_description` | `HMFIELD`, `HRAVS`, `HUBMAP`, `SENNET` | `HUBMAP` |
| `has_assaytype` | `HUBMAP` | `HMFIELD`, `HRAVS`, `HUBMAP`, `SENNET` |
| `has_description` | `HUBMAP` | `HMFIELD`, `HRAVS`, `HUBMAP`, `SENNET` |
| `inverse_has_fig2_category` | `HUBMAP` | `HMFIELD`, `HRAVS`, `HUBMAP`, `SENNET` |
| `inverse_has_fig2_modality` | `HUBMAP` | `HMFIELD`, `HRAVS`, `HUBMAP`, `SENNET` |
| `inverse_has_vitessce_hint` | `HUBMAP` | `HMFIELD`, `HRAVS`, `HUBMAP`, `SENNET` |
| `inverse_must_contain` | `HRAVS`, `HUBMAP`, `SENNET` | `HUBMAP` |
| `must_contain` | `HUBMAP` | `HRAVS`, `HUBMAP`, `SENNET` |
| `contains` | `HUBMAP` | `HUBMAP` |
| `has_dir_schema` | `HUBMAP` | `HUBMAP` |
| `has_pipeline_shorthand` | `HUBMAP` | `HUBMAP` |
| `has_process_state` | `HUBMAP` | `HUBMAP` |
| `has_provider` | `HUBMAP` | `HUBMAP` |
| `has_tbl_schema` | `HUBMAP` | `HUBMAP` |
| `inverse_contains` | `HUBMAP` | `HUBMAP` |
| `inverse_has_dir_schema` | `HUBMAP` | `HUBMAP` |
| `inverse_has_pipeline_shorthand` | `HUBMAP` | `HUBMAP` |
| `inverse_has_process_state` | `HUBMAP` | `HUBMAP` |
| `inverse_has_provider` | `HUBMAP` | `HUBMAP` |
| `inverse_has_tbl_schema` | `HUBMAP` | `HUBMAP` |

## IDGD

*Compound-to-disease indications*  — 124 triples, 2 predicates.

| Predicate | Subject SABs | Object SABs |
| --- | --- | --- |
| `inverse_indication` | `ALT`, `AOT`, `CCC`, `CCS` +58 more | `PUBCHEM` |
| `indication` | `PUBCHEM` | `ALT`, `AOT`, `CCC`, `CCS` +58 more |

## IDGP

*Compound-to-protein bioactivity*  — 2 triples, 2 predicates.

| Predicate | Subject SABs | Object SABs |
| --- | --- | --- |
| `bioactivity` | `PUBCHEM` | `UNIPROTKB` |
| `inverse_bioactivity` | `UNIPROTKB` | `PUBCHEM` |

## KF

*Kids First cohorts, participants, variants*  — 138 triples, 6 predicates.

| Predicate | Subject SABs | Object SABs |
| --- | --- | --- |
| `phenotype_of` | `AOT`, `CCC`, `CCS`, `CCSR_ICD10CM` +44 more | `KFPT` |
| `has_phenotype` | `KFPT` | `AOT`, `CCC`, `CCS`, `CCSR_ICD10CM` +44 more |
| `inverse_gene_has_variants` | `AOT`, `CHEBI`, `CHV`, `CSP` +15 more | `KFGENEBIN` |
| `gene_has_variants` | `KFGENEBIN` | `AOT`, `CHEBI`, `CHV`, `CSP` +15 more |
| `inverse_belongs_to_cohort` | `KFCOHORT` | `KFGENEBIN`, `KFPT` |
| `belongs_to_cohort` | `KFGENEBIN`, `KFPT` | `KFCOHORT` |

`KFGENEBIN` CodeIDs have the observed form `<symbol>-variant-count`.
Treat this as source-format documentation, not permission to recover gene
identity by splitting a CodeID.

## LINCS

*Small-molecule perturbation signatures*  — 78 triples, 6 predicates.

| Predicate | Subject SABs | Object SABs |
| --- | --- | --- |
| `negatively_regulated_by` | `AOT`, `CHEBI`, `CHV`, `CSP` +15 more | `PUBCHEM` |
| `positively_regulated_by` | `AOT`, `CHEBI`, `CHV`, `CSP` +15 more | `PUBCHEM` |
| `negatively_regulates` | `PUBCHEM` | `AOT`, `CHEBI`, `CHV`, `CSP` +15 more |
| `positively_regulates` | `PUBCHEM` | `AOT`, `CHEBI`, `CHV`, `CSP` +15 more |
| `in_similarity_relationship_with` | `PUBCHEM` | `PUBCHEM` |
| `inverse_in_similarity_relationship_with` | `PUBCHEM` | `PUBCHEM` |

## MOTRPAC

*Exercise response, tissue and sex*  — 42 triples, 6 predicates.

| Predicate | Subject SABs | Object SABs |
| --- | --- | --- |
| `location_of` | `CHV`, `CSP`, `FMA`, `FTU2D` +15 more | `MOTRPAC` |
| `located_in` | `MOTRPAC` | `CHV`, `CSP`, `FMA`, `FTU2D` +15 more |
| `inverse_associated_with` | `ENSEMBL` | `MOTRPAC` |
| `associated_with` | `MOTRPAC` | `ENSEMBL` |
| `sex` | `MOTRPAC` | `PATO` |
| `inverse_sex` | `PATO` | `MOTRPAC` |

MoTrPAC feature CodeIDs have the observed form
`<rat Ensembl gene>-<tissue>-<sex>`. The components are useful for audit and
diagnosis; graph relationships remain the durable identity path.

## MW

*Metabolomics Workbench*  — 8,384 triples, 6 predicates.

| Predicate | Subject SABs | Object SABs |
| --- | --- | --- |
| `produced_by` | `ALT`, `ATC`, `CHEBI`, `CHV` +58 more | `ATC`, `AZ`, `CHV`, `CL` +34 more |
| `produces` | `ATC`, `AZ`, `CHV`, `CL` +34 more | `ALT`, `ATC`, `CHEBI`, `CHV` +58 more |
| `correlated_with_condition` | `ALT`, `ATC`, `CHEBI`, `CHV` +45 more | `CCS`, `CCSR_ICD10CM`, `CHV`, `CSP` +36 more |
| `inverse_correlated_with_condition` | `CCS`, `CCSR_ICD10CM`, `CHV`, `CSP` +36 more | `ALT`, `ATC`, `CHEBI`, `CHV` +45 more |
| `causally_influenced_by` | `ALT`, `ATC`, `CHEBI`, `CHV` +46 more | `CHV`, `EFO`, `ENSEMBL`, `ENTREZ` +10 more |
| `causally_influences` | `CHV`, `EFO`, `ENSEMBL`, `ENTREZ` +10 more | `ALT`, `ATC`, `CHEBI`, `CHV` +46 more |

## NPO

*Neuroscience information*  — 4,190 triples, 14 predicates.

| Predicate | Subject SABs | Object SABs |
| --- | --- | --- |
| `inverse_isa` | `AOT`, `AZ`, `CHEBI`, `CHV` +46 more | `AOT`, `ATC`, `CHEBI`, `CHV` +57 more |
| `isa` | `AOT`, `ATC`, `CHEBI`, `CHV` +57 more | `AOT`, `AZ`, `CHEBI`, `CHV` +46 more |
| `part_of` | `AOT`, `CHEBI`, `CHV`, `CL` +34 more | `AZ`, `CHEBI`, `CHV`, `CL` +33 more |
| `has_part` | `AZ`, `CHEBI`, `CHV`, `CL` +33 more | `AOT`, `CHEBI`, `CHV`, `CL` +34 more |
| `contributes_to_morphology_of` | `CHV`, `CSP`, `EFO`, `FMA` +21 more | `CHV`, `CL`, `CSP`, `EFO` +24 more |
| `inverse_contributes_to_morphology_of` | `CHV`, `CL`, `CSP`, `EFO` +24 more | `CHV`, `CSP`, `EFO`, `FMA` +21 more |
| `inverse_is_part_of` | `CHV`, `CSP`, `FMA`, `FTU2D` +17 more | `ILX`, `NIFSTD.NLX` |
| `is_part_of` | `ILX`, `NIFSTD.NLX` | `CHV`, `CSP`, `FMA`, `FTU2D` +17 more |
| `has_role` | `ILX.TR` | `NIFSTD` |
| `role_of` | `NIFSTD` | `ILX.TR` |
| `delineates` | `PAX.PAXRAT` | `UBERON` |
| `inverse_isdelineatedby` | `PAX.PAXRAT` | `UBERON` |
| `inverse_delineates` | `UBERON` | `PAX.PAXRAT` |
| `isdelineatedby` | `UBERON` | `PAX.PAXRAT` |

## NPOSKCAN

*SPARC anatomical connectivity*  — 5,168 triples, 76 predicates.

| Predicate | Subject SABs | Object SABs |
| --- | --- | --- |
| `part_of` | `AOT`, `CHEBI`, `CHV`, `CL` +42 more | `AZ`, `CHEBI`, `CHV`, `CL` +40 more |
| `has_part` | `AZ`, `CHEBI`, `CHV`, `CL` +40 more | `AOT`, `CHEBI`, `CHV`, `CL` +42 more |
| `inverse_isa` | `AIBS.MUS.LAB`, `AOT`, `AZ`, `CHEBI` +52 more | `AIBS.MUS.LAB`, `ALLENTRANSGENICLINE`, `AOT`, `ATC` +69 more |
| `isa` | `AIBS.MUS.LAB`, `ALLENTRANSGENICLINE`, `AOT`, `ATC` +69 more | `AIBS.MUS.LAB`, `AOT`, `AZ`, `CHEBI` +52 more |
| `contributes_to_morphology_of` | `CHV`, `CSP`, `EFO`, `FMA` +21 more | `CHV`, `CL`, `CSP`, `FMA` +23 more |
| `inverse_contributes_to_morphology_of` | `CHV`, `CL`, `CSP`, `FMA` +23 more | `CHV`, `CSP`, `EFO`, `FMA` +21 more |
| `inverse_hasneurotransmitterphenotype` | `ATC`, `CHEBI`, `CHV`, `CPM` +24 more | `NIFSDT.NLX.CELL`, `NIFSTD`, `NIFSTD.NIFEXT`, `NIFSTD.NLX` +1 more |
| `hasneurotransmitterphenotype` | `NIFSDT.NLX.CELL`, `NIFSTD`, `NIFSTD.NIFEXT`, `NIFSTD.NLX` +1 more | `ATC`, `CHEBI`, `CHV`, `CPM` +24 more |
| `inverse_hasinstanceintaxon` | `CHV`, `CSP`, `LCH_NW`, `LNC` +8 more | `ILX.TR`, `NIFSDT.NLX.CELL`, `NIFSTD`, `NIFSTD.NIFEXT` +2 more |
| `hasinstanceintaxon` | `ILX.TR`, `NIFSDT.NLX.CELL`, `NIFSTD`, `NIFSTD.NIFEXT` +2 more | `CHV`, `CSP`, `LCH_NW`, `LNC` +8 more |
| `inverse_is_part_of` | `CHV`, `CSP`, `FMA`, `FTU2D` +17 more | `ILX`, `NIFSTD.NLX` |
| `is_part_of` | `ILX`, `NIFSTD.NLX` | `CHV`, `CSP`, `FMA`, `FTU2D` +17 more |
| `inverse_hasprojectionphenotype` | `CSP`, `FMA`, `ILX.TR`, `MSH` +6 more | `ILX.TR`, `NIFSDT.NLX.CELL`, `NIFSTD`, `NIFSTD.NIFEXT` +1 more |
| `hasprojectionphenotype` | `ILX.TR`, `NIFSDT.NLX.CELL`, `NIFSTD`, `NIFSTD.NIFEXT` +1 more | `CSP`, `FMA`, `ILX.TR`, `MSH` +6 more |
| `inverse_delineates` | `CHV`, `CSP`, `FBBT`, `FMA` +18 more | `MBA`, `PAX.PAXRAT`, `UBERON` |
| `delineates` | `MBA`, `PAX.PAXRAT`, `UBERON` | `CHV`, `CSP`, `FBBT`, `FMA` +18 more |
| `isdelineatedby` | `CHV`, `CSP`, `FMA`, `HUBMAP` +16 more | `MBA`, `PAX.PAXRAT`, `UBERON` |
| `inverse_isdelineatedby` | `MBA`, `PAX.PAXRAT`, `UBERON` | `CHV`, `CSP`, `FMA`, `HUBMAP` +16 more |
| `hasmolecularphenotype` | `ILX.TR`, `NIFSDT.NLX.CELL`, `NIFSTD`, `NIFSTD.NIFEXT` +2 more | `ILX.TR`, `NIFSTD`, `NIFSTD.NIFEXT`, `NIFSTD.NLX` +2 more |
| `inverse_hasmolecularphenotype` | `ILX.TR`, `NIFSTD`, `NIFSTD.NIFEXT`, `NIFSTD.NLX` +2 more | `ILX.TR`, `NIFSDT.NLX.CELL`, `NIFSTD`, `NIFSTD.NIFEXT` +2 more |
| `inverse_hasmorphologicalphenotype` | `ILX.TR`, `NIFSTD` | `NIFSDT.NLX.CELL`, `NIFSTD`, `NIFSTD.NIFEXT`, `NIFSTD.NLX` +1 more |
| `hasmorphologicalphenotype` | `NIFSDT.NLX.CELL`, `NIFSTD`, `NIFSTD.NIFEXT`, `NIFSTD.NLX` +1 more | `ILX.TR`, `NIFSTD` |
| `hascircuitrolephenotype` | `ILX.TR`, `NIFSDT.NLX.CELL`, `NIFSTD`, `NIFSTD.NIFEXT` +2 more | `ILX.TR` |
| `inverse_hascircuitrolephenotype` | `ILX.TR` | `ILX.TR`, `NIFSDT.NLX.CELL`, `NIFSTD`, `NIFSTD.NIFEXT` +2 more |
| `inverse_ismeasurementof` | `CHV`, `MTH`, `NCBI`, `NCI` +1 more | `ILX.TR` |
| `inverse_hasexpressionphenotype` | `ENTREZ`, `ILX.TR`, `NIFSTD.NIFEXT`, `PR` +1 more | `NIFSTD.NLX`, `NPOKB` |
| `ismeasurementof` | `ILX.TR` | `CHV`, `MTH`, `NCBI`, `NCI` +1 more |
| `hasexpressionphenotype` | `NIFSTD.NLX`, `NPOKB` | `ENTREZ`, `ILX.TR`, `NIFSTD.NIFEXT`, `PR` +1 more |
| `inverse_hasdendritemorphologicalphenotype` | `ILX.TR` | `NIFSTD`, `NIFSTD.NIFEXT`, `NIFSTD.NLX`, `NPOKB` |
| `hasdendritemorphologicalphenotype` | `NIFSTD`, `NIFSTD.NIFEXT`, `NIFSTD.NLX`, `NPOKB` | `ILX.TR` |
| `inverse_labelpartof` | `MBA`, `UBERON` | `MBA`, `UBERON` |
| `labelpartof` | `MBA`, `UBERON` | `MBA`, `UBERON` |
| `inverse_hasdriverexpressioninducedphenotype` | `GETSDS.JSP?MMRRC`, `JAX` | `NPOKB` |
| `inverse_hasdriverexpressionphenotype` | `GETSDS.JSP?MMRRC`, `JAX` | `NPOKB` |
| `hasdriverexpressioninducedphenotype` | `NPOKB` | `GETSDS.JSP?MMRRC`, `JAX` |
| `hasdriverexpressionphenotype` | `NPOKB` | `GETSDS.JSP?MMRRC`, `JAX` |
| `inverse_hasfunctionalcircuitrolephenotype` | `ILX` | `ILX.TR` |
| `annotates` | `ILX.TR` | `ILX.TR` |
| `hasdirectionmappedtopositivex` | `ILX.TR` | `ILX.TR` |
| `hasdirectionmappedtopositivey` | `ILX.TR` | `ILX.TR` |
| `hasdirectionmappedtopositivez` | `ILX.TR` | `ILX.TR` |
| `hasdirection` | `ILX.TR` | `ILX.TR` |
| `hasforwardconnectionphenotype` | `ILX.TR` | `ILX.TR` |
| `hasfunctionalcircuitrolephenotype` | `ILX.TR` | `ILX` |
| `hasinformationinput` | `ILX.TR` | `ILX.TR` |
| `hasinformationoutput` | `ILX.TR` | `ILX.TR` |
| `has_member` | `ILX.TR` | `ILX.TR` |
| `hasoppositedirection` | `ILX.TR` | `ILX.TR` |
| `hasphenotype` | `ILX.TR` | `ILX.TR` |
| `hasresolution` | `ILX.TR` | `ILX.TR` |
| `has_role` | `ILX.TR` | `NIFSTD` |
| `hasspace` | `ILX.TR` | `ILX.TR` |
| `inverse_annotates` | `ILX.TR` | `ILX.TR` |
| `inverse_hasdirectionmappedtopositivex` | `ILX.TR` | `ILX.TR` |
| `inverse_hasdirectionmappedtopositivey` | `ILX.TR` | `ILX.TR` |
| `inverse_hasdirectionmappedtopositivez` | `ILX.TR` | `ILX.TR` |
| `inverse_hasdirection` | `ILX.TR` | `ILX.TR` |
| `inverse_hasforwardconnectionphenotype` | `ILX.TR` | `ILX.TR` |
| `inverse_hasinformationinput` | `ILX.TR` | `ILX.TR` |
| `inverse_hasinformationoutput` | `ILX.TR` | `ILX.TR` |
| `inverse_hasoppositedirection` | `ILX.TR` | `ILX.TR` |
| `inverse_hasphenotype` | `ILX.TR` | `ILX.TR` |
| `inverse_hasresolution` | `ILX.TR` | `ILX.TR` |
| `inverse_hasspace` | `ILX.TR` | `ILX.TR` |
| `inverse_names` | `ILX.TR` | `ILX.TR` |
| `inverse_transforms` | `ILX.TR` | `ILX.TR` |
| `member_of` | `ILX.TR` | `ILX.TR` |
| `names` | `ILX.TR` | `ILX.TR` |
| `transforms` | `ILX.TR` | `ILX.TR` |
| `inverse_hasreporterexpressionphenotype` | `JAX` | `NPOKB` |
| `role_of` | `NIFSTD` | `ILX.TR` |
| `hasbiologicalsex` | `NPOKB` | `PATO` |
| `hasphenotypemodifier` | `NPOKB` | `PATO` |
| `hasreporterexpressionphenotype` | `NPOKB` | `JAX` |
| `inverse_hasbiologicalsex` | `PATO` | `NPOKB` |
| `inverse_hasphenotypemodifier` | `PATO` | `NPOKB` |

## PROTEOFORM

*Glycosylated proteoforms*  — 18 triples, 18 predicates.

| Predicate | Subject SABs | Object SABs |
| --- | --- | --- |
| `inverse_has_amino_acid` | `AMINO.ACID` | `GLYGEN.LOCATION` |
| `citation` | `GLYCOPROTEIN.EVIDENCE` | `GLYGEN.CITATION` |
| `is_evidence_for` | `GLYCOPROTEIN.EVIDENCE` | `GLYCOPROTEIN` |
| `glycosylated_at` | `GLYCOPROTEIN` | `GLYCOSYLATION.SITE` |
| `has_evidence` | `GLYCOPROTEIN` | `GLYCOPROTEIN.EVIDENCE` |
| `has_pro_entry` | `GLYCOPROTEIN` | `GP.ID2PRO` |
| `sequence` | `GLYCOPROTEIN` | `UNIPROTKB.ISOFORM` |
| `has_saccharide` | `GLYCOSYLATION.SITE` | `GLYTOUCAN` |
| `inverse_glycosylated_at` | `GLYCOSYLATION.SITE` | `GLYCOPROTEIN` |
| `location` | `GLYCOSYLATION.SITE` | `GLYGEN.LOCATION` |
| `inverse_citation` | `GLYGEN.CITATION` | `GLYCOPROTEIN.EVIDENCE` |
| `has_amino_acid` | `GLYGEN.LOCATION` | `AMINO.ACID` |
| `inverse_location` | `GLYGEN.LOCATION` | `GLYCOSYLATION.SITE` |
| `inverse_has_saccharide` | `GLYTOUCAN` | `GLYCOSYLATION.SITE` |
| `inverse_has_pro_entry` | `GP.ID2PRO` | `GLYCOPROTEIN` |
| `has_isoform` | `UNIPROTKB` | `UNIPROTKB.ISOFORM` |
| `inverse_has_isoform` | `UNIPROTKB.ISOFORM` | `UNIPROTKB` |
| `inverse_sequence` | `UNIPROTKB.ISOFORM` | `GLYCOPROTEIN` |

## Source modelling idioms

How a source is *shaped*, beyond which SABs it connects. These patterns come
from the DDKG Data Dictionary, the release registries, and live validation on
the December 2025 build. They are the patterns that make a query work or
silently return the wrong column.

### Azimuth (`AZ` and `HMAZ`)

Two sources, and conflating them fails. **`AZ`** carries the cell-type
Concepts — 730 codes — and their `isa` hierarchy linking fine annotation
levels to coarser ones. **`HMAZ`** is edge-only and carries the marker
assertions:

| Predicate | Edges |
| --- | --- |
| `has_marker_gene_in_kidney` | 485 |
| `has_marker_gene_in_liver` | 225 |
| `has_marker_gene_in_heart` | 200 |

Markers run from an `AZ` cell-type Concept to an `HGNC` gene Concept.

**These are label-transfer discriminators, not expression profiles.** Azimuth
selects markers for their power to distinguish cell types during annotation
transfer, so the list is neither comprehensive for a cell type nor a claim
about expression level.

**Azimuth carries model-organism reference atlases**, so constrain or state
species — see `05_entity_resolution.md#species`.

Each organ is a separate predicate, so the whole marker set for one organ is
small enough to enumerate; count first rather than capping.

### DisGeNET (`DGN`)

15.7M edges, all `refers_to` / `inverse_refers_to`, and **the disease does not
connect to genes directly.** It connects to association nodes, which carry the
gene on a second hop.

Association classes observed for one disease anchor, with their relative
volumes:

| Partner SAB | Apparent class |
| --- | --- |
| `DGNV` | variant–disease |
| `DGNGV` | gene–variant |
| `DGNBM` | biomarker |
| `DGNCM` | causal mutation |
| `DGNAGE` | age of onset |
| `DGNGDA` | gene–disease association |
| `DGNTH` | therapeutic |
| `DGNMM` | unresolved |

These labels denote different provisional record classes. `DGNCM` appears
to represent causal-mutation records; `DGNBM`, biomarker records; and
`DGNAGE`, age-of-onset records rather than a generic association. On the
anchor tested, the putative gene–disease association class had only 6
partners, versus 2,196 variant–disease, 1,542 gene–variant, 995 biomarker, and
673 causal-mutation partners.

**Report a DGN result by class, never as a single count.** Collect the
association node's Code SAB alongside the gene:

```cypher
MATCH (d:Concept {CUI:$cui})-[:refers_to {SAB:'DGN'}]-(assoc:Concept)
MATCH (assoc)-[:refers_to {SAB:'DGN'}]-(g:Concept)-[:HAS_CODE]->(gc:Code {SAB:'HGNC'})
WHERE g <> d
MATCH (assoc)-[:HAS_CODE]->(ac:Code)
RETURN gc.CodeID AS gene, collect(DISTINCT ac.SAB) AS assoc_classes,
       count(DISTINCT assoc) AS n_assoc
ORDER BY n_assoc DESC
```

This per-gene class-mix pattern is a hand-over query derived from the observed
topology; the corresponding Tier 7 Stage 3 run remains outstanding.

The internal model of the `DGN*` vocabularies is not documented in the DDKG
User Guide or Data Dictionary. The class names above are inferred from their
partner volumes and abbreviations; treat them as provisional and let the graph
report the topology rather than assuming it.

### GTEx expression (`GTEXEXP`)

A `GTEXEXP` Concept is one gene-tissue measurement. It fans out to three
places, and each carries a different part of the record:

| Predicate | Reaches | Carries |
| --- | --- | --- |
| `expresses` / `expressed_in` | `HGNC` | which gene |
| `expresses` / `expressed_in` | `UBERON` (42 tissue nodes) | **which tissue** |
| `expresses` / `expressed_in` | `EFO` | tissue, for a subset |
| `has_expression` | `EXPBINS` | the TPM value, as a bin |

**`expresses` and `expressed_in` are an inverse pair**, 4,145,472 edges each,
and both connect the measurement Concept to a gene and a tissue.

**But the traversable direction is not symmetric in practice.** On the
December 2025 CSV release, a tissue anchor traverses to its measurements
through `expresses`; binding `expressed_in` from the tissue side returns
nothing and gives no error. Verified in testing, where that binding zeroed a
chain at its first hop.

**So do not bind a single predicate name on this pair.** Either leave the
predicate unbound and pin `{SAB:'GTEXEXP'}` on the relationship, or bind both
names. Disambiguate the endpoints by their Code SAB, which remains reliable.

Where a chain through this pair returns nothing, test the hop in isolation
with the predicate unbound and return `type(r)` before assuming the anchor or
a later hop is at fault.

So a gene-to-tissue query is a fan-out from the measurement Concept, not a
chain through it, and each leg is pinned by the SAB at its far end:

```cypher
MATCH (gene:Concept)-[:HAS_CODE]->(:Code {SAB:'HGNC', CODE:$code})
MATCH (gene)-[gm {SAB:'GTEXEXP'}]-(m:Concept)
WHERE type(gm) IN ['expresses', 'expressed_in']
MATCH (m)-[mt {SAB:'GTEXEXP'}]-(tissue:Concept)-[:HAS_CODE]->(ub:Code {SAB:'UBERON'})
WHERE type(mt) IN ['expresses', 'expressed_in']
OPTIONAL MATCH (m)-[:has_expression {SAB:'GTEXEXP'}]-(b:Concept)-[:HAS_CODE]->(bin:Code {SAB:'EXPBINS'})
RETURN DISTINCT ub.CodeID AS tissue, bin.CodeID AS expression_bin
LIMIT 50
```

TPM is ingested as-is and each measurement additionally carries an edge to the
`EXPBINS` node covering its value — a TPM of 10.5 links to the bin
representing [10,11]. There are 159 bins.

**`EXPBINS` Codes carry no numeric properties**, only `SAB`, `CODE`, `CodeID`.
`bin.lowerbound` returns null for every row. The bound properties were added
to the model after this dataset was ingested, so the bins predate them; the
JKG generation is expected to carry the values properly.

The bounds are visible in the CodeID (`EXPBINS:0.1.0.2` is [0.1, 0.2]).
Do not split that string, but do match on it: enumerate the 159 bins with
`MATCH (c:Code {SAB:'EXPBINS'}) RETURN c.CodeID ORDER BY c.CodeID`, then
select the range wanted with `bin.CodeID IN [...]` or `STARTS WITH`.

So a `GTEXEXP` edge means a measurement exists, and **roughly half of all
gene-tissue pairs sit in the exact-zero bin** — 842,108 of about 1.57M
measurements on the December 2025 release. An unfiltered "expressed in tissue
X" query is therefore around half zeros.

Report a bare `GTEXEXP` edge as "measured", never as "expressed", and apply a
bin filter when the question means expression. Bin structure and occupancy:
`17_gtex_bins_addendum.md`.

**Do not derive tissue by parsing a `GTEXEXP` CodeID.** Traverse to UBERON.

The CodeID does contain the tissue, which is what makes parsing it tempting:

```
GTEXEXP:ENSG00000266203-1-Heart-Atrial-Appendage
GTEXEXP:ENSG00000266203-1-Esophagus-Gastroesophageal-Junction
GTEXEXP:ENSG00000266203-1-Fallopian-Tube
```

The shape is `GTEXEXP:<Ensembl gene ID>-<N>-<Tissue-Name>`, where the tissue
name itself contains hyphens and **`N` varies between genes**. So a parse that
splits on a fixed delimiter works for the genes carrying that value of `N` and
returns null for every other one.

Observed: a query splitting on `-12-` populated the tissue column for two
genes out of two hundred. The other 198 had a different `N`, `split` returned
a one-element list, index `[1]` was null, and `collect` dropped the nulls —
leaving an empty column that reads as missing data rather than a broken parse.

Note also that the gene in the CodeID is an **Ensembl** identifier, not HGNC,
so even the gene half is not what a parse would assume.

Both are avoidable. Traverse: gene identity is the hop to `HGNC`, tissue
identity is the hop to `UBERON`.

#### GTEx heart tissues

Verified: GTEx samples heart at **two** sites.

| UBERON | Terms it carries |
| --- | --- |
| `UBERON:0006566` | left ventricle myocardium, myocardium of left ventricle |
| `UBERON:0006631` | right atrium appendage, heart right atrial appendage, right atrium auricular region |

`UBERON:0004550` is **not** heart — it is the gastroesophageal junction, and
its terms are "cardiac sphincter" and "esophageal-cardiac junction". A filter
matching `'cardiac'` pulls it in, because *cardia* (the stomach opening) and
*cardiac* (of the heart) share a root and name different organs.

This is why anatomy should be selected by enumerated CodeID rather than by
string. Terms are written for humans who know which organ they mean.

Other false friends in the same family: `'atri'` matches atrium and atresia;
`'cardio'` matches cardiomyopathy and cardia; `'hepat'` matches liver terms
and hepatitis; `'renal'` is a substring of `'adrenal'`.

**Organ names also match assays and procedures, not only diseases.** Filtering
conditions on `'kidney'` matches `ALKALINE PHOSPHATASE, LIVER/BONE/KIDNEY
TYPE` — an isoenzyme measurement. Filtering on an organ returns lab tests,
imaging studies, transplant status, and specimen types alongside the diseases.
Return the matched term as an audit column, look at it, then pin the filter to
CodeIDs.

#### Joining loops to genomic features

Verified: loop anchors and eQTLs both attach to **1 kb `HSCLO` bins**, and a
loop anchor attaches to the bin containing its coordinate. So the join is
shared bin membership at that resolution, with no rollup needed:

```cypher
MATCH (bin:Concept)-[:HAS_CODE]->(bin_code:Code {SAB:'HSCLO'})
WHERE bin_code.CodeID STARTS WITH 'HSCLO:chr22.'
MATCH (loop:Concept)-[a:loop_us_start|loop_us_end|loop_ds_start|loop_ds_end {SAB:'4DN'}]->(bin)
MATCH (eqtl:Concept)-[:located_in {SAB:'GTEXEQTL'}]-(bin)
```

**This finds features at loop anchors, not inside loops.** The interior is a
bin-chain walk between `loop_us_end` and `loop_ds_start` using
`precedes_1kbp_band`, which is a much heavier traversal. Anchor coincidence
and interior containment are different biological questions — say which one a
query answers.

`STARTS WITH` on a CodeID is a label scan without indexes, so chromosome
scoping is slow but bounded, and it is the cheap direction compared with
starting from the eQTL side.

#### Loop cell type is three hops away

A loop's biological context is not on the loop. It sits on the `4DND`
dataset: `4DNL` ← `file_has_loop` ← `4DNF` ← `dataset_has_file` ← `4DND` →
`dataset_involves_cell_type`.

So an overlap between a loop and a tissue-specific feature is positional
coincidence until the contexts are checked. Say so when reporting one — the
row gives no hint that the loop and the eQTL may come from unrelated cell
types.

### GTEx eQTL (`GTEXEQTL`)

eQTLs were filtered to those present in every tissue, leaving roughly two
million. P-values are bin Concepts under `PVALUEBINS` (17 bins), the same
shape as `EXPBINS`. Genomic position comes through `HSCLO`.

### GTEx co-expression (`GTEXCOEXP`)

Pearson correlation computed per tissue across the GTEx-HGNC intersection,
with pairs above 0.99 tagged as strongly correlated. So a `GTEXCOEXP` edge
means "correlated above 0.99 in at least one tissue", not a correlation
value — there is no coefficient to filter on.

### Observed CodeID formats

Recorded so nobody has to guess. **These are documentation of why parsing is
unsafe, not an invitation to parse.** Traverse to the vocabulary carrying the
attribute instead.

| SAB | Example | Shape |
| --- | --- | --- |
| `HSCLO` | `HSCLO:chr1.67420001-67421000` | chromosome, then start-end |
| `4DNL` | `4DNL:4DNFICRGVN5L.chr11.47175000-47200000.chr11.47350000-47375000` | source file accession, then both loop anchors |
| `4DNF` | `4DNF:4DNFI3RMWQ85` | file accession, atomic |
| `4DNQ` | `4DNQ:1e-10.1e-10` | q-value bin bounds, scientific notation |
| `GTEXEXP` | `GTEXEXP:ENSG00000266203-1-Heart-Atrial-Appendage` | Ensembl gene, a varying number, tissue with **hyphens** |
| `GTEXEQTL` | `GTEXEQTL:eQTL.chr15.85772872.C.T.b38.Heart.Left.Ventricle` | position, ref, alt, build, tissue with **dots** |
| `EXPBINS` | `EXPBINS:0.1.0.2` | bin bounds [0.1, 0.2] |
| `PVALUEBINS` | `PVALUEBINS:1e-12.1e-11` | bin bounds |
| `KFGENEBIN` | `KFGENEBIN:FLYWCH1-variant-count` | gene symbol, then a fixed suffix |
| `KFPT` | `KFPT:PT-9X741E8Z` | participant accession, atomic |

Four independent reasons these defeat parsing:

**The delimiter is also the decimal point.** `EXPBINS:0.1.0.2` is the bin
[0.1, 0.2]. Splitting on `.` gives four fields, and no rule recovers which
dots are separators — `3.0.4.0` could be [3.0, 4.0] or [3, 0.4, 0]. This is
not a hard parse; it is ambiguous, and `bin.lowerbound` / `bin.upperbound`
exist precisely so nobody attempts it.

**The delimiter appears inside values.** `4DNQ:1e-10.1e-10` and
`PVALUEBINS:1e-12.1e-11` carry hyphens inside exponents and dots inside the
notation, so both candidate separators occur within the fields.

**Components vary between records.** The number in a `GTEXEXP` CodeID differs
by gene, which is why a fixed-delimiter split populated two rows out of two
hundred and left the rest looking like sparse data.

**Conventions differ within one DCC.** GTEx writes tissue as
`Heart-Atrial-Appendage` in `GTEXEXP` and `Heart.Left.Ventricle` in
`GTEXEQTL`. A parser written against one will silently fail on the other.

Where the identity is needed, it is reachable: gene via `HGNC` or `ENSEMBL`,
tissue via `UBERON`, position via `HSCLO`, numeric bounds via `lowerbound`
and `upperbound` on the bin Code.

### 4DN chromatin loops

A `4DNL` Concept is one loop call. Its CodeID embeds the source file and both
anchor intervals, which means a loop is self-describing — and still should not
be parsed. The structure is reachable:

- `4DNF` — the source file the loop came from
- `4DNQ` — the q-value bin for the call
- `HSCLO` — the genomic bins the anchors occupy

Anchors connect to `HSCLO` bins, and `HSCLO` codes are chromosome plus a
1 kb interval (`HSCLO:chr1.67420001-67421000`). Bins chain to one another, so
the span between two anchors is a path rather than an arithmetic comparison,
and the interval a feature occupies is found by shared bin membership rather
than by comparing coordinates.

Consult the User Guide's chromatin-loop query (see
`09_query_task_index.md`) before composing one of these. Choose the coarsest
bin resolution that answers the question: traversing at 1 kb where 100 kb
would do multiplies the path count by roughly a hundred.

### The general rule

**Never parse a `CodeID` to extract meaning — but matching one is fine.**
Splitting a CodeID into fields invents a format, produces empty columns when
it guesses wrong, and fails silently because `split()` on an absent delimiter
yields null rather than an error. Comparing a CodeID against values enumerated
from the graph is exact and safe.

So: `bin.CodeID IN ['EXPBINS:5.0.6.0', ...]` after listing the bins, yes.
`split(gx.CodeID,'-12-')[1]`, no.

Where an attribute is available through a traversal, prefer the traversal —
tissue via `UBERON` rather than either operation on the string.

When a query needs an attribute of a Concept, ask which SAB carries that
attribute and traverse to it. Where the answer is not in `dcc_endpoints.md`,
the Data Dictionary documents the ingestion methodology per source.

## Ingestion scope: what was loaded, and what was not

A source in the graph is rarely the whole source. The DDKG Data Dictionary
records what each ingestion actually took, and the omissions are invisible at
query time — an absent gene set looks identical to a gene set with no members.

State the scope when reporting from a source whose coverage is partial.

### MSIGDB

**Five subsets of MSigDB v7.4 only**: C1 (positional), C2 (curated), C3
(regulatory target), C8 (cell type signature), and H (hallmark). Concept nodes
were created for MSigDB systematic names, **excluding KEGG data**.

Consequences for a pathway query:

- **No KEGG gene sets.** `KEGG_MAPK_SIGNALING_PATHWAY` and its relatives are
  not present, and KEGG is not a source in the release. Offering a
  KEGG-derived superset as the broad-scope option describes something the
  graph does not contain.

  **KEGG nomenclature does survive elsewhere, without KEGG content.** A term
  scan finds ten KEGG-named pathway concepts under `NCI` — `TGF-beta
  Signaling Pathway KEGG`, `p53 Signaling Pathway KEGG`, `mTOR Signaling
  Pathway KEGG` among them. These are NCI Thesaurus concepts carrying KEGG
  labels; membership, where any exists, is NCI's own curation rather than
  KEGG's. The remaining hits are DisGeNET abstract text mentioning KEGG
  analysis (`DGNBM`, `DGNAGE`, `DGNGV`), identifier-type terminology
  (`EDAM`, `MI`), and one substring false friend in `MSH`.

  So "no KEGG" is correct for gene sets and wrong as a statement about the
  string. Anchoring on `NCI:…Signaling Pathway KEGG` yields a pathway concept
  whose membership is not KEGG's.
- **No C5 (GO), C6 (oncogenic signatures), or C7 (immunologic signatures).**
  An MSigDB anchor cannot reach GO biological process sets.
- C2 carries the Reactome-, BioCarta- and PID-derived sets, which is what
  MSigDB pathway names in this graph mostly are.

#### MSigDB C2:CP overlaps REACTOME and WP

C2's canonical-pathways collection is **built from** Reactome, WikiPathways,
BioCarta and PID. The DDKG also loads `REACTOME` and `WP` as sources in their
own right. So the same pathway can be present twice, under two SABs, from one
upstream provider:

| SAB | Example form |
| --- | --- |
| `MSIGDB` | `REACTOME_MAPK3_ERK1_ACTIVATION`, `PID_MAPK_TRK_PATHWAY` |
| `REACTOME` | `R-HSA-` identifiers |
| `WP` | `WP` identifiers |

Two consequences, and the second is the serious one.

**Gene membership may differ between the copies.** MSigDB v7.4 captured
Reactome and WikiPathways at whatever release was current for that MSigDB
build; the DDKG's own `REACTOME` and `WP` ingestions are separate releases.
Whether they agree is a question about two release identifiers, and the graph
carries no equivalence edge between the copies. Selecting both gives the union
of two snapshots, not a larger pathway.

**Multi-source agreement is invalid across them.** Ranking genes by how many
sources assert them treats `MSIGDB` and `REACTOME` as independent evidence.
For a C2:CP set they are one source counted twice, and a gene present in both
looks corroborated when it has simply been redistributed.

**What to do:** pick one representation per pathway rather than both. Where a
result draws on `MSIGDB` alongside `REACTOME` or `WP`, say that the sources
are not independent, and do not count them separately when ranking. If the
release versions matter to the analysis, they need checking upstream — the
graph does not record which Reactome or WikiPathways release either side
came from.

The same caution applies to any redistributing source. A vocabulary that
republishes another's content produces apparent agreement between two SABs
that share an origin.

### IDGP compounds and clinical drug vocabularies do not overlap

**Verified graph-wide: no Concept carries both an IDGP `bioactivity` edge and
a `DRUGBANK`, `RXNORM`, or `ATC` code.** Zero, not few.

The clinical codes are present — roughly 1,292 PubChem Concepts carry RxNorm,
1,150 DrugBank, 748 ATC — and IDGP bioactivity is present. They sit on
disjoint Concept sets. The same molecule presumably appears in both, under
different PubChem CIDs or without a cross-reference merging them, and the
graph records no link.

**So this filter can never return anything:**

```cypher
// always empty, for every protein
MATCH (cmpd:Concept)-[:bioactivity {SAB:'IDGP'}]-(prot:Concept)
MATCH (cmpd)-[:HAS_CODE]->(d:Code) WHERE d.SAB IN ['DRUGBANK','RXNORM','ATC']
```

An empty result there reads as "no approved drug targets this protein" and
means "these two ingestions do not share Concepts". It is a false-negative
generator, and a tempting one, because restricting bioactivity hits to
clinically-coded compounds is the obvious way to answer "which *drugs* target
this".

**What to do:** answer "which drugs target X" from IDGP as *compounds with
measured bioactivity*, and say plainly that the graph cannot distinguish tool
compounds from clinical agents on this route. Do not attempt the clinical
restriction and report its emptiness. If approved-drug status matters, it has
to come from outside the graph, or from a separate query against the clinical
vocabularies that does not pass through IDGP.

### CLINVAR

**v2023-01-05, filtered.** Only genes with pathogenic, likely pathogenic, or
pathogenic/likely pathogenic variants; associations with no assertion criteria
met were excluded. Target phenotypes come through MedGen IDs, reaching MONDO,
HPO and EFO.

So a gene absent from CLINVAR here may have benign or VUS variants only, or
may have submissions without assertion criteria. Absence is not evidence of no
clinical variation.

### LINCS

Each perturbagen links to its **top 25 most up-regulated and top 25 most
down-regulated genes** from the L1000 consensus signatures, plus its top 5
most similar drugs. Roughly 4,419 genes are covered in total.

Most genes therefore have no LINCS edges at all. An empty compound result for
a gene is a coverage finding, not pharmacology.

### GTEXEQTL

Filtered to eQTLs **present in every tissue**, leaving roughly two million.
This is a deliberate, restrictive selection: tissue-specific eQTLs are absent
by construction.

### GTEXCOEXP

Pearson correlation per tissue across the GTEx–HGNC intersection, with pairs
above 0.99 tagged as strongly correlated. An edge means "correlated above 0.99
in at least one tissue", not a coefficient — there is no value to filter on.

### HCOPMP

Mouse gene nodes to Mammalian Phenotype ontology, built from IMPC and MGI —
the mouse counterpart of `HGNCHPO`. Mouse content reachable from a gene query
that does not constrain species.

### Where to check

`sources/` does not include the Data Dictionary, which lives in the project
repository under `DataDistillery29August2025`. Its per-source sections record
version, filtering, and thresholds. Check it before describing what a source
contains — several statements in this skill were corrected by doing so.
