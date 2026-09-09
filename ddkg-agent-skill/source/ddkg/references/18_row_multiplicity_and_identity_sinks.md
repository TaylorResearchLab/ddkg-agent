# Row multiplicity and identity sinks (30-31 Aug 2026)

Additive reference file for the /ddkg skill. All findings confirmed by live runs
against the December 2025 CSV release (DataDistillery_2025_04_DEC, Neo4j 5.26.28
Community) while producing printed example output for the eleven manuscript
queries. Every one of them was invisible until rows were printed and counted:
each query returned its nominal `LIMIT`, so nothing looked wrong.

## 1. The tenth rule

**Decide the grain, then make it explicit.** A query returns one row per
*combination of everything bound*, not one row per thing you meant to ask
about. Two failure directions, both silent:

- **Multiplication**: a variable bound in `MATCH` but absent from `RETURN`
  still multiplies rows. Ten rows under a `LIMIT 10` looked like ten results
  and were one gene fanned over hidden loci.
- **Collapse**: aggregating a multi-valued endpoint into one scalar
  (`collect(...)[0]`, or a sliced code list) hides the set and can misname the
  entity entirely.

Cures, in order of preference: filter constraints in `WHERE EXISTS { }` when
they are not returned data; bind one label edge per source; return the hidden
variable when it is informative; aggregate into a visible list when it is not;
`RETURN DISTINCT` as the backstop for value-identical duplicates.

## 2. MTH:NOCODE is an identity sink

`MTH:NOCODE` is the UMLS placeholder Code used where a source supplies none.
On this build it carries **259,349 Terms across 258,919 Concepts** (edge types
`SY`, `PN`, `RT`, `DT`, `CV`; no `PT`).

Consequence: any pattern that reaches a `Code` **without binding `SAB` or
`CodeID`** and then matches a `Term` by name can land on it, and it will match
almost any string. Observed: a MoTrPAC gastrocnemius (skeletal muscle) feature
satisfied a "tissue whose Term is named Heart" filter through `MTH:NOCODE`,
so a heart-constrained query silently returned skeletal muscle rows.

```cypher
// wrong: Term-name match across an unbound Code
MATCH (c)-[:HAS_CODE]->(:Code)-[]->(:Term {name:'Heart'})
// right: bind the vocabulary
MATCH (c)-[:HAS_CODE]->(:Code {CodeID:'UBERON:0000948'})
```

This extends the existing rule *select anatomy and disease by CodeID, not by
string* (`15_query_rules.md`): the hazard is not only false friends in the
vocabulary, it is a hub node that makes name matching meaningless. It also
means Concept **code counts include placeholders** — check before citing a
count as evidence of cross-vocabulary aggregation.

## 3. Minted CUI twins duplicate assertions

A `Code` can be attached to two `Concepts`: a UMLS CUI that already holds the
Code among other vocabulary memberships, and a minted `<CodeID> CUI` Concept
holding only that Code. DCC assertions can be written in full to both.

On the target release, 276 of 1,506 PubChem Codes with MW condition assertions
were twinned (18%). `PUBCHEM:5280450` carried 26 gene, 8 condition, and 62
tissue MW edges on each twin. `PUBCHEM:2247` (astemizole) carried its LINCS
edges on the minted twin only.

Consequences:

- Grouping by `Concept` double-counts every chain through a twinned entity.
  Group by the `Code`, normally its `CodeID`.
- `LIMIT 1` after a Code-to-Concept expansion is a coin toss between twins.
  Require the edge the next stage needs with a constraint such as
  `WHERE EXISTS { (c)-[:predicate {SAB:'SOURCE'}]-() }`, or carry both
  Concepts forward.
- Diagnostic: for a given SAB and predicate, count Codes whose assertions are
  split across twins — match the Code, expand to every Concept holding it,
  and compare per-Concept edge counts for that predicate. A Code whose counts
  differ between Concepts is twinned with an uneven split; one whose counts
  are equal is twinned with duplication.

This finding superseded the earlier interpretation, now corrected in
`13_empirical_findings_aug2025_validation.md`: the apparent missing term was
observed on the untwinned Concept rather than the Concept carrying the LINCS
assertions.

## 4. One Concept, several diseases

`C0338451` carries `HP:0002145`, `MONDO:0010857` (semantic dementia),
`MONDO:0011842` (GRN-related FTLD with TDP-43 inclusions), `MONDO:0017276`
(frontotemporal dementia), and `DOID:0060672` (FTD2).

Name a condition by the Code the query displays, never by the CUI's UMLS
name. Counts of vocabulary Codes on one Concept measure vocabulary membership,
not a count of distinct diseases.

## 5. GTEx measurements attach to a tissue and its parent term

`GTEXEXP` measurement Concepts carry `expressed_in` to the specific UBERON
tissue and to a parent Concept. On the Q09 gene set of 44 genes, coronary
vessel, frontal lobe, and small intestine Peyer's patch duplicated their
specific tissues exactly; uterine cervix was the union of ectocervix and
endocervix; cerebellum held two GTEx samplings.

Tissue-grain aggregation therefore returned 57 columns for 54 GTEx tissues.
For per-tissue matrices, group by the measurement Code
(`GTEXEXP:<ENSG>-<n>-<GTEx tissue label>`), not by the UBERON Concept.

