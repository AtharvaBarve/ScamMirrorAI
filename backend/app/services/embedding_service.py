import logging
from typing import List, Union

logger = logging.getLogger(__name__)

class EmbeddingService:
    """
    Service responsible for generating vector embeddings from text for ChromaDB.
    Uses sentence-transformers which is optimized for fast, accurate retrieval (RAG).
    """
    def __init__(self):
        # We use a small, fast model optimized for semantic search and retrieval
        self.model_name = "all-MiniLM-L6-v2"
        self.model = None
        self._initialize_model()

    def _initialize_model(self):
        try:
            from sentence_transformers import SentenceTransformer
            logger.info(f"Loading embedding model: {self.model_name}")
            self.model = SentenceTransformer(self.model_name)
            logger.info("Embedding model loaded successfully.")
        except Exception as e:
            logger.error(f"Failed to load embedding model: {str(e)}")
            self.model = None

    def generate_embedding(self, text: Union[str, List[str]]) -> List[List[float]]:
        """
        Generates embeddings for a single string or a list of strings.
        Returns a list of vectors (even for a single string).
        """
        if not self.model:
            logger.warning("Embedding model is not loaded. Returning empty embedding.")
            # ChromaDB typically expects a list of floats. Return a zero vector of dim 384 for fallback.
            return [[0.0] * 384] if isinstance(text, str) else [[0.0] * 384 for _ in text]
        
        try:
            # model.encode returns a numpy array, convert to list of floats for ChromaDB
            embeddings = self.model.encode(text)
            
            # If a single string was passed, encode returns 1D array. Wrap it in a list.
            if isinstance(text, str):
                return [embeddings.tolist()]
            return embeddings.tolist()
        except Exception as e:
            logger.error(f"Error generating embedding: {str(e)}")
            return [[0.0] * 384] if isinstance(text, str) else [[0.0] * 384 for _ in text]

embedding_service = EmbeddingService()
