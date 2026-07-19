import json

from src.base.base_service import BaseService
from src.domain.entities.workflow_context import WorkflowContext
from src.prompts.summary_churn_analysis_prompt import (
    build_summary_churn_analysis_prompt
)
from src.providers.llm.groq_provider import GroqProvider


class SummaryChurnAnalysisService(BaseService):
    """
    Service that generates summary/update-based churn analysis.

    Input:
    - current summary/update text
    - retrieved top similar historical summary matches

    Output:
    - context.summary_probability
    - context.summary_analysis
    - context.summary_red_flags
    - context.summary_bottlenecks
    - context.summary_historical_insights
    """

    def __init__(self):
        super().__init__(
            service_name="Summary Churn Analysis Service",
            service_type="SUMMARY_CHURN_ANALYSIS"
        )

        self.groq_provider = GroqProvider()

    def validate(
        self,
        context: WorkflowContext
    ) -> bool:
        """
        Validate required inputs before LLM analysis.
        """

        current_summary = (
            context.updated_summary
            or context.final_client_summary
            or context.summary
            or context.formatted_update_history
        )

        if not current_summary:
            raise ValueError(
                "Current summary/update text is required before summary churn analysis."
            )

        if not context.summary_matches:
            raise ValueError(
                "Summary matches are required before summary churn analysis."
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
                f"Failed to parse summary churn analysis JSON: {exc}"
            ) from exc

        # Save token usage for audit/debugging.
        context_usage = parsed_response.get("usage", {})

        return {
            "result": result,
            "usage": context_usage,
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
                f"Summary churn analysis missing keys: {missing_keys}"
            )

        probability = result["probability"]

        if not isinstance(probability, int):
            raise ValueError(
                "Summary churn probability must be an integer."
            )

        if probability < 0 or probability > 100:
            raise ValueError(
                "Summary churn probability must be between 0 and 100."
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

        prompt = build_summary_churn_analysis_prompt(context)

        llm_response = self._call_llm(prompt)
        validated_result = self._validate_llm_output(
            llm_response["result"]
        )

        context.summary_probability = validated_result["probability"]
        context.summary_analysis = validated_result["analysis"]
        context.summary_red_flags = validated_result["red_flags"]
        context.summary_bottlenecks = validated_result["bottlenecks"]
        context.summary_historical_insights = (
            validated_result["historical_insights"]
        )

        context.llm_usage["summary_prompt_tokens"] = (
            llm_response["usage"].get("prompt_tokens", 0)
        )
        context.llm_usage["summary_completion_tokens"] = (
            llm_response["usage"].get("completion_tokens", 0)
        )
        context.llm_usage["summary_total_tokens"] = (
            llm_response["usage"].get("total_tokens", 0)
        )

        context.metadata["summary_analysis_model"] = (
            llm_response["model"]
        )
        context.metadata["summary_analysis_completed"] = True

        return context