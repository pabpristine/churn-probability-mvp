from src.services.summary_service import SummaryService
from src.domain.entities.workflow_context import WorkflowContext

context = WorkflowContext(
    client_id="967783"
)

service = SummaryService()

result = service.execute(context)

print(result.summary)

print(result.satisfaction_score)