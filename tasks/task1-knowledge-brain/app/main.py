"""
FastAPI application entrypoint for Task 1: Knowledge Brain.
"""
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import db
from app.api.routes_query import router as query_router
from app.api.routes_ingestion import router as ingestion_router
from app.api.routes_escalations import router as escalations_router
from app.api.routes_health import router as health_router
from seed_data.seed_knowledge import seed_knowledge_base

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("knowledge_brain")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ensure database is initialized and seeded if empty
    counts = db.get_counts()
    if counts["active_articles"] == 0:
        logger.info("Database empty, running initial seed...")
        seed_knowledge_base()
    logger.info("Knowledge Brain service started successfully on port %d", settings.API_PORT)
    yield
    logger.info("Shutting down Knowledge Brain service...")

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Knowledge Brain API - Multimodal RAG with Brilliant Directories sitemap crawling, image understanding, citations, and human escalations.",
    lifespan=lifespan
)

# Enable CORS for frontend dashboard and cross-service calls
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(query_router)
app.include_router(ingestion_router)
app.include_router(escalations_router)
app.include_router(health_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host=settings.HOST, port=settings.API_PORT, reload=False)
