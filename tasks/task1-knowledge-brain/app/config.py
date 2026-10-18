"""
Configuration settings for Task 1: Knowledge Brain Service.
"""
import os
from pathlib import Path
from pydantic import BaseModel

BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseModel):
    PROJECT_NAME: str = "AI Tech Consultant - Knowledge Brain"
    VERSION: str = "1.0.0"
    API_PORT: int = int(os.getenv("TASK1_PORT", "8001"))
    HOST: str = "0.0.0.0"
    
    # Database
    DATABASE_PATH: str = os.getenv("TASK1_DB_PATH", str(BASE_DIR / "knowledge_brain.db"))
    
    # Crawler settings
    SITEMAP_URL: str = "https://support.brilliantdirectories.com/support/sitemap.xml"
    CRAWL_MAX_CONCURRENCY: int = int(os.getenv("CRAWL_CONCURRENCY", "3"))
    CRAWL_DELAY_SECONDS: float = float(os.getenv("CRAWL_DELAY", "0.5"))
    CRAWL_MAX_RETRIES: int = 3
    CRAWL_TIMEOUT_SECONDS: float = 15.0
    
    # Retrieval & RAG
    EMBEDDING_DIMENSION: int = 384
    RETRIEVAL_TOP_K: int = 5
    SIMILARITY_THRESHOLD: float = 0.55
    HYBRID_ALPHA: float = 0.6  # 0.6 vector + 0.4 BM25
    
    # LLM Settings
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    CLAUDE_MODEL_PRIMARY: str = os.getenv("CLAUDE_MODEL", "claude-3-5-sonnet-20241022")
    CLAUDE_MODEL_FAST: str = "claude-3-5-haiku-20241022"
    
    # System Prompt versioning
    RAG_PROMPT_VERSION: str = "v1.2.0-grounded-citations"

settings = Settings()
