from pydantic import BaseModel
from typing import List, Dict, Optional, Any
from enum import Enum
from datetime import datetime

class Role(str, Enum):
    USER = "user"
    COWORKER = "coworker"
    SUPERVISOR = "supervisor"

class Message(BaseModel):
    role: Role
    content: str
    timestamp: datetime = datetime.now()
    metadata: Dict[str, Any] = {}

class CoworkerType(str, Enum):
    CEO = "gucci_ceo"
    CHRO = "gucci_chro"
    REGIONAL_MANAGER = "regional_manager"

class ConversationState(BaseModel):
    session_id: str = ""
    simulation_id: str = "gucci_2024"
    coworker_type: CoworkerType
    history: List[Message] = []
    user_frustration_level: int = 0
    topic_relevance: float = 1.0
    turns_since_progress: int = 0
    total_turns: int = 0
    jailbreak_attempts: int = 0
    memory_embeddings: List[Any] = []

class SafetyFlags(BaseModel):
    is_jailbreak: bool = False
    needs_hint: bool = False
    off_topic: bool = False

class ChatRequest(BaseModel):
    simulation_id: str = "gucci_2024"
    coworker_type: CoworkerType
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    reply: str
    session_id: str
    safety_flags: Dict[str, bool]