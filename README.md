# 🎭 AI Coworker Engine — Gucci Leadership Simulation

> **Take-home Assignment for AI Engineer Intern @ Edtronaut**
>
> A dynamic, multi-agent AI simulation engine that enables learners to collaborate with realistic AI coworkers (CEO, CHRO, Regional Manager) in a Gucci Group leadership development context.

---

## 🌟 Project Overview

Unlike traditional "static" simulations (e.g., reading PDFs and submitting forms), this project introduces a **Dynamic AI Simulation Engine**. Users interact with AI coworkers who have distinct personalities, memory, and emotional states. The system acts as an **autonomous multi-agent platform** capable of using business tools, retrieving documents via RAG, and enforcing safety guardrails.

**Simulation Context:** Gucci Group Leadership Development
- **Role:** Group Global Organization Development (OD) Director
- **Mission:** Design a group-wide leadership system across 9 iconic luxury brands
- **Challenge:** Balance brand autonomy with group needs (inter-brand mobility, talent pipeline)

---

## ✨ Key Features

### 🎭 Persona-Based AI Coworkers (3 Distinct Roles)

The system features **three distinct AI coworkers**, each with unique personalities, expertise, and hidden constraints:

| Coworker | Personality | Expertise | Hidden Constraints |
|----------|-------------|-----------|-------------------|
| **Gucci Group CEO** | Strategic, authoritative, brand-protective | Brand DNA, Group mission, Autonomy vs Group needs | Refuses to dilute brand DNA, gets annoyed when users ignore brand identity |
| **Gucci Group CHRO** | Diplomatic, data-driven, people-focused | Competency framework, Talent mobility, HR strategy | Always references 4 competency themes, never violates employee privacy |
| **Regional Manager** | Practical, operational, realistic | Regional insights, Training needs, Rollout challenges | Never over-promises on rollout speed, shares real constraints like frozen budget |

### 🧠 Stateful Memory Management

The system maintains comprehensive conversation state:
- **Short-term memory**: Last 10 conversation turns (configurable)
- **Long-term memory**: FAISS-based semantic search across entire conversation history
- **State tracking**: User frustration level (0-10), topic relevance (0-1), jailbreak attempts, turns since progress, total turns

### 👁️ Supervisor Agent (The "Director" Layer)

An invisible background agent that monitors the conversation:
- **Stuck detection**: If no progress for 4+ consecutive turns, injects a subtle hint
- **Hint generation**: Guides user toward relevant topics (competency framework, 360 feedback, KPIs, regional insights)
- **Progress tracking**: Monitors turns since last meaningful progress

### 🛠️ Agentic Tool Use

The AI doesn't just chat — it **executes Python functions**. Included tools:

| Tool | Function | Example Output |
|------|----------|----------------|
| **KPI Lookup** | Retrieve current metrics | Inter-brand mobility: 23% (target 40%) |
| **Competency Framework** | Access 4 themes | Vision, Entrepreneurship, Passion, Trust |
| **Regional Insights** | Get challenges by region | Europe: frozen budget, local HR resistance |
| **360 Score Calculator** | Calculate multi-rater feedback | Average score: 4.2/5, strengths: Vision, Trust |
| **Module Info** | Get simulation module details | Module 1: Frame leadership problem (35-45 min) |

### 📚 RAG-Enabled Knowledge

Integrated with **FAISS** and **HuggingFace Sentence Transformers** (`all-MiniLM-L6-v2`) to ground AI responses strictly in Gucci's official leadership development documents (`data/knowledge/data.docx`).

### 🛡️ Safety Guardrails

Robust safety features prevent misuse:

| Feature | Detection Method | Response |
|---------|-----------------|----------|
| **Jailbreak detection** | Keyword matching ("ignore instructions", "act as", "forget your role") | "I can't change my role. Let's focus on the simulation." |
| **Off-topic detection** | Keyword matching (leadership, competency, 360, brand, DNA, talent, mobility, etc.) | Redirects back to simulation topics |
| **Stuck detection** | Turns since progress > 4 | Injects hint with suggested directions |

