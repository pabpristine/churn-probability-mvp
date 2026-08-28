from typing import List, Dict, Any
from fastapi import HTTPException
from src.repositories.client_repository import ClientRepository
from src.repositories.kpi_repository import KPIRepository

class ClientsController:
    def __init__(self):
        self.client_repo = ClientRepository()
        self.kpi_repo = KPIRepository()

    def _map_client(self, row: Dict[str, Any]) -> Dict[str, Any]:
        """
        Maps a DB row from client_updates into a frontend-compatible Client object.
        """
        c_id = row.get("client_id") or str(row.get("id"))
        name = row.get("client_name") or "Unknown Client"
        
        # Calculate Churn & Health
        churn_prob = row.get("churn_probability")
        if churn_prob is None:
            # Fallback if None (try matching by satisfaction)
            sat = row.get("satisfaction_score") or 80
            churn_prob = max(0, min(100, 100 - sat))
        
        health = 100 - churn_prob
        
        # Map Risk Level
        if churn_prob > 75:
            risk = "critical"
            status = "churned"
        elif churn_prob > 45:
            risk = "high"
            status = "at-risk"
        elif churn_prob > 25:
            risk = "medium"
            status = "at-risk"
        elif churn_prob > 10:
            risk = "low"
            status = "active"
        else:
            risk = "healthy"
            status = "active"

        # Dynamically map industry based on keywords in client name
        name_lower = name.lower()
        if "lawn" in name_lower or "land" in name_lower or "tree" in name_lower:
            industry = "Landscaping"
        elif "roof" in name_lower or "construct" in name_lower or "build" in name_lower or "contract" in name_lower:
            industry = "Construction"
        elif "tech" in name_lower or "cloud" in name_lower or "soft" in name_lower:
            industry = "SaaS"
        else:
            industry = "Professional Services"

        # Dynamically map financial tier
        mrr = 12000 if churn_prob < 30 else 6000
        arr = mrr * 12

        # Timestamp formatting
        ts = row.get("timestamp") or "2024-08-01T00:00:00Z"

        return {
            "id": c_id,
            "name": name,
            "industry": industry,
            "tier": "enterprise" if mrr > 10000 else "growth",
            "status": status,
            "riskLevel": risk,
            "churnProbability": int(churn_prob),
            "healthScore": int(health),
            "mrr": mrr,
            "arr": arr,
            "contractValue": arr,
            "contractStartDate": "2024-01-01",
            "contractEndDate": "2025-01-01",
            "lastActivityDate": ts,
            "createdAt": ts,
            "updatedAt": ts,
            "tags": row.get("flags") or ["Active Campaign"],
            "accountManager": "Sarah Jenkins",
            "campaign": "Q3 Retention Drive",
            "program": "Enterprise Success Plan",
            "contact": {
                "name": "Primary Lead",
                "email": f"contact@{name_lower.replace(' ', '')}.com",
                "role": "Operations Manager",
                "isPrimary": True
            },
            "address": {
                "city": "Dallas",
                "state": "Texas",
                "country": "USA"
            },
            "metadata": {
                "summary": row.get("summary"),
                "satisfaction_score": row.get("satisfaction_score"),
                "bottlenecks": row.get("bottlenecks"),
                "action_items": row.get("action_items")
            }
        }

    def get_all_clients(self) -> List[Dict[str, Any]]:
        rows = self.client_repo.find_all()
        # Filter duplicates by client_id, keeping the latest one
        seen = set()
        unique_clients = []
        for row in reversed(rows): # Read in reverse to get newest first
            c_id = row.get("client_id")
            if c_id not in seen:
                seen.add(c_id)
                unique_clients.append(self._map_client(row))
        return unique_clients

    def get_client(self, client_id: str) -> Dict[str, Any]:
        row = self.client_repo.find_by_client_id(client_id)
        if not row:
            # Fallback check by id
            rows = self.client_repo.find_all()
            for r in rows:
                if str(r.get("id")) == client_id:
                    row = r
                    break
        if not row:
            raise HTTPException(status_code=404, detail="Client not found")
        return self._map_client(row)

    def get_client_kpis(self, client_id: str) -> List[Dict[str, Any]]:
        row = self.kpi_repo.find_by_id(client_id)
        if not row:
            # Default mock KPIs if none exist yet for this client ID
            return [
                {"id": "k1", "clientId": client_id, "name": "Lead Flow Cost", "category": "Lead Quality", "value": 75, "unit": "%", "status": "improving"},
                {"id": "k2", "clientId": client_id, "name": "Appointment Volume", "category": "Conversions", "value": 80, "unit": "units", "status": "stable"},
                {"id": "k3", "clientId": client_id, "name": "Ad Placement Score", "category": "Reach", "value": 65, "unit": "/100", "status": "stable"}
            ]
        
        # Mapped from DB fields (adSpend7D, apptCostMTD, etc.)
        return [
            {"id": "k1", "clientId": client_id, "name": "Lead Cost (7D)", "category": "billing", "value": int(row.get("leadCost7D") or 50), "unit": "$", "status": "stable"},
            {"id": "k2", "clientId": client_id, "name": "Lead Cost (MTD)", "category": "billing", "value": int(row.get("leadCostMTD") or 50), "unit": "$", "status": "stable"},
            {"id": "k3", "clientId": client_id, "name": "Appointment Cost (7D)", "category": "billing", "value": int(row.get("apptCost7D") or 150), "unit": "$", "status": "improving"},
            {"id": "k4", "clientId": client_id, "name": "Appointment Cost (MTD)", "category": "billing", "value": int(row.get("apptCostMTD") or 150), "unit": "$", "status": "improving"}
        ]
