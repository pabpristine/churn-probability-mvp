from typing import List, Dict, Any
from src.api.controllers.clients_controller import ClientsController

class DashboardController:
    def __init__(self):
        self.clients_controller = ClientsController()

    def get_metrics(self) -> Dict[str, Any]:
        clients = self.clients_controller.get_all_clients()
        total = len(clients)
        active = sum(1 for c in clients if c["status"] == "active")
        at_risk = sum(1 for c in clients if c["status"] == "at-risk")
        churned = sum(1 for c in clients if c["status"] == "churned")
        
        avg_health = sum(c["healthScore"] for c in clients) / total if total > 0 else 80
        avg_churn = sum(c["churnProbability"] for c in clients) / total if total > 0 else 20
        total_mrr = sum(c["mrr"] for c in clients)
        total_arr = sum(c["arr"] for c in clients)

        return {
            "totalClients": total,
            "activeClients": active,
            "atRiskClients": at_risk,
            "churnedClients": churned,
            "avgHealthScore": int(avg_health),
            "avgChurnProbability": int(avg_churn),
            "totalMRR": total_mrr,
            "totalARR": total_arr,
            "mrrGrowth": 8.4,
            "healthGrowth": 3.1,
            "riskGrowth": -4.6,
            "activeGrowth": 2.2
        }

    def get_alerts(self) -> List[Dict[str, Any]]:
        clients = self.clients_controller.get_all_clients()
        alerts = []
        for index, c in enumerate(clients):
            if c["riskLevel"] in ["critical", "high"]:
                alerts.append({
                    "id": f"alert-{index}",
                    "clientId": c["id"],
                    "clientName": c["name"],
                    "type": "risk",
                    "severity": "high" if c["riskLevel"] == "critical" else "medium",
                    "message": f"High Churn Risk detected for {c['name']} ({c['churnProbability']}% probability)",
                    "isRead": False,
                    "createdAt": c["lastActivityDate"]
                })
        # Add a default alert if no clients are high risk
        if not alerts:
            alerts.append({
                "id": "alert-default",
                "clientId": "system",
                "clientName": "System Alert",
                "type": "info",
                "severity": "low",
                "message": "All client health metrics are currently stable.",
                "isRead": False,
                "createdAt": "2026-08-21T00:00:00Z"
            })
        return alerts

    def get_recent_activity(self) -> List[Dict[str, Any]]:
        clients = self.clients_controller.get_all_clients()
        activity = []
        for index, c in enumerate(clients[:5]):  # limit to top 5 recent
            activity.append({
                "id": f"act-{index}",
                "type": "workflow",
                "title": "Analysis Completed",
                "description": f"Workflow run completed for client {c['name']}.",
                "timestamp": c["lastActivityDate"],
                "status": "success",
                "author": "System Orchestrator"
            })
        return activity

    def get_churn_risk_chart(self) -> List[Dict[str, Any]]:
        clients = self.clients_controller.get_all_clients()
        categories = {"Critical": 0, "High": 0, "Medium": 0, "Low": 0, "Healthy": 0}
        for c in clients:
            lvl = c["riskLevel"].capitalize()
            if lvl in categories:
                categories[lvl] += 1
            else:
                categories["Healthy"] += 1
        
        return [
            {"name": k, "value": v} for k, v in categories.items()
        ]

    def get_health_distribution(self) -> List[Dict[str, Any]]:
        clients = self.clients_controller.get_all_clients()
        ranges = {"90-100": 0, "70-89": 0, "50-69": 0, "30-49": 0, "0-29": 0}
        for c in clients:
            score = c["healthScore"]
            if score >= 90:
                ranges["90-100"] += 1
            elif score >= 70:
                ranges["70-89"] += 1
            elif score >= 50:
                ranges["50-69"] += 1
            elif score >= 30:
                ranges["30-49"] += 1
            else:
                ranges["0-29"] += 1
        return [
            {"name": k, "value": v} for k, v in ranges.items()
        ]

    def get_revenue_chart(self, period: str = "12m") -> List[Dict[str, Any]]:
        # Mock time-series revenue timeline data based on total MRR
        metrics = self.get_metrics()
        base_mrr = metrics["totalMRR"] or 75000
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        chart_data = []
        for i, m in enumerate(months):
            # Simulate slight growth
            factor = 0.85 + (i * 0.015)
            chart_data.append({
                "name": m,
                "value": int(base_mrr * factor)
            })
        return chart_data
