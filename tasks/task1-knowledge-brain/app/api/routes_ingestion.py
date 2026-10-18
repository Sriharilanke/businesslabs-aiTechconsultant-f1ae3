"""
Ingestion and sitemap sync endpoints for Task 1: Knowledge Brain.
"""
import asyncio
from fastapi import APIRouter, BackgroundTasks, HTTPException
from app.models.schemas import IngestionRequest, IngestionStatus
from ingestion.sitemap_crawler import crawler
from app.database import db

router = APIRouter(prefix="/ingestion", tags=["Ingestion"])

@router.post("/run", response_model=IngestionStatus)
async def run_ingestion(req: IngestionRequest, background_tasks: BackgroundTasks):
    """
    Triggers polite crawler on Brilliant Directories sitemap.
    Supports 'sample' (15 pages) or 'incremental'.
    """
    if crawler.is_running:
        return IngestionStatus(
            job_id=crawler.current_job_id or "active",
            status="running",
            message="An ingestion job is currently executing.",
            active_articles_count=db.get_counts()["active_articles"],
            total_chunks_count=db.get_counts()["total_chunks"]
        )

    # Launch task
    background_tasks.add_task(crawler.run_ingestion, mode=req.mode, max_pages=req.max_pages or 15, urls=req.urls)
    
    return IngestionStatus(
        job_id="job_queued",
        status="running",
        message=f"Ingestion started in mode='{req.mode}' for up to {req.max_pages} pages.",
        active_articles_count=db.get_counts()["active_articles"],
        total_chunks_count=db.get_counts()["total_chunks"]
    )

@router.get("/status", response_model=IngestionStatus)
async def get_ingestion_status():
    counts = db.get_counts()
    return IngestionStatus(
        job_id=crawler.current_job_id or "idle",
        status="running" if crawler.is_running else "idle",
        total_discovered=crawler.stats.get("total_discovered", 0),
        pages_processed=crawler.stats.get("processed", 0),
        pages_failed=crawler.stats.get("failed", 0),
        pages_new=crawler.stats.get("new_count", 0),
        pages_updated=crawler.stats.get("updated_count", 0),
        pages_deactivated=crawler.stats.get("deactivated_count", 0),
        active_articles_count=counts["active_articles"],
        total_chunks_count=counts["total_chunks"],
        message="Crawler idle" if not crawler.is_running else "Crawler active"
    )

@router.post("/sync")
async def trigger_daily_sync():
    """Simulates daily sitemap check, detecting changes and deactivating deleted pages."""
    result = await crawler.sync_daily()
    return result
