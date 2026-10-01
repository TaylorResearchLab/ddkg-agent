# R8 design specification and freeze manifest

**Status:** pre-freeze design authority  
**Date:** 2026-10-01  
**Repository:** `TaylorResearchLab/ddkg-agent`  
**Branch:** `r8-skill-hardening`  
**DDKG target:** `DataDistillery_2025_04_DEC`  
**R7 base commit:** `57352d09e692c52e1b56afacfdf05851ae6282af`

The purpose of this file is to make the R8 design explicit **before the release is
frozen**. `R8_BUILD.md` records the current release candidate; this file records
what R8 is required to become. If the implementation and this specification
differ, reconcile them before freeze rather than silently changing the design.

The current release candidate predates requirement **R8-D12** below. Its present
archive identity therefore remains a release-candidate identity, not the final
R8 identity.

## 1. R8 objective

R8 is a defect-hardening release for the December 2025 DDKG skill. It is not a
new planner and it is not the MCP execution layer. Its job is to prevent
plausible-looking but scientifically misleading output when the graph, schema,
query, or evidence cannot support the requested conclusion.

The release must preserve these invariants:

1. **The graph determines the result.** The model does not predict what the
   graph should contain.
2. **Diagnostics are gates.** A failed prerequisite stops dependent query
   composition.
3. **Missing data are not biological negatives.** Empty, absent, unsupported,
   failed, and impossible are distinct states.
4. **No silent failure.** A syntactically valid zero, truncation, timeout,
   schema mismatch, entity-level mismatch, or incomplete branch must be
   surfaced when it changes interpretation.
5. **Scientific correctness outranks narrative smoothness.** The skill must not
   omit adverse findings because they weaken the apparent success of an answer.
6. **No invented criticism.** Concerns must be grounded in execution output,
   release structure, source semantics, or a documented failed prerequisite.

## 2. Hardening requirements

| ID | Requirement | R8 behavior | Current RC |
| --- | --- | --- | --- |
| R8-D01 | Diagnostic gates | If a prerequisite check fails, stop dependent composition and state what failed. | implemented |
| R8-D02 | Cross-source comparability | Before intersection, subtraction, or antijoin, verify that both sources meet at the same biological entity and identifier level. | implemented |
| R8-D03 | Direct-link versus route absence | A failed direct edge proves only that the direct edge is absent. Inspect neighboring identifier spaces and documented bridges before declaring the requested route unavailable. | implemented |
| R8-D04 | Display-label integrity | Use a verified source-specific preferred-term edge or fall back to CodeID. Do not take an arbitrary synonym as the display label. | implemented |
| R8-D05 | GTEx quantitative thresholds | Select verified `EXPBINS`/`PVALUEBINS` identifiers; do not assume numeric node properties. | implemented |
| R8-D06 | Truncation and client limits | Count or otherwise bound result size first; treat Browser/client display limits as configuration-dependent and report truncation. | implemented |
| R8-D07 | Identifier-layer boundaries | Keep ingest submission syntax, `Concept.CUI`, and stored `CodeID` values distinct. Resolve the stored identifier form before traversal. | implemented |
| R8-D08 | Synonym scans | Broad name/synonym scans discover candidates only. Confirm source Code and appropriate preferred term before using a candidate as an anchor. | implemented |
| R8-D09 | One Code, several Concepts | Carry or profile the complete Concept fan for an identifier; do not choose one arbitrary CUI with `LIMIT 1`. | implemented |
| R8-D10 | MED-RT endpoint range | Inspect returned endpoint vocabularies before filtering. Do not assume contraindication endpoints are disease-only. | implemented |
| R8-D11 | Query-cost and index-aware resolution | Preserve the R7 repair: inspect active indexes when cost matters, avoid function-wrapped name scans when they defeat useful indexes, stage broad resolution, and use `EXPLAIN`/`PROFILE` when appropriate. | inherited; must regress |
| **R8-D12** | **Scientific adverse-result reporting** | **Negative, null, absent, impossible, unsupported, incomplete, contradictory, truncated, failed, or pending results that materially affect the conclusion must be reported explicitly and prominently.** | **new; required before freeze** |

## 3. Scientific adverse-result reporting contract

R8-D12 is a correctness requirement, not a writing-style preference.

Before giving a final scientific interpretation, the skill must perform a
critical-result audit:

- Did a valid executed query return zero, null, or an unexpected absence?
- Did a prerequisite gate fail?
- Did a query time out, crash, truncate, or remain unexecuted?
- Is a requested source, measurement, property, or biological entity level not
  represented in this DDKG release?
- Do two sources fail to meet at the requested entity level?
- Is only a direct route absent while indirect routes remain untested?
- Is the requested conclusion impossible to derive from the available graph
  representation without external data?
- Is there explicit negative or contradictory evidence, including evidence
  classes such as `Disputed` or `Refuted`?
- Is any part of the answer based on an assumption, pending result, or
  unverified route rather than returned graph data?

If any answer is yes and it changes the interpretation, the finding must appear
in the main answer, not be buried after a positive narrative.

### Required distinctions

The skill must distinguish at least these states in user-facing language:

1. **Validated negative result** - the query and route were checked and the
   graph returned no matching records.
2. **Data absence** - the relevant source, measurement, relationship, or value
   is not represented in the target DDKG release.
3. **Unsupported derivation** - the requested conclusion cannot be derived
   from the represented entity levels or sources.
4. **Execution failure** - the query failed, timed out, crashed, or otherwise
   did not produce an interpretable result.
5. **Incomplete result** - truncation, pagination, an unexecuted branch, or a
   pending step prevents a complete conclusion.
6. **Evidence conflict or negative evidence** - returned evidence weakens,
   disputes, refutes, or contradicts the apparently positive story.

Do not collapse these into "no result."

### Output rules

- If an adverse result changes the headline conclusion, surface it in the first
  substantive summary.
- If a question is partly answerable and partly impossible, answer the
  supported part **and explicitly identify the unsupported part**.
- If a negative result is validated, report it as a result rather than trying
  to replace it with a more positive proxy.
- If a requested derivation is impossible from this release, say why: identify
  the missing source, bridge, property, entity level, or execution result.
- If a direct route is absent, do not call the overall derivation impossible
  until indirect routes have been inspected according to R8-D03.
- If execution has not occurred, do not phrase the proposed query as though its
  expected result were observed.
- Do not hide a failed branch because another branch succeeded.
- Do not invent flaws or overstate uncertainty merely to appear critical.
  Every reported concern must have a concrete basis in the graph, execution
  record, source semantics, or failed prerequisite.

## 4. Why R8-D12 is explicit

A secondary-source article supplied during R8 planning summarized the study
*Language Models Are "Insecure" Reporters*. It reported that, in one planted
negative-result experiment, GPT-5.5 surfaced the negative result in only 2 of
200 baseline reports, while a short honesty instruction increased disclosure
to 190 of 200. The article also describes adversarial reporting scenarios
covering concealed negative/null results, ignored code bugs, hallucinated data,
design flaws, mismatched evidence, collateral damage, incomplete tasks, and
pending tool calls.

R8 does not treat those reported numbers as a benchmark for ddkg.skill. The
design implication is narrower: **scientific adverse findings must be an
explicit reporting obligation rather than something the model is expected to
volunteer spontaneously.**

For ddkg.skill this is especially important because an empty graph result can
mean very different things: a true negative, a missing source, a schema error,
an invalid cross-source comparison, an absent route, truncation, or a failed
query. Hiding that distinction can turn a technical failure into a false
biological conclusion.

## 5. Engineering regression plan before freeze

The focused R8 regressions remain engineering checks, not evidence of
orthogonal generalization. Every generated query that is applicable must be
executed against `DataDistillery_2025_04_DEC`.

Required regression families:

1. diagnostic/set-operation gate;
2. direct-link versus indirect-route inspection;
3. source-specific display labels;
4. GTEx threshold bins;
5. client/configuration-dependent truncation;
6. ingest versus stored identifiers;
7. synonym candidate discovery;
8. one-Code/several-Concept handling;
9. MED-RT endpoint range;
10. query-cost/index-aware resolution;
11. **adverse-result reporting integrity**; and
12. **clean-result control**, to verify that the critical-reporting rule does
    not cause the skill to invent defects when no material defect is present.

The reporting-integrity regression must include a case in which a positive
result coexists with a negative, impossible, incomplete, or failed component.
Passing requires the adverse component to be stated prominently and classified
correctly rather than omitted or softened.

## 6. Freeze criteria

R8 is frozen only when all of the following are true:

- R8-D01 through R8-D12 are implemented in the source skill.
- The reporting-integrity rule is routed to every result-interpretation path
  where it can matter.
- `route.py --check` passes.
- The deterministic archive build passes.
- Focused live engineering regressions pass or have explicitly accepted,
  documented residual failures.
- The archive identity is rebuilt and locked: file count, routing relationship
  count, bytes, and SHA-256.
- The final build record is updated to the frozen identity.
- No source-skill edits occur after freeze during the formal Tier 8 evaluation.

## 7. Tier 8 evaluation after freeze

Tier 8 is created **after** the R8 artifact is frozen.

The Tier 8 packet should:

- use fixed questions not taken from the engineering regressions;
- include source and query-shape coverage not represented in the worked
  examples;
- record all generated Cypher, diagnostic stops, and explicit refusals;
- execute every applicable generated query;
- score from execution behavior, not visual plausibility;
- report n/N rather than only selected successes;
- include at least one adversarial reporting-integrity test in which a
  narrative-changing negative or impossible component is present;
- include a clean control so "critical" behavior is not rewarded for inventing
  a flaw; and
- remain immutable once cross-assistant evaluation begins.

## 8. Successor architecture: R9 route planner

R9 is intentionally outside R8 scope.

The planned R9 improvement is a release-specific transition representation,
approximately an SAB x predicate contact/transition model. Candidate transition
records should encode at least:

`subject_sab, predicate, edge_sab, object_sab, count, direction/role, species`

Route search should be deterministic and risk-aware rather than simply choosing
the fewest hops. The search state should preserve biological entity role and
species so that a mathematically short but biologically invalid path is
rejected.

R9 should be able to:

- find the lowest-risk valid route between source/entity spaces;
- return more than one candidate route when appropriate;
- explain why a requested route is unsupported;
- distinguish no direct edge from no valid path;
- use the same hard gates introduced in R8; and
- preserve R8-D12 so an unsupported route is reported rather than hidden behind
  a superficially related answer.

## 9. Successor architecture: controlled read-only MCP layer

The MCP/backend work is also outside R8 scope.

The intended separation is:

`user -> natural language -> LLM + ddkg.skill -> typed plan -> DDKG MCP server -> DDKG`

The controlled backend should eventually provide:

- identifier resolution;
- schema and route validation;
- typed plan validation;
- Cypher compilation;
- `EXPLAIN`/cost and limit checks;
- read-only execution; and
- explicit return of negative, incomplete, impossible, and failed states to
  the calling model so that R8-D12 can be enforced at the reporting layer.

The skill remains the domain/query-planning intelligence. The MCP server is the
controlled execution boundary.

## 10. Change-control rule

This design specification is the pre-freeze authority for R8 intent.
`R8_BUILD.md` is the record of the built artifact. The engineering regression
file is the executable pre-freeze checklist.

Any new R8 behavior discovered before freeze must be added here first. Any
proposal that changes the planner architecture rather than hardening the
current skill belongs in R9 or the MCP layer unless explicitly promoted into
R8 by project decision.
