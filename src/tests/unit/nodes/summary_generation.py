from src.domain.entities.workflow_context import (
    WorkflowContext
)

from src.nodes.client_data_retrieval_service import (
    ClientDataRetrievalService
)

from src.nodes.updates_data_service import (
    UpdatesDataService
)

from src.nodes.summary_batch_preparation_service import (
    SummaryBatchPreparationService
)

from src.nodes.summary_service import (
    SummaryService
)


def main():

    # -------------------------------------------------
    # Create Workflow Context
    # -------------------------------------------------

    context = WorkflowContext()

    context.client_name = (
        "Yardworx Land Management"
    )

    print("\n========== SUMMARY SERVICE TEST ==========\n")

    # -------------------------------------------------
    # Retrieve Client Data
    # -------------------------------------------------

    print("Step 1 : Retrieving Client Data")

    context = (
        ClientDataRetrievalService()
        .execute(context)
    )

    # -------------------------------------------------
    # Retrieve Previous Summary
    # -------------------------------------------------

    print("Step 2 : Retrieving Previous Summary")

    context = (
        UpdatesDataService()
        .execute(context)
    )

    # -------------------------------------------------
    # Prepare Batches
    # -------------------------------------------------

    print("Step 3 : Preparing Summary Batches")

    context = (
        SummaryBatchPreparationService()
        .execute(context)
    )

    # -------------------------------------------------
    # Generate Updated Summary
    # -------------------------------------------------

    print("Step 4 : Generating Updated Summary")

    context = (
        SummaryService()
        .execute(context)
    )

    # -------------------------------------------------
    # Display Results
    # -------------------------------------------------

    print("\n")
    print("=" * 100)
    print("FINAL UPDATED SUMMARY")
    print("=" * 100)

    print()

    print(
        context.updated_summary
    )

    print()

    print("=" * 100)
    print("UPDATED SATISFACTION SCORE")
    print("=" * 100)

    print()

    print(
        context.updated_satisfaction_score
    )

    print()

    print("=" * 100)
    print("TOKEN USAGE")
    print("=" * 100)

    print()

    for key, value in context.llm_usage.items():

        print(
            f"{key:<20}: {value}"
        )


if __name__ == "__main__":

    main()
    