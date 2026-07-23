from src.base.base_service import BaseService
from src.domain.entities.workflow_context import WorkflowContext
from src.repositories.client_repository import ClientRepository


class FinalClientSummaryService(BaseService):
    """
    Updates the latest generated summary and
    satisfaction score in the client_updates table.
    """

    def __init__(self):

        super().__init__(
            service_name="Final Client Summary Service",
            service_type="SUMMARY"
        )

        self.client_repository = ClientRepository()

    # -------------------------------------------------
    # Validation
    # -------------------------------------------------

    def validate(
        self,
        context: WorkflowContext
    ):

        if context.previous_record is None:

            raise ValueError(
                "Previous client record not found."
            )

        if context.updated_summary is None:

            raise ValueError(
                "Updated summary is missing."
            )

        return True

    # -------------------------------------------------
    # Business Logic
    # -------------------------------------------------

    def process(
        self,
        context: WorkflowContext
    ) -> WorkflowContext:

        update_id = context.previous_record["id"]

        data = {
            "summary": context.updated_summary,
            "satisfaction_score":
                context.updated_satisfaction_score
        }

        self.client_repository.update(
            update_id,
            data
        )

        return context