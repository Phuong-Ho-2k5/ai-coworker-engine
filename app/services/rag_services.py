from typing import List, Dict, Any
from app.services.memory import MemoryService
from app.services.vector_store import get_vector_store
from app.services.tools import get_competency_framework


class RAGService:
    def __init__(self, memory_service: MemoryService):
        self.memory = memory_service
        self.vector_store = get_vector_store()
    
    def augment_prompt(self, user_query: str, coworker_type: str) -> str:
        context_parts = []
 
        doc_context = self.vector_store.get_context(user_query, k=3)
        if doc_context:
            context_parts.append(f"=== GUCCI OFFICIAL DOCUMENTS ===\n{doc_context}")

        relevant_history = self.memory.recall_relevant(user_query, k=2)
        if relevant_history:
            history_text = "\n".join(relevant_history)
            context_parts.append(f"=== RELEVANT CONVERSATION HISTORY ===\n{history_text}")

        competency = get_competency_framework("all")
        if competency:
            competency_text = "\n".join([f"- {k}: {v}" for k, v in competency.items()])
            context_parts.append(f"=== COMPETENCY FRAMEWORK ===\n{competency_text}")
        
        return "\n\n".join(context_parts)
    
    def search_knowledge_base(self, query: str, k: int = 3) -> List[Dict]:
        return self.vector_store.search(query, k)
    
    def get_similar_documents(self, query: str, k: int = 3) -> List[str]:
        results = self.vector_store.search(query, k)
        return [r["content"] for r in results]