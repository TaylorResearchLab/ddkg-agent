# GTEx bin schemes: decoded structure and occupancy (addendum, 29 Aug 2026)
Additive reference for the /ddkg skill, from the bin inventory runs on the
December 2025 CSV release.

**The Data Dictionary already documents the bins** — node counts (159 EXPBINS,
17 PVALUEBINS), edge counts, and the ingestion methodology including the
worked `[10,11]` TPM example. Cite it as authoritative for those. What this
file adds and the dictionary does not carry is the **decoded bin scheme**, the
**parse landmines**, and **occupancy**.

**Unresolved discrepancy.** The Data Dictionary records
`GTEXEQTL p_value PVALUEBINS` at 1,251,403 edges against 1,270,900 GTEXEQTL
Codes, which is about 98% coverage. The occupancy figure below totals
1,025,446 and concludes roughly a fifth of eQTL nodes carry no `p_value` edge.
Those disagree by close to the claimed fifth. Either the release changed
between the two measurements, or the occupancy sum counts something other than
edges. **Until resolved, treat the coverage claim as unverified** and use
`OPTIONAL MATCH` on `p_value` for robustness rather than because a gap is
established.

## EXPBINS decoded (159 bins, median TPM, GTEx v8)
Logarithmic by decade, each decade split into ninths, EXCEPT 10 to 100 TPM at
unit width (90 bins, the fine region). Special bins: exact zero
(EXPBINS:0.0.0.0), initial 0 to 0.0007, terminal 100000 to 300000.
Decades: 0.0007-0.001 (0.0001 steps, 3), 0.001-0.01, 0.01-0.1, 0.1-1, 1-10
(ninths each), 10-100 (unit, 90), 100-1e3, 1e3-1e4, 1e4-1e5 (ninths each).
CodeID is `EXPBINS:<lower>.<upper>`, and integer bounds carry an explicit `.0`
decimal, so a bin renders as four dot-separated tokens: the [100,200] bin is
`EXPBINS:100.0.200.0`, not `EXPBINS:100.200`. The dot is both delimiter and
decimal point, which is why the bounds cannot be recovered by splitting on it
without knowing the convention — and why constructing a bin CodeID from
memory fails silently.

**Enumerate before selecting.** `MATCH (c:Code {SAB:'EXPBINS'}) RETURN
c.CodeID ORDER BY c.CodeID` returns the full set; match against what it
returns rather than against a constructed string.

## PVALUEBINS decoded (17 bins, eQTL p-values)
Decades 1e-12 to 0.001, split at 0.005 in the 0.001-0.01 range, linear 0.01
steps to 0.06, terminal high-significance bin 0 to 1e-12. Nothing above 0.06
(significance-filtered source).
LANDMINE, exact form: PVALUEBINS:0.1e-12 means the interval 0 to 1e-12, NOT
0.1e-12. The dot delimiter collides with scientific notation; a naive parse
misreads the most significant bin by an order of magnitude. Used only by
GTEXEQTL via p_value {SAB:'GTEXEQTL'} (single-bin neighborhood evidence;
"only" pending an all-bin sweep).

## Occupancy facts for the December 2025 release
- Exact-zero EXPBINS bin holds 842,108 of ~1.57M measurements: roughly half of
  all gene-tissue pairs have median TPM exactly 0. Guidance: expression-
  anchored queries traverse a minority of the gene-tissue matrix; absence of
  an expression path is the majority state, not a query failure.
- One PVALUEBINS occupancy run totals 1,025,446 against 1,270,900 GTEXEQTL
  Codes, but the Data Dictionary reports 1,251,403 `p_value` edges. The
  missingness rate is therefore **not established**. Guidance: use
  `OPTIONAL MATCH`, report any nulls that actually occur, and do not describe
  a one-fifth coverage gap until the two measurements are reconciled.

## Suggested routing edges (skill_graph.tsv)
expression bin	answers	17_gtex_bins_addendum.md#expbins-decoded
TPM	answers	17_gtex_bins_addendum.md#expbins-decoded
p-value bin	answers	17_gtex_bins_addendum.md#pvaluebins-decoded
pvaluebins	must_read_with	17_gtex_bins_addendum.md#pvaluebins-decoded	the 0.1e-12 misparse landmine
zero expression	answers	17_gtex_bins_addendum.md#occupancy-facts
missing p_value	answers	17_gtex_bins_addendum.md#occupancy-facts
