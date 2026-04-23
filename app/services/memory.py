from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
from typing import List, Dict, Any
from app.core.config import Config

class MemoryService:
    def __init__(self):
        self.model = SentenceTransformer(Config.EMBEDDING_MODEL)
        self.dimension = self.model.get_embedding_dimension()
        self.index = faiss.IndexFlatL2(self.dimension)
        self.memory_store: List[Dict] = []

    def add_message(self, message: str, metadata: Dict[str, Any]):
        embedding = self.model.encode([message])[0]
        self.index.add(np.array([embedding]).astype('float32'))
        self.memory_store.append({"text": message, "metadata": metadata})

    def recall_relevant(self, query: str, k: int = 3) -> List[str]:
        if len(self.memory_store) == 0:
            return []
        query_emb = self.model.encode([query])[0]
        distances, indices = self.index.search(np.array([query_emb]).astype('float32'), min(k, len(self.memory_store)))
        return [self.memory_store[i]["text"] for i in indices[0] if i < len(self.memory_store)]
    
    def get_session_memory(self, session_id: str) -> List[Dict]:
        """Lấy memory theo session"""
        return [m for m in self.memory_store if m.get("metadata", {}).get("session") == session_id]