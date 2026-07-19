from src.base.base_service import BaseService
from src.domain.entities.workflow_context import WorkflowContext
from src.repositories.kpi_embedding_repository import KPIEmbeddingRepository


class HistoricalKPIMatchService(BaseService):
    """
    Retrieves historical client KPI profiles that are semantically similar
    to the current client's generated KPI embedding.

    Requires the Supabase function:
    public.match_historical_kpis(
        query_embedding vector(384),
        match_threshold float,
        match_count int
    )
    """

    DEFAULT_MATCH_THRESHOLD = 0.65
    DEFAULT_MATCH_COUNT = 5

    def __init__(
        self,
        match_threshold: float = DEFAULT_MATCH_THRESHOLD,
        match_count: int = DEFAULT_MATCH_COUNT
    ):
        super().__init__(
            service_name="Historical KPI Match Service",
            service_type="KPI_RETRIEVAL"
        )

        self.match_threshold = match_threshold
        self.match_count = match_count

        self.kpi_embedding_repository = (
            KPIEmbeddingRepository()
        )

    def validate(
        self,
        context: WorkflowContext
    ) -> bool:
        """
        A KPI embedding must be generated before historical retrieval.
        """

        if not context.kpi_embedding:
            raise ValueError(
                "KPI embedding is required before historical KPI matching."
            )

        if len(context.kpi_embedding) != 384:
            raise ValueError(
                "KPI embedding must contain exactly 384 dimensions."
            )

        return True

    def process(
        self,
        context: WorkflowContext
    ) -> WorkflowContext:
        """
        Call the SQL RPC function and store the best historical KPI matches.
        """

        self.validate(context)

        matches = (
            self.kpi_embedding_repository
            .match_historical_kpis(
                query_embedding=context.kpi_embedding,
                match_threshold=self.match_threshold,
                match_count=self.match_count
            )
        )

        context.kpi_matches = matches or []

        context.metadata["kpi_match_count"] = len(
            context.kpi_matches
        )

        context.metadata["kpi_match_threshold"] = (
            self.match_threshold
        )

        return context