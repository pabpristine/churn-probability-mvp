from typing import List, Any, Dict

import numpy as np
from sentence_transformers import SentenceTransformer  # NEW

from src.base.base_provider import BaseProvider
from src.core.settings import settings


class HuggingFaceProvider(BaseProvider):
    """
    Provider responsible for generating embeddings
    using a local sentence-transformers model.

    This provider contains NO business logic.
    """

    EXPECTED_DIMENSION = 768

    def __init__(self):
        super().__init__(
            provider_name="HuggingFace Local Provider",
            base_url="LOCAL_MODEL",
        )
        self.client = None  # not used; kept for interface

        # Load local sentence-transformers model
        # Use settings.embedding_model if you want to override via .env,
        # otherwise default to all-mpnet-base-v2.
        model_name = getattr(settings, "embedding_model", None) or "sentence-transformers/all-mpnet-base-v2"
        self.model = SentenceTransformer(model_name)

        # Embedding dimension expectation
        self.expected_dimension = getattr(settings, "embedding_dimension", self.EXPECTED_DIMENSION)

    # -------------------------------------------------
    # Connection
    # -------------------------------------------------

    def connect(self):
        """
        For local model, nothing special to connect.
        Kept for interface compatibility.
        """
        super().connect()
        # Optionally verify model outputs correct dimension
        test_vec = self.model.encode("test", convert_to_numpy=True)
        if test_vec.shape[-1] != self.expected_dimension:
            raise ValueError(
                f"Embedding dimension mismatch: expected "
                f"{self.expected_dimension}, got {test_vec.shape[-1]}"
            )

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

        if len(embedding) != self.expected_dimension:
            raise ValueError(
                f"Embedding dimension mismatch: expected "
                f"{self.expected_dimension}, got {len(embedding)}"
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
    # Local Embedding Execution
    # -------------------------------------------------

    def _generate_local_embedding(self, text: str) -> List[float]:
        """
        Generate embedding using local sentence-transformers model.
        """
        # model.encode returns numpy array if convert_to_numpy=True
        vec = self.model.encode(text, convert_to_numpy=True)
        # Ensure 1D vector
        if vec.ndim > 1:
            vec = vec.squeeze()
        return self._to_float_list(vec)

    def send_request(self, text: str):
        """
        Generate embedding for input text via local model.
        """
        self.connect()
        self._validate_text(text)

        embedding = self._generate_local_embedding(text)

        # Keep numpy array internally for compatibility with existing code
        return np.asarray(embedding, dtype=np.float32)

    # -------------------------------------------------
    # Weighted Embedding
    # -------------------------------------------------

    def generate_weighted_embedding(
        self,
        summary_embedding: List[float],
        kpi_embedding: List[float],
        summary_weight: float = 0.7,
        kpi_weight: float = 0.3,
    ) -> List[float]:
        """
        Generate a weighted embedding by combining
        summary and KPI embeddings.

        The resulting vector is normalized to unit length.
        """
        summary_embedding_arr = np.asarray(summary_embedding, dtype=np.float32)
        kpi_embedding_arr = np.asarray(kpi_embedding, dtype=np.float32)

        self._validate_embedding_dimension(summary_embedding_arr)
        self._validate_embedding_dimension(kpi_embedding_arr)

        if summary_embedding_arr.shape != kpi_embedding_arr.shape:
            raise ValueError(
                "Summary and KPI embeddings must have the same dimension."
            )

        weighted_embedding = (
            summary_weight * summary_embedding_arr +
            kpi_weight * kpi_embedding_arr
        )

        norm = np.linalg.norm(weighted_embedding)

        if norm > 0:
            weighted_embedding = weighted_embedding / norm

        weighted_embedding = weighted_embedding.astype(np.float32)
        self._validate_embedding_dimension(weighted_embedding)

        return weighted_embedding.tolist()

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
            "model": settings.embedding_model,
        }

    # -------------------------------------------------
    # Disconnect
    # -------------------------------------------------

    def disconnect(self):
        """
        For local provider, there's nothing heavy to release.
        Kept for interface compatibility.
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