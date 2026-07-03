import logging
import unittest
import warnings

from src.domain.entities.workflow_context import WorkflowContext
from src.workflows.kpi_workflow import KPIWorkflow


class TestKPIWorkflowIntegration(unittest.TestCase):
    def setUp(self):
        logging.disable(logging.CRITICAL)
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        warnings.filterwarnings("ignore", category=ResourceWarning)

    def tearDown(self):
        logging.disable(logging.NOTSET)
        warnings.resetwarnings()

    def test_workflow_with_real_supabase_and_real_llm(self):
        context = WorkflowContext(
            client_id="182135",
            client_name="Yardworx Land Management",
            summary=(
                "Client is active, and KPI performance should be evaluated for "
                "current risk signals and business interpretation."
            )
        )

        workflow = KPIWorkflow()
        updated_context = workflow.execute(context)

        print("\n===== REAL KPI WORKFLOW OUTPUT =====")
        print("Client ID:", updated_context.client_id)
        print("Current KPIs:", updated_context.current_kpis)
        print("KPI Dataset:", updated_context.kpi_dataset)
        print("KPI Interpretation:", updated_context.kpi_interpretation)
        print("====================================\n")

        self.assertEqual(updated_context.client_id, "182135")
        self.assertIsInstance(updated_context.kpi_dataset, dict)
        self.assertIsInstance(updated_context.kpi_interpretation, dict)
        self.assertTrue(len(updated_context.kpi_dataset) > 0)
        self.assertTrue(len(updated_context.kpi_interpretation) > 0)


if __name__ == "__main__":
    unittest.main()