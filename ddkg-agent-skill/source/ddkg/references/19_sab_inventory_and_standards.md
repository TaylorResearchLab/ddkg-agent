# SAB inventory and community standards

This reference answers release-level questions such as:

- How many Code nodes are in each source abbreviation (SAB)?
- How many source-attributed relationships are in each SAB?
- Which SABs are node-only, edge-only, or both?
- Which common biomedical standards, ontologies, vocabularies, and major DDKG datasets are represented?

The complete machine-readable table is `assets/sab_manifest.csv`.

## Counting semantics

An SAB is a **source abbreviation**, but node SABs and edge SABs mean different things.

- A node SAB is stored on a `Code` node: `(c:Code {SAB:'...'})`.
- An edge SAB is stored on a source-attributed relationship: `-[r {SAB:'...'}]-`.
- `Concept` nodes are shared integration objects. They do **not** belong to one SAB, so "nodes in an SAB" should be reported as **Code nodes in that SAB**, not Concepts.
- Structural and lexical relationships such as `HAS_CODE`, `HAS_TERM`, `HAS_SEMANTIC`, and `HAS_DEFINITION` may have no SAB and are therefore outside per-SAB edge totals.
- Many biological assertions are stored as inverse pairs. The edge counts below are **stored Neo4j relationships**, not necessarily counts of unique biological assertions.

Do not interpret an edge-only SAB returning zero Code nodes as absence of that source.

## Release-wide accounting

Validated on `DataDistillery_2025_04_DEC` on 8 October 2026:

| Quantity | Count |
| --- | ---: |
| Code nodes | 20,599,990 |
| Code nodes with an SAB | 20,599,990 |
| Code nodes without an SAB | 0 |
| Source-attributed relationships with an SAB | 131,710,076 |
| Relationships without an SAB | 54,941,340 |
| Total relationships | 186,651,416 |
| Node SABs | 289 |
| Edge SABs | 143 |
| SABs present as both node and edge sources | 109 |
| Node-only SABs | 180 |
| Edge-only SABs | 34 |
| Distinct SAB labels across nodes or edges | 323 |

The two validation queries were:

```cypher
MATCH (c:Code)
RETURN
    count(*) AS all_code_nodes,
    count(c.SAB) AS code_nodes_with_sab,
    count(*) - count(c.SAB) AS code_nodes_without_sab
```

```cypher
MATCH ()-[r]->()
RETURN
    count(*) AS all_relationships,
    count(r.SAB) AS relationships_with_sab,
    count(*) - count(r.SAB) AS relationships_without_sab
```

## Full SAB manifest

`assets/sab_manifest.csv` has one row for every SAB appearing on a Code node or source-attributed relationship.

Columns:

| Column | Meaning |
| --- | --- |
| `sab` | Source abbreviation stored in DDKG |
| `code_node_count` | Number of `Code` nodes carrying that SAB |
| `source_edge_count` | Number of relationships carrying `r.SAB = sab` |
| `presence` | `node_only`, `edge_only`, or `both` |
| `common_name` | Curated expansion for commonly used standards/resources |
| `resource_class` | Curated class such as community ontology, clinical standard, research resource, Common Fund dataset, or DDKG bridge |
| `domain` | Broad scientific domain |
| `common_standard_or_vocabulary` | `yes` for common standards/ontologies/vocabularies; otherwise `no` |
| `notes` | Short interpretation note where curated |

The descriptive annotation is deliberately selective. A blank or `other_or_unclassified` entry means this resource has not curated the expansion, **not** that the SAB is unimportant or invalid.

## Common community standards and vocabularies represented

The DDKG includes many widely used community standards and biomedical vocabularies. Selected examples are below.

### Clinical terminology and coding

| SAB | Standard/vocabulary | Code nodes | Source-attributed edges |
| --- | --- | ---: | ---: |
| `SNOMEDCT_US` | SNOMED CT US Edition | 382,258 | 3,020,296 |
| `MSH` | Medical Subject Headings (MeSH) | 355,278 | 2,554,072 |
| `NCI` | NCI Thesaurus | 194,625 | 2,700,740 |
| `RXNORM` | RxNorm | 128,583 | 1,660,156 |
| `LNC` | LOINC | 297,596 | 4,020,948 |
| `ICD10CM` | ICD-10-CM | 98,506 | 215,452 |
| `ICD10PCS` | ICD-10-PCS | 192,560 | 385,118 |
| `CPT` | Current Procedural Terminology | 15,245 | 288,802 |
| `HCPCS` | Healthcare Common Procedure Coding System | 7,925 | 20,272 |
| `ATC` | Anatomical Therapeutic Chemical Classification | 6,897 | 13,608 |
| `NDC` | National Drug Code | 250,589 | 0 |
| `MED-RT` | Medication Reference Terminology | 3,640 | 172,998 |

### Disease, phenotype, anatomy, and cell ontologies

| SAB | Standard/vocabulary | Code nodes | Source-attributed edges |
| --- | --- | ---: | ---: |
| `OMIM` | Online Mendelian Inheritance in Man | 111,086 | 534,874 |
| `HP` | Human Phenotype Ontology | 20,730 | 51,414 |
| `MONDO` | Mondo Disease Ontology | 27,575 | 0 |
| `DOID` | Disease Ontology | 12,000 | 42,478 |
| `ORDO` | Orphanet Rare Disease Ontology | 15,348 | 98,768 |
| `EFO` | Experimental Factor Ontology | 16,424 | 193,336 |
| `UBERON` | Uberon | 14,671 | 0 |
| `FMA` | Foundational Model of Anatomy | 104,379 | 366,852 |
| `CL` | Cell Ontology | 3,232 | 19,946 |
| `MP` | Mammalian Phenotype Ontology | 14,515 | 239,828 |
| `EMAPA` | Mouse developmental anatomy | 8,004 | 44,560 |

