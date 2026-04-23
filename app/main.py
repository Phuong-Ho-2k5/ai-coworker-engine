from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from contextlib import asynccontextmanager
import logging
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.api.routes import router
from app.core.config import Config
import uvicorn

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Quản lý vòng đời của ứng dụng"""
    logger.info("=" * 60)
    logger.info("🚀 AI Coworker Engine Starting...")
    logger.info(f"📝 LLM Model: {Config.LLM_MODEL}")
    logger.info(f"🧠 Memory Window: {Config.MEMORY_WINDOW_SIZE}")
    logger.info(f"🔍 RAG Enabled: Yes (FAISS + Sentence Transformers)")
    logger.info(f"🛡️ Safety Features: Jailbreak Detection, Off-topic Detection, Stuck Detection")
    logger.info("=" * 60)
    logger.info("🌐 Chat UI available at: http://localhost:8000/chat")
    logger.info("=" * 60)
    
    yield
    
    logger.info("🛑 AI Coworker Engine Shutting down...")


app = FastAPI(
    title="AI Coworker Engine",
    description="AI Co-worker Engine for Edtronaut Job Simulation Platform",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

static_path = Path(__file__).parent / "static"
if not static_path.exists():
    static_path.mkdir(parents=True)

app.mount("/static", StaticFiles(directory=str(static_path)), name="static")

@app.get("/chat")
async def chat_ui():
    """Giao diện chat web"""
    html_path = static_path / "index.html"
    if html_path.exists():
        return FileResponse(str(html_path))
    return {"error": "Chat UI not found. Please ensure app/static/index.html exists"}

@app.get("/")
async def root():
    return {
        "service": "AI Coworker Engine",
        "version": "1.0.0",
        "status": "running",
        "chat_ui": "http://localhost:8000/chat",
        "api_docs": "http://localhost:8000/docs",
        "endpoints": {
            "chat": "POST /api/v1/chat",
            "session": "GET /api/v1/session/{session_id}",
            "sessions": "GET /api/v1/sessions",
            "health": "GET /health"
        }
    }


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "AI Coworker Engine",
        "llm_model": Config.LLM_MODEL
    }


@app.get("/info")
async def info():
    """Thông tin chi tiết về hệ thống"""
    return {
        "config": {
            "llm_model": Config.LLM_MODEL,
            "memory_window_size": Config.MEMORY_WINDOW_SIZE,
            "max_turns": Config.MAX_TURNS,
            "embedding_model": Config.EMBEDDING_MODEL
        },
        "coworkers": [
            {
                "type": "gucci_ceo",
                "name": "Gucci Group CEO",
                "personality": "Strategic, authoritative, brand-protective"
            },
            {
                "type": "gucci_chro",
                "name": "Gucci Group CHRO",
                "personality": "Diplomatic, data-driven, people-focused"
            },
            {
                "type": "regional_manager",
                "name": "Regional Employer Branding Manager",
                "personality": "Practical, operational, realistic"
            }
        ]
    }

app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )