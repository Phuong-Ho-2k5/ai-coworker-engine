from fastapi import APIRouter, HTTPException, Request
from app.schemas.models import Message, CoworkerType, ConversationState, ChatRequest, ChatResponse
from app.agents.coworker import CoworkerAgent
from app.agents.supervisor import SupervisorAgent
from app.services.memory import MemoryService
from app.services.vector_store import get_vector_store
from app.core.config import Config
import uuid
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["chat"])
memory_service = MemoryService()

sessions = {}


@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    
    logger.info(f"Chat request: coworker={request.coworker_type}, message={request.message[:50]}...")

    session_id = request.session_id or str(uuid.uuid4())
    
    if session_id not in sessions:
        logger.info(f"Creating new session: {session_id}")
        sessions[session_id] = ConversationState(
            coworker_type=request.coworker_type,
            session_id=session_id,
            simulation_id=request.simulation_id
        )
    
    state = sessions[session_id]
    
    coworker = CoworkerAgent(request.coworker_type)
    supervisor = SupervisorAgent()

    user_msg = Message(role="user", content=request.message)

    coworker_resp, new_state, safety = await coworker.respond(user_msg, state)
    
    supervisor_resp, new_state, safety2 = await supervisor.respond(user_msg, new_state)
    
    final_reply = coworker_resp.content
    if safety2.needs_hint and supervisor_resp:
        final_reply = f"{final_reply}\n\n💡 *Hint: {supervisor_resp.content}*"
        logger.info(f"Hint injected for session {session_id}")

    memory_service.add_message(request.message, {
        "type": request.coworker_type.value, 
        "session": session_id,
        "role": "user"
    })
    memory_service.add_message(final_reply, {
        "type": "response", 
        "session": session_id,
        "role": "assistant"
    })

    sessions[session_id] = new_state
    
    logger.info(f"Response sent for session {session_id}")
    
    return ChatResponse(
        reply=final_reply,
        session_id=session_id,
        safety_flags={
            "is_jailbreak": safety.is_jailbreak,
            "is_off_topic": safety.off_topic,
            "needs_hint": safety2.needs_hint if hasattr(safety2, 'needs_hint') else False,
            "is_stuck": safety2.needs_hint if hasattr(safety2, 'needs_hint') else False
        }
    )


@router.get("/session/{session_id}")
async def get_session(session_id: str):
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail=f"Session {session_id} not found")
    
    state = sessions[session_id]
    return {
        "session_id": session_id,
        "simulation_id": state.simulation_id,
        "coworker_type": state.coworker_type.value,
        "total_turns": state.total_turns,
        "turns_since_progress": state.turns_since_progress,
        "topic_relevance": state.topic_relevance,
        "jailbreak_attempts": state.jailbreak_attempts,
        "history": [
            {"role": m.role.value, "content": m.content[:200], "timestamp": str(m.timestamp)}
            for m in state.history[-10:]
        ]
    }


@router.get("/sessions")
async def list_sessions():
    return {
        "active_sessions": list(sessions.keys()),
        "count": len(sessions)
    }


@router.delete("/session/{session_id}")
async def clear_session(session_id: str):
    if session_id in sessions:
        del sessions[session_id]
        return {"status": "cleared", "session_id": session_id}
    raise HTTPException(status_code=404, detail="Session not found")


@router.get("/rag/search")
async def rag_search(query: str, k: int = 3):
    vector_store = get_vector_store()
    results = vector_store.search(query, k)
    
    return {
        "query": query,
        "num_results": len(results),
        "results": [
            {
                "source": r["source"],
                "content": r["content"],
                "relevance_score": 1 - r["score"]
            }
            for r in results
        ]
    }


@router.get("/rag/status")
async def rag_status():
    vector_store = get_vector_store()
    
    return {
        "status": "ready" if vector_store.vector_store else "not_initialized",
        "vector_store_path": str(vector_store.vector_store_path),
        "knowledge_path": str(vector_store.knowledge_path),
        "embedding_model": Config.EMBEDDING_MODEL,
        "chunk_config": {
            "chunk_size": 500,
            "chunk_overlap": 50
        }
    }


@router.post("/rag/rebuild")
async def rebuild_vector_store():
    vector_store = get_vector_store()
    success = vector_store.build_vector_store(force_rebuild=True)
    
    if success:
        return {
            "status": "success",
            "message": "Vector store rebuilt",
            "num_vectors": vector_store.vector_store.index.ntotal
        }
    else:
        raise HTTPException(status_code=500, detail="Failed to rebuild vector store")