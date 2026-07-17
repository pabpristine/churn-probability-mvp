from groq import Groq

from src.base.base_provider import BaseProvider
from src.core.settings import settings


class GroqProvider(BaseProvider):
    """
    Provider responsible for interacting with the Groq LLM.

    This provider contains no business logic and is used
    only for communicating with the Groq API.
    """

    def __init__(self):

        super().__init__(
            provider_name="Groq Provider",
            base_url="https://api.groq.com/openai/v1"
        )

        self.client = None

    # -------------------------------------------------
    # Connection
    # -------------------------------------------------

    def connect(self):
        """
        Establish a connection to the Groq API.
        """

        super().connect()

        self.client = Groq(
            api_key=settings.groq_api_key
        )

    # -------------------------------------------------
    # Request Execution
    # -------------------------------------------------

    def send_request(
        self,
        prompt: str,
        system_prompt: str = "You are a helpful AI assistant.",
        temperature: float = 0.2,
        max_tokens: int = 1024,
        response_format: dict = None
    ):
        """
        Send a chat completion request to Groq.

        response_format example:
        {"type": "json_object"}
        """

        if self.client is None:
            raise ValueError(
                "Groq client is not initialized."
            )

        request_payload = {
            "model": settings.groq_model,
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        # Add response_format only when explicitly requested.
        if response_format:
            request_payload["response_format"] = response_format

        return self.client.chat.completions.create(
            **request_payload
        )

    # -------------------------------------------------
    # Response Parsing
    # -------------------------------------------------

    def parse_response(
        self,
        response
    ):
        """
        Standardize the Groq response.
        """

        return {
            "content": response.choices[0].message.content,
            "model": response.model,
            "usage": {
                "prompt_tokens": response.usage.prompt_tokens,
                "completion_tokens": response.usage.completion_tokens,
                "total_tokens": response.usage.total_tokens
            },
            "finish_reason": response.choices[0].finish_reason
        }

    # -------------------------------------------------
    # Disconnect
    # -------------------------------------------------

    def disconnect(self):
        """
        Release the Groq client.
        """

        super().disconnect()

        self.client = None

    # -------------------------------------------------
    # Convenience Method
    # -------------------------------------------------

    def generate_response(
        self,
        prompt: str,
        system_prompt: str = "You are a helpful AI assistant.",
        temperature: float = 0.2,
        max_tokens: int = 1024,
        response_format: dict = None
    ):
        """
        Generate a response using the Groq LLM.
        """

        return self.execute(
            prompt=prompt,
            system_prompt=system_prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            response_format=response_format
        )