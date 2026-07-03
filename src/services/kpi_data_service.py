from typing import Any, Dict, List, Optional

from src.base.base_service import BaseService
from src.domain.entities.workflow_context import WorkflowContext
from src.repositories.kpi_repository import KPIRepository


class KPIDataService(BaseService):
    """
    Fetch KPI data for a client, normalize numeric values,
    prepare a structured KPI dataset, and update the workflow context.
    """

    def __init__(self):
        super().__init__(
            service_name="KPI Data Service",
            service_type="KPI_DATA"
        )
        self.kpi_repository = KPIRepository()

    def validate(self, context: WorkflowContext):
        if not context.client_id:
            raise ValueError("client_id is required in workflow context")
        return True

    def process(self, context: WorkflowContext) -> WorkflowContext:
        raw_records = self.kpi_repository.find_by_id(context.client_id) or []

        normalized_records = [
            self._normalize_record(record)
            for record in raw_records
        ]

        latest_record = self._select_latest_record(normalized_records)

        kpi_dataset = {
            "client_id": context.client_id,
            "client_name": context.client_name,
            "source_table": "client_kpi",
            "record_count": len(normalized_records),
            "records": normalized_records,
            "current_kpis": latest_record or {},
            "windows_calculated": self._infer_windows(latest_record or {})
        }

        context.current_kpis = latest_record or {}
        context.kpi_dataset = kpi_dataset

        return context

    def _select_latest_record(
        self,
        records: List[Dict[str, Any]]
    ) -> Optional[Dict[str, Any]]:
        if not records:
            return None

        if len(records) == 1:
            return records[0]

        return sorted(
            records,
            key=lambda x: x.get("updated_at") or x.get("created_at") or "",
            reverse=True
        )[0]

    def _normalize_record(
        self,
        record: Dict[str, Any]
    ) -> Dict[str, Any]:
        numeric_fields = {
            "ad_spend_7d",
            "ad_spend_mtd",
            "ad_spend_30d",
            "lead_cost_7d",
            "lead_cost_mtd",
            "lead_cost_30d",
            "appt_cost_7d",
            "appt_cost_mtd",
            "appt_cost_30d",
            "appointments_7d",
            "appointments_mtd",
            "appointments_30d",
            "retry_count",
        }

        normalized = {}

        for key, value in record.items():
            if key in numeric_fields:
                normalized[key] = self._to_float(value)
            else:
                normalized[key] = value

        return normalized

    def _to_float(self, value: Any):
        if value is None or value == "":
            return None

        try:
            return float(value)
        except (TypeError, ValueError):
            return value

    def _infer_windows(
        self,
        record: Dict[str, Any]
    ) -> List[str]:
        windows = []

        if any(key.endswith("_7d") and record.get(key) is not None for key in record):
            windows.append("7d")

        if any(key.endswith("_mtd") and record.get(key) is not None for key in record):
            windows.append("mtd")

        if any(key.endswith("_30d") and record.get(key) is not None for key in record):
            windows.append("30d")

        return windows