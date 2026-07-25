from src.domain.entities.workflow_context import WorkflowContext

from src.nodes.historical_knowledge_service import HistoricalKnowledgeService
from src.nodes.historical_update_match_service import HistoricalUpdateMatchService
from src.nodes.historical_kpi_match_service import HistoricalKPIMatchService


class HistoricalRetrievalOrchestrator:
    """
    Orchestrates the historical retrieval flow:
    Historical Knowledge -> Historical Update Match -> Historical KPI Match
    """

    def __init__(self):
        self.historical_knowledge_service = HistoricalKnowledgeService()
        self.historical_update_match_service = HistoricalUpdateMatchService()
        self.historical_kpi_match_service = HistoricalKPIMatchService()

    def validate(self, context: WorkflowContext) -> bool:
        if context is None:
            raise ValueError("WorkflowContext cannot be None.")

        if not context.client_id:
            raise ValueError("client_id is required before historical retrieval flow.")

        if not context.summary_embedding:
            raise ValueError("summary_embedding is required before historical update matching.")

        if not context.kpi_embedding:
            raise ValueError("kpi_embedding is required before historical KPI matching.")

        return True

    def run_with_context(self, context: WorkflowContext) -> WorkflowContext:
        self.validate(context)

        context = self.historical_knowledge_service.execute(context)
        context = self.historical_update_match_service.execute(context)
        context = self.historical_kpi_match_service.execute(context)

        return context