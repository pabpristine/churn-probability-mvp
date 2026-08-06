from typing import Any, Dict, List, Optional

from src.base.base_service import BaseService
from src.domain.entities.workflow_context import WorkflowContext
from src.repositories.kpi_repository import KPIRepository


class KPIDataNode(BaseService):
    """
    Fetch KPI data for a client, normalize numeric values,
    prepare a structured KPI dataset, and update the workflow context.

    If the client does not exist in the client_kpi table,
    create a new KPI row from workflow context data first.
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
        print("KPIDataNode: client_id =", context.client_id, "client_name =", context.client_name)

        # Try to fetch existing KPI records
        raw_records = self.kpi_repository.find_by_id(context.client_id) or []
        print("KPIDataNode: initial raw_records len =", len(raw_records))

        # If none, build from context and insert once
        if not raw_records:
            new_record = self._build_kpi_record_from_context(context)
            print("KPIDataNode: new_record to insert =", new_record)

            if new_record:
                result = self.kpi_repository.save(new_record)
                print("KPIDataNode: save result =", result)

                raw_records = self.kpi_repository.find_by_id(context.client_id) or []
                print("KPIDataNode: raw_records after insert len =", len(raw_records))

        # Normalize each KPI record
        normalized_records = [
            self._normalize_record(record)
            for record in raw_records
        ]

        # Select the latest KPI snapshot
        latest_record = self._select_latest_record(normalized_records)

        # Build dataset
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

    def _build_kpi_record_from_context(
        self,
        context: WorkflowContext
    ) -> Dict[str, Any]:
        sheet = context.google_sheet_data or {}
        latest_update = context.latest_client_update or {}

        print("KPIDataNode: google_sheet_data keys =", list(sheet.keys()))
        print("KPIDataNode: latest_client_update keys =", list(latest_update.keys()))

        def pick(*keys, default=None):
            # direct lookup
            for key in keys:
                if key in sheet and sheet.get(key) not in (None, ""):
                    return sheet.get(key)
                if key in latest_update and latest_update.get(key) not in (None, ""):
                    return latest_update.get(key)

            # case-insensitive fallback
            lower_sheet = {k.lower(): v for k, v in sheet.items()}
            lower_update = {k.lower(): v for k, v in latest_update.items()}

            for key in keys:
                lk = key.lower()
                if lk in lower_sheet and lower_sheet[lk] not in (None, ""):
                    return lower_sheet[lk]
                if lk in lower_update and lower_update[lk] not in (None, ""):
                    return lower_update[lk]

            return default

        return {
            "client_id": context.client_id or pick("client_id", "clientId"),
            "client_name": context.client_name or pick("client_name", "clientName"),

            "program_type": pick("program_type", "programType"),
            "program_stage": pick("program_stage", "programStage"),
            "program_duration": pick("program_duration", "programDuration"),
            "campaign_status": pick("campaign_status", "campaignStatus"),
            "call_center_status": pick("call_center_status", "callCenterStatus"),

            "ad_spend_7d": self._to_float(pick("ad_spend_7d", "adSpend7D")),
            "ad_spend_mtd": self._to_float(pick("ad_spend_mtd", "adSpendMTD")),
            "ad_spend_30d": self._to_float(pick("ad_spend_30d", "adSpend30D")),

            "lead_cost_7d": self._to_float(pick("lead_cost_7d", "leadCost7D")),
            "lead_cost_mtd": self._to_float(pick("lead_cost_mtd", "leadCostMTD")),
            "lead_cost_30d": self._to_float(pick("lead_cost_30d", "leadCost30D")),

            "appt_cost_7d": self._to_float(pick("appt_cost_7d", "apptCost7D")),
            "appt_cost_mtd": self._to_float(pick("appt_cost_mtd", "apptCostMTD")),
            "appt_cost_30d": self._to_float(pick("appt_cost_30d", "apptCost30D")),

            # appointments_* are not present in sheet yet; they will be None for now
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