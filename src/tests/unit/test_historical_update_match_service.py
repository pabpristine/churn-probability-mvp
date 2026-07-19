import unittest
from unittest.mock import patch

from src.domain.entities.workflow_context import WorkflowContext
from src.services.historical_update_match_service import HistoricalUpdateMatchService


MOCK_MATCHES = [
    {
        "client_id": "182135",
        "client_name": "Yardworx Land Management",
        "summary": "Client showed delayed payments and lower engagement.",
        "similarity": 0.91
    },
    {
        "client_id": "182999",
        "client_name": "GreenScape Services",
        "summary": "Client had weak follow-up response and declining sentiment.",
        "similarity": 0.84
    }
]


class TestHistoricalUpdateMatchService(unittest.TestCase):

    @patch(
        "src.services.historical_update_match_service.ClientUpdateEmbeddingRepository"
    )
    def test_valid_summary_embedding_returns_and_stores_matches(
        self,
        MockRepository
    ):
        mock_repository = MockRepository.return_value
        mock_repository.match_historical_clients.return_value = MOCK_MATCHES

        service = HistoricalUpdateMatchService()
        context = WorkflowContext()
        context.summary_embedding = [0.1] * 384
        context.metadata = {}

        result = service.process(context)

        mock_repository.match_historical_clients.assert_called_once_with(
            query_embedding=context.summary_embedding,
            match_threshold=0.65,
            match_count=5
        )

        self.assertEqual(result.update_matches, MOCK_MATCHES)
        self.assertEqual(result.metadata["update_match_count"], 2)
        self.assertEqual(result.metadata["update_match_threshold"], 0.65)

    @patch(
        "src.services.historical_update_match_service.ClientUpdateEmbeddingRepository"
    )
    def test_no_matches_stores_empty_list(
        self,
        MockRepository
    ):
        mock_repository = MockRepository.return_value
        mock_repository.match_historical_clients.return_value = []

        service = HistoricalUpdateMatchService()
        context = WorkflowContext()
        context.summary_embedding = [0.1] * 384
        context.metadata = {}

        result = service.process(context)

        self.assertEqual(result.update_matches, [])
        self.assertEqual(result.metadata["update_match_count"], 0)
        self.assertEqual(result.metadata["update_match_threshold"], 0.65)

    def test_missing_summary_embedding_raises_value_error(self):
        service = HistoricalUpdateMatchService()
        context = WorkflowContext()
        context.summary_embedding = None
        context.metadata = {}

        with self.assertRaises(ValueError) as error:
            service.process(context)

        self.assertEqual(
            str(error.exception),
            "Summary embedding is required before historical update matching."
        )

    def test_non_384_summary_embedding_raises_value_error(self):
        service = HistoricalUpdateMatchService()
        context = WorkflowContext()
        context.summary_embedding = [0.1] * 100
        context.metadata = {}

        with self.assertRaises(ValueError) as error:
            service.process(context)

        self.assertEqual(
            str(error.exception),
            "Summary embedding must contain exactly 384 dimensions."
        )

    @patch(
        "src.services.historical_update_match_service.ClientUpdateEmbeddingRepository"
    )
    def test_repository_called_with_expected_arguments(
        self,
        MockRepository
    ):
        mock_repository = MockRepository.return_value
        mock_repository.match_historical_clients.return_value = MOCK_MATCHES

        service = HistoricalUpdateMatchService(
            match_threshold=0.65,
            match_count=5
        )

        context = WorkflowContext()
        context.summary_embedding = [0.1] * 384
        context.metadata = {}

        service.process(context)

        mock_repository.match_historical_clients.assert_called_once_with(
            query_embedding=context.summary_embedding,
            match_threshold=0.65,
            match_count=5
        )


if __name__ == "__main__":
    unittest.main()