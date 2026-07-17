import unittest
from unittest.mock import MagicMock

from src.domain.entities.workflow_context import WorkflowContext
from src.services.historical_kpi_match_service import (
    HistoricalKPIMatchService,
)


class TestHistoricalKPIMatchService(unittest.TestCase):

    def setUp(self):
        self.service = HistoricalKPIMatchService(
            match_threshold=0.65,
            match_count=5
        )

        self.service.kpi_embedding_repository = MagicMock()

    def test_returns_and_stores_historical_kpi_matches(self):
        context = WorkflowContext(
            client_id="9470852278",
            client_name="Rare Estimators",
        )

        context.kpi_embedding = [0.01] * 384

        expected_matches = [
            {
                "client_id": "7624165720",
                "client_name": "Dirt Dudes",
                "kpi_content": "Client: Dirt Dudes\n...",
                "similarity": 0.91,
            },
            {
                "client_id": "9350791453",
                "client_name": "Miller Industries",
                "kpi_content": "Client: Miller Industries\n...",
                "similarity": 0.88,
            },
        ]

        self.service.kpi_embedding_repository.match_historical_kpis.return_value = (
            expected_matches
        )

        result = self.service.process(context)

        self.assertIs(result, context)

        self.assertEqual(
            context.kpi_matches,
            expected_matches
        )

        self.assertEqual(
            context.metadata["kpi_match_count"],
            2
        )

        self.assertEqual(
            context.metadata["kpi_match_threshold"],
            0.65
        )

        self.service.kpi_embedding_repository.match_historical_kpis.assert_called_once_with(
            query_embedding=context.kpi_embedding,
            match_threshold=0.65,
            match_count=5
        )

    def test_empty_matches_are_saved_as_empty_list(self):
        context = WorkflowContext(
            client_id="9470852278"
        )

        context.kpi_embedding = [0.01] * 384

        self.service.kpi_embedding_repository.match_historical_kpis.return_value = None

        self.service.process(context)

        self.assertEqual(
            context.kpi_matches,
            []
        )

        self.assertEqual(
            context.metadata["kpi_match_count"],
            0
        )

    def test_raises_error_when_embedding_does_not_exist(self):
        context = WorkflowContext(
            client_id="9470852278"
        )

        with self.assertRaises(ValueError) as error:
            self.service.process(context)

        self.assertIn(
            "KPI embedding is required",
            str(error.exception)
        )

    def test_raises_error_when_embedding_dimension_is_not_384(self):
        context = WorkflowContext(
            client_id="9470852278"
        )

        context.kpi_embedding = [0.01] * 100

        with self.assertRaises(ValueError) as error:
            self.service.process(context)

        self.assertIn(
            "exactly 384 dimensions",
            str(error.exception)
        )


if __name__ == "__main__":
    unittest.main()