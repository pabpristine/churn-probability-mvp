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
        tb_str = "".join(
            traceback.format_exception(type(exc), exc, exc.__traceback__)
        )

        data = {
            "created_at": datetime.utcnow().isoformat(),
            "workflow_name": workflow_name,
            "workflow_id": workflow_id,
            "execution_id": execution_id,
            "execution_url": execution_url,
            "retry_of": retry_of,
            "mode": mode,
            "node_name": node_name,
            "error_name": type(exc).__name__,
            "error_message": str(exc),
            "error_stack": tb_str,
            "severity": severity,
            "client_id": client_id,
            "client_name": client_name,
            "run_id": run_id,
            "parent_run_id": parent_run_id,
            "root_run_id": root_run_id,
            "source_workflow_type": source_workflow_type,
            "environment": environment,
            "error_payload": error_payload or {},
            "execution_payload": execution_payload or {},
            "workflow_payload": workflow_payload or {},
            "trigger_payload": trigger_payload or {},
            "extra_payload": extra_payload or {},
        }

        self.repo.log_error(data)