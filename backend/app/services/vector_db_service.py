import logging
import os
import uuid
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

class VectorDBService:
    """
    Manages local ChromaDB instance and its modular collections for RAG.
    """
    def __init__(self):
        self.client = None
        self.collections = {}
        self._initialize_db()

    def _initialize_db(self):
        try:
            import chromadb
            # Initialize persistent local ChromaDB
            db_path = os.path.join(os.path.dirname(__file__), "../../chroma_db")
            os.makedirs(db_path, exist_ok=True)
            
            logger.info(f"Initializing ChromaDB at {db_path}")
            self.client = chromadb.PersistentClient(path=db_path)
            
            # Initialize modular knowledge collections
            collection_names = [
                "community_reports",
                "historical_campaigns",
                "government_advisories",
                "threat_intel_feeds"
            ]
            
            for name in collection_names:
                self.collections[name] = self.client.get_or_create_collection(
                    name=name,
                    metadata={"hnsw:space": "cosine"} # Cosine similarity for sentence transformers
                )
            
            logger.info(f"Successfully initialized {len(collection_names)} ChromaDB collections.")
            
        except Exception as e:
            logger.error(f"Failed to initialize ChromaDB: {str(e)}", exc_info=True)
            self.client = None

    def add_document(self, collection_name: str, text: str, embedding: List[float], metadata: Dict[str, Any], doc_id: Optional[str] = None):
        """
        Add a document and its embedding to a specific collection.
        """
        if not self.client or collection_name not in self.collections:
            logger.error(f"Cannot add document. Collection {collection_name} not found or DB offline.")
            return False
            
        try:
            if not doc_id:
                doc_id = str(uuid.uuid4())
                
            self.collections[collection_name].add(
                documents=[text],
                embeddings=[embedding],
                metadatas=[metadata],
                ids=[doc_id]
            )
            return True
        except Exception as e:
            logger.error(f"Error adding document to {collection_name}: {str(e)}")
            return False

    def query_collection(self, collection_name: str, query_embedding: List[float], n_results: int = 3, where: Optional[Dict] = None) -> List[Dict[str, Any]]:
        """
        Query a specific collection for similar documents.
        """
        if not self.client or collection_name not in self.collections:
            return []
            
        try:
            results = self.collections[collection_name].query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                where=where
            )
            
            formatted_results = []
            if results["documents"] and len(results["documents"]) > 0:
                for i in range(len(results["documents"][0])):
                    formatted_results.append({
                        "id": results["ids"][0][i],
                        "document": results["documents"][0][i],
                        "metadata": results["metadatas"][0][i] if results["metadatas"] else {},
                        "distance": results["distances"][0][i] if "distances" in results and results["distances"] else 0.0
                    })
            return formatted_results
        except Exception as e:
            logger.error(f"Error querying collection {collection_name}: {str(e)}")
            return []

vector_db = VectorDBService()
