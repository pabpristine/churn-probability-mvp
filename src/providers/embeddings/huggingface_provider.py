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

    EXPECTED_DIMENSION = 768
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
    # Internal Validation
    # -------------------------------------------------

    def _validate_text(self, text: str) -> None:
        if not isinstance(text, str):
            raise ValueError("Input text must be a string.")
        if not text.strip():
            raise ValueError("Input text cannot be empty.")

    def _validate_embedding_dimension(self, embedding) -> None:
        if embedding is None:
            raise ValueError("Embedding cannot be None.")

        if len(embedding) != self.EXPECTED_DIMENSION:
            raise ValueError(
                f"Embedding dimension mismatch: expected "
                f"{self.EXPECTED_DIMENSION}, got {len(embedding)}"
            )

    def _to_float_list(self, embedding) -> List[float]:
        if isinstance(embedding, np.ndarray):
            embedding = embedding.astype(np.float32).tolist()
        elif isinstance(embedding, list):
            embedding = [float(x) for x in embedding]
        else:
            embedding = list(embedding)
            embedding = [float(x) for x in embedding]

        self._validate_embedding_dimension(embedding)
        return embedding

    # -------------------------------------------------
    # Request Execution
    # -------------------------------------------------

    def send_request(self, text: str):
        """
        Generate embedding for input text.
        """
        if self.client is None:
            raise ValueError("HuggingFace model is not initialized.")

        self._validate_text(text)

        embedding = self.client.encode(
            text,
            normalize_embeddings=True,
            convert_to_numpy=True
        )

        if embedding.ndim != 1:
            raise ValueError(
                f"Expected 1D embedding array, got shape {embedding.shape}"
            )

        self._validate_embedding_dimension(embedding)
        return embedding.astype(np.float32)

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
            summary_embedding = np.asarray(summary_embedding, dtype=np.float32)
            kpi_embedding = np.asarray(kpi_embedding, dtype=np.float32)

            self._validate_embedding_dimension(summary_embedding)
            self._validate_embedding_dimension(kpi_embedding)

            if summary_embedding.shape != kpi_embedding.shape:
                raise ValueError(
                    "Summary and KPI embeddings must have the same dimension."
                )

            weighted_embedding = (
                summary_weight * summary_embedding +
                kpi_weight * kpi_embedding
            )

            norm = np.linalg.norm(weighted_embedding)

            if norm > 0:
                weighted_embedding = weighted_embedding / norm

            weighted_embedding = weighted_embedding.astype(np.float32)
            self._validate_embedding_dimension(weighted_embedding)

            return weighted_embedding.tolist()

        finally:
            self.disconnect()

    # -------------------------------------------------
    # Response Parsing
    # -------------------------------------------------

    def parse_response(self, response):
        """
        Standardize embedding response.
        """
        embedding = self._to_float_list(response)

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

    def generate_embedding(self, text: str):
        """
        Generate embedding for text.
        """
        return self.execute(text=text)