### 🌐 Web Interface

Clean, modern chat UI with:
- **Switch between 3 AI coworkers** in real-time
- **Session persistence** (refresh doesn't lose history)
- **Real-time safety indicators** (jailbreak, off-topic alerts)
- **Conversation reset** functionality
- **Session info display** (session ID, total turns, jailbreak attempts)

---

## 🏗️ System Architecture

The system utilizes a **Multi-Agent Orchestration Pipeline**:

```text
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              🌐 NGƯỜI DÙNG (Browser)                                 │
│                           http://localhost:8000/chat                                 │
└─────────────────────────────────────────────────────────────────────────────────────┘
                                          │
                                          ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                           🚀 FastAPI Server (main.py)                                │
│              - CORS middleware     - Static files serving                           │
│              - Route handling      - Session management                             │
└─────────────────────────────────────────────────────────────────────────────────────┘
                                          │
                                          ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                           📡 API Routes (routes.py)                                  │
│                      POST /api/v1/chat  -  GET /api/v1/session                       │
└─────────────────────────────────────────────────────────────────────────────────────┘
                                          │
                          ┌───────────────┴───────────────┐
                          ▼                               ▼
┌────────────────────────────────────┐   ┌────────────────────────────────────┐
│       🤖 Coworker Agent            │   │       👁️ Supervisor Agent           │
│         (coworker.py)              │   │         (supervisor.py)             │
├────────────────────────────────────┤   ├────────────────────────────────────┤
│ • Jailbreak detection              │   │ • Stuck detection (4+ turns)        │
│ • Off-topic detection              │   │ • Hint generation                   │
│ • Gọi RAG Service                  │   │ • Progress tracking                 │
│ • Gọi LLM (OpenAI/Mock)            │   │                                    │
└────────────────────────────────────┘   └────────────────────────────────────┘
                          │                               │
                          └───────────────┬───────────────┘
                                          ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                           🧠 RAG Service (rag_service.py)                            │
│                      augment_prompt() - Tạo context từ nhiều nguồn                   │
└─────────────────────────────────────────────────────────────────────────────────────┘
                                          │
              ┌───────────────────────────┼───────────────────────────┐
              ▼                           ▼                           ▼
┌────────────────────────────┐ ┌────────────────────────────┐ ┌────────────────────────────┐
│    📚 Vector Store         │ │    💾 Memory Service        │ │    🔧 Tools Service         │
│    (vector_store.py)       │ │      (memory.py)            │ │      (tools.py)             │
├────────────────────────────┤ ├────────────────────────────┤ ├────────────────────────────┤
│ • LangChain FAISS          │ │ • FAISS index              │ │ • lookup_kpi()              │
│ • HuggingFace embeddings   │ │ • Lưu lịch sử              │ │ • get_competency_framework()│
│ • Đọc file DOCX            │ │ • recall_relevant()        │ │ • get_regional_insights()   │
│ • search() / get_context() │ │ • add_message()            │ │ • calculate_360_score()     │
│ • build_vector_store()     │ │ • get_session_memory()     │ │ • format_kpi_dashboard()    │
└────────────────────────────┘ └────────────────────────────┘ └────────────────────────────┘
              │                           │                           │
              └───────────────────────────┼───────────────────────────┘
                                          ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              💾 DỮ LIỆU (data/knowledge/)                            │
├─────────────────────────────────────────────────────────────────────────────────────┤
│  • data.docx (Tài liệu Gucci chính thức)                                             │
│  • prompts/prompts.py (System prompts cho CEO, CHRO, Regional Manager)               │
│  • vector_store/ (FAISS index - tự động tạo)                                         │
└─────────────────────────────────────────────────────────────────────────────────────┘
                                          │
                                          ▼
┌─────────────────────────────────────────────────────────────────────────────────────┐
│                              ☁️ OpenAI API (Optional)                                │
│                           Model: gpt-4o-mini / Mock Mode                             │
└─────────────────────────────────────────────────────────────────────────────────────┘
```

## 📋 Data Flow

```text
User → Frontend → API → Coworker Agent → RAG → LLM → Response → User
                              ↑
                        Supervisor Agent
                        (kiểm tra stuck)
```

## 🚀 Tech Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Backend Framework** | FastAPI + Uvicorn | API server, routing, session management |
| **LLM** | OpenAI GPT-4o-mini / Mock Mode | Response generation (mock mode when no API key) |
| **Vector Database** | FAISS + LangChain | Store and search documents (data.docx) |
| **Embeddings** | HuggingFace Sentence Transformers | Convert text to vectors (all-MiniLM-L6-v2) |
| **Document Parsing** | python-docx | Read Gucci DOCX files |
| **Frontend** | HTML/CSS/JS (vanilla) | Chat interface, no build required |
| **Memory** | FAISS (custom) | Store conversation history, semantic search |

---

## 💻 Installation & Setup

### Prerequisites
- Python 3.10+
- (Optional) OpenAI API key for real LLM mode

### Installation Steps

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/ai-coworker-engine.git
cd ai-coworker-engine

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
source venv/bin/activate       # Mac/Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file (if you have API key)
echo "OPENAI_API_KEY=your_key_here" > .env
echo "LLM_MODEL=gpt-4o-mini" >> .env

# 5. Build vector store from data.docx
python scripts/build_vector_store.py

# 6. Run the server
python run.py
```

### Access the Application
Once the server is running, you can access the following endpoints:

| Service | URL | Description |
|---------|-----|-------------|
| 💬 **Chat Interface** | http://localhost:8000/chat | Web UI for interacting with AI coworkers |
| 📚 **API Documentation** | http://localhost:8000/docs | Swagger UI - test all API endpoints |
| ❤️ **Health Check** | http://localhost:8000/health | Verify server status |
| ℹ️ **System Info** | http://localhost:8000/info | View configuration and available coworkers |

### Quick Start

1. Open your browser and go to **http://localhost:8000/chat**
2. Select an AI coworker (CEO, CHRO, or Regional Manager)
3. Type your message and press Enter
4. Watch the AI respond with context from Gucci's official documents

### Default Port

The server runs on port `8000` by default. To change it, update the `.env` file:

```env
PORT=8080
```

### Environment Variables (.env)
Create a `.env` file in the root directory to configure the application:

```env
# OpenAI Configuration (optional - Mock Mode works without it)
OPENAI_API_KEY=your_api_key_here
LLM_MODEL=gpt-4o-mini

# Embedding Model
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2

# Memory Settings
MEMORY_WINDOW_SIZE=10
MAX_TURNS=30

# Server Configuration
HOST=0.0.0.0
PORT=8000
DEBUG=true
```

### Mock Mode

When no valid OpenAI API key is provided, the system automatically runs in **Mock Mode**.

#### How It Works

- All responses are generated from pre-defined templates based on Gucci's official documentation
- The RAG pipeline still retrieves context from `data.docx`
- Safety features (jailbreak, off-topic, stuck detection) remain fully active
- Session management and memory work exactly the same

## 🙏 Acknowledgements

This project was developed as part of the **AI Engineer Intern Take-home Assignment** for **Edtronaut**.

### Special Thanks

| To | For |
|----|-----|
| **Edtronaut** | The assignment, simulation context, and evaluation framework |
| **Gucci Group** | The leadership development framework and brand DNA |
| **LangChain** | Vector store utilities and text splitting |
| **FAISS** | Efficient similarity search library |
| **HuggingFace** | Sentence transformers embeddings |
| **FastAPI** | Modern, fast web framework for Python |
| **OpenAI** | GPT-4o-mini API (optional) |