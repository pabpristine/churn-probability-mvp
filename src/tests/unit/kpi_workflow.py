import unittest
from unittest.mock import patch

from src.domain.entities.workflow_context import WorkflowContext
from src.workflows.kpi_workflow import KPIWorkflow


# Unit test class for verifying KPIWorkflow behavior.
class TestKPIWorkflow(unittest.TestCase):
    # Patch all services so the workflow can be tested
    # without calling real service implementations.
    @patch("src.workflows.kpi_workflow.KPIEmbeddingService")
    @patch("src.workflows.kpi_workflow.KPIAnalysisService")
    @patch("src.workflows.kpi_workflow.KPIDataService")
    def test_workflow_executes_services_in_sequence(
        self,
        mock_kpi_data_service_cls,
        mock_kpi_analysis_service_cls,
        mock_kpi_embedding_service_cls
    ):
        # Create a sample workflow context to pass into the workflow.
        context = WorkflowContext(
            client_id="182135",
            client_name="Yardworx Land Management",
            summary="Client summary"
        )

        # Get the mocked service instances returned by the patched classes.
        data_service_instance = mock_kpi_data_service_cls.return_value
        analysis_service_instance = mock_kpi_analysis_service_cls.return_value
        embedding_service_instance = mock_kpi_embedding_service_cls.return_value

        # Make all mocked services return the same context
        # after execution to simulate normal workflow behavior.
        data_service_instance.execute.return_value = context
        analysis_service_instance.execute.return_value = context
        embedding_service_instance.execute.return_value = context

        # Create the workflow and execute it with the sample context.
        workflow = KPIWorkflow()
        result = workflow.execute(context)

        # Verify the workflow returns the expected context.
        self.assertEqual(result.client_id, "182135")

        # Verify all services were added to the workflow.
        self.assertEqual(len(workflow.services), 3)

        # Verify each service was executed exactly once.
        data_service_instance.execute.assert_called_once()
        analysis_service_instance.execute.assert_called_once()
        embedding_service_instance.execute.assert_called_once()

        # Verify the services were executed in the expected order.
        self.assertEqual(workflow.services[0], data_service_instance)
        self.assertEqual(workflow.services[1], analysis_service_instance)
        self.assertEqual(workflow.services[2], embedding_service_instance)


if __name__ == "__main__":
    unittest.main()