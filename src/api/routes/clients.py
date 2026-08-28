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
    # Returns vector matches. We can return historical similarity matches or default ones.
    return [
        {
            "id": "hc1",
            "name": "Vanguard Tech",
            "industry": "SaaS",
            "similarityScore": 92,
            "outcome": "churned",
            "healthAtTime": 30,
            "reasonForChurn": "Lack of perceived ROI after 12 months. Executive sponsor left.",
            "lessonsLearned": "Ensure multi-threading of executive relationships."
        },
        {
            "id": "hc2",
            "name": "DataFlow Inc",
            "industry": "SaaS",
            "similarityScore": 88,
            "outcome": "retained",
            "healthAtTime": 35,
            "lessonsLearned": "Intervened early with an on-site workshop which realigned goals."
        }
    ]
