from src.workflows.input_pipeline_orchestrator import InputPipelineOrchestrator


def test_red_circle_flow_real_execution():
    orchestrator = InputPipelineOrchestrator()

    context = orchestrator.run("give me churn analysis for Yardworx Land Management")

    assert context is not None
    assert context.client_name is not None
    assert context.client_id is not None

    assert hasattr(context, "google_sheet_data")
    assert context.google_sheet_data is not None

    assert hasattr(context, "client_updates")
    assert isinstance(context.client_updates, list)

    assert hasattr(context, "is_new_client")

    assert hasattr(context, "kpi_dataset")
    assert context.kpi_dataset is not None
    assert context.kpi_dataset.get("client_id") == context.client_id