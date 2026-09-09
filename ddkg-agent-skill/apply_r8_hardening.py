#!/usr/bin/env python3
"""Apply the reviewed R8 hardening changes to the R7 ddkg.skill source tree.

This is an implementation helper for the R8 branch. It edits only curated
skill material and routing. Primary documentation under source/ddkg/sources is
left unchanged.
"""

from __future__ import annotations

from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE / "source" / "ddkg"


def replace_once(path: Path, old: str, new: str, marker: str | None = None) -> None:
    text = path.read_text(encoding="utf-8")
    if marker and marker in text:
        print(f"skip {path.name}: marker already present")
        return
    if old not in text:
        raise SystemExit(f"Expected text not found in {path}: {old[:120]!r}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8")
    print(f"updated {path.relative_to(HERE)}")


def append_once(path: Path, marker: str, addition: str) -> None:
    text = path.read_text(encoding="utf-8")
    if marker in text:
        print(f"skip {path.name}: marker already present")
        return
    if not text.endswith("\n"):
        text += "\n"
    path.write_text(text + addition, encoding="utf-8")
    print(f"updated {path.relative_to(HERE)}")


def main() -> int:
    skill = ROOT / "SKILL.md"
    replace_once(
        skill,
        """If nothing connects the two spaces directly, chain through an intermediate\nrather than inventing a predicate. A predicate can be one hop from the\nanchor and two from the answer — see the OMIM example in\n`05_entity_resolution.md`.\n""",
        """If nothing connects the two spaces directly, chain through an intermediate\nrather than inventing a predicate. A predicate can be one hop from the\nanchor and two from the answer — see the OMIM example in\n`05_entity_resolution.md`.\n\n**A diagnostic is a gate, not a caveat.** If a prerequisite check shows that\nthe required anchor, source, entity type, or bridge is absent, do not compose\nthe query that depends on it. State what failed and stop, or offer a different\nscientifically valid question.\n\nBefore any intersection, subtraction, antijoin, or other cross-source set\noperation, verify that both sides attach to the same biological entity and\nidentifier level. A source that reaches variants cannot be subtracted from a\ngene-level source as though both were gene sets.\n\nLikewise, a failed direct-link check establishes only that the direct link is\nabsent. Before saying that a requested set must come from outside DDKG, inspect\nthe anchor's neighbouring identifier spaces and the documented bridge\nrelationships for an indirect graph route.\n""",
        marker="A diagnostic is a gate, not a caveat.",
    )
    replace_once(
        skill,
        """- **Labels are decoration.** Reach `Term` with `OPTIONAL MATCH` and\n  `coalesce(t.name, c.CodeID)`. A required term edge kills a valid chain.\n""",
        """- **Labels are decoration, but display labels still need a verified edge.**\n  Keep the `Term` hop `OPTIONAL`. When the source's preferred-term edge is\n  known, bind that one edge and use `coalesce(t.name, c.CodeID)`. If no\n  preferred-term edge is verified, display the `CodeID` rather than choosing\n  an arbitrary synonym or `collect(...)[0]` from an unbound term fan.\n""",
        marker="display labels still need a verified edge",
    )

    rules = ROOT / "references" / "15_query_rules.md"
    replace_once(
        rules,
        """- **Census presence is not conjunction coverage.** A predicate can exist with\n  hundreds of edges while its intersection with another leg is empty —\n  `predicted_in {ERCCRBP}` has 268 edges against 462K for\n  `molecularly_interacts_with`. Run a staged funnel, one leg per statement,\n  before composing a multi-leg chain; the first zero is the dead constraint.\n""",
        """- **Census presence is not conjunction coverage.** A predicate can exist with\n  hundreds of edges while its intersection with another leg is empty —\n  `predicted_in {ERCCRBP}` has 268 edges against 462K for\n  `molecularly_interacts_with`. Run a staged funnel, one leg per statement,\n  before composing a multi-leg chain; the first zero is the dead constraint.\n- **Gate set operations on shared identity.** Before an intersection,\n  subtraction, antijoin, or negation, establish that both sources attach to\n  the same biological entity and identifier level. If one side reaches genes\n  and the other reaches variants, stop rather than subtracting the two result\n  sets and interpreting the empty or residual set biologically.\n""",
        marker="Gate set operations on shared identity",
    )
    replace_once(
        rules,
        """- **Threshold numbers on the Code node**, not the edge. Values live on bin Codes (`EXPBINS`, `PVALUEBINS`).\n""",
        """- **Threshold by selecting bin identifiers.** GTEx expression and eQTL\n  thresholds are represented by `EXPBINS` and `PVALUEBINS` Codes. Enumerate\n  the available bin `CodeID` values first and select the bins required by the\n  threshold. Do not assume usable numeric lower/upper properties, and do not\n  construct a bin identifier from memory.\n""",
        marker="Threshold by selecting bin identifiers",
    )

    handoff = ROOT / "references" / "14_handing_over_queries.md"
    replace_once(
        handoff,
        """## Staged queries: hand over one step, then rebuild the next\n\nSome chains genuinely need a decision in the middle. Choosing which pathway\n""",
        """## Staged queries: hand over one step, then rebuild the next\n\nA diagnostic stage is a **gate**. If its result shows that the next query is\nnot structurally valid — for example, the required source, endpoint type, or\nbridge is absent — do not write the dependent query anyway. Report the failed\nprerequisite and stop or propose a different scientifically valid route.\n\nSome chains genuinely need a decision in the middle. Choosing which pathway\n""",
        marker="A diagnostic stage is a **gate**",
    )

    ids = ROOT / "references" / "04_identifier_conventions.md"
    replace_once(
        ids,
        """No single rule converts a CURIE to a `CODE`.\n\n```cypher\n""",
        """No single rule converts a CURIE to a `CODE`.\n\n## Ingest syntax is not stored identity\n\nThe bundled UBKG ingest-format documentation describes **submission input**.\nForms such as `HGNC HGNC:9999`, `UBERON 0004086`, and underscore-delimited\nidentifiers are accepted by the generation framework and normalized during\ningestion. They are not a promise that the same literal string is stored in\n`Code.CodeID`, and copying a submission-format identifier into Cypher can\nreturn zero rows without an error. Query the stored `CodeID` form instead.\n\nA minted Concept identifier such as `UBERON:0002113 CUI` is also not a\n`CodeID`. The string with the ` CUI` suffix belongs in `Concept.CUI`; the Code\nremains `UBERON:0002113`. Keep ingest syntax, Concept identifiers, and Code\nidentifiers separate.\n\n```cypher\n""",
        marker="## Ingest syntax is not stored identity",
    )
    replace_once(
        ids,
        """Concepts sourced outside the UMLS carry a minted CUI of the form\n`SAB:CODE CUI` — so one Code can reach both a `C`-prefixed UMLS CUI and a\nminted one such as `HP:0001631 CUI`. Filtering on `CUI STARTS WITH 'C'` drops\nthe minted ones.\n""",
        """Concepts sourced outside the UMLS carry a minted CUI of the form\n`SAB:CODE CUI` — so one Code can reach both a `C`-prefixed UMLS CUI and a\nminted one such as `HP:0001631 CUI`. The ` CUI` suffix identifies a\n`Concept.CUI`; it is not part of the Code's `CodeID`. Filtering on\n`CUI STARTS WITH 'C'` drops the minted Concepts.\n""",
        marker="The ` CUI` suffix identifies a",
    )

    resolution = ROOT / "references" / "05_entity_resolution.md"
    replace_once(
        resolution,
        """A name match cannot tell a pathway from a mutation carrying the pathway's name\nin its label. Neither can a semantic-type filter on its own. The workable\nroute is to enumerate, look, and select CodeIDs, which is why pathway\nselection is a staged decision rather than something to automate.\n\n## Species\n""",
        """A name match cannot tell a pathway from a mutation carrying the pathway's name\nin its label. Neither can a semantic-type filter on its own. The workable\nroute is to enumerate, look, and select CodeIDs, which is why pathway\nselection is a staged decision rather than something to automate.\n\n## Synonym scans are candidate discovery only\n\nConcepts can carry unrelated or misleading synonym Terms. A reverse lookup\nthat accepts an entity solely because *any* synonym matched can therefore\nresolve to the wrong Concept while still returning fluent-looking results.\nTreat synonym and substring scans as candidate discovery only: confirm the\nsource Code and its preferred term before traversing onward.\n\n## Species\n""",
        marker="## Synonym scans are candidate discovery only",
    )

    setup = ROOT / "references" / "12_setup_and_access.md"
    replace_once(
        setup,
        """### Browser row cap\n\nThe Neo4j Browser truncates result tables, in one observed case at exactly\n5,000 rows, with no warning. A result of exactly 5,000 rows should be assumed\ntruncated. For large results use `cypher-shell` writing to a file, or raise\n`:config maxRows`. Combined with `ORDER BY`, a row cap amputates cleanly —\nan alphabetically sorted list cut at the limit is the head, not a sample.\n""",
        """### Browser row cap\n\nNeo4j Browser display limits are client- and configuration-dependent. Values\nof 1,000 and 5,000 rows were both observed during development, so neither is\na universal Browser limit. Count first. If a result ends exactly at the\nactive display limit, treat it as potentially truncated until the count or an\nexport confirms completeness. For large results use `cypher-shell` writing to\na file, or inspect/raise the active `:config maxRows` setting. Combined with\n`ORDER BY`, any display cap cuts off a clean prefix of the ordered list rather\nthan producing a representative sample.\n""",
        marker="Values\nof 1,000 and 5,000 rows were both observed",
    )

    multiplicity = ROOT / "references" / "18_row_multiplicity_and_identity_sinks.md"
    replace_once(
        multiplicity,
        """Keep the match `OPTIONAL` with `coalesce(term.name, code.CodeID)`: rule 4\n(labels are decoration) still holds. Binding a type is not the same as\nrequiring one.\n""",
        """Keep the label match `OPTIONAL`: labels are decoration, not constraints.\nFor display, bind one verified preferred-term edge for the source being\nreported, then use `coalesce(term.name, code.CodeID)`. If no preferred-term\nedge is verified, display the `CodeID`. Do not choose an arbitrary synonym or\nuse `collect(...)[0]` over an unbound term fan as the entity's name. Binding a\npreferred edge is not the same as requiring a label to exist.\n""",
        marker="Do not choose an arbitrary synonym",
    )

    interpreting = ROOT / "references" / "11_interpreting_results.md"
    append_once(
        interpreting,
        "## MED-RT contraindication endpoints are not disease-only",
        """\n## MED-RT contraindication endpoints are not disease-only\n\n**Confirmed on the target release.** The MED-RT relationship named\n`contraindicated_with_disease` has a looser endpoint range than its name\nsuggests. Returned objects can include disease Concepts, but also age,\nlife-stage, or pregnancy-related context. A query that keeps only objects\ncarrying a disease vocabulary can therefore silently discard valid MED-RT\ncontraindication assertions.\n\nWhat to do: return the endpoint Codes and inspect what each represents before\napplying an object-side vocabulary filter. Treat the predicate name as the\nsource's relationship label, not as a guarantee that every object is a\ndisease.\n""",
    )

    graph = ROOT / "assets" / "skill_graph.tsv"
    append_once(
        graph,
        "# ---------------------------------------------------------- R8 hardening",
        """\n# ---------------------------------------------------------- R8 hardening\ncomparison\tmust_read_with\t15_query_rules.md#anchoring-and-cost\tset operations require both sources at the same biological identifier level\nset difference\tmust_read_with\t15_query_rules.md#anchoring-and-cost\tverify shared entity identity before subtraction\nantijoin\tmust_read_with\t15_query_rules.md#anchoring-and-cost\ta failed comparability diagnostic stops the query\nnegation\tmust_read_with\t15_query_rules.md#anchoring-and-cost\tabsence is meaningful only after both sides are comparable\nintersection\tmust_read_with\t15_query_rules.md#anchoring-and-cost\tverify shared entity identity before intersecting\nontology term\tmust_read_with\t05_entity_resolution.md#a-predicate-can-be-one-hop-from-the-anchor-and-two-from-the-answer\tno direct gene edge does not establish that no graph route exists\ngene set\tmust_read_with\t05_entity_resolution.md#a-predicate-can-be-one-hop-from-the-anchor-and-two-from-the-answer\tinspect neighbouring identifier spaces before requiring an external set\nlabel\tmust_read_with\t18_row_multiplicity_and_identity_sinks.md#6-label-fans-bind-one-preferred-term-per-source\tbind one verified preferred term edge or display CodeID\ndisplay name\tmust_read_with\t18_row_multiplicity_and_identity_sinks.md#6-label-fans-bind-one-preferred-term-per-source\tdo not select an arbitrary synonym from an unbound term fan\nsynonym\tmust_read_with\t05_entity_resolution.md#synonym-scans-are-candidate-discovery-only\tconfirm Code and preferred term before traversal\nname scan\tmust_read_with\t05_entity_resolution.md#synonym-scans-are-candidate-discovery-only\tmatching any synonym is candidate discovery, not resolution\ningest format\tanswers\t04_identifier_conventions.md#ingest-syntax-is-not-stored-identity\tsubmission syntax is normalized and is not a stored CodeID promise\nsubmission format\tanswers\t04_identifier_conventions.md#ingest-syntax-is-not-stored-identity\tdo not paste ingest literals directly into Cypher\nstored identifier\tmust_read_with\t04_identifier_conventions.md#ingest-syntax-is-not-stored-identity\tseparate input syntax, Concept.CUI, and CodeID\ncompound\tmust_read_with\t04_identifier_conventions.md#one-code-several-concepts\tprofile the full Concept fan from a Code before selecting one CUI\ndrug\tmust_read_with\t04_identifier_conventions.md#one-code-several-concepts\tlegitimate multi-CUI splits extend beyond minted twins\nentity\tmust_read_with\t04_identifier_conventions.md#one-code-several-concepts\ta Code can attach to several legitimate Concepts\ncontraindication\tmust_read_with\t11_interpreting_results.md#med-rt-contraindication-endpoints-are-not-disease-only\tinspect endpoint type before filtering to disease vocabularies\nMED-RT\tmust_read_with\t11_interpreting_results.md#med-rt-contraindication-endpoints-are-not-disease-only\tpredicate name does not guarantee disease-only objects\n""",
    )

    print("R8 hardening edits applied.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
