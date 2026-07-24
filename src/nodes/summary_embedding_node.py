from src.base.base_service import BaseService
from src.domain.entities.workflow_context import WorkflowContext
from src.providers.embeddings.huggingface_provider import (
    HuggingFaceProvider
)
from src.repositories.summary_embedding_repository import (
    SummaryEmbeddingRepository
)


class SummaryEmbeddingNode(BaseService):
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

        if not context.updated_summary:
            raise ValueError(
                "Summary is required."
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
        # Generate Embedding
        # ------------------------------------------

        embedding = self.embedding_provider.generate_embedding(
            context.updated_summary
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

                    "content": context.updated_summary,

                    "embedding": embedding,

                    "metadata": metadata

                }

            )

        # ------------------------------------------
        # Create New
        # ------------------------------------------

        else:

            self.summary_embedding_repository.save_embedding(

                context.updated_summary,

                embedding,

                metadata

            )

        # ------------------------------------------
        # Update Workflow Context
        # ------------------------------------------

        context.summary_embedding = embedding

        context.summary_embedding_content = (
            context.updated_summary
        )

        context.metadata[
            "summary_embedding_metadata"
        ] = metadata

        return context