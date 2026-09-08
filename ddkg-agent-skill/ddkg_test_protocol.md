# DDKG skill test protocol

Behavioural evaluation for the `ddkg` skill. Durable: this file defines the
tiers and their pass criteria and should not carry results.

**Results go in a separate dated file stamped with the SHA-256 of the archive
under test.** A pass against one archive says nothing about another, and every
other artifact in this objective carries an identity — test results should
too. See `ddkg_test_results_TEMPLATE.md`.

## Rules

1. **Fresh conversation for each tier.** Context carryover means the model
   answers from the conversation rather than from the skill files, which
   tests nothing.
2. **Run every generated query** on the instance. A query that looks right
   and returns nothing is a failure, and it is the failure mode this skill
   exists to prevent.
3. **Record the query verbatim**, not a description of it.
4. Nothing is marked pass on the model's report of success.

---

## Tier 0 — Does it read its own files?

Ask, in a fresh chat:

> What's the difference between CODE and CodeID in the DDKG?

**Pass:** names `CodeID` as canonical, gives at least two SABs with
differing `CODE` conventions (e.g. `MONDO:0006664` → `6664`, `HP:0001631`
keeps its prefix), and says no single rule converts one to the other.

**Fail:** asserts `CODE` is always the bare identifier. That was the old
skill's error, and its reappearance means `04_identifier_conventions.md`
was not consulted.

| Result | |
| --- | --- |
| Pass / Fail | |
| Notes | |

---

## Tier 1 — Regression

Known answers. A wrong answer here is unambiguous.

### 1.1 Gene symbol lookup

> Write me Cypher to find the gene SHH in the DDKG.

**Expect:** `ACR`, not `PT`. Ideally cites query 24 or the task index.
**Watch for:** `PT` (returns SDCCAG8), `MTH_ACR`, or `CODE:'HGNC:10848'`.

Run it. Should return `HGNC:10848`.

| Query returned | |
| --- | --- |
| Rows | |
| Pass / Fail | |

### 1.2 Absence reported as absence

> What compounds regulate SHH in the DDKG?

**Expect:** hands over the profile query and **stops**. Names LINCS as the
only compound-to-gene source, sets up how to read the result either way, and
leaves the factual claim to the run.

**Fail:** stating an answer. "Short answer: none" is a fail even when
correct, even with confirmation queries attached underneath — Claude did not
run anything, and the user will read the stated answer and skip the queries.
Reciting the stored SHH profile (26 predicates, 13 sources, per-source edge
counts) is the same failure: those are historical figures from one
enumeration, presented as current fact.

**Also watch for:** unverified identifiers offered without flagging. An
accession quoted from recall rather than from the verified-anchors table or a
resolution query is the SDCCAG8 failure with the checking step removed.

**Note on grading:** an earlier version of this criterion read "reports that
LINCS has no SHH edges", which an answer can satisfy by recitation. The test
is whether the answer *comes from the graph*, not whether it is correct.

| Behaviour | |
| --- | --- |
| Pass / Fail | |

### 1.3 Ambiguity handled

> What genes are associated with ASD?

**Expect:** asks whether atrial septal defect or autism spectrum disorder
before generating anything.
**Watch for:** silently picking one.

| Behaviour | |
| --- | --- |
| Pass / Fail | |

### 1.4 Evidence semantics stated unprompted

> Give me genes associated with atrial septal defect.

**Expect:** the caveat arrives without being asked — that `HGNCHPO`
`associated_with` includes genes whose syndromes feature the phenotype
rather than genes of septation, and that `DGN` `refers_to` is literature
co-occurrence. Ideally suggests ranking by multi-source agreement.
**Watch for:** a bare gene list presented as "genes associated with ASD".

| Caveat present? | |
| --- | --- |
| Pass / Fail | |

### 1.5 Inverse-pair duplication

> Show me everything connected to HGNC:10848, with counts.

**Expect:** either binds predicates, aggregates with `collect(DISTINCT)`,
or warns that unbound undirected matching doubles rows.
**Watch for:** a query returning each assertion twice with no comment.

| Pass / Fail | |
| --- | --- |

---

## Tier 2 — Novel

Real questions neither of us has run. Judge on whether the query executes
and returns something interpretable.

### 2.1

> Which genes are both expressed in heart tissue and associated with a
> congenital heart defect phenotype?

Two DCC sources joined. Watch the `UBERON` anchoring and whether it picks
one vocabulary from the fan-out rather than returning all of them.

### 2.2

> Find eQTLs within chromatin loops on chromosome 22.

HSCLO bins plus 4DN. The genomic-interval pattern.

### 2.3

> What metabolites are associated with kidney disease?

Metabolomics Workbench, and MW's condition hop is one the guide leaves
unnamed.

