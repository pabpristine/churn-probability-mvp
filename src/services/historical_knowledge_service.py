from src.base.base_service import BaseService
from src.domain.entities.workflow_context import WorkflowContext

from src.repositories.summary_embedding_repository import (
    SummaryEmbeddingRepository
)

from src.repositories.kpi_embedding_repository import (
    KPIEmbeddingRepository
)


class HistoricalKnowledgeService(BaseService):
    """
    Fetches historical summary and KPI embeddings
    for downstream similarity search.
    """

    def __init__(self):

        super().__init__(
            service_name="Historical Knowledge Service",
            service_type="RETRIEVAL"
        )

        self.summary_repository = (
            SummaryEmbeddingRepository()
        )

        self.kpi_repository = (
            KPIEmbeddingRepository()
        )

    # -------------------------------------------------
    # Validation
    # -------------------------------------------------

    def validate(
        self,
        context: WorkflowContext
    ):

        if not context.client_id:

            raise ValueError(
                "Client ID is required."
            )

        return True

    # -------------------------------------------------
    # Business Logic
    # -------------------------------------------------

    def process(
        self,
        context: WorkflowContext
    ) -> WorkflowContext:

        # ------------------------------------------
        # Fetch Summary Embeddings
        # ------------------------------------------

        summary_embeddings = (
            self.summary_repository.find_all()
        )

        historical_summary_embeddings = []

        for embedding in summary_embeddings:

            metadata = embedding.get("metadata", {})

            if not isinstance(metadata, dict):
                continue

            client_id = metadata.get("client_id")

            if client_id is None:
                continue

            if str(client_id) != str(context.client_id):

                historical_summary_embeddings.append(
                    embedding
                )

        # ------------------------------------------
        # Fetch KPI Embeddings
        # ------------------------------------------

        kpi_embeddings = (
            self.kpi_repository.find_all()
        )

        historical_kpi_embeddings = []

        for embedding in kpi_embeddings:

            metadata = embedding.get("metadata", {})

            if not isinstance(metadata, dict):
                continue

            client_id = metadata.get("client_id")

            if client_id is None:
                continue

            if str(client_id) != str(context.client_id):

                historical_kpi_embeddings.append(
                    embedding
                )

        # ------------------------------------------
        # Store in Workflow Context
        # ------------------------------------------

        context.historical_summary_embeddings = (
            historical_summary_embeddings
        )

        context.historical_kpi_embeddings = (
            historical_kpi_embeddings
        )

        return context