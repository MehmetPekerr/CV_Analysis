import logging
import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

load_dotenv()

from app.controllers.cv_controller import router as cv_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(name)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("CV Analysis API starting up...")
    logger.info(
        "Ollama endpoint: %s | Model: %s",
        os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
        os.getenv("OLLAMA_MODEL", "llama3"),
    )
    yield
    logger.info("CV Analysis API shutting down.")


app = FastAPI(
    title="CV Scoring & Filtering API",
    description="AI-powered multi-criteria CV evaluation system backed by a local Ollama LLM.",
    version="2.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(cv_router)

frontend_dir = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "frontend")
)

if os.path.isdir(frontend_dir):
    app.mount("/static", StaticFiles(directory=frontend_dir), name="frontend")

    @app.get("/", include_in_schema=False)
    async def serve_index():
        return FileResponse(os.path.join(frontend_dir, "index.html"))