### Genes, proteins, sequence, chemicals, and pathways

| SAB | Standard/vocabulary | Code nodes | Source-attributed edges |
| --- | --- | ---: | ---: |
| `HGNC` | HUGO Gene Nomenclature Committee | 44,245 | 0 |
| `ENSEMBL` | Ensembl | 336,662 | 0 |
| `REFSEQ` | NCBI RefSeq | 140,124 | 0 |
| `DBSNP` | dbSNP | 309,035 | 0 |
| `GO` | Gene Ontology | 40,278 | 238,658 |
| `UNIPROTKB` | UniProtKB | 38,180 | 1,020,330 |
| `REACTOME` | Reactome | 29,197 | 778,778 |
| `CHEBI` | ChEBI | 202,642 | 741,148 |
| `PUBCHEM` | PubChem | 336,189 | 0 |
| `PR` | Protein Ontology | 5,353 | 0 |
| `MI` | Molecular Interactions Ontology | 1,474 | 3,330 |
| `SO` | Sequence Ontology | 18 | 0 |
| `UO` | Units of Measurement Ontology | 574 | 1,348 |
| `OBI` | Ontology for Biomedical Investigations | 3,973 | 21,310 |
| `EDAM` | EDAM bioinformatics ontology | 2,403 | 8,200 |

## Major DDKG and NIH/Common Fund data resources

These are not all "community standards", but they are major scientific resources represented by SABs and are often what a DDKG user means by source.

| SAB | Resource | Code nodes | Source-attributed edges | Notes |
| --- | --- | ---: | ---: | --- |
| `GTEXEXP` | GTEx expression | 2,073,492 | 12,437,928 | expression measurements |
| `GTEXEQTL` | GTEx eQTL | 1,270,900 | 8,237,366 | eQTL records |
| `GTEXCOEXP` | GTEx co-expression | 0 | 1,078,034 | edge-only |
| `4DN` | 4D Nucleome | 0 | 2,589,950 | edge SAB; nodes use separate 4DN* SABs |
| `HUBMAP` | HuBMAP | 733 | 4,548 | atlas/resource identifiers |
| `MOTRPAC` | MoTrPAC | 8,571 | 51,424 | exercise molecular transducers |
| `KF` | Kids First | 0 | 153,380 | edge-only; nodes use KF* SABs |
| `MW` | Metabolomics Workbench | 0 | 157,502 | edge-only |
| `LINCS` | LINCS | 0 | 487,288 | edge-only |
| `IDGP` | Illuminating the Druggable Genome | 0 | 857,272 | edge-only |
| `DGN` | DisGeNET | 0 | 15,741,306 | edge-only; DGN* association vocabularies carry nodes |
| `MSIGDB` | Molecular Signatures Database | 9,990 | 2,584,008 | gene sets/signatures |
| `STRING` | STRING | 0 | 918,992 | edge-only interactions |
| `CLINVAR` | ClinVar | 0 | 123,344 | edge-only assertions |
| `CLINGEN` | ClinGen | 0 | 6,090 | edge-only assertions |
| `MPMGI` | MGI/IMPC mouse genotype-phenotype | 0 | 438,984 | edge-only |
| `HCOP` | HCOP orthology | 0 | 135,868 | edge-only |
| `HRA` | Human Reference Atlas | 1,473 | 53,276 | atlas content |
| `SENNET` | SenNet | 737 | 4,564 | Cellular Senescence Network |

## Naming traps

A dataset name is not always its SAB.

- There is no bare `GTEX`: use `GTEXEXP`, `GTEXEQTL`, or edge-only `GTEXCOEXP`.
- HPO nodes use `HP`; `HGNCHPO` and `HPOMP` are edge-only association/crosswalk sources.
- `4DN` is an edge SAB; node SABs include `4DND`, `4DNF`, `4DNL`, and `4DNQ`.
- `KF` is edge-only; node SABs include `KFPT`, `KFCOHORT`, and `KFGENEBIN`.
- DisGeNET uses edge-only `DGN` plus several `DGN*` node vocabularies.
- GlyGen content is distributed across several node and edge SABs rather than a single `GLYGEN` SAB.

Always inspect the manifest before constructing a query around a guessed source name.

## Regenerating the counts

Node counts:

```cypher
MATCH (c:Code)
RETURN c.SAB AS sab, count(*) AS code_node_count
ORDER BY code_node_count DESC, sab
```

Edge counts:

```cypher
MATCH ()-[r]->()
WHERE r.SAB IS NOT NULL
RETURN r.SAB AS sab, count(*) AS source_edge_count
ORDER BY source_edge_count DESC, sab
```

The two result tables can be outer-joined on SAB to regenerate the count columns of `assets/sab_manifest.csv`.

## Reporting rule

When answering "how many nodes and edges are in each SAB", report the count semantics with the table:

> Node counts are Code nodes carrying that SAB. Edge counts are stored relationships carrying that SAB. Concepts are shared across sources and are not assigned to one SAB. Structural/lexical relationships without an SAB are reported separately. Because inverse assertions may be materialized in both directions, stored edge counts are not necessarily counts of unique biological assertions.

That note is part of the scientific answer, not optional bookkeeping.
