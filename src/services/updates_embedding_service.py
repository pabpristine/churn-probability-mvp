from typing import List

from src.base.base_service import BaseService
from src.domain.entities.workflow_context import WorkflowContext
from src.providers.embeddings.huggingface_provider import HuggingFaceProvider


class UpdatesEmbeddingService(BaseService):
    """
    Generates an embedding from the current client's update-related text.

    The service reads the best available update text from WorkflowContext,
    creates an embedding using HuggingFaceProvider, and stores:

    - context.summary_embedding
    - context.summary_embedding_content

    This embedding will later be used to retrieve historical clients
    with similar update situations.
    """

    def __init__(self):
        super().__init__(
            service_name="Updates Embedding Service",
            service_type="EMBEDDING"
        )

        # This provider converts text into a numerical vector embedding.
        self.embedding_provider = HuggingFaceProvider()

    # -------------------------------------------------
    # Validation
    # -------------------------------------------------

    def validate(self, context: WorkflowContext):
        """
        Validate that at least one client update text source is available.
        """

        update_text = self._get_update_text(context)

        if not update_text:
            raise ValueError(
                "Update text is required for summary embedding. "
                "Provide updated_summary, final_client_summary, summary, "
                "formatted_update_history, or latest_client_update."
            )

        return True

    # -------------------------------------------------
    # Helpers
    # -------------------------------------------------

    def _get_update_text(self, context: WorkflowContext) -> str:
        """
        Return the best available current-client update text.

        Priority order:
        1. updated_summary: newest generated update summary
        2. final_client_summary: finalized client summary
        3. summary: normal client summary
        4. formatted_update_history: formatted historical update text
        5. latest_client_update: raw latest update dictionary
        """

        # Prefer the most recently generated summary.
        if context.updated_summary:
            return context.updated_summary.strip()

        # Use final summary if an updated summary is not available.
        if context.final_client_summary:
            return context.final_client_summary.strip()

        # Use standard summary as the next fallback.
        if context.summary:
            return context.summary.strip()

        # Use formatted historical updates when no summary exists.
        if context.formatted_update_history:
            return context.formatted_update_history.strip()

        # Last fallback: convert raw latest update fields into text.
        if context.latest_client_update:
            update_lines = []

            for key, value in context.latest_client_update.items():
                # Ignore missing or empty values.
                if value in (None, "", "null"):
                    continue

                update_lines.append(f"{key}: {value}")

            return "\n".join(update_lines).strip()

        # No valid update content was found.
        return ""

    def _generate_embedding(self, text: str) -> List[float]:
        """
        Generate a vector embedding from update text.

        The provider is expected to return:
        {
            "embedding": [float, float, ...]
        }
        """

        response = self.embedding_provider.generate_embedding(text)

        # Stop if provider did not return anything.
        if not response:
            raise ValueError("Empty response from embedding provider.")

        embedding = response.get("embedding")

        # Ensure expected embedding field is present.
        if embedding is None:
            raise ValueError(
                "Embedding provider response does not contain 'embedding'."
            )

        # Convert NumPy array or another iterable into a normal Python list.
        if not isinstance(embedding, list):
            embedding = list(embedding)

        # An empty vector should not be stored in the workflow context.
        if not embedding:
            raise ValueError("Generated summary embedding is empty.")

        return embedding

    # -------------------------------------------------
    # Main Process
    # -------------------------------------------------

    def process(self, context: WorkflowContext) -> WorkflowContext:
        """
        Generate the current client's update embedding and store it
        in WorkflowContext for later similarity retrieval.
        """

        # Get current client update text using the priority logic above.
        update_text = self._get_update_text(context)

        # Generate the vector from current client update text.
        embedding = self._generate_embedding(update_text)

        # Store embedding vector in shared workflow context.
        context.summary_embedding = embedding

        # Store the exact text used to generate the embedding.
        # This helps in debugging and explaining retrieval results later.
        context.summary_embedding_content = update_text

        # Optional metadata for logging/debugging.
        context.metadata["summary_embedding_generated"] = True
        context.metadata["summary_embedding_dimension"] = len(embedding)

        return context