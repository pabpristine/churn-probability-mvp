import logging
import unittest
from unittest.mock import MagicMock

from src.domain.entities.workflow_context import WorkflowContext
from src.services.kpi_embedding_service import KPIEmbeddingService


# Unit test class for KPIEmbeddingService.
class TestKPIEmbeddingService(unittest.TestCase):
    def setUp(self):
        # Disable logging output during test execution
        # so the console stays clean.
        logging.disable(logging.CRITICAL)

        # Create the service instance to be tested.
        self.service = KPIEmbeddingService()

        # Replace real external dependencies with mocks
        # so the test does not call Hugging Face or database code.
        self.service.embedding_provider = MagicMock()
        self.service.kpi_embedding_repository = MagicMock()

    def tearDown(self):
        # Re-enable logging after each test.
        logging.disable(logging.NOTSET)

    def test_process_generates_embedding_and_updates_context(self):
        # Sample KPI interpretation data used to build the embedding content.
        kpi_interpretation = {
            "client_id": "182135",
            "matched_pattern_names": [
                "High Appointment Cost",
                "Stable Lead Cost"
            ],
            "matched_patterns": [
                {
                    "pattern_name": "High Appointment Cost",
                    "interpretation": "Appointment cost is elevated compared with recent periods.",
                    "severity_level": "medium"
                },
                {
                    "pattern_name": "Stable Lead Cost",
                    "interpretation": "Lead cost is relatively stable across the measured windows.",
                    "severity_level": "low"
                }
            ],
            "overall_severity": "medium",
            "llm_summary": "The account shows stable lead cost but elevated appointment cost."
        }

        # Sample current KPI snapshot.
        current_kpis = {
            "program_type": "Seasonal",
            "program_stage": "First Month",
            "campaign_status": "Active",
            "call_center_status": "On",
            "ad_spend_7d": 580.93,
            "ad_spend_mtd": 2209.40,
            "ad_spend_30d": 2244.23,
            "lead_cost_7d": 52.81,
            "lead_cost_mtd": 52.60,
            "lead_cost_30d": 53.43,
            "appt_cost_7d": 116.19,
            "appt_cost_mtd": 157.81,
            "appt_cost_30d": 160.30
        }

        # Mock embedding provider response.
        self.service.embedding_provider.generate_embedding.return_value = {
            "embedding": [0.11, 0.22, 0.33, 0.44]
        }

        # Create workflow context with required input data.
        context = WorkflowContext(
            client_id="182135",
            client_name="Yardworx Land Management",
            current_kpis=current_kpis,
            kpi_interpretation=kpi_interpretation
        )

        # Execute the embedding service.
        updated_context = self.service.execute(context)

        # Print the output for demonstration.
        print("\n===== KPI EMBEDDING SERVICE OUTPUT =====")
        print("Client ID:", updated_context.client_id)
        print("Embedding Vector:", updated_context.kpi_embedding)
        print("Embedding Content:")
        print(updated_context.kpi_embedding_content)
        print("Embedding Metadata:", updated_context.metadata["kpi_embedding_metadata"])
        print("========================================\n")

        # Verify the provider was called exactly once.
        self.service.embedding_provider.generate_embedding.assert_called_once()

        # Verify the repository insert was called exactly once.
        self.service.kpi_embedding_repository.insert.assert_called_once()

        # Verify context was updated with the embedding vector.
        self.assertEqual(updated_context.kpi_embedding, [0.11, 0.22, 0.33, 0.44])

        # Verify content was stored directly in the context.
        self.assertIsNotNone(updated_context.kpi_embedding_content)

        # Verify metadata was stored in context metadata.
        self.assertIn("kpi_embedding_metadata", updated_context.metadata)

        # Verify some important content text exists.
        content = updated_context.kpi_embedding_content
        self.assertIn("Client: Yardworx Land Management", content)
        self.assertIn("Program Type: Seasonal", content)
        self.assertIn("Pattern key: High Appointment Cost,Stable Lead Cost", content)
        self.assertIn("Severity: medium", content)

        # Verify metadata structure.
        metadata = updated_context.metadata["kpi_embedding_metadata"]
        self.assertEqual(metadata["client_id"], "182135")
        self.assertEqual(metadata["source"], "kpi_interpretation")
        self.assertEqual(metadata["overall_severity"], "medium")
        self.assertEqual(
            metadata["matched_pattern_names"],
            ["High Appointment Cost", "Stable Lead Cost"]
        )

        # Verify payload inserted into repository.
        inserted_payload = self.service.kpi_embedding_repository.insert.call_args.args[0]
        self.assertEqual(inserted_payload["content"], updated_context.kpi_embedding_content)
        self.assertEqual(inserted_payload["embedding"], [0.11, 0.22, 0.33, 0.44])
        self.assertEqual(inserted_payload["metadata"]["client_id"], "182135")

    def test_process_uses_kpi_dataset_current_kpis_when_context_current_kpis_missing(self):
        # Mock embedding provider to return a plain list response.
        self.service.embedding_provider.generate_embedding.return_value = [0.91, 0.82, 0.73]

        # Create interpretation data.
        kpi_interpretation = {
            "matched_pattern_names": ["Stable Performance"],
            "matched_patterns": [
                {
                    "pattern_name": "Stable Performance",
                    "interpretation": "Performance is stable across tracked KPI windows.",
                    "severity_level": "low"
                }
            ],
            "overall_severity": "low",
            "llm_summary": "Stable KPI summary."
        }

        # Put KPI values only inside kpi_dataset.current_kpis
        # to verify fallback behavior.
        dataset_current_kpis = {
            "program_type": "Evergreen",
            "program_stage": "Month 2",
            "campaign_status": "Active",
            "call_center_status": "Off",
            "ad_spend_7d": 100.0,
            "ad_spend_mtd": 400.0,
            "ad_spend_30d": 1200.0,
            "lead_cost_7d": 25.0,
            "lead_cost_mtd": 27.0,
            "lead_cost_30d": 30.0,
            "appt_cost_7d": 75.0,
            "appt_cost_mtd": 82.0,
            "appt_cost_30d": 90.0
        }

        context = WorkflowContext(
            client_id="abc123",
            client_name="Fallback Client",
            current_kpis={},
            kpi_interpretation=kpi_interpretation,
            kpi_dataset={
                "client_id": "abc123",
                "current_kpis": dataset_current_kpis,
                "records": [dataset_current_kpis],
                "record_count": 1
            }
        )

        # Execute the embedding service.
        updated_context = self.service.execute(context)

        # Print fallback output for demonstration.
        print("\n===== KPI EMBEDDING FALLBACK OUTPUT =====")
        print("Client ID:", updated_context.client_id)
        print("Embedding Vector:", updated_context.kpi_embedding)
        print("Embedding Content:")
        print(updated_context.kpi_embedding_content)
        print("=========================================\n")

        # Verify the fallback KPI source was used successfully.
        self.assertEqual(updated_context.kpi_embedding, [0.91, 0.82, 0.73])

        content = updated_context.kpi_embedding_content
        self.assertIn("Client: Fallback Client", content)
        self.assertIn("Program Type: Evergreen", content)
        self.assertIn("Program Stage: Month 2", content)
        self.assertIn("Severity: low", content)

    def test_generate_embedding_accepts_vector_key(self):
        # Mock provider response using "vector" instead of "embedding".
        self.service.embedding_provider.generate_embedding.return_value = {
            "vector": [1.0, 2.0, 3.0]
        }

        # Call helper method directly.
        result = self.service._generate_embedding("Sample KPI embedding content")

        # Print helper output for demonstration.
        print("\n===== KPI EMBEDDING VECTOR KEY OUTPUT =====")
        print("Generated Vector:", result)
        print("===========================================\n")

        # Verify the returned vector is normalized properly.
        self.assertEqual(result, [1.0, 2.0, 3.0])

    def test_generate_embedding_raises_for_invalid_provider_response(self):
        # Mock provider response with an invalid format.
        self.service.embedding_provider.generate_embedding.return_value = "invalid-response"

        # Verify the helper raises ValueError.
        with self.assertRaises(ValueError):
            self.service._generate_embedding("Invalid response test content")

        # Print validation result for demonstration.
        print("\n===== KPI EMBEDDING INVALID RESPONSE OUTPUT =====")
        print("Validation test passed: invalid provider response correctly raised ValueError")
        print("=================================================\n")

    def test_validate_raises_when_client_id_missing(self):
        # Create a context without client_id
        # to test validation failure.
        context = WorkflowContext(
            client_id=None,
            kpi_interpretation={"llm_summary": "Some summary"}
        )

        # Verify the service raises ValueError.
        with self.assertRaises(ValueError):
            self.service.execute(context)

        # Print validation result for demonstration.
        print("\n===== KPI EMBEDDING VALIDATION OUTPUT =====")
        print("Validation test passed: missing client_id correctly raised ValueError")
        print("==========================================\n")

    def test_validate_raises_when_kpi_interpretation_missing(self):
        # Create a context without kpi_interpretation
        # to test validation failure.
        context = WorkflowContext(
            client_id="182135",
            kpi_interpretation={}
        )

        # Verify the service raises ValueError.
        with self.assertRaises(ValueError):
            self.service.execute(context)

        # Print validation result for demonstration.
        print("\n===== KPI EMBEDDING VALIDATION OUTPUT =====")
        print("Validation test passed: missing kpi_interpretation correctly raised ValueError")
        print("==========================================\n")

    def test_format_number_handles_none_numeric_and_text_values(self):
        # Verify None becomes $0.
        self.assertEqual(self.service._format_number(None), "$0")

        # Verify empty string becomes $0.
        self.assertEqual(self.service._format_number(""), "$0")

        # Verify numeric strings are formatted to two decimals.
        self.assertEqual(self.service._format_number("123.4"), "$123.40")

        # Verify integers are formatted to two decimals.
        self.assertEqual(self.service._format_number(50), "$50.00")

        # Verify non-numeric strings are returned as-is.
        self.assertEqual(self.service._format_number("N/A"), "N/A")

        # Print formatting examples for demonstration.
        print("\n===== KPI EMBEDDING FORMAT NUMBER OUTPUT =====")
        print("None ->", self.service._format_number(None))
        print("'' ->", self.service._format_number(""))
        print("'123.4' ->", self.service._format_number("123.4"))
        print("50 ->", self.service._format_number(50))
        print("'N/A' ->", self.service._format_number("N/A"))
        print("==============================================\n")


if __name__ == "__main__":
    unittest.main()