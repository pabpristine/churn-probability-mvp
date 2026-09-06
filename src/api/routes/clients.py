from fastapi import APIRouter, Depends
from typing import List, Dict, Any
from src.api.controllers.clients_controller import ClientsController

router = APIRouter(
    prefix="/api/v1/clients",
    tags=["Clients Management"]
)

controller = ClientsController()

@router.get("", response_model=List[Dict[str, Any]])
def list_clients():
    return controller.get_all_clients()

@router.get("/{client_id}", response_model=Dict[str, Any])
def get_client(client_id: str):
    return controller.get_client(client_id)

@router.get("/{client_id}/kpis", response_model=List[Dict[str, Any]])
def get_client_kpis(client_id: str):
    return controller.get_client_kpis(client_id)

@router.get("/{client_id}/analysis", response_model=Dict[str, Any])
def get_client_analysis(client_id: str):
    client = controller.get_client(client_id)
    # Return formatted risk details based on AI summary and scores
    return {
        "status": "success",
        "data": {
            "clientId": client_id,
            "churnProbability": client["churnProbability"],
            "healthScore": client["healthScore"],
            "summary": client["metadata"]["summary"],
            "satisfactionScore": client["metadata"]["satisfaction_score"],
            "redFlags": client["tags"],
            "bottlenecks": client["metadata"]["bottlenecks"] or [],
            "actionItems": client["metadata"]["action_items"] or []
        }
    }

@router.get("/{client_id}/history", response_model=List[Dict[str, Any]])
def get_client_history(client_id: str):
    # Returns historical similarity matches from Supabase if available
    try:
        from src.repositories.summary_embedding_repository import SummaryEmbeddingRepository
        from src.repositories.client_repository import ClientRepository

        client_repo = ClientRepository()
        client_row = client_repo.find_by_client_id(client_id)
        if not client_row:
            return []

        # Return any stored similar historical clients from the client record
        historical = client_row.get("historical_matches") or []
        if historical:
            return historical

        # No historical similarity found yet (workflow not run for this client)
        return []
    except Exception:
        return []
