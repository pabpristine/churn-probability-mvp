from typing import Any, Dict, List, Optional

from src.base.base_service import BaseService
from src.domain.entities.workflow_context import WorkflowContext
from src.repositories.kpi_repository import KPIRepository


# Service responsible for fetching KPI data,
# creating a new KPI record when missing,
# normalizing records, and storing the final KPI dataset
# in the workflow context.
class KPIDataService(BaseService):
    """
    Fetch KPI data for a client, normalize numeric values,
    prepare a structured KPI dataset, and update the workflow context.

    If the client does not exist in the client_kpi table,
    create a new KPI row from workflow context data first.
    """

    def __init__(self):
        # Initialize the base service with service name and type metadata.
        super().__init__(
            service_name="KPI Data Service",
            service_type="KPI_DATA"
        )

        # Repository used for all client_kpi table operations.
        self.kpi_repository = KPIRepository()

    def validate(self, context: WorkflowContext):
        # Ensure that client_id is present before processing.
        if not context.client_id:
            raise ValueError("client_id is required in workflow context")
        return True

    def process(self, context: WorkflowContext) -> WorkflowContext:
        # First try to fetch KPI records for the given client_id.
        raw_records = self.kpi_repository.find_by_id(context.client_id) or []

        # If the client is not present in the table,
        # build a new KPI row using workflow context data
        # and store it in the database.
        if not raw_records:
            new_record = self._build_kpi_record_from_context(context)

            if new_record:
                self.kpi_repository.save(new_record)

                # Fetch again after insert so the rest of the flow
                # always works with table data.
                raw_records = self.kpi_repository.find_by_id(context.client_id) or []

        # Normalize each KPI record so numeric fields become usable Python numbers.
        normalized_records = [
            self._normalize_record(record)
            for record in raw_records
        ]

        # Select the most recent KPI record as the current KPI snapshot.
        latest_record = self._select_latest_record(normalized_records)

        # Build the final KPI dataset structure to store in the context.
        kpi_dataset = {
            "client_id": context.client_id,
            "client_name": context.client_name,
            "source_table": "client_kpi",
            "record_count": len(normalized_records),
            "records": normalized_records,
            "current_kpis": latest_record or {},
            "windows_calculated": self._infer_windows(latest_record or {})
        }

        # Store the latest KPI snapshot directly for easy downstream access.
        context.current_kpis = latest_record or {}

        # Store the full KPI dataset in the workflow context.
        context.kpi_dataset = kpi_dataset

        return context

    def _build_kpi_record_from_context(
        self,
        context: WorkflowContext
    ) -> Dict[str, Any]:
        # Use Google Sheet data as the primary source
        # for creating a missing KPI record.
        sheet = context.google_sheet_data or {}

        # Use latest client update as a secondary fallback source.
        latest_update = context.latest_client_update or {}

        # Helper function to pick the first non-empty value
        # from google_sheet_data or latest_client_update.
        def pick(*keys, default=None):
            for key in keys:
                if key in sheet and sheet.get(key) not in (None, ""):
                    return sheet.get(key)
                if key in latest_update and latest_update.get(key) not in (None, ""):
                    return latest_update.get(key)
            return default

        # Build the row according to the client_kpi table schema.
        return {
            "client_id": context.client_id,
            "client_name": context.client_name or pick("client_name"),
            "program_type": pick("program_type"),
            "program_stage": pick("program_stage"),
            "program_duration": pick("program_duration"),
            "campaign_status": pick("campaign_status"),
            "call_center_status": pick("call_center_status"),
            "ad_spend_7d": self._to_float(pick("ad_spend_7d")),
            "ad_spend_mtd": self._to_float(pick("ad_spend_mtd")),
            "ad_spend_30d": self._to_float(pick("ad_spend_30d")),
            "lead_cost_7d": self._to_float(pick("lead_cost_7d")),
            "lead_cost_mtd": self._to_float(pick("lead_cost_mtd")),
            "lead_cost_30d": self._to_float(pick("lead_cost_30d")),
            "appt_cost_7d": self._to_float(pick("appt_cost_7d")),
            "appt_cost_mtd": self._to_float(pick("appt_cost_mtd")),
            "appt_cost_30d": self._to_float(pick("appt_cost_30d")),
            "appointments_7d": self._to_float(pick("appointments_7d")),
            "appointments_mtd": self._to_float(pick("appointments_mtd")),
            "appointments_30d": self._to_float(pick("appointments_30d")),
            "isembeddings_created": False,
            "retry_count": 0
        }

    def _select_latest_record(
        self,
        records: List[Dict[str, Any]]
    ) -> Optional[Dict[str, Any]]:
        # Return None if there are no KPI records.
        if not records:
            return None

        # If only one record exists, return it directly.
        if len(records) == 1:
            return records[0]

        # Otherwise, sort by updated_at first, then created_at,
        # and return the newest record.
        return sorted(
            records,
            key=lambda x: x.get("updated_at") or x.get("created_at") or "",
            reverse=True
        )[0]

    def _normalize_record(
        self,
        record: Dict[str, Any]
    ) -> Dict[str, Any]:
        # These fields are expected to contain numeric KPI values.
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

        # Convert known numeric fields to float
        # while keeping all other values unchanged.
        for key, value in record.items():
            if key in numeric_fields:
                normalized[key] = self._to_float(value)
            else:
                normalized[key] = value

        return normalized

    def _to_float(self, value: Any):
        # Treat None and empty string as missing values.
        if value is None or value == "":
            return None

        # Try converting the value to float.
        # If conversion fails, return the original value.
        try:
            return float(value)
        except (TypeError, ValueError):
            return value

    def _infer_windows(
        self,
        record: Dict[str, Any]
    ) -> List[str]:
        # Collect which KPI time windows are present in the record.
        windows = []

        # Add 7d if at least one 7-day KPI value exists.
        if any(key.endswith("_7d") and record.get(key) is not None for key in record):
            windows.append("7d")

        # Add mtd if at least one month-to-date KPI value exists.
        if any(key.endswith("_mtd") and record.get(key) is not None for key in record):
            windows.append("mtd")

        # Add 30d if at least one 30-day KPI value exists.
        if any(key.endswith("_30d") and record.get(key) is not None for key in record):
            windows.append("30d")

        return windows