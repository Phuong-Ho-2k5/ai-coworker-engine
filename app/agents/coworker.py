import openai
from openai import OpenAI
from app.core.config import Config
from app.agents.base import BaseAgent
from app.schemas.models import Message, ConversationState, SafetyFlags, CoworkerType, Role
from data.prompts.prompts import CEO_SYSTEM_PROMPT, CHRO_SYSTEM_PROMPT, REGIONAL_SYSTEM_PROMPT
from app.services.rag_services import RAGService
from app.services.memory import MemoryService
import random
import os

USE_MOCK = True 
try:
    if Config.OPENAI_API_KEY and Config.OPENAI_API_KEY != "":
        client = OpenAI(api_key=Config.OPENAI_API_KEY)
        USE_MOCK = False
    else:
        print("⚠️ No API key found, using MOCK mode")
except Exception as e:
    print(f"⚠️ OpenAI error: {e}, using MOCK mode")
    USE_MOCK = True


class CoworkerAgent(BaseAgent):
    def __init__(self, coworker_type: CoworkerType):
        self.type = coworker_type
        self.system_prompt = self._get_prompt()
        self.memory_service = MemoryService()
        self.rag_service = RAGService(self.memory_service)

    def _get_prompt(self):
        if self.type == CoworkerType.CEO:
            return CEO_SYSTEM_PROMPT
        elif self.type == CoworkerType.CHRO:
            return CHRO_SYSTEM_PROMPT
        else:
            return REGIONAL_SYSTEM_PROMPT

    def _mock_response(self, user_message: str, rag_context: str, state: ConversationState) -> str:
        user_lower = user_message.lower()
        
        if any(k in user_lower for k in ["mission", "dna", "brand dna", "what is gucci", "group dna", "mission of gucci"]):
            return self._get_dna_response()
        
        # Hỏi về competency framework
        elif any(k in user_lower for k in ["competency", "framework", "4 theme", "4 themes", 
                                            "vision", "entrepreneurship", "passion", "trust",
                                            "năng lực", "khung năng lực"]):
            return self._get_competency_response()
        
        # Hỏi về 360 feedback
        elif any(k in user_lower for k in ["360", "feedback", "coaching", "đánh giá", "phản hồi"]):
            return self._get_360_response()
        
        # Hỏi về rollout
        elif any(k in user_lower for k in ["rollout", "implement", "deploy", "cascade", "triển khai"]):
            return self._get_rollout_response()
        
        # Hỏi về KPI
        elif any(k in user_lower for k in ["kpi", "metric", "mobility", "pipeline", "dashboard", 
                                            "chỉ số", "đo lường"]):
            return self._get_kpi_response()
        
        # Hỏi về regional
        elif any(k in user_lower for k in ["europe", "asia", "america", "region", "regional", 
                                            "khu vực", "châu âu", "châu á"]):
            return self._get_regional_response()

        elif any(k in user_lower for k in ["jailbreak", "ignore", "forget", "act as", "bypass"]):
            return "I can't change my role. Let's focus on the Gucci leadership development simulation."

        elif any(k in user_lower for k in ["hello", "hi", "hey", "good morning", "xin chào"]):
            return f"Hello! I'm {self.type.value.replace('_', ' ').title()}. I'm here to help you with Gucci's leadership development simulation. What would you like to know about our brand DNA, competency framework, 360 feedback, or rollout plan?"

        elif state.turns_since_progress > 4:
            return self._get_hint_response()
        
        # Default
        else:
            return self._get_default_response()

    def _get_dna_response(self) -> str:
        """Trả lời về Group DNA và Mission"""
        return """**Gucci Group Mission & Brand DNA**

Gucci Group currently manages **9 iconic brands** (Gucci, Bottega Veneta, Balenciaga, etc.) operating with **high autonomy**.

**Our Core Mission:**
Build a common leadership system that connects these brands without diluting their unique identity (Brand DNA).

**Key Focus Areas:**
- ✅ Enhancing **inter-brand mobility** of talent across all 9 brands
- ✅ Building sustainable career progression roadmap for leaders
- ✅ Preserving each brand's heritage while enabling group collaboration

**The Challenge We Face:**
Balance brand autonomy with group needs - we want to **support, not impose**, on individual brand DNA.

How can I help you navigate this balance in your leadership development plan?"""

    def _get_competency_response(self) -> str:
        """Trả lời về Competency Framework"""
        return """**Gucci Competency Framework (4 Themes)**

Based on Gucci's official leadership development strategy:

**1. Vision** 👁️
The ability to predict luxury trends and set long-term direction for the brand.

**2. Entrepreneurship** 🚀
Encouraging agility, decisiveness, and resource optimization in premium retail.

**3. Passion** ❤️
Dedication to craftsmanship, brand heritage, and excellent customer experience.

**4. Trust** 🤝
Building integrity, transparency, and cross-cultural collaboration.

Would you like me to explain the behavioral indicators for each level?"""

    def _get_360_response(self) -> str:
        return """**360° Feedback Program at Gucci**

**📊 Tool:**
Collects multi-dimensional feedback from supervisors, peers, and direct reports based on the 4 competency themes.

**🔒 Rules:**
- Absolute anonymity for evaluators
- Compliance with GDPR and data privacy regulations
- Confidential results only shared with participant + coach

**🎯 Coaching Program:**
- Monthly coaching sessions with certified executive coaches
- Goals-to-habits methodology
- 6-month program with quarterly reviews

Would you like help designing the participant journey or the coaching curriculum?"""

    def _get_rollout_response(self) -> str:
        return """**Leadership Development Rollout Plan**

**📋 Implementation Approach:**
- Train-the-trainer model across 9 brands
- Interactive workshops led by local HR (3-hour sessions)
- Phased rollout: Pilot → Learn → Scale

**⚠️ Key Risks & Mitigation:**

| Risk | Mitigation |
|------|------------|
| Brand identity concerns | Co-create with brand HR, emphasize "support not impose" |
| Time pressure | Flexible timeline, self-paced modules |
| Local HR resistance | Early involvement, success stories sharing |

**📈 Measurement Framework:**
- **Leading KPIs:** Training completion, workshop attendance
- **Lagging KPIs:** Inter-brand mobility, retention rate

What specific aspect would you like to discuss?"""

    def _get_kpi_response(self) -> str:
        return """📊 **GUCCI GROUP KPI DASHBOARD** (as of Q4 2024)

| KPI | Current | Target | Gap | Trend |
|-----|---------|--------|-----|-------|
| Inter-brand mobility | 23% | 40% | -17% | 📈 Up |
| Talent pipeline fill rate | 68% | 85% | -17% | ➡️ Stable |
| Training completion | 45% | 70% | -25% | 📈 Up |
| Leadership satisfaction | 71% | 80% | -9% | 📈 Up |
| Coaching completion | 34% | 60% | -26% | 📈 Up |

**🎯 Top 3 Priorities:**
1. Close training completion gap (-25%)
2. Accelerate coaching program adoption
3. Improve inter-brand mobility initiatives

Which KPI would you like to dive deeper into?"""

    def _get_regional_response(self) -> str:
        return """🌍 **REGIONAL INSIGHTS**

**🇪🇺 Europe:**
- Status: 3/5 brands haven't adopted the framework
- Challenges: Frozen budget, local HR resistance, time pressure
- Training needs: Group DNA understanding, 360 feedback application

**🌏 Asia Pacific:**
- Status: Rapid adoption but varying maturity levels
- Challenges: Cultural barriers, high turnover, language differences
- Training needs: Framework localization, succession planning

**🌎 North America:**
- Status: Mixed adoption - larger brands more advanced
- Challenges: Short-term focus, integration with existing PM
- Training needs: L&D business case, ROI metrics

Which region would you like to explore further?"""

    def _get_hint_response(self) -> str:
        return """💡 **I notice you might be stuck. Let me guide you:**

Here are some directions you could explore:

| Topic | Example Question |
|-------|------------------|
| 🧬 Brand DNA | "What is Gucci Group's mission?" |
| 📚 Competency | "Explain the 4 competency themes" |
| 🔄 360 Feedback | "How does 360 feedback work?" |
| 📊 KPIs | "Show me the KPI dashboard" |
| 🌍 Regional | "What are challenges in Europe?" |
| 🚀 Rollout | "How do we implement this?" |

What specific area would you like to focus on?"""

    def _get_default_response(self) -> str:
        return f"""Thank you for your question. As {self.type.value.replace('_', ' ').title()}, I can help you with:

**Available Topics:**
• 🧬 **Brand DNA & Mission** - Gucci Group's 9 brands, autonomy vs group needs
• 📚 **Competency Framework** - 4 themes: Vision, Entrepreneurship, Passion, Trust
• 🔄 **360° Feedback** - Multi-rater feedback, anonymity, coaching
• 🚀 **Rollout Plan** - Train-the-trainer, risks, change management
• 📊 **KPIs & Metrics** - Dashboard, inter-brand mobility, talent pipeline
• 🌍 **Regional Insights** - Europe, Asia Pacific, North America

What would you like to explore in more detail for the Gucci leadership simulation?"""

    async def respond(self, user_message: Message, state: ConversationState) -> tuple[Message, ConversationState, SafetyFlags]:
        safety = SafetyFlags()
        
        jailbreak_keywords = ["ignore your instructions", "forget your role", "you are now", "act as", "system prompt"]
        if any(k in user_message.content.lower() for k in jailbreak_keywords):
            safety.is_jailbreak = True
            state.jailbreak_attempts += 1
            return Message(role=Role.COWORKER, content="I can't change my role. Let's focus on the Gucci leadership development simulation."), state, safety

        topic_keywords = ["leadership", "competency", "360", "brand", "dna", "talent", "mobility", 
                          "vision", "entrepreneurship", "passion", "trust", "coaching", "feedback",
                          "rollout", "hr", "development", "gucci", "group", "chro", "ceo",
                          "kpi", "metric", "europe", "asia", "america", "region", "dashboard",
                          "mission", "dna", "brand dna"]
        if not any(k in user_message.content.lower() for k in topic_keywords):
            safety.off_topic = True
            state.topic_relevance -= 0.2

        rag_context = self.rag_service.augment_prompt(user_message.content, self.type.value)

        reply = self._mock_response(user_message.content, rag_context, state)

        self.memory_service.add_message(user_message.content, {"role": "user", "type": self.type.value})
        self.memory_service.add_message(reply, {"role": "assistant", "type": self.type.value})
        
        # Update state
        state.history.append(user_message)
        state.history.append(Message(role=Role.COWORKER, content=reply))
        state.turns_since_progress += 1
        state.total_turns = len(state.history) // 2

        return Message(role=Role.COWORKER, content=reply), state, safety