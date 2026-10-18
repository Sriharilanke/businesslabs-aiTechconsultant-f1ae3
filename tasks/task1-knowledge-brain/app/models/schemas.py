"""
Pydantic schemas and contracts for Task 1 Knowledge Brain API.
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class SourceCitation(BaseModel):
    title: str = Field(..., description="Article title")
    url: str = Field(..., description="Canonical article URL")
    snippet: str = Field(..., description="Verbatim evidence snippet supporting the answer")
    relevance_score: float = Field(..., description="Combined hybrid retrieval score [0.0 - 1.0]")
    section_heading: Optional[str] = Field(None, description="H2/H3 section heading from article")
    image_urls: List[str] = Field(default_factory=list, description="Associated screenshot URLs")

class ImageEvidence(BaseModel):
    image_url: str = Field(..., description="Direct URL or path to UI screenshot")
    alt_text: Optional[str] = Field(None, description="Image alt text")
    description: str = Field(..., description="Vision analysis description of UI layout and settings")
    ui_elements: List[str] = Field(default_factory=list, description="Extracted UI controls (buttons, toggles, inputs)")
    uncertainty_score: float = Field(0.0, description="Vision model uncertainty score [0.0 = certain, 1.0 = ambiguous]")

class QueryRequest(BaseModel):
    question: str = Field(..., min_length=2, description="Customer or consultant question about product features")
    top_k: int = Field(5, ge=1, le=15, description="Number of source chunks to retrieve")
    category_filter: Optional[str] = Field(None, description="Optional category filter")
    user_id: Optional[str] = Field(None, description="Identifier for client or agent making query")

class QueryResponse(BaseModel):
    answer: str = Field(..., description="Grounded answer synthesized from evidence")
    status: str = Field(..., description="'answered' | 'insufficient_evidence' | 'escalated'")
    sources: List[SourceCitation] = Field(default_factory=list, description="Source citations")
    images: List[ImageEvidence] = Field(default_factory=list, description="Relevant screenshots & UI details")
    confidence: float = Field(..., description="Calibrated confidence score [0.0 - 1.0]")
    needs_human: bool = Field(False, description="True if answer is uncertain or evidence is absent")
    escalation_id: Optional[int] = Field(None, description="ID of created escalation task if triggered")
    prompt_version: str = Field("v1.2.0-grounded-citations", description="Version of RAG prompt used")
    model_used: str = Field("claude-3-5-sonnet", description="Model used for synthesis")

class IngestionRequest(BaseModel):
    mode: str = Field("sample", description="'sample' (15 pages), 'incremental' (sitemap diff), or 'full'")
    max_pages: Optional[int] = Field(15, ge=1, le=500, description="Max pages to crawl in this batch")
    urls: Optional[List[str]] = Field(None, description="Explicit list of URLs to crawl")

class IngestionStatus(BaseModel):
    job_id: str
    status: str = Field("idle", description="'idle' | 'running' | 'completed' | 'failed'")
    total_discovered: int = 0
    pages_processed: int = 0
    pages_failed: int = 0
    pages_new: int = 0
    pages_updated: int = 0
    pages_deactivated: int = 0
    last_run_timestamp: Optional[str] = None
    active_articles_count: int = 0
    total_chunks_count: int = 0
    message: Optional[str] = None

class EscalationRequest(BaseModel):
    question: str = Field(..., description="Unanswered question")
    context: Optional[str] = Field(None, description="Context from conversation or query attempt")
    user_id: Optional[str] = Field(None, description="Identifier for requester")
    reason: str = Field("insufficient_evidence", description="Reason for escalation")

class EscalationResolveRequest(BaseModel):
    expert_answer: str = Field(..., min_length=10, description="Verified human answer")
    expert_name: str = Field("Lead Tech Consultant", description="Name of resolving expert")
    category: Optional[str] = Field("General", description="Category for the new knowledge entry")

class EscalationResponse(BaseModel):
    id: int
    question: str
    context: Optional[str] = None
    reason: str
    status: str
    expert_answer: Optional[str] = None
    created_at: str
    resolved_at: Optional[str] = None

class HealthResponse(BaseModel):
    status: str
    service: str
    version: str
    active_articles: int
    total_chunks: int
    open_escalations: int
    uptime_seconds: float
