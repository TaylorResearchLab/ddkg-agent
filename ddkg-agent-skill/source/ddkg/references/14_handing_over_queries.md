# Handing over a query

Nothing is executed here. What is handed over has to run as pasted, and the
user has to be able to tell whether it went wrong.

## Runnable as pasted

One fenced `cypher` block, no placeholders, no `PASTE_YOUR_CODE_HERE`, no
`WITH 'FILL_THIS_IN' AS x`. Inline the values rather than using `$params` —
Neo4j Browser needs a separate `:param` step and users forget it.

A query the user must edit shifts the work back, and usually the hardest part:
they run a resolution query, read the result, decide which row is right, and
paste it into the correct line. Four chances to go wrong, and avoiding those
calls is why they asked.

**Anchor by term match when no verified identifier exists, but reduce the
candidate set first.** A tolerant name comparison is legitimate, but it should
not force a scan of every Term when a source or identifier can narrow the
search:

```cypher
MATCH (c:Code {SAB:'HP'})
WITH c
MATCH (c)-[]->(t:Term)
WHERE trim(toLower(t.name)) = 'atrial septal defect'
MATCH (pheno:Concept)-[:HAS_CODE]->(c)
```

Leave the term edge unbound; bindings are source-specific. The `trim()` guards
against trailing whitespace in Term names, but the function means a plain
`Term.name` index cannot serve that predicate. The preceding Code anchor is
therefore important: where `Code.SAB` is indexed it reduces candidates first.
If an indexable `Term.name CONTAINS` or `STARTS WITH` candidate scan is more
appropriate, use it to discover candidate Codes and verify the selected Code
before the main traversal. On a deployment without applicable property indexes,
say that the resolution may be expensive and stage it separately when needed.

Ordering: a verified identifier from `04_identifier_conventions.md` if one
covers the entity; otherwise resolve inline by term match; a separate
resolution step only when the choice is genuinely the user's.

## Bracket at drafting

During drafting, bracket any number or name emitted without a run behind it,
so a placeholder cannot be mistaken for a measurement. Brackets are a
drafting control only: before hand-over, replace them with run-backed values
or remove the claim. The user-facing query still must be runnable as pasted
and placeholder-free.

## Multi-statement files

A file containing more than one statement starts with:

```text
RUN ONE BLOCK AT A TIME
```

This prevents the Query-based Browser from accepting a multi-statement paste
while evaluating none of the statements.

## Query headers

Each query header carries one functional comment describing what the query
does. Validation history and amendment history belong in the rename map and
the Collaboration Log, not in the query header.

## Do not predict what the query will return

Any statement about what the graph contains — a row count, a gene list,
"none", "N predicates across M sources" — is an assertion this skill is not in
a position to make.

Adding a query underneath does not fix it. "Short answer: none. Here are
queries to confirm" has already delivered the answer; the confirmation is
decorative and users skip it.

**This covers the shape of a result, not only its values.** "Expect the
Reactome rows to split into a curated cascade versus individual events" names
no entity and asserts no count, so it reads as framing. It is a claim, and it
primes the user to see what they were told to expect — a reader told to expect
diversity across four sources is less likely to notice that two of them
redistribute a third.

Say what to **look for** instead:

> Worth checking how many MSigDB rows carry `REACTOME_` or `WP_` prefixes, and
> whether any name-match the Reactome or WP rows — MSigDB's C2:CP collection
> redistributes both, so what looks like four independent sources may be two.

Worked examples in `references/` are historical results from one enumeration.
They show shape, never values, and a question about an entity does not become
answerable because that entity happens to be the example.

## Give a falsification criterion

How the user will know it went wrong:

- Which column identifies a correct match, where a verified anchor exists —
  "a correct match returns `HGNC:10848`; `HGNC:10671` means it fell through to
  `PT` and found SDCCAG8."
- What an empty result would mean here, and which check separates the causes.
- Whether truncation is a risk at this `LIMIT`.

**Identifiers are claims too.** Quote a `CodeID` from the verified-anchors
table or from a resolution the user has run, never from recall.

## Staged queries: hand over one step, then rebuild the next

A diagnostic stage is a **gate**. If its result shows that the next query is
not structurally valid — for example, the required source, endpoint type, or
bridge is absent — do not write the dependent query anyway. Report the failed
prerequisite and stop or propose a different scientifically valid route.

Some chains genuinely need a decision in the middle. Choosing which pathway
sets to keep is a scientific judgement — curated cascades and broad supersets
carry similar names and give very different answers — and it should not be
made silently.

**That is not a licence to emit a placeholder.** A templated second step with
`'<CodeID 1>'` in it is the same work-shifting in a more considerate tone: the
user still has to read a result, decide, and paste a value into the right line
of a query they did not write.

Do this instead:

1. Hand over **step one only**, runnable as pasted, returning the columns the
   decision needs — and say which column the decision turns on.
2. Ask them to paste the result back.
3. Write step two with their chosen values **inlined**, runnable as pasted.
4. Repeat for further steps.

> Run this, then paste back the rows you want to keep — the `semantic_type`
> column separates real pathway concepts from gene records sharing the name,
> and for Reactome keep only the `R-HSA-` entries. I will write the next query
> against whatever you choose.

This costs one round trip and removes every chance to paste into the wrong
place. It also lets the next query be built against what the graph actually
returned rather than against an assumption about it — which is the whole
reason this skill hands over queries instead of predicting results.

Where a value list must be edited by the user, put it on **one line at the
top** as data, never buried mid-query:

```cypher
UNWIND ['MSIGDB:M27565','MSIGDB:M27557'] AS keep
MATCH (pw:Concept)-[:HAS_CODE]->(pwc:Code {CodeID: keep})
```

Offer the staged route explicitly. Users do not know it is on the table, and
left to guess they will edit the template and get it subtly wrong.

**Do not predict what the query will return, and do not answer the question
yourself.** No query is executed here. Any statement about what the graph
contains — a row count, a gene list, "none", "N predicates across M
sources", "this should give you about 40 results" — is an assertion this skill
is not in a position to make.

This is not satisfied by adding a query underneath. "Short answer: none. Here
are queries to confirm" has already delivered the answer; the confirmation
step is decorative and users will skip it. The answer must come from the
user's run, not from the assistant with a citation attached.

The failure is most likely on entities that appear as worked examples in
`references/`. SHH's anchor profile and the atrial-septal-defect gene lists
are recorded there as *historical* results from one enumeration of one build.
They exist to show what a profile looks like and how to read one. They are not
cached answers, and a question about SHH does not become answerable because
SHH happens to be the example.

The correct shape is: **the query, what it will tell them, and how to read
what comes back.**

> LINCS is the only compound-to-gene regulation source in this build. This
> profile will show whether SHH has LINCS edges at all:
>
> ```cypher
> ...
> ```
>
> If `LINCS` is absent from the result, that is a coverage finding rather than
> a biological one — the data dictionary records that LINCS links each
> perturbagen only to its top 25 up- and down-regulated genes, so most genes
> have no edges. If it is present, the second query below returns the
> compounds.

That names the source, sets up the interpretation in advance, and leaves the
factual claim to the graph.

Give a **falsification criterion** — how the user will know the query went
wrong:

- Which column identifies a correct match, where a verified anchor exists:
  "a correct match returns `HGNC:10848`; `HGNC:10671` means it fell through to
  `PT` and found SDCCAG8."
- What an empty result would mean here, and which check separates the causes.
- Whether truncation is a risk at this `LIMIT`.

The distinction is between *how to check the answer* and *what the answer is*.
Give the first, never the second.

This covers statements about how the graph will *behave*, not just what it
holds. "These two anchors will profile differently", "sources attach to one or
the other, rarely both", "expect this predicate to appear with a large count" —
each is an unverified claim about the data wearing the form of guidance.

**It also covers the shape of a result, not only its values.** "Expect the
Reactome rows to split into a curated cascade versus individual events", "the
MSigDB rows will span hallmark and curated sets of very different sizes" — no
row count is asserted and no entity named, so it reads as framing rather than
as a claim. It is a claim: the result has not been seen and cannot be
characterised.

Shape predictions do a specific harm: they prime the user to read the result
as matching the description. A reader told to expect diversity across four
sources is less likely to notice that two of them redistribute a third. Hand
over the query, and say what to *look for* rather than what will be there:

> Worth checking how many of the MSigDB rows carry `REACTOME_` or `WP_` name
> prefixes, and whether any name-match the Reactome or WP rows — MSigDB's
> C2:CP collection redistributes both, so what looks like four independent
> sources may be two.

That is actionable, falsifiable, and makes no claim about what the graph
returned.

**Identifiers are claims too.** Quote a `CodeID` from
`04_identifier_conventions.md`'s verified-anchors table, or from a resolution
query the user has run. Never from recall. An unverified accession offered
without flagging is the SDCCAG8 failure with the query step removed.
