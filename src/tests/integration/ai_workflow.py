from src.workflows.ai_workflow_orchestrator import AIWorkflowOrchestrator


def test_ai_workflow():

    orchestrator = AIWorkflowOrchestrator()

    context = orchestrator.run(
        "give me churn analysis for Yardworx Land Management"
    )

    print("\n========== CLIENT ==========")
    print("Client ID:", context.client_id)
    print("Client Name:", context.client_name)

    print("\n========== SUMMARY ==========")
    print(context.updated_summary)
    print("Satisfaction Score:", context.updated_satisfaction_score)

    print("\n========== KPI ==========")
    print(context.kpi_interpretation)

    print("\n========== SUMMARY CHURN ==========")
    print("Probability:", context.summary_probability)
    print("Analysis:", context.summary_analysis)

    print("\n========== KPI CHURN ==========")
    print("Probability:", context.kpi_probability)
    print("Analysis:", context.kpi_analysis)

    print("\n========== FINAL CHURN ==========")
    print("Probability:", context.final_probability)
    print("Risk Level:", context.risk_level)
    print("Analysis:", context.final_analysis)

    print("\n========== RECOMMENDATIONS ==========")
    for index, recommendation in enumerate(context.recommendations, start=1):
        print(f"{index}. {recommendation}")

    print("\n========== LLM USAGE ==========")
    print(context.llm_usage)

    print("\n========== METADATA ==========")
    print(context.metadata)


if __name__ == "__main__":
    test_ai_workflow()