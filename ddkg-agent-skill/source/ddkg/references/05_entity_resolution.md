# Resolving and profiling an anchor

Two steps before any traversal. Skipping either is where most wrong answers
come from — the query executes perfectly against the wrong anchor, or
against an entity the source has no data for.

Identifier conventions and term-edge bindings are in
`04_identifier_conventions.md`.

## A SAB is a source, not a kind of thing

Selecting `SAB IN ['MSIGDB','REACTOME','NCI','WP']` picks vocabularies. It does
not restrict the result to pathways, and several of those vocabularies contain
much else.

Observed once: a term match for pathway names across those sources returned,
from NCI alone, gene records, wild-type alleles, protein variants, a drug
class, and a disease subtype — all carrying the matched string in their names,
none of them a pathway. Reactome contributed individual reaction events
alongside pathways.

**`HAS_SEMANTIC` excludes, it does not select.** The UMLS semantic type is
useful for ruling entries *out* — NCI records typed `Cell or Molecular
Dysfunction` turn out to be gene mutations, `Pharmacologic Substance` to be
drug classes — but many concepts carry no semantic type at all. **Every
MSigDB pathway concept observed had none.** So a filter demanding a particular
type drops the source you most likely want, silently.

Use it to see what a match actually is, then exclude. Do not require a type:

```cypher
MATCH (c:Concept)-[:HAS_SEMANTIC]->(sty:Semantic)
RETURN sty.name, count(*) AS n
ORDER BY n DESC
LIMIT 40
```

Return `sty.name` as an audit column, read it, and exclude the types that are
plainly not what was asked for. Treat a null type as uninformative rather than
as evidence either way — for some sources it is the norm.

A name match cannot tell a pathway from a mutation carrying the pathway's name
in its label. Neither can a semantic-type filter on its own. The workable
route is to enumerate, look, and select CodeIDs, which is why pathway
selection is a staged decision rather than something to automate.

## Species

**The graph is not human-only.** `sources/ubkg_contexts.md` names these
sources as non-human or cross-species:

| SAB | Content |
| --- | --- |
| `HCOP` | human-to-mouse orthologs |
| `RATHCOP` | human-to-rat orthologs |
| `MPMGI` | mouse genotype-phenotype mapping |
| `EMAPA` | mouse developmental anatomy, embryonic and postnatal |
| `MP` | Mammalian Phenotype Ontology |

`AZ` (Azimuth) also carries model-organism reference atlases.

Species can also be hidden **inside identifiers rather than in the SAB**.
Reactome uses `R-HSA-` for human and `R-MMU-` for mouse under the single SAB
`REACTOME`, so a name match returns both and the pathway names are identical
between them. Check before assuming:

```cypher
MATCH (c:Code {SAB:'REACTOME'})
RETURN DISTINCT split(c.CodeID,'-')[1] AS species_prefix, count(*) AS n
ORDER BY n DESC
```

`EMAPA` deserves particular care in developmental work: it is mouse
developmental anatomy, which is precisely the vocabulary a human developmental
question reaches for, and substituting it is silent. `UBERON` is the
species-neutral anatomy ontology.

A mixed-species result is not obviously wrong on its face. Say which species a
query covers, and exclude the ortholog and model-organism sources unless they
were wanted.

## Resolve inside the query where you can

Resolution can stay inside the query when a source or identifier gives a
useful anchor. Prefer, in order: a verified `CodeID`; a known or candidate
`Code.SAB` set followed by term comparison; an indexable raw `Term.name`
predicate for candidate discovery when a TEXT index is present; and only then
a global function-wrapped name scan as an explicit fallback.

Do not start a large query by applying `toLower()` or `trim(toLower())` to every
`Term.name`. Those functions prevent a plain `Term.name` index from serving the
name predicate. If the source is known, reduce on the Code first and apply the
tolerant comparison only to its terms:

```cypher
MATCH (c:Code {SAB:'HP'})
WITH c
MATCH (c)-[]->(t:Term)
WHERE trim(toLower(t.name)) = toLower($name)
MATCH (anchor:Concept)-[:HAS_CODE]->(c)
```

On a deployment with a `Code.SAB` index, the Code anchor can reduce the
candidate set before the function-wrapped term comparison. If an appropriate
`Term.name` TEXT index is present and a case-preserving fragment is available,
`CONTAINS` or `STARTS WITH` can instead be used for candidate discovery; inspect
the returned term and Code before traversing onward.

A standalone resolution step earns its place when the name is genuinely
ambiguous, when the candidate source is unknown, or when the user needs to see
what the graph calls the entity. Do not hide an unconstrained all-Term scan
inside a much larger traversal.

## Step 1 — resolve the name to an anchor

Never bind a term edge type on an unfamiliar source. Leave it open and
return which one matched:

```cypher
MATCH (c:Code)
WHERE c.SAB IN $candidate_sabs
WITH c
MATCH (c)-[tr]->(t:Term)
WHERE trim(toLower(t.name)) = toLower($name)
MATCH (concept:Concept)-[:HAS_CODE]->(c)
RETURN c.SAB, c.CodeID, c.CODE, concept.CUI, type(tr) AS term_edge, t.name
LIMIT 25
```

Give several candidate SABs at once rather than guessing one — a disease may
live in `HP`, `MONDO`, `ORDO`, `OMIM`, `DOID`, `MEDGEN` or `SNOMEDCT_US`, and
the result shows which actually carry it.

If nothing returns, use an indexable `t.name CONTAINS $fragment` or `STARTS WITH`
candidate scan when the deployment has a suitable TEXT index, then inspect the
matched terms and Codes before traversing onward. Substring matches routinely hit
descriptions rather than symbols, so candidate discovery is not entity resolution.

