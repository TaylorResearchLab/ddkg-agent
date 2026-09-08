# DDKG skill test results — 2026-08-18

**Archive under test:** SHA-256
`098be6ded3618543bbd1833015394c5170d9b238df782f89868586d25639106a`
(the genericized candidate, 287,649 bytes)

**Instance:** CHOP December 2025 CSV release (`DataDistillery_2025_04_DEC`),
Neo4j 5.26.28 Community, August 2025 schema

**Protocol:** `ddkg_test_protocol.md`

> **Superseded.** This run predates the `SKILL.md` size reduction, references
> 14–17, and every repair from the GPT review and the R2 correction. The
> findings below remain informative about the failure classes they document.
> The pass and fail results do **not** transfer to R2
> (`90bcd1d5201408d4303e9ea742db2b7a76baa8d0810b249219fc83373fd76f46`) and
> should not be cited as evidence for it.

---

## Summary

| Tier | Result |
| --- | --- |
| 0 | Pass |
| 1 | 1.1–1.4 pass (1.2 after a rule correction). 1.5 not formally run |
| 2 | All four completed. Real defects found in 2.1, 2.3, 2.4 |
| 3 | Not run |
| 4 | Not run |

## Tier 0 — pass

Returned the per-source `CODE`/`CodeID` table with the reason, and volunteered
a connection stated nowhere in the files: that `CODE` is also the
UBKG-documented name for the structural edge, renamed in this schema. Two
files read and joined.

## Tier 1

**1.1 Gene symbol — pass.** Used `ACR`, cited the validated query, gave the
anchor profile unprompted, and named in advance both the correct result and
the specific wrong one (`HGNC:10671`, SDCCAG8) that would indicate falling
through to `PT`.

**1.2 Absence — fail, then pass.** First attempt asserted "none" from a stored
worked example with confirmation queries appended decoratively. Rule tightened
from "don't predict results" to "don't answer the question yourself"; worked
examples marked as not answer sources; stored results stripped from the
reference files. Re-run opened with "the answer has to come from your run" and
reframed to the IDGP route, which produced real data.

**1.3 Ambiguity — pass.** Disambiguated before generating, then offered
evidence *routes* rather than a source list. Both branches delivered; direct
branch surfaced the canonical septation genes ranked by multi-source support.

**1.4 Evidence semantics — pass.** Caveats stated unprompted in both variants.
Both also predicted `DGN` would dominate, traced to a prediction written into
the evidence-semantics table and contradicted by the real result. Fixed at
source.

## Tier 2

**2.1 Heart expression × CHD phenotype — pass after four rounds.**
Round 1 derived tissue by splitting a `GTEXEXP` CodeID on a fixed delimiter,
populating the column for 2 of 200 genes. Round 2 never finished (six hours).
Round 3 fast and correct, but its own audit column exposed `UBERON:0004550` —
the gastroesophageal junction, caught by a `'cardiac'` filter. Round 4 clean,
with CLINGEN classifications surfaced.

**2.2 eQTLs in chromatin loops — clean pass.** Resolved "within a loop" to
shared `HSCLO` bin membership at anchors, distinguished anchor coincidence
from loop interior, and flagged unprompted that a loop's cell type sits three
hops back on the `4DND` dataset.

**2.3 Metabolites × kidney disease — pass, defects found.** Applied a
`renal`/`adrenal` exclusion generalised from a documented rule. The audit
column then revealed `'kidney'` matching an alkaline phosphatase isoenzyme
assay, and metabolites duplicated across UMLS and minted Concepts.

**2.4 Drugs targeting RAS/MAPK — completed after eight attempts.**
Two domain errors early (NCI is not a pathway vocabulary; Reactome mixes human
and mouse), then five consecutive truncation failures in four different forms,
then a real structural finding: IDGP bioactivity compounds and the clinical
drug vocabularies share no Concepts anywhere in the graph, so "which drugs
target X" is unanswerable on that route. Final result: 5,763 compounds against
29 of 52 pathway proteins, none clinically coded.

## What testing produced

Findings not derivable from documentation, each from running a query:

- Worked examples become cached answers for their entities
- `HAS_SEMANTIC` excludes but cannot select — MSigDB pathway concepts carry
  none
- Truncation amputates whole groups; a query spanning groups must aggregate
- `OPTIONAL MATCH` to `Term` before a `LIMIT` truncates by synonym count
- Errors amplify across hops
- Boolean precedence: `a OR b AND c` applies `c` to one branch
- Group on the identifier the user thinks in, not on `CUI`
- Anatomical and organ strings have false friends, including assay names
- Two sources can be present and share no Concepts

## Standing observation

Mechanical checks stick; advisory rules do not. `--check` on the relationship
index, `keys()` before a numeric filter, count-before-pull are applied
reliably. "Watch for", "consider whether" get written into an answer as a
caveat and violated two lines later in the same query. The truncation rule was
restated three times, each version correcting the mechanism of the last, and
still did not reliably fire.

Five of the eight 2.4 failures were mechanical and would have been caught by a
pre-flight check on the generated Cypher.

---