from src.base.base_repository import BaseRepository


class ClientUpdateEmbeddingRepository(BaseRepository):
    """
    Repository for the client_update_embeddings table.
    Provides semantic similarity search via the Supabase RPC:
    public.match_historical_clients(
        query_embedding vector(384),
        match_threshold float,
        match_count int
    )
    """

    def __init__(self):
        super().__init__(
            repository_name="Client Update Embedding Repository",
            table_name="client_update_embeddings"
        )

    def match_historical_clients(
        self,
        query_embedding: list,
        match_threshold: float = 0.65,
        match_count: int = 5,
    ) -> list:
        response = (
            self.supabase
            .rpc(
                "match_historical_clients",
                {
                    "query_embedding": query_embedding,
                    "match_threshold": match_threshold,
                    "match_count": match_count,
                }
            )
            .execute()
        )

        return response.data or []