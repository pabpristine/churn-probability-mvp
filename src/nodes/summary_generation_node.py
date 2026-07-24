import json

from src.base.base_service import BaseService
from src.domain.entities.workflow_context import WorkflowContext

from src.providers.llm.groq_provider import GroqProvider

from src.prompts.summary_system_prompt import (
    SUMMARY_SYSTEM_PROMPT
)

from src.prompts.summary_user_prompt import (
    SUMMARY_USER_PROMPT
)

from src.core.logging import setup_logger


logger = setup_logger()


class SummaryGenerationNode(BaseService):
    """
    Generates an updated client summary by
    iteratively processing all summary batches.

    This service DOES NOT update the database.
    """

    def __init__(self):

        super().__init__(
            service_name="Summary Service",
            service_type="SUMMARY"
        )

        self.groq_provider = GroqProvider()

    # -------------------------------------------------
    # Validation
    # -------------------------------------------------

    def validate(
        self,
        context: WorkflowContext
    ):

        if not context.client_id:

            raise ValueError(
                "Client ID is required."
            )

        if not context.summary_batches:

            raise ValueError(
                "Summary batches are missing."
            )

        return True

    # -------------------------------------------------
    # Prompt Builder
    # -------------------------------------------------

    def build_prompt(

        self,

        context,

        previous_summary,

        batch_text

    ):

        return SUMMARY_USER_PROMPT.format(

            client_name=context.client_name,

            client_id=context.client_id,

            previous_summary=previous_summary,

            new_updates=batch_text

        )

    # -------------------------------------------------
    # Groq Call
    # -------------------------------------------------

    def call_llm(

        self,

        user_prompt

    ):

        return self.groq_provider.execute(

            system_prompt=SUMMARY_SYSTEM_PROMPT,

            prompt=user_prompt

        )

    # -------------------------------------------------
    # Parse Response
    # -------------------------------------------------

    def parse_response(

        self,

        response

    ):

        if not isinstance(response, dict):

            raise Exception(
                "Invalid provider response."
            )

        if "content" not in response:

            raise Exception(
                "LLM content missing."
            )

        llm_output = (

            response["content"]

            .replace("```json", "")

            .replace("```", "")

            .strip()

        )

        try:

            result = json.loads(
                llm_output
            )

        except Exception as error:

            raise Exception(

                f"\nUnable to parse JSON\n\n"

                f"{llm_output}\n\n"

                f"{error}"

            )

        return result

    # -------------------------------------------------
    # Validate JSON
    # -------------------------------------------------

    def validate_response(

        self,

        result

    ):

        required_keys = [

            "client_name",

            "client_id",

            "summary",

            "satisfaction_score"

        ]

        for key in required_keys:

            if key not in result:

                raise Exception(
                    f"Missing key : {key}"
                )

    # -------------------------------------------------
    # Business Logic
    # -------------------------------------------------

    def process(

        self,

        context: WorkflowContext

    ) -> WorkflowContext:

        current_summary = (

            context.previous_summary

            if context.previous_summary

            else "No previous summary available."

        )

        current_score = (

            context.previous_satisfaction_score

            if context.previous_satisfaction_score

            else 50

        )

        total_prompt_tokens = 0

        total_completion_tokens = 0

        total_tokens = 0

        logger.info(

            f"Processing "

            f"{len(context.summary_batches)} "

            f"summary batches."

        )

        for batch in context.summary_batches:

            logger.info(

                f"Batch "

                f"{batch['batch_index']} "

                f"of "

                f"{batch['batch_count']}"

            )
            

            user_prompt = self.build_prompt(

                context,

                current_summary,

                batch["text"]

            )

            response = self.call_llm(

                user_prompt

            )

            usage = response.get(

                "usage",

                {}

            )

            total_prompt_tokens += usage.get(

                "prompt_tokens",

                0

            )

            total_completion_tokens += usage.get(

                "completion_tokens",

                0

            )

            total_tokens += usage.get(

                "total_tokens",

                0

            )

            result = self.parse_response(

                response

            )

            self.validate_response(

                result

            )

            current_summary = (

                result["summary"]

            )

            current_score = (

                result["satisfaction_score"]

            )

            context.llm_output = result

        context.updated_summary = (

            current_summary

        )

        context.updated_satisfaction_score = (

            current_score

        )

        context.llm_usage = {

            "prompt_tokens":
                total_prompt_tokens,

            "completion_tokens":
                total_completion_tokens,

            "total_tokens":
                total_tokens

        }

        return context