from typing import Any, Dict, List, Optional

from src.base.base_service import BaseService
from src.domain.entities.workflow_context import WorkflowContext
from src.providers.llm.groq_provider import GroqProvider
from src.repositories.kpi_repository import KPIRepository
from src.repositories.pattern_repository import PatternRepository


class KPIAnalysisService(BaseService):
    """
    Analyze KPI trends, detect predefined patterns,
    fetch business interpretations from the repository,
    and update the workflow context with KPI interpretation.
    """

    def __init__(self):
        super().__init__(
            service_name="KPI Analysis Service",
            service_type="KPI_ANALYSIS"
        )
        self.kpi_repository = KPIRepository()
        self.pattern_repository = PatternRepository()
        self.groq_provider = GroqProvider()

    def validate(self, context: WorkflowContext):
        if not context.client_id:
            raise ValueError("client_id is required in workflow context")

        summary_text = context.final_client_summary or context.summary
        if not summary_text:
            raise ValueError("final summary is required for KPI analysis")

        return True

    def process(self, context: WorkflowContext) -> WorkflowContext:
        summary_text = context.final_client_summary or context.summary
        kpi_dataset = context.kpi_dataset or self._load_kpi_dataset(context)
        current_kpis = kpi_dataset.get("current_kpis", {})

        matched_pattern_names = self._detect_patterns(current_kpis)
        matched_patterns = self._fetch_pattern_rows(matched_pattern_names)

        if not matched_patterns:
            stable_pattern = self.pattern_repository.find_by_pattern_name(
                "Stable Performance"
            ) or []
            matched_patterns = stable_pattern[:1]
            matched_pattern_names = ["Stable Performance"]

        overall_severity = self._calculate_overall_severity(matched_patterns)

        llm_summary = self._generate_llm_summary(
            client_name=context.client_name,
            summary_text=summary_text,
            current_kpis=current_kpis,
            matched_patterns=matched_patterns
        )

        context.kpi_interpretation = {
            "client_id": context.client_id,
            "client_name": context.client_name,
            "summary_used": summary_text,
            "matched_pattern_names": matched_pattern_names,
            "matched_patterns": matched_patterns,
            "overall_severity": overall_severity,
            "llm_summary": llm_summary
        }

        return context

    def _load_kpi_dataset(
        self,
        context: WorkflowContext
    ) -> Dict[str, Any]:
        raw_records = self.kpi_repository.find_by_id(context.client_id) or []
        normalized_records = [self._normalize_record(record) for record in raw_records]
        current_kpis = normalized_records[0] if normalized_records else {}

        return {
            "client_id": context.client_id,
            "client_name": context.client_name,
            "source_table": "client_kpi",
            "record_count": len(normalized_records),
            "records": normalized_records,
            "current_kpis": current_kpis,
            "windows_calculated": []
        }

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

    def _detect_patterns(
        self,
        kpi: Dict[str, Any]
    ) -> List[str]:
        patterns = []

        def num(field: str) -> Optional[float]:
            value = kpi.get(field)
            if value is None:
                return None
            try:
                return float(value)
            except (TypeError, ValueError):
                return None

        lead_7d = num("lead_cost_7d")
        lead_mtd = num("lead_cost_mtd")
        lead_30d = num("lead_cost_30d")

        appt_7d = num("appt_cost_7d")
        appt_mtd = num("appt_cost_mtd")
        appt_30d = num("appt_cost_30d")

        ad_7d = num("ad_spend_7d")
        ad_mtd = num("ad_spend_mtd")
        ad_30d = num("ad_spend_30d")

        campaign_status = kpi.get("campaign_status")
        call_center_status = kpi.get("call_center_status")
        program_stage = kpi.get("program_stage")

        if lead_7d is None or appt_7d is None:
            patterns.append("Incomplete Tracking")
            return list(dict.fromkeys(patterns))

        if lead_30d is None and lead_7d is not None:
            patterns.append("Historical Data Gap")

        if lead_mtd is not None and lead_30d is not None:
            if lead_7d > lead_mtd and lead_mtd > lead_30d:
                patterns.append("Rising Lead Cost")

            if lead_7d < lead_mtd and lead_mtd < lead_30d:
                patterns.append("Declining Lead Cost")

            if abs(lead_7d - lead_30d) < (lead_30d * 0.1):
                patterns.append("Stable Lead Cost")

            if lead_7d > (lead_30d * 1.5):
                patterns.append("Spike in Lead Cost")

            if lead_7d > lead_mtd and lead_mtd <= lead_30d:
                patterns.append("Early Warning Trend")

            if lead_7d < lead_mtd and lead_mtd > lead_30d:
                patterns.append("Flash Recovery")

        if appt_mtd is not None and appt_30d is not None:
            if appt_7d > appt_mtd and appt_mtd > appt_30d:
                patterns.append("Rising Appointment Cost")

            if lead_7d is not None and appt_7d < (lead_7d * 2):
                patterns.append("Efficient Appointment Generation")

            if lead_7d is not None and appt_7d > (lead_7d * 5):
                patterns.append("Poor Appointment Conversion")

        if ad_30d is not None:
            if ad_7d is not None and ad_7d > (ad_30d / 4.3):
                patterns.append("Aggressive Spending")

            if ad_7d is not None and ad_7d < (ad_30d / 6):
                patterns.append("Reduced Spending")

            if ad_7d is not None and abs(ad_7d - (ad_30d / 4.3)) < (ad_30d * 0.05):
                patterns.append("Consistent Spend")

        if lead_mtd is not None and ad_mtd is not None and ad_7d is not None:
            if lead_7d < lead_mtd and ad_7d >= ad_mtd:
                patterns.append("Improving ROI Trajectory")

            if lead_7d > lead_mtd and ad_7d > ad_mtd:
                patterns.append("Deteriorating Efficiency")

            if (
                lead_30d is not None
                and appt_30d is not None
                and appt_7d is not None
                and lead_7d < lead_30d
                and appt_7d > appt_30d
            ):
                patterns.append("Cost-Quality Mismatch")

            if (
                appt_mtd is not None
                and appt_7d is not None
                and ad_7d > ad_mtd
                and lead_7d < lead_mtd
                and appt_7d < appt_mtd
            ):
                patterns.append("Healthy Growth Pattern")

            if ad_7d < ad_mtd and lead_7d > lead_mtd:
                patterns.append("Budget Constraint Impact")

        if campaign_status == "Active" and lead_30d is not None and lead_7d > (lead_30d * 1.3):
            patterns.append("Active Campaign Stall")

        if (
            campaign_status == "Paused"
            and lead_30d is not None
            and appt_30d is not None
            and lead_30d < (appt_30d / 3)
        ):
            patterns.append("Paused with Good Metrics")

        if call_center_status == "Limited Capacity" and appt_30d is not None and appt_7d < appt_30d:
            patterns.append("Call Center Bottleneck")

        if call_center_status == "Available" and appt_30d is not None and appt_7d > (appt_30d * 1.3):
            patterns.append("Call Center Underutilization")

        if program_stage == "Testing" and lead_30d is not None and lead_7d > lead_30d:
            patterns.append("Testing Phase High Cost")

        if program_stage == "Mature" and lead_mtd is not None and lead_7d > lead_mtd:
            patterns.append("Mature Program Decline")

        if (
            program_stage == "Scaling"
            and lead_mtd is not None
            and ad_mtd is not None
            and lead_7d < lead_mtd
            and ad_7d > ad_mtd
        ):
            patterns.append("Scaling Success")

        if (
            program_stage == "Launch"
            and lead_mtd is not None
            and abs(lead_7d - lead_mtd) < (lead_mtd * 0.2)
        ):
            patterns.append("Launch Stability")

        if not patterns:
            patterns.append("Stable Performance")

        return list(dict.fromkeys(patterns))

    def _fetch_pattern_rows(
        self,
        pattern_names: List[str]
    ) -> List[Dict[str, Any]]:
        rows = []

        for pattern_name in pattern_names:
            result = self.pattern_repository.find_by_pattern_name(pattern_name) or []
            if result:
                rows.append(result[0])

        return rows

    def _calculate_overall_severity(
        self,
        matched_patterns: List[Dict[str, Any]]
    ) -> str:
        severity_rank = {
            "low": 1,
            "medium": 2,
            "high": 3,
            "critical": 4
        }

        highest = "low"

        for pattern in matched_patterns:
            severity = (pattern.get("severity_level") or "low").lower()
            if severity_rank.get(severity, 1) > severity_rank.get(highest, 1):
                highest = severity

        return highest

    def _generate_llm_summary(
        self,
        client_name: Optional[str],
        summary_text: str,
        current_kpis: Dict[str, Any],
        matched_patterns: List[Dict[str, Any]]
    ) -> Optional[str]:
        try:
            prompt = f"""
Client Name: {client_name}

Final Client Summary:
{summary_text}

Current KPIs:
{current_kpis}

Matched KPI Patterns:
{matched_patterns}

Write a concise KPI interpretation in 4-6 sentences.
Focus on:
1. performance trend,
2. main risks,
3. most important business takeaway.
""".strip()

            response = self.groq_provider.generate_response(
                prompt=prompt,
                system_prompt=(
                    "You are a churn risk analysis assistant. "
                    "Summarize KPI pattern signals clearly and concisely."
                ),
                temperature=0.2,
                max_tokens=300
            )

            return response.get("content")

        except Exception:
            return None