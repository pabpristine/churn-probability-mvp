from src.domain.entities.workflow_context import WorkflowContext

from src.nodes.historical_knowledge_service import (
    HistoricalKnowledgeService
)


def main():

    print(
        "\n========== HISTORICAL KNOWLEDGE TEST ==========\n"
    )

    context = WorkflowContext()

    # ------------------------------------------
    # Test Data
    # ------------------------------------------

    context.client_id = 1

    service = HistoricalKnowledgeService()

    context = service.execute(
        context
    )

    # ------------------------------------------
    # Summary Embeddings
    # ------------------------------------------

    print(
        f"Summary Embeddings Retrieved : "
        f"{len(context.historical_summary_embeddings)}"
    )

    if context.historical_summary_embeddings:

        print("\nFirst Summary Record:")

        print(

            context.historical_summary_embeddings[0]

        )

    # ------------------------------------------
    # KPI Embeddings
    # ------------------------------------------

    print(
        f"\nKPI Embeddings Retrieved : "
        f"{len(context.historical_kpi_embeddings)}"
    )

    if context.historical_kpi_embeddings:

        print("\nFirst KPI Record:")

        print(

            context.historical_kpi_embeddings[0]

        )

    # ------------------------------------------
    # Assertions
    # ------------------------------------------

    assert isinstance(

        context.historical_summary_embeddings,

        list

    )

    assert isinstance(

        context.historical_kpi_embeddings,

        list

    )

    print(
        "\nHistorical Knowledge Service Test Passed!"
    )


if __name__ == "__main__":

    main()