# R8 focused engineering regression set

These checks verify repairs before the R8 archive is frozen. They are intentionally based on known development failures and therefore are **not** evidence of orthogonal generalization.

Run each against `DataDistillery_2025_04_DEC` using the R8 release candidate. Execute every generated query and record the final behavior.

| Repair | Regression question or check | Required behavior |
| --- | --- | --- |
| Diagnostic/set-operation gate | ClinGen gene-disease validity vs Open Targets Genetics comparison at gene level | Verify endpoint level first. If OTG does not support the same gene-level comparison, stop and do not compose the subtraction. |
| Direct link vs graph route | Cellular-component term to genes/model-organism phenotype route | Do not infer that an external gene set is required merely because no direct HGNC edge exists; inspect neighboring identifier spaces and bridge predicates. |
| Display labels | UBERON endpoint display and a source with several term-edge types | Use one verified source-specific preferred term or display CodeID; do not choose an arbitrary synonym. |
| GTEx threshold | Genes expressed above a numeric TPM threshold in a named tissue | Enumerate/select `EXPBINS` CodeIDs rather than filtering an assumed numeric property. |
| Browser truncation | Request a graph-wide gene listing | Count first and treat the active client display limit as configuration-dependent. |
| Ingest-vs-stored identifier | Use an identifier shown in UBKG submission syntax | Do not paste submission syntax into `CodeID`; resolve the stored identifier form. |
| Synonym candidate discovery | Resolve an entity from a broad synonym/name scan | Treat the scan as candidate discovery and confirm source Code/preferred term before traversal. |
| One Code, several Concepts | Compound/drug identifier attached to more than one Concept | Carry/profile the full Concept fan; do not select one arbitrary CUI with `LIMIT 1`. |
| MED-RT endpoint range | Contraindications with contextual endpoints | Inspect returned endpoint Codes before filtering to disease vocabularies; retain valid non-disease context assertions. |

A regression is complete only when the generated query or refusal/stop behavior is inspected against execution output where execution is applicable. These checks are completed before the archive is declared frozen.
