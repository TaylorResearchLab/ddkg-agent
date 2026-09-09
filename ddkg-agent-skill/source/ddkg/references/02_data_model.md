# The UBKG data model

From `sources/ubkg_data_model.md`. This is *why* the graph is shaped as it
is. For the edge names this build actually uses, see
`03_schema_this_build.md` — the model document predates the rename.

## Concepts and synonymy

The UBKG organises assertions around **concepts**, following the UMLS
Metathesaurus. A concept is one idea; each data source encodes that idea
with its own code. SNOMEDCT_US calls a cell `4421005`; NCI calls it
`C12508`. Because those codes are synonyms, assertions made about either can
be consolidated at the concept level.

That consolidation is the entire point. Two sources asserting `cat isa
animal` and `feline chases mouse` become connected once `cat` and `feline`
resolve to one concept.

**Consequence for querying:** an assertion is always between Concepts, never
between Codes. To ask a question about a gene you enter through its Code,
step to its Concept, traverse, and step back out to a Code in whatever
vocabulary you want the answer in.

## The concept subgraph

Each concept carries a subgraph of metadata nodes:

| Node | Properties | Holds |
| --- | --- | --- |
| `Concept` | `CUI` | The concept itself |
| `Code` | `SAB`, `CODE`, `CodeID` | One source's encoding of it |
| `Term` | `name` | A label or synonym |
| `Definition` | `ATUI`, `DEF`, `SAB` | A source-attributed definition |
| `Semantic` | `STN`, `TUI`, `name` | UMLS semantic type |

CUIs from the UMLS start with `C`. When a non-UMLS code cannot be matched to
a UMLS concept, the generation framework mints a CUI of the form
`SAB:CODE CUI` — for example `HP:0001631 CUI`. **A CUI that does not look
like a CUI is not an error**, and filtering on `STARTS WITH 'C'` silently
drops every non-UMLS concept.

## Assertions and inverses

Every assertion is stored as a **bidirectional pair**: the forward
relationship and its inverse. Source files contain only forward assertions;
the UBKG derives the inverse on ingestion.

How the inverse is named depends on the Relations Ontology:

- If the predicate matches an RO relationship, RO's own inverse is used —
  `has_part` becomes `part_of`, not `inverse_has_part`.
- If it does not match RO, `inverse_` is prepended.

**Consequence:** filtering with `WHERE NOT type(r) STARTS WITH 'inverse_'`
catches only the second kind. `part_of`/`has_part`,
`location_of`/`located_in`, and `transcribed_from`/`transcribed_to` all
survive it and duplicate the result. Use `assets/inverse_pairs.json`, which
maps all pairs found in this build.

## Business rules

### PT and PREF_TERM

A Code's preferred term has term type `PT`. A Concept's preferred term is
reached by a separate relationship. One Term can serve both.

### PT_SAB

A source may define a preferred term for a code it does not steward — UBERON
naming a PATO code, for instance. The UBKG reserves the plain preferred-term
relationship for the code's actual steward, and gives the non-steward's term
a `PT_<SAB>` relationship instead.

**Consequence:** `PT_IDGP`, `PT_MW`, `PT_MONDO_SIMPLE`, `PT_HPOMP`,
`PT_PROTEOFORM`, `PT_PATO_BASE` are not irregularities. They are the rule
working. A query binding only `PT` misses every non-steward label.

### Preferred concept

Ideally each Code maps to one Concept, but many map to several — in this
build `MONDO:0006664` reaches three. The UBKG associates a Code with **all**
concepts a source specifies, then identifies a preferred one: the `CUI`
property on the Code-to-Term preferred-term relationship names it.

**Consequence:** anchoring on one CUI when a Code has several narrows the
result with no sign that it did. Either anchor on the Code, or use the
preferred-concept mechanism deliberately.

## Cross-references versus isa

- **`isa`** is hierarchical. The two codes stay distinct concepts, linked
  through their Concept nodes.
- **`dbxref`** is equivalence. The two codes end up sharing one Concept.

This is how a tissue Concept comes to carry `UBERON`, `CL`, `FMA` and other
codes at once, and therefore why a DCC predicate appears to reach dozens of
vocabularies. See `11_11_interpreting_results.md`.

## Permitted properties

The UBKG is a knowledge graph with a deliberately small property set.

- **Node properties** a source may define: `value`, `lowerbound`,
  `upperbound`, `unit`.
- **Edge property** a source may define: `evidence_class`.
- **Assigned by the framework:** `SAB` on assertion relationships, `CUI` on
  Code-to-Term relationships.

Nothing else. If a query needs a property not on this list, the query is
wrong about the model.
