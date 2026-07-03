import logging
import unittest
import warnings

from src.domain.entities.workflow_context import WorkflowContext
from src.services.kpi_analysis_service import KPIAnalysisService
from src.services.kpi_data_service import KPIDataService


class TestKPIAnalysisServiceIntegration(unittest.TestCase):
    def setUp(self):
        logging.disable(logging.CRITICAL)
        warnings.filterwarnings("ignore", category=DeprecationWarning)
        warnings.filterwarnings("ignore", category=ResourceWarning)
        self.data_service = KPIDataService()
        self.analysis_service = KPIAnalysisService()

    def tearDown(self):
        logging.disable(logging.NOTSET)
        warnings.resetwarnings()

    def test_process_with_real_supabase_and_real_llm(self):
        context = WorkflowContext(
            client_id="182135",
            client_name="Yardworx Land Management",
            summary=(
                "Client is active, but recent campaign efficiency and spend trends "
                "need to be evaluated against KPI patterns."
            )
        )

        context = self.data_service.execute(context)
        updated_context = self.analysis_service.execute(context)

        print("\n===== REAL KPI ANALYSIS SERVICE OUTPUT =====")
        print("Client ID:", updated_context.kpi_interpretation.get("client_id"))
        print("Matched Pattern Names:", updated_context.kpi_interpretation.get("matched_pattern_names"))
        print("Overall Severity:", updated_context.kpi_interpretation.get("overall_severity"))
        print("Matched Patterns:", updated_context.kpi_interpretation.get("matched_patterns"))
        print("LLM Summary:", updated_context.kpi_interpretation.get("llm_summary"))
        print("============================================\n")

        self.assertEqual(updated_context.kpi_interpretation.get("client_id"), "182135")
        self.assertIn("matched_pattern_names", updated_context.kpi_interpretation)
        self.assertIn("matched_patterns", updated_context.kpi_interpretation)
        self.assertIn("overall_severity", updated_context.kpi_interpretation)
        self.assertTrue(
            updated_context.kpi_interpretation.get("llm_summary") is None
            or len(updated_context.kpi_interpretation.get("llm_summary", "").strip()) > 0
        )


if __name__ == "__main__":
    unittest.main()