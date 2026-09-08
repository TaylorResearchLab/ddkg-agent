#!/usr/bin/env python3
from pathlib import Path
import hashlib
import re

base = Path('ddkg-agent-skill/source/ddkg')

# 03: remove deployment-specific index assumptions and make cost advice index-aware.
p = base / 'references' / '03_schema_this_build.md'
s = p.read_text(encoding='utf-8')
start = s.index('## Indexes\n')
keep = s.index('### Anchor on the smallest enumerable set\n', start)
new = '''## Indexes

**Check the deployment before assuming anything about query cost.**

```cypher
SHOW INDEXES YIELD name, type, entityType, labelsOrTypes, properties
```

DDKG deployments may have different index configurations. A deployment may
include property indexes on fields such as `Code.CodeID`, `Code.SAB`, and
`Concept.CUI`, and may include a TEXT index on `Term.name`. Where appropriate
indexes are present, identifier and source anchors can be served by indexes
rather than full node scans.

Neo4j databases also normally include token `LOOKUP` indexes for node labels
and relationship types. These help resolve labels and relationship types but
do not index node properties.

**Do not wrap an indexed property in a function unless the resulting query
plan has been checked.** Expressions such as `toLower(t.name)` or
`trim(toLower(t.name))` prevent a plain index on `Term.name` from serving that
property predicate. The overall query can still be efficient if another
indexed anchor, such as `Code.SAB` or `Code.CodeID`, first reduces the
candidate set.

When case or whitespace normalization is required, reduce candidates with an
indexable identifier, source, or raw text predicate where possible, then apply
the normalization test to those candidates. If a deployment maintains an
appropriately normalized property or full-text index, use that facility
instead.

The anchoring and staging guidance below applies regardless of deployment.
The expected cost can differ substantially depending on the available indexes.

## Query cost

Anchoring and staging determine whether a query finishes. Check the active
deployment before assigning a cost to a property match. A query that is
logically correct but impractical to execute is not a usable answer.

### What costs what

| Construct | With an applicable property index | Without one |
| --- | --- | --- |
| `(c:Code {CodeID:'X:Y'})` | index-backed anchor | scan of `Code` nodes |
| `(c:Code {SAB:'HP'})` | index-backed but potentially broad | scan of `Code` nodes |
| `(c:Concept {CUI:...})` | index-backed anchor | scan of `Concept` nodes |
| `t.name CONTAINS '…'` | may use a TEXT index | scan of `Term` nodes |
| `toLower(t.name) = '…'` | plain `Term.name` index cannot serve this predicate | scan/filter of `Term` nodes |
| `-[]->(t:Term)` with unbound relationship type | expands every matching term edge | same |
| `-[r:predicate]-` | relationship-type LOOKUP can serve the type | same |

Use `EXPLAIN` or `PROFILE` when query cost matters rather than inferring the
plan from a different DDKG installation.

'''
s = s[:start] + new + s[keep:]
p.write_text(s, encoding='utf-8')

# 05: stage tolerant name matching behind a source/identifier reduction.
p = base / 'references' / '05_entity_resolution.md'
s = p.read_text(encoding='utf-8')
start = s.index('## Resolve inside the query where you can\n')
end = s.index('## Step 1 — resolve the name to an anchor\n', start)
new = '''## Resolve inside the query where you can

Resolution can stay inside the query when a source or identifier gives a
useful anchor. Prefer, in order: a verified `CodeID`; a known or candidate
`Code.SAB` set followed by term comparison; an indexable raw `Term.name`
predicate for candidate discovery when a TEXT index is present; and only then
a global function-wrapped name scan as an explicit fallback.

Do not start a large query by applying `toLower()` or `trim(toLower())` to every
`Term.name`. Those functions prevent a plain `Term.name` index from serving the
name predicate. If the source is known, reduce on the Code first and apply the
tolerant comparison only to its terms:

```cypher
MATCH (c:Code {SAB:'HP'})
WITH c
MATCH (c)-[]->(t:Term)
WHERE trim(toLower(t.name)) = toLower($name)
MATCH (anchor:Concept)-[:HAS_CODE]->(c)
```

On a deployment with a `Code.SAB` index, the Code anchor can reduce the
candidate set before the function-wrapped term comparison. If an appropriate
`Term.name` TEXT index is present and a case-preserving fragment is available,
`CONTAINS` or `STARTS WITH` can instead be used for candidate discovery; inspect
the returned term and Code before traversing onward.

A standalone resolution step earns its place when the name is genuinely
ambiguous, when the candidate source is unknown, or when the user needs to see
what the graph calls the entity. Do not hide an unconstrained all-Term scan
inside a much larger traversal.

'''
s = s[:start] + new + s[end:]
old = '''```cypher
MATCH (c:Code)-[tr]->(t:Term)
WHERE trim(toLower(t.name)) = toLower($name)
  AND c.SAB IN $candidate_sabs
MATCH (concept:Concept)-[:HAS_CODE]->(c)
RETURN c.SAB, c.CodeID, c.CODE, concept.CUI, type(tr) AS term_edge, t.name
LIMIT 25
```'''
new = '''```cypher
MATCH (c:Code)
WHERE c.SAB IN $candidate_sabs
WITH c
MATCH (c)-[tr]->(t:Term)
WHERE trim(toLower(t.name)) = toLower($name)
MATCH (concept:Concept)-[:HAS_CODE]->(c)
RETURN c.SAB, c.CodeID, c.CODE, concept.CUI, type(tr) AS term_edge, t.name
LIMIT 25
```'''
if s.count(old) != 1:
    raise SystemExit('05 Step 1 query block did not match exactly once')
