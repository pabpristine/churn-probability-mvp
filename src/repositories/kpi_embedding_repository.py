from typing import Any, Dict

from src.base.base_embedding_repository import BaseEmbeddingRepository


# Repository responsible for storing and
# retrieving KPI embeddings.
class KPIEmbeddingRepository(BaseEmbeddingRepository):
    """
    Repository for client KPI embedding records.

    Inherits common embedding-table operations
    from BaseEmbeddingRepository.
    """

    def __init__(self):
        # Initialize repository metadata and target table name.
        super().__init__(
            repository_name="KPI Embedding Repository",
            table_name="client_kpi_embeddings"
        )

    def insert(self, data: Dict[str, Any]):
        """
        Insert a KPI embedding row into the vector table.
        """
        return self.supabase.table(self.table_name).insert(data).execute()