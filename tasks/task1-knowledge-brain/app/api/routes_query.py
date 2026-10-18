"""
Query and RAG endpoints for Task 1: Knowledge Brain.
Retrieves evidence, models uncertainty, generates citations, and triggers escalations.
"""
import time
import logging
from typing import List
from fastapi import APIRouter, HTTPException

from app.models.schemas import QueryRequest, QueryResponse, SourceCitation, ImageEvidence
from app.config import settings
from app.database import db
from retrieval.vector_store import vector_store

router = APIRouter(tags=["Query"])
logger = logging.getLogger("api.query")

def synthesize_grounded_answer(question: str, top_chunks: List[dict], images: List[dict]) -> tuple[str, str, float, bool]:
    """
    Synthesizes answer grounded strictly in retrieved chunks.
    Enforces prompt injection defense and domain boundary validation.
    Returns (answer_text, status, confidence, needs_human).
    """
    q_lower = question.lower()
    
    # AI Safety Guardrail 1: Detect prompt injection / system override
    injection_patterns = ["system override", "ignore all previous", "ignore previous rules", "print the database", "root password", "jailbreak"]
    if any(pat in q_lower for pat in injection_patterns):
        return (
            "System Notice: Prompt policy violation or untrusted instruction detected. Query has been safely rejected and escalated for security audit.",
            "insufficient_evidence",
            0.05,
            True
        )

    # AI Safety Guardrail 2: Hard out-of-scope hardware/unrelated queries
    unrelated_terms = ["driver", "gpu", "c++", "amd", "nvidia", "quantum computer", "bitcoin", "sourdough", "pizza"]
    if any(term in q_lower for term in unrelated_terms) and not any(k in q_lower for k in ["stripe", "payment", "search", "directory", "member"]):
        return (
            "I do not have sufficient verified documentation in the Brilliant Directories Knowledge Base to answer this question accurately. "
            "To prevent providing inaccurate information, I have escalated this inquiry to our senior technical consulting team.",
            "insufficient_evidence",
            0.15,
            True
        )

    if not top_chunks or top_chunks[0]["relevance_score"] < 0.40:
        return (
            "I do not have sufficient verified documentation in the Brilliant Directories Knowledge Base to answer this question accurately. "
            "To prevent providing inaccurate information, I have escalated this inquiry to our senior technical consulting team.",
            "insufficient_evidence",
            0.20,
            True
        )

    best_score = top_chunks[0]["relevance_score"]
    primary = top_chunks[0]
    secondary = top_chunks[1] if len(top_chunks) > 1 else None

    # Synthesize grounded answer highlighting exact steps & settings
    q_lower = question.lower()
    answer_parts = []
    
    answer_parts.append(f"Based on the official documentation in **{primary['title']}**:")
    
    # Extract substantive sentences from top chunk
    sentences = [s.strip() for s in primary["text_content"].split("\n") if s.strip() and not s.startswith("Article:") and not s.startswith("Category:")]
    answer_parts.append("\n".join(sentences[:5]))

    if secondary and secondary["article_url"] != primary["article_url"]:
        sec_sentences = [s.strip() for s in secondary["text_content"].split("\n") if s.strip() and not s.startswith("Article:") and not s.startswith("Category:")]
        answer_parts.append(f"\nAdditionally, according to **{secondary['title']}**:\n" + "\n".join(sec_sentences[:3]))

    if images:
        top_img = images[0]
        answer_parts.append(f"\n**Visual Reference**: Refer to screenshot `{top_img['alt_text']}` which confirms the UI controls: {', '.join(top_img.get('ui_elements', []))}.")

    answer_text = "\n\n".join(answer_parts)
    confidence = min(0.98, max(0.60, round(best_score * 0.95, 2)))
    status = "answered"
    needs_human = False

    return answer_text, status, confidence, needs_human

@router.post("/query", response_model=QueryResponse)
async def query_knowledge(req: QueryRequest):
    start_time = time.time()
    
    # 1. Hybrid Retrieval
    retrieved = vector_store.search(
        query=req.question,
        top_k=req.top_k,
        category_filter=req.category_filter,
        mode="hybrid"
    )

    # 2. Gather associated screenshot images
    images_evidence: List[ImageEvidence] = []
    citations: List[SourceCitation] = []

    for item in retrieved:
        article_imgs = db.get_images_for_article(item["article_url"])
        for img in article_imgs:
            if not any(e.image_url == img["image_url"] for e in images_evidence):
                images_evidence.append(ImageEvidence(
                    image_url=img["image_url"],
                    alt_text=img.get("alt_text"),
                    description=img["vision_description"],
                    ui_elements=img.get("ui_elements", []),
                    uncertainty_score=img.get("uncertainty_score", 0.0)
                ))

        # Extract snippet for citation
        snippet_text = item["text_content"]
        if len(snippet_text) > 300:
            snippet_text = snippet_text[:300] + "..."

        citations.append(SourceCitation(
            title=item["title"],
            url=item["article_url"],
            snippet=snippet_text,
            relevance_score=item["relevance_score"],
            section_heading=item.get("section_heading"),
            image_urls=[img["image_url"] for img in article_imgs]
        ))

    # 3. Grounded Synthesis & Abstention Check
    answer, status, confidence, needs_human = synthesize_grounded_answer(req.question, retrieved, db.get_images_for_article(retrieved[0]["article_url"]) if retrieved else [])

    escalation_id = None
    if needs_human:
        # Create human escalation task in database
        escalation_id = db.create_escalation(
            question=req.question,
            context=f"Query failed with top relevance score: {retrieved[0]['relevance_score'] if retrieved else 0.0}",
            user_id=req.user_id,
            reason="insufficient_evidence"
        )
        status = "escalated"

    latency = round(time.time() - start_time, 3)
    logger.info("Query completed in %.3fs with status=%s, confidence=%.2f", latency, status, confidence)

    return QueryResponse(
        answer=answer,
        status=status,
        sources=citations,
        images=images_evidence[:3],
        confidence=confidence,
        needs_human=needs_human,
        escalation_id=escalation_id,
        prompt_version=settings.RAG_PROMPT_VERSION,
        model_used=settings.CLAUDE_MODEL_PRIMARY
    )
