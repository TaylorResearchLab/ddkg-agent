# SAB registry

Derived from the live December 2025 build, not from the User Guide's examples.
**289 node SABs**, **143 edge SABs**, 109 appearing as both.
20,599,990 Code nodes and 186,651,416 relationships in total.

The guide demonstrates 42 of these. The rest are mostly UMLS vocabularies
that no DCC use case happens to touch — real, queryable, and invisible to
anyone working from the examples alone.

Full lists: `assets/node_sabs.csv`, `assets/edge_sabs.csv`.

## Contents

1. [The three populations](#the-three-populations)
2. [Edge-only SABs](#edge-only-sabs)
3. [Largest node SABs](#largest-node-sabs)
4. [Largest edge SABs](#largest-edge-sabs)
5. [Naming traps](#naming-traps)
6. [Singleton SABs](#singleton-sabs)
7. [Licence-sensitive sources](#licence-sensitive-sources)

## The three populations

| Population | Count | Match it as |
| --- | --- | --- |
| Node **and** edge SAB | 109 | either `(c:Code {SAB:'X'})` or `-[r {SAB:'X'}]-` |
| Node only | 180 | `(c:Code {SAB:'X'})` — has no relationships of its own |
| Edge only | 34 | `-[r {SAB:'X'}]-` — **has no Code nodes at all** |

Matching a Code node with an edge-only SAB returns nothing, and the
emptiness is indistinguishable from a biological negative.

## Edge-only SABs

All 34. Never write `(c:Code {SAB:'…'})` for any of these.

| SAB | Edges |
| --- | --- |
| `ERCCREG` | 29,794,186 |
| `DGN` | 15,741,306 |
| `GENCODE` | 3,530,426 |
| `4DN` | 2,589,950 |
| `CMAP` | 2,451,782 |
| `ERCCRBP` | 1,908,926 |
| `HGNCHPO` | 1,314,616 |
| `GENCODEHSCLO` | 1,181,976 |
| `GTEXCOEXP` | 1,078,034 |
| `GLYCANS` | 929,318 |
| `STRING` | 918,992 |
| `PROTEOFORM` | 910,938 |
| `IDGP` | 857,272 |
| `LINCS` | 487,288 |
| `MPMGI` | 438,984 |
| `OTG` | 360,466 |
| `MW` | 157,502 |
| `KF` | 153,380 |
| `HCOP` | 135,868 |
| `CLINVAR` | 123,344 |
| `MONDO_SIMPLE` | 85,410 |
| `RATHCOP` | 84,740 |
| `UBERON_BASE` | 84,422 |
| `UBERONEMAPA` | 26,084 |
| `NPOSKCAN` | 24,334 |
| `IDGD` | 14,572 |
| `NPO` | 7,932 |
| `CLINGEN` | 6,090 |
| `PATO_BASE` | 5,148 |
| `HPOMP` | 2,452 |
| `HMAZ` | 1,820 |
| `GLYCORDF` | 192 |
| `CEDAR_ENTITY` | 88 |
| `GLYCOCOO` | 38 |

## Largest node SABs

| SAB | Codes |
| --- | --- |
| `HSCLO` | 3,431,265 |
| `ENCODE.CCRE.ACTIVITY` | 2,196,935 |
| `GTEXEXP` | 2,073,492 |
| `DGNBM` | 1,705,576 |
| `GTEXEQTL` | 1,270,900 |
| `DGNGV` | 800,444 |
| `NCBI` | 762,055 |
| `DGNV` | 736,241 |
| `DGNAGE` | 638,378 |
| `ENCODE.RBS.150.NO.OVERLAP` | 462,297 |
| `MEDCIN` | 422,303 |
| `SNOMEDCT_US` | 382,258 |
| `MSH` | 355,278 |
| `ENCODE.CCRE` | 342,850 |
| `ENSEMBL` | 336,662 |
| `PUBCHEM` | 336,189 |
| `DBSNP` | 309,035 |
| `LNC` | 297,596 |
| `NDC` | 250,589 |
| `4DNL` | 215,822 |
| `CHEBI` | 202,642 |
| `NCI` | 194,625 |
| `ICD10PCS` | 192,560 |
| `BIOMARKER` | 183,546 |
| `REFSEQ` | 140,124 |
| `RXNORM` | 128,583 |
| `MTHSPL` | 125,690 |
| `GLYGEN.GLYCOSEQUENCE` | 117,146 |
| `OMIM` | 111,086 |
| `FMA` | 104,379 |

Remaining 259 in `assets/node_sabs.csv`.

## Largest edge SABs

| SAB | Edges | Has Code nodes |
| --- | --- | --- |
| `ERCCREG` | 29,794,186 | **no** |
| `DGN` | 15,741,306 | **no** |
| `HSCLO` | 13,724,374 | yes |
| `GTEXEXP` | 12,437,928 | yes |
| `GTEXEQTL` | 8,237,366 | yes |
| `LNC` | 4,020,948 | yes |
| `GENCODE` | 3,530,426 | **no** |
| `SNOMEDCT_US` | 3,020,296 | yes |
| `NCI` | 2,700,740 | yes |
| `4DN` | 2,589,950 | **no** |
| `MSIGDB` | 2,584,008 | yes |
| `MSH` | 2,554,072 | yes |
| `CMAP` | 2,451,782 | **no** |
| `MEDCIN` | 2,288,978 | yes |
| `ERCCRBP` | 1,908,926 | **no** |
| `RXNORM` | 1,660,156 | yes |
| `NCBI` | 1,523,110 | yes |
| `MTHSPL` | 1,333,678 | yes |
| `HGNCHPO` | 1,314,616 | **no** |
| `GENCODEHSCLO` | 1,181,976 | **no** |
| `GTEXCOEXP` | 1,078,034 | **no** |
| `MTH` | 1,070,878 | yes |
| `UNIPROTKB` | 1,020,330 | yes |
| `GLYCANS` | 929,318 | **no** |
| `STRING` | 918,992 | **no** |
| `PROTEOFORM` | 910,938 | **no** |
| `BIOMARKER` | 907,912 | yes |
| `IDGP` | 857,272 | **no** |
| `REACTOME` | 778,778 | yes |
| `CHEBI` | 741,148 | yes |

Remaining 113 in `assets/edge_sabs.csv`.

## Non-human sources

Named in `sources/ubkg_contexts.md`. Exclude these unless cross-species
content is wanted:

| SAB | Content |
| --- | --- |
| `HCOP` | human-to-mouse orthologs |
| `RATHCOP` | human-to-rat orthologs |
| `MPMGI` | mouse genotype-phenotype mapping |
| `EMAPA` | mouse developmental anatomy |
| `MP` | Mammalian Phenotype Ontology |

`REACTOME` is mixed rather than non-human: human entries carry `R-HSA-` and
mouse entries `R-MMU-` under the same SAB.

`PT_EMAPA` and `PT_MP` appear among the term edges, so mouse labels can reach
a query through the lexical layer as well as the assertion layer.

## Naming traps

The SAB is frequently not the DCC's name.

| Expected | Actual |
| --- | --- |
| `GTEX` | `GTEXEXP`, `GTEXEQTL`, and `GTEXCOEXP` (edge-only) — no bare `GTEX` |
| `HPO` | `HP` for nodes; `HGNCHPO` and `HPOMP` are edge-only crosswalks |
| `IDG` | `IDGP` and `IDGD`, both edge-only |
| `ERCC` | `ERCCREG` and `ERCCRBP`, both edge-only |
| `4DN` | `4DN` on edges; nodes are `4DND`, `4DNF`, `4DNL`, `4DNQ` |
| `KF` / `GMKF` | `KF` is edge-only; nodes are `KFPT`, `KFCOHORT`, `KFGENEBIN` |
| `GLYGEN` | split across `GLYTOUCAN`, `GLYGEN.*` nodes and `GLYCANS`, `PROTEOFORM`, `GLYCOCOO`, `GLYCORDF` edges |
| `LINCS` | edge-only; also see `CMAP` |
| `DisGeNET` | `DGN` edge-only; nodes are `DGNBM`, `DGNV`, `DGNGV`, `DGNAGE` and other `DGN*` |
| `UBERON` | `UBERON` nodes; `UBERON_BASE` and `UBERONEMAPA` are edge-only |

When unsure of a spelling, substring-match rather than guessing:

```cypher
MATCH (code:Code) WHERE code.SAB CONTAINS 'GTEX'
RETURN DISTINCT code.SAB
```

## Singleton SABs

48 SABs have exactly one Code node. Several look like ingestion
artefacts rather than sources — `9606` (an NCBI taxon id), `22-RDF-SYNTAX-NS`,
`3B75`, and a set of bare numerics. Treat a singleton SAB as suspect before
building a query around it.

```
0000016542, 127230, 127231, 127232, 127234, 127235, 203750, 22-RDF-SYNTAX-NS, 231670, 246450, 251000, 251110, 3B75, 9606, AIBS.MUS.LAB, CARO, CODAO, DRON, EFO-0000572, EFO-0002009, ERO, FBDV, FLU, FOAF, HAS.PRO.ENTRY, LA2-8, LA3-6, LMHA, LP20607-5, LP6121-0, LP6310-9, LP6368-7, LP6443-8, LP6537-7, LP6562-5, LP75287-0, MOD, MTHCMSFRF, NIFSTD.NLX.ORG, NODE1GMBSNJ22X1, OAE, PAX.PAXSPN, PCO, REPUBLIC, SOUTH, VO, WBLS, ZEA
```

## Licence-sensitive sources

Relevant when advising on a reduced-licence build:

| SAB | Codes | Edges |
| --- | --- | --- |
| `SNOMEDCT_US` | 382,258 | 3,020,296 |
| `DRUGBANK` | 10,903 | 0 |
| `RXNORM` | 128,583 | 1,660,156 |
| `MSH` | 355,278 | 2,554,072 |
| `NCI` | 194,625 | 2,700,740 |
| `LNC` | 297,596 | 4,020,948 |
| `MEDCIN` | 422,303 | 2,288,978 |
| `MTHSPL` | 125,690 | 1,333,678 |
| `ICD10CM` | 98,506 | 215,452 |
| `CPT` | 15,245 | 288,802 |

`SNOMEDCT_US` and `DRUGBANK` together are 393,161 Codes (1.9% of all
Codes) and 3,020,296 relationships (1.6%). A build excluding them loses
clinical-terminology coverage but leaves the DCC contributions intact.
`DRUGBANK` carries Code nodes but asserts no relationships of its own.
