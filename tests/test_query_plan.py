from ddkg_agent.query_plan import EntityReference, QueryPlan


def test_minimal_ready_plan() -> None:
    plan = QueryPlan(
        status="ready",
        intent="gene_tissue_expression",
        entities=[
            EntityReference(role="gene", entity_type="gene", text="BRCA2")
        ],
        result_limit=50,
    )
    assert plan.schema_version == "0.1"
    assert plan.entities[0].text == "BRCA2"
