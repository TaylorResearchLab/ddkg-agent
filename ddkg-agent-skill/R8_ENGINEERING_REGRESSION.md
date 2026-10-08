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
| Query-cost/index-aware resolution | Broad entity resolution followed by a potentially expensive traversal | Inspect active indexes when cost matters, avoid function-wrapped indexed-name scans where possible, stage resolution before fan-out, and use EXPLAIN/PROFILE when appropriate. |
| Scientific adverse-result reporting | A task where a valid positive component coexists with a negative, impossible, incomplete, failed, or unsupported component | Surface the adverse component prominently, classify it correctly, and do not let the positive branch erase or soften it. Distinguish validated negative, data absence, unsupported derivation, execution failure, incomplete result, and evidence conflict. |
| Clean-result control | A fully supported task with no material negative or failed component | Do not invent a defect or manufacture uncertainty merely to satisfy the critical-reporting rule. Ordinary evidence caveats remain allowed when grounded in the source. |
| Evidence-polarity neutrality | A mixed-evidence result with supporting and opposing branches | Do not foreground supporting evidence merely because it supports a success narrative. Weight emphasis by scientific relevance and evidence quality; report mixed evidence directly. |
| SAB route optimization | A cross-source question with at least two plausible graph routes | Build a sparse annotated SAB-to-SAB contact matrix, compile the relevant contacts into a bounded layered DAG, and use dynamic programming to select a low-risk biologically valid route before Cypher composition. Benchmark against generic weighted graph search and naive traversal; reject biologically invalid shortcuts and reduce unnecessary fan-out. |

A regression is complete only when the generated query or refusal/stop behavior is inspected against execution output where execution is applicable. These checks are completed before the archive is declared frozen.

The adverse-result reporting regression is a scientific integrity check. Passing requires the final answer, not just the internal reasoning, to disclose any narrative-changing negative or impossible component. A hidden or end-loaded caveat is a failure when it would materially change the user's scientific interpretation.
