import logging
import unittest
from unittest.mock import MagicMock

from src.domain.entities.workflow_context import WorkflowContext
from src.services.kpi_data_service import KPIDataService


class TestKPIDataService(unittest.TestCase):
    def setUp(self):
        logging.disable(logging.CRITICAL)
        self.service = KPIDataService()
        self.service.kpi_repository = MagicMock()

    def tearDown(self):
        logging.disable(logging.NOTSET)

    def test_process_populates_kpi_dataset_and_current_kpis(self):
        mock_rows = [
            {
                "client_id": "182135",
                "client_name": "Yardworx Land Management",
                "ad_spend_7d": "580.93",
                "ad_spend_mtd": "2209.4",
                "ad_spend_30d": "2244.23",
                "lead_cost_7d": "52.81",
                "lead_cost_mtd": "52.6",
                "lead_cost_30d": "53.43",
                "appt_cost_7d": "116.19",
                "appt_cost_mtd": "157.81",
                "appt_cost_30d": "160.3",
                "appointments_7d": None,
                "appointments_mtd": None,
                "appointments_30d": None,
                "created_at": "2026-02-22 06:23:48.699252+00",
                "updated_at": "2026-02-22 06:23:48.699252+00",
                "isembeddings_created": False,
                "retry_count": 0
            }
        ]

        self.service.kpi_repository.find_by_id.return_value = mock_rows

        context = WorkflowContext(
            client_id="182135",
            client_name="Yardworx Land Management"
        )

        updated_context = self.service.execute(context)

        print("\n===== KPI DATA SERVICE OUTPUT =====")
        print("Client ID:", updated_context.kpi_dataset["client_id"])
        print("Client Name:", updated_context.current_kpis["client_name"])
        print("Record Count:", updated_context.kpi_dataset["record_count"])
        print("Current KPIs:", updated_context.current_kpis)
        print("Windows Calculated:", updated_context.kpi_dataset["windows_calculated"])
        print("===================================\n")

        self.assertIn("current_kpis", updated_context.kpi_dataset)
        self.assertEqual(updated_context.kpi_dataset["client_id"], "182135")
        self.assertEqual(updated_context.kpi_dataset["record_count"], 1)
        self.assertEqual(updated_context.current_kpis["ad_spend_7d"], 580.93)
        self.assertEqual(updated_context.current_kpis["lead_cost_7d"], 52.81)

    def test_validate_raises_when_client_id_missing(self):
        context = WorkflowContext(client_id=None)

        with self.assertRaises(ValueError):
            self.service.execute(context)

        print("\n===== KPI DATA VALIDATION OUTPUT =====")
        print("Validation test passed: missing client_id correctly raised ValueError")
        print("======================================\n")


if __name__ == "__main__":
    unittest.main()