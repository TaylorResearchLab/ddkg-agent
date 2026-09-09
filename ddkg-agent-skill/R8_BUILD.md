# R8 build record

- DDKG target: `DataDistillery_2025_04_DEC`
- Base commit: R7 merge `57352d09e692c52e1b56afacfdf05851ae6282af`
- Bundled files: 38
- Routing relationships: 258
- Archive size: 305646 bytes
- SHA-256: `f33334b293a4572b64198e1a7c039c61702bf6182b19ce7f5648d86102530546`

## R8 changes

R8 hardens the December 2025 release skill around silent-failure modes identified during R5b/R7 development testing:

- failed diagnostics are gates that stop dependent query composition;
- cross-source set operations require both sources at the same biological identifier level;
- absence of a direct link is not treated as absence of every possible graph route;
- display labels use a verified source-specific preferred-term edge or fall back to CodeID;
- GTEx thresholds select enumerated EXPBINS/PVALUEBINS identifiers rather than assumed numeric properties;
- Browser display limits are treated as client/configuration dependent rather than a universal row number;
- ingest submission syntax, Concept.CUI values, and stored CodeID values are explicitly separated;
- synonym scans are candidate discovery only;
- compound/drug resolution routes to the general one-Code/several-Concepts rule, not only minted-twin handling;
- MED-RT contraindication endpoints are not assumed to be disease-only;
- the public hygiene procedure requires a deployment-specific denylist before the artifact is formally frozen for evaluation.

## Release status

This branch artifact is the **R8 release candidate**. Generic public-hygiene checks passed on both the source tree and built archive. Before the evaluation artifact is declared frozen, the release owner must rerun `check_public_skill_hygiene.py` on both source and archive with `--require-denylist` and an external deployment-specific denylist that is not committed to the repository.
