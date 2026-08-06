from src.workflows.ai_workflow_orchestrator import AIWorkflowOrchestrator


def main():
    # Yaha client ka exact naam daal do
    user_query = "Give me churn and KPI analysis for Anvil Custom (ID 967783)"

    orchestrator = AIWorkflowOrchestrator()
    context = orchestrator.run(user_query)

    print("=== Workflow Execution Completed ===")
    print("Execution ID:", context.metadata.get("execution_id"))
    print("Client ID:", context.client_id)
    print("Client Name:", context.client_name)
    print("Final Probability:", context.final_probability)
    print("Risk Level:", context.risk_level)


if __name__ == "__main__":
    main()