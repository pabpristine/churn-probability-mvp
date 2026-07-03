import logging
import unittest
import warnings

from src.domain.entities.workflow_context import WorkflowContext
from src.services.kpi_data_service import KPIDataService


class TestKPIDataServiceIntegration(unittest.TestCase):
    def setUp(self):
        logging.disable(logging.CRITICAL)
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        warnings.filterwarnings("ignore", category=ResourceWarning)
        self.service = KPIDataService()

    def tearDown(self):
        logging.disable(logging.NOTSET)
        warnings.resetwarnings()

    def test_process_with_real_supabase_data(self):
        context = WorkflowContext(
            client_id="182135",
            client_name="Yardworx Land Management"
        )

        updated_context = self.service.execute(context)

        print("\n===== REAL KPI DATA SERVICE OUTPUT =====")
        print("Client ID:", updated_context.kpi_dataset.get("client_id"))
        print("Client Name:", updated_context.current_kpis.get("client_name"))
        print("Record Count:", updated_context.kpi_dataset.get("record_count"))
        print("Windows Calculated:", updated_context.kpi_dataset.get("windows_calculated"))
        print("Current KPIs:", updated_context.current_kpis)
        print("========================================\n")

        self.assertEqual(updated_context.kpi_dataset.get("client_id"), "182135")
        self.assertGreaterEqual(updated_context.kpi_dataset.get("record_count", 0), 1)
        self.assertIsInstance(updated_context.current_kpis, dict)
        self.assertTrue(len(updated_context.current_kpis) > 0)


if __name__ == "__main__":
    unittest.main()