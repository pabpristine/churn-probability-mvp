from src.base.base_repository import BaseRepository


class ClientRepository(BaseRepository):
    """
    Repository responsible for all database
    operations on the client_updates table.
    """

    def __init__(self):

        super().__init__(
            repository_name="Client Repository",
            table_name="client_updates"
        )

    # -------------------------------------------------
    # Create
    # -------------------------------------------------

    def save(
        self,
        data
    ):
        """
        Insert a new client update.
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
        update_id,
        data
    ):
        """
        Update an existing client update.
        """

        return self.provider.execute(
            operation="update",
            table=self.table_name,
            data=data,
            filters={
                "id": update_id
            }
        )

    # -------------------------------------------------
    # Delete
    # -------------------------------------------------

    def delete(
        self,
        update_id
    ):
        """
        Delete a client update.
        """

        return self.provider.execute(
            operation="delete",
            table=self.table_name,
            filters={
                "id": update_id
            }
        )

    # -------------------------------------------------
    # Read
    # -------------------------------------------------

    def find_by_id(
        self,
        update_id
    ):
        """
        Retrieve a client update by ID.
        """

        return self.provider.execute(
            operation="select",
            table=self.table_name,
            filters={
                "id": update_id
            }
        )

    def find_all(self):
        """
        Retrieve all client updates.
        """

        return self.provider.execute(
            operation="select",
            table=self.table_name
        )

    # -------------------------------------------------
    # Business Methods
    # -------------------------------------------------

    def find_by_client_id(
        self,
        client_id
    ):
        """
        Retrieve the client record.

        Returns a single record since each client
        has only one row in the table.
        """

        response = self.provider.execute(
            operation="select",
            table=self.table_name,
            filters={
                "client_id": client_id
            }
        )

        if response:
            return response[0]

        return None

    def find_latest_update(
        self,
        client_id
    ):
        """
        Retrieve the latest update
        for a client.
        """

        return self.find_by_client_id(
            client_id
        )
    
    def save_summary(
        self,
        client_id,
        client_name,
        summary,
        satisfaction_score
    ):
        """
        Update the existing client summary.

        If the client does not exist,
        create a new record.
        """

        existing = self.find_by_client_id(
            client_id
        )

        if existing:

            return self.update(
                existing["id"],
                {
                    "summary": summary,
                    "satisfaction_score": satisfaction_score
                }
            )

        else:

            return self.save(
                {
                    "client_id": client_id,
                    "client_name": client_name,
                    "summary": summary,
                    "satisfaction_score": satisfaction_score
                }
            )

    def update_embedding_status(
        self,
        update_id,
        status=True
    ):
        """
        Mark whether embeddings have
        been generated.
        """

        return self.update(
            update_id,
            {
                "isembeddings_created": status
            }
        )

    def increment_retry_count(
        self,
        update_id,
        retry_count
    ):
        """
        Update retry count.
        """

        return self.update(
            update_id,
            {
                "retry_count": retry_count
            }
        )
    # -------------------------------------------------
    #  Utility
    # -------------------------------------------------

    def exists(
        self,
        update_id
    ):
        """
        Check whether a client update exists.
        """

        response = self.find_by_id(
            update_id
        )

        return len(response) > 0