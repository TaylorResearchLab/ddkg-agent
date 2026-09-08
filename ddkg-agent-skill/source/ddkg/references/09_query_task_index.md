# Query task index

The 51 queries in `10_query_examples.md` were extracted from the DDKG User
Guide and were known to run on the guide's build. They are **not all validated
against the December 2025 target release**. The later campaign recorded legacy
forms that failed or hung, so consult `16_manuscript_validated_queries.md`
first and use this index as a historical pattern catalogue. A current-release
validated pattern adapted beats a fresh composition; a guide example still
requires the release-specific rules in references 13 and 15.

Numbers refer to the position of the query within its section in
`10_query_examples.md`, listed here in file order.

## Start here for common tasks

| I want to... | Query |
| --- | --- |
| **Find a gene by its symbol** | **24, anchor fragment only** — `(:Code {SAB:'HGNC'})-[:ACR]->(:Term {name:'ALOX5'})`. `ACR` carries the symbol; do not reuse the later CodeID parsing from the full legacy query. |
| Get a gene's tissue expression | 42; manuscript Q04/Q07 patterns. Query 18 is a legacy direct form and is not preferred for the target release. |
| Get expression values, not just presence | 42 (EXPBINS). Query 24's `ACR` anchor is useful, but its CodeID tissue parsing is not. |
| Find eQTLs with p-value thresholds | 43 (PVALUEBINS) |
| Find compounds that regulate a gene | 46, 20, 21 (LINCS) |
| Find compound-protein bioactivity | 16, 23 (IDGP) |
| Find compound-disease indications | 17, 20 (IDGD) |
| Go from gene to phenotype | 21, 45 |
| Find what connects two vocabularies | 9, 11 (unbound), 10 (bound) |
| See a Concept's whole neighbourhood | 12, 13 |
| Work with chromatin loops | 37 (4DN full model) |
| Work with regulatory elements | 33-36, 39 (ENCODE cCRE) |
| Work with RNA-binding protein sites | 29-32, 38 (ERCC) |
| Work with glycans or glycosylation | 40, 41, 27 |
| Work with Kids First cohorts | 45 |
| Work with exercise response | 25, 47 (MoTrPAC) |
| Work with metabolites | 48, 14 (MW) |
| Find cell-type marker genes | 44 (Azimuth) |
| Make a slow query fast | 50 vs 51 — anchor on the smaller side |

## Every query

| # | Section | Task | Sources |
| --- | --- | --- | --- |
| 1 | Introduction / The simplest way to | List Codes for a source — Anchor on SAB, return Codes | `HGNC` |
| 2 | Introduction / The simplest way to | Count nodes by label — Graph size and shape |  |
| 3 | Introduction / The simplest way to | Codes with a property filter — Narrowing a Code scan | `HGNC` |
| 4 | Introduction / The simplest way to | List relationship types — Discover the predicate vocabulary |  |
| 5 | Introduction / The simplest way to | Count relationships by type — Predicate volumes |  |
| 6 | Introduction / The simplest way to | Code to Concept — The HAS_CODE hop | `HGNC` |
| 7 | Introduction / The simplest way to | Code to preferred Term — Descriptive name via PT | `HGNC` |
| 8 | Introduction / The simplest way to | Concept to all its Terms — Every label on a Concept | `HGNC` |
| 9 | Introduction / The simplest way to | Cross-vocabulary hop, unbound predicate — HGNC to GO, exploratory | `HGNC`, `GO` |
| 10 | Introduction / The simplest way to | Cross-vocabulary hop, bound predicate + SAB — HGNC to GO via process_involves_gene{NCI} | `HGNC`, `GO`, `NCI` |
| 11 | Introduction / The simplest way to | Cross-vocabulary, count by predicate — What connects two sources | `HGNC`, `GO` |
| 12 | Introduction / The simplest way to | Gene to any connected vocabulary — Open-ended neighbourhood | `HGNC` |
| 13 | Introduction / The simplest way to | Neighbourhood with readable labels — Terms on both ends | `HGNC` |
| 14 | DCC Use Cases / IDG and Metabolomi | Gene to metabolite to condition — IDG + MW, four hops | `HGNC`, `UNIPROTKB`, `PUBCHEM`, `IDGP` |
| 15 | DCC Use Cases / IDG and Metabolomi | Same, with counts — Aggregated form of 14 | `HGNC`, `UNIPROTKB`, `PUBCHEM`, `IDGP` |
| 16 | DCC Use Cases / Illuminating the D | Compound to protein bioactivity — IDGP core pattern | `PUBCHEM`, `UNIPROTKB`, `IDGP` |
| 17 | DCC Use Cases / Illuminating the D | Compound to disease indication — IDGD core pattern | `PUBCHEM`, `SNOMEDCT_US`, `IDGD` |
| 18 | DCC Use Cases / Illuminating the D | Gene to tissue expression — GTEXEXP core pattern | `HGNC`, `GTEXEXP` |
| 19 | DCC Use Cases / Illuminating the D | Compound to protein to gene to tissue — IDG + GTEx chain | `PUBCHEM`, `UNIPROTKB`, `HGNC`, `GTEXEXP` |
| 20 | DCC Use Cases / Illuminating the D | Compound indication to regulated genes — IDGD + LINCS | `PUBCHEM`, `SNOMEDCT_US`, `HGNC`, `IDGD` |
| 21 | DCC Use Cases / Illuminating the D | Compound to gene to phenotype — LINCS + HPO | `PUBCHEM`, `HGNC`, `HP`, `LINCS` |
| 22 | DCC Use Cases / Illuminating the D | Same, aggregated — Counts form of 21 | `PUBCHEM`, `HGNC`, `HP`, `LINCS` |
| 23 | DCC Use Cases / Illuminating the D | Protein bioactivity partners — From the protein side | `UNIPROTKB`, `IDGP` |
| 24 | DCC Use Cases / Illuminating the D | **Gene symbol to expression bins** — ALOX5 by name via ACR; the canonical symbol lookup | `HGNC`, `GTEXEXP`, `EXPBINS` |
| 25 | DCC Use Cases / MoTrPAC, LINCS and | Exercise response to human ortholog to tissue — MoTrPAC + GTEx + LINCS | `MOTRPAC`, `HGNC`, `GTEXEXP`, `LINCS` |
| 26 | DCC Use Cases / MoTrPAC, LINCS and | Same, aggregated — Counts form of 25 | `MOTRPAC`, `HGNC`, `GTEXEXP`, `LINCS` |
| 27 | DCC Use Cases / GlyGen, KF and GTE | Glycan enzyme to gene to expression — GlyGen + KF + GTEx | `GLYCANS`, `HGNC`, `KFGENEBIN`, `GTEXEXP` |
| 28 | DCC Use Cases / GlyGen, KF and GTE | Same, aggregated — Counts form of 27 | `GLYCANS`, `HGNC`, `KFGENEBIN`, `GTEXEXP` |
| 29 | DCC Use Cases / ERCC — RBP | RBP binding site to transcript — ERCC RBP chain | `ERCCRBP` |
| 30 | DCC Use Cases / ERCC — RBP | RBP variants — Alternate ERCC RBP form | `ERCCRBP` |
| 31 | DCC Use Cases / ERCC — RBP | RBP with tissue correlation — ERCC RBP + expression | `ERCCRBP` |
| 32 | DCC Use Cases / ERCC — RBP | RBP correlated in tissue — Full ERCC RBP pattern | `ERCCRBP` |
| 33 | DCC Use Cases / ERCC — Regulatory  | cCRE to activity — ENCODE regulatory elements | `ENCODE.CCRE` |
| 34 | DCC Use Cases / ERCC — Regulatory  | cCRE activity in genomic location — cCRE + HSCLO | `ENCODE.CCRE`, `HSCLO` |
| 35 | DCC Use Cases / ERCC — Regulatory  | cCRE by chromatin mark — CTCF / H3K27ac / H3K4me3 | `ENCODE.CCRE.CTCF` |
| 36 | DCC Use Cases / ERCC — Regulatory  | Regulatory element to regulated gene — ERCCREG to ENSEMBL | `ENSEMBL`, `ERCCREG` |
| 37 | Queries to reproduce the Data Dict | Chromatin loop full model — 4DN dataset to file to loop to bins | `4DND`, `4DNF`, `4DNL`, `4DNQ` |
| 38 | Queries to reproduce the Data Dict | RBP site reproduction query — Data dictionary counts for ERCCRBP | `ERCCRBP`, `ENSEMBL`, `UBERON` |
| 39 | Queries to reproduce the Data Dict | cCRE reproduction query — Data dictionary counts for ERCCREG | `ENCODE.CCRE`, `CLINGEN.ALLELE.REGISTRY` |
| 40 | Queries to reproduce the Data Dict | Glycosylation site model — GlyGen proteoform structure | `GLYCOPROTEIN`, `GLYCOSYLATION.SITE`, `AMINO.ACID` |
| 41 | Queries to reproduce the Data Dict | Glycan structure model — GlyGen glycan structure | `GLYCANS`, `GLYCAN.MOTIF` |
| 42 | Queries to reproduce the Data Dict | Expression with bins — GTEx expression + EXPBINS + UBERON | `HGNC`, `GTEXEXP`, `EXPBINS`, `UBERON` |
| 43 | Queries to reproduce the Data Dict | eQTL with p-value bins — GTEx eQTL + PVALUEBINS | `GTEXEQTL`, `HGNC`, `PVALUEBINS`, `UBERON` |
| 44 | Queries to reproduce the Data Dict | Azimuth cell-type marker genes — AZ marker genes per organ | `AZ`, `HGNC`, `HMAZ` |
| 45 | Queries to reproduce the Data Dict | Kids First cohort to gene to phenotype — KF full chain | `KFPT`, `KFCOHORT`, `KFGENEBIN`, `HGNC` |
| 46 | Queries to reproduce the Data Dict | Compound-gene regulation and similarity — LINCS full model | `PUBCHEM`, `HGNC`, `LINCS` |
| 47 | Queries to reproduce the Data Dict | MoTrPAC exercise, sex-stratified — MOTRPAC + PATO sex | `MOTRPAC`, `HGNC`, `ENSEMBL`, `PATO` |
| 48 | Queries to reproduce the Data Dict | Metabolite to gene and condition — MW full model | `HGNC`, `MW` |
| 49 | Queries to reproduce the Data Dict | SPARC neuroscience hierarchy — NPO / ILX isa | `ILX`, `NPO` |
| 50 | Tips and Tricks | Anchor on the smaller side — Performance idiom, ~20x | `HP` |
| 51 | Tips and Tricks | Anchor on the larger side — Slow counter-example | `HP` |

## Why this index exists

These queries were extracted mechanically and then not read. The gene-symbol
lookup in query 24 sat unused while the same problem was solved from scratch
against the live graph. Counting queries is not reading them.
