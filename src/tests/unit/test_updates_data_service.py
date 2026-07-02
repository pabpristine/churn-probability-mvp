from src.domain.entities.workflow_context import WorkflowContext
from src.services.updates_data_service import UpdatesDataService


context = WorkflowContext()

context.client_id = "182135"

service = UpdatesDataService()

result = service.execute(context)

print("\n========== LATEST CLIENT UPDATE ==========\n")

print(result.latest_client_update)