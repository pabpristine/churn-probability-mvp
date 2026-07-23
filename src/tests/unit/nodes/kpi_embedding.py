from src.domain.entities.workflow_context import WorkflowContext
from src.nodes.kpi_embedding import KPIEmbeddingService


def main():

    print("\n========== KPI EMBEDDING SERVICE TEST ==========\n")

    context = WorkflowContext()

    # -------------------------------------------------
    # Test Client
    # -------------------------------------------------

    context.client_id = 182135

    context.client_name = "Yardworx Land Management"

    # -------------------------------------------------
    # Sample KPI Snapshot
    # -------------------------------------------------

    context.current_kpis = {

        "program_type": "Landscaping",

        "program_stage": "Scaling",

        "campaign_status": "Active",

        "call_center_status": "Healthy",

        "ad_spend_7d": 850,

        "ad_spend_mtd": 3200,

        "ad_spend_30d": 5600,

        "lead_cost_7d": 62,

        "lead_cost_mtd": 59,

        "lead_cost_30d": 61,

        "appt_cost_7d": 145,

        "appt_cost_mtd": 152,

        "appt_cost_30d": 149

    }

    # -------------------------------------------------
    # Sample KPI Interpretation
    # -------------------------------------------------

    context.kpi_interpretation = {

        "matched_pattern_names": [

            "Stable Campaign",

            "Healthy Lead Cost"

        ],

        "overall_severity": "LOW",

        "llm_summary": (
            "Campaign is performing consistently. "
            "Lead costs remain healthy while ad spend "
            "is stable. Continue monitoring current trend."
        ),

        "matched_patterns": [

            {

                "interpretation":
                "Lead acquisition costs are within the expected range."

            },

            {

                "interpretation":
                "Advertising spend is producing consistent results."

            }

        ]

    }

    # -------------------------------------------------
    # Execute Service
    # -------------------------------------------------

    service = KPIEmbeddingService()

    context = service.execute(
        context
    )

    # -------------------------------------------------
    # Print Results
    # -------------------------------------------------

    print("\n========== KPI EMBEDDING ==========\n")

    print("Embedding Dimension")
    print("-" * 50)
    print(len(context.kpi_embedding))

    print("\nFirst 10 Values")
    print("-" * 50)
    print(context.kpi_embedding[:10])

    print("\nContent")
    print("-" * 50)
    print(context.kpi_embedding_content)

    print("\nMetadata")
    print("-" * 50)
    print(
        context.metadata.get(
            "kpi_embedding_metadata"
        )
    )


if __name__ == "__main__":
    main()