## 6. Label fans: bind one preferred term, per source

Codes carry several Terms. An unbound term match returns one row per Term.

- **Synonyms**: `MP:0010403` carries `PT` "atrial septal defect" plus three
  `SY` ("asd", "atrial septum foramen", "interatrial septal defect"). Ten rows
  held two and a half genes.
- **Per-source preferred terms with identical names**: one PUBCHEM Code carries
  `PT_IDGD` and `PT_IDGP` with byte-identical strings, some also `PT_MW` with
  different capitalization. Every row duplicated. Bind *one source's* PT —
  match the source of the assertion being reported (`PT_IDGP` alongside IDGP
  bioactivity, `PT_LINCS` alongside LINCS regulation).
- **No bare `PT` at all**: UBERON Codes carry only per-source preferred terms
  (`PT_UBERON_BASE`, `PT_EFO`, `PT_OBI`, `PT_OBIB`, `PT_MP`). A generic
  `-[:PT]->` match yields nothing and the CodeID fallback prints, which reads
  as missing data rather than as a wrong edge type.

Keep the match `OPTIONAL` with `coalesce(term.name, code.CodeID)`: rule 4
(labels are decoration) still holds. Binding a type is not the same as
requiring one.

## 7. Stored inverse orientations double rows

Assertions are stored in both directions under paired type names, so an
undirected match hits each copy. Two naming conventions:

- `inverse_` prefix (ontology-style): HGNCHPO `associated_with` /
  `inverse_associated_with`.
- Suffix pairs: LINCS `positively_regulates` / `positively_regulated_by`.

```cypher
WHERE NOT type(dg) STARTS WITH 'inverse_'
WHERE NOT type(lr) ENDS WITH '_regulated_by'
```

Regulation *sign* is a separate axis from storage orientation; excluding the
mirror does not drop negative regulation. Storage behavior must be diagnosed
per source and predicate. On the target release, IDGP stores `bioactivity`
from PUBCHEM to UNIPROTKB and `inverse_bioactivity` from UNIPROTKB to PUBCHEM
as a paired orientation. A probe restricted to the `bioactivity` type on a
known pair therefore counts one edge, while an undirected or type-unbound
match can still encounter both stored orientations. Do not infer source-wide
single-edge storage from a type-restricted count, and do not apply a blanket
inverse filter without inspecting `type(r)`.

## 8. Diagnose before amending

Each of the above was identified by a ten-second probe before any query was
changed. The probes generalize:

```cypher
// what label edges does this Code carry?
MATCH (c:Code {CodeID:$id})-[t]->(term:Term)
RETURN type(t) AS term_edge, term.name AS term ORDER BY term_edge;

// is this edge stored twice?
MATCH (a:Concept)-[b:predicate {SAB:$sab}]-(x:Concept)-[:HAS_CODE]->(:Code {CodeID:$id})
RETURN count(b) AS n_edges, collect(DISTINCT type(b)) AS edge_types;

// is this Concept one entity, or several codes merged?
MATCH (c:Concept)-[:HAS_CODE]->(cc:Code)
RETURN count(DISTINCT cc.CodeID) AS n_codes, collect(DISTINCT cc.SAB)[0..10] AS sabs;
```

Corollary for reporting: when a Concept can carry many codes, return
`size(collect(DISTINCT code.CodeID))` alongside any sliced list, so a reader
can see that the printed identifiers are a slice.

## 9. Two orthology cautions

- `in_1_to_1_orthology_relationship_with` (HCOP) resolves to **family-level**
  mappings on this build: BRAF and RAF1 each reach Braf, Raf1, and Araf; NSD1
  and NSD2 each reach the Nsd trio. A chain that filters on a phenotype
  therefore reports "the family ortholog carrying the annotation", which may
  not be the nearest one-to-one partner. Say so rather than treating the
  returned mouse gene as strict.
- Capped per-entity samples are storage-ordered, not biology-ordered: the same
  three GTEx tissues (venous blood, vagina, uterus) surface first under
  independent per-gene caps. Do not read a capped sample as a top-N.

## 10. Runtime observations (December 2025 build, same session)

Anchor cardinality dominates everything else. Same instance, same day:

| Query shape | Wall time |
| --- | --- |
| Relationship-anchored, capped per hop (GLYCANS, 182 edges) | 0.1 s |
| Family term scan over UNIPROTKB PTs, capped | 1.0 s |
| Phenotype CodeID anchor to LINCS compounds | 1.5 s |
| Cross-species chain, four staged hops | 2.4 s |
| Compound to metabolite to condition, six hops, hard caps | 3 s |
| Common Neighbors by two-hop traversal, one phenotype anchor | 13.5 s |
| Same, four anchors plus ranking and pivot | 73 s |
| Cohort join across orthology and phenotype ontologies, capped | 670 s |
| Same, uncapped monolithic form | abandoned past 30 min |
| Same, staged with `WITH DISTINCT` per hop, uncapped | ~60 s |

The last three are one query in three forms: the doctrine's staging rules are
worth roughly a factor of thirty on the wide join, and the capped form's speed
says nothing about the uncapped form's feasibility.
