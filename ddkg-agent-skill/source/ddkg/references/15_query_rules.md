# Query rules

The ten rules in `SKILL.md` step 5 decide whether a query returns the right
rows at all. These are the rest — each one caused a real failure, and each is
routed from the topics where it applies rather than held in working memory.

`route.py <topic>` returns the ones bearing on a given question.

## Anchoring and cost

- **Anchor on the smallest set you can name**, not the smaller half of the
  question. Three UBERON codes beat a string match over 11.1M Terms, even when
  the tissue looks incidental. On builds without property indexes every
  `{SAB:'X'}` match is a full label scan — see the cost section in
  `03_schema_this_build.md`, and warn the user when a query will be slow.
- **Reduce between halves of an intersection.** `WITH DISTINCT` after the
  first half, or both halves expand before anything collapses.
- **Census presence is not conjunction coverage.** A predicate can exist with
  hundreds of edges while its intersection with another leg is empty —
  `predicted_in {ERCCRBP}` has 268 edges against 462K for
  `molecularly_interacts_with`. Run a staged funnel, one leg per statement,
  before composing a multi-leg chain; the first zero is the dead constraint.
- **Cap every stage.** `CALL (x) { ... LIMIT n }` per-row subqueries bound
  per-entity expansion, and symmetric predicates need a walk-back guard
  (`WHERE t <> g`) when hops are split across `MATCH` clauses. On Neo4j 5.26,
  `CALL { WITH x ... }` raises a deprecation warning; write
  `CALL (x) { ... }`.

## Caps count what the DISTINCT tuple contains

A per-stage cap counts distinct tuples. If the tuple carries relationship
variables, the cap counts edge multiplicity rather than entity diversity. One
entity with many parallel edges can fill a stage and starve every stage below
it, and raising the cap does not repair the grain. This occurred in the Q10
figure variant when an unbound condition-tissue closure remained inside the
tuple.

Funnel stages should carry `Concept` nodes only. Test closure constraints with
`WHERE EXISTS { ... }`, then re-match the relationships needed for display
after the node set is fixed.

For exemplar output, cap per anchor with `CALL (x) { ... LIMIT n }`. A global
`LIMIT` can print only the largest member: the old Q04 form returned 25 rows,
all for `ALOX12`.

## Identity and matching

- **Never match a Code node with an edge-only SAB** — 34 of them, including
  `LINCS`, `CMAP`, `DGN`, `IDGP`, `IDGD`, `ERCCREG`, `4DN`, `KF`, `GENCODE`,
  `CLINVAR`, `STRING`. Those go on the relationship.
- **Never split a `CodeID` to extract meaning — matching one is fine.** Identity lives in the
  vocabulary the Concept connects to — GTEx tissue is a hop to `UBERON`, not a
  substring of the `GTEXEXP` code. Composite CodeIDs carry components that
  vary between records, so a fixed delimiter works for some rows and not
  others, and the failure is invisible: `split()` on an absent delimiter
  yields null, `collect` drops nulls, and the column comes back partially
  populated as though the data were sparse. Source shapes are in
  `08_dcc_endpoints.md`.
- **Select anatomy and disease by CodeID, not by string.** Vocabulary has
  false friends: `'cardiac'` matches the gastroesophageal junction, `'atri'`
  matches atresia, `'renal'` is inside `'adrenal'`, and an organ name matches
  lab assays and procedures as well as diseases. Enumerate, look, then pin —
  and always return the matched term as an audit column.
- **Group on the identifier the user thinks in, not on `CUI`.** One entity can
  hold both a UMLS Concept and a minted `SAB:CODE CUI` Concept, so grouping on
  `CUI` splits it and the row count overstates the entity count.

## Values and properties

- **A `GTEXEXP` edge means measured, not expressed.** Roughly half of all
  gene-tissue pairs sit in the exact-zero bin — 842,108 of about 1.57M
  measurements. An unfiltered expression query is therefore around half zeros,
  so apply a bin filter when the question means expression. Structure and
  occupancy: `17_gtex_bins_addendum.md`.

- **Threshold numbers on the Code node**, not the edge. Values live on bin
  Codes (`EXPBINS`, `PVALUEBINS`).
- **`evidence_class` is heterogeneous.** Numeric strings on LINCS, assay types
  on IDGP, expert classifications on CLINGEN. Report it, never filter on it,
  never assume it is categorical.
- **Return the relationship, not just its endpoints.** Relationships are
  first-class objects; 42 predicates carry `evidence_class` alongside `SAB`.
