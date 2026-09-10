# R9 live schema-transition extraction

## Purpose

The R9 route planner needs a release-specific table of source-qualified schema transitions:

```text
subject_sab,predicate,edge_sab,object_sab
```

This table describes the small SAB/predicate graph used for route planning. It does not enumerate DDKG nodes and does not store database access information.

## Pilot extraction

Before scanning every source-qualified relationship in the release, benchmark the extraction on four sources that exercise the R8 model-organism route and ordinary ontology structure:

```cypher
MATCH (a:Concept)-[r]->(b:Concept)
WHERE r.SAB IN ['GO', 'UNIPROTKB', 'HCOP', 'MPMGI']
MATCH (a)-[:HAS_CODE]->(ac:Code)
MATCH (b)-[:HAS_CODE]->(bc:Code)
WHERE ac.SAB IS NOT NULL AND bc.SAB IS NOT NULL
RETURN DISTINCT
  ac.SAB AS subject_sab,
  type(r) AS predicate,
  r.SAB AS edge_sab,
  bc.SAB AS object_sab
ORDER BY edge_sab, predicate, subject_sab, object_sab;
```

Export the result as CSV. The pilot deliberately retains every endpoint Code SAB present on the two Concepts. This lets us measure how much Concept normalization expands the raw SAB-to-SAB map before deciding which rows are safe routing transitions.

The expected columns are exactly the four columns accepted by `source/ddkg/scripts/build_schema_transitions.py`.

## Why the pilot comes first

A Concept can carry Codes from several vocabularies. A raw relationship therefore can appear to connect several SAB pairs even when only one identifier pair is scientifically useful for a given query. R9 must distinguish:

1. a **structural endpoint compatibility map**, which records all endpoint SABs observed around a relationship; from
2. an **admissible routing map**, which records transitions that are safe to use for query construction under the requested entity role and species.

The pilot is used to quantify that difference before a full-release extraction is attempted.

## Full extraction

Do not run a full-release scan until the pilot output and runtime have been reviewed. If the pilot is tractable, the full extraction will use the same four-column form, preferably in source-SAB batches so each batch can be validated and rerun independently.
