# R8 change specification

## Scope

R8 is a hardening release for the December 2025 DDKG (`DataDistillery_2025_04_DEC`). It does not add a new DDKG schema or new data sources. It converts failure modes identified during R5b/R7 development into explicit controller rules, routing requirements, and source-specific cautions.

## Implemented changes

1. **Diagnostic gates.** A failed prerequisite check stops the query that depends on it rather than becoming a caveat above an invalid query.
2. **Cross-source comparability.** Intersections, subtractions, antijoins, and negation require both sources to attach at the same biological identifier level.
3. **Indirect-route discipline.** Failure to find a direct relationship is not treated as evidence that no graph route exists.
4. **Display labels.** A display name comes from one verified source-specific preferred-term edge; otherwise the source CodeID is shown. Arbitrary synonyms are not selected as canonical labels.
5. **GTEx thresholds.** Expression and eQTL thresholds select enumerated `EXPBINS` and `PVALUEBINS` identifiers rather than assuming numeric Code properties or constructing bin identifiers from memory.
6. **Browser truncation.** Browser display limits are treated as client/configuration dependent. Completeness is checked with counts or export rather than a universal 1,000- or 5,000-row assumption.
7. **Identifier-format boundary.** UBKG ingest submission syntax is distinguished from stored `CodeID`; minted `<CodeID> CUI` values are distinguished from Code identifiers.
8. **Synonym resolution.** Synonym and substring scans are candidate discovery only and require confirmation of the source Code and preferred term before traversal.
9. **One Code, several Concepts.** Compound, drug, and general entity routing reaches the existing rule that a Code can attach to several legitimate Concepts, not only the minted-twin special case.
10. **MED-RT endpoint range.** `contraindicated_with_disease` is not assumed to have disease-only objects; endpoint identity is inspected before applying a disease-vocabulary filter.

## Verification before formal evaluation

Static/build checks have passed for the release candidate. The remaining pre-freeze work is listed in `R8_REVIEW_CHECKLIST.md` and consists of focused live engineering regressions against the target DDKG instance plus evaluation-packet preparation.

The formal evaluation begins only after those checks, final archive freeze, prompt contamination audit, and construction of the new orthogonal Tier 8. Once formal evaluation begins, the archive is immutable.
