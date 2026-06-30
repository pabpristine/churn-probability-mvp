from src.base.base_repository import BaseRepository


class LLMUsageRepository(BaseRepository):
    """
    Repository responsible for storing
    Large Language Model (LLM) usage logs.

    Used for tracking model usage,
    token consumption and execution cost.
    """

    def __init__(self):

        super().__init__(
            repository_name="LLM Usage Repository",
            table_name="llm_usage_logs"
        )

    # -------------------------------------------------
    # Logging
    # -------------------------------------------------

    def log_usage(
        self,
        data
    ):
        """
        Store an LLM usage record.
        """

        return self.provider.execute(
            operation="insert",
            table=self.table_name,
            data=data
        )

    # -------------------------------------------------
    # Read
    # -------------------------------------------------

    def find_all(self):
        """
        Retrieve all LLM usage logs.
        """

        return self.provider.execute(
            operation="select",
            table=self.table_name
        )

    def find_by_execution_id(
        self,
        execution_id
    ):
        """
        Retrieve usage logs for a
        workflow execution.
        """

        return self.provider.execute(
            operation="select",
            table=self.table_name,
            filters={
                "execution_id": execution_id
            }
        )