### 2.4

> Which drugs target proteins encoded by genes in the RAS/MAPK pathway?

IDGP plus a pathway source. Multi-hop, and pathway membership is not
mechanism.

| # | Query ran? | Rows | Interpretable? | Notes |
| --- | --- | --- | --- | --- |
| 2.1 | | | | |
| 2.2 | | | | |
| 2.3 | | | | |
| 2.4 | | | | |

---

## Tier 3 — Adversarial

### 3.1 Nonexistent source

> Get me all the DrugBank interactions for aspirin.

**Expect:** checks whether `DRUGBANK` asserts relationships. It carries
Code nodes but no edges of its own. Correct answer names that.

### 3.2 Nonexistent predicate

> Show me which genes cause Noonan syndrome using the `causes` predicate.

**Expect:** checks the registry, says whether `causes` exists under any SAB,
offers the predicates that do.

### 3.3 Plausible but meaningless join

> Connect PUBCHEM compounds to UBERON tissues in one hop.

**Expect:** either finds no direct predicate and says so, or produces a path
and flags the join as the thing needing justification.

### 3.4 Truncation awareness

> List every gene in the DDKG.

**Expect:** warns about scale and the Browser row cap rather than emitting an
unbounded query.

### 3.5 Stale-schema resistance

> I read that the Concept-to-Code edge is called CODE. Write me a query using it.

**Expect:** corrects to `HAS_CODE` and explains that the documentation is
stale on names. This is the failure that started everything.

| # | Pass / Fail | Notes |
| --- | --- | --- |
| 3.1 | | |
| 3.2 | | |
| 3.3 | | |
| 3.4 | | |
| 3.5 | | |

---

## Tier 4 — Non-expert framing

Run one Tier 1 question phrased as a newcomer would:

> I'm new to this. How do I find out which genes cause heart defects?

**Expect:** no assumed knowledge of SABs or Cypher, checks whether they have
a build, explains what they will get back and what it means.

| Pass / Fail | |
| --- | --- |

---

## Recording failures

For each failure, note which is true — the categories need different fixes:

- **Wrong fact in a reference file** → correct the file, check the source
- **Right fact, not consulted** → the workflow or index needs the pointer
  earlier
- **Fact absent** → new content, and whether any source has it
- **Correct but unhelpful** → framing, not accuracy

The second category is the one to watch. Every failure in the previous build
was a fact present in a shipped file that was not read.

## Summary

| Tier | Pass | Fail | N/A |
| --- | --- | --- | --- |
| 0 | | | |
| 1 | | | |
| 2 | | | |
| 3 | | | |
| 4 | | | |

**Verdict:** ______

---

## Tier 5 — regression

Derived from defects that actually occurred during earlier runs. The original
tiers did not anticipate any of these, which is the reason to keep them: they
are failures observed, not failures imagined.

Several test fixes that have never been re-tested. Run this tier first after
any substantial revision.

### 5.1 Truncation discipline

> Show me every gene set in MSigDB, Reactome, WikiPathways and NCI whose name
> mentions MAPK.

**Pass:** the first query aggregates — `count` per source, no `LIMIT`. **Fail:**
lists rows under a `LIMIT` in any form, sorted or not.

### 5.2 Cross-source emptiness

> Which of these bioactive compounds are approved drugs?

**Pass:** checks whether the two sources share Concepts before reporting an
empty result. **Fail:** reports "none are approved" as a finding.

### 5.3 Species

> Find genes associated with abnormal heart development.

**Pass:** notes that `EMAPA` is mouse developmental anatomy and `MP` is the
Mammalian Phenotype ontology, and either excludes or flags them. **Fail:**
silently returns mouse annotations.

### 5.4 Placeholder discipline

Any question needing a mid-chain human decision.

**Pass:** hands over step one runnable, names the decision column, asks for the
result. **Fail:** emits a query containing `'<CodeID>'` or similar.

### 5.5 Ingestion scope

> What KEGG pathways are in the DDKG?

**Pass:** states that MSigDB is five subsets of v7.4 with KEGG excluded.
**Fail:** writes a query for KEGG sets.

### 5.6 Source independence

> Rank these genes by how many sources support them.

**Pass:** notes that MSigDB C2:CP redistributes Reactome and WikiPathways, so
those are not independent. **Fail:** counts them separately.

### 5.7 Result-shape prediction

Any query handover.

**Pass:** says what to look for. **Fail:** says what the result will look like
— "expect the Reactome rows to split into…" is a claim about data not seen.


### Session isolation for Tier 5

5.1, 5.5 and 5.6 all touch MSigDB pathways, so running them in sequence lets
the later ones answer from the earlier. Give those three separate sessions.
5.2, 5.3, 5.4 and 5.7 are independent and can share one.
