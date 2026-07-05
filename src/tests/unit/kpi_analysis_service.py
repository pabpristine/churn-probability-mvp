import logging
import unittest
from unittest.mock import MagicMock


from src.domain.entities.workflow_context import WorkflowContext
from src.services.kpi_analysis_service import KPIAnalysisService


# Unit test class for KPIAnalysisService.
class TestKPIAnalysisService(unittest.TestCase):
    def setUp(self):
        # Disable logging output during test execution
        # so the console stays clean.
        logging.disable(logging.CRITICAL)

        # Create the service instance to be tested.
        self.service = KPIAnalysisService()

        # Replace external dependencies with mocks
        # so no real database or LLM calls are made.
        self.service.kpi_repository = MagicMock()
        self.service.pattern_repository = MagicMock()
        self.service.groq_provider = MagicMock()

    def tearDown(self):
        # Re-enable logging after each test.
        logging.disable(logging.NOTSET)

    def test_process_detects_patterns_and_builds_interpretation(self):
        # Sample KPI values used as input for pattern detection.
        current_kpis = {
            "client_id": "182135",
            "client_name": "Yardworx Land Management",
            "campaign_status": "Active",
            "call_center_status": None,
            "program_stage": "First Month",
            "ad_spend_7d": 580.93,
            "ad_spend_mtd": 2209.4,
            "ad_spend_30d": 2244.23,
            "lead_cost_7d": 52.81,
            "lead_cost_mtd": 52.6,
            "lead_cost_30d": 53.43,
            "appt_cost_7d": 116.19,
            "appt_cost_mtd": 157.81,
            "appt_cost_30d": 160.3
        }

        # Mock pattern repository response for each detected pattern.
        self.service.pattern_repository.find_by_pattern_name.side_effect = lambda name: [
            {
                "pattern_name": name,
                "interpretation": f"Interpretation for {name}",
                "severity_level": "medium"
            }
        ]

        # Mock the LLM response returned by the Groq provider.
        self.service.groq_provider.generate_response.return_value = {
            "content": "This is a concise KPI interpretation."
        }

        # Create workflow context with KPI data and summary.
        context = WorkflowContext(
            client_id="182135",
            client_name="Yardworx Land Management",
            summary="Client performance summary.",
            kpi_dataset={
                "client_id": "182135",
                "current_kpis": current_kpis,
                "records": [current_kpis],
                "record_count": 1
            }
        )

        # Execute the analysis service.
        updated_context = self.service.execute(context)

        # Print the analysis output for demonstration.
        print("\n===== KPI ANALYSIS SERVICE OUTPUT =====")
        print("Client ID:", updated_context.kpi_interpretation["client_id"])
        print("Matched Pattern Names:", updated_context.kpi_interpretation["matched_pattern_names"])
        print("Overall Severity:", updated_context.kpi_interpretation["overall_severity"])
        print("LLM Summary:", updated_context.kpi_interpretation["llm_summary"])
        print("Matched Patterns:", updated_context.kpi_interpretation["matched_patterns"])
        print("=======================================\n")

        # Verify the final interpretation object contains
        # the expected analysis fields.
        self.assertIn("matched_pattern_names", updated_context.kpi_interpretation)
        self.assertIn("matched_patterns", updated_context.kpi_interpretation)
        self.assertIn("overall_severity", updated_context.kpi_interpretation)
        self.assertEqual(updated_context.kpi_interpretation["client_id"], "182135")
        self.assertIsNotNone(updated_context.kpi_interpretation["llm_summary"])

    def test_falls_back_to_stable_performance_when_no_patterns(self):
        # Minimal KPI input for testing fallback behavior.
        current_kpis = {
            "client_id": "abc"
        }

        # Mock repository response for fallback pattern lookup.
        self.service.pattern_repository.find_by_pattern_name.side_effect = lambda name: [
            {
                "pattern_name": name,
                "interpretation": f"Interpretation for {name}",
                "severity_level": "low"
            }
        ]

        # Mock fallback LLM summary.
        self.service.groq_provider.generate_response.return_value = {
            "content": "Stable KPI summary."
        }

        # Force no patterns to be detected so fallback logic is used.
        self.service._detect_patterns = MagicMock(return_value=[])

        # Create workflow context for fallback testing.
        context = WorkflowContext(
            client_id="abc",
            summary="Summary text",
            kpi_dataset={
                "client_id": "abc",
                "current_kpis": current_kpis,
                "records": [current_kpis],
                "record_count": 1
            }
        )

        # Execute the analysis service.
        updated_context = self.service.execute(context)

        # Print fallback output for demonstration.
        print("\n===== KPI ANALYSIS FALLBACK OUTPUT =====")
        print("Matched Pattern Names:", updated_context.kpi_interpretation["matched_pattern_names"])
        print("Overall Severity:", updated_context.kpi_interpretation["overall_severity"])
        print("LLM Summary:", updated_context.kpi_interpretation["llm_summary"])
        print("========================================\n")

        # Verify fallback behavior uses Stable Performance
        # with low severity.
        self.assertEqual(
            updated_context.kpi_interpretation["matched_pattern_names"],
            ["Stable Performance"]
        )
        self.assertEqual(
            updated_context.kpi_interpretation["overall_severity"],
            "low"
        )

    def test_validate_raises_when_summary_missing(self):
        # Create a context with missing summary fields
        # to test validation failure.
        context = WorkflowContext(
            client_id="182135",
            summary=None,
            final_client_summary=None,
            kpi_dataset={}
        )

        # Verify the service raises ValueError
        # when required summary input is missing.
        with self.assertRaises(ValueError):
            self.service.execute(context)

        # Print validation output for demonstration.
        print("\n===== KPI ANALYSIS VALIDATION OUTPUT =====")
        print("Validation test passed: missing summary correctly raised ValueError")
        print("==========================================\n")


if __name__ == "__main__":
    unittest.main()