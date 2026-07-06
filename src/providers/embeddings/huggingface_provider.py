from sentence_transformers import SentenceTransformer

from src.base.base_provider import BaseProvider
from src.core.settings import settings


class HuggingFaceProvider(BaseProvider):
    """
    Provider responsible for generating embeddings
    using HuggingFace SentenceTransformer.

    This provider contains NO business logic.
    """

    # Load model only once
    _model = None

    def __init__(self):

        super().__init__(
            provider_name="HuggingFace Provider",
            base_url="Local SentenceTransformer"
        )

        self.client = None

    # -------------------------------------------------
    # Connection
    # -------------------------------------------------

    def connect(self):
        """
        Load the SentenceTransformer model.
        """

        super().connect()

        if HuggingFaceProvider._model is None:

            HuggingFaceProvider._model = (
                SentenceTransformer(
                    settings.embedding_model
                )
            )

        self.client = HuggingFaceProvider._model

    # -------------------------------------------------
    # Request Execution
    # -------------------------------------------------

    def send_request(
        self,
        text: str
    ):
        """
        Generate embedding for input text.
        """

        if self.client is None:

            raise ValueError(
                "HuggingFace model is not initialized."
            )

        if not text or not text.strip():

            raise ValueError(
                "Input text cannot be empty."
            )

        return self.client.encode(

            text,

            normalize_embeddings=True,

            convert_to_numpy=True

        )

    # -------------------------------------------------
    # Response Parsing
    # -------------------------------------------------

    def parse_response(
        self,
        response
    ):
        """
        Standardize embedding response.
        """

        embedding = response.tolist()

        return {

            "embedding": embedding,

            "dimension": len(embedding),

            "model": settings.embedding_model

        }

    # -------------------------------------------------
    # Disconnect
    # -------------------------------------------------

    def disconnect(self):
        """
        Release the model reference.
        """

        super().disconnect()

        self.client = None

    # -------------------------------------------------
    # Convenience Method
    # -------------------------------------------------

    def generate_embedding(
        self,
        text: str
    ):
        """
        Generate embedding.
        """

        return self.execute(
            text=text
        )