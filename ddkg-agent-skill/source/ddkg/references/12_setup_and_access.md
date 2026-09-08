# Obtaining, deploying, and querying a build

From `sources/ubkg_downloads.md`, `sources/ubkg_api.md`, and
`sources/ubkg_contexts.md`.

## Licensing

UBKG distributions are not published to public repositories, and use
requires authorization under the licensing terms. Access comes from the UBKG
steward, and the download site authenticates with a free UMLS licence key
from NLM.

So the path is: obtain a UMLS licence, request distribution access, then
download the dated archive from
[ubkg-downloads.xconsortia.org](https://ubkg-downloads.xconsortia.org/).
Releases are named by build date.

State this plainly rather than implying a one-command install. It is also why
the graph cannot ship with this skill even though the skill is freely
shareable.

Licensing and citation for **every SAB** are tabulated per context in
`sources/ubkg_contexts.md` — the reference for "what is this source and may I
redistribute it". Licensing questions go to the UBKG steward, Jonathan
Silverstein at the University of Pittsburgh.

### Reduced-licence builds

Most sources carry Creative Commons licences; the UMLS-derived clinical
vocabularies are the constrained ones. In this build `SNOMEDCT_US` plus
`DRUGBANK` together are 393,161 Codes (1.9%) and 3,020,296 relationships
(1.6%), so a build excluding them loses clinical terminology and almost none
of the DCC contributions. Whether such a distribution is currently published
is a question for the steward — do not assert that one exists.

## Deployment

Three shapes:

- **Turnkey Docker container** — lighter, right when Cypher over Bolt is the
  whole point.
- **UBKGBox** — Docker Compose with a neo4j back end and a front end
  including the ubkg-api. Right for users who want the REST endpoints.
- **Standalone Neo4j Community Server** — no Docker. Install Neo4j, load the
  database, run it as a service. Often easiest on an institutional host.

Ports are set by the run script and are not always the Neo4j defaults; one
documented parameter set uses browser port 4000 and Bolt 4500. A browser URL
is not a Bolt URI — someone working at `http://host:7474/browser/` connects a
driver at `bolt://host:7687`.

### Community Edition constraints

Most deployments run Community, which has no role-based access control:
there are no read-only users, so anyone with credentials can write. On a
shared instance the lever is server-wide —
`server.databases.default_to_read_only` in `neo4j.conf`, or
`ALTER DATABASE ... SET ACCESS READ ONLY`. Community also hosts one database
plus `system`, so two releases means two installations.

A global transaction timeout is worth setting on a shared host.

## The REST API

The ubkg-api is a Flask application exposing parameterised GET endpoints. It
sits between external applications and the Neo4j database underlying the
DDKG, and **the constrained surface is the design, not a shortcoming**: users
can run only predefined operations, which makes it a controlled access point
and removes the risk of arbitrary queries against the graph.

That property decides where each interface belongs. Bolt gives full Cypher and
therefore has to be trusted; the API enforces its own limits and therefore does
not. An instance that cannot expose Bolt may still be able to expose the API.

Documentation: <https://ubkg.docs.xconsortia.org/api/>.

**The base URL is per-deployment and must be looked up, not constructed.** The
UBKG documentation site is on `xconsortia.org`, but the Data Distillery API
examples in that documentation use
`https://datadistillery.api.sennetconsortium.org` — a different domain
entirely. Guessing a hostname from the docs domain produces one that does not
resolve.

Each deployment publishes its own SmartAPI entry; take the base URL from
there or from whoever runs the instance. Confirm before relying on it:

```bash
curl -s -o /dev/null -w "%{http_code}\n" <base-url>/sabs
```

`000` means the host did not resolve or nothing answered — a different problem
from `404` (wrong path) or `401` (key required).

The practical consequence for query writing is unchanged — it is not a Cypher
pass-through, so many questions have no endpoint. When one does not, say so
and offer the Cypher for someone with Bolt access. Never bend a question to
fit a near-matching endpoint; a near match answers a different question
confidently.

Some deployments require an API key; the Data Distillery API is one. Server
timeout is about 28 seconds and the payload cap about 10 MB, so path endpoints
need their filters (`sab`, `rel`, `mindepth`, `maxdepth`, `limit`, `skip`) set
deliberately.

### Connecting an agent

A Neo4j MCP server exists and can give a model direct read access to a Bolt
endpoint. **Do not suggest pointing one at an institutional instance.** A
graph behind an organisation's firewall should not be opened to an outbound
connection for convenience, and read-only enforcement in the client does not
address that — the objection is the connection, not what it is permitted to
do.

The API is the interface designed to be reached from outside. Where connected
access is wanted, wrapping the API is the appropriate route, because the
boundary is enforced by the server rather than trusted to the caller.

Assume users are working by hand: they run the query and paste the result
back. That is the expected mode for this skill, not a limitation being worked
around.

### Introspection endpoints

These answer schema questions without writing Cypher, and are worth reaching
for before enumerating anything by hand:

| Endpoint | Returns |
| --- | --- |
| `/sabs` | Every SAB associated with Code nodes |
| `/sabs/codes/counts` | Code counts by SAB |
| `/sabs/{sab}/codes/details` | Codes for one SAB, with terms |
| `/sabs/{sab}/term-types` | **Term types used by that SAB** |
| `/relationship-types` | Every relationship type |
| `/node-types`, `/node-types/{t}/counts_by_sab` | Node labels and counts |
| `/property-types` | The permitted property set |

`/sabs/HGNC/term-types` answers "how do I look up a gene symbol" directly.

### Entity endpoints

`/codes/{code_id}/codes`, `/codes/{code_id}/concepts`,
`/codes/{code_id}/terms`, `/concepts/{concept_id}/codes`,
`/concepts/{concept_id}/definition`, `/concepts/{concept_id}/nodeobjects`,
`/terms/{term_id}/codes`, `/terms/{term_id}/concepts`.

### Path endpoints

`/concepts/{id}/paths/expand`, `/paths/trees`,
`/concepts/paths/subgraph`, `/concepts/{id}/paths/subgraph/sequential`,
`/concepts/{origin}/paths/shortestpath/{terminus}`. These use APOC and are
the ones most likely to time out.

## Where the user runs it

Ask once per session, not per query.

- **Neo4j Browser, `cypher-shell`, or a driver** — arbitrary Cypher, so
  everything in the registries is available. The default.
- **The REST API** — no Cypher needed, but limited to existing endpoints.
  When no endpoint covers the question, say so and offer the Cypher instead.
  Never bend a question to fit a near-matching endpoint.
- **Nothing installed yet** — this file. A normal starting point.

### Browser row cap

The Neo4j Browser truncates result tables, in one observed case at exactly
5,000 rows, with no warning. A result of exactly 5,000 rows should be assumed
truncated. For large results use `cypher-shell` writing to a file, or raise
`:config maxRows`. Combined with `ORDER BY`, a row cap amputates cleanly —
an alphabetically sorted list cut at the limit is the head, not a sample.

## Versioning

Build releases are dated and carry release notes. Per-SAB versions are
assigned by the framework and recorded in an in-graph ontology with SAB
`UBKGSOURCE`, which also carries licensing and citation. The API exposes it
through the `sources` endpoint. **The graph documents its own provenance** —
query `UBKGSOURCE` rather than guessing a source's version.

## Browser behavior that changes results

In the current Browser (Query-based), pasting a file containing several
statements can return `no changes, no records` while evaluating none of them.
Run one statement per execution.

The current Browser draws only relationships returned by the query. The
legacy Browser can also draw stored inverse relationships between returned
nodes. In GRASS, the current Browser honors only color, size, and caption for
nodes and color, width, and caption for relationships; it chooses caption
text color from fill brightness.

## Comparing releases on an old-schema build

Two substitutions made December-release queries run on the July 2025
old-schema build:

- use `CODE` in place of `HAS_CODE`;
- use `[:ACR|MTH_ACR]` in place of `[:ACR]`.

The second substitution doubles symbol labels, returning forms such as `FUT5`
and `FUT5 gene`. The DCC predicates and SABs tested, including
`has_enzyme_protein {SAB:'GLYCANS'}` and `gene_product_of`, were unchanged.
The Q09 gene set was identical on the two builds at 44 genes.

These observations establish a limited comparison for the tested routes, not
general compatibility between releases.
