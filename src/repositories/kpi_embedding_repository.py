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

    def match_historical_kpis(
        self,
        query_embedding,
        match_threshold: float = 0.65,
        match_count: int = 5
    ):
        """
        Calls the Supabase RPC function that runs KPI vector similarity search.
        """

        response = (
            self.supabase
            .rpc(
                "match_historical_kpis",
                {
                    "query_embedding": query_embedding,
                    "match_threshold": match_threshold,
                    "match_count": match_count,
                }
            )
            .execute()
        )

        return response.data or []