from src.base.base_repository import BaseRepository


class KPIRepository(BaseRepository):
    """
    Repository responsible for all database
    operations on the client_kpi table.
    """

    def __init__(self):

        super().__init__(
            repository_name="KPI Repository",
            table_name="client_kpi"
        )

    # -------------------------------------------------
    # Create
    # -------------------------------------------------

    def save(
        self,
        data
    ):
        """
        Insert a new KPI record.
        """

        return self.provider.execute(
            operation="insert",
            table=self.table_name,
            data=data
        )

    # -------------------------------------------------
    # Update
    # -------------------------------------------------

    def update(
        self,
        client_id,
        data
    ):
        """
        Update KPI data for a client.
        """

        return self.provider.execute(
            operation="update",
            table=self.table_name,
            data=data,
            filters={
                "client_id": client_id
            }
        )

    # -------------------------------------------------
    # Delete
    # -------------------------------------------------

    def delete(
        self,
        client_id
    ):
        """
        Delete KPI data for a client.
        """

        return self.provider.execute(
            operation="delete",
            table=self.table_name,
            filters={
                "client_id": client_id
            }
        )

    # -------------------------------------------------
    # Read
    # -------------------------------------------------

    def find_by_id(
        self,
        client_id
    ):
        """
        Retrieve KPI data using the client ID.
        """

        return self.provider.execute(
            operation="select",
            table=self.table_name,
            filters={
                "client_id": client_id
            }
        )

    def find_all(self):
        """
        Retrieve all KPI records.
        """

        return self.provider.execute(
            operation="select",
            table=self.table_name
        )

    # -------------------------------------------------
    # Utility
    # -------------------------------------------------

    def exists(
        self,
        client_id
    ):
        """
        Check whether KPI data exists
        for the specified client.
        """

        response = self.find_by_id(
            client_id
        )

        return len(response) > 0

    # -------------------------------------------------
    # Business Methods
    # -------------------------------------------------

    def find_by_client_name(
        self,
        client_name
    ):
        """
        Retrieve KPI data using
        the client name.
        """

        return self.provider.execute(
            operation="select",
            table=self.table_name,
            filters={
                "client_name": client_name
            }
        )

    def update_embedding_status(
        self,
        client_id,
        status=True
    ):
        """
        Mark whether KPI embeddings
        have been generated.
        """

        return self.update(
            client_id,
            {
                "isembeddings_created": status
            }
        )

    def increment_retry_count(
        self,
        client_id,
        retry_count
    ):
        """
        Update the retry count
        for a client's KPI record.
        """

        return self.update(
            client_id,
            {
                "retry_count": retry_count
            }
        )