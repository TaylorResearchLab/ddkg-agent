# Tier 7: orthogonal evaluation — complete record

Nine tests, their design, and every result from both run sessions.

**Scope of this record.** This is the historical evaluation record for the R5b-rebased archive used for the manuscript's Tier 7 evaluation. It records the test design, query-stage ledger, execution status, returned results, and resulting revisions. It is not validation of the later R7 archive. Recovered original interactions are included where available, with generated Cypher preserved verbatim and bulky execution output summarized. The query ledger remains the compact index of stages, execution status, and outcomes.

**Archive under test:** SHA-256
`c092480a61f2e46efb3586aacfe2240a3cebb83a0c769c5dfa0eb5ea54b8c52b`
(R5b-rebased; 297,218 bytes, 38 files, 227 routing entries)

**Instance:** DataDistillery_2025_04_DEC, Neo4j 5.26.28 Community. Deployment hostname omitted from the public record.
Property indexes present throughout: `Code.CodeID`, `Code.SAB`,
`Concept.CUI` (RANGE) and `Term.name` (TEXT), plus the two automatic
LOOKUP indexes.

**Sessions.** 2 September 2026: T7.1, T7.2, T7.3, T7.4, T7.8 composed and
executed. 8 September 2026: T7.5, T7.6, T7.7, T7.9 executed, having previously
been assessed on composed queries alone.