**Ambiguous abbreviations must be disambiguated with the user, never
silently.** "ASD" is atrial septal defect and autism spectrum disorder. Picking
one silently produces a fluent answer to a question nobody asked.

But do not follow that with a question about sources. "Which would you like —
OMIM, HPO, ClinVar?" hands the allowlist decision to the person with less
information about the graph, and answering it requires exactly the knowledge
they came for. Run unfiltered, return `collect(DISTINCT r.SAB)`, and explain
what came back.

Asking which *route* they want is different and often worth doing, because
routes give different answers: direct gene-phenotype association and
syndrome-mediated association return different gene sets, and the second is
frequently what a clinical geneticist means.

## Step 2 — profile the anchor

Before composing the real query, ask what the anchor actually connects to.
One query, and it decides whether the question is answerable at all:

```cypher
MATCH (a:Concept)-[:HAS_CODE]->(:Code {CodeID:$codeid})
MATCH (a)-[r]-(:Concept)
RETURN type(r) AS predicate, r.SAB AS sab, count(*) AS n
ORDER BY n DESC
LIMIT 30
```

### Reading a profile

The result is a list of predicate/SAB pairs with counts. Read it as three
questions:

- **Is the source I need present at all?** If not, the question has no answer
  for this entity, and that is the finding.
- **Which predicates does that source use here?** They are often not the ones
  the question suggests.
- **What else is there?** When the asked-for source is missing, the sources
  that *are* present are usually worth offering.

A predicate name can mean different things under different sources.
`regulates` under `ERCCREG` is a regulatory element acting on a gene, not a
compound acting on a gene. Read the SAB, not the predicate name.

**Do not state the profile result.** Hand over the query. A profile recorded
in this file from an earlier enumeration is not an answer to a question asked
today.

## What the registries cannot tell you

`08_dcc_endpoints.md` says which SABs a predicate connects **in general**. It
cannot say whether a **particular** entity participates. Only the anchor
profile answers that, and the difference is the whole reason step 2 exists.

## Do not filter by SAB when the endpoint already constrains

A traversal anchored at both ends is already specific. Anchoring the far side
on a `Code` with a known SAB restricts the result to that entity type, so an
additional `WHERE r.SAB IN [...]` adds nothing but the risk of omitting a
source nobody thought to list.

```cypher
// asks the graph which sources connect these two things
MATCH (d:Concept {CUI:$cui})-[r]-(g:Concept)-[:HAS_CODE]->(hgnc:Code {SAB:'HGNC'})
OPTIONAL MATCH (hgnc)-[:ACR]->(sym:Term)
RETURN sym.name AS gene, hgnc.CodeID AS hgnc_id, collect(DISTINCT r.SAB) AS sources
ORDER BY size(sources) DESC, gene
```

Collecting sources per entity also folds away the inverse-pair duplication
and ranks by breadth of support.

## A predicate can be one hop from the anchor and two from the answer

Anchoring the far side on `(:Code {SAB:'HGNC'})` excludes any predicate that
does not terminate at a gene — including ones that reach genes through an
intermediate.

Asked for genes associated with a phenotype, a gene-anchored query can appear
to show OMIM missing. OMIM asserts `has_manifestation` from **disease to
phenotype**, so its genes are one hop further out — through each syndrome's
own gene association:

```cypher
MATCH (pheno:Concept {CUI:$cui})-[:has_manifestation {SAB:'OMIM'}]-(disease:Concept)
MATCH (disease)-[:HAS_CODE]->(mim:Code {SAB:'OMIM'})
MATCH (disease)-[gr]-(gene:Concept)-[:HAS_CODE]->(hgnc:Code {SAB:'HGNC'})
OPTIONAL MATCH (hgnc)-[:ACR]->(sym:Term)
RETURN sym.name AS gene, hgnc.CodeID AS hgnc_id,
       count(DISTINCT mim.CodeID) AS syndromes,
       collect(DISTINCT gr.SAB) AS sources
ORDER BY syndromes DESC, gene
```

That returns genes ranked by how many syndromes featuring the phenotype each
one causes, which is a different and often more useful answer than the direct
route: it shows *why* a gene is implicated, by name.

**So check the anchor profile for predicates that do not terminate where you
expected, and consider the two-hop route.**

## OPTIONAL MATCH to Term before a LIMIT truncates by synonym count

Expanding terms multiplies each code by its number of labels, so a `LIMIT`
applied afterwards measures synonyms rather than codes — a limit of 100 can be
consumed by a handful of codes. Aggregate first, expand labels last:

```cypher
// count the shape first
MATCH (d:Concept {CUI:$cui})-[r:has_manifestation {SAB:'OMIM'}]-(x:Concept)
MATCH (x)-[:HAS_CODE]->(c:Code)
RETURN c.SAB AS sab, count(DISTINCT c.CodeID) AS codes
ORDER BY codes DESC
```

## Name scans versus symbol anchors

A UniProtKB preferred-name scan for `ALOX` returns `ALOX12`, `ALOX15`, and
`ALOX15B`, but misses `ALOX5` because its preferred name is
`Polyunsaturated fatty acid 5-lipoxygenase ` with a trailing space. The
padding breaks equality but not `CONTAINS`.

An HGNC symbol-prefix search through `ACR` returns twelve genes: five
lipoxygenases, five pseudogenes that drop out at `gene_product_of`, and
`ALOX5AP`. `ALOX5AP` is not a lipoxygenase and had the largest IDG assay
footprint in the returned set, 2,021.

Retrieve gene families by symbol. Treat name scans as discovery aids whose
misses are assumed, and inspect every member returned by a prefix. `FUT10` and
`FUT11` had no `gene_product_of` edge on either the July or December build.
