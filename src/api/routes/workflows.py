from fastapi import APIRouter, Body
from typing import List, Dict, Any
from src.api.controllers.workflows_controller import WorkflowsController

router = APIRouter(
    prefix="/api/v1/workflows",
    tags=["Workflow Monitor"]
)

controller = WorkflowsController()

@router.get("", response_model=List[Dict[str, Any]])
def get_workflows():
    return controller.get_workflows()

@router.get("/stats", response_model=Dict[str, Any])
def get_stats():
    return controller.get_stats()

@router.get("/executions", response_model=List[Dict[str, Any]])
def get_executions():
    return controller.get_executions()

@router.get("/executions/{exec_id}/logs", response_model=List[Dict[str, Any]])
def get_execution_logs(exec_id: str):
    return controller.get_execution_logs(exec_id)

@router.post("/{workflow_id}/execute", response_model=Dict[str, Any])
def execute_workflow(workflow_id: str, data: Dict[str, Any] = Body(default={})):
    return controller.execute_workflow(workflow_id, data)
