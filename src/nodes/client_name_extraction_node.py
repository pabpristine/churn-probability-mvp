import re
from typing import Optional

from src.base.base_service import BaseService
from src.domain.entities.workflow_context import WorkflowContext
from src.providers.llm.groq_provider import GroqProvider
from src.prompts.client_name_extraction_prompt import (
    CLIENT_NAME_EXTRACTION_SYSTEM_PROMPT,
)


class ClientNameExtractionNode(BaseService):
    """
    Service to extract client name from user query.

    Flow:
    1. Try code-based extraction first.
    2. If it fails, use LLM fallback.
    3. Store final result in context.client_name.
    """

    def __init__(self):
        # Initialize base service
        super().__init__(
            service_name="Client Name Extraction Service",
            service_type="CLIENT_NAME_EXTRACTION"
        )

        # Initialize Groq provider for AI fallback
        self.groq_provider = GroqProvider()

    def validate(self, context: WorkflowContext):
        """
        Validate that user_query exists in context metadata.
        """
        user_query = context.metadata.get("user_query")

        if not user_query:
            raise ValueError(
                "user_query is required inside context.metadata"
            )

        return True

    def _clean_extracted_name(
        self,
        extracted_name: str
    ) -> str:
        """
        Clean unwanted trailing words from extracted client name.
        """
        extracted_name = extracted_name.strip(" .,!?:")

        trailing_words_pattern = (
            r"\b(in|on|at|with|for|from|this|that|full|details|latest)\b.*$"
        )

        extracted_name = re.sub(
            trailing_words_pattern,
            "",
            extracted_name,
            flags=re.IGNORECASE
        ).strip()

        return extracted_name

    def _extract_client_name_code(
        self,
        user_query: str
    ) -> Optional[str]:
        """
        Try to extract client name using regex-based logic.
        Works for both lowercase and uppercase queries.
        """

        patterns = [
            r"(?:for|of|about)\s+([a-zA-Z][a-zA-Z0-9&'_.-]*(?:\s+[a-zA-Z][a-zA-Z0-9&'_.-]*)*)",
            r"client\s+([a-zA-Z][a-zA-Z0-9&'_.-]*(?:\s+[a-zA-Z][a-zA-Z0-9&'_.-]*)*)",
            r"([a-zA-Z][a-zA-Z0-9&'_.-]*(?:\s+[a-zA-Z][a-zA-Z0-9&'_.-]*)*)\s+(?:report|summary|analysis|churn|kpi|updates)",
        ]

        for pattern in patterns:
            match = re.search(
                pattern,
                user_query,
                flags=re.IGNORECASE
            )

            if match:
                extracted_name = match.group(1).strip()
                extracted_name = self._clean_extracted_name(
                    extracted_name
                )

                if extracted_name:
                    return extracted_name

        return None

    def _extract_client_name_ai(
        self,
        user_query: str
    ) -> Optional[str]:
        """
        Use AI fallback to extract the client name.
        If Groq fails, return None instead of crashing.
        """

        prompt = f"""
Extract the client name from the following user query.

User Query:
{user_query}

Return only the client name.
If no client name is found, return UNKNOWN.
""".strip()

        try:
            response = self.groq_provider.generate_response(
                prompt=prompt,
                system_prompt=CLIENT_NAME_EXTRACTION_SYSTEM_PROMPT,
                temperature=0.0,
                max_tokens=20
            )

            content = response.get("content", "").strip()

            if not content or content.upper() == "UNKNOWN":
                return None

            return content

        except Exception as error:
            print(f"AI fallback failed: {error}")
            return None

    def process(
        self,
        context: WorkflowContext
    ) -> WorkflowContext:
        """
        Main processing logic:
        first code-based extraction,
        then AI fallback if needed.
        """

        user_query = context.metadata.get("user_query", "").strip()

        # Step 1: Try code-based extraction
        extracted_name = self._extract_client_name_code(
            user_query
        )

        if extracted_name:
            context.client_name = extracted_name
            context.metadata["client_name_extraction_method"] = "code"
            return context

        # Step 2: Try AI fallback
        extracted_name = self._extract_client_name_ai(
            user_query
        )

        if extracted_name:
            context.client_name = extracted_name
            context.metadata["client_name_extraction_method"] = "ai"
        else:
            context.client_name = None
            context.metadata["client_name_extraction_method"] = "not_found"

        return context


if __name__ == "__main__":
    user_query = input("Enter user query: ").strip()

    context = WorkflowContext()
    context.metadata["user_query"] = user_query

    service = ClientNameExtractionNode()
    result = service.execute(context)

    print("\nExtracted Client Name:", result.client_name)
    print(
        "Extraction Method:",
        result.metadata.get("client_name_extraction_method")
    )