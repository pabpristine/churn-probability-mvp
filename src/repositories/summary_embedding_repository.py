from src.base.base_embedding_repository import (
    BaseEmbeddingRepository
)


class SummaryEmbeddingRepository(
    BaseEmbeddingRepository
):
    """
    Repository responsible for storing and
    retrieving summary embeddings.

    Inherits all common embedding operations
    from BaseEmbeddingRepository.
    """

    def __init__(self):

        super().__init__(
            repository_name="Summary Embedding Repository",
            table_name="client_summary_embeddings"
        )