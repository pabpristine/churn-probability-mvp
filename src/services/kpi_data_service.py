from typing import Any, Dict, List, Optional


from src.base.base_service import BaseService
from src.domain.entities.workflow_context import WorkflowContext
from src.repositories.kpi_repository import KPIRepository


# Service responsible for fetching KPI data,
# normalizing it, and storing it in the workflow context.
class KPIDataService(BaseService):
    """
    Fetch KPI data for a client, normalize numeric values,
    prepare a structured KPI dataset, and update the workflow context.
    """

    def __init__(self):
        # Initialize the base service with service metadata.
        super().__init__(
            service_name="KPI Data Service",
            service_type="KPI_DATA"
        )

        # Repository used to fetch KPI records from the data source.
        self.kpi_repository = KPIRepository()

    def validate(self, context: WorkflowContext):
        # Ensure a client_id exists before processing.
        if not context.client_id:
            raise ValueError("client_id is required in workflow context")
        return True

    def process(self, context: WorkflowContext) -> WorkflowContext:
        # Fetch all KPI records for the given client_id.
        raw_records = self.kpi_repository.find_by_id(context.client_id) or []

        # Normalize each record so numeric values are converted properly.
        normalized_records = [
            self._normalize_record(record)
            for record in raw_records
        ]

        # Select the most recent KPI record as the current snapshot.
        latest_record = self._select_latest_record(normalized_records)

        # Build the final KPI dataset to store in the workflow context.
        kpi_dataset = {
            "client_id": context.client_id,
            "client_name": context.client_name,
            "source_table": "client_kpi",
            "record_count": len(normalized_records),
            "records": normalized_records,
            "current_kpis": latest_record or {},
            "windows_calculated": self._infer_windows(latest_record or {})
        }

        # Store the latest KPI record separately for easy access.
        context.current_kpis = latest_record or {}

        # Store the full KPI dataset in the workflow context.
        context.kpi_dataset = kpi_dataset

        return context

    def _select_latest_record(
        self,
        records: List[Dict[str, Any]]
    ) -> Optional[Dict[str, Any]]:
        # Return None if there are no records.
        if not records:
            return None

        # If there is only one record, use it directly.
        if len(records) == 1:
            return records[0]

        # Sort records by updated_at first, then created_at, and pick the newest.
        return sorted(
            records,
            key=lambda x: x.get("updated_at") or x.get("created_at") or "",
            reverse=True
        )[0]

    def _normalize_record(
        self,
        record: Dict[str, Any]
    ) -> Dict[str, Any]:
        # Fields that should be treated as numeric values.
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

        # Store normalized values here.
        normalized = {}

        # Convert numeric fields to floats while keeping other values as-is.
        for key, value in record.items():
            if key in numeric_fields:
                normalized[key] = self._to_float(value)
            else:
                normalized[key] = value

        return normalized

    def _to_float(self, value: Any):
        # Treat empty values as missing data.
        if value is None or value == "":
            return None

        # Convert numeric-like values to float.
        try:
            return float(value)
        except (TypeError, ValueError):
            return value

    def _infer_windows(
        self,
        record: Dict[str, Any]
    ) -> List[str]:
        # Collect the time windows present in the KPI record.
        windows = []

        # Add 7d if at least one 7-day metric exists.
        if any(key.endswith("_7d") and record.get(key) is not None for key in record):
            windows.append("7d")

        # Add mtd if at least one month-to-date metric exists.
        if any(key.endswith("_mtd") and record.get(key) is not None for key in record):
            windows.append("mtd")

        # Add 30d if at least one 30-day metric exists.
        if any(key.endswith("_30d") and record.get(key) is not None for key in record):
            windows.append("30d")

        return windows