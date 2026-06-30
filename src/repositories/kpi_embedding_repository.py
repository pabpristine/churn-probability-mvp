from src.base.base_embedding_repository import (
    BaseEmbeddingRepository
)


class KPIEmbeddingRepository(
    BaseEmbeddingRepository
):
    """
    Repository responsible for storing and
    retrieving KPI embeddings.

    Inherits all common embedding operations
    from BaseEmbeddingRepository.
    """

    def __init__(self):

        super().__init__(
            repository_name="KPI Embedding Repository",
            table_name="client_kpi_embeddings"
        )