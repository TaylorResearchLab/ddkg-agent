# Identifier conventions

Where resolution goes wrong. Every rule here is confirmed against the live
graph, with the documented explanation from `sources/ubkg_ingest_formats.md`
and `sources/ubkg_contexts.md`.

## Anchor on CodeID

`CodeID` is the canonical CURIE for every source. `CODE` is whatever that
source stored, and the conventions disagree:

| SAB | `CodeID` | `CODE` |
| --- | --- | --- |
| `HGNC` | `HGNC:10848` | `10848` |
| `MONDO` | `MONDO:0006664` | `6664` — zero-padding lost |
| `DOID` | `DOID:1882` | `1882` |
| `SNOMEDCT_US` | `SNOMEDCT_US:70142008` | `70142008` |
| `OMIM` | `OMIM:MTHU036339` | `MTHU036339` |
| `HP` | `HP:0001631` | `HP:0001631` — prefix retained |

No single rule converts a CURIE to a `CODE`.

```cypher
MATCH (c:Code {CodeID:'MONDO:0006664'})          // reliable
MATCH (c:Code {SAB:'MONDO', CODE:'0006664'})     // nothing — padding stripped
MATCH (c:Code {SAB:'HP', CODE:'0001631'})        // nothing — HP keeps its prefix
```

**Why.** The colon is reserved as the SAB/code delimiter in `CodeID`. A few
UMLS vocabularies natively embed their own name in the code — HGNC as
`HGNC HGNC:x`, GO as `GO GO:x`, HPO as `HPO HP:x`. The generation step
reformats these to `SAB:CODE` and standardizes HPO's SAB to `HP`. The
normalization was applied unevenly, which is why `HP` still carries its
prefix inside `CODE` and `HGNC` does not.

When the convention for a source is unknown, match either form:

```cypher
MATCH (c:Code {SAB:$sab})
WHERE c.CODE = $code OR c.CodeID = $sab + ':' + $code
RETURN c.CodeID, c.CODE
```

## Verified anchors

Confirmed by query. Extend this table whenever an anchor is verified.

| Entity | CodeID | CODE | Symbol edge |
| --- | --- | --- | --- |
| SHH | `HGNC:10848` | `10848` | `ACR` → `SHH` |
| GTEx heart, left ventricle | `UBERON:0006566` | — | — |
| GTEx heart, atrial appendage | `UBERON:0006631` | — | — |
| SDCCAG8 | `HGNC:10671` | `10671` | `ACR` → `SDCCAG8` |
| Atrial septal defect | `HP:0001631` | `HP:0001631` | `PT`, `PT_HPOMP` |
| Atrial septal defect | `MONDO:0006664` | `6664` | `SY`, `PT_MONDO_SIMPLE` |

These are anchors — identifiers confirmed to exist and to carry the term
shown. They are not results: what each connects to is a question for the
graph, not for this table.

## Gene symbols use ACR

For HGNC, `ACR` carries the symbol and `PT` carries the long descriptive
name. Matching a symbol against `PT` fails in a way that looks like success:
searching `PT` for a name starting with `SHH` returns **HGNC:10671,
SDCCAG8** — whose descriptive name begins "SHH signaling and ciliogenesis
regulator". A plausible gene, silently the wrong one.

```cypher
MATCH (c:Code {SAB:'HGNC'})-[:ACR]->(t:Term)
WHERE t.name = 'SHH'
RETURN c.CodeID, c.CODE
```

**Bind `ACR` alone, not `ACR|MTH_ACR`.** Both exist and carry different
strings: `ACR` is the bare symbol (`ALOX5`), `MTH_ACR` appends a suffix
(`ALOX5 gene`). Binding both doubles the rows and yields two spellings of the
same symbol.

**Term names may carry trailing whitespace** — `"ALOX12 "` was observed. An
exact `=` match fails on padding with no indication. Use `trim(t.name) = $sym`
where an exact match matters, or `STARTS WITH` where it does not.

The general form, for any source:

```cypher
MATCH (c:Code {SAB:$sab})-[tr]->(t:Term)
WHERE t.name = $name
RETURN type(tr) AS term_edge, c.CodeID, c.CODE, t.name
LIMIT 10
```

## MTHU codes

A `CodeID` like `OMIM:MTHU036339` is not an OMIM accession. `MTHU` prefixes
are minted by the UMLS Metathesaurus when a source contributes a term
without its own identifier for it.

Real OMIM entries are six-digit MIM numbers. `OMIM:MTHU036339` for "atrial
septal defect" means UMLS created a placeholder — **not** that the OMIM
import failed. OMIM catalogues numbered subtype entries — six-digit MIM
numbers — rather than one umbrella term, so its content sits one level down.

**An `MTHU` code is the tell that a source organises the domain at a
different granularity.** Look for its specific entries before reporting the
source as absent:

```cypher
MATCH (c:Code {SAB:$sab})-[tr]->(t:Term)
WHERE toLower(t.name) CONTAINS $fragment
RETURN c.CodeID, c.CODE, type(tr) AS term_edge, t.name
ORDER BY c.CODE
LIMIT 30
```

## Non-UMLS CUIs

Concepts sourced outside the UMLS carry a minted CUI of the form
`SAB:CODE CUI` — so one Code can reach both a `C`-prefixed UMLS CUI and a
minted one such as `HP:0001631 CUI`. Filtering on `CUI STARTS WITH 'C'` drops
the minted ones.

## One Code, several Concepts

A Code may map to several Concepts. The UBKG associates a Code with every
Concept a source specifies, then identifies a **preferred concept** via the
`CUI` property on the Code's preferred-term relationship.

Anchoring on one CUI when a Code has several narrows the result invisibly.
Either anchor on the Code and let `HAS_CODE` fan out, or collect the CUIs
deliberately:

```cypher
MATCH (concept:Concept)-[:HAS_CODE]->(:Code {CodeID:$codeid})
RETURN collect(DISTINCT concept.CUI) AS cuis
```
