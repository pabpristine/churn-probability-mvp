from src.base.base_service import BaseService
from src.domain.entities.workflow_context import WorkflowContext
from src.providers.embeddings.huggingface_provider import (
    HuggingFaceProvider
)
from src.repositories.weighted_embedding_repository import (
    WeightedEmbeddingRepository
)


class WeightedEmbeddingService(BaseService):
    """
    Generates a weighted embedding by combining
    the summary embedding and KPI embedding,
    persists it, and updates the workflow context.
    """

    SUMMARY_WEIGHT = 0.7
    KPI_WEIGHT = 0.3

    def __init__(self):

        super().__init__(
            service_name="Weighted Embedding Service",
            service_type="WEIGHTED_EMBEDDING"
        )

        self.embedding_provider = HuggingFaceProvider()

        self.weighted_embedding_repository = (
            WeightedEmbeddingRepository()
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

        if not context.summary_embedding:
            raise ValueError(
                "Summary embedding is required."
            )

        if not context.kpi_embedding:
            raise ValueError(
                "KPI embedding is required."
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
        # Generate Weighted Embedding
        # ------------------------------------------
        summary_embedding = context.summary_embedding
        kpi_embedding = context.kpi_embedding

        if isinstance(summary_embedding, dict):
            summary_embedding = summary_embedding["embedding"]

        if isinstance(kpi_embedding, dict):
            kpi_embedding = kpi_embedding["embedding"]


        weighted_embedding = (
            self.embedding_provider.generate_weighted_embedding(

                summary_embedding=context.summary_embedding,

                kpi_embedding=context.kpi_embedding,

                summary_weight=self.SUMMARY_WEIGHT,

                kpi_weight=self.KPI_WEIGHT

            )
        )

        # ------------------------------------------
        # Build Content
        # ------------------------------------------

        kpi_summary = ""

        if context.kpi_interpretation:

            kpi_summary = context.kpi_interpretation.get(
                "llm_summary",
                ""
            )

        content = f"""
Summary

{context.summary or ""}

----------------------------------------

KPI Summary

{kpi_summary}
""".strip()

        # ------------------------------------------
        # Metadata
        # ------------------------------------------

        metadata = {

            "client_id": context.client_id,

            "source": "weighted",

            "summary_weight": self.SUMMARY_WEIGHT,

            "kpi_weight": self.KPI_WEIGHT

        }

        # ------------------------------------------
        # Check Existing Record
        # ------------------------------------------

        existing = (
            self.weighted_embedding_repository
            .find_by_client_id(
                context.client_id
            )
        )

        # ------------------------------------------
        # Update Existing
        # ------------------------------------------

        if existing:

            self.weighted_embedding_repository.update_embedding(

                existing["id"],

                {

                    "content": content,

                    "embedding": weighted_embedding,

                    "metadata": metadata

                }

            )

        # ------------------------------------------
        # Create New
        # ------------------------------------------

        else:

            self.weighted_embedding_repository.save_embedding(

                content,

                weighted_embedding,

                metadata

            )

        # ------------------------------------------
        # Update Workflow Context
        # ------------------------------------------

        context.weighted_embedding = weighted_embedding

        context.weighted_embedding_content = content

        context.metadata[
            "weighted_embedding_metadata"
        ] = metadata

        return context