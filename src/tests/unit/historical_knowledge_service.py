import logging
import unittest
from unittest.mock import MagicMock

from src.domain.entities.workflow_context import WorkflowContext
from src.services.historical_knowledge_service import (
    HistoricalKnowledgeService
)


# Unit test class for HistoricalKnowledgeService.
class TestHistoricalKnowledgeService(unittest.TestCase):
    def setUp(self):
        # Disable logging output during test execution
        # so the console stays clean except for print statements.
        logging.disable(logging.CRITICAL)

        # Create the service instance to be tested.
        self.service = HistoricalKnowledgeService()

        # Replace external dependencies with mocks
        # so no real embedding model or database calls are made.
        self.service.huggingface_provider = MagicMock()
        self.service.weighted_embedding_repository = MagicMock()

    def tearDown(self):
        # Re-enable logging after each test.
        logging.disable(logging.NOTSET)

    def test_process_builds_profile_and_returns_historical_matches(self):
        # Mock the embedding provider to return a fake vector.
        self.service.huggingface_provider.generate_embedding.return_value = {
            "embedding": [0.1, 0.2, 0.3],
            "dimension": 3,
            "model": "fake-model"
        }

        # Mock the repository to return sample similarity matches,
        # including one for the current client that should be filtered out.
        self.service.weighted_embedding_repository.find_similar.return_value = [
            {
                "id": "match-1",
                "content": "Summary: ... KPIs: ...",
                "metadata": {"client_id": "999999"},
                "similarity": 0.91
            },
            {
                "id": "match-2",
                "content": "Summary: ... KPIs: ...",
                "metadata": {"client_id": "182135"},  # same as current client
                "similarity": 0.99
            }
        ]

        # Create workflow context representing the current client's state.
        context = WorkflowContext(
            client_id="182135",
            client_name="Yardworx Land Management",
            program_type="Lead Generation",
            program_stage="Scaling",
            program_duration="120",
            campaign_status="Active",
            final_client_summary="Client performance is trending upward.",
            kpi_interpretation={
                "matched_pattern_names": ["Scaling Success"],
                "overall_severity": "low"
            }
        )

        # Execute the service.
        updated_context = self.service.execute(context)

        # Print output for demonstration.
        print("\n===== HISTORICAL KNOWLEDGE SERVICE OUTPUT =====")
        print("Historical Matches:", updated_context.historical_matches)
        print("================================================\n")

        # Verify the current client's own record was excluded.
        match_ids = [m["id"] for m in updated_context.historical_matches]
        self.assertIn("match-1", match_ids)
        self.assertNotIn("match-2", match_ids)

        # Verify the embedding provider was called once with a text profile.
        self.service.huggingface_provider.generate_embedding.assert_called_once()
        embed_call_kwargs = (
            self.service.huggingface_provider.generate_embedding.call_args.kwargs
        )
        self.assertIn("text", embed_call_kwargs)
        self.assertIn("Scaling Success", embed_call_kwargs["text"])
        self.assertIn("Active", embed_call_kwargs["text"])

        # Verify the repository was called with the embedding vector.
        self.service.weighted_embedding_repository.find_similar.assert_called_once()
        find_call_kwargs = (
            self.service.weighted_embedding_repository.find_similar.call_args.kwargs
        )
        self.assertEqual(find_call_kwargs["query_embedding"], [0.1, 0.2, 0.3])
        self.assertEqual(find_call_kwargs["match_count"], 5)
        self.assertEqual(find_call_kwargs["match_threshold"], 0.75)

    def test_validate_raises_when_client_id_missing(self):
        # Create a context missing the required client_id.
        context = WorkflowContext(
            client_id=None,
            final_client_summary="Some summary."
        )

        # Verify the service raises ValueError when client_id is missing.
        with self.assertRaises(ValueError):
            self.service.execute(context)

        print("\n===== HISTORICAL KNOWLEDGE VALIDATION OUTPUT =====")
        print("Validation test passed: missing client_id correctly raised ValueError")
        print("===================================================\n")

    def test_validate_raises_when_no_summary_or_kpi_interpretation(self):
        # Create a context with no summary and no KPI interpretation.
        context = WorkflowContext(
            client_id="182135",
            summary=None,
            final_client_summary=None,
            kpi_interpretation={}
        )

        # Verify the service raises ValueError when there is nothing
        # to build a retrieval profile from.
        with self.assertRaises(ValueError):
            self.service.execute(context)

        print("\n===== HISTORICAL KNOWLEDGE VALIDATION OUTPUT =====")
        print("Validation test passed: missing summary/kpi correctly raised ValueError")
        print("===================================================\n")

    def test_process_falls_back_to_summary_when_final_summary_missing(self):
        # Mock the embedding provider and repository.
        self.service.huggingface_provider.generate_embedding.return_value = {
            "embedding": [0.4, 0.5, 0.6],
            "dimension": 3,
            "model": "fake-model"
        }
        self.service.weighted_embedding_repository.find_similar.return_value = []

        # Create context with only the older "summary" field populated.
        context = WorkflowContext(
            client_id="182135",
            summary="Older rolling summary text.",
            final_client_summary=None,
            kpi_interpretation={
                "matched_pattern_names": [],
                "overall_severity": "low"
            }
        )

        # Execute the service.
        updated_context = self.service.execute(context)

        # Verify the fallback summary text made it into the embedded profile.
        embed_call_kwargs = (
            self.service.huggingface_provider.generate_embedding.call_args.kwargs
        )
        self.assertIn("Older rolling summary text.", embed_call_kwargs["text"])

        # Verify empty results are handled gracefully.
        self.assertEqual(updated_context.historical_matches, [])


if __name__ == "__main__":
    unittest.main()