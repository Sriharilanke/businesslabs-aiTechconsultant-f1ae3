"""
Database management for Task 1: Knowledge Brain using SQLite.
"""
import sqlite3
import json
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
from app.config import settings

logger = logging.getLogger("knowledge_brain.db")

class Database:
    def __init__(self, db_path: str = settings.DATABASE_PATH):
        self.db_path = db_path
        self.init_db()

    def get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Articles table
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS articles (
                url TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                category TEXT DEFAULT 'General',
                folder TEXT DEFAULT 'Documentation',
                content_hash TEXT,
                raw_html TEXT,
                clean_text TEXT NOT NULL,
                status TEXT DEFAULT 'active', -- 'active' or 'deactivated'
                last_crawled TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_modified TEXT
            );
            """)

            # Chunks table with embeddings
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS article_chunks (
                chunk_id TEXT PRIMARY KEY,
                article_url TEXT NOT NULL,
                section_heading TEXT,
                text_content TEXT NOT NULL,
                embedding_json TEXT NOT NULL,
                token_count INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (article_url) REFERENCES articles(url) ON DELETE CASCADE
            );
            """)

            # Article Images table with vision analysis
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS article_images (
                image_url TEXT PRIMARY KEY,
                article_url TEXT NOT NULL,
                alt_text TEXT,
                vision_description TEXT NOT NULL,
                ui_elements_json TEXT,
                uncertainty_score REAL DEFAULT 0.0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (article_url) REFERENCES articles(url) ON DELETE CASCADE
            );
            """)

            # Crawler manifest table for polite resumable crawling
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS crawler_manifest (
                url TEXT PRIMARY KEY,
                status TEXT DEFAULT 'pending', -- 'pending', 'crawled', 'failed', 'deactivated'
                attempts INTEGER DEFAULT 0,
                last_attempt TIMESTAMP,
                error_message TEXT
            );
            """)

            # Escalations table for human-in-the-loop
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS escalations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                question TEXT NOT NULL,
                context TEXT,
                user_id TEXT,
                reason TEXT DEFAULT 'insufficient_evidence',
                status TEXT DEFAULT 'open', -- 'open' or 'resolved'
                expert_answer TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                resolved_at TIMESTAMP
            );
            """)

            # Ingestion runs log
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS ingestion_runs (
                job_id TEXT PRIMARY KEY,
                started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                completed_at TIMESTAMP,
                status TEXT DEFAULT 'running',
                total_discovered INTEGER DEFAULT 0,
                processed INTEGER DEFAULT 0,
                failed INTEGER DEFAULT 0,
                new_count INTEGER DEFAULT 0,
                updated_count INTEGER DEFAULT 0,
                deactivated_count INTEGER DEFAULT 0,
                message TEXT
            );
            """)

            conn.commit()
            logger.info("Database initialized successfully at %s", self.db_path)

    # Article operations
    def upsert_article(self, url: str, title: str, category: str, folder: str, 
                       content_hash: str, raw_html: str, clean_text: str, last_modified: str = None) -> bool:
        """Returns True if article is new or updated, False if unchanged."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT content_hash, status FROM articles WHERE url = ?", (url,))
            row = cursor.fetchone()
            
            is_new_or_updated = False
            if row is None:
                cursor.execute("""
                INSERT INTO articles (url, title, category, folder, content_hash, raw_html, clean_text, status, last_modified)
                VALUES (?, ?, ?, ?, ?, ?, ?, 'active', ?)
                """, (url, title, category, folder, content_hash, raw_html, clean_text, last_modified))
                is_new_or_updated = True
            elif row["content_hash"] != content_hash or row["status"] != "active":
                cursor.execute("""
                UPDATE articles SET title = ?, category = ?, folder = ?, content_hash = ?, 
                                    raw_html = ?, clean_text = ?, status = 'active', 
                                    last_crawled = CURRENT_TIMESTAMP, last_modified = ?
                WHERE url = ?
                """, (title, category, folder, content_hash, raw_html, clean_text, last_modified, url))
                is_new_or_updated = True
            
            conn.commit()
            return is_new_or_updated

    def deactivate_article(self, url: str):
        """Soft-deletes/deactivates an article removed from sitemap."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE articles SET status = 'deactivated' WHERE url = ?", (url,))
            cursor.execute("UPDATE crawler_manifest SET status = 'deactivated' WHERE url = ?", (url,))
            conn.commit()

    def store_chunks(self, article_url: str, chunks: List[Dict[str, Any]]):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            # Remove previous chunks for this article
            cursor.execute("DELETE FROM article_chunks WHERE article_url = ?", (article_url,))
            for ch in chunks:
                cursor.execute("""
                INSERT INTO article_chunks (chunk_id, article_url, section_heading, text_content, embedding_json, token_count)
                VALUES (?, ?, ?, ?, ?, ?)
                """, (ch["chunk_id"], article_url, ch.get("heading", ""), ch["text"], 
                      json.dumps(ch["embedding"]), ch.get("token_count", 0)))
            conn.commit()

    def store_image(self, article_url: str, image_url: str, alt_text: str, vision_desc: str, ui_elements: List[str], uncertainty: float = 0.0):
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT OR REPLACE INTO article_images (image_url, article_url, alt_text, vision_description, ui_elements_json, uncertainty_score)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (image_url, article_url, alt_text, vision_desc, json.dumps(ui_elements), uncertainty))
            conn.commit()

    def get_all_active_chunks(self) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT c.chunk_id, c.article_url, c.section_heading, c.text_content, c.embedding_json, a.title, a.category, a.folder
            FROM article_chunks c
            JOIN articles a ON c.article_url = a.url
            WHERE a.status = 'active'
            """)
            rows = cursor.fetchall()
            results = []
            for r in rows:
                results.append({
                    "chunk_id": r["chunk_id"],
                    "article_url": r["article_url"],
                    "section_heading": r["section_heading"],
                    "text_content": r["text_content"],
                    "embedding": json.loads(r["embedding_json"]),
                    "title": r["title"],
                    "category": r["category"],
                    "folder": r["folder"]
                })
            return results

    def get_images_for_article(self, article_url: str) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            SELECT image_url, alt_text, vision_description, ui_elements_json, uncertainty_score
            FROM article_images WHERE article_url = ?
            """, (article_url,))
            rows = cursor.fetchall()
            return [{
                "image_url": r["image_url"],
                "alt_text": r["alt_text"],
                "vision_description": r["vision_description"],
                "ui_elements": json.loads(r["ui_elements_json"]) if r["ui_elements_json"] else [],
                "uncertainty_score": r["uncertainty_score"]
            } for r in rows]

    # Escalations
    def create_escalation(self, question: str, context: Optional[str] = None, user_id: Optional[str] = None, reason: str = "insufficient_evidence") -> int:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO escalations (question, context, user_id, reason, status)
            VALUES (?, ?, ?, ?, 'open')
            """, (question, context, user_id, reason))
            conn.commit()
            return cursor.lastrowid

    def resolve_escalation(self, escalation_id: int, expert_answer: str) -> bool:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
            UPDATE escalations
            SET expert_answer = ?, status = 'resolved', resolved_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """, (expert_answer, escalation_id))
            conn.commit()
            return cursor.rowcount > 0

    def get_escalations(self, status: Optional[str] = None) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            if status:
                cursor.execute("SELECT * FROM escalations WHERE status = ? ORDER BY id DESC", (status,))
            else:
                cursor.execute("SELECT * FROM escalations ORDER BY id DESC")
            rows = cursor.fetchall()
            return [dict(r) for r in rows]

    def get_counts(self) -> Dict[str, int]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM articles WHERE status = 'active'")
            active_articles = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM article_chunks")
            total_chunks = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM escalations WHERE status = 'open'")
            open_escalations = cursor.fetchone()[0]
            return {
                "active_articles": active_articles,
                "total_chunks": total_chunks,
                "open_escalations": open_escalations
            }

db = Database()
