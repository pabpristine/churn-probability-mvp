from src.base.base_service import BaseService
from src.domain.entities.workflow_context import WorkflowContext
from src.repositories.client_repository import ClientRepository


class UpdatesDataNode(BaseService):
    """
    Retrieves the previously stored summary
    for a client from Supabase.

    If no record exists, the client is
    considered a new client.
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

        if context is None:
            raise ValueError(
                "WorkflowContext cannot be None."
            )

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

        record = self.client_repository.find_by_client_id(
            context.client_id
        )

        # ---------------------------------------------
        # New Client
        # ---------------------------------------------

        if record is None:

            context.is_new_client = True
            context.previous_summary = None
            context.previous_summary_timestamp = None
            context.previous_satisfaction_score = None

            return context

        # ---------------------------------------------
        # Existing Client
        # ---------------------------------------------

        context.is_new_client = False

        context.previous_summary = record.get(
            "summary"
        )

        context.previous_summary_timestamp = record.get(
            "timestamp"
        )

        context.previous_satisfaction_score = record.get(
            "satisfaction_score"
        )

        context.previous_record = record

        return context