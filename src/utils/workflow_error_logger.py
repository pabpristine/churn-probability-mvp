import traceback
from datetime import datetime
from typing import Any, Dict, Optional

from src.repositories.workflow_error_repository import WorkflowErrorRepository


class WorkflowErrorLogger:
    """
    Thin wrapper around WorkflowErrorRepository that prepares
    a payload matching the workflow_error_logs table schema.
    """

    def __init__(self):
        self.repo = WorkflowErrorRepository()

    def log(
        self,
        *,
        workflow_name: Optional[str],
        workflow_id: Optional[str] = None,
        execution_id: Optional[str] = None,
        execution_url: Optional[str] = None,
        retry_of: Optional[str] = None,
        mode: Optional[str] = None,
        node_name: Optional[str] = None,
        exc: BaseException,
        severity: str = "error",
        client_id: Optional[str] = None,
        client_name: Optional[str] = None,
        run_id: Optional[str] = None,
        parent_run_id: Optional[str] = None,
        root_run_id: Optional[str] = None,
        source_workflow_type: Optional[str] = None,
        environment: str = "production",
        error_payload: Optional[Dict[str, Any]] = None,
        execution_payload: Optional[Dict[str, Any]] = None,
        workflow_payload: Optional[Dict[str, Any]] = None,
        trigger_payload: Optional[Dict[str, Any]] = None,
        extra_payload: Optional[Dict[str, Any]] = None,
    ):
        """
        Store a workflow error using only the columns
        available in the workflow_error_logs table.

        Database columns:
            id
            workflow_name
            failed_node
            error_message
            execution_id
            workflow_id
            error_stack
            created_at
        """

        # Build complete traceback
        tb_str = "".join(
            traceback.format_exception(
                type(exc),
                exc,
                exc.__traceback__
            )
        )

        # IMPORTANT:
        # Only include columns that actually exist
        # in workflow_error_logs.
        data = {
            "workflow_name": workflow_name,
            "failed_node": node_name,
            "error_message": str(exc),
            "execution_id": execution_id,
            "workflow_id": workflow_id,
            "error_stack": tb_str,
            "created_at": datetime.utcnow().isoformat(),
        }

        return self.repo.log_error(data)