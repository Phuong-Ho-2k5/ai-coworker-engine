from abc import ABC, abstractmethod
from app.schemas.models import Message, ConversationState, SafetyFlags

class BaseAgent(ABC):
    @abstractmethod
    async def respond(self, user_message: Message, state: ConversationState) -> tuple[Message, ConversationState, SafetyFlags]:
        pass