s = s.replace(old, new)
old_para = '''If nothing returns, try `CONTAINS` before concluding absence. Substring
matches routinely hit descriptions rather than symbols, so return the matched
term and check it rather than traversing onward from it.'''
new_para = '''If nothing returns, use an indexable `t.name CONTAINS $fragment` or `STARTS WITH`
candidate scan when the deployment has a suitable TEXT index, then inspect the
matched terms and Codes before traversing onward. Substring matches routinely hit
descriptions rather than symbols, so candidate discovery is not entity resolution.'''
if old_para not in s:
    raise SystemExit('05 CONTAINS paragraph not found')
s = s.replace(old_para, new_para)
p.write_text(s, encoding='utf-8')

# 14: inline resolution remains allowed, but source reduction must precede tolerant text matching.
p = base / 'references' / '14_handing_over_queries.md'
s = p.read_text(encoding='utf-8')
start = s.index('**Anchor by term match when no verified identifier exists.**')
end = s.index('Ordering: a verified identifier', start)
new = '''**Anchor by term match when no verified identifier exists, but reduce the
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

'''
s = s[:start] + new + s[end:]
p.write_text(s, encoding='utf-8')

# README: R7 wording and reproducible-source/build documentation.
p = Path('ddkg-agent-skill/README.md')
s = p.read_text(encoding='utf-8')
s = s.replace('The current R6 package contains **38 bundled files**.',
              'The current R7 package contains **38 bundled files**.')
s = s.replace('a **versioned, release-calibrated query instrument**, not a static prompt.',
              'a **versioned, release-specific query instrument**, not a static prompt.')
marker = '## Install the skill\n'
source_note = '''## Reproducible source and release checks

The unpacked public source for the archive is kept under [`source/ddkg/`](source/ddkg/).
`build_skill.py` rebuilds `ddkg.skill` deterministically after running
`route.py --check`. `check_public_skill_hygiene.py` scans either the source tree
or a built archive for generic local/private artifacts and can also accept an
external deployment-specific denylist at release time. Keep that denylist
outside the repository.

A release should not encode assumptions about a private deployment. Query-cost
guidance therefore begins by inspecting `SHOW INDEXES`, and deployment-specific
hostnames, filesystem paths, credentials, and internal project links do not
belong in the public skill.

'''
if source_note not in s:
    s = s.replace(marker, source_note + marker)
p.write_text(s, encoding='utf-8')

# Release-time scan for three known historical local-compute tokens. Only hashes
# are stored here so the private values are not reintroduced into public text.
forbidden_hashes = {
    '5744323314533d2583cc8dd73ee7c98b45ce3c4c87c33c19d88bded2306d738d',
    'fe9bab5e32ff1d0383deef4c92942c09b5ee5eb071c57842a19597bd2ce4338a',
    '61ea2a8760cc16477992fa926a480dda9c86d84627bcfd480004a591cf753cb4',
}
for path in base.rglob('*'):
    if not path.is_file() or path.suffix.lower() not in {'.md','.txt','.tsv','.csv','.json','.py','.yaml','.yml'}:
        continue
    text = path.read_text(encoding='utf-8', errors='replace')
    for token in re.findall(r"[A-Za-z][A-Za-z0-9_.-]*", text.lower()):
        if hashlib.sha256(token.encode()).hexdigest() in forbidden_hashes:
            raise SystemExit(f'private-deployment token remains in {path}')

print('R7 source repairs applied')
