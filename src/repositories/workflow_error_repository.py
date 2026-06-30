from src.base.base_repository import BaseRepository


class WorkflowErrorRepository(BaseRepository):
    """
    Repository responsible for storing
    workflow execution errors.

    Used for debugging and monitoring.
    """

    def __init__(self):

        super().__init__(
            repository_name="Workflow Error Repository",
            table_name="workflow_error_logs"
        )

    # -------------------------------------------------
    # Logging
    # -------------------------------------------------

    def log_error(
        self,
        data
    ):
        """
        Store a workflow error.
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
        Retrieve all workflow errors.
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
        Retrieve errors for a
        workflow execution.
        """

        return self.provider.execute(
            operation="select",
            table=self.table_name,
            filters={
                "execution_id": execution_id
            }
        )