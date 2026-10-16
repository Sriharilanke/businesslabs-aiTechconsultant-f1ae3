"""
Health, metrics and article discovery endpoints for Task 1: Knowledge Brain.
"""
import time
from typing import List, Dict, Any
from fastapi import APIRouter
from app.models.schemas import HealthResponse
from app.config import settings
from app.database import db

router = APIRouter(tags=["Health & System"])
START_TIME = time.time()

@router.get("/health", response_model=HealthResponse)
async def health_check():
    counts = db.get_counts()
    return HealthResponse(
        status="healthy",
        service="Knowledge Brain Service",
        version=settings.VERSION,
        active_articles=counts["active_articles"],
        total_chunks=counts["total_chunks"],
        open_escalations=counts["open_escalations"],
        uptime_seconds=round(time.time() - START_TIME, 2)
    )

@router.get("/metrics")
async def get_metrics():
    counts = db.get_counts()
    return {
        "status": "operational",
        "active_articles": counts["active_articles"],
        "total_chunks": counts["total_chunks"],
        "open_escalations": counts["open_escalations"],
        "embedding_dimension": settings.EMBEDDING_DIMENSION,
        "hybrid_alpha": settings.HYBRID_ALPHA,
        "claude_model": settings.CLAUDE_MODEL_PRIMARY,
        "rag_prompt_version": settings.RAG_PROMPT_VERSION
    }

@router.get("/articles")
async def list_articles() -> List[Dict[str, Any]]:
    with db.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT a.url, a.title, a.category, a.folder, a.status, a.last_crawled,
               COUNT(DISTINCT c.chunk_id) as chunk_count,
               COUNT(DISTINCT i.image_url) as image_count
        FROM articles a
        LEFT JOIN article_chunks c ON a.url = c.article_url
        LEFT JOIN article_images i ON a.url = i.article_url
        GROUP BY a.url
        ORDER BY a.last_crawled DESC
        """)
        rows = cursor.fetchall()
        return [dict(r) for r in rows]