**Execution status.** Every test now has at least one executed query. Three
queries do not run: T7.1 stage 2 (never completed), T7.9b (crashed the
instance), and T7.9c (not attempted, sharing 9b's shape). Those failures are
results, not gaps.

## Summary

| Test | Probes | Executed | Outcome |
| --- | --- | --- | --- |
| T7.1 | CLINVAR, negation | stage 1 only | fail |
| T7.2 | DGN, 15.7M edges | yes | correct, with a finding on DGN's model |
| T7.3 | GTEXCOEXP | yes | correct; true negative reached by elimination |
| T7.4 | numeric threshold | yes | correct after four rounds; exposed two false statements in the skill |
| T7.5 | HCOP, MPMGI | yes | correct; one conclusion overstated |
| T7.6 | CLINGEN, OTG | yes | answer void; the skill predicted this and supplied the probe |
| T7.7 | AZ, HMAZ | yes | correct, exactly at the predicted bound |
| T7.8 | MED-RT | yes | correct; falsified the test's own premise |
| T7.9 | partial decline | 1 of 3 queries | decline correct; two queries do not run |

**Five of the seven uncovered-source tests produced correct executed
results** (T7.2, T7.3, T7.5, T7.7, T7.8). T7.6's delivered answer is invalid,
which the skill anticipated. T7.1 failed.



---

Tiers 0–6 reuse entities the skill documents. Every anchor tested so far —
SHH, ALOX5, ABO, astemizole, asthma, frontotemporal dementia, atrial septal
defect, RAS/MAPK — appears in a shipped reference, a verified-anchors table, or
a manuscript query. Those tests measure recall of documented material.

They also inherit a second bias. The skill was built from the User Guide's 51
queries, the manuscript's 11, and the data dictionary's examples. Those are the
DCC authors' chosen biological questions, selected to demonstrate their own
datasets, not to exercise the graph. Tuning a skill to them and then testing on
them measures the fit, not the function.

This tier is designed against both, from two measurements of the shipped
archive.

## Measurement 1 — source coverage

19 of 34 DCC edge sources appear in **zero** queries in the shipped corpus.

| Source | Edges | In corpus |
| --- | --- | --- |
| `DGN` | 15,741,306 | none |
| `GENCODE` | 3,530,426 | none |
| `MSIGDB` | 2,584,008 | none |
| `CMAP` | 2,451,782 | none |
| `GENCODEHSCLO` | 1,181,976 | none |
| `GTEXCOEXP` | 1,078,034 | none |
| `MPMGI` | 438,984 | none |
| `OTG` | 360,466 | none |
| `MW` | 157,502 | none |
| `KF` | 153,380 | none |
| `HCOP` | 135,868 | none |
| `CLINVAR` | 123,344 | none |
| `RATHCOP` | 84,740 | none |
| `WP` | 37,550 | none |
| `NPOSKCAN` | 24,334 | none |
| `CLINGEN` | 6,090 | none |
| `HUBMAP` | 4,548 | none |
| `AZ` | 2,912 | none |
| `GLYCORDF` / `GLYCOCOO` | 230 | none |

The largest gene–disease source in the graph has never been queried in a
shipped example. Well-covered sources — `GTEXEXP`, `4DN`, `GLYCANS`,
`PROTEOFORM`, `LINCS`, `IDGP` — are the ones with DCC use cases.

## Measurement 2 — query shape coverage

Of 53 query blocks in the shipped corpus:

| Shape | Count |
| --- | --- |
| Multi-source union in one query | 10 / 53 |
| Aggregation (`count`, `collect`) | 4 / 53 |
| String `CONTAINS` filter | 3 / 53 |
| Subquery `CALL` | 2 / 53 |
| Ordering by a computed score | 1 / 53 |
| Comparison of two anchors | 1 / 53 |
| **Negation (`NOT`, `NOT EXISTS`)** | **0 / 53** |
| **Set difference / antijoin** | **0 / 53** |
| **`OPTIONAL MATCH`** | **0 / 53** |
| **Numeric threshold on a value** | **0 / 53** |
| **Variable-length path** | **0 / 53** |

The corpus is almost entirely match-and-return. **The skill's rules instruct
behaviours its examples never demonstrate** — "labels are decoration, reach
Terms with `OPTIONAL MATCH`", "a query spanning groups must aggregate",
"threshold by matching bin CodeIDs". A model told to adapt the nearest
validated example is adapting from a corpus that does none of those things.

That tension is worth testing directly, and no earlier tier does.

---

## Test design

Each test names the source and shape it probes, so a failure is diagnostic.
Entities were chosen to appear nowhere in the shipped archive.

Pass criteria are on the generated Cypher **and** on returned grain where the
query is run.

---

---

# T7.1

## Design and 2 September assessment

negation, and an unqueried source

> Which genes are associated with Ehlers-Danlos syndrome in ClinVar but have
> no reported eQTL in GTEx?

**Probes:** `CLINVAR` (zero coverage) and `GTEXEQTL`; negation, absent from the
corpus.

**Pass:** uses `NOT EXISTS { ... }` or an antijoin rather than collecting both
sets and differencing in prose. States that "no eQTL" means no record in the
filtered eQTL set — which retains only eQTLs present in every tissue, so
absence is a strong filter, not an absence of regulation.

**Fail:** returns both lists and leaves the difference to the reader; or treats
the empty side as biological.

**Result (2026-09-02): fail on two mechanical rules.** The reasoning was
strong and the query construction was not.

**Stage 1 amputated.** 100 rows at exactly `LIMIT 100`, `ORDER BY c.SAB`, and
only `DOID` (40) and `MONDO` (60) appear. `OMIM`, `ORDO`, `HP`, `MEDGEN` and
`SNOMEDCT_US` were all requested in the `IN` list and none surfaced — cut off
alphabetically after MONDO.

`SKILL.md` states the test mechanically: if the `ORDER BY` column has fewer
distinct values than the `LIMIT`, the query is wrong. Seven SABs, limit 100.

This mattered more than a usual truncation. The answer's own reasoning said
the ClinVar disease side arrives **through MedGen at subtype level** — and
`MEDGEN` is among the SABs the truncation dropped. The resolution step never
displayed the vocabulary the rest of the analysis depends on.

Also 100 rows for 39 distinct CodeIDs: term-level fanout, one row per synonym,
so the visible code count is smaller than it appears.

**Stage 2 did not complete.** Two costs stack. The disease sweep is
`toLower(t.name) CONTAINS 'ehlers'` with **no SAB filter at all** — unlike
stage 1 — so it scans all 11.1M Terms and matches every vocabulary rather than
the seven. Then `OPTIONAL MATCH (g)-[:located_in|location_of]-(e)` expands
unbounded per gene against a 3.5M-edge predicate, with no `WITH DISTINCT`
reduction between the two halves.

**Corrected stage 1:**

```cypher
MATCH (c:Code)-[tr]->(t:Term)
WHERE toLower(t.name) CONTAINS 'ehlers'
  AND c.SAB IN ['MONDO','ORDO','OMIM','DOID','HP','MEDGEN','SNOMEDCT_US']
RETURN c.SAB, count(DISTINCT c.CodeID) AS codes
ORDER BY codes DESC
```

One row per SAB, no limit, and it answers whether MEDGEN carries EDS at all
before anything downstream is written.

**What was strong.** The ClinVar filtering caveat (v2023-01-05, pathogenic and
likely-pathogenic with assertion criteria met). The observation that GTEx
eQTLs are filtered to those present in every tissue, making "no eQTL" a much
weaker claim than it sounds — and that collagen genes with tissue-restricted
expression are exactly the class that drops out for that reason alone. The
partition design returning every gene with its eQTL count, so the answer and
its own control arrive together. And the disjoint-source diagnostic: if every
gene shows `n_eqtl = 0`, that is a join failure rather than an eQTL desert.

**The pattern.** Interpretation is working; the mechanical rules are not. Both
failing rules are in `SKILL.md` and neither fired.
### Recovered original interaction

**User**

> Which genes are associated with Ehlers-Danlos syndrome in ClinVar but have no reported eQTL in GTEx?

**Claude**

Claude first noted that the ClinVar load was restricted to pathogenic/likely-pathogenic variants with assertion criteria met, and that the GTEx eQTL source was filtered to eQTLs present in every tissue. It therefore framed the requested negative as absence from the filtered DDKG eQTL set rather than absence of all GTEx regulation.

**Stage 1: disease-name resolution**

```cypher
MATCH (c:Code)-[tr]->(t:Term)
WHERE toLower(t.name) CONTAINS 'ehlers'
  AND c.SAB IN ['MONDO','ORDO','OMIM','DOID','HP','MEDGEN','SNOMEDCT_US']
MATCH (concept:Concept)-[:HAS_CODE]->(c)
RETURN c.SAB, c.CodeID, concept.CUI, type(tr) AS term_edge, t.name
ORDER BY c.SAB
LIMIT 100
```

Claude instructed the user to scan the returned terms for false friends before continuing.

**Stage 2: ClinVar genes partitioned by GTEx eQTL count**

```cypher
MATCH (dc:Code)-[]->(t:Term)
WHERE toLower(t.name) CONTAINS 'ehlers'
MATCH (d:Concept)-[:HAS_CODE]->(dc)
MATCH (d)-[r:gene_associated_with_disease_or_phenotype {SAB:'CLINVAR'}]-(g:Concept)
MATCH (g)-[:HAS_CODE]->(hg:Code {SAB:'HGNC'})
WITH DISTINCT g, hg
OPTIONAL MATCH (g)-[:located_in|location_of]-(e:Concept)-[:HAS_CODE]->(:Code {SAB:'GTEXEQTL'})
WITH g, hg, count(DISTINCT e) AS n_eqtl
OPTIONAL MATCH (hg)-[:ACR]->(sym:Term)
RETURN coalesce(sym.name, hg.CodeID) AS gene, n_eqtl,
       n_eqtl = 0 AS no_gtex_eqtl
ORDER BY no_gtex_eqtl DESC, gene
LIMIT 300
```

Claude explicitly supplied a falsification rule: if every returned gene had `n_eqtl = 0`, that pattern should be treated as a likely disjoint-source failure rather than a biological absence of eQTLs. The later execution showed that Stage 1 was truncated by the low-cardinality sort and Stage 2 did not complete.


---

---

# T7.2

## Design and 2 September assessment

an untouched large source

> What does DisGeNET say about hypertrophic cardiomyopathy?

**Probes:** `DGN` at 15.7M edges, never queried in a shipped example.

**Pass:** resolves the condition, uses `refers_to`, and states unprompted that
DisGeNET is literature co-occurrence rather than curated causation. Keys rows
on a Code.

**Fail:** presents the result as gene–disease evidence without the
co-occurrence caveat, or assumes a predicate the source does not use.

**Result (2026-09-02): pass, with a substantive finding about DGN's model.**

**Stage 1 correct, and notable after T7.1.** All eight requested SABs are
represented in 50 rows — no amputation — because the sort is on
`dgn_partners DESC`, a high-cardinality computed column, rather than on the
grouping column. That is the mechanical ordering rule applied correctly, one
test after T7.1 failed it.

Three distinct CUIs, one carrying everything: `C0007194` has **5,569 DGN
partners** and is reached from DOID, MONDO, OMIM, SNOMEDCT_US, HP, MSH, NCI
and ORDO. So DisGeNET attaches at the umbrella concept, not at subtypes —
contradicting the answer's own hypothesis about OMIM's CMH locus series, which
was flagged as a hypothesis rather than asserted.

Minor: the predicate column splits 24 `refers_to` / 26 `inverse_refers_to`,
because the type was left unbound on an undirected match. It does not corrupt
the count, since both members return the same partner set, but it doubles the
rows — which is why 50 rows carry only 3 CUIs.

### The finding: DGN is eight association classes, not one

Stage 2 returned no HGNC partners at all. All 5,569 are `DGN*` association
nodes:

| Partner SAB | n | Apparent class |
| --- | --- | --- |
| `DGNV` | 2,196 | variant–disease |
| `DGNGV` | 1,542 | gene–variant |
| `DGNBM` | 995 | biomarker |
| `DGNCM` | 673 | causal mutation |
| `DGNAGE` | 152 | age of onset |
| `DGNGDA` | 6 | gene–disease association |
| `DGNTH` | 4 | therapeutic |
| `DGNMM` | 1 | — |

These are not interchangeable. `DGNCM` asserts causal mutation; `DGNBM`
asserts biomarker. And `DGNGDA` — the class whose name most suggests
gene–disease association — carries **6** partners against 2,196 for variants.

A user asking what DisGeNET says about HCM and receiving 5,569 associations
would reasonably read them as gene–disease evidence. They are mostly
variant-level, and only six are the curated gene–disease class.

### Consequence for the skill

`11_interpreting_results.md` states that `DGN` `refers_to` is "literature
co-occurrence, not curated causation." That is true at the predicate level and
flattens eight association classes into one sentence — including `DGNCM`,
which asserts causal mutation, and `DGNTH`, therapeutic.

The caveat is right about the aggregate and loses the structure. DGN's
internal model is documented nowhere in the skill, and the answer said so
rather than assuming it: *"the guide doesn't document their internal model, so
the queries below let the graph report the topology rather than assuming it."*

**Proposed addition** to `08_dcc_endpoints.md`: a DGN section recording the
association classes, their relative volumes for a worked anchor, and the rule
that a DGN result should be reported by class rather than as a single count.
Stage 3, which collects `assoc_classes` per gene, is the query shape that
surfaces it.
### Recovered original interaction

**User**

> What does DisGeNET say about hypertrophic cardiomyopathy?

**Claude**

Claude treated the internal DisGeNET model as something to inspect rather than assume.

**Stage 1: resolve HCM and count DGN partners**

```cypher
MATCH (c:Code)-[tr]->(t:Term)
WHERE toLower(t.name) CONTAINS 'hypertrophic cardiomyopathy'
  AND c.SAB IN ['HP','MONDO','ORDO','OMIM','DOID','MEDGEN','SNOMEDCT_US','MSH','NCI']
MATCH (d:Concept)-[:HAS_CODE]->(c)
OPTIONAL MATCH (d)-[r {SAB:'DGN'}]-(x:Concept)
RETURN c.SAB, c.CodeID, d.CUI, t.name AS disease_term,
       type(r) AS dgn_predicate, count(DISTINCT x) AS dgn_partners
ORDER BY dgn_partners DESC
LIMIT 50
```

**Stage 2: inspect the endpoint vocabularies of the DGN partners**

```cypher
MATCH (d:Concept {CUI:'C0007194'})-[:refers_to {SAB:'DGN'}]-(x:Concept)
MATCH (x)-[:HAS_CODE]->(xc:Code)
RETURN xc.SAB AS partner_sab, count(DISTINCT x) AS n
ORDER BY n DESC
LIMIT 20
```

Claude cautioned that `C0007194` should be replaced with the CUI actually returned by Stage 1.

**Stage 3: if the partners are DGN association nodes, traverse through them to genes**

```cypher
MATCH (d:Concept {CUI:'C0007194'})-[:refers_to {SAB:'DGN'}]-(assoc:Concept)
MATCH (assoc)-[:refers_to {SAB:'DGN'}]-(g:Concept)-[:HAS_CODE]->(gc:Code {SAB:'HGNC'})
WHERE g <> d
OPTIONAL MATCH (gc)-[:ACR]->(sym:Term)
OPTIONAL MATCH (assoc)-[:HAS_CODE]->(ac:Code)
RETURN coalesce(sym.name, gc.CodeID) AS gene,
       collect(DISTINCT ac.SAB) AS assoc_classes,
       count(DISTINCT assoc) AS n_assoc
ORDER BY n_assoc DESC
LIMIT 50
```

The original response explicitly said that Stage 2, not prior documentation, should determine whether the intermediate association-node hop was required. Stage 3 was composed but not executed in the formal test.


---

---

# T7.3

## Design and 2 September assessment

a source with a documented quirk and no example

> Which genes are strongly co-expressed with PCSK9?

**Probes:** `GTEXCOEXP` at 1.1M edges, zero coverage. The skill documents that
an edge means "correlated above 0.99 in at least one tissue" with no
coefficient to filter on.

**Pass:** states that the threshold is baked into the edge and there is no
value to rank by, so "strongly" cannot be graded further within the graph.

**Fail:** invents a coefficient property, or offers a numeric threshold.

**Result (2026-09-02): pass**, and the strongest empty-result handling in any
tier so far.

**Criterion met in the opening lines**, unprompted: *"The edge is a binary tag,
so 'strongly' means that 0.99 threshold. There's no coefficient stored to rank
or filter on, and no tissue identity on the edge itself."* No invented
property, no numeric threshold offered.

**The query was well-formed and the zero was real.** `coexpressed_with` under
`GTEXCOEXP` is verified in the registry at 539,017 edges each direction, and
exists under no other SAB. PCSK9 has no partner above r > 0.99 in any tissue.

**Empty-result diagnosis executed in order**, matching reference 13's method:
schema discriminator, then resolution with `STARTS WITH` (citing the
trailing-whitespace hazard), then an unfiltered anchor profile, and only then
a SAB-filtered confirmation. The negative was not accepted until the last
step.

When only rows 33–50 of the profile were pasted back, it noted the profile was
sorted descending so rows 1–32 were where a co-expression predicate would sit,
and wrote a query that did not depend on seeing them.

**The substitution was correctly characterised.** Offered MSigDB co-membership
and STRING as different claims rather than fallbacks, and when the MSigDB rows
came back dominated by `inverse_targets_expression_of_gene`, identified those
as shared TF/miRNA targeting — co-regulation by inference — and steered to the
expression-derived signature and marker sets instead.

**Final result grain clean.** 40 rows, 40 distinct HGNC codes, every partner
named, aggregation before term expansion. Partners are F10, PLG, AGT, C1R, F2,
SERPINC1, ITIH1, ANG — coagulation, complement, serpins, angiotensinogen:
the hepatocyte secretory program, which is where PCSK9 sits. The answer's own
caution about generic housekeeping hits did not materialise.

### Recovered original interaction

The original Claude interaction for T7.3 was recovered on 26 September 2026 from the shared September 2 conversation. UI chrome and repeated interface text are omitted below. The generated Cypher is preserved verbatim; execution outputs are summarized where the full row dump is not needed to identify the stage.

**User**

> Which genes are strongly co-expressed with PCSK9?

**Claude**

Claude first stated that `GTEXCOEXP` is a binary edge indicating a Pearson correlation above 0.99 in at least one GTEx tissue, with no stored coefficient or tissue identity to rank further. It then generated:

```cypher
MATCH (gc:Code {SAB:'HGNC'})-[:ACR]->(gt:Term)
WHERE trim(gt.name) = 'PCSK9'
MATCH (g:Concept)-[:HAS_CODE]->(gc)
MATCH (g)-[r:coexpressed_with]-(p:Concept)
MATCH (p)-[:HAS_CODE]->(pc:Code {SAB:'HGNC'})
OPTIONAL MATCH (pc)-[:ACR]->(pt:Term)
RETURN DISTINCT coalesce(trim(pt.name), pc.CodeID) AS partner,
       pc.CodeID AS hgnc, r.SAB AS source
ORDER BY partner
LIMIT 100
```

It also supplied a truncation check:

```cypher
MATCH (gc:Code {SAB:'HGNC'})-[:ACR]->(gt:Term)
WHERE trim(gt.name) = 'PCSK9'
MATCH (g:Concept)-[:HAS_CODE]->(gc)
MATCH (g)-[r:coexpressed_with]-(p:Concept)
RETURN count(DISTINCT p) AS n_partners
```

**User**

> It returns 0

**Claude**

Claude then generated three diagnostics in sequence.

**1. Schema discriminator**

```cypher
CALL db.relationshipTypes() YIELD relationshipType
WHERE relationshipType IN ['CODE','HAS_CODE']
RETURN collect(relationshipType) AS concept_code_edge
```

**2. PCSK9 resolution**

```cypher
MATCH (gc:Code {SAB:'HGNC'})-[:ACR]->(gt:Term)
WHERE trim(gt.name) STARTS WITH 'PCSK9'
RETURN gc.CodeID, gt.name
LIMIT 10
```

**3. Unfiltered anchor profile**

```cypher
MATCH (gc:Code {SAB:'HGNC'})-[:ACR]->(gt:Term)
WHERE trim(gt.name) STARTS WITH 'PCSK9'
MATCH (g:Concept)-[:HAS_CODE]->(gc)
MATCH (g)-[r]-(:Concept)
RETURN type(r) AS predicate, r.SAB AS source, count(*) AS n
ORDER BY n DESC
LIMIT 50
```

The schema check returned `HAS_CODE`. PCSK9 resolved to `HGNC:20001`, `PCSK9`. The anchor profile returned exactly 50 rows and was therefore truncated; the pasted tail contained only relationships with counts of two or one.

Claude then generated a direct source-specific confirmation:

```cypher
MATCH (g:Concept)-[:HAS_CODE]->(:Code {CodeID:'HGNC:20001'})
MATCH (g)-[r]-(p:Concept)
WHERE r.SAB = 'GTEXCOEXP'
RETURN type(r) AS predicate, count(DISTINCT p) AS n_partners
```

and, separately, an alternative-source inspection:

```cypher
MATCH (g:Concept)-[:HAS_CODE]->(:Code {CodeID:'HGNC:20001'})
MATCH (g)-[r]-(p:Concept)
WHERE r.SAB IN ['STRING','MSIGDB']
MATCH (p)-[:HAS_CODE]->(pc:Code)
OPTIONAL MATCH (pc)-[:ACR]->(pt:Term)
RETURN type(r) AS predicate, r.SAB AS source,
       coalesce(trim(pt.name), pc.CodeID) AS partner
LIMIT 100
```

**User**

The `GTEXCOEXP` confirmation returned no records. The STRING/MSigDB inspection returned 80 rows; the visible tail was dominated by MSigDB gene-set nodes, including `inverse_targets_expression_of_gene`, `inverse_has_marker_gene`, and `inverse_has_signature_gene`.

**Claude**

Claude treated the zero as a confirmed negative for `GTEXCOEXP` in this release, then explained that the MSigDB neighbors were gene-set nodes rather than partner genes. It generated a two-hop co-membership query restricted to signature and marker sets:

```cypher
MATCH (g:Concept)-[:HAS_CODE]->(:Code {CodeID:'HGNC:20001'})
MATCH (g)-[r1:inverse_has_signature_gene|inverse_has_marker_gene]-(s:Concept)
MATCH (s)-[r2:has_signature_gene|has_marker_gene]-(p:Concept)
WHERE p <> g
MATCH (p)-[:HAS_CODE]->(pc:Code {SAB:'HGNC'})
WITH pc, count(DISTINCT s) AS shared_sets
ORDER BY shared_sets DESC
LIMIT 40
OPTIONAL MATCH (pc)-[:ACR]->(pt:Term)
RETURN coalesce(trim(pt.name), pc.CodeID) AS partner, pc.CodeID AS hgnc, shared_sets
```

This is the eight-stage sequence summarized in the query ledger below: initial query, optional count check, schema check, resolution check, anchor profile, explicit `GTEXCOEXP` confirmation, STRING/MSigDB inspection, and MSigDB co-membership query.

### Two observations

**The ranking barely discriminates.** `shared_sets` runs 1 to 3, with one gene
at 3 and 39 of 40 at 1 or 2. The answer flagged the cause in advance — counts
inflated by large sets and MSigDB's internal redundancy, so shared sets are
not independent observations — and proposed weighting by set size as the
refinement. Worth doing; as returned, the ordering carries little information.

**One line drifts from reporting a null to explaining it.** "No pair exceeded
r = 0.99 in any single tissue" is precise. Adding that this is *"unsurprising
for a gene with PCSK9's profile — expression concentrated in liver"* is
plausible biology the graph did not show. Minor, and it did not affect the
query, but it is the shape the no-prediction rule guards against.

---

---

# T7.4

## Design and 2 September assessment

numeric threshold, a shape the corpus never demonstrates

> List genes expressed above 100 TPM in pancreas.

**Probes:** `GTEXEXP` with a real threshold; bin selection, which no shipped
query performs.

**Pass:** enumerates or matches `EXPBINS` CodeIDs rather than filtering on a
numeric property, since the bounds are null. Notes that roughly half of all
gene–tissue pairs sit in the exact-zero bin. Groups by measurement Code.

**Fail:** writes `bin.lowerbound >= 100`, which returns null for every row; or
parses the CodeID by splitting.

**Result (2026-09-02): pass on outcome after four rounds — and it exposed two
documented facts that are wrong.**

**Final result clean.** 314 rows, 314 distinct HGNC codes, no duplication,
under the 500 cap so the list is complete. The biology is exactly right for
bulk adult pancreas: PRSS2, PRSS1, REG1A, CPA1, CELA3A, CLPS, PNLIP, CTRB2 —
the acinar secretory program in descending order, with mitochondrial
transcripts interleaved as expected in any high-expression tail.

The criterion was met: bins were selected by matching CodeIDs, never by a
numeric property, and the answer stated up front that expression values are
bin Concepts rather than numeric properties.

### Defect 1 — reference 17's stated bin format is wrong

Reference 17 line 27 reads *"CodeID is EXPBINS:lower.upper"*. Line 24 of the
same file shows `EXPBINS:0.0.0.0`. The prose describes two tokens; the example
has four.

Integer bounds carry explicit `.0` decimals: the [100,200] bin is
**`EXPBINS:100.0.200.0`**, not `EXPBINS:100.200`. Two constructed bin lists
were built from the stated convention and both matched nothing, silently.

### Defect 2 — reference 08's symmetric-predicate claim does not hold from the tissue side

Reference 08 states that `expresses` and `expressed_in` are duplicate
symmetric predicates, *"each connects the measurement Concept to both the gene
and the tissue"*, and that *"neither the predicate name nor the arrow
direction tells you which end you reached."*

The registry confirms the pair — 4,145,472 edges each. But on this release the
tissue side materialises **`expresses`** only. Binding `expressed_in` from the
tissue zeroed the chain at hop one.

The documented claim is what made that binding look safe.

### The recovery is the valuable part

After two dead constructed lists, it stopped constructing. It wrote a
diagnostic walking the chain with **predicates unbound**, returning `type(r)`
at each hop and sampling actual bin CodeIDs, designed so either failure mode
would be visible in one paste:

```cypher
MATCH (tissue:Concept)-[:HAS_CODE]-(:Code {CodeID:'UBERON:0001150'})
MATCH (tissue)-[r {SAB:'GTEXEXP'}]-(m:Concept)
WITH type(r) AS tissue_edge, m LIMIT 5000
OPTIONAL MATCH (m)-[r2 {SAB:'GTEXEXP'}]-(b:Concept)-[:HAS_CODE]-(bc:Code {SAB:'EXPBINS'})
RETURN tissue_edge, type(r2) AS bin_edge, count(DISTINCT m) AS measurements,
       collect(DISTINCT bc.CodeID)[..30] AS sample_bins
```

It also enumerated the correct answer for each possible outcome before seeing
it — which predicate name would indicate which failure — so the result was
diagnostic rather than merely informative.

The working query then selects bins by a four-token parse on the first token,
which separates ≥100 without hitting the delimiter-as-decimal ambiguity, and
**verified the parse returned 28 bins before using it**.

### Notable

The tissue anchor was `UBERON:0001150`, not the obvious pancreas code. The
answer had predicted this failure mode in advance, citing the documented heart
case where GTEx files tissues under more specific UBERON codes than expected,
and supplied the resolution query for it.

Four rounds is slow, but each round eliminated a specific hypothesis and none
repeated a failed approach.
### Recovered original multi-turn interaction

The original T7.4 interaction was iterative. The failed and corrected queries are retained because the test's main finding came from execution exposing two false assumptions in the skill.

**User**

> List genes expressed above 100 TPM in pancreas.

**Claude: initial query**

```cypher
WITH ['EXPBINS:100.200','EXPBINS:200.300','EXPBINS:300.400','EXPBINS:400.500',
      'EXPBINS:500.600','EXPBINS:600.700','EXPBINS:700.800','EXPBINS:800.900',
      'EXPBINS:900.1000','EXPBINS:1000.2000','EXPBINS:2000.3000','EXPBINS:3000.4000',
      'EXPBINS:4000.5000','EXPBINS:5000.6000','EXPBINS:6000.7000','EXPBINS:7000.8000',
      'EXPBINS:8000.9000','EXPBINS:9000.10000','EXPBINS:10000.20000','EXPBINS:20000.30000',
      'EXPBINS:30000.40000','EXPBINS:40000.50000','EXPBINS:50000.60000','EXPBINS:60000.70000',
      'EXPBINS:70000.80000','EXPBINS:80000.90000','EXPBINS:90000.100000','EXPBINS:100000.300000'] AS hi_bins
MATCH (tissue:Concept)-[:HAS_CODE]->(:Code {CodeID:'UBERON:0001264'})
MATCH (tissue)-[:expressed_in {SAB:'GTEXEXP'}]-(m:Concept)
MATCH (m)-[:has_expression {SAB:'GTEXEXP'}]-(:Concept)-[:HAS_CODE]->(bin:Code {SAB:'EXPBINS'})
WHERE bin.CodeID IN hi_bins
MATCH (m)-[:expressed_in {SAB:'GTEXEXP'}]-(g:Concept)
WHERE g <> tissue
MATCH (g)-[:HAS_CODE]->(hg:Code {SAB:'HGNC'})
OPTIONAL MATCH (hg)-[:ACR]->(sym:Term)
RETURN DISTINCT coalesce(sym.name, hg.CodeID) AS gene, hg.CodeID AS hgnc_id, bin.CodeID AS tpm_bin
ORDER BY tpm_bin DESC, gene
LIMIT 500
```

Claude also generated a bin-format verification:

```cypher
MATCH (b:Code {SAB:'EXPBINS'})
WHERE b.CodeID STARTS WITH 'EXPBINS:1' OR b.CodeID STARTS WITH 'EXPBINS:2'
   OR b.CodeID STARTS WITH 'EXPBINS:3' OR b.CodeID STARTS WITH 'EXPBINS:4'
   OR b.CodeID STARTS WITH 'EXPBINS:5' OR b.CodeID STARTS WITH 'EXPBINS:6'
   OR b.CodeID STARTS WITH 'EXPBINS:7' OR b.CodeID STARTS WITH 'EXPBINS:8'
   OR b.CodeID STARTS WITH 'EXPBINS:9'
RETURN collect(b.CodeID) AS bins
```

and an initial pancreas-resolution query:

```cypher
MATCH (m:Concept)-[:has_expression {SAB:'GTEXEXP'}]-(:Concept)
WITH m LIMIT 100000
MATCH (m)-[:expressed_in {SAB:'GTEXEXP'}]-(t:Concept)-[:HAS_CODE]->(uc:Code {SAB:'UBERON'})
OPTIONAL MATCH (uc)-[:PT]->(tt:Term)
WITH uc.CodeID AS ub, coalesce(tt.name, uc.CodeID) AS name, count(*) AS n
WHERE toLower(name) CONTAINS 'pancrea'
RETURN ub, name, n
```

**User**

> No changes, no records.

**Claude: discriminate tissue-anchor versus bin failure**

```cypher
MATCH (tissue:Concept)-[:HAS_CODE]->(:Code {CodeID:'UBERON:0001264'})
OPTIONAL MATCH (tissue)-[r {SAB:'GTEXEXP'}]-(:Concept)
RETURN count(DISTINCT tissue) AS anchor_concepts, count(r) AS gtexexp_edges
```

Claude additionally supplied a no-bin-filter check:

```cypher
MATCH (tissue:Concept)-[:HAS_CODE]->(:Code {CodeID:'UBERON:0001264'})
MATCH (tissue)-[:expressed_in {SAB:'GTEXEXP'}]-(m:Concept)
MATCH (m)-[:has_expression {SAB:'GTEXEXP'}]-(:Concept)-[:HAS_CODE]->(bin:Code {SAB:'EXPBINS'})
RETURN bin.CodeID AS bin, count(*) AS n
ORDER BY n DESC
```

**User**

> anchor concepts =1, gtexexp edges=0

**Claude: resolve the actual GTEx pancreas anchor**

```cypher
MATCH (uc:Code {SAB:'UBERON'})-[]->(t:Term)
WHERE toLower(t.name) CONTAINS 'pancrea'
WITH DISTINCT uc, collect(DISTINCT t.name) AS names
MATCH (c:Concept)-[:HAS_CODE]->(uc)
OPTIONAL MATCH (c)-[r {SAB:'GTEXEXP'}]-(:Concept)
RETURN uc.CodeID AS ub, names, count(r) AS gtexexp_edges
ORDER BY gtexexp_edges DESC
LIMIT 50
```

The returned table identified `UBERON:0001150` (body of pancreas) as the only pancreatic UBERON code with GTEXEXP edges.

Claude then reran the main query with that anchor but still using the original predicate and bin assumptions:

```cypher
WITH ['EXPBINS:100.200','EXPBINS:200.300','EXPBINS:300.400','EXPBINS:400.500',
      'EXPBINS:500.600','EXPBINS:600.700','EXPBINS:700.800','EXPBINS:800.900',
      'EXPBINS:900.1000','EXPBINS:1000.2000','EXPBINS:2000.3000','EXPBINS:3000.4000',
      'EXPBINS:4000.5000','EXPBINS:5000.6000','EXPBINS:6000.7000','EXPBINS:7000.8000',
      'EXPBINS:8000.9000','EXPBINS:9000.10000','EXPBINS:10000.20000','EXPBINS:20000.30000',
      'EXPBINS:30000.40000','EXPBINS:40000.50000','EXPBINS:50000.60000','EXPBINS:60000.70000',
      'EXPBINS:70000.80000','EXPBINS:80000.90000','EXPBINS:90000.100000','EXPBINS:100000.300000'] AS hi_bins
MATCH (tissue:Concept)-[:HAS_CODE]->(:Code {CodeID:'UBERON:0001150'})
MATCH (tissue)-[:expressed_in {SAB:'GTEXEXP'}]-(m:Concept)
MATCH (m)-[:has_expression {SAB:'GTEXEXP'}]-(:Concept)-[:HAS_CODE]->(bin:Code {SAB:'EXPBINS'})
WHERE bin.CodeID IN hi_bins
MATCH (m)-[:expressed_in {SAB:'GTEXEXP'}]-(g:Concept)
WHERE g <> tissue
MATCH (g)-[:HAS_CODE]->(hg:Code {SAB:'HGNC'})
OPTIONAL MATCH (hg)-[:ACR]->(sym:Term)
RETURN DISTINCT coalesce(sym.name, hg.CodeID) AS gene, hg.CodeID AS hgnc_id, bin.CodeID AS tpm_bin
ORDER BY tpm_bin DESC, gene
LIMIT 500
```

This again returned no records.

**Claude: graph-driven chain diagnostic**

```cypher
MATCH (tissue:Concept)-[:HAS_CODE]-(:Code {CodeID:'UBERON:0001150'})
MATCH (tissue)-[r {SAB:'GTEXEXP'}]-(m:Concept)
WITH type(r) AS tissue_edge, m
LIMIT 5000
OPTIONAL MATCH (m)-[r2 {SAB:'GTEXEXP'}]-(b:Concept)-[:HAS_CODE]-(bc:Code {SAB:'EXPBINS'})
RETURN tissue_edge, type(r2) AS bin_edge,
       count(DISTINCT m) AS measurements,
       collect(DISTINCT bc.CodeID)[..30] AS sample_bins
```

The returned diagnostic showed `expresses` from the tissue side and bins such as `EXPBINS:100.0.200.0`. Claude then verified the corrected four-token parse:

```cypher
MATCH (bin:Code {SAB:'EXPBINS'})
WITH bin.CodeID AS id, split(replace(bin.CodeID,'EXPBINS:',''),'.') AS p
WHERE size(p) = 4 AND toInteger(p[0]) >= 100
RETURN count(*) AS n_bins, collect(id) AS bins
```

and generated the final working query:

```cypher
MATCH (bin:Code {SAB:'EXPBINS'})
WITH bin, split(replace(bin.CodeID,'EXPBINS:',''),'.') AS p
WHERE size(p) = 4 AND toInteger(p[0]) >= 100
WITH collect(bin) AS hi_bins
MATCH (tissue:Concept)-[:HAS_CODE]-(:Code {CodeID:'UBERON:0001150'})
MATCH (tissue)-[r1 {SAB:'GTEXEXP'}]-(m:Concept)
MATCH (m)-[r2 {SAB:'GTEXEXP'}]-(bc:Concept)-[:HAS_CODE]-(bin:Code {SAB:'EXPBINS'})
WHERE bin IN hi_bins
MATCH (m)-[r3 {SAB:'GTEXEXP'}]-(g:Concept)-[:HAS_CODE]-(hg:Code {SAB:'HGNC'})
WHERE g <> tissue
OPTIONAL MATCH (hg)-[:ACR]-(sym:Term)
RETURN DISTINCT coalesce(sym.name, hg.CodeID) AS gene,
       hg.CodeID AS hgnc_id,
       bin.CodeID AS tpm_bin,
       toInteger(split(replace(bin.CodeID,'EXPBINS:',''),'.')[0]) AS tpm_lower
ORDER BY tpm_lower DESC, gene
LIMIT 500
```

The final execution returned 314 distinct HGNC genes and did not hit the row cap.


---

---

# T7.5

## Design and 2 September assessment

cross-species, deliberate rather than accidental

> Which mouse phenotypes are associated with human orthologs of genes in the
> ciliary transition zone?

**Probes:** `HCOP` and `MPMGI`, both zero coverage; the deliberate
cross-species route rather than the accidental contamination Tier 5.3 tested.

**Pass:** uses `HCOP` for orthology and `MPMGI` for mouse phenotype, names both
as mouse sources, and distinguishes this intended use from silent
contamination. Handles "ciliary transition zone" as a set requiring definition,
not a single anchor.

**Fail:** returns mouse phenotypes without saying they are mouse; or treats the
gene set as resolvable from one term.

**Result (2026-09-02): pass on every criterion, and it improved on the test
design.**

All predicate claims verified against the registry:
`in_1_to_1_orthology_relationship_with` under `HCOP` at 67,934;
`involved_in` under `MPMGI` at 219,492; `is_approximately_equivalent_to` under
`HPOMP` at exactly 1,226 — the figure quoted. The only gene-to-GO route is
NCI's `process_involves_gene` (biological process); `part_of` under `GO` at
8,582 is GO-internal structure, not gene membership.

**It made the gene set an empirical question rather than a judgement call.**
The test expected "ciliary transition zone" to be treated as a set requiring
definition. Instead it asked whether the graph can supply the set at all —
profiling `GO:0035869` with a falsification criterion stated in advance: if
every row is GO-internal, no source asserts gene membership and the set must
come from outside. That establishes *why* curation is necessary rather than
asserting that it is.

**Cross-species handling is unambiguous throughout.** "MGI mouse gene",
"MPMGI, built from MGI/IMPC genotype-phenotype data", "a mouse carrying a
disrupted allele of that gene shows the phenotype". No reading of the output
as human is available.

### Three caveats beyond the criterion

**`involved_in` under MPMGI is knockout evidence** — a mutant-allele mouse
displaying the phenotype — not expression or association. The output is
loss-of-function phenotype space. This semantic is documented nowhere in the
skill.

**HCOP carries 1:1 orthologs only**, so a human gene without a clean 1:1 mouse
ortholog drops out silently and its absence is a mapping artefact rather than
a biological negative. With the diff instruction: compare returned genes
against the input list.

**The `LIMIT` truncates by gene, not phenotype**, so per-gene lists are
complete while the roster may be cut. Grain stated before the result, which is
what Tier 6 found missing.

The HPOMP note is well-calibrated: 1,226 assertions is thin, expect
substantial loss, treat the mapped subset as a lower bound.

---

---

### Recovered original 2 September interaction

A separate original Claude interaction for the formal T7.5 test was recovered on 26 September 2026. This resolves an apparent discrepancy with a different exploratory ciliary-transition-zone chat that used a 19-gene seed list. The formal Tier 7 test used the 17-gene seed list below; the 19-gene interaction is therefore not substituted into this evaluation record.

**User**

> Which mouse phenotypes are associated with human orthologs of genes in the ciliary transition zone?

**Claude**

Claude first treated direct gene membership in `GO:0035869` as an empirical question and generated an anchor profile:

```cypher
MATCH (a:Concept)-[:HAS_CODE]->(:Code {CodeID:'GO:0035869'})
MATCH (a)-[r]-(:Concept)
RETURN type(r) AS predicate, r.SAB AS sab, count(*) AS n
ORDER BY n DESC
LIMIT 30
```

It stated the falsification criterion in advance: if the profile were entirely GO-internal, the graph would not directly supply the gene set; if a gene-bearing predicate appeared, that predicate should be used instead.

For the cross-species query it then supplied a 17-gene seed list:

```cypher
WITH ['CEP290','TMEM67','MKS1','B9D1','B9D2','CC2D2A','TCTN1','TCTN2','TCTN3',
      'AHI1','NPHP1','NPHP4','RPGRIP1L','TMEM216','TMEM231','TMEM138','TMEM237'] AS symbols
MATCH (hc:Code {SAB:'HGNC'})-[:ACR]->(ht:Term)
WHERE ht.name IN symbols
MATCH (hg:Concept)-[:HAS_CODE]->(hc)
MATCH (hg)-[:in_1_to_1_orthology_relationship_with {SAB:'HCOP'}]-(mg:Concept)
MATCH (mg)-[:involved_in {SAB:'MPMGI'}]-(mp:Concept)
MATCH (mp)-[:HAS_CODE]->(mpc:Code {SAB:'MP'})
WITH ht.name AS gene, collect(DISTINCT mpc) AS mp_codes
UNWIND mp_codes AS mpc
OPTIONAL MATCH (mpc)-[:PT]->(mt:Term)
RETURN gene,
       collect(DISTINCT coalesce(mt.name, mpc.CodeID)) AS mouse_phenotypes
ORDER BY gene
LIMIT 50
```

Claude explicitly characterized the two bridge assertions: HCOP contributes 1:1 orthology, so a human gene without a clean 1:1 mouse ortholog can disappear as a mapping artifact; MPMGI `involved_in` is knockout/mutant-allele phenotype evidence, not expression or generic association evidence. It also noted that the `LIMIT` applies after grouping by gene, so phenotype lists for returned genes are complete even if the gene roster is capped.

This recovered interaction matches the 17-seed formal test summarized in the ledger below. A separate 19-gene exploratory interaction recovered from Claude added `TMEM107` and `TMEM17`; that interaction is retained separately and should not be used to overwrite the formal T7.5 test history.

## 8 September execution

### 5a: the skill's falsification criterion was met

No `HGNC` appears in the `GO:0035869` profile. The neighbourhood is
`has_part`/`part_of` under `UNIPROTKB` (67 each), `part_of`/`has_part` under
`GO` (7), `ro` under `GO` (4), and `isa` pairs under `MP` and `GO`.

The skill's stated test was that a wholly GO-internal profile means no source
asserts gene membership and the set must be curated. That was the right call,
and the decision to hand curation to the user was correct.

**One overstatement.** The skill concluded the gene set "has to come in from
outside the graph." It does not: **67 UniProtKB proteins are `part_of` the
ciliary transition zone term**, and `gene_product_of` reaches HGNC from there.
So a graph-derived set exists at the protein layer. The skill established
correctly that no *direct gene* membership exists and drew a broader conclusion
than the evidence supported.

### 5b: 16 of 17 genes, exactly as predicted

Only `TMEM216` dropped. The skill anticipated this precisely, instructing the
user to diff returned genes against the input list because HCOP carries 1:1
orthologs only and a missing gene is a mapping artifact rather than a
biological negative. One drop of seventeen is consistent with that.

---

---

# T7.6

## Design and 2 September assessment

set difference across two unqueried sources

> Which genes have ClinGen gene–disease validity assertions but no OTG
> variant–disease association?

**Probes:** `CLINGEN` (6,090 edges) and `OTG` (360,466), both zero coverage;
antijoin across sources, never demonstrated.

**Pass:** antijoin rather than two lists. Returns ClinGen's `evidence_class`
and notes it can be `Disputed` or `Limited`, so presence is not endorsement.
States that OTG absence reflects GWAS coverage.

**Fail:** counts a ClinGen hit as support without reading the classification;
or reports the difference as biologically meaningful without naming both
coverage limits.

**Result (2026-09-02): pass on all criteria.**

Figures verified: `gene_disease_validity` under `CLINGEN` at 2,350,
`has_variant_associated_with_disease` under `OTG` at 180,233. The cost note is
correct — the relationship-type index serves 2,350 edges without property
indexes.

**A real antijoin**, `NOT EXISTS { (g)-[:has_variant_associated_with_disease]-() }`,
not two lists differenced in prose. `evidence_class` returned, with the
distinction stated sharply: *a gene with only a `Disputed` classification "has
a ClinGen assertion" in the letter of your question but the panel came away
doubting the relationship.* OTG absence characterised as GWAS tractability
rather than a property of the gene.

### Three things beyond the criterion

**It named the ambiguity and picked one, explicitly.** "Genes with no OTG
association to anything" and "ClinGen gene-disease pairs where that disease
has no OTG signal" are different sets. It implemented the first, said so, and
offered the second — a clarifying question that narrows intent without
stalling for an answer.

**It probed granularity before differencing.** OTG is variant-level evidence
and its attachment point is undocumented, so the first query samples 500 edges
and returns the endpoint Code SABs, with the falsification stated in advance:
if `HGNC` does not appear, the difference set is a granularity artefact rather
than biology. Establishing that a join is well-posed before computing a set
difference across it is the right order, and no shipped example demonstrates
it.

**Count before listing**, with the 500-row cap flagged against the count.

### The contrast with T7.1

Same tier, same shape — an antijoin across two zero-coverage sources — and
opposite outcomes. T7.1 amputated its resolution step under a low-cardinality
sort and then ran an unbounded expansion that did not complete. T7.6 probed,
counted, then listed.

The difference is not knowledge of the rules. It is that here the mechanical
steps were sequenced as separate queries, each with its own falsification
criterion, rather than compressed into one query that had to be right first
time.

---

---

## 8 September execution

### 6a: no `HGNC` among the endpoints

OTG's `has_variant_associated_with_disease` connects `HSCLO` genomic locations
to disease vocabularies (`HP`, `MONDO`, `DOID`, `OMIM`, `SNOMEDCT_US`, `ORDO`,
`MSH` and many clinical terminologies). **It never reaches genes.**

The skill's stated criterion: *"If `HGNC` appears in that list, the set
difference is well-posed."* It does not appear.

### 6b: confirmed decisively

```
clingen_genes  with_otg  without_otg
         1935         0         1935
```

Every ClinGen gene lacks an OTG association, because no gene can have one. A
100% difference is the signature of a disjoint join, which is exactly what the
skill warned would indicate a granularity artifact rather than biology.

### 6c: 500 rows, truncated, and biologically meaningless

The list presents 1,935 genes as lacking OTG support when the comparison
cannot be made. A user who ran 6c without running 6a first would receive a
plausible-looking gene list that means nothing.

**How to grade this.** The skill diagnosed the failure in advance, supplied the
probe that detects it, and stated what a zero would mean. That is the behavior
the skill is for. It also composed and offered the invalid query, and the
protection depends on the user running the stages in order.

### What 6c does establish

The `clingen_classes` column confirms the skill's claim that a ClinGen
assertion can express doubt:

| Classification | Rows |
| --- | --- |
| Definitive | 304 |
| Limited | 64 |
| Moderate | 42 |
| **Disputed** | **16** |
| Strong | 8 |
| mixed combinations | 26 |

Sixteen genes carry a `Disputed` call. Counting a ClinGen hit as support would
invert the finding for those, which is what the skill's guidance says.
### Recovered original interaction

**User**

> Which genes have ClinGen gene-disease validity assertions but no OTG variant-disease association?

**Claude**

Claude distinguished gene-wide absence from pairwise disease-specific absence and implemented the gene-wide reading. Before differencing, it generated an endpoint-granularity probe:

```cypher
MATCH (a:Concept)-[r:has_variant_associated_with_disease]-(b:Concept)
WITH a, b LIMIT 500
OPTIONAL MATCH (a)-[:HAS_CODE]->(ca:Code)
OPTIONAL MATCH (b)-[:HAS_CODE]->(cb:Code)
RETURN collect(DISTINCT ca.SAB) + collect(DISTINCT cb.SAB) AS endpoint_code_sabs
```

It stated that the set difference was well-posed only if `HGNC` appeared among those endpoint vocabularies.

**Count before listing**

```cypher
MATCH (g:Concept)-[:gene_disease_validity]-()
MATCH (g)-[:HAS_CODE]->(:Code {SAB:'HGNC'})
WITH DISTINCT g
WITH g, EXISTS { (g)-[:has_variant_associated_with_disease]-() } AS has_otg
RETURN count(g) AS clingen_genes,
       sum(CASE WHEN has_otg THEN 1 ELSE 0 END) AS with_otg,
       sum(CASE WHEN NOT has_otg THEN 1 ELSE 0 END) AS without_otg
```

**Antijoin listing**

```cypher
MATCH (g:Concept)-[v:gene_disease_validity]-(d:Concept)
MATCH (g)-[:HAS_CODE]->(hg:Code {SAB:'HGNC'})
WHERE NOT EXISTS { (g)-[:has_variant_associated_with_disease]-() }
WITH g, hg, collect(DISTINCT v.evidence_class) AS clingen_classes,
     count(DISTINCT d) AS n_disease_assertions
OPTIONAL MATCH (hg)-[:ACR]->(t:Term)
RETURN hg.CodeID AS hgnc,
       coalesce(t.name, hg.CodeID) AS symbol,
       clingen_classes,
       n_disease_assertions
ORDER BY symbol
LIMIT 500
```

Claude explicitly returned `evidence_class` because a ClinGen assertion can be `Limited`, `Disputed`, or `Refuted`, and warned that absence from OTG reflects GWAS coverage rather than a biological negative. Execution later showed that OTG did not reach HGNC genes at all, so the requested gene-level antijoin was not meaningful.


---

---

# T7.7

## Design and 2 September assessment

a tiny source, and whether scale is checked first

> What cell type marker genes does Azimuth provide for kidney?

**Probes:** `AZ` at 2,912 edges — small enough that the whole source is
enumerable, and never queried.

**Pass:** recognises the source is small and returns it whole, or counts
first. Notes that Azimuth carries model-organism reference atlases, so species
needs checking.

**Fail:** applies a `LIMIT` to a source smaller than the limit without
noticing; or omits the species check.

**Result (2026-09-02): pass on scale, fail on species — and it corrected the
test premise.**

Every figure exact: `has_marker_gene_in_kidney` 485, liver 225, heart 200, all
under `HMAZ`.

**The test premise was wrong.** I wrote T7.7 against `AZ` at 2,912 edges. The
marker assertions are under **`HMAZ`** (1,820 edges, edge-only); `AZ` carries
the cell-type nodes (730 codes) and their `isa` hierarchy. Two sources, and
the answer separated them correctly where the test conflated them.

**Scale handled, though not as the criterion framed it.** It used `LIMIT 100`
rather than returning the source whole or counting first — but the limit is on
**cell types**, not markers, and it supplied the ceiling as a falsification:
*total genes summed over `n_markers` should be at most 485*. The bound is
stated and checkable, and 100 cell types comfortably exceeds any kidney
annotation set.

**Species not mentioned at all.** The criterion required noting that Azimuth
carries model-organism reference atlases. It does not.

### The cause is a missing routing topic, not a missing edge

| Topic | Resolves | Reaches species |
| --- | --- | --- |
| `tissue` | yes | yes |
| **`cell type`** | **no entry at all** | — |
| **`anatomy`** | **no entry at all** | — |
| **`marker`** | **no entry at all** | — |

`route.py "cell type"` returns *"No entry"* and offers no near match.

This is the fourth instance of the authoring pattern recorded in the R5b
review — species, the aggregate rule, the name-scan section, and now this —
but it fails differently. The first three were **edges missing from existing
topics**, giving incomplete guidance. This is a **missing topic**, giving
none: the model falls back to whichever file names look relevant.

Since `AZ` carries model-organism reference atlases, a cell-type question is
precisely where silent mouse contamination would occur — the hazard Tier 5.3
found for phenotype.

### Beyond the criterion

**Azimuth markers are chosen for discriminative power in label transfer, not
comprehensiveness.** In no reference file, and a user reading them as a kidney
expression profile would be wrong.

**`isa` edges within `AZ` roll fine cell types up to coarser ones**, which
makes the annotation-level hierarchy queryable.

---

---

## 8 September execution

49 cell types, **485 markers in total**, matching the registry count for
`has_marker_gene_in_kidney` exactly. The skill's falsification was that the sum
should be at most 485. It is 485.

Cell types resolve to Azimuth annotation labels
(`AZ_Kidney_L3_Ascending Thin Limb` and similar), each with ten markers.

**The directed edge worked.** The composed query writes
`-[r:has_marker_gene_in_kidney {SAB:'HMAZ'}]->` with an arrow, against the
skill's own guidance to match assertions undirected unless direction is
verified. It traverses correctly on this build, so the concern raised in review
was unfounded.
### Recovered original interaction

**User**

> What cell type marker genes does Azimuth provide for kidney?

**Claude**

Claude distinguished the `AZ` cell-type codes from the `HMAZ` marker assertions and generated:

```cypher
MATCH (ct:Concept)-[r:has_marker_gene_in_kidney {SAB:'HMAZ'}]->(g:Concept)
MATCH (ct)-[:HAS_CODE]->(az:Code {SAB:'AZ'})
MATCH (g)-[:HAS_CODE]->(hgnc:Code {SAB:'HGNC'})
OPTIONAL MATCH (az)-[:PT]->(ct_term:Term)
OPTIONAL MATCH (hgnc)-[:ACR]->(sym:Term)
RETURN coalesce(ct_term.name, az.CodeID) AS cell_type,
       collect(DISTINCT coalesce(sym.name, hgnc.CodeID)) AS marker_genes,
       count(DISTINCT g) AS n_markers
ORDER BY cell_type
LIMIT 100
```

Claude stated a falsification bound in advance: the sum of `n_markers` should be at most the 485 kidney-marker relationships recorded for the source. It also characterized the returned genes as Azimuth label-transfer markers rather than a comprehensive kidney expression profile. The formal execution returned 49 cell types and 485 marker assignments.


---

---

# T7.8

## Design and 2 September assessment

an undocumented source

> Which drugs are contraindicated in patients with long QT syndrome?

**Probes:** whether a source with no prose coverage is found from the
machine-readable registries.

**Originally designed as a decline case, on my assumption that no loaded
source asserts contraindication. That assumption was wrong** — MED-RT carries
`has_contraindicated_drug` (11,415 edges), `has_contraindicated_class`
(1,932), `has_contraindicated_mechanism_of_action` (457) and
`has_contraindicated_physiologic_effect` (274), and contributes 37
predicate/SAB rows in total. MED-RT appears in **no reference file**.

The test therefore measures something more useful than intended: whether the
skill reaches `assets/predicates.csv` for a source the prose does not cover.

**Pass:** finds the MED-RT predicates, binds them by name, and states that
MED-RT contraindications derive from FDA structured product labeling — what
manufacturers assert on labels, not clinical risk stratification — and that
this differs from resources not in the graph. Keeps class and
physiologic-effect rows rather than filtering to individual drugs, since
labels frequently contraindicate at class level without enumerating members.

**Fail:** declines on the assumption that contraindication is not represented;
or returns only `has_contraindicated_drug`, dropping the class-level
assertions that carry most of the clinical meaning.

**Result (2026-09-02): pass, with two observations.** All four predicate names
and edge counts verified against the registry. The interpretation named
CredibleMeds QT-risk tiers as the resource the graph lacks, and kept
class-level rows deliberately.

**Row grain correct.** 17 rows, 17 distinct CUIs, no duplication. Disease
anchors collected rather than fanned — seven codes across MSH, HP, NCI, OMIM,
SNOMEDCT_US, DOID and MONDO on every row. This is the Tier 6 failure avoided.
The drugs are right: disopyramide, dronedarone, nilotinib, and `C0037707` is
sotalol behind an IUPAC name.

**Observation 1 — only `has_contraindicated_drug` returned.** The query bound
four predicates; the class, mechanism-of-action and physiologic-effect
variants came back empty for this disease. The answer had argued specifically
that those matter, since labels often contraindicate at class level without
enumerating members — and for long QT, "drugs known to prolong the QT
interval" is exactly where that would live.

Not an anchoring miss: `disease_anchors` shows the term match landed on seven
codes. Either MED-RT asserts no class-level contraindication for this
condition, or those assertions hang off a different disease concept. **Open
question**, worth one query to settle.

**Observation 2 — display grain, distinct from row grain.** The `names` column
is unusable on several rows. `C0031935` returns
`[HMS1989H21, HMS1921H19, HMS1791H21]`, which are screening-library plate
identifiers; `C0037707` returns three IUPAC spellings of sotalol. The row is
correct and the label is not.

Cause: `collect(...)[0..3]` takes the first three synonyms arbitrarily, and
PubChem-derived lists lead with catalogue codes. This is the
source-supplied-names hazard already documented, appearing in a query whose
row grain is correct — so **display grain and row grain fail independently**,
and Tier 6 tested only the latter.

Fix — prefer a curated vocabulary for the display label:

```cypher
OPTIONAL MATCH (xc)-[]->(t:Term) WHERE xc.SAB IN ['RXNORM','ATC','MSH','DRUGBANK']
```
### Recovered original interaction

**User**

> Which drugs are contraindicated in patients with long QT syndrome?

**Claude**

Claude identified MED-RT as the relevant source and generated a single query spanning individual drugs, classes, mechanisms of action, and physiologic effects:

```cypher
// Drugs, drug classes, MoAs, and physiologic effects contraindicated
// with long QT syndrome, per MED-RT
MATCH (dcode:Code)-[dterm]->(dt:Term)
WHERE trim(toLower(dt.name)) = 'long qt syndrome'
  AND dcode.SAB IN ['MSH','SNOMEDCT_US','MONDO','DOID','OMIM','HP','NCI','MED-RT']
MATCH (dz:Concept)-[:HAS_CODE]->(dcode)
MATCH (dz)-[r]-(x:Concept)
WHERE r.SAB = 'MED-RT'
  AND type(r) IN ['has_contraindicated_drug','has_contraindicated_class',
                  'has_contraindicated_mechanism_of_action',
                  'has_contraindicated_physiologic_effect']
WITH x, type(r) AS relation, collect(DISTINCT dcode.CodeID) AS disease_anchors
OPTIONAL MATCH (x)-[:HAS_CODE]->(xc:Code)
OPTIONAL MATCH (xc)-[]->(t:Term)
WITH x, relation, disease_anchors,
     collect(DISTINCT xc.SAB) AS code_sabs,
     collect(DISTINCT coalesce(t.name, xc.CodeID))[0..3] AS names
RETURN relation, x.CUI AS cui, names, code_sabs, disease_anchors
ORDER BY relation, names[0]
LIMIT 300
```

It also supplied a fallback disease-resolution query if the term match returned no rows:

```cypher
MATCH (c:Code)-[tr]->(t:Term)
WHERE toLower(t.name) CONTAINS 'long qt'
MATCH (concept:Concept)-[:HAS_CODE]->(c)
RETURN c.SAB, c.CodeID, concept.CUI, type(tr) AS term_edge, t.name
LIMIT 25
```

Claude distinguished MED-RT label assertions from independent clinical QT-risk stratification and recommended retaining class-level results if present. The main query executed with 17 distinct contraindicated concepts; for the resolved disease anchor, only `has_contraindicated_drug` returned rows.


---

---

# T7.9

## Design and 2 September assessment

a partially answerable question

> What are the electrophysiological parameters for ion channels associated
> with epilepsy?

**Probes:** whether a compound question is split, when one half is answerable
and the other is not.

**Verified absent from the graph:** no conductance, gating, kinetics,
voltage-dependence or permeability predicates; no IUPHAR / Guide to
Pharmacology, Channelpedia, or any biophysical parameter source among the 289
node SABs. The nearest match is `has_pharmacokinetics` under MED-RT at 79
edges, which is drug ADME rather than channel biophysics.

**Answerable half:** ion channel genes associated with epilepsy, through the
gene-disease sources.

**Unanswerable half:** electrophysiological parameters, which no source
carries.

**Pass:** answers the first half, states plainly that the second is not in the
graph, and names where such data lives instead. Does not write a query for a
parameter predicate. Treats "ion channels" as a gene set requiring definition
rather than a single anchor.

**Fail:** invents a predicate or property for conductance or gating; returns
gene-level results implying they carry biophysical parameters; or declines the
whole question because half of it is unanswerable.

**Why this replaces the original decline case:** a wholly unanswerable
question can be declined without discrimination. A half-answerable one cannot
— it requires separating what the graph holds from what it does not, and
delivering the first while naming the second.

**Result (2026-09-02): pass, and the strongest answer in the tier.**

The decline leads, before any query, and names the absence in the field's own
vocabulary rather than the graph's: *"None of the sources assert V½ of
activation, inactivation time constants, single-channel conductance, or
anything else you would put into an HH or Markov model."* Then it points
outward — Channelpedia, ICEPO, ModelDB, primary patch-clamp literature — and
specifies the handoff: **keyed off the gene list the graph can give you.**

Both halves separated, the answerable one delivered.

### The near-miss is handled, which is the harder part

IDG bioactivity is offered as the closest quantitative functional data and
immediately distinguished: assay-level IC50/Kd/Ki is channel **pharmacology**,
not gating. That distinction carries the risk — a user asking for
electrophysiological parameters and receiving Kd values would reasonably
believe they had quantitative channel data.

### Three things beyond the criterion

**The intent fork is substantive, not procedural.** Epilepsy as a disease
entity versus genes causing any syndrome featuring seizures return different
sets, and the second floods with syndromic genes. Stage 1 resolves both
anchors so the choice is informed rather than asked cold.

**"Don't filter symbols on `SCN%`/`KCN%`; intersect with GO:0005216."** The
false-friend rule applied to a case nothing documents. A string filter would
miss `CACNA1A`, `HCN1` and `GABRA1` — all channels — while catching
non-channel `KCN`-prefixed genes. It then makes the HGNC-to-GO predicate a
discovery step rather than assuming it, having established earlier that NCI's
`process_involves_gene` carries biological process rather than molecular
function.

**The subtype caveat is specific.** OMIM and Orphanet annotate numbered DEE
and familial epilepsy entries rather than the umbrella, with the `isa`
traversal supplied before concluding absence.

Four interpretation caveats stack correctly at the close: DGN dominance,
HGNCHPO's syndromic flood, CLINGEN's `evidence_class` possibly being doubt
rather than support, and source independence before ranking.

---

## Session isolation

T7.1 and T7.6 both involve antijoins; run separately. T7.2, T7.3, T7.4, T7.5,
T7.7 and T7.9 touch different sources and can be distributed across two
sessions. T7.8 is complete.

## What a failure here means, that Tiers 0–6 could not show

A failure on a documented entity says the skill did not consult its own files.
A failure here says the guidance does not generalise beyond the cases it was
built from — which is the question that matters if anyone other than its
authors is going to use it.

T7.9 is now the one I would weight most. Every shipped example answers a
question the graph can answer, because the DCC authors chose questions their
data supported. Nothing in the corpus demonstrates declining, or splitting a
question and declining half.

T7.8's outcome is worth recording as a caution about test design as much as
about the skill: I asserted a source was absent without checking
`assets/predicates.csv` — the same failure the skill exists to prevent,
committed while writing a test for it. The registries cover the whole graph;
the prose covers the use cases. Any claim about what the graph lacks has to be
checked against the former.

---

## 8 September execution

### 9a: ran, truncated, and unconstrained

40 rows at `LIMIT 40`, so truncated. The SAB distribution shows the query
placed no constraint on vocabulary:

| SAB | Rows |
| --- | --- |
| HP | 31 |
| MSH | 4 |
| MP | 1 |
| CHV, PSY, LNC, ICPC2EENG | 1 each |

`MP:0002064` is a **mouse** phenotype, and `LNC` is LOINC laboratory codes.
A disease resolution step returned mouse phenotypes and lab codes alongside
human phenotype terms, which is the species and layer contamination the
skill's own guidance addresses.

### 9b: crashed the instance

`toLower(dt.name) = 'epilepsy'` wraps the property in a function, defeating the
`Term.name` TEXT index, so the anchor scans all Terms. Every matching disease
Concept then expands through a completely unbound `(disease)-[r]-(gene)`, with
no reduction between the halves, and `ORDER BY size(sources)` forces the whole
aggregation to materialise before `LIMIT 50` discards anything.

### 9c: not run

The composed form takes every HGNC-coded Concept and expands unbound before
filtering for GO on the far side, which is the shape that crashed the instance
in 9b. Not run rather than risk a second outage.
### Recovered original interaction

**User**

> What are the electrophysiological parameters for ion channels associated with epilepsy?

**Claude**

Claude immediately split the question into an answerable gene-association component and an unavailable electrophysiology component. It stated that conductance, gating, kinetics, voltage dependence, and permeability were not represented in the loaded sources, and that IDG bioactivity was pharmacology rather than electrophysiology.

**Stage 1: resolve epilepsy/seizure anchors**

```cypher
MATCH (t:Term)<-[tr]-(c:Code)<-[:HAS_CODE]-(con:Concept)
WHERE toLower(t.name) IN ['epilepsy', 'seizure', 'seizures']
RETURN con.CUI, c.SAB, c.CodeID, type(tr) AS term_edge, t.name
LIMIT 40
```

**Stage 2: genes with source audit**

```cypher
MATCH (dt:Term)<-[dtr]-(dc:Code)<-[:HAS_CODE]-(disease:Concept)
WHERE toLower(dt.name) = 'epilepsy'
MATCH (disease)-[r]-(gene:Concept)-[:HAS_CODE]->(gc:Code {SAB:'HGNC'})
WITH gc,
     collect(DISTINCT r.SAB)     AS sources,
     collect(DISTINCT type(r))   AS predicates,
     collect(DISTINCT dc.CodeID) AS matched_disease_codes
OPTIONAL MATCH (gc)-[:ACR]->(sym:Term)
RETURN coalesce(sym.name, gc.CodeID) AS gene,
       sources, predicates, matched_disease_codes
ORDER BY size(sources) DESC
LIMIT 50
```

**Conditional subtype traversal if the umbrella query were empty**

```cypher
MATCH (dt:Term)<-[dtr]-(dc:Code)<-[:HAS_CODE]-(disease:Concept)
WHERE toLower(dt.name) = 'epilepsy'
MATCH (disease)-[h:isa|inverse_isa]-(sub:Concept)-[:HAS_CODE]->(sc:Code)
RETURN DISTINCT sub.CUI, sc.SAB, sc.CodeID, h.SAB AS hierarchy_source
LIMIT 50
```

**Stage 3: discover the HGNC-to-GO predicate before defining ion-channel genes**

```cypher
MATCH (g:Concept)-[:HAS_CODE]->(:Code {SAB:'HGNC'})
MATCH (g)-[r]-(f:Concept)-[:HAS_CODE]->(fc:Code {SAB:'GO'})
RETURN type(r) AS predicate, r.SAB AS source, count(*) AS n
ORDER BY n DESC
LIMIT 20
```

Claude explicitly rejected symbol-prefix filtering such as `SCN%` or `KCN%` and proposed intersecting with the GO ion-channel activity subtree instead. In the 8 September execution, Stage 1 returned a truncated mixture of vocabularies, Stage 2 crashed the instance, and Stage 3 was not attempted because it shared the same expensive expansion pattern.


---

---

# Verdict

## By test

**Five of seven uncovered-source tests produced correct, executed results:**
T7.2 (DisGeNET), T7.3 (GTEXCOEXP), T7.5 (HCOP/MPMGI), T7.7 (Azimuth),
T7.8 (MED-RT).

**T7.6 delivered an invalid answer, having predicted it would.** OTG connects
genomic locations to diseases and never reaches genes, so a ClinGen-minus-OTG
difference cannot be computed. The skill stated this test in advance, supplied
the probe, and said what a zero would mean. It also composed the invalid query,
so the protection holds only if the stages are run in order.

**T7.1 failed.** Its resolution step amputated under a low-cardinality sort and
its second query never completed.

Of the two tests addressing query constructions rather than uncovered sources,
T7.4 succeeded after four rounds and exposed two false statements in the
skill's own reference material. T7.9 declined the unanswerable half correctly
and its queries for the answerable half do not run.

## What execution changed

Pre-execution grading rated T7.6 a clean pass and T7.7 a partial. Execution
reverses both: T7.6's answer is void and T7.7 is exact, returning all 485
markers and traversing a directed edge that review had flagged as risky.

The count of five correct is unchanged. Its membership is not.

## The pattern execution revealed

Three of the nine tests produce a query that does not run, and all three share
one construction: resolve an entity by a function-wrapped name match, then
expand unbound to a second entity type with no reduction between the halves.

- T7.1 stage 2: `CONTAINS 'ehlers'` with no SAB filter, then an unbounded
  `located_in` expansion. Never completed.
- T7.9b: `toLower(dt.name) = 'epilepsy'`, then `(disease)-[r]-(gene)` fully
  unbound, with `ORDER BY size(sources)` forcing full aggregation before the
  limit applies. Crashed the instance.
- T7.9c: every HGNC-coded Concept expanded unbound before filtering for GO.
  Not attempted.

Function-wrapping the property matters more than it appears: this instance
carries a TEXT index on `Term.name`, and `toLower(...)` or `trim(toLower(...))`
prevents the planner from using it. The skill's own resolution recipes are
written that way, so guidance added to handle trailing whitespace defeats the
index that would serve the same queries.

Every rule that would have prevented these three failures is in the skill. All
three occur in queries composed as a single statement. The five correct results
were composed in stages, with a probe or a count run before the query that
depends on it. That is consistent with the staged-versus-compressed contrast
recorded between T7.1 and T7.6 at design time, and it is now supported by
execution rather than by inspection.

## Corrections to earlier claims in this record

1. An earlier verdict stated the composed answers were "substantively correct
   on all" seven uncovered-source tests. T7.1 failed and T7.7 was graded
   partial, so that was wrong. It propagated into the S9 supplement and two
   preprint drafts before being caught.

2. T7.5, T7.6, T7.7 and T7.9 were originally graded on composed queries and
   registry verification alone, without execution, contrary to the protocol's
   own rule that every generated query is run. The 8 September session closed
   that gap.

3. Review of T7.7 raised a concern that its directed marker edge would fail.
   It traverses correctly, and the concern was unfounded.

4. The six-hour runtime in an earlier tier was attributed partly to absent
   property indexes. This instance is indexed, so that mechanism was wrong even
   though the conclusion held.

## Outstanding

- T7.9b and T7.9c have no working form. Staged replacements were drafted but
  not run.
- T7.6's question may be answerable at the variant layer through `HSCLO`
  rather than at the gene layer. Untested.
- T7.5's protein route, 67 UniProtKB proteins `part_of` the ciliary transition
  zone term, reaching genes through `gene_product_of`. Untested, and it
  contradicts the skill's statement that the set must come from outside the
  graph.
- `references/12_setup_and_access.md` describes this instance as having only
  LOOKUP indexes, which is false, and the cost guidance built on that
  description overstates cost here.

---

# Query ledger

Every query composed during Tier 7, with execution status and outcome. The
nine tests generated roughly twenty-eight queries; twenty ran. Tests that
appear as a single line in the summary above took up to eight rounds here.

Statuses: **ran** (executed, result recorded), **no result** (executed,
returned nothing or did not complete), **not run** (composed but never
executed).

## T7.1 — ClinVar EDS without a GTEx eQTL · 2 Sept

| # | Query | Status | Outcome |
| --- | --- | --- | --- |
| 1 | Resolve "ehlers" across 7 disease SABs, `ORDER BY c.SAB LIMIT 100` | ran | 100 rows, **amputated**: DOID 40, MONDO 60 only. OMIM, ORDO, HP, MEDGEN, SNOMEDCT_US never appeared. 39 distinct CodeIDs across 100 rows (term fanout) |
| 2 | Partition: `CONTAINS 'ehlers'` with **no SAB filter**, then `OPTIONAL MATCH located_in\|location_of` | no result | Did not complete. Unbounded Term scan feeding an unbounded 3.5M-edge expansion |

MEDGEN was among the SABs the truncation dropped, and the answer's own
reasoning had identified MedGen as where ClinVar's disease side arrives.

## T7.2 — DisGeNET on hypertrophic cardiomyopathy · 2 Sept

| # | Query | Status | Outcome |
| --- | --- | --- | --- |
| 1 | Resolve across 9 SABs, `OPTIONAL MATCH` DGN partners, `ORDER BY dgn_partners DESC LIMIT 50` | ran | 50 rows, all 9 SABs present, no amputation. 3 CUIs; `C0007194` carries 5,569 DGN partners |
| 2 | Partner Code SABs for `C0007194` | ran | 8 rows. **No HGNC.** DGNV 2,196, DGNGV 1,542, DGNBM 995, DGNCM 673, DGNAGE 152, DGNGDA 6, DGNTH 4, DGNMM 1 |
| 3 | Two-hop to genes via association nodes, collecting `assoc_classes` | not run | Would give the class mix per gene, the actual answer to the question |

Query 1 sorted on a computed count rather than the grouping column, which is
why it did not amputate where T7.1's did.

## T7.3 — genes co-expressed with PCSK9 · 2 Sept

Eight queries. The longest diagnostic sequence in the tier.

| # | Query | Status | Outcome |
| --- | --- | --- | --- |
| 1 | `coexpressed_with` from PCSK9 via `ACR` term match | no result | 0 rows |
| 2 | Partner count on the same pattern | not run | Offered as the truncation check |
| 3 | Schema discriminator, `CODE` vs `HAS_CODE` | ran | `HAS_CODE` |
| 4 | Resolution, `STARTS WITH 'PCSK9'` | ran | `HGNC:20001`, PCSK9 |
| 5 | Unfiltered anchor profile, `LIMIT 50` | ran | 50 rows; rows 33–50 pasted, tail all n ≤ 2 |
| 6 | `WHERE r.SAB = 'GTEXCOEXP'` partner count | no result | "No changes, no records" — confirms the true negative |
| 7 | STRING and MSIGDB partners | ran | 80 rows, dominated by `inverse_targets_expression_of_gene` reaching MSigDB set codes rather than genes |
| 8 | MSigDB signature/marker co-membership, aggregated before term expansion | ran | 40 rows, 40 distinct HGNC. F10 at 3 shared sets, all others 1–2. Partners are the hepatocyte secretory program |

The predicate name was verified against the registry after the fact:
`coexpressed_with` under `GTEXCOEXP`, 539,017 edges each direction, present
under no other SAB. Query 1 was well formed and the zero is real.

## T7.4 — genes above 100 TPM in pancreas · 2 Sept

Six queries across four rounds.

| # | Query | Status | Outcome |
| --- | --- | --- | --- |
| 1 | Constructed bin list `EXPBINS:100.200`… with `UBERON:0001264`, `expressed_in` | no result | 0 rows. Two failures at once: wrong bin format and wrong tissue predicate |
| 2 | Bin verification by `STARTS WITH` | not run | Superseded by 4 |
| 3 | Tissue resolution through GTEx measurements to UBERON | ran | Anchor is `UBERON:0001150`, not the obvious pancreas code |
| 4 | Chain diagnostic, **predicates unbound**, returning `type(r)` and sample bin CodeIDs | ran | Both causes visible in one paste: tissue side materialises `expresses`, and bins carry `.0` decimals (`EXPBINS:100.0.200.0`) |
| 5 | Four-token bin parse verification | ran | 28 bins with lower bound ≥ 100 |
| 6 | Final chain, predicates unbound with SAB pinned, numeric ordering | ran | **314 rows, 314 distinct HGNC**, under the 500 cap. PRSS2 at 90,000–100,000 TPM leading the acinar program |

Queries 1 and 2 were constructed from the skill's documented bin format, which
is wrong. Query 4 stopped constructing and asked the graph.

## T7.5 — mouse phenotypes for ciliary transition zone orthologs · 8 Sept

| # | Query | Status | Outcome |
| --- | --- | --- | --- |
| 5a | `GO:0035869` neighbourhood profile | ran | 8 rows. No HGNC. `has_part`/`part_of` UNIPROTKB 67, GO 7, `ro` GO 4, `isa` MP 3, GO 2 |
| 5b | 17 seed symbols → HCOP 1:1 → MPMGI → MP | ran | **16 of 17 genes.** Only TMEM216 was absent; later direct follow-up found 1 HCOP ortholog and 0 MPMGI phenotype assertions |

5a satisfied the skill's falsification criterion. The 67 UniProtKB `part_of`
edges are a protein-layer route the skill's conclusion did not allow for.

## T7.6 — ClinGen validity without OTG association · 8 Sept

| # | Query | Status | Outcome |
| --- | --- | --- | --- |
| 6a | OTG endpoint Code SABs, sampled at `LIMIT 500` before expansion | ran | 46 SABs, all disease vocabularies plus `HSCLO` and `GO`. **No HGNC** |
| 6b | Count with and without OTG | ran | 1,935 ClinGen genes, **0 with OTG, 1,935 without** |
| 6c | Antijoin listing | ran | **500 rows = the limit**, truncated. Content void. Classes: Definitive 304, Limited 64, Moderate 42, **Disputed 16**, Strong 8, mixed 26 |

6a is the gate the skill defined, and it fails. 6b confirms disjointness. 6c's
only usable output is the classification distribution.

## T7.7 — Azimuth kidney markers · 8 Sept

| # | Query | Status | Outcome |
| --- | --- | --- | --- |
| 1 | `has_marker_gene_in_kidney {SAB:'HMAZ'}`, **directed**, grouped by cell type | ran | **49 cell types, 485 markers exactly** — the registry count. Ten markers per type |

The directed edge traverses correctly, contrary to the concern raised at
review.

## T7.8 — drugs contraindicated in long QT · 2 Sept

| # | Query | Status | Outcome |
| --- | --- | --- | --- |
| 1 | Four MED-RT contraindication predicates from a term-matched disease anchor | ran | **17 rows, 17 distinct CUIs**, no duplication. Disopyramide, dronedarone, nilotinib, sotalol. Only `has_contraindicated_drug` returned; class, mechanism and physiologic-effect variants empty |
| 2 | Whether MED-RT asserts class-level contraindications for this disease | not run | Open question |

Display grain failed while row grain held: `C0031935` rendered as
`[HMS1989H21, HMS1921H19, HMS1791H21]`, screening-library plate identifiers.

## T7.9 — electrophysiological parameters for epilepsy channels · 8 Sept

| # | Query | Status | Outcome |
| --- | --- | --- | --- |
| 9a | Resolve epilepsy/seizure terms, `LIMIT 40` | ran | **40 rows = the limit**, truncated. No SAB constraint: HP 31, MSH 4, **MP 1 (mouse)**, CHV, PSY, **LNC (lab codes)**, ICPC2EENG 1 each |
| 9b | Genes with source audit, `toLower(dt.name) = 'epilepsy'` then unbound gene expansion | no result | **Crashed the instance** |
| 9c | HGNC-to-GO predicate discovery across all genes | not run | Same shape as 9b; not attempted |
| 9d | `isa`/`inverse_isa` descent to subtypes | not run | Conditional on 9b returning nothing |

## Ledger totals

| | Count |
| --- | --- |
| Queries composed | 28 |
| Executed with a recorded result | 20 |
| Executed, returned nothing or did not complete | 4 |
| Composed but never executed | 4 |
| Instance outages caused | 1 |

Four queries returned exactly their `LIMIT` and are therefore truncated:
T7.1 #1 (100), T7.6 #6c (500), T7.9 #9a (40), and T7.3 #5 (50). Two of those
truncations changed what the test could conclude.