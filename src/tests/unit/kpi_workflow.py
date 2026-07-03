import unittest
from unittest.mock import patch

from src.domain.entities.workflow_context import WorkflowContext
from src.workflows.kpi_workflow import KPIWorkflow


class TestKPIWorkflow(unittest.TestCase):
    @patch("src.workflows.kpi_workflow.KPIAnalysisService")
    @patch("src.workflows.kpi_workflow.KPIDataService")
    def test_workflow_executes_services_in_sequence(
        self,
        mock_kpi_data_service_cls,
        mock_kpi_analysis_service_cls
    ):
        context = WorkflowContext(
            client_id="182135",
            client_name="Yardworx Land Management",
            summary="Client summary"
        )

        data_service_instance = mock_kpi_data_service_cls.return_value
        analysis_service_instance = mock_kpi_analysis_service_cls.return_value

        data_service_instance.execute.return_value = context
        analysis_service_instance.execute.return_value = context

        workflow = KPIWorkflow()
        result = workflow.execute(context)

        self.assertEqual(result.client_id, "182135")
        self.assertEqual(len(workflow.services), 2)
        data_service_instance.execute.assert_called_once()
        analysis_service_instance.execute.assert_called_once()


if __name__ == "__main__":
    unittest.main()