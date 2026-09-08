# Empirical findings: December 2025 release validation campaign (28-29 Aug 2026)
Additive reference file for the /ddkg skill. The filename is retained for
routing compatibility, but the findings were confirmed by live runs against
the December 2025 CSV release (`DataDistillery_2025_04_DEC`), which uses the
August 2025 `HAS_CODE` schema, during Nature Methods paper query validation.

## 1. Query-design doctrine (five rules)
Six of eleven legacy queries failed or hung on violations of these; all
validated queries pass under them.
1. Anchor on the smallest enumerable leg. Relationship-type anchors are the
   only index-backed starts on an unindexed build (MW predicates; GLYCANS
   has_enzyme_protein, 182 edges).
2. Stage per hop: expand only from bound nodes, WITH DISTINCT between stages.
   Large single MATCH patterns let the planner hash-join from superhub ends
   (observed: GTEXEXP tissue-side scan; two hangs, one timeout).
3. Never write directed arrows on assertion predicates unless the direction is
   verified on this build. Inverse assertions are separate relationship types;
   a wrong arrow returns zero silently. Verified: has_enzyme_protein is
   reaction -> enzyme; 4DN loop predicates emit from the loop concept.
4. Labels are decoration, never constraints: reach Terms with OPTIONAL MATCH
   and coalesce(term.name, code.CodeID). A required term edge on
   PUBCHEM:2247's UMLS Concept (which carries none) zeroed an entire valid
   chain in 2 s.
5. Cap every stage; use CALL { ... LIMIT n } per-row subqueries to bound
   per-entity expansion; guard symmetric predicates against walk-back
   (WHERE t <> g) when hops are split across MATCH clauses.

## 2. SAB facts
- Node SAB and edge SAB can differ for one dataset: 4DNL nodes / 4DN edges.
  GLYCANS is edge-only (0 Code nodes, 182 has_enzyme_protein edges) with
  endpoints under GLYCOSYLTRANSFERASE.REACTION, GLYGEN.GLYCOSYLATION,
  UNIPROTKB.
- gene_product_of edge SABs: UNIPROTKB (20,208), GENCODE (73).
- HPOMP bridges MP <-> HP via is_approximately_equivalent_to.
- Full 289-SAB node inventory captured (d5_all_node_sabs.out); merge into the
  SAB registry.

## 3. Predicate and structure facts
- Inverse pairs are separate types, usually inverse_-prefixed, but some
  sources name inverses semantically (LINCS positively_regulates /
  positively_regulated_by). Unbound hops match both members: filter
  NOT type(r) STARTS WITH 'inverse_' or aggregate DISTINCT entities.
- GTEXEXP `expresses` and `expressed_in` are an inverse pair with equal
  GTEXEXP counts. Directed traversal is not interchangeable from every
  endpoint on this release: tissue to measurement uses `expresses`, while
  binding `expressed_in` in that direction returns zero. For robust
  composition, leave the type unbound with `SAB:'GTEXEXP'` or bind both names,
  then disambiguate endpoint roles by Code SAB.
- Identical duplicate edges occur (CLINVAR disease-gene x2): multi-assertion
  preservation, not error; collapse with DISTINCT when reporting.
- Thin legs are real: predicted_in {ERCCRBP} has 268 edges vs 462K
  molecularly_interacts_with. Census presence says nothing about conjunction
  coverage; run a staged funnel before composing multi-leg chains.

## 4. Property and label facts
- evidence_class is heterogeneous: numeric strings on LINCS regulation edges
  (e.g. 0.0221) and assay types on IDGP bioactivity (IC50, Ki). Report, never
  filter, never assume categorical.
- Term names may carry trailing whitespace ("ALOX12 "): exact matches can
  fail on padding.
- MTH_ACR labels append " gene"; ACR carries the bare symbol. Bind ACR alone
  for symbols; ACR|MTH_ACR doubles rows.
- EXPBINS CodeIDs embed bin bounds as strings (EXPBINS:300.0.400.0); numeric
  bound properties remain absent. Bounds recoverable by string parsing only.
- GTEXEQTL CodeIDs embed dotted tissue names (...b38.Heart.Left.Ventricle);
  tissue identity should still traverse UBERON for durability.

## 5. Verified anchors (December 2025 release)
- HP:0002145 (PT Frontotemporal dementia); HP:0002099 (Asthma);
  HP:0001631 (atrial septal defect).
- HGNC:435 (ACR ALOX5; MTH_ACR "ALOX5 gene"; SYN 5-LOX).
- UNIPROTKB:P09917 (ALOX5 protein; 1,174 IDGP compounds; gene_product_of to
  HGNC:435 confirmed).
- PUBCHEM:2247's UMLS Concept carries no term edge; its minted twin carries
  both the term and the LINCS regulation edges (25 per direction type). The
  apparent absence was the untwinned Concept — see reference 18, section 3.
  Displayed synonym "Waruzol" pending verification against astemizole.
- RATHCOP carries the rat has_human_ortholog assertions (MoTrPAC path).

## 6. Empty-result diagnosis method (S9-ready)
(1) schema discriminator; (2) predicate census via db.relationshipTypes name
filter (instant); (3) node-SAB census; (4) type-anchored per-predicate SAB
counts; (5) staged survivor funnel, one leg per statement, first zero = dead
constraint; (6) anchor neighborhood dumps. Nine failure classes identified
and fixed this way across eleven queries.
