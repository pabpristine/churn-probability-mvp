import json

from src.base.base_service import BaseService
from src.domain.entities.workflow_context import WorkflowContext
from src.prompts.kpi_churn_analysis_prompt import (
    build_kpi_churn_analysis_prompt
)
from src.providers.llm.groq_provider import GroqProvider


class KPIChurnAnalysisService(BaseService):
    """
    Service that generates KPI-based churn analysis.

    Input:
    - current KPI snapshot
    - KPI interpretation
    - retrieved top similar historical KPI matches

    Output:
    - context.kpi_probability
    - context.kpi_analysis
    - context.kpi_red_flags
    - context.kpi_bottlenecks
    - context.kpi_historical_insights
    """

    def __init__(self):
        super().__init__(
            service_name="KPI Churn Analysis Service",
            service_type="KPI_CHURN_ANALYSIS"
        )

        self.groq_provider = GroqProvider()

    def validate(
        self,
        context: WorkflowContext
    ) -> bool:
        """
        Validate required inputs before LLM analysis.
        """

        if not context.current_kpis:
            raise ValueError(
                "Current KPIs are required before KPI churn analysis."
            )

        if not context.kpi_interpretation:
            raise ValueError(
                "KPI interpretation is required before KPI churn analysis."
            )

        if not context.kpi_matches:
            raise ValueError(
                "KPI matches are required before KPI churn analysis."
            )

        return True

    def _call_llm(
        self,
        prompt: str
    ) -> dict:
        """
        Call Groq in JSON mode and parse the returned JSON safely.
        """

        raw_response = self.groq_provider.generate_response(
            prompt=prompt,
            system_prompt=(
                "You are a churn-risk analysis assistant. "
                "Return only valid JSON."
            ),
            temperature=0.2,
            max_tokens=1200,
            response_format={"type": "json_object"}
        )

        parsed_response = self.groq_provider.parse_response(
            raw_response
        )

        content = parsed_response["content"]

        try:
            result = json.loads(content)
        except Exception as exc:
            raise ValueError(
                f"Failed to parse KPI churn analysis JSON: {exc}"
            ) from exc

        return {
            "result": result,
            "usage": parsed_response.get("usage", {}),
            "model": parsed_response.get("model")
        }

    def _validate_llm_output(
        self,
        result: dict
    ) -> dict:
        """
        Validate the structure of the LLM output.
        """

        required_keys = {
            "probability",
            "analysis",
            "red_flags",
            "bottlenecks",
            "historical_insights"
        }

        missing_keys = required_keys - set(result.keys())

        if missing_keys:
            raise ValueError(
                f"KPI churn analysis missing keys: {missing_keys}"
            )

        probability = result["probability"]

        if not isinstance(probability, int):
            raise ValueError(
                "KPI churn probability must be an integer."
            )

        if probability < 0 or probability > 100:
            raise ValueError(
                "KPI churn probability must be between 0 and 100."
            )

        return {
            "probability": probability,
            "analysis": str(result["analysis"]).strip(),
            "red_flags": result["red_flags"] or [],
            "bottlenecks": result["bottlenecks"] or [],
            "historical_insights": result["historical_insights"] or []
        }

    def process(
        self,
        context: WorkflowContext
    ) -> WorkflowContext:
        """
        Build prompt, call LLM, validate JSON, and write analysis to context.
        """

        self.validate(context)

        prompt = build_kpi_churn_analysis_prompt(context)

        llm_response = self._call_llm(prompt)
        validated_result = self._validate_llm_output(
            llm_response["result"]
        )

        context.kpi_probability = validated_result["probability"]
        context.kpi_analysis = validated_result["analysis"]
        context.kpi_red_flags = validated_result["red_flags"]
        context.kpi_bottlenecks = validated_result["bottlenecks"]
        context.kpi_historical_insights = (
            validated_result["historical_insights"]
        )

        context.llm_usage["kpi_prompt_tokens"] = (
            llm_response["usage"].get("prompt_tokens", 0)
        )
        context.llm_usage["kpi_completion_tokens"] = (
            llm_response["usage"].get("completion_tokens", 0)
        )
        context.llm_usage["kpi_total_tokens"] = (
            llm_response["usage"].get("total_tokens", 0)
        )

        context.metadata["kpi_analysis_model"] = (
            llm_response["model"]
        )
        context.metadata["kpi_analysis_completed"] = True

        return context