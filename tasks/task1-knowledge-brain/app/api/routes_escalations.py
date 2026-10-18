"""
Human Expert Escalation & Knowledge Loop routes for Task 1: Knowledge Brain.
"""
from typing import List, Optional
from fastapi import APIRouter, HTTPException
from app.models.schemas import EscalationRequest, EscalationResolveRequest, EscalationResponse
from app.database import db
from retrieval.chunker import chunker
from retrieval.embedder import embedder

router = APIRouter(prefix="/escalations", tags=["Escalations"])

@router.post("", response_model=dict)
async def create_escalation(req: EscalationRequest):
    escalation_id = db.create_escalation(
        question=req.question,
        context=req.context,
        user_id=req.user_id,
        reason=req.reason
    )
    return {
        "status": "created",
        "escalation_id": escalation_id,
        "message": "Escalation logged for senior tech consultant review"
    }

@router.get("", response_model=List[EscalationResponse])
async def list_escalations(status: Optional[str] = None):
    rows = db.get_escalations(status=status)
    return [
        EscalationResponse(
            id=r["id"],
            question=r["question"],
            context=r.get("context"),
            reason=r["reason"],
            status=r["status"],
            expert_answer=r.get("expert_answer"),
            created_at=str(r["created_at"]),
            resolved_at=str(r.get("resolved_at")) if r.get("resolved_at") else None
        )
        for r in rows
    ]

@router.post("/{escalation_id}/resolve", response_model=dict)
async def resolve_escalation(escalation_id: int, req: EscalationResolveRequest):
    """
    Saves approved human expert answer and feeds it back into the Knowledge Brain vector store
    so the system evolves and answers the question in all future queries.
    """
    success = db.resolve_escalation(escalation_id, req.expert_answer)
    if not success:
        raise HTTPException(status_code=404, detail="Escalation ID not found")

    # Fetch escalation to retrieve original question
    all_esc = db.get_escalations()
    target = next((e for e in all_esc if e["id"] == escalation_id), None)
    question = target["question"] if target else f"Inquiry #{escalation_id}"

    # Self-Evolving Knowledge Loop: Create a verified solution article in the database
    new_url = f"https://support.brilliantdirectories.com/expert-verified/solution-{escalation_id}"
    article_title = f"Expert Resolution: {question}"
    clean_text = f"## Overview\nVerified solution provided by {req.expert_name}.\n\n## Solution Details\n{req.expert_answer}"

    db.upsert_article(
        url=new_url,
        title=article_title,
        category=req.category or "Expert Solutions",
        folder="Verified Knowledge",
        content_hash=f"expert_{escalation_id}",
        raw_html=f"<html><body><h1>{article_title}</h1><p>{req.expert_answer}</p></body></html>",
        clean_text=clean_text
    )

    # Chunk and embed immediately into vector store
    article_dict = {
        "url": new_url,
        "title": article_title,
        "category": req.category or "Expert Solutions",
        "folder": "Verified Knowledge",
        "clean_text": clean_text,
        "sections": [{"heading": "Solution Details", "content": req.expert_answer}]
    }
    chunks = chunker.chunk_article(article_dict)
    for ch in chunks:
        ch["embedding"] = embedder.embed_text(ch["text"])
    db.store_chunks(new_url, chunks)

    return {
        "status": "resolved",
        "escalation_id": escalation_id,
        "knowledge_article_url": new_url,
        "chunks_indexed": len(chunks),
        "message": "Expert answer successfully verified and integrated into Knowledge Brain vector memory."
    }
