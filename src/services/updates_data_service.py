from src.base.base_service import BaseService
from src.domain.entities.workflow_context import WorkflowContext
from src.repositories.client_repository import ClientRepository


class UpdatesDataService(BaseService):
    """
    Fetches all updates for a client from the
    client_updates table.
    """

    def __init__(self):

        super().__init__(
            service_name="Updates Data Service",
            service_type="DATA"
        )

        self.client_repository = ClientRepository()

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

        return True

    # -------------------------------------------------
    # Business Logic
    # -------------------------------------------------

    def process(
        self,
        context: WorkflowContext
    ) -> WorkflowContext:

        updates = self.client_repository.find_by_client_id(
            context.client_id
        )

        if not updates:

            raise Exception(
                f"No updates found for client {context.client_id}"
            )

        # Sort updates chronologically
        updates = sorted(
            updates,
            key=lambda update: update["timestamp"]
        )

        # Store all updates in WorkflowContext
        context.client_updates = updates

        # Store the latest update separately
        context.latest_client_update = updates[-1]

        return context