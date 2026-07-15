import json

from src.base.base_service import BaseService
from src.domain.entities.workflow_context import WorkflowContext

from src.prompts.recommendation_generation_prompt import (
    RECOMMENDATION_SYSTEM_PROMPT,
    RECOMMENDATION_USER_PROMPT
)

from src.providers.llm.groq_provider import (
    GroqProvider
)


class RecommendationGenerationService(BaseService):

    def __init__(self):

        super().__init__(

            service_name="Recommendation Generation Service",

            service_type="LLM"

        )

        self.groq_provider = GroqProvider()

    # -------------------------------------------------
    # Validation
    # -------------------------------------------------

    def validate(
        self,
        context: WorkflowContext
    ):

        if context.final_probability is None:

            raise ValueError(
                "Final churn probability is required."
            )

        if context.risk_level is None:

            raise ValueError(
                "Risk level is required."
            )

        if not context.final_analysis:

            raise ValueError(
                "Final analysis is required."
            )

        return True

    # -------------------------------------------------
    # Prompt Builder
    # -------------------------------------------------

    def build_prompt(
        self,
        context: WorkflowContext
    ):

        kpis = "\n".join(

            f"{key}: {value}"

            for key, value in context.current_kpis.items()

        )

        red_flags = "\n".join(

            f"- {item}"

            for item in context.final_red_flags

        )

        bottlenecks = "\n".join(

            f"- {item}"

            for item in context.final_bottlenecks

        )

        historical_insights = "\n".join(

            f"- {item}"

            for item in context.final_historical_insights

        )

        return RECOMMENDATION_USER_PROMPT.format(

            client_name=context.client_name,

            program_stage=context.program_stage,

            campaign_status=context.campaign_status,

            kpis=kpis,

            final_probability=context.final_probability,

            risk_level=context.risk_level,

            analysis=context.final_analysis,

            red_flags=red_flags,

            bottlenecks=bottlenecks,

            historical_insights=historical_insights

        )

    # -------------------------------------------------
    # LLM
    # -------------------------------------------------

    def call_llm(
        self,
        prompt
    ):

        return self.groq_provider.generate_response(

            prompt=prompt,

            system_prompt=RECOMMENDATION_SYSTEM_PROMPT,

            temperature=0.2,

            max_tokens=800

        )

    # -------------------------------------------------
    # Business Logic
    # -------------------------------------------------

    def process(
        self,
        context: WorkflowContext
    ) -> WorkflowContext:

        # Build prompt
        prompt = self.build_prompt(
            context
        )

        # Call LLM
        response = self.call_llm(
            prompt
        )

        # Store token usage
        context.llm_usage = response["usage"]

        # Get generated content
        content = response["content"].strip()

        # Parse JSON response
        try:

            result = json.loads(
                content
            )

        except json.JSONDecodeError:

            raise ValueError(
                "LLM returned invalid JSON."
            )

        # Validate recommendations
        recommendations = result.get(
            "recommendations"
        )

        if not isinstance(
            recommendations,
            list
        ):

            raise ValueError(
                "Recommendations field missing."
            )

        # Update workflow context
        context.recommendations = recommendations

        return context