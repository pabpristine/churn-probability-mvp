import json

from src.base.base_service import BaseService
from src.domain.entities.workflow_context import WorkflowContext

from src.repositories.client_repository import ClientRepository
from src.providers.llm.groq_provider import GroqProvider

from src.prompts.summary_system_prompts import SUMMARY_SYSTEM_PROMPT
from src.prompts.summary_user_prompts import SUMMARY_USER_PROMPT


class SummaryService(BaseService):
    """
    Generates an updated client summary by combining
    the latest update with historical context.
    """

    def __init__(self):

        super().__init__(
            service_name="Summary Service",
            service_type="SUMMARY"
        )

        self.client_repository = ClientRepository()
        self.groq_provider = GroqProvider()

    # -------------------------------------------------
    # Validation
    # -------------------------------------------------

    def validate(
        self,
        context: WorkflowContext
    ):

        if not context.client_id:
            raise ValueError("Client ID is required.")

        return True

    # -------------------------------------------------
    # Business Logic
    # -------------------------------------------------

    def process(
        self,
        context: WorkflowContext
    ) -> WorkflowContext:

        # ------------------------------------------
        # Fetch latest client update
        # ------------------------------------------

        client = self.client_repository.find_by_client_id(
            context.client_id
        )

        if client is None:
            raise Exception(
                f"Client not found : {context.client_id}"
            )

        # ------------------------------------------
        # Build Prompt
        # ------------------------------------------

        user_prompt = SUMMARY_USER_PROMPT.format(

            client_name=client.get("client_name"),

            client_id=context.client_id,

            latest_update=client.get("monday_input") or "",

            historical_summary=client.get("summary") or "NONE"

        )

        # ------------------------------------------
        # Call Groq
        # ------------------------------------------

        response = self.groq_provider.execute(

            system_prompt=SUMMARY_SYSTEM_PROMPT,

            user_prompt=user_prompt

        )

        print("\n================ RAW PROVIDER RESPONSE ================")
        print(response)

        # ------------------------------------------
        # Extract LLM Content
        # ------------------------------------------

        if not isinstance(response, dict):
            raise Exception(
                f"Expected dict from GroqProvider. Got {type(response)}"
            )

        if "content" not in response:
            raise Exception(
                f"'content' key missing.\nResponse = {response}"
            )

        llm_output = response["content"]

        print("\n================ LLM OUTPUT ================")
        print(llm_output)

        # Remove markdown if present

        llm_output = (
            llm_output
            .replace("```json", "")
            .replace("```", "")
            .strip()
        )

        # ------------------------------------------
        # Parse JSON
        # ------------------------------------------

        try:

            result = json.loads(llm_output)

        except Exception as error:

            raise Exception(
                f"\nUnable to parse JSON.\n\nLLM Output:\n{llm_output}\n\nError:{error}"
            )

        print("\n================ PARSED JSON ================")
        print(result)

        # ------------------------------------------
        # Validate JSON Keys
        # ------------------------------------------

        required_keys = [
            "client_name",
            "client_id",
            "summary",
            "satisfaction_score"
        ]

        for key in required_keys:

            if key not in result:

                raise Exception(
                    f"Missing key '{key}' in LLM Response.\n\nParsed JSON:\n{result}"
                )

        # ------------------------------------------
        # Update Database
        # ------------------------------------------

        self.client_repository.update(

            client["id"],

            {

                "summary": result["summary"],

                "satisfaction_score": result["satisfaction_score"]

            }

        )

        # ------------------------------------------
        # Update Context
        # ------------------------------------------

        context.summary = result["summary"]

        context.satisfaction_score = result["satisfaction_score"]

        context.output = result

        return context