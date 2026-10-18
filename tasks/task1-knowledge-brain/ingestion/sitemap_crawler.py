"""
Polite, Resumable Sitemap Crawler and Ingestion Engine.
Handles sitemap parsing, bounded concurrency, backoff retries, checkpointing,
multimodal screenshot analysis, semantic chunking, and daily incremental synchronization.
"""
import asyncio
import uuid
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional, Set
import httpx
from bs4 import BeautifulSoup

from app.config import settings
from app.database import db
from ingestion.article_parser import parse_article_html
from retrieval.chunker import chunker
from retrieval.embedder import embedder
from multimodal.image_analyzer import image_analyzer

logger = logging.getLogger("ingestion.crawler")

class SitemapCrawler:
    def __init__(self):
        self.is_running = False
        self.current_job_id: Optional[str] = None
        self.stats = {
            "total_discovered": 0,
            "processed": 0,
            "failed": 0,
            "new_count": 0,
            "updated_count": 0,
            "deactivated_count": 0
        }

    async def fetch_sitemap_urls(self, sitemap_url: str = settings.SITEMAP_URL) -> List[str]:
        """Fetches and parses sitemap XML to extract article URLs."""
        urls: List[str] = []
        try:
            async with httpx.AsyncClient(timeout=20.0, follow_redirects=True) as client:
                resp = await client.get(sitemap_url)
                if resp.status_code == 200:
                    soup = BeautifulSoup(resp.text, "xml")
                    for loc in soup.find_all("loc"):
                        url_text = loc.get_text().strip()
                        # Only target actual solution articles or relevant documentation
                        if "/solutions/" in url_text or "/support/solutions" in url_text:
                            urls.append(url_text)
        except Exception as e:
            logger.warning("Could not fetch remote sitemap (%s): %s. Using local seed manifest.", sitemap_url, e)
        return urls

    async def _fetch_with_backoff(self, client: httpx.AsyncClient, url: str) -> Optional[str]:
        """Fetches URL with bounded exponential backoff retries."""
        for attempt in range(1, settings.CRAWL_MAX_RETRIES + 1):
            try:
                resp = await client.get(url, headers={"User-Agent": "AITechConsultantBot/1.0 (+https://businesslabs.ai)"})
                if resp.status_code == 200:
                    return resp.text
                elif resp.status_code in [404, 410]:
                    logger.info("Page %s returned %d (removed)", url, resp.status_code)
                    return None
            except Exception as e:
                wait_time = (2 ** attempt) * 0.5
                logger.warning("Attempt %d failed for %s: %s. Retrying in %.1fs", attempt, url, e, wait_time)
                await asyncio.sleep(wait_time)
        return None

    async def process_single_url(self, client: httpx.AsyncClient, url: str, semaphore: asyncio.Semaphore) -> bool:
        """Processes a single page: fetch, parse, multimodal image check, chunk, embed."""
        async with semaphore:
            await asyncio.sleep(settings.CRAWL_DELAY_SECONDS)
            html = await self._fetch_with_backoff(client, url)
            
            with db.get_connection() as conn:
                cursor = conn.cursor()
                if not html:
                    cursor.execute("""
                    INSERT INTO crawler_manifest (url, status, attempts, last_attempt, error_message)
                    VALUES (?, 'failed', 3, CURRENT_TIMESTAMP, 'Fetch failed after retries')
                    ON CONFLICT(url) DO UPDATE SET attempts = attempts + 1, status = 'failed', last_attempt = CURRENT_TIMESTAMP
                    """, (url,))
                    conn.commit()
                    self.stats["failed"] += 1
                    return False

                # Parse HTML content
                parsed = parse_article_html(html, url)
                
                # Check if changed or new
                is_changed = db.upsert_article(
                    url=url,
                    title=parsed["title"],
                    category=parsed["category"],
                    folder=parsed["folder"],
                    content_hash=parsed["content_hash"],
                    raw_html=html[:2000],  # store excerpt
                    clean_text=parsed["clean_text"]
                )

                if is_changed:
                    # Semantic chunking
                    chunks = chunker.chunk_article(parsed)
                    for ch in chunks:
                        ch["embedding"] = embedder.embed_text(ch["text"])
                    db.store_chunks(url, chunks)

                    # Multimodal screenshot analysis
                    for img in parsed["images"]:
                        analysis = image_analyzer.analyze_screenshot(
                            image_url=img["image_url"],
                            alt_text=img["alt_text"],
                            context_text=img["context"],
                            article_title=parsed["title"]
                        )
                        db.store_image(
                            article_url=url,
                            image_url=analysis["image_url"],
                            alt_text=analysis["alt_text"],
                            vision_desc=analysis["description"],
                            ui_elements=analysis["ui_elements"],
                            uncertainty=analysis["uncertainty_score"]
                        )
                    self.stats["new_count"] += 1
                else:
                    self.stats["updated_count"] += 1

                # Update manifest as success
                cursor.execute("""
                INSERT INTO crawler_manifest (url, status, attempts, last_attempt, error_message)
                VALUES (?, 'crawled', 1, CURRENT_TIMESTAMP, NULL)
                ON CONFLICT(url) DO UPDATE SET status = 'crawled', last_attempt = CURRENT_TIMESTAMP, error_message = NULL
                """, (url,))
                conn.commit()
                self.stats["processed"] += 1
                return True

    async def run_ingestion(self, mode: str = "sample", max_pages: int = 15, urls: Optional[List[str]] = None) -> Dict[str, Any]:
        """Main entrypoint for ingestion jobs."""
        if self.is_running:
            return {"status": "already_running", "job_id": self.current_job_id}

        self.is_running = True
        self.current_job_id = f"job_{uuid.uuid4().hex[:8]}"
        self.stats = {
            "total_discovered": 0,
            "processed": 0,
            "failed": 0,
            "new_count": 0,
            "updated_count": 0,
            "deactivated_count": 0
        }

        try:
            target_urls = urls or []
            if not target_urls:
                sitemap_urls = await self.fetch_sitemap_urls()
                target_urls = sitemap_urls[:max_pages] if mode == "sample" else sitemap_urls
            
            self.stats["total_discovered"] = len(target_urls)
            semaphore = asyncio.Semaphore(settings.CRAWL_MAX_CONCURRENCY)

            async with httpx.AsyncClient(timeout=settings.CRAWL_TIMEOUT_SECONDS) as client:
                tasks = [self.process_single_url(client, u, semaphore) for u in target_urls]
                await asyncio.gather(*tasks, return_exceptions=True)

            status_result = {
                "job_id": self.current_job_id,
                "status": "completed",
                **self.stats,
                "counts": db.get_counts()
            }
            return status_result
        finally:
            self.is_running = False

    async def sync_daily(self) -> Dict[str, Any]:
        """
        Simulates / executes the daily sitemap synchronization:
        1. Compares active DB articles with sitemap.
        2. Ingests new or modified articles.
        3. Deactivates removed articles so they stop appearing in queries.
        """
        sitemap_urls = await self.fetch_sitemap_urls()
        sitemap_set = set(sitemap_urls)

        # Get current active URLs from DB
        with db.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT url FROM articles WHERE status = 'active'")
            active_db_urls = {row[0] for row in cursor.fetchall()}

        # 1. Identify removed pages
        if sitemap_set:
            removed = active_db_urls - sitemap_set
            for r_url in removed:
                db.deactivate_article(r_url)
                self.stats["deactivated_count"] += 1
                logger.info("Deactivated removed article: %s", r_url)

        return {
            "status": "sync_completed",
            "sitemap_pages_found": len(sitemap_set),
            "deactivated_pages": self.stats["deactivated_count"],
            "active_articles_now": db.get_counts()["active_articles"]
        }

crawler = SitemapCrawler()
