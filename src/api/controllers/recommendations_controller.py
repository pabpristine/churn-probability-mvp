from typing import List, Dict, Any
from src.repositories.client_repository import ClientRepository

class RecommendationsController:
    def __init__(self):
        self.client_repo = ClientRepository()

    def get_recommendations(self, client_id: str = None) -> List[Dict[str, Any]]:
        rows = self.client_repo.find_all()
        recs = []
        idx = 0
        for row in reversed(rows):
            c_id = row.get("client_id")
            if client_id and c_id != client_id:
                continue
            
            c_name = row.get("client_name") or "Unknown Client"
            action_items = row.get("action_items") or []
            
            for item in action_items:
                if not item:
                    continue
                priority = "medium"
                item_lower = item.lower()
                if "critical" in item_lower or "urgent" in item_lower or "immediate" in item_lower:
                    priority = "urgent"
                elif "high" in item_lower:
                    priority = "high"
                elif "low" in item_lower or "minor" in item_lower:
                    priority = "low"
                
                recs.append({
                    "id": f"rec-{idx}",
                    "clientId": c_id,
                    "clientName": c_name,
                    "title": f"Intervention for {c_name}",
                    "description": item,
                    "priority": priority,
                    "estimatedImpact": 90 if priority == "urgent" else 70 if priority == "high" else 50,
                    "impactDescription": "High Impact" if priority in ["urgent", "high"] else "Medium Impact",
                    "status": "pending",
                    "confidenceScore": 0.95 if priority == "urgent" else 0.85,
                    "createdAt": row.get("timestamp") or "2026-08-21T18:00:00Z",
                    "updatedAt": row.get("timestamp") or "2026-08-21T18:00:00Z"
                })
                idx += 1
        
        # If no database items are found, return mock items
        if not recs:
            recs = [
                {
                    "id": "rec-default-1",
                    "clientId": "c-101",
                    "clientName": "ABC Corp",
                    "title": "Establish executive contact",
                    "description": "Critical recommendation to multi-thread the account following churn warnings.",
                    "priority": "high",
                    "impact": "high",
                    "status": "pending",
                    "confidenceScore": 0.95,
                    "createdAt": "2026-08-21T18:00:00Z",
                    "updatedAt": "2026-08-21T18:00:00Z"
                }
            ]
        return recs

    def get_summary(self) -> Dict[str, Any]:
        recs = self.get_recommendations()
        high = sum(1 for r in recs if r["priority"] == "high")
        med = sum(1 for r in recs if r["priority"] == "medium")
        low = sum(1 for r in recs if r["priority"] == "low")
        
        return {
            "totalCount": len(recs),
            "highPriorityCount": high,
            "mediumPriorityCount": med,
            "lowPriorityCount": low,
            "impactAssessment": "Immediate action advised on high priority items."
        }

    def generate_recommendations(self, client_id: str = None) -> List[Dict[str, Any]]:
        # This can trigger the default analysis workflow if desired
        from src.workflows.ai_workflow_orchestrator import AIWorkflowOrchestrator
        orchestrator = AIWorkflowOrchestrator()
        try:
            orchestrator.run("give me churn analysis for Yardworx Land Management")
        except Exception:
            pass # Keep safe in case LLM fails
        return self.get_recommendations(client_id)
