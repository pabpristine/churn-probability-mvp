from typing import Any, Dict, List, Optional

from src.base.base_service import BaseService
from src.domain.entities.workflow_context import WorkflowContext
from src.providers.embeddings.huggingface_provider import HuggingFaceProvider
from src.repositories.kpi_embedding_repository import KPIEmbeddingRepository


# Service responsible for reading KPI interpretation data,
# converting it into embedding-ready content, generating
# the embedding vector, storing it in the repository,
# and updating the workflow context.
class KPIEmbeddingService(BaseService):
    """
    Generate and persist KPI embeddings from the KPI interpretation
    already produced in the workflow.
    """

    def __init__(self):
        # Initialize base service metadata.
        super().__init__(
            service_name="KPI Embedding Service",
            service_type="KPI_EMBEDDING"
        )

        # Provider used to generate embedding vectors.
        self.embedding_provider = HuggingFaceProvider()

        # Repository used to store KPI embeddings.
        self.kpi_embedding_repository = KPIEmbeddingRepository()

    def validate(self, context: WorkflowContext):
        # Ensure a client_id exists before processing.
        if not context.client_id:
            raise ValueError("client_id is required in workflow context")

        # Ensure KPI interpretation exists before generating embedding.
        if not context.kpi_interpretation:
            raise ValueError("kpi_interpretation is required in workflow context")

        return True

    def process(self, context: WorkflowContext) -> WorkflowContext:
        # Read KPI interpretation and current KPI snapshot from context.
        interpretation = context.kpi_interpretation or {}
        current_kpis = context.current_kpis or {}
        if not current_kpis and context.kpi_dataset:
            current_kpis = context.kpi_dataset.get("current_kpis", {})

        # Build embedding-friendly text content from KPI data.
        content = self._build_embedding_content(
            client_name=context.client_name,
            current_kpis=current_kpis,
            interpretation=interpretation
        )

        # Generate the embedding vector from the formatted content.
        embedding_vector = self._generate_embedding(content)

        # Prepare metadata for storage and later retrieval/filtering.
        metadata = {
            "client_id": context.client_id,
            "source": "kpi_interpretation",
            "matched_pattern_names": interpretation.get("matched_pattern_names", []),
            "overall_severity": interpretation.get("overall_severity"),
        }

        # Build the final payload expected by the vector table.
        payload = {
            "content": content,
            "embedding": embedding_vector,
            "metadata": metadata
        }

        # Store the embedding row in the repository.
        self.kpi_embedding_repository.insert(payload)

        # Update the workflow context for downstream workflows.
        context.kpi_embedding = embedding_vector
        context.kpi_embedding_content = content
        context.metadata["kpi_embedding_metadata"] = metadata

        return context

    def _build_embedding_content(
        self,
        client_name: Optional[str],
        current_kpis: Dict[str, Any],
        interpretation: Dict[str, Any]
    ) -> str:
        # Extract fields from the current KPI snapshot.
        program_type = current_kpis.get("program_type")
        program_stage = current_kpis.get("program_stage")
        campaign_status = current_kpis.get("campaign_status")
        call_center_status = current_kpis.get("call_center_status")

        ad_spend_7d = self._format_number(current_kpis.get("ad_spend_7d"))
        ad_spend_mtd = self._format_number(current_kpis.get("ad_spend_mtd"))
        ad_spend_30d = self._format_number(current_kpis.get("ad_spend_30d"))

        lead_cost_7d = self._format_number(current_kpis.get("lead_cost_7d"))
        lead_cost_mtd = self._format_number(current_kpis.get("lead_cost_mtd"))
        lead_cost_30d = self._format_number(current_kpis.get("lead_cost_30d"))

        appt_cost_7d = self._format_number(current_kpis.get("appt_cost_7d"))
        appt_cost_mtd = self._format_number(current_kpis.get("appt_cost_mtd"))
        appt_cost_30d = self._format_number(current_kpis.get("appt_cost_30d"))

        # Extract fields from KPI interpretation.
        matched_pattern_names = interpretation.get("matched_pattern_names", [])
        matched_patterns = interpretation.get("matched_patterns", [])
        llm_summary = interpretation.get("llm_summary")
        overall_severity = interpretation.get("overall_severity")

        # Collect interpretation text from matched patterns if present.
        interpretation_lines = []
        for pattern in matched_patterns:
            pattern_text = pattern.get("interpretation")
            if pattern_text:
                interpretation_lines.append(pattern_text)

        # Remove duplicates while preserving order.
        interpretation_lines = list(dict.fromkeys(interpretation_lines))

        # Build a text block similar to your current Supabase rows.
        content_parts = [
            f"Client: {client_name or 'Unknown Client'}",
            f"Program Type: {program_type or 'unknown'}",
            f"Program Stage: {program_stage or 'unknown'}",
            f"Campaign Status: {campaign_status or 'unknown'}",
            f"Call Center Status: {call_center_status or 'unknown'}",
            "",
            f"Ad Spend (30D): {ad_spend_30d}",
            f"Lead Cost (30D): {lead_cost_30d}",
            f"Appointment Cost (30D): {appt_cost_30d}",
            "",
            f"Recent Ad Spend: 7D = {ad_spend_7d}, MTD = {ad_spend_mtd}",
            f"Recent Lead Cost: 7D = {lead_cost_7d}, MTD = {lead_cost_mtd}",
            f"Recent Appointment Cost: 7D = {appt_cost_7d}, MTD = {appt_cost_mtd}",
            f"Pattern key: {','.join(matched_pattern_names) if matched_pattern_names else 'NONE'}",
            f"Interpretation: {','.join(interpretation_lines) if interpretation_lines else (llm_summary or 'No interpretation available')}",
            f"Severity: {overall_severity or 'unknown'}",
            f"KPI Summary: {llm_summary or 'No KPI summary available'}"
        ]

        return "\n".join(content_parts).strip()

    def _generate_embedding(self, content: str) -> List[float]:
        # Call the embedding provider using the formatted content.
        response = self.embedding_provider.generate_embedding(content)

        # Normalize provider response so the service always returns a list.
        if isinstance(response, dict):
            if "embedding" in response:
                return response["embedding"]
            if "vector" in response:
                return response["vector"]

        if isinstance(response, list):
            return response

        raise ValueError("Invalid embedding response returned by HuggingFaceProvider")

    def _format_number(self, value: Any) -> str:
        # Format numeric KPI values consistently for embedding text.
        if value is None or value == "":
            return "$0"

        try:
            return f"${float(value):.2f}"
        except (TypeError, ValueError):
            return str(value)