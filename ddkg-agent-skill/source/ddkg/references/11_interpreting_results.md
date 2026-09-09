# Interpreting results

A DDKG result is not self-explanatory. The same query shape returns curated
causal claims from one source and literature co-mention from another, and
nothing in the output distinguishes them. Users asking these questions are
usually domain experts in biology and newcomers to how NIH organises its
data — they will read a gene list as a gene list.

**So state the caveat unprompted.** Someone who sees a generic `DGN`
`refers_to` edge cannot know whether its association node represents a
variant–disease record, biomarker, causal mutation, age-of-onset assertion, or
another class. Naming the limitation is part of answering, not a hedge
appended to it.

Each section below marks what is **confirmed** against the graph versus what
is **inferred** and still worth verifying.

**Every observed result in this file is a single instance.** They are here to
show what a failure mode looks like, never to be quoted back as an answer.
Gene lists, source lists, classifications, and which entities pass a filter
all depend on the anchor, the threshold, and the build — and all of them
change. Cite the mechanism; get the values from the user's run.

## Contents

1. [Absence has several meanings](#absence-has-several-meanings)
2. [MTHU codes: UMLS coined the identifier](#mthu-codes-umls-coined-the-identifier)
3. [Umbrella concepts and subtype entries](#umbrella-concepts-and-subtype-entries)
4. [What each evidence type actually asserts](#what-each-evidence-type-actually-asserts)
5. [IDGP bioactivity is attributed at assay level](#idgp-bioactivity-is-attributed-at-assay-level)
6. [CLINGEN carries its own confidence — and it can be negative](#clingen-carries-its-own-confidence--and-it-can-be-negative)
7. [Adult expression data censors developmental genes](#adult-expression-data-censors-developmental-genes)
5. [Multi-source agreement is the signal](#multi-source-agreement-is-the-signal)
6. [One Code, several Concepts](#one-code-several-concepts)
7. [Fan-out is not breadth](#fan-out-is-not-breadth)
8. [What to say in an answer](#what-to-say-in-an-answer)

## Absence has several meanings

**Confirmed.** An empty result can mean any of these, and they are not
distinguishable without checking:

| Meaning | How to tell |
| --- | --- |
| The entity did not resolve | Anchor profile returns nothing at all |
| The source has no data for this entity | Profile returns other sources but not this one |
| The source organises the domain differently | The concept resolves to an `MTHU` code, or only to broad vocabularies |
| The relationship genuinely is not asserted | Profile shows the source present with other predicates |

Worked example. A gene may have edges from a dozen sources and none from the
one the question needs. That is a coverage finding, reportable as it stands.

What to say: hand over the profile query, name which source would have to be
present, and set up how to read either outcome. Do not state which sources
will be there.

## MTHU codes: UMLS coined the identifier

**Confirmed in structure, inferred in consequence.** A `CodeID` of the form
`OMIM:MTHU036339` is not an OMIM accession. `MTHU` prefixes are assigned by
the UMLS Metathesaurus when a source contributes a term without its own
identifier for it.

Real OMIM entries are six-digit MIM numbers, so an `MTHU` code means UMLS
created a placeholder — **not** that the import failed or that the source
lacks relevant content.

This is the tell that a source holds the material under different, more
specific codes. To find them:

```cypher
MATCH (c:Code {SAB:'OMIM'})-[tr]->(t:Term)
WHERE toLower(t.name) CONTAINS 'atrial septal defect'
RETURN c.CodeID, c.CODE, type(tr) AS term_edge, t.name
ORDER BY c.CODE
LIMIT 30
```

What to say: this source does not have an entry for the concept as asked,
because it organises the area differently — here are its specific entries.

## Umbrella concepts and subtype entries

**Confirmed for OMIM's structure; the general pattern is inferred.**
Vocabularies differ in granularity, and a query anchored at one level misses
content held at another.

OMIM catalogues numbered subtype entries, each a distinct MIM number, rather
than one umbrella disease. HPO and MONDO carry umbrella terms. So a query
anchored on an umbrella concept can find HPO and MONDO annotations and appear
to show OMIM missing.

The fix is to traverse the vocabulary's own hierarchy from the umbrella
before concluding anything:

```cypher
MATCH (umbrella:Concept {CUI:$cui})-[r:isa|inverse_isa]-(sub:Concept)
MATCH (sub)-[:HAS_CODE]->(c:Code)
RETURN DISTINCT c.SAB, c.CodeID, r.SAB AS hierarchy_source
LIMIT 50
```

What to say: this concept has subtypes, and some sources annotate at the
subtype level only.

## What each evidence type actually asserts

**Scale is relative and drifts between builds; check `assets/predicates.csv`
for current counts. The interpretations are the sources' own documented
semantics, not derived from this graph.** These differ enormously in what
they mean, and the difference is invisible in a result set.

| Source | Predicate | Scale | What it means |
| --- | --- | --- | --- |
| `DGN` | `refers_to` | very large | DisGeNET uses generic relationship names through `DGN*` association Concepts rather than direct disease-to-gene edges. The association-node SAB distinguishes eight provisional classes, including variant–disease, biomarker, causal mutation, age of onset, gene–disease association, and therapeutic records. Report by class rather than flattening them into one literature-co-occurrence count or one causal claim — see `08_dcc_endpoints.md#disgenet-dgn`. Large in the graph overall, which says nothing about whether it covers any particular entity. |
| `HGNCHPO` | `associated_with` | large | Gene-to-phenotype annotation. A gene is included when it causes **any** syndrome featuring that phenotype, so syndromic genes flood in alongside organ-specific ones. |
| `MPMGI` | `involved_in` | moderate | Mouse genotype-phenotype from MGI and IMPC. **Knockout or mutant-allele evidence**: a mouse with a disrupted allele displays the phenotype. Not expression, not association. Report as loss-of-function phenotype space. |
| `HCOP` | `in_1_to_1_orthology_relationship_with` | moderate | HCOP exposes only the relation named **1:1 orthology**; a human gene without such an assertion drops out silently, so absence is a mapping artefact rather than a biological negative. At DDKG Concept grain, merged identifiers can still make returned mappings fan to family-level partners — see `18_row_multiplicity_and_identity_sinks.md#9-two-orthology-cautions`. Diff returned genes against the input list and inspect the returned Codes before calling a pair strictly one-to-one. |
| `MSIGDB` | `pathway_associated_with_gene` | large | Pathway membership, as curated by the gene set. Membership, not mechanism. |
| `OTG` | `has_variant_associated_with_disease` | moderate | Open Targets Genetics, GWAS-derived. Statistical association at variant level. |
| `CLINVAR` | `gene_associated_with_disease_or_phenotype` | small | Clinical variant submissions. Closer to curated causation, and much narrower. |
| `OMIM` | `allelic_variant_of` | small | Catalogued allelic variants. Curated, subtype-level. |
| `IDGP` | `bioactivity` | moderate | A measured assay result — IC50, Kd, Ki — linking a compound to a protein. Attribution is assay-level, so the compound may act elsewhere in the pathway. See below. |
| `CLINGEN` | `gene_disease_validity`, the actionability tiers, the inheritance predicates | small | Expert-panel curation. **The highest-stringency gene-disease source in the build.** `evidence_class` is mandatory here and carries the classification — definitive, strong, moderate, limited. A gene appearing under CLINGEN has been formally adjudicated, which nothing else in this table can claim. |
| `MEDLINEPLUS` | `related_to`, `has_associated_condition` | small | Consumer health information. Editorially curated for patients, not research-grade evidence. Useful for lay-readable framing, weak as support for a gene-disease claim. |
| `ORDO` | `disease_causing_germline_mutation_s__in` | very small | Orphanet rare-disease curation. Explicitly causal, very narrow. |

Worked example. A phenotype query drawing on `HGNCHPO` returns genes whose
associated syndromes feature the phenotype — which includes genes for
multi-system syndromes that happen to involve it, alongside genes of the
affected process. Reported as "genes associated with X" that list misleads;
reported as "genes whose associated syndromes include X" it is accurate.

What to say: name the evidence type in the answer, not just the gene list.

### IDGP bioactivity is attributed at assay level

`bioactivity` records that a compound was measured in an assay associated
with a protein, with `evidence_class` carrying the assay type — `IC50`, `Kd`,
`Ki`. What it does not carry is the compound's molecular target within the
pathway.

Observed once, as an illustration: IDGP bioactivity for the SHH protein
returned jervine, cyclopamine, and vismodegib with IC50 and Kd values. Do not
report those compounds as the answer to a future SHH query — coverage changes,
and the point here is the attribution level, not the hit list. These are canonical Hedgehog
inhibitors, and they act on **SMO**, a downstream receptor, rather than on the
SHH ligand itself. Pathway-level assays are attributed to the pathway's named
protein.

**This is the right answer to "what compounds regulate this gene's pathway"
and the wrong answer to "what compounds bind this protein."** Which one the
user asked matters, and the graph does not distinguish them.

**What to say:** report the hits, and note that the attribution is
assay-level — a compound may act at any point in the pathway rather than on
the named protein. Where the user needs direct molecular targets, suggest
re-anchoring on the specific receptor or enzyme.

### CLINGEN carries its own confidence — and it can be negative

Most sources leave stringency to be inferred from which source they are.
CLINGEN states it: `evidence_class` is mandatory on `gene_disease_validity`,
the four actionability tiers, and the inheritance predicates, and it holds the
expert panel's classification.

`evidence_class` is **heterogeneous across sources** — numeric strings on
LINCS, assay types on IDGP, expert classifications on CLINGEN. What follows
applies to CLINGEN's values only; do not carry it to another source's use of
the same property.

**The classification is not always support.** Observed values include
`Moderate`, `Limited`, and `Disputed`; the ClinGen framework also defines
`Definitive`, `Strong`, and `Refuted`. `Limited` means the panel found minimal
evidence. `Disputed` means the gene-disease relationship has been contested —
the panel looked and came away doubting it.

So CLINGEN's position at the top of the stringency ordering is a statement
about how carefully the assessment was made, **not** about whether it was
favourable. Reporting "supported by CLINGEN" for a `Disputed` gene reverses
the finding.

Observed once: a congenital-heart-defect query returned `HAND2` as Moderate,
`ADAM17`, `BMPR2`, `CRELD1` and `ACVR1` as Limited, and `ATE1` as Disputed.
Ranked on source count alone, `ATE1` sat among genes with real support.

Those classifications are an illustration of the range of values, **not a
lookup table**. Panels revise their calls, and the values depend on the
gene-disease pair being assessed. Never report a gene's CLINGEN class from
this file; read it from `evidence_class` in the user's result.

So where CLINGEN appears, **return `evidence_class`, report the classification
in words, and do not let a `Disputed` or `Limited` gene rank on source count
as though the sources agreed.** A negative expert call carries more
information than a positive co-occurrence, and it points the other way.

The inheritance predicates (`autosomal_dominant_inheritance`,
`x_linked_inheritance`, and the rest) additionally encode the mode, which is
often what a clinical user wants.

#### Size in the graph is not coverage of an entity

A source's total edge count says how much of it there is, not whether it has
anything for the entity in hand. These are independent, and conflating them
produces confident wrong guidance.

Observed once: a query for genes associated with a septal-defect phenotype
returned `HGNCHPO`, `CLINVAR`, `ORDO`, `NCI`, `CLINGEN`, `MEDLINEPLUS` and
`MTH`, and `DGN` — by a wide margin the largest gene-disease source in the
build — did not appear at all. That is evidence that size and coverage are
independent, not a claim about which sources cover septal defects.

So do not tell a user which sources will show up, or which will dominate.
Describe what each source *is*, and let the result say which are present. The
`sources` column is the finding.

## Absence of an expression path is the majority state

Roughly half of all gene-tissue pairs in GTEx have a median TPM of exactly
zero — 842,108 of about 1.57M measurements. So a gene failing an expression
filter is the common case, not a signal, and an expression-anchored query
traverses a minority of the gene-tissue matrix by construction.

Whether `GTEXEQTL` nodes all carry a `p_value` edge is **unresolved** — the
Data Dictionary's edge count implies near-full coverage, a later occupancy
measurement implies about a fifth are missing, and the two have not been
reconciled (`17_gtex_bins_addendum.md`). Match `p_value` with `OPTIONAL MATCH`
either way, and report nulls rather than dropping those eQTLs.

**What to say:** when expression is used as a filter, say that most of the
matrix is zeros, so the surviving set is small by design. A short result is
not evidence the genes are unusual.

## Adult expression data censors developmental genes

GTEx is adult post-mortem bulk tissue. Intersecting it with a **developmental**
phenotype removes exactly the genes whose action is confined to the
developmental window — and those are often the mechanistically central ones.

Observed once, as an illustration of the mechanism: applying a ≥1 TPM floor to
a congenital-heart-defect gene set dropped `NODAL`, a laterality gene
expressed in the embryonic node and largely silent in adult myocardium. The
gene did not fail the phenotype half. It failed a tissue assay taken decades
after the phenotype was determined.

**That is an example, not a fact to reuse.** It came from one query against
one build, with one phenotype anchor and one arbitrary threshold. Do not tell
a user that `NODAL` will drop out, that it is absent from adult heart, or that
any particular gene survives or fails an expression floor — those depend on
the anchor, the tissue set, the threshold, and the build. Whether a given gene
is censored is a question for their query, not for this file.

What generalises is the **shape**: adult expression filters bias against
developmentally restricted genes. What does not generalise is which genes.

This is a **systematic false-negative class**, not a scattering of misses. Any
query of the form "associated with a congenital or developmental phenotype AND
expressed in the relevant adult tissue" loses developmental regulators while
retaining structural and housekeeping genes. The result looks cleaner and is
biased.

**What to say:** name the censoring before the user reads the list. If the
question is about mechanism during development, adult expression is the wrong
filter, and the honest answer may be that this graph cannot supply the right
one.

Where expression is a filter rather than the question, consider reporting both
sets — the intersection, and the phenotype-associated genes that failed the
expression floor. The second set is where developmentally restricted genes
concentrate, and discarding it silently is the error.

## Positional overlap is not biological co-occurrence

Genomic features join through shared `HSCLO` bins, which is a statement about
coordinates and nothing else. Two features can share a bin and belong to
unrelated biological contexts.

A chromatin loop carries a cell type, three hops back on its `4DND` dataset.
An eQTL carries a tissue. Neither constrains the other, so an anchor overlap
between a loop called in one cell type and an eQTL measured in a different
tissue is a coordinate coincidence — real, and not evidence of a regulatory
relationship in either context.

**What to say:** when reporting a positional join, name both contexts, and say
plainly that matching them is a separate question the query did not ask. If
the user wants context-matched overlaps, that constraint has to be added
explicitly.

The same applies to any feature intersection through coordinates: cCRE
activity, RBP binding sites, and expression are each measured in particular
systems, and the bins do not know that.

## One entity, several Concepts

A molecule or disease can appear under both a UMLS Concept and a minted one.
The UMLS Concept carries codes from several vocabularies; the minted Concept
(`SAB:CODE CUI`) carries only the source's own code. Both are real nodes and
both may sit on the same edge set.

Consequence for aggregation: grouping on `CUI` splits the entity into two
rows, while grouping on the source identifier merges them. Neither is wrong,
but a count of "distinct metabolites" differs depending on which was used, and
the row count overstates the entity count.

**What to say:** when a result is a list of entities, group on the identifier
the user thinks in — a PubChem CID, an HGNC accession — rather than on `CUI`,
and say which was used. Where both forms appear, note that the list has fewer
distinct entities than rows.

## Names come from the source, not from a curator

Terms are whatever the contributing vocabulary supplied. PubChem chemical
names include supplier catalogue entries — grade, purity, packaging, vendor
part numbers — so truncating a name list can leave a row with no recognisable
chemical name.

Use one verified source-specific preferred-term edge as the display label when
that edge is known. Synonyms may be returned as additional audit information,
but do not choose the first or shortest synonym as the entity name. If no
preferred-term edge is verified, display the source `CodeID`.

## Errors amplify across hops

A false positive at the first hop becomes hundreds of rows at the fourth. In a
chain like pathway → gene → protein → compound, one over-broad pathway
contributes all of its genes, each gene its proteins, each protein its
compounds. The output looks abundant and is mostly the consequence of a single
bad match.

This makes the **first** hop the one to verify, and it makes an audit column
mandatory rather than nice to have: carry the intermediate identity through to
the result so the contamination is visible. A drug list alone gives no way to
see that the pathway match was wrong; a drug list with its target genes shows
it immediately.

Verify the first hop before running the full chain. One query returning
`DISTINCT` the matched entities at hop one costs almost nothing and prevents
interpreting an amplified artefact.

## Pathway membership is set membership, and sets vary in scope

Pathway sources define their sets to different standards and at wildly
different breadths. A curated cascade and a broad signalling superset can carry
the same name fragment, so matching pathway *names* by string returns sets
whose contents were never compared.

Membership is also not mechanism: a gene may be in a set because it is a core
component, a downstream effector, a transcriptional target, or because the
curator drew the boundary widely.

**What to say:** name which pathway entries were matched, not just how many
genes came out. Where a category has a structural definition — an ontology
term with descendants — prefer expanding that hierarchy to matching names.

## Two sources can be present and unjoinable

A pair of sources can each be well populated and share no Concepts, so a query
crossing them returns empty for every input. The emptiness is a property of
the ingestion, not of the entities.

Verified case: IDGP bioactivity compounds and the clinical drug vocabularies
(`DRUGBANK`, `RXNORM`, `ATC`) have **no** Concepts in common anywhere in the
graph, though both are substantial. Any query restricting bioactivity hits to
clinically-coded compounds returns nothing, for any protein.

This is worse than sparse coverage because it is total and uniform — there is
no positive case to reveal the problem. A sparse join returns few rows and
invites suspicion; a disjoint join returns none and reads as a finding.

**Before reporting an empty cross-source result**, check whether the two
sources share any Concepts at all:

```cypher
MATCH (c:Concept)-[:HAS_CODE]->(:Code {SAB:$sab_a})
MATCH (c)-[:HAS_CODE]->(:Code {SAB:$sab_b})
RETURN count(DISTINCT c) AS shared_concepts
```

Zero there means the query could never have succeeded, and that is what to
report.

## Sources are not always independent

Multi-source agreement only means something when the sources are independent.
Some are not: a vocabulary that republishes another's content produces two
SABs asserting the same thing from one origin.

The known case is MSigDB's C2:CP collection, built from Reactome,
WikiPathways, BioCarta and PID — all of which the DDKG also loads separately.
A gene appearing under both `MSIGDB` and `REACTOME` for the same pathway has
been redistributed, not corroborated, and counting them as two sources
inflates its apparent support.

**What to say:** before ranking on source count, check whether any of the
sources present derive from another. Where they do, count them once and say
so. `08_dcc_endpoints.md` records the overlap that is known; others may exist,
so a suspiciously well-agreed result is worth checking rather than trusting.

## A rough stringency ordering

Useful when ranking, though it is a judgement about the sources rather than a
property of the graph:

1. `CLINGEN` — expert-panel adjudicated. Rigour of assessment, not direction
   of finding: read `evidence_class` before treating a hit as support
2. `ORDO`, `OMIM`, `CLINVAR` — curated, narrow, explicitly causal or clinical
3. `OTG` — statistical association from GWAS
4. `HGNCHPO`, `MSIGDB` — annotation and membership, broad and indirect
5. `DGN` — heterogeneous association-node classes; interpret and rank by
   class rather than treating the source as one evidence tier
6. `MEDLINEPLUS` — consumer health material

A gene supported across tiers is better evidenced than one appearing several
times within a tier. Say which tiers a result draws on rather than only how
many sources agree.

## Multi-source agreement is the signal

**Confirmed.** When sources differ this much in what they assert, a gene
supported by several is more interesting than a gene supported by one large
noisy source.

A gene appearing under both a broad annotation source and a curated clinical
one is independently supported; a gene appearing only under a co-occurrence
source is not.

So return sources per entity and rank by breadth:

```cypher
MATCH (d:Concept {CUI:$cui})-[r]-(g:Concept)-[:HAS_CODE]->(hgnc:Code {SAB:'HGNC'})
OPTIONAL MATCH (hgnc)-[:ACR]->(sym:Term)
RETURN sym.name AS gene, hgnc.CodeID AS hgnc_id,
       collect(DISTINCT r.SAB) AS sources
ORDER BY size(sources) DESC, gene
```

This also folds away the inverse-pair duplication that would otherwise
return every row twice.

## One Code, several Concepts

**Confirmed.** A Code can map to several Concepts — see
`04_identifier_conventions.md`. Anchoring on one CUI silently excludes
whatever the others carry, with no sign in the output that anything was
excluded.

When a resolution returns several CUIs for one Code, either check each or
anchor on the Code and let `HAS_CODE` fan out:

```cypher
MATCH (concept:Concept)-[:HAS_CODE]->(:Code {CodeID:$codeid})
MATCH (concept)-[r]-(:Concept)
RETURN concept.CUI, type(r) AS predicate, r.SAB AS sab, count(*) AS n
ORDER BY concept.CUI, n DESC
```

## Fan-out is not breadth

**Confirmed.** A DCC predicate reaching 30-60 SABs is one Concept wearing
many identifier systems, not many distinct relationships.
`expressed_in {SAB:'GTEXEXP'}` reaches `UBERON`, `CL`, `FMA` and others
because a tissue Concept carries codes from all of them.

96.8% of Concepts carry exactly one SAB, but DCC edges attach preferentially
to the heavily normalised minority — tissues, diseases, phenotypes — so
fan-out is the norm in exactly the queries users care about.

What to say: pick the vocabulary the user already works in, and do not
present the alias list as findings.

## Never state a result that has not been run

Every number in this file came from one enumeration of one build. Source
refreshes change counts. They are recorded to show what the *kinds* of
evidence look like, not to be quoted as current values.

So when a user asks about an entity that happens to appear as a worked example
here, give them the query. Do not give them the recorded result as though it
were the answer. Where the historical figure is genuinely useful, attribute
it explicitly: "when this build was enumerated, that source had no edges for
this gene — worth confirming, since coverage changes."

The query has not been run here, so any statement about what it will return is
a guess wearing the clothes of an answer.

## What to say in an answer

A result is not an answer until it carries its interpretation. Include:

- **Which source asserted it**, named, not just `r.SAB` in a column.
- **What that source's evidence type means**, in one clause. "From HPO
  phenotype annotation, so this includes genes for syndromes that feature
  ASD rather than septation genes specifically."
- **What is absent and why**, when a source the user might expect is
  missing. Absence from the graph is not absence from biology.
- **Where the result is truncated**, if a `LIMIT` was applied. An
  alphabetically sorted list cut at 300 is not the top 300.

The user cannot supply these caveats themselves. That is the whole reason
this skill exists rather than a text-to-Cypher box.

## MED-RT contraindication endpoints are not disease-only

**Confirmed on the target release.** The MED-RT relationship named
`contraindicated_with_disease` has a looser endpoint range than its name
suggests. Returned objects can include disease Concepts, but also age,
life-stage, or pregnancy-related context. A query that keeps only objects
carrying a disease vocabulary can therefore silently discard valid MED-RT
contraindication assertions.

What to do: return the endpoint Codes and inspect what each represents before
applying an object-side vocabulary filter. Treat the predicate name as the
source's relationship label, not as a guarantee that every object is a
disease.
