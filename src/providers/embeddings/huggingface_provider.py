from typing import List

import numpy as np
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

            HuggingFaceProvider._model = SentenceTransformer(
                settings.embedding_model
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
    # Weighted Embedding
    # -------------------------------------------------

    def generate_weighted_embedding(
        self,
        summary_embedding: List[float],
        kpi_embedding: List[float],
        summary_weight: float = 0.7,
        kpi_weight: float = 0.3
    ) -> List[float]:
        """
        Generate a weighted embedding by combining
        summary and KPI embeddings.

        The resulting vector is normalized to unit length.
        """

        self.connect()

        try:

            summary_embedding = np.asarray(
                summary_embedding,
                dtype=np.float32
            )

            kpi_embedding = np.asarray(
                kpi_embedding,
                dtype=np.float32
            )

            if summary_embedding.shape != kpi_embedding.shape:

                raise ValueError(
                    "Summary and KPI embeddings must have the same dimension."
                )

            weighted_embedding = (

                summary_weight * summary_embedding +

                kpi_weight * kpi_embedding

            )

            norm = np.linalg.norm(
                weighted_embedding
            )

            if norm > 0:

                weighted_embedding = (
                    weighted_embedding / norm
                )

            return weighted_embedding.tolist()

        finally:

            self.disconnect()

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
        Generate embedding for text.
        """

        return self.execute(
            text=text
        )