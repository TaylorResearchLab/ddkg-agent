# R8 build record

- DDKG target: `DataDistillery_2025_04_DEC`
- Base commit: R7 merge `57352d09e692c52e1b56afacfdf05851ae6282af`
- Bundled files: 38
- Routing relationships: 258
- Archive size: 305719 bytes
- SHA-256: `a8f24199de1855cb95fc2d0391ab6d1674ef00b7942dd40e9dfbdf27eac97486`

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
- compound/drug resolution routes to the general one-Code/several-Concepts rule, not only minted-twin handling; and
- MED-RT contraindication endpoints are not assumed to be disease-only.

## Release status

This branch artifact is the **R8 release candidate**. Routing validation and deterministic build checks passed. Focused live engineering regressions against the target DDKG remain before the evaluation artifact is declared frozen.
