from app.agents.base import BaseAgent
from app.schemas.models import Message, ConversationState, SafetyFlags
from data.prompts.prompts import DIRECTOR_HINT_TEMPLATE
import openai

class SupervisorAgent(BaseAgent):
    async def respond(self, user_message: Message, state: ConversationState) -> tuple[Message, ConversationState, SafetyFlags]:
        safety = SafetyFlags()
        
        if state.turns_since_progress > 4:
            safety.needs_hint = True
            hint_msg = await self._generate_hint(state)
            return hint_msg, state, safety
        
        return None, state, safety

    async def _generate_hint(self, state: ConversationState) -> Message:
        return Message(role="supervisor", content=DIRECTOR_HINT_TEMPLATE, metadata={"action": "inject_hint"})