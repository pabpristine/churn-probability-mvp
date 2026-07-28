from src.base.base_service import BaseService
from src.domain.entities.workflow_context import WorkflowContext
from src.providers.embeddings.huggingface_provider import (
    HuggingFaceProvider
)
from src.repositories.summary_embedding_repository import (
    SummaryEmbeddingRepository
)


class SummaryEmbeddingService(BaseService):
    """
    Generates and persists the latest summary embedding.
    """

    def __init__(self):
        super().__init__(
            service_name="Summary Embedding Service",
            service_type="SUMMARY_EMBEDDING"
        )

        self.embedding_provider = HuggingFaceProvider()
        self.summary_embedding_repository = (
            SummaryEmbeddingRepository()
        )

    def _get_summary_text(
        self,
        context: WorkflowContext
    ):
        return (
            getattr(context, "updated_summary", None)
            or getattr(context, "final_client_summary", None)
            or getattr(context, "summary", None)
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

        summary_text = self._get_summary_text(context)
        if not summary_text:
            raise ValueError(
                "updated_summary, final_client_summary, or summary is required."
            )

        return True

    # -------------------------------------------------
    # Business Logic
    # -------------------------------------------------

    def process(
        self,
        context: WorkflowContext
    ) -> WorkflowContext:

        summary_text = self._get_summary_text(context)

        # ------------------------------------------
        # Generate Embedding
        # ------------------------------------------

        embedding = self.embedding_provider.generate_embedding(
            summary_text
        )

        # Provider may return either a list or dict
        if isinstance(embedding, dict):

            embedding = (
                embedding.get("embedding")
                or embedding.get("vector")
            )

        # ------------------------------------------
        # Metadata
        # ------------------------------------------

        metadata = {
            "client_id": context.client_id,
            "source": "summary"
        }

        # ------------------------------------------
        # Check Existing Embedding
        # ------------------------------------------

        existing = (
            self.summary_embedding_repository
            .find_by_client_id(
                context.client_id
            )
        )

        # ------------------------------------------
        # Update Existing
        # ------------------------------------------

        if existing:

            self.summary_embedding_repository.update_embedding(
                existing["id"],
                {
                    "content": summary_text,
                    "embedding": embedding,
                    "metadata": metadata
                }
            )

        # ------------------------------------------
        # Create New
        # ------------------------------------------

        else:

            self.summary_embedding_repository.save_embedding(
                summary_text,
                embedding,
                metadata
            )

        # ------------------------------------------
        # Update Workflow Context
        # ------------------------------------------

        context.summary_embedding = embedding
        context.summary_embedding_content = summary_text

        context.metadata[
            "summary_embedding_metadata"
        ] = metadata